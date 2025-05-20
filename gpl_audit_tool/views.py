from optparse import Values
from traceback import print_tb
from matplotlib import axis
import numpy as np
from rest_framework.decorators import api_view
from rest_framework.response import Response
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
import pandas as pd
from gpl_audit_tool.extractors.table_extractor import TableExtractor
from gpl_audit_tool.serializers import ExcelUploadSerializer
from gpl_audit_tool.writer.excel_writer import ExcelWriter
from gpl_audit_tool.extractors.command_extractor import CommandExtractor
from gpl_audit_tool.utils.thread_pool import ThreadPool
from gpl_audit_tool.utils.file_reader import FileReader
from gpl_audit_tool.config.settings import Config
from gpl_audit_tool.writer.script_generator import GplScriptFactory
from concurrent.futures import ThreadPoolExecutor
from xlsxwriter import Workbook
from django.core.files.storage import default_storage
import json
import os
from rest_framework import status
from django.conf import settings
from datetime import datetime
from typing import Dict, List, Optional, Tuple


def delete_existing_files(folder_path: str) -> None:
    """ Delete all files in the specified folder."""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")


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


def process_files(file, log_folder, result):
    log_path = os.path.join(log_folder, file)
    log_lines = FileReader.read_file(log_path)
    extractor = TableExtractor(log_lines)
    return file, extract_tables(extractor, result)


def process_cell_data(df: pd.DataFrame) -> pd.DataFrame:
    """Process cell data by handling FDD and TDD cells."""
    # Standardize column names
    df.rename(
        columns={
            "left_channelBandwidth": "left_dlChannelBandwidth",
            "left_earfcn": "left_earfcndl",
        },
        inplace=True,
    )
    df.drop(columns=["right_Node_ID"], inplace=True)

    if "left_MO" not in df.columns:
        return df

    # Process FDD and TDD cells
    is_fdd = df["left_MO"].astype(str).str.startswith("EUtranCellFDD=")
    is_tdd = df["left_MO"].astype(str).str.startswith("EUtranCellTDD=")

    if not is_tdd.any():
        df["left_earfcnul"] = None
        return df

    df_fdd = df[is_fdd].copy()
    df_tdd = df[is_tdd].copy()

    if not df_tdd.empty:
        try:
            start_idx = df.columns.get_loc("left_earfcnul")
            end_idx = df.columns.get_loc("left_userLabel")
            df_tdd.iloc[:, start_idx + 1 : end_idx + 1] = df_tdd.iloc[
                :, start_idx:end_idx
            ].to_numpy()
            df_tdd.loc[:, "left_earfcnul"] = ""
            df_tdd["left_userLabel"] = df_tdd["left_ulChannelBandwidth"]
            df_tdd["left_ulChannelBandwidth"] = ""
        except Exception as e:
            print(f"Error processing TDD cells: {e}")

    return pd.concat([df_fdd, df_tdd], ignore_index=True)


def merge_pre_post_data(
    pre_df: pd.DataFrame, post_df: pd.DataFrame, merge_on: str
) -> pd.DataFrame:
    """Merge pre and post data with proper handling of missing values."""
    merged_df = pre_df.merge(
        post_df, on=merge_on, how="outer", suffixes=("_pre", "_post")
    ).fillna("Missing")

    # Clean up column names
    for col in merged_df.columns:
        if col.endswith("_pre"):
            merged_df.rename(
                columns={col: f"pre_{col.replace('_pre', '')}"}, inplace=True
            )
        elif col.endswith("_post"):
            merged_df.rename(
                columns={col: f"post_{col.replace('_post', '')}"}, inplace=True
            )
        elif col not in [merge_on] and not col.startswith(("pre_", "post_")):
            merged_df.rename(columns={col: f"pre_{col}"}, inplace=True)

    return merged_df


def generate_mos_file(
    df_set: pd.DataFrame, df_crn: pd.DataFrame, output_file: str
) -> None:
    """Generate MOS file from DataFrames."""
    timestamp = datetime.now().strftime("%y%m%d_%H%M")
    mos_content = [
        "$date = `date +%y%m%d_%H%M`",
        f"\ncvms Pre_Relation_$date",
        "gs+\n",
    ]

    # Add set commands
    df_set = df_set.dropna(subset=["MO", "Relation Parameter", "Value"])
    mos_content.extend(
        f"set {row['MO']}$ {row['Relation Parameter']} {row['Value'].split('|')[0] if '|' in str(row['Value']) else row['Value']}"
        for _, row in df_set.iterrows()
    )

    # Add crn sections
    if not df_crn.empty:
        df_crn = df_crn.dropna(subset=["MO", "Relation Parameter", "Value"])
        for mo, group in df_crn.groupby("MO"):
            mos_content.extend(
                [
                    f"\ncrn {mo}",
                    *[
                        f"{row['Relation Parameter']} {row['Value']}"
                        for _, row in group.iterrows()
                    ],
                    "end",
                ]
            )

    mos_content.extend(
        ["\n$date = `date +%y%m%d_%H%M`", "\ncvms Post_Relation_$date\ngs-"]
    )

    with open(output_file, "w") as f:
        f.write("\n".join(mos_content))


@api_view(["POST", "GET"])
def get_table_data(request):
    ############################### Process command file #######################################
    command_lines = FileReader.read_file(Config().get("command_file"))
    result = get_commands(command_lines)

    ############################### Add logging to debug request parameters #####################
    print("Request Method:", request.method)
    print("POST Data:", request.POST)
    print("FILES Data:", request.FILES)

    ############################### Validate required parameters #################################
    services = request.POST.get("services")
    circle = request.POST.get("circle")

    if not services or not circle:
        return Response(
            {"error": "Service and circle parameters are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    print(f"Processing request for service: {services}, circle: {circle}")

    if services == "GPL PRE AUDIT":
        pre_logs = request.FILES.getlist("pre_log_files")
        if not pre_logs:
            print("No pre_log_files found in request")
            return Response(
                {"error": "Logs Files are required to proceed towards audit"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        pre_log_folder = Config().get("pre_log_folder")

        if not os.path.exists(pre_log_folder):
            os.mkdir(pre_log_folder)

        delete_existing_files(pre_log_folder)

        saved_files = []
        for file in pre_logs:
            file_path = os.path.join(pre_log_folder, file.name)
            with open(file_path, "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            saved_files.append(file_path)

        all_dfs = {"Summary": []} | {key: [] for key in result.keys()}

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(process_files, file, pre_log_folder, result): file
                for file in saved_files
            }

            for future in futures:
                file, df_dict = future.result()
                for key, df in df_dict.items():
                    all_dfs[key].append(df)

        # Constants for cell types
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

        # Process each DataFrame in cell_data
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
        excel_path = Config().get("pre_output_excel")

        # Get current datetime and node_id
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        node_id = (
            all_merged_df["cell_data"]["left_Node_ID"].iloc[0]
            if not all_merged_df["cell_data"].empty
            else "UNKNOWN"
        )
        excel_path = os.path.join(excel_path)

        # Create new filename with datetime and node_id
        base_dir = os.path.dirname(excel_path)
        base_name = os.path.basename(excel_path)
        new_filename = (
            f"{node_id}_{base_name.replace('.xlsx', '')}_{current_datetime}.xlsx"
        )
        excel_path = os.path.join(base_dir, new_filename)
        try:
            # First try the primary output location
            gpl_output_path = os.path.join(
                Config().get("GPL_AUDIT_OUTPUT"), f"{node_id}", "pre"
            )
            os.makedirs(gpl_output_path, exist_ok=True, mode=0o777)
            gpl_output_path = os.path.join(gpl_output_path, new_filename)
        except (PermissionError, OSError) as e:
            print(f"Error creating primary output directory: {e}")
            try:
                # Fallback to a simpler path structure
                gpl_output_path = os.path.join(
                    Config().get("GPL_AUDIT_OUTPUT"), f"{node_id}", "pre"
                )
                os.makedirs(gpl_output_path, exist_ok=True, mode=0o777)
                gpl_output_path = os.path.join(
                    gpl_output_path, f"{node_id}_{current_datetime}.xlsx"
                )
            except (PermissionError, OSError) as e:
                print(f"Error creating fallback directory: {e}")
                gpl_output_path = excel_path

        with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer, pd.ExcelWriter(
            gpl_output_path, engine="xlsxwriter"
        ) as output:
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
                df.to_excel(output, sheet_name=sheet_name, index=False)
                format_excel_sheet(output, sheet_name, df)

            if not summary_df.empty:
                summary_df["Post SiteId"] = ""

                summary_df["Post CellName"] = ""

                summary_df.to_excel(writer, sheet_name="Summary", index=False)
                format_excel_sheet(writer, "Summary", summary_df)

        return Response(
            {
                "message": f"{services} data is sucesfully feteched...",
                "download_url": os.path.join(MEDIA_ROOT, excel_path),
            },
            status=status.HTTP_200_OK,
        )

    elif services == "GPL PRE POST AUDIT":
        post_logs = request.FILES.getlist("post_log_files")
        serializer = ExcelUploadSerializer(
            data=request.FILES, context={"request": request}
        )

        print("Post logs:", post_logs)
        print(
            "Serializer errors:",
            serializer.errors if not serializer.is_valid() else "Valid",
        )

        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        excel_file = request.FILES["pre_audit_file"]
        post_log_folder = Config().get("post_log_folder")
        os.makedirs(post_log_folder, exist_ok=True)
        delete_existing_files(post_log_folder)

        saved_files = []

        for file in post_logs:
            file_path = os.path.join(post_log_folder, file.name)
            with open(file_path, "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            saved_files.append(file_path)

        gpl_audit_file_path = Config().get("gpl_pre_post_audit")

        # Save uploaded file
        with open(gpl_audit_file_path, "wb+") as destination:
            for chunk in excel_file.chunks():
                destination.write(chunk)

        # Process pre-audit data
        pre_df_data = pd.ExcelFile(excel_file, engine="openpyxl")
        pre_cell_id_df = pre_df_data.parse("Summary")[
            ["Pre SiteId", "Pre CellName", "Pre eNBID", "cellId"]
        ].copy()

        # Initialize dataframes dictionary
        all_dfs = {"Summary": []} | {key: [] for key in result.keys()}

        # Process post files in parallel
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(process_files, file, post_log_folder, result): file
                for file in saved_files
            }
            for future in futures:
                file, df_dict = future.result()
                for key, df in df_dict.items():
                    all_dfs[key].append(df)

        # Process cell data
        for i, mo_df in enumerate(all_dfs["cell_data"]):
            # Standardize column names
            mo_df.rename(
                columns={
                    "left_channelBandwidth": "left_dlChannelBandwidth",
                    "left_earfcn": "left_earfcndl",
                },
                inplace=True,
            )
            mo_df.drop(columns=["right_Node_ID"], inplace=True)

            if "left_MO" not in mo_df.columns:
                continue

            # Process FDD and TDD cells
            is_fdd = mo_df["left_MO"].astype(str).str.startswith("EUtranCellFDD=")
            is_tdd = mo_df["left_MO"].astype(str).str.startswith("EUtranCellTDD=")

            if not is_tdd.any():
                # Process FDD cells
                mo_df["left_earfcnul"] = None
                all_dfs["cell_data"][i] = mo_df
                continue

            # Process mixed FDD and TDD cells
            df_fdd = mo_df[is_fdd].copy()
            df_tdd = mo_df[is_tdd].copy()

            if not df_tdd.empty:
                # Process TDD cells
                try:
                    start_idx = mo_df.columns.get_loc("left_earfcnul")
                    end_idx = mo_df.columns.get_loc("left_userLabel")
                    df_tdd.iloc[:, start_idx + 1 : end_idx + 1] = df_tdd.iloc[
                        :, start_idx:end_idx
                    ].to_numpy()
                    df_tdd.loc[:, "left_earfcnul"] = ""
                    df_tdd["left_userLabel"] = df_tdd["left_ulChannelBandwidth"]
                    df_tdd["left_ulChannelBandwidth"] = ""
                except Exception as e:
                    print(f"Error processing TDD cells: {e}")

            all_dfs["cell_data"][i] = pd.concat([df_fdd, df_tdd], ignore_index=True)

        ############################################################### Merge all DataFrames ##############################################################
        all_merged_df = {
            key: pd.concat(dfs, ignore_index=False, axis=0) if dfs else pd.DataFrame()
            for key, dfs in all_dfs.items()
        }

        ################################################################ Prepare post cell data ###########################################################
        post_cell_id_df = all_merged_df["cell_data"][
            ["left_Node_ID", "left_MO", "left_cellId"]
        ].rename(
            columns={
                "left_MO": "Post CellName",
                "left_Node_ID": "Post SiteId",
                "left_cellId": "cellId",
            }
        )

        ############################################################ mapping eNBId with Site ID ############################################################

        enodeid_mapping = {
            row["Node_ID"]: row["eNBId"]
            for _, row in all_merged_df["enbinfo"].iterrows()
        }

        #####################################################################################################################################################

        # Merge pre and post data
        pre_cell_id_df["cellId"] = pre_cell_id_df["cellId"].astype(str)
        post_cell_id_df["cellId"] = post_cell_id_df["cellId"].astype(str)
        all_merged_df["Summary"] = pd.merge(
            pre_cell_id_df, post_cell_id_df, on=["cellId"], how="outer"
        ).fillna("NA")

        for idx, row in all_merged_df["Summary"].iterrows():
            print(type(row["Pre eNBID"]))
            if type(row["Pre eNBID"]) == float:
                all_merged_df["Summary"].at[idx, "Pre eNBID"] = str(
                    int(row["Pre eNBID"])
                )

        all_merged_df["Summary"] = all_merged_df["Summary"].sort_values(
            by=["Pre SiteId", "Pre CellName", "cellId"], ascending=True
        )

        ##################################################################################### Adding enode id ###############################################

        all_merged_df["Summary"]["Post eNBID"] = all_merged_df["Summary"][
            "Post SiteId"
        ].apply(lambda x: enodeid_mapping[x] if x != "NA" else "NA")
        all_merged_df["Summary"].insert(
            5, "Post eNBID", all_merged_df["Summary"].pop("Post eNBID")
        )

        ################################################################################### Create output filename with node_id and timestamp ###############
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        node_id = (
            all_merged_df["cell_data"]["left_Node_ID"].iloc[0]
            if not all_merged_df["cell_data"].empty
            else "UNKNOWN"
        )

        base_dir = os.path.dirname(gpl_audit_file_path)
        base_name = os.path.basename(gpl_audit_file_path)
        new_filename = (
            f"{node_id}_{base_name.replace('.xlsx', '')}_{current_datetime}.xlsx"
        )
        gpl_audit_file_path = os.path.join(base_dir, new_filename)
        try:
            # First try the primary output location
            gpl_output_path = os.path.join(
                Config().get("GPL_AUDIT_OUTPUT"), f"{node_id}", "post"
            )
            os.makedirs(gpl_output_path, exist_ok=True, mode=0o777)
            gpl_output_path = os.path.join(gpl_output_path, new_filename)
        except (PermissionError, OSError) as e:
            print(f"Error creating primary output directory: {e}")
            try:
                # Fallback to a simpler path structure
                gpl_output_path = os.path.join(
                    Config().get("GPL_AUDIT_OUTPUT"), f"{node_id}", "post"
                )
                os.makedirs(gpl_output_path, exist_ok=True, mode=0o777)
                gpl_output_path = os.path.join(
                    gpl_output_path, f"{node_id}_{current_datetime}.xlsx"
                )
            except (PermissionError, OSError) as e:
                print(f"Error creating fallback directory: {e}")
                gpl_output_path = excel_path

        # Write to Excel
        with pd.ExcelWriter(
            gpl_audit_file_path, engine="xlsxwriter"
        ) as writer, pd.ExcelWriter(gpl_output_path, engine="xlsxwriter") as output:
            workbook = writer.book
            for sheet_name, df in all_merged_df.items():
                if sheet_name == "Summary":
                    df.to_excel(
                        writer,
                        sheet_name=sheet_name,
                        startcol=9,
                        startrow=3,
                        index=False,
                    )
                    format_excel_sheet(writer, sheet_name, df, startrow=3, startcol=9)
                    # df.to_excel(
                    #     output,
                    #     sheet_name=sheet_name,
                    #     startcol=9,
                    #     startrow=3,
                    #     index=False,
                    # )
                    # format_excel_sheet(output, sheet_name, df, startrow=3, startcol=9)

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
                    cell_id_df = all_merged_df["Summary"].sort_values(by="Pre SiteId")
                    gpl_pre_df = pre_df_data.parse(sheet_name)
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
                    feature_pre_df = pre_df_data.parse(sheet_name)
                    cell_id_df = all_merged_df["Summary"]

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

                    cell_id_df = all_merged_df["Summary"]

                    node_mapping = {
                        row["Pre SiteId"]: row["Post SiteId"]
                        for i, row in cell_id_df.iterrows() if row['Post SiteId'] != 'NA'
                    }

                    print(node_mapping)
                    pre_freq_df = pre_df_data.parse(sheet_name).copy()
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


             
                    pre_freq_relation_df = pre_df_data.parse(sheet_name)
                    cell_id_df = all_merged_df["Summary"]
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

                    merged_df = pd.merge(left=pre_freq_relation_df, right=post_freq_relation_df, on=['cellId'], how='left', suffixes=('_x', '_y'))
                    ##################################################### selecting columns with float64 to int64 ######################################
                    float64_to_int64 = merged_df.select_dtypes(include='float64').columns.tolist()
                    for column in float64_to_int64:
                        merged_df[column] = (pd.to_numeric(merged_df[column], errors='coerce').replace([np.inf, -np.inf], pd.NA).astype('Int64'))
                    ####################################################################################################################################
                    merged_df.drop(columns=['eutranFrequencyRef_x'], inplace=True)
                    merged_df.rename(columns={'eutranFrequencyRef_y': "eutranFrequencyRef"}, inplace=True) 
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
                                    # temp_merged_df.at[idx, 'Status'] = "Missing"
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
                        pre_df_data.parse("enbinfo")["eNBId"].unique().tolist()
                    )
                    post_endb_id = all_merged_df["enbinfo"]["eNBId"].unique().tolist()
                    pre_endb_id = [str(val) for val in pre_endb_id]

                    ############################################################### Process pre and post cell relation data ##############################################################
                    pre_freq_cell_relation_df = pre_df_data.parse(sheet_name)
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
                    df.to_excel(output, sheet_name=sheet_name, index=False)
                    format_excel_sheet(output, sheet_name, df, startrow=0, startcol=0)

        # Generate download URL
        relative_url = gpl_audit_file_path.replace(str(settings.MEDIA_ROOT), "").lstrip(
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
    elif services == "SCRIPT GENERATOR":
        serializer = ExcelUploadSerializer(
            data=request.FILES, context={"request": request}
        )
        if not serializer.is_valid():
            print("Serializer errors:", serializer.errors)
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        excel_file = request.FILES["PRE_POST_AUDIT_FILE"]

        pre_post_df_data = pd.ExcelFile(excel_file, engine="openpyxl")

        ###### GPL parameter script generation ###############
        gpl_para_df = pre_post_df_data.parse("gpl-para").copy()
        node_id = gpl_para_df["Node_ID"].unique()[1]
        # Filter out rows with OK status and ensure Current Value is not NA
        mask = (gpl_para_df["Parameter Setting Status"] != "OK") & pd.notna(
            gpl_para_df["Current value"]
        )
        gpl_para_df = gpl_para_df[mask].copy()

        # Verify we have data after filtering
        if gpl_para_df.empty:
            print("Warning: No parameters need correction after filtering")
            return Response(
                {"message": "No parameters need correction", "download_url": None},
                status=status.HTTP_200_OK,
            )

        gpl_correction_script = GplScriptFactory.create_generator(gpl_para_df)
        print(gpl_para_df)

        path = Config().get("GPL_correction_script")

        gpl_correction_script.create_script(
            script_path=path,
            script_type="Pre_Parameters_correction",
            script_line="LTE Pre Parameters",
            script_ender="Post_LTE_GPL_Correction",
            node_id=node_id,
        )

        ###### feature State script generation #####################
        featureState_df = pre_post_df_data.parse("FeatureState")
        featureState_df = featureState_df[
            featureState_df["Feature setting Status"] != "OK"
        ]
        print(gpl_para_df)
        featureState_df_script = GplScriptFactory.create_generator(featureState_df)
        path = Config().get("GPL_correction_script")
        featureState_df_script.create_script(
            script_path=path,
            script_type="Pre_Parameters_correction",
            script_line="LTE Post Para Feature Correction",
            script_ender="Post_LTE_GPL_Correction",
            node_id=node_id,
        )

        ######### Relation Script generation ####################\\

        def format_mos_line(mo, param, value):
            value = value.split("|")[0] if "|" in value else value
            return f"set {mo}$ {param} {value}"

        def generate_crn_section(df: pd.DataFrame):
            mos_content = []
            if not df.empty:
                df = df.dropna(subset=["MO", "Relation Parameter", "Value"])
                for mo, group in df.groupby("MO"):
                    print(mo)
                    mos_content.append(f"\ncrn {mo}")
                    for _, row in group.iterrows():
                        mos_content.append(
                            f"{row['Relation Parameter']} {row['Value']}"
                        )
                    mos_content.append("end")
            return mos_content

        def generate_mos_file(
            df_set: pd.DataFrame,
            df_crn: pd.DataFrame,
            # cell_rel_df: pd.DataFrame,
            # crn_cell_relation_df: pd.DataFrame,
            output_file,
        ):
            timestamp = datetime.now().strftime("%y%m%d_%H%M")

            mos_content = [
                "$date = `date +%y%m%d_%H%M`",
                f"\ncvms Pre_Relation_$date",
                "gs+\n",
            ]

            df_set = df_set.dropna(subset=["MO", "Relation Parameter", "Value"])
            mos_content.extend(
                format_mos_line(row["MO"], row["Relation Parameter"], row["Value"])
                for _, row in df_set.iterrows()
            )

            mos_content.extend(generate_crn_section(df_crn))
            print("relation cen cell realtion:- ", crn_cell_relation_df)
            # if not cell_rel_df.empty:
            #     mos_content.append(
            #         f"""\n ############################## CELL RELATION SCRIPT ##################################### \n """
            #     )

            #     mos_content.extend(
            #         format_mos_line(row["MO"], row["Relation Parameter"], row["Value"])
            #         for _, row in cell_rel_df.iterrows()
            #     )
            #     if not crn_cell_relation_df.empty:
            #         mos_content.extend(generate_crn_section(crn_cell_relation_df))

            mos_content.append("\n$date = `date +%y%m%d_%H%M`")
            mos_content.append("\ncvms Post_Relation_$date\ngs-")
            with open(output_file, "w") as f:
                f.write("\n".join(mos_content))

            print(f"MOS file generated: {output_file}")

        # === Data preparation ===
        cell_id_df = pd.read_excel(
            excel_file,
            sheet_name="Summary",
            engine="openpyxl",
            skiprows=3,
            usecols="J:P",
        )
        print(cell_id_df)
        eutran_freq_relation_df = pre_post_df_data.parse("EutranfreqRelation")
        node_id = cell_id_df["Post SiteId"].unique()
        pre_remaining_df = eutran_freq_relation_df[
            eutran_freq_relation_df["Status"] == "Missing"
        ].copy()
        eutran_freq_relation_df = eutran_freq_relation_df[
            eutran_freq_relation_df["Status"] != "Missing"
        ].copy()
        pre_post_cell_id_dict = {
            row["Pre CellName"]: row["Post CellName"]
            for _, row in cell_id_df.iterrows()
        }
        post_cell_id_dict = {
            row["cellId"]: row["Post SiteId"] for _, row in cell_id_df.iterrows()
        }
        pre_remaining_df["MO"] = (
            pre_remaining_df["MO"]
            .astype(str)
            .apply(
                lambda x: (
                    str(pre_post_cell_id_dict[x.split(",")[0]]) + x.split(",")[1]
                    if "," in x
                    else x
                )
            )
        )
        print(pre_remaining_df.columns)
        for cell_id in pre_remaining_df["cellId"].unique():
            pre_remaining_df.loc[pre_remaining_df["cellId"] == cell_id, "Node_ID"] = (
                post_cell_id_dict.get(cell_id, "Cell is not Found in Post")
            )

        pre_remaining_df.loc[:, "MO"] = pre_remaining_df.apply(
            lambda row: (
                str(row["MO"])
                + ",EUtranFreqRelation="
                + str(str(row["eutranFrequencyRef"]).split(",")[2].split("=")[1])
                if pd.notna(row.get("eutranFrequencyRef"))
                and len(str(row["eutranFrequencyRef"]).split(",")) > 2
                else row["MO"]
            ),
            axis=1,
        )
        eutran_freq_relation_df = eutran_freq_relation_df[
            eutran_freq_relation_df["Status"] != "OK"
        ]

        eutran_freq_relation_df.drop(
            columns=["cellId", "Status", "Node_ID"], inplace=True
        )

        pre_remaining_df.drop(columns=["cellId", "Status", "Node_ID"], inplace=True)

        id_vars = ["MO"]
        value_vars = [
            col for col in eutran_freq_relation_df.columns if col not in id_vars
        ]
        eutran_freq_relation_df = eutran_freq_relation_df.melt(
            id_vars=id_vars,
            value_vars=value_vars,
            var_name="Relation Parameter",
            value_name="Value",
        )
        eutran_freq_relation_df.sort_values(by="MO", inplace=True)
        # eutran_freq_relation_df.drop_duplicates(
        #     subset=["MO", "Relation Parameter"], inplace=True
        # )

        eutran_freq_relation_df = eutran_freq_relation_df[
            (
                eutran_freq_relation_df["Value"]
                .astype(str)
                .str.contains(r"\|", regex=True, na=False)
            )
        ]
        print(eutran_freq_relation_df)
        id_vars = ["MO"]
        value_vars = [
            col
            for col in pre_remaining_df.columns
            if col not in id_vars and col not in ["eutranFrequencyRef", "Node_ID"]
        ]
        print(pre_remaining_df)
        pre_remaining_df = pre_remaining_df.melt(
            id_vars=id_vars,
            value_vars=value_vars,
            var_name="Relation Parameter",
            value_name="Value",
        )

        pre_remaining_df = pre_remaining_df[~pd.isna(pre_remaining_df["MO"])]

        pre_remaining_df["Value"] = pre_remaining_df["Value"].apply(
            lambda x: str(x).split("|")[0] if "|" in str(x) else x
        )

        pre_remaining_df.drop_duplicates(
            subset=["MO", "Relation Parameter"], inplace=True
        )

        print(pre_remaining_df)

        path = Config().get("GPL_Relation_script")
        dir_path = os.path.dirname(path)  # getting directory path
        filename = os.path.basename(path)
        current_datetime = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )  # getting original filename
        new_filename = f"{node_id[0]}_{filename.replace('.txt', '')}_{current_datetime}.txt"  # renaming file with node_id prefix
        path = os.path.join(dir_path, new_filename)  # creating final path

        ########################################## CELL RELATION SCRIPT ###################################################################

        cell_relation_df = pre_post_df_data.parse("CellRelation")

        cell_relation_df = cell_relation_df[cell_relation_df["MO"] != "OK"]
        crn_cell_relation_df = cell_relation_df[
            cell_relation_df["Node_ID"] == "cell not found in post"
        ]
        cell_relation_df.drop(
            columns=["cellId", "Status", "Node_ID", "neighborCellRef"], inplace=True
        )

        crn_cell_relation_df.drop(
            columns=["cellId", "Status", "Node_ID", "neighborCellRef"], inplace=True
        )
        id_vars = ["MO"]
        value_vars = [col for col in cell_relation_df.columns if col not in id_vars]
        cell_relation_df = cell_relation_df.melt(
            id_vars=id_vars,
            value_vars=value_vars,
            var_name="Relation Parameter",
            value_name="Value",
        )
        crn_cell_relation_df = crn_cell_relation_df.melt(
            id_vars=id_vars,
            value_vars=value_vars,
            var_name="Relation Parameter",
            value_name="Value",
        )

        # cell_relation_df["Value"] = cell_relation_df["Value"].apply(
        #     lambda x: str(x).split("|")[0] if "|" in str(x) else x
        # )

        cell_relation_df = cell_relation_df[
            (
                cell_relation_df["Value"]
                .astype(str)
                .str.contains(r"\|", regex=True, na=False)
            )
        ]

        cell_relation_df.drop_duplicates(
            subset=["MO", "Relation Parameter"], inplace=True
        )

        cell_relation_df = cell_relation_df[cell_relation_df["MO"] != "Missing"]
        cell_relation_df.sort_values(by="MO", inplace=True)

        generate_mos_file(
            eutran_freq_relation_df,
            pre_remaining_df,
            # cell_relation_df,
            # crn_cell_relation_df,
            output_file=path,
        )

        print(cell_relation_df)

        # download url
        relative_url = path.replace(str(settings.MEDIA_ROOT), "").lstrip("/")
        download_url = request.build_absolute_uri(settings.MEDIA_URL + relative_url)

        return Response(
            {"message": "Script Generated Successfully!", "download_url": download_url},
            status=status.HTTP_200_OK,
        )
    else:
        print(f"Invalid service type: {services}")
        return Response(
            {"error": f"Invalid service type: {services}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
