from binascii import b2a_base64
from csv import excel
import pandas as pd
from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
import re
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
from gpl_audit_tool_V1_1.extractors.command_extractor import CommandExtractor
from gpl_audit_tool_V1_1.extractors.table_extractor import TableExtractor
from gpl_audit_tool_V1_1.thread_pool import ThreadPool
from concurrent.futures import ThreadPoolExecutor




def format_excel_sheet(writer, sheet_name, df, startrow=0, startcol=0):
    """Apply formatting to an Excel sheet with adjustable start positions."""
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    header_format = workbook.add_format(
        {
            "bold": True,
            "bg_color": "#000957",
            "border": 2,
            "font_color": "#ffffff",
            "align": "center",
            "valign": "vcenter",
        }
    )
    center_format = workbook.add_format(
        {
            "align": "center",
            "valign": "center",
            "border": 1,
            "border_color": "#000000",
            "bold": True,
        }
    )
    ok_format = workbook.add_format(
        {
            "bg_color": "#90EE90",
            "font_color": "#000000",
            "align": "center",
            "valign": "center",
        }
    )
    not_ok_format = workbook.add_format(
        {
            "bg_color": "#FF0000",
            "font_color": "#FFFFFF",
            "align": "center",
            "valign": "center",
        }
    )

    worksheet.set_row(startrow, 23)

    for col_num, col_name in enumerate(df.columns):
        worksheet.write(startrow, startcol + col_num, str(col_name), header_format)

        column_series = df[col_name]
        if isinstance(column_series, pd.DataFrame):
            column_series = column_series.iloc[:, 0]

        max_length = max(
            column_series.astype(str).fillna("").str.len().max(skipna=True) or 0,
            len(str(col_name)),
        )
        max_length = min(max_length, 255)
        worksheet.set_column(startcol + col_num, startcol + col_num, max_length + 5)

    for row_num in range(len(df)):
        worksheet.set_row(startrow + row_num + 1, 15)

        for col_num in range(len(df.columns)):
            cell_value = str(df.iloc[row_num, col_num])
            format_style = center_format
            if cell_value == "OK":
                format_style = ok_format
            elif cell_value == "NOT OK":
                format_style = not_ok_format
            elif cell_value == "Missing" or cell_value=="Missing in Post":
                format_style = workbook.add_format(
                    {
                        "bg_color": "#FF6347",
                        "font_color": "#FFFFFF",
                        "align": "center",
                        "valign": "center",
                    }
                )
            elif cell_value == "NA":
                format_style = workbook.add_format(
                    {
                        "bg_color": "#FCF259",
                        "font_color": "#222831",
                        "align": "center",
                        "valign": "center",
                    }
                )
            elif "|" in cell_value:
                format_style = workbook.add_format(
                    {
                        "font_color": "#FF0000",
                        "align": "center",
                        "valign": "center",
                        "bold": True,
                        "border": 1,
                        "border_color": "#000000",
                    }
                )

            worksheet.write(
                startrow + row_num + 1, startcol + col_num, cell_value, format_style
            )



# Create your views here.
def get_commands(command_lines):
    pool = ThreadPool()
    result = {}

    tasks = [
        (
            r"#+Start:\senbinfo\sAudit\s#+",
            r"#+\sEND\sof\senbinfo\sAudit\s#+",
            "enbinfo",
        ),
        (r"#+Start:\sCELL\sDATA\s#+", r"#+\sEND\sOF\sCELL\sDATA\s#+", "cell_data"),
        (
            r"#+Start:\sLTE\sGPL\sAudit\s#+",
            r"#####END of LTE GPL Audit #######",
            "gpl-para",
        ),
        (
            r"#+Start:\sFeatureState\sAudit\s#+",
            r"#+\sEND\sof\sFeatureState\sAudit\s#+",
            "FeatureState",
        ),
        (
            r"#+Start:\sEutranfrequency\sAudit\s#+",
            r"#+\sEND\sof\sEutranfrequency\sAudit\s#+",
            "Eutranfrequency",
        ),
        (
            r"#+Start:\sEutranfreqRelation\sAudit\s#+",
            r"#+\sEND\sof\sEutranfreqRelation\sAudit\s#+",
            "EutranfreqRelation",
        ),
        (
            r"#####Start:\s*CellRelation\s+Audit\s*#+",
            r"#####\s*END\s+of\s+CellRelation\s+Audit\s*#+",
            "CellRelation",
        ),
        (
            r"#####Start:\sGeranFreqRelation\sAudit\s#######",
            r"#####\sEND\sof\sGeranFreqRelation\sAudit\s#######",
            "GeranFreqRelation",
        ),
    ]

    for start, end, key in tasks:
        pool.submit_task(
            CommandExtractor.extract_command, command_lines, start, end, result, key
        )

    pool.wait_for_completion()

    return result


def process_files(file, log_path, result):
    with open(log_path, 'r') as f:
        log_lines = [line.strip() for line in f.readlines()]
    extractor = TableExtractor(log_lines)
    return file, extract_tables(extractor, result)


def extract_tables(extractor, result):
    dataframes = {}
    for key, commands in result.items():
        dataframes[key] = {}
        temp_dfs = []
        for command in commands:
            table = extractor.extract_table(command)
            node_id = extractor.get_nodeID() or "UNKNOWN_NODE"
            if table:
                headers = [col.strip() for col in table[0].split(";")]
                max_cols = len(headers)
                data = [str(row).split(";") for row in table[1:]]
                data = [[i.strip() for i in val] for val in data]
                data = [
                    (
                        row + [""] * (max_cols - len(row))
                        if len(row) < max_cols
                        else row[:max_cols]
                    )
                    for row in data
                ]
                df = pd.DataFrame(data, columns=headers)

                if key == "gpl-para":
                    df = df.melt(
                        id_vars=["MO"] if "MO" in df.columns else [],
                        var_name="Parameter",
                        value_name="Value",
                    )

                    df["Value"] = (
                        df["Value"]
                        .apply(lambda x: str(x).split(" ")[0] if " " in x else x)
                        .astype(str)
                    )

                df.insert(0, "Node_ID", [node_id] * len(df))
                temp_dfs.append(df)

        if temp_dfs:
            merged_df = pd.concat(temp_dfs, axis=0, ignore_index=False)
            if key == "cell_data":
                merged_df = pd.concat(
                    temp_dfs,
                    axis=1,
                    ignore_index=False,
                    keys=["left", "right"],
                )
                merged_df.columns = merged_df.columns.map(
                    lambda x: f"{x[0]}_{x[1]}" if isinstance(x, tuple) else x
                )
            dataframes[key] = merged_df
    return dataframes





@api_view(['POST'])
def get_log_parser(request):
    ########################################################## getting log files from the frontend ########################################
    log_files = request.FILES.getlist('log_files')


    baseURL = os.path.join(MEDIA_ROOT, '4G_5G_GPL_AUDIT')
    current_time = datetime.now().strftime("%Y%M%D_%H%M%S")
    ############################################################### getting commands from the log files ##################################################
    command_file_path = os.path.join(baseURL, 'command_file', 'GPL_Audit_command_updated.txt')
    with open(command_file_path, 'r') as command_file:
        command_lines = [line.strip() for line in command_file.readlines()]
    ######################################################################################################################################################
    results = get_commands(command_lines)

    if not os.path.exists(baseURL):
        os.makedirs(baseURL, exist_ok=True, mode=0o777)

    log_folder = os.path.join(baseURL, 'log_input_control', f"logs_{current_time}")
    if not os.path.exists(log_folder):
        os.makedirs(log_folder, exist_ok=True, mode=0o777)

    ############################################################# saved log files on the folder ##########################################
    saved_files = []

    for file in log_files:
        file_path = os.path.join(log_folder, file.name)
        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        saved_files.append(file_path)

    ############################################################ getting the node list ###################################################
    node_list = []

    for file in saved_files:
        if not (file.endswith('.log') or file.endswith('.txt')):
            return Response({"error": "All files must be .log files or .txt files."}, status=status.HTTP_400_BAD_REQUEST)
        
        with open(file, 'r') as f:
            file_content = f.read()
            
        
        regex_pattern = "ManagedElement=([\w-]+)"

        match = re.search(regex_pattern, file_content)

        if match:
            node = match.group(1)
            node_list.append({
                f"node" : node,
                f"file_path": file
            })
        else:
            print("No match found.")

    ################################################## iterating the node and file path items persent in the node list ##################################################
    for item in node_list:
        node = item.get('node')
        file_path = item.get('file_path')

        all_dfs = {"Summary": []} | {key: [] for key in results.keys()}

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(process_files, file, file_path, results): file
                for file in saved_files
            }

            for future in futures:
                file, df_dict = future.result()
                for key, df in df_dict.items():
                    all_dfs[key].append(df)
        
        ####################################################### Constants for cell types #######################################################
        FDD_PREFIX = "EUtranCellFDD="
        TDD_PREFIX = "EUtranCellTDD="

        # Column configuration
        COLUMN_CONFIG = {
            "renames": {
                "left_channelBandwidth": "left_dlChannelBandwidth",
                "left_earfcn": "left_earfcndl",
            },
            "shift_columns": {"start": "left_earfcnul", "end": "left_userLabel"},
        }

        def process_fdd_cells(df: pd.DataFrame) -> pd.DataFrame:
            """Process FDD cells by adding earfcnul and removing right_Node_ID"""
            df["left_earfcnul"] = None
            if "right_Node_ID" in df.columns:
                df.drop(columns=["right_Node_ID"], inplace=True)
            return df

        def process_tdd_cells(df: pd.DataFrame) -> pd.DataFrame:
            """Process TDD cells by shifting columns and updating values"""
            try:
                start_idx = df.columns.get_loc(COLUMN_CONFIG["shift_columns"]["start"])
                end_idx = df.columns.get_loc(COLUMN_CONFIG["shift_columns"]["end"])

                # Shift columns
                df.iloc[:, start_idx + 1 : end_idx + 1] = df.iloc[
                    :, start_idx:end_idx
                ].to_numpy()
                df.loc[:, COLUMN_CONFIG["shift_columns"]["start"]] = ""
                df["left_userLabel"] = df["left_ulChannelBandwidth"]
                df["left_ulChannelBandwidth"] = ""
            except Exception as e:
                print(f"Error processing TDD cells: {e}")
            return df

        ############################################################ Process each DataFrame in cell_data ##########################################################
        for i, mo_df in enumerate(all_dfs["cell_data"]):
            # Standardize column names
            mo_df.rename(columns=COLUMN_CONFIG["renames"], inplace=True)
            mo_df.drop(columns=["right_Node_ID"], inplace=True)

            # Skip if required column is missing
            if "left_MO" not in mo_df.columns:
                continue

            # Identify cell types
            is_fdd = mo_df["left_MO"].astype(str).str.startswith(FDD_PREFIX)
            is_tdd = mo_df["left_MO"].astype(str).str.startswith(TDD_PREFIX)

            # Case 1: Pure FDD or no TDD cells
            if not is_tdd.any():
                all_dfs["cell_data"][i] = process_fdd_cells(mo_df)
                continue

            # Case 2: Mixed FDD and TDD cells
            df_fdd = mo_df[is_fdd].copy()
            df_tdd = mo_df[is_tdd].copy()

            # Process TDD cells if they exist
            if not df_tdd.empty:
                df_tdd = process_tdd_cells(df_tdd)

            # Combine FDD and TDD data
            all_dfs["cell_data"][i] = pd.concat([df_fdd, df_tdd], ignore_index=True)

        # Final cleanup: reorder FDD and TDD cells
        for i, mo_df in enumerate(all_dfs["cell_data"]):
            if "left_MO" in mo_df.columns:
                tdd_df = mo_df[mo_df["left_MO"].astype(str).str.startswith(TDD_PREFIX)]
                fdd_df = mo_df[mo_df["left_MO"].astype(str).str.startswith(FDD_PREFIX)]
                all_dfs["cell_data"][i] = pd.concat(
                    [tdd_df, fdd_df], axis=0, ignore_index=True
                )

        # Merge all DataFrames
        all_merged_df = {
            key: pd.concat(dfs, ignore_index=False, axis=0) if dfs else pd.DataFrame()
            for key, dfs in all_dfs.items()
        }
        excel_path = os.path.join(baseURL,f"parsed_files_{current_time}", f"{node}_GPL_PARSED_DUMP_{current_time}.xlsx")
        if not os.path.exists(os.path.dirname(excel_path)):
            os.makedirs(os.path.dirname(excel_path), exist_ok=True, mode=0o777)
        ############################################################### saving the excel file ##########################################################
        with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
            workbook = writer.book
            for sheet_name, df in all_merged_df.items():
                if sheet_name == "cell_data":
                    print(df.columns)
                    summary_df = df[["left_Node_ID", "left_MO", "left_cellId"]].copy()
                    summary_df.rename(
                        columns={
                            "left_Node_ID": "Pre SiteId",
                            "left_MO": "Pre CellName",
                            "left_cellId": "cellId",
                        },
                        inplace=True,
                    )
                    ########################################################################## ADDING PRE ENBID ########################################################

                    enodeid_mapping = {
                        row["Node_ID"]: row["eNBId"]
                        for _, row in all_merged_df["enbinfo"].iterrows()
                    }
                    print(enodeid_mapping)

                    summary_df["Pre eNBID"] = summary_df["Pre SiteId"].apply(
                        lambda x: enodeid_mapping[x]
                    )
                    summary_df.insert(2, "Pre eNBID", summary_df.pop("Pre eNBID"))

                    df.columns = [
                        (
                            col.replace("left_", "")
                            if col.startswith("left_")
                            else col.replace("right_", "")
                        )
                        for col in df.columns
                    ]

                elif sheet_name == "gpl-para":
                    df.rename(columns={"Value": "Current value"}, inplace=True)

                    columns_to_add = [
                        "Pre-existing Value",
                        "Parameter Setting Status",
                        "Band",
                    ]

                    for col in columns_to_add:
                        df[col] = ""

                elif sheet_name == "FeatureState":
                    df["featureState"] = df["featureState"].apply(
                        lambda x: str(x).split(" ")[0] if " " in x else x
                    )
                    df["licenseState"] = df["licenseState"].apply(
                        lambda x: str(x).split(" ")[0] if " " in x else x
                    )
                    df.rename(
                        columns={
                            "MO": "CXC ID",
                            "featureState": "Current FeatureState",
                            "licenseState": "Current LicenseState",
                        },
                        inplace=True,
                    )

                    columns_to_add = [
                        "Pre Existing FeatureState",
                        "Pre Existing LicenseState",
                        "Feature setting Status",
                    ]
                    for col in columns_to_add:
                        df[col] = ""

                df.to_excel(writer, sheet_name=sheet_name, index=False)
                format_excel_sheet(writer, sheet_name, df)

            if not summary_df.empty:
                summary_df["Post SiteId"] = ""

                summary_df["Post CellName"] = ""

                summary_df.to_excel(writer, sheet_name="Summary", index=False)
                format_excel_sheet(writer, "Summary", summary_df)


    return Response(
        {
            "message": f" data is sucesfully feteched...",
            "download_url": os.path.join(MEDIA_ROOT, excel_path),
        },
        status=status.HTTP_200_OK,
    )