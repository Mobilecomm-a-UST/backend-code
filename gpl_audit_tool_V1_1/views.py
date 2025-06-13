
import os
import re
from csv import excel
import pandas as pd
from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
from gpl_audit_tool_V1_1.extractors.command_extractor import CommandExtractor
from gpl_audit_tool_V1_1.extractors.table_extractor import TableExtractor
from gpl_audit_tool_V1_1.thread_pool import ThreadPool
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from django.conf import settings




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
    log_files = request.FILES.getlist('log_files')
    baseURL = os.path.join(settings.MEDIA_ROOT, '4G_5G_GPL_AUDIT')
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    ################################################################## Create datetime-based folder ###########################################
    output_folder = os.path.join(baseURL, 'parsed_dumps',f"parsed_files_{current_time}")
    os.makedirs(output_folder, exist_ok=True, mode=0o777)

    #################################################################### Load command list ######################################################
    command_file_path = os.path.join(baseURL, 'command_file', 'GPL_Audit_command_updated.txt')
    with open(command_file_path, 'r') as command_file:
        command_lines = [line.strip() for line in command_file.readlines()]
    results = get_commands(command_lines)

    ############################################################# Save log files to disk ########################################################
    log_input_folder = os.path.join(baseURL, f"log_input_control/logs_{current_time}")
    os.makedirs(log_input_folder, exist_ok=True, mode=0o777)

    saved_files = []
    for file in log_files:
        file_path = os.path.join(log_input_folder, file.name)
        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        saved_files.append(file_path)

    ################################################# Extract node names from files #################################################################
    node_list = []
    for file in saved_files:
        if not (file.endswith('.log') or file.endswith('.txt')):
            return Response({"error": "All files must be .log or .txt files."}, status=status.HTTP_400_BAD_REQUEST)

        with open(file, 'r') as f:
            content = f.read()

        match = re.search(r"ManagedElement=([\w-]+)", content)
        if match:
            node = match.group(1)
            node_list.append({"node": node, "file_path": file})
        else:
            print("No node match found in:", file)

    all_download_urls = []

    ################################################### Process each node separately ###########################################################
    for item in node_list:
        node = item["node"]
        file_path = item["file_path"]

        all_dfs = defaultdict(list)
        all_dfs["Summary"] = []

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(process_files, file_path, file_path, results): file_path
                for file_path in saved_files
            }
            for future in futures:
                file, df_dict = future.result()
                for key, df in df_dict.items():
                    all_dfs[key].append(df)

        ################################################ FDD/TDD processing #####################################################################
        FDD_PREFIX = "EUtranCellFDD="
        TDD_PREFIX = "EUtranCellTDD="
        COLUMN_CONFIG = {
            "renames": {
                "left_channelBandwidth": "left_dlChannelBandwidth",
                "left_earfcn": "left_earfcndl",
            },
            "shift_columns": {"start": "left_earfcnul", "end": "left_userLabel"},
        }

        def process_fdd_cells(df):
            df["left_earfcnul"] = None
            df.drop(columns=["right_Node_ID"], errors='ignore', inplace=True)
            return df

        def process_tdd_cells(df):
            try:
                start = df.columns.get_loc(COLUMN_CONFIG["shift_columns"]["start"])
                end = df.columns.get_loc(COLUMN_CONFIG["shift_columns"]["end"])
                df.iloc[:, start+1:end+1] = df.iloc[:, start:end].to_numpy()
                df.iloc[:, start] = ""
                df["left_userLabel"] = df["left_ulChannelBandwidth"]
                df["left_ulChannelBandwidth"] = ""
            except Exception as e:
                print("TDD processing error:", e)
            return df

        for i, mo_df in enumerate(all_dfs["cell_data"]):
            mo_df.rename(columns=COLUMN_CONFIG["renames"], inplace=True)
            mo_df.drop(columns=["right_Node_ID"], errors='ignore', inplace=True)
            if "left_MO" not in mo_df.columns:
                continue
            is_fdd = mo_df["left_MO"].astype(str).str.startswith(FDD_PREFIX)
            is_tdd = mo_df["left_MO"].astype(str).str.startswith(TDD_PREFIX)

            if not is_tdd.any():
                all_dfs["cell_data"][i] = process_fdd_cells(mo_df)
                continue

            df_fdd = mo_df[is_fdd].copy()
            df_tdd = mo_df[is_tdd].copy()
            if not df_tdd.empty:
                df_tdd = process_tdd_cells(df_tdd)
            all_dfs["cell_data"][i] = pd.concat([df_fdd, df_tdd], ignore_index=True)

        for i, mo_df in enumerate(all_dfs["cell_data"]):
            if "left_MO" in mo_df.columns:
                tdd_df = mo_df[mo_df["left_MO"].astype(str).str.startswith(TDD_PREFIX)]
                fdd_df = mo_df[mo_df["left_MO"].astype(str).str.startswith(FDD_PREFIX)]
                all_dfs["cell_data"][i] = pd.concat([tdd_df, fdd_df], ignore_index=True)

        all_merged_df = {
            key: pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
            for key, dfs in all_dfs.items()
        }

        excel_path = os.path.join(output_folder, f"{node}_GPL_PARSED_DUMP_{current_time}.xlsx")
        with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
            workbook = writer.book
            for sheet_name, df in all_merged_df.items():
                if sheet_name == "cell_data":
                    summary_df = df[["left_Node_ID", "left_MO", "left_cellId"]].copy()
                    summary_df.rename(columns={
                        "left_Node_ID": "Pre SiteId",
                        "left_MO": "Pre CellName",
                        "left_cellId": "cellId",
                    }, inplace=True)
                    enbinfo_df = all_merged_df.get("enbinfo", pd.DataFrame())
                    enodeid_map = dict(zip(enbinfo_df["Node_ID"], enbinfo_df["eNBId"])) if not enbinfo_df.empty else {}
                    summary_df["Pre eNBID"] = summary_df["Pre SiteId"].map(enodeid_map)
                    summary_df.insert(2, "Pre eNBID", summary_df.pop("Pre eNBID"))

                    df.columns = [col.replace("left_", "").replace("right_", "") for col in df.columns]

                elif sheet_name == "gpl-para":
                    df.rename(columns={"Value": "Current value"}, inplace=True)


                elif sheet_name == "FeatureState":
                    df["featureState"] = df["featureState"].astype(str).str.split().str[0]
                    df["licenseState"] = df["licenseState"].astype(str).str.split().str[0]
                    df.rename(columns={
                        "MO": "CXC ID",
                        "featureState": "Current FeatureState",
                        "licenseState": "Current LicenseState",
                    }, inplace=True)


                df.to_excel(writer, sheet_name=sheet_name, index=False)
                format_excel_sheet(writer, sheet_name, df)

            if 'summary_df' in locals() and not summary_df.empty:
                summary_df.to_excel(writer, sheet_name="Summary", index=False)
                format_excel_sheet(writer, "Summary", summary_df)

        # Create full download link
        relative_path = os.path.relpath(excel_path, settings.MEDIA_ROOT)
        download_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, relative_path))
        all_download_urls.append(download_url)

    return Response({
        "message": "Data processed successfully.",
        "download_urls": all_download_urls
    }, status=status.HTTP_200_OK)



@api_view(['POST'])
def get_pre_post_audit(request):
    ########################################################## Get pre and post files from frontend ##############################################
    pre_log_files = request.FILES.getlist('pre_log_files')
    post_log_files = request.FILES.getlist('post_log_files')

    ################################################################## Define base folders ####################################################
    base_dir = os.path.join(settings.MEDIA_ROOT, '4G_5G_GPL_AUDIT')
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    session_folder = os.path.join(base_dir, 'GPL_AUDIT_FILES', f"GPL_AUDIT_{current_time}")
    os.makedirs(session_folder, exist_ok=True, mode=0o777)

    ###################################################### Prepare folders to save raw logs #######################################################
    pre_folder = os.path.join(session_folder, 'pre_logs')
    post_folder = os.path.join(session_folder, 'post_logs')
    os.makedirs(pre_folder, exist_ok=True)
    os.makedirs(post_folder, exist_ok=True)

    def save_files(file_list, folder):
        saved_paths = []
        for f in file_list:
            path = os.path.join(folder, f.name)
            with open(path, 'wb+') as dest:
                for chunk in f.chunks():
                    dest.write(chunk)
            saved_paths.append(path)
        return saved_paths
    #################################################################### Load command list ######################################################
    command_file_path = os.path.join(base_dir, 'command_file', 'GPL_Audit_command_updated.txt')
    with open(command_file_path, 'r') as command_file:
        command_lines = [line.strip() for line in command_file.readlines()]
    results = get_commands(command_lines)

    ################################################################## Save both pre and post files ###################################################
    pre_paths = save_files(pre_log_files, pre_folder)
    post_paths = save_files(post_log_files, post_folder)

    def extract_node(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        match = re.search(r"ManagedElement=([\w-]+)", content)
        return match.group(1) if match else None

    ######################################################## Extract node names from files #################################################################
    pre_nodes = {extract_node(p): p for p in pre_paths if extract_node(p)}
    post_nodes = {extract_node(p): p for p in post_paths if extract_node(p)}

    pre_all_dfs, post_all_dfs = defaultdict(list), defaultdict(list)
    pre_all_dfs["Summary"], post_all_dfs["Summary"] = [], []

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(process_files, pre_file, pre_file, results): pre_file
            for pre_file in pre_paths
        }
        for future in futures:
            file, df_dict = future.result()
            for key, df in df_dict.items():
                pre_all_dfs[key].append(df)
        futures = {
            executor.submit(process_files, post_file, post_file, results): post_file
            for post_file in post_paths
        }
        for future in futures:
            file, df_dict = future.result()
            for key, df in df_dict.items():
                post_all_dfs[key].append(df)

    ################################################ FDD/TDD processing #####################################################################
    FDD_PREFIX = "EUtranCellFDD="
    TDD_PREFIX = "EUtranCellTDD="
    COLUMN_CONFIG = {
        "renames": {
            "left_channelBandwidth": "left_dlChannelBandwidth",
            "left_earfcn": "left_earfcndl",
        },
        "shift_columns": {"start": "left_earfcnul", "end": "left_userLabel"},
    }
    def process_fdd_cells(df):
        df["left_earfcnul"] = None
        df.drop(columns=["right_Node_ID"], errors='ignore', inplace=True)
        return df
    def process_tdd_cells(df):
        try:
            start = df.columns.get_loc(COLUMN_CONFIG["shift_columns"]["start"])
            end = df.columns.get_loc(COLUMN_CONFIG["shift_columns"]["end"])
            df.iloc[:, start+1:end+1] = df.iloc[:, start:end].to_numpy()
            df.iloc[:, start] = ""
            df["left_userLabel"] = df["left_ulChannelBandwidth"]
            df["left_ulChannelBandwidth"] = ""
        except Exception as e:
            print("TDD processing error:", e)
        return df
    for i, mo_df in enumerate(pre_all_dfs["cell_data"]):
        mo_df.rename(columns=COLUMN_CONFIG["renames"], inplace=True)
        mo_df.drop(columns=["right_Node_ID"], errors='ignore', inplace=True)
        if "left_MO" not in mo_df.columns:
            continue
        is_fdd = mo_df["left_MO"].astype(str).str.startswith(FDD_PREFIX)
        is_tdd = mo_df["left_MO"].astype(str).str.startswith(TDD_PREFIX)
        if not is_tdd.any():
            pre_all_dfs["cell_data"][i] = process_fdd_cells(mo_df)
            continue
        df_fdd = mo_df[is_fdd].copy()
        df_tdd = mo_df[is_tdd].copy()
        if not df_tdd.empty:
            df_tdd = process_tdd_cells(df_tdd)
        pre_all_dfs["cell_data"][i] = pd.concat([df_fdd, df_tdd], ignore_index=True)
    for i, mo_df in enumerate(post_all_dfs["cell_data"]):
        mo_df.rename(columns=COLUMN_CONFIG["renames"], inplace=True)
        mo_df.drop(columns=["right_Node_ID"], errors='ignore', inplace=True)
        if "left_MO" not in mo_df.columns:
            continue
        is_fdd = mo_df["left_MO"].astype(str).str.startswith(FDD_PREFIX)
        is_tdd = mo_df["left_MO"].astype(str).str.startswith(TDD_PREFIX)
        if not is_tdd.any():
            post_all_dfs["cell_data"][i] = process_fdd_cells(mo_df)
            continue
        df_fdd = mo_df[is_fdd].copy()
        df_tdd = mo_df[is_tdd].copy()
        if not df_tdd.empty:
            df_tdd = process_tdd_cells(df_tdd)
        post_all_dfs["cell_data"][i] = pd.concat([df_fdd, df_tdd], ignore_index=True)

    all_pre_merged_df = {
        key: pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
        for key, dfs in pre_all_dfs.items()
    }
    all_post_merged_df = {
        key: pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
        for key, dfs in post_all_dfs.items()
    }

    ################################################################ Prepare post cell data ###########################################################
    post_cell_id_df = all_post_merged_df["cell_data"][
        ["left_Node_ID", "left_MO", "left_cellId"]
    ].rename(
        columns={
            "left_MO": "Post CellName",
            "left_Node_ID": "Post SiteId",
            "left_cellId": "cellId",
        }
    )
    pre_cell_id_df = all_pre_merged_df["cell_data"][
        ["left_Node_ID", "left_MO", "left_cellId"]
    ].rename(
        columns={
            "left_MO": "Pre CellName",
            "left_Node_ID": "Pre SiteId",
            "left_cellId": "cellId",
        }
    )

    
    ############################################################ mapping eNBId with Site ID ############################################################
    
    pre_enodeid_mapping = {
        row["Node_ID"]: row["eNBId"]
        for _, row in all_pre_merged_df["enbinfo"].iterrows()
    }
    post_enodeid_mapping = {
        row["Node_ID"]: row["eNBId"]
        for _, row in all_post_merged_df["enbinfo"].iterrows()
    }
    
    #####################################################################################################################################################
    
    #------------------------------------------------------------------ Merge pre and post data ---------------------------------------------------------#
    pre_cell_id_df["cellId"] = pre_cell_id_df["cellId"].astype(str)
    post_cell_id_df["cellId"] = post_cell_id_df["cellId"].astype(str)
    all_post_merged_df["Summary"] = pd.merge(
        pre_cell_id_df, post_cell_id_df, on=["cellId"], how="outer"
    ).fillna("NA")

    print("all post merged df:- \n", all_post_merged_df['Summary'])
    
    for idx, row in all_post_merged_df["Summary"].iterrows():
        print(type(row["Pre eNBID"]))
        if type(row["Pre eNBID"]) == float:
            all_post_merged_df["Summary"].at[idx, "Pre eNBID"] = str(
                int(row["Pre eNBID"])
            )

    
    all_post_merged_df["Summary"] = all_post_merged_df["Summary"].sort_values(
        by=["Pre SiteId", "Pre CellName", "cellId"], ascending=True
    )
    
    ##################################################################################### Adding enode id ###############################################
    
    all_post_merged_df["Summary"]["Post eNBID"] = all_post_merged_df["Summary"][
        "Post SiteId"
    ].apply(lambda x: enodeid_mapping[x] if x != "NA" else "NA")
    all_post_merged_df["Summary"].insert(
        5, "Post eNBID", all_post_merged_df["Summary"].pop("Post eNBID")
    )

    gpl_pre_post_file_path = os.path.join(
        session_folder, f"GPL_AUDIT_Parameter_AReport_{current_time}.xlsx"
    )

    with pd.ExcelWriter(gpl_pre_post_file_path, engine="xlsxwriter") as writer:
            workbook = writer.book
            for sheet_name, df in all_post_merged_df.items():
                if sheet_name == "Summary":
                    df.to_excel(
                        writer,
                        sheet_name=sheet_name,
                        startcol=9,
                        startrow=3,
                        index=False,
                    )
                    format_excel_sheet(writer, sheet_name, df, startrow=3, startcol=9)

                elif sheet_name == "gpl-para":


                    def create_cell_mappings(summary_df):
                        # summary_df = summary_df[summary_df['Post SiteId'] != 'NA']
                        return (
                            {
                                row["Pre CellName"]: row["cellId"]
                                for _, row in summary_df.iterrows()
                            },
                            {
                                row["Post CellName"]: row["cellId"]
                                for _, row in summary_df.iterrows()
                            },
                            {
                                row["Pre SiteId"]: row["Post SiteId"]
                                for _, row in summary_df.iterrows() if row['Post SiteId'] != 'NA'
                            },
                        )

                    
                    def add_cell_ids(df: pd.DataFrame, col_name, mapping):
                        df.insert(1, "cellId", df["MO"].apply(lambda x: mapping.get(x.split(",")[0], 0)))
                        return df
                    #####################################################################################################################################
                    cell_id_df = all_post_merged_df["Summary"].sort_values(by="Pre SiteId")
                    gpl_pre_df = all_pre_merged_df.get(sheet_name)
                    gpl_pre_df = gpl_pre_df.assign(
                        **{
                            "Pre-existing Value": gpl_pre_df["Current value"],
                            "Current value": "",
                        }
                    )
                    pre_map, post_map, site_map = create_cell_mappings(cell_id_df)
                    print(pre_map,post_map,site_map)

                    ########################################################merging the datafraems#############################
                    gpl_pre_df = add_cell_ids(gpl_pre_df, "MO", pre_map)
                    df = add_cell_ids(df, "MO", post_map)
                    merged_df = pd.merge(left=gpl_pre_df, right=df, how='left', on=['cellId', 'Parameter'], indicator=True)
                    merged_df["MO_y"] = merged_df["MO_y"].fillna(merged_df["MO_x"])
                    merged_df["Node_ID_y"] = merged_df["Node_ID_y"].fillna("Cell is not Found in Post")
                    merged_df["Current value"] = merged_df["Value"]
                    merged_df.drop(columns=["MO_x", "Node_ID_x", "Value"], inplace=True)
                    merged_df.rename(columns={"MO_y": "MO", "Node_ID_y": "Node_ID"}, inplace=True)
                    merged_df.drop_duplicates(subset=["MO", "Parameter"], inplace=True)
                    
                    ################################################ Step 5: Add audit status ######################################
                    merged_df["Parameter Setting Status"] = merged_df.apply(
                        lambda row: (
                            "OK"
                            if row["Current value"] == row["Pre-existing Value"]
                            else (
                                "Missing"
                                if pd.isna(row["Current value"]) or pd.isna(row["Pre-existing Value"])
                                else "NOT OK"
                            )
                        ),
                        axis=1,
                    )
                    merged_df['Current value'] = merged_df['Current value'].fillna('NA')
                    def get_band(cell_name):
                        if '_F1_' in cell_name:
                            return 'L2100'
                        elif '_F3_' in cell_name:
                            return 'L1800'
                        elif '_F8_' in cell_name:
                            return 'L900'
                        elif '_T1_' in cell_name or '_T2_' in cell_name:
                            return 'L23'
                        else:
                            return 'Band Error'
                        
                    merged_df['Band'] = merged_df['MO'].apply(lambda x: get_band(x))
                    
                    ######################################################### Step 6: Output ########################################
                    merged_df = merged_df[
                        ["Node_ID", "MO"]
                        + [col for col in merged_df.columns if col not in ["Node_ID", "MO"]]
                    ]
                    merged_df.to_excel(writer, sheet_name=sheet_name, index=False)
                    format_excel_sheet(writer, sheet_name, merged_df, startrow=0, startcol=0)



                elif sheet_name == "FeatureState":
                    feature_pre_df = all_pre_merged_df.get(sheet_name)
                    cell_id_df = all_post_merged_df["Summary"]

                    feature_pre_df["Pre Existing FeatureState"] = feature_pre_df[
                        "Current FeatureState"
                    ]
                    feature_pre_df["Current FeatureState"] = ""
                    feature_pre_df["Pre Existing LicenseState"] = feature_pre_df[
                        "Current LicenseState"
                    ]
                    feature_pre_df["Pre Existing FeatureState"] = feature_pre_df[
                        "Pre Existing FeatureState"
                    ].astype(str)
                    feature_pre_df["Pre Existing LicenseState"] = feature_pre_df[
                        "Pre Existing LicenseState"
                    ].astype(str)
                    feature_pre_df["Current LicenseState"] = ""

                    feature_post_df = df.copy()
                    feature_post_df.rename(columns={"MO": "CXC ID"}, inplace=True)
                    feature_post_df["featureState"] = feature_post_df[
                        "featureState"
                    ].apply(lambda x: x.split(" ")[0] if " " in x else x)
                    feature_post_df["licenseState"] = feature_post_df[
                        "licenseState"
                    ].apply(lambda x: x.split(" ")[0] if " " in x else x)

                    pre_post_site_mapping = {
                        row["Pre SiteId"]: row["Post SiteId"]
                        for i, row in cell_id_df.iterrows() if row["Post SiteId"] != 'NA'
                    }

                    merged_df = pd.DataFrame()

                    for node_id in feature_pre_df["Node_ID"].unique():

                        post_node_id = pre_post_site_mapping.get(node_id, None)
                        if post_node_id is None:
                            continue

                        pre_df = feature_pre_df[feature_pre_df["Node_ID"] == node_id]
                        post_df = feature_post_df[
                            feature_post_df["Node_ID"] == post_node_id
                        ]

                        commind_df = pd.merge(
                            pre_df, post_df, on=["CXC ID", "description"], how="left"
                        )
                        # commind_df["featureState"] = commind_df["featureState"].astype(int)
                        # commind_df["licenseState"] = commind_df["licenseState"].astype(int)

                        commind_df["Node_ID_y"] = commind_df["Node_ID_y"].fillna(
                            commind_df["Node_ID_x"]
                        )
                        commind_df["Node_ID_x"] = commind_df["Node_ID_y"]

                        commind_df["Current FeatureState"] = commind_df["featureState"]
                        commind_df["Current LicenseState"] = commind_df["licenseState"]

                        commind_df.rename(
                            columns={"Node_ID_x": "Node_ID"}, inplace=True
                        )
                        commind_df.drop(
                            columns=["Node_ID_y", "featureState", "licenseState"],
                            inplace=True,
                        )

                        commind_df["Current FeatureState"] = commind_df[
                            "Current FeatureState"
                        ].astype(str)
                        commind_df["Current LicenseState"] = commind_df[
                            "Current LicenseState"
                        ].astype(str)

                        merged_df = pd.concat(
                            [merged_df, commind_df], axis=0, ignore_index=True
                        )

                    # merged_df.sort_values(by=["Node_ID"], inplace=True)
                    # columns_to_numeric = ["Pre Existing FeatureState", "Current FeatureState", "Current LicenseState", "Pre Existing LicenseState"]
                    # for col in columns_to_numeric:
                    #     merged_df["Pre Existing FeatureState"] = pd.to_numeric(merged_df["Current FeatureState"], errors="coerce").astype('int64')

                    merged_df["Feature setting Status"] = merged_df.apply(
                        lambda row: (
                            "OK"
                            if (
                                row["Current FeatureState"]
                                == row["Pre Existing FeatureState"]
                            )
                            and (
                                row["Current LicenseState"]
                                == row["Pre Existing LicenseState"]
                            )
                            else (
                                "Missing" if pd.isna(row['Current FeatureState']) or row['Current FeatureState'] == 'nan' or row['Pre Existing LicenseState'] == 'nan' or pd.isna(row['Pre Existing LicenseState']) else "NOT OK")
                        ),
                        axis=1,
                    )

                    # print(merged_df)
                    merged_df.to_excel(writer, sheet_name=sheet_name, index=False)
                    format_excel_sheet(
                        writer, sheet_name, merged_df, startrow=0, startcol=0
                    )

                elif sheet_name == "Eutranfrequency":

                    cell_id_df = all_post_merged_df["Summary"]

                    node_mapping = {
                        row["Pre SiteId"]: row["Post SiteId"]
                        for i, row in cell_id_df.iterrows() if row['Post SiteId'] != 'NA'
                    }

                    print(node_mapping)
                    pre_freq_df = all_pre_merged_df.get(sheet_name).copy()
                    post_freq_df = df[
                        df["MO"].astype(str).str.startswith("ENodeBFunction=")
                    ].copy()

                    merged_df = pre_freq_df.merge(
                        post_freq_df, how="left", on=["MO"]
                    ).sort_values(by=["arfcnValueEUtranDl_y"])

                    merged_df["arfcnValueEUtranDl_x"] = merged_df[
                        "arfcnValueEUtranDl_x"
                    ].astype(str)
                    merged_df["arfcnValueEUtranDl_y"] = merged_df[
                        "arfcnValueEUtranDl_y"
                    ].astype(str)

                    merged_df["Status"] = merged_df.apply(
                        lambda row: (
                            "OK"
                            if row["arfcnValueEUtranDl_x"]
                            == row["arfcnValueEUtranDl_y"]
                            else (
                                "Missing in Post"
                                if pd.isna(row["arfcnValueEUtranDl_y"]) or row['arfcnValueEUtranDl_y'] == 'nan'
                                else "NOT OK"
                            )
                        ),
                        axis=1,
                    )

                    merged_df.drop(columns=["Node_ID_y", 'arfcnValueEUtranDl_y'], inplace=True)

                    # Fix the rename issue
                    merged_df.rename(columns={"Node_ID_x": "Node_ID", "arfcnValueEUtranDl_x":"arfcnValueEUtranDl"}, inplace=True)

                    merged_df["Node_ID"] = merged_df["Node_ID"].apply(
                        lambda x: (
                            node_mapping[x] if x != "NA" and x in node_mapping else "NA"
                        )
                    )

                    merged_df.sort_values(by=["Node_ID"], inplace=True)


                    merged_df.to_excel(writer, sheet_name=sheet_name, index=False)
                    format_excel_sheet(
                        writer, sheet_name, merged_df, startrow=0, startcol=0
                    )

                elif sheet_name == "EutranfreqRelation":
                    pre_freq_relation_df = all_pre_merged_df.get(sheet_name)
                    cell_id_df = all_post_merged_df["Summary"]
                    post_freq_relation_df = df.copy()
                    pre_cell_mapping = {row["Pre CellName"]: row["cellId"] for i, row in cell_id_df.iterrows()}
                    mo_cell_mapping = {row["Pre CellName"]: row["Post CellName"] for i, row in cell_id_df.iterrows()}
                    
                    pre_post_site_mapping = {row["Pre SiteId"]: row["Post SiteId"] for i, row in cell_id_df.iterrows() if row["Post SiteId"] != 'NA'}
                    post_cell_mapping = {row["Post CellName"]: row["cellId"] for i, row in cell_id_df.iterrows()}
                    pre_freq_relation_df.insert(1, "cellId", "")
                    pre_freq_relation_df["cellId"] = pre_freq_relation_df["MO"].apply(lambda x: pre_cell_mapping[x.split(",")[0] if "," in x else x])
                    pre_freq_relation_df["lbBnrPolicy"] = pre_freq_relation_df["lbBnrPolicy"].apply(lambda x: x.split(" ")[0] if " " in x else x)
                    post_freq_relation_df.insert(1, "cellId", "")
                    post_freq_relation_df["cellId"] = post_freq_relation_df["MO"].apply(lambda x: post_cell_mapping[x.split(",")[0] if "," in x else x])
                    post_freq_relation_df["lbBnrPolicy"] = post_freq_relation_df["lbBnrPolicy"].apply(lambda x: x.split(" ")[0] if " " in x else x)

                    ########################################## selecting columns with the columns which have same types like: int64 ####################
                    int64_columns = pre_freq_relation_df.select_dtypes(include='int64').columns.tolist()
                    for col in int64_columns:
                        post_freq_relation_df[col] = post_freq_relation_df[col].astype('int64')
                    ####################################################################################################################################

                    merged_df = pd.merge(left=pre_freq_relation_df, right=post_freq_relation_df, on=['cellId', 'eutranFrequencyRef'], how='left', suffixes=('_x', '_y'))
                    ##################################################### selecting columns with float64 to int64 ######################################
                    float64_to_int64 = merged_df.select_dtypes(include='float64').columns.tolist()
                    for column in float64_to_int64:
                        merged_df[column] = (pd.to_numeric(merged_df[column], errors='coerce').replace([np.inf, -np.inf], pd.NA).astype('Int64'))
                    ####################################################################################################################################
                    # merged_df.drop(columns=['eutranFrequencyRef_x'], inplace=True)
                    # merged_df.rename(columns={'eutranFrequencyRef_y': "eutranFrequencyRef"}, inplace=True) 
                    merged_df["MO_y"] = merged_df["MO_y"].fillna(merged_df["MO_x"])
                    
                    merged_df["Node_ID_y"] = merged_df["Node_ID_y"].fillna("Cell is not Found in Post")
                    merged_df["Node_ID_x"] = merged_df["Node_ID_y"]
                    merged_df["MO_x"] = merged_df["MO_y"]
                    merged_df['duplicates_mask'] = merged_df.duplicated(subset=merged_df.columns.tolist())
                    merged_df.drop_duplicates(subset='MO_x', inplace=True)
                    merged_df.drop(columns=["MO_y", "Node_ID_y"], inplace=True)
                    merged_df.rename(columns={"MO_x": "MO", "Node_ID_x": "Node_ID"}, inplace=True)

                    merged_df.insert(3, "Status", "OK")
                    for col in pre_freq_relation_df.columns:
                        if col not in ["MO","Node_ID","eutranFrequencyRef","cellId",]:
                            pre_col = f"{col}_x"
                            post_col = f"{col}_y" 
                            
                            merged_df[pre_col] = (merged_df[pre_col].astype(str).str.lower())
                            merged_df[post_col] = (merged_df[post_col].astype(str).str.lower()) 
                            mask = merged_df[pre_col].ne(merged_df[post_col]) 
                            merged_df.loc[mask, "Status"] = "NOT OK"
                            for idx in merged_df[mask].index:
                                pre_value = merged_df.at[idx, pre_col]
                                post_value = merged_df.at[idx, post_col] 
                                if pd.isna(post_value) or post_value in ["nan",0,'0','<na>', '<NA>']:
                                    merged_df.at[idx, pre_col] = f"{pre_value}"
                                else:
                                    merged_df.at[idx, pre_col] = (f"{pre_value}|{post_value}")
                                    
                    for idx, row in merged_df.iterrows():
                        if row['Node_ID'] == 'Cell is not Found in Post':
                            merged_df.at[idx, 'Status'] = 'Missing'

                    merged_df.sort_values(by=["Node_ID"], inplace=True)

                    merged_df = merged_df[[col if col.endswith("_x") else col for col in merged_df.columns if not col.endswith("_y")]] 
                    merged_df.rename(columns={col: col.replace("_x", "") for col in merged_df.columns}, inplace=True)
                    merged_df.to_excel(writer, sheet_name=sheet_name, index=False)
                    format_excel_sheet(writer, sheet_name, merged_df, startrow=0, startcol=0)

                elif sheet_name == "CellRelation":
                    ################################################################ Get eNB IDs from pre and post data ##################################################################
                    pre_endb_id = (
                        all_pre_merged_df.get("enbinfo")["eNBId"].unique().tolist()
                    )
                    post_endb_id = all_post_merged_df["enbinfo"]["eNBId"].unique().tolist()
                    pre_endb_id = [str(val) for val in pre_endb_id]

                    ############################################################### Process pre and post cell relation data ##############################################################
                    pre_freq_cell_relation_df = all_pre_merged_df.get(sheet_name)
                    post_freq_cell_relation_df = df.copy()

                    ############################################################### Convert MO to string and extract eNB ID #############################################################
                    pre_freq_cell_relation_df["MO"] = pre_freq_cell_relation_df[
                        "MO"
                    ].astype(str)

                    post_freq_cell_relation_df["MO"] = post_freq_cell_relation_df[
                        "MO"
                    ].astype(str)

                    ################################################################ Extract eNB ID from MO ############################################################################
                    def extract_enb_id(mo: str) -> str:
                        return str(mo.split("-")[1]) if "-" in mo else mo

                    pre_freq_cell_relation_df["mo_enodbid"] = pre_freq_cell_relation_df[
                        "MO"
                    ].apply(extract_enb_id)
                    post_freq_cell_relation_df["mo_enodbid"] = (
                        post_freq_cell_relation_df["MO"].apply(extract_enb_id)
                    )

                    ################################################################# Filter data based on eNB IDs #####################################################################
                    pre_freq_cell_relation_df = pre_freq_cell_relation_df[
                        pre_freq_cell_relation_df["mo_enodbid"].isin(pre_endb_id)
                    ]
                    post_freq_cell_relation_df = post_freq_cell_relation_df[
                        post_freq_cell_relation_df["mo_enodbid"].isin(
                            post_endb_id+pre_endb_id + [""]
                        )
                    ]

                    ################################################################# Remove temporary eNB ID column ###################################################################
                    pre_freq_cell_relation_df.drop(columns=["mo_enodbid"], inplace=True)
                    post_freq_cell_relation_df.drop(
                        columns=["mo_enodbid"], inplace=True
                    )

                    ################################################################## Convert numeric columns #########################################################################
                    numeric_columns = [
                        "coverageIndicator",
                        "loadBalancing",
                        "reportDlActivity",
                        "sCellCandidate",
                        "sleepModeCovCellCandidate",
                    ]

                    def convert_to_int(value):
                        return int(
                            str(value).split(" ")[0] if " " in str(value) else value
                        )

                    for col in numeric_columns:
                        pre_freq_cell_relation_df[col] = pre_freq_cell_relation_df[
                            col
                        ].apply(convert_to_int)
                        post_freq_cell_relation_df[col] = post_freq_cell_relation_df[
                            col
                        ].apply(convert_to_int)

                    ################################################################### Create cell ID mappings ########################################################################
                    pre_cell_mapping = {
                        row["Pre CellName"]: row["cellId"]
                        for _, row in cell_id_df.iterrows()
                    }
                    post_cell_mapping = {
                        row["Post CellName"]: row["cellId"]
                        for _, row in cell_id_df.iterrows()
                    }

                    #################################################################### Add cell IDs to dataframes ####################################################################
                    def get_cell_id(mo: str, mapping: dict) -> str:
                        return mapping.get(mo.split(",")[0], "") if "," in mo else mo

                    pre_freq_cell_relation_df.insert(1, "cellId", "")
                    pre_freq_cell_relation_df["cellId"] = pre_freq_cell_relation_df[
                        "MO"
                    ].apply(lambda x: get_cell_id(x, pre_cell_mapping))

                    post_freq_cell_relation_df.insert(1, "cellId", "")
                    post_freq_cell_relation_df["cellId"] = post_freq_cell_relation_df[
                        "MO"
                    ].apply(lambda x: get_cell_id(x, post_cell_mapping))

                    ##################################################################### Merge pre and post data ########################################################################
                    merged_df = pd.merge(
                        left=pre_freq_cell_relation_df,
                        right=post_freq_cell_relation_df,
                        on=["cellId"],
                        how="left",
                        suffixes=("_x", "_y"),
                    )

                    # merged_df = merged_df[merged_df['MO_x'] != 'Missing']

                    merged_df.drop_duplicates(subset=["MO_x"], inplace=True)
                    # merged_df.columns = [f"{val[0]}_{val[1]}" for val in merged_df.columns]

                    merged_df["MO_y"] = merged_df["MO_y"].fillna(merged_df["MO_x"])
                    merged_df["MO_x"] = merged_df["MO_y"]
                    merged_df["Node_ID_y"] = merged_df["Node_ID_y"].fillna(
                        "cell not found in post"
                    )
                    merged_df["Node_ID_x"] = merged_df["Node_ID_y"]
                    merged_df["neighborCellRef_x"] = merged_df["neighborCellRef_y"]
                    merged_df.drop(columns=["MO_y", "Node_ID_y"], inplace=True)
                    merged_df.rename(
                        columns={
                            "MO_x": "MO",
                            "Node_ID_x": "Node_ID",
                            "neighborCellRef_x": "neighborCellRef",
                        },
                        inplace=True,
                    )

                    merged_df = merged_df[
                        merged_df["Node_ID"] != "cell not found in post"
                    ].copy()

                    for col in numeric_columns:
                        merged_df[f"{col}_x"] = pd.to_numeric(
                            merged_df[f"{col}_x"], errors="coerce"
                        )
                        merged_df[f"{col}_x"] = (
                            merged_df[f"{col}_x"].fillna(0).astype(int)
                        )
                        # merged_df[f'pre_{col}'] = merged_df[f'pre_{col}'].astype(int) if merged_df[f'pre_{col}'] else merged_df[f'pre_{col}']
                        merged_df[f"{col}_y"] = pd.to_numeric(
                            merged_df[f"{col}_y"], errors="coerce"
                        )
                        merged_df[f"{col}_y"] = (
                            merged_df[f"{col}_y"].fillna(0).astype(int)
                        )

                    merged_df.insert(3, "Status", "OK")

                    for col in pre_freq_cell_relation_df.columns:
                        if col not in ["MO", "Node_ID", "neighborCellRef", "cellId"]:
                            pre_col = f"{col}_x"
                            post_col = f"{col}_y"

                            merged_df[pre_col] = (
                                merged_df[pre_col].astype(str).str.lower()
                            )
                            merged_df[post_col] = (
                                merged_df[post_col].astype(str).str.lower()
                            )

                            mask = merged_df[pre_col].ne(merged_df[post_col])

                            merged_df.loc[mask, "Status"] = "NOT OK"
                            for idx in merged_df[mask].index:
                                pre_value = merged_df.at[idx, pre_col]
                                post_value = merged_df.at[idx, post_col]

                                if pd.isna(post_value) or post_value in [
                                    "nan",
                                ]:
                                    merged_df.at[idx, pre_col] = f"{pre_value}"
                                    merged_df.at[idx, 'Status'] = "Missing"
                                else:
                                    merged_df.at[idx, pre_col] = (
                                        f"{pre_value}|{post_value}"
                                    )

                    merged_df.sort_values(by=["Node_ID"], inplace=True)
                    merged_df = merged_df[
                        [
                            col if col.endswith("_x") else col
                            for col in merged_df.columns
                            if not col.endswith("_y")
                        ]
                    ]

                    merged_df.rename(
                        columns={
                            col: col.replace("_x", "") for col in merged_df.columns
                        },
                        inplace=True,
                    )

                    merged_df.sort_values(by=["MO", "Node_ID"], inplace=True)

                    #################################################################### Write to Excel ####################################################################################
                    merged_df.to_excel(writer, sheet_name=sheet_name, index=False)
                    format_excel_sheet(
                        writer, sheet_name, merged_df, startrow=0, startcol=0
                    )

                else:
                    if sheet_name == "cell_data":
                        df.columns = [
                            (
                                col.replace("left_", "")
                                if col.startswith("left_")
                                else col.replace("right_", "")
                            )
                            for col in df.columns
                        ]
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    format_excel_sheet(writer, sheet_name, df, startrow=0, startcol=0)

    # Generate download URL
    relative_url = gpl_pre_post_file_path.replace(str(settings.MEDIA_ROOT), "").lstrip(
        "/"
    )
    download_url = request.build_absolute_uri(settings.MEDIA_URL + relative_url)

    # Return success response
    return Response(
        {
            "message": "Post logs and Pre-audit file uploaded successfully",
            "download_url": download_url,
        },
        status=status.HTTP_200_OK,
    )




    