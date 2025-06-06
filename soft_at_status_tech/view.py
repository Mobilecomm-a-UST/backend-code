from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from pathlib import Path
from collections import Counter
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
import os
import re
import pandas as pd
import openpyxl
import xlsxwriter
import shutil
import stat
import datetime
import json
import zipfile


###################### TAKING ENM VALUES ####################################################


# SPLIT_PATTEREN = r"\[[A-Z_@]+scp-\d+-amos\([a-z0-9]+\)\s+~\]\$\s+amos\s+[a-fA-F0-9\.:]+"
SPLIT_PATTEREN = r"Checking ip contact...OK"


################################################################################################

""" 
    CREATE HELPER FUNCTIONES HERE ----------------------------------
"""


def read_and_write_func(file_path):
    ######### reading the file_path or file ################
    with open(file_path, "r") as file:
        log_content = file.readlines()

    joined_content = "".join(log_content)

    ##################### spliting text in the logs ################################
    nodes = re.split(rf"{SPLIT_PATTEREN}", joined_content)

    nodes = [node.strip().split("\n") for node in nodes if node.strip() and not node.startswith("Logging to file")]

    print("nodes list:- ",nodes[0])

    # exit(0)

    return nodes


def zip_folder(folder_path, output_zip):
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=folder_path)
                zipf.write(file_path, arcname)


def on_rm_error(func, path, exc_info):
    # Change the permission and retry
    os.chmod(path, stat.S_IWRITE)
    func(path)


def get_data_from_log(command, start_point, end_point, node):
    """
    this function is responsible for extracting header and values in the log files
    """

    values_lines = []
    header_line = None
    command_found = False
    header_found = False
    ip_address = None

    for line in node:
        line = line.strip()

        if re.match(rf"{command}", line):
            command_found = True
            continue

        if command_found:
            ip_match = re.match(
                r"(\d{6}-\d{2}:\d{2}:\d{2}\+\d{4})\s+([\da-fA-F:.]+)\s+(\d+\.\d+[a-zA-Z]*)\s+([\w.-]+)\s+(stopfile=[/\w\d]+)",
                line,
            )
            if ip_match:
                ip_address = ip_match.group(2)
            if re.match(rf"{start_point}", line):
                header_found = True
                header_line = line
                continue

            if header_found and re.match(rf"{end_point}", line):
                break

            if re.match(r"={2,}+", line):
                continue

            if header_found:
                values_lines.append(line)

    return header_line, values_lines, ip_address


def delete_existing_files(folder_path):
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")


def ensure_clean_directory(directory_path, clean=True):
    """
    Ensures a directory exists and optionally cleans it.
    If clean is True, removes existing files.
    If clean is False, just ensures directory exists.
    
    Args:
        directory_path (str): Path to the directory to ensure
        clean (bool): Whether to clean the directory
    """
    try:
        if clean and os.path.exists(directory_path):
            delete_existing_files(directory_path)
        
        # Create directory if it doesn't exist
        os.makedirs(directory_path, exist_ok=True)
    except Exception as e:
        print(f"Error managing directory {directory_path}: {str(e)}")
        raise


#################################################################################################


@api_view(["POST", "GET"])
def extract_data_from_log(request):
    try:
        circle = request.POST.get("circle")
        files = request.FILES.getlist("files")

        if not files:
            return Response(
                {"status": "ERROR", "message": "No files uploaded"},
                status=HTTP_400_BAD_REQUEST,
            )

        ############## DEFINEING THE PATH FOR TOOL MEDIA ######################
        base_media_url = os.path.join(MEDIA_ROOT, "soft_at_status")
        output_path = os.path.join(base_media_url, "OUTPUT")
        log_folder = os.path.join(base_media_url, "circle_LOGS")
        log_excel_folder = os.path.join(base_media_url, "logs_excel")
        
        # Clean only input directories, preserve output
        ensure_clean_directory(log_folder, clean=True)  # Clean input directory
        ensure_clean_directory(log_excel_folder, clean=True)  # Clean input directory
        ensure_clean_directory(output_path, clean=False)  # Don't clean output directory

        saved_files = []
        for file in files:
            file_path = os.path.join(log_folder, file.name)
            with open(file_path, "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            saved_files.append(file_path)

        ######################################################################################################################
        all_files_data = {}
        for file_path in saved_files:
            file_key = os.path.basename(file_path)
            try:
                nodes = read_and_write_func(file_path)

                print(f"{file_path}:- ", len(nodes))

                # base_name = os.path.basename(file_path)

                commands = [
                    "st cell",
                    "get 0",
                    "st ret",
                    "get . sectorc",
                    "get . enroll",
                    "get . bsc",
                    "get . tac",
                    "hget field prod",
                    "st rru",
                    "get . maxtx",
                    "get . nooftx",
                    "invxgr",
                    "st sync",
                    "st trx",
                    "get . Gsmsec",
                ]

                node_data = {}

                for node_index, node in enumerate(nodes):
                    node_key = f"node_{node_index+1}"
                    node_data[node_key] = {}

                    for command in commands:
                        if command == "st cell":
                            header_line, values_lines, ip_address = get_data_from_log(
                                r"^[A-Z0-9_-]+>\sst\scell", r"^Proxy", r"^Total:", node
                            )

                        elif command == "get 0":
                            header_line, values_lines, ip_address = get_data_from_log(
                                r"^[A-Z0-9_-]+>\sget\s0", r"^0", r"Total:", node
                            )

                        elif command == "st ret":
                            header_line, values_lines, ip_address = get_data_from_log(
                                r"^[A-Z0-9_-]+>\sst\sret",
                                r"^Proxy\s+Adm\s",
                                r"Total:",
                                node,
                            )

                        elif command == "get . sectorc":
                            header_line, values_lines, ip_address = get_data_from_log(
                                r"^[A-Z0-9_-]+>\sget\s\.\ssectorc",
                                r"^MO  ",
                                r"Total:",
                                node,
                            )

                        elif command == "get . enroll":
                            header_line, values_lines, ip_address = get_data_from_log(
                                r"^[A-Z0-9_-]+>\sget\s\.\senroll",
                                r"^MO  ",
                                r"Total:",
                                node,
                            )

                        elif command == "get . bsc":
                            header_line, values_lines, ip_address = get_data_from_log(
                                r"^[A-Z0-9_-]+>\sget\s\.\sbsc",
                                r"^MO  ",
                                r"Total:",
                                node,
                            )

                        elif command == "get . tac":
                            header_line, values_lines, ip_address = get_data_from_log(
                                r"^[A-Z0-9_-]+>\sget\s\.\stac",
                                r"^MO  ",
                                r"Total:",
                                node,
                            )

                        elif command == "hget field prod":
                            header_line, values_lines, ip_address = get_data_from_log(
                                r"^[A-Z0-9_-]+>\shget\sfield\sprod",
                                r"^MO  ",
                                r"Total:",
                                node,
                            )

                        elif command == "st rru":
                            header_line, values_lines, ip_address = get_data_from_log(
                                r"^[A-Z0-9_-]+>\sst\srru", r"^Proxy", r"Total:", node
                            )

                        elif command == "get . maxtx":
                            header_line, values_lines, ip_address = get_data_from_log(
                                r"^[A-Z0-9_-]+>\sget\s\.\smaxtx",
                                r"^MO  ",
                                r"Total:",
                                node,
                            )

                        elif command == "get . nooftx":
                            header_line, values_lines, ip_address = get_data_from_log(
                                r"^[A-Z0-9_-]+>\sget\s\.\snooftx",
                                r"^MO  ",
                                r"Total:",
                                node,
                            )

                        elif command == "invxgr":
                            header_line, values_lines, ip_address = get_data_from_log(
                                r"^[A-Z0-9_-]+>\sinvxgr",
                                r"^ID\s+LINK\s+RiL\s+WL1\s+TEMP1\s+TXbs1\sTXdBm1\s+RXdBm1\s+BER1\s+WL2\s+TEMP2\s+TXbs2\s+TXdBm2\s+RXdBm2\s+BER2\s+DlLoss\s+UlLoss\s+LENGTH\s+TT",
                                r"---{2,}+",
                                node,
                            )

                        elif command == "st sync":
                            header_line, values_lines, ip_address = get_data_from_log(
                                r"^[A-Z0-9_-]+>\sst\ssync",
                                r"^Proxy\s+Adm\s",
                                r"Total:",
                                node,
                            )

                        elif command == "st trx":
                            header_line, values_lines, ip_address = get_data_from_log(
                                r"^[A-Z0-9_-]+>\sst\strx",
                                r"^Proxy\s+Adm\s",
                                r"Total:",
                                node,
                            )

                        elif command == "get . Gsmsec":
                            header_line, values_lines, ip_address = get_data_from_log(
                                r"^[A-Z0-9_-]+>\sget\s\.\sGsmsec",
                                r"^MO  ",
                                r"Total:",
                                node,
                            )
                        else:
                            continue

                        node_data[node_key][command] = {
                            "header_line": header_line,
                            "values_lines": values_lines,
                            "ip_address": ip_address,
                        }

                # Save the parsed data for this filef
                all_files_data[file_key] = node_data

                ############################################ LOGS EXCEL FILE #####################################################
                log_excel_folder = os.path.join(base_media_url, "logs_excel")
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

                # Create logs_excel directory if it doesn't exist
            
                # if not os.path.exists(log_excel_folder):
                #     os.makedirs(log_excel_folder, exist_ok=True)
                # else:
                #     try:
                #         shutil.rmtree(log_excel_folder, onexc=on_rm_error)
                #         os.makedirs(log_excel_folder, exist_ok=True)
                #     except PermissionError as e:
                #         print("Permission denied:- ", str(e))

                #######################################################################################################
                # json_filename = os.path.join(
                #         log_excel_folder, f"{file_key}_{timestamp}.json"
                #     )

                #     # Save data as JSON
                # with open(json_filename, "w") as json_file:
                #     json.dump(node_data, json_file, indent=4)

                # Loop through each file's node_data in all_files_data
                ########################################################################################################

                for file_key, node_data in all_files_data.items():
                    # Create Excel file
                    excel_filename = os.path.join(
                        log_excel_folder, f"{file_key}_{timestamp}.xlsx"
                    )
                    ######################################## Extracting the text log data into Excel with cicrle wise excel files #############################
                    with pd.ExcelWriter(excel_filename, engine="xlsxwriter") as writer:
                        for command in commands:
                            node_dfs = []

                            for node, command_info in node_data.items():
                                if command not in command_info:
                                    continue

                                header = command_info[command].get("header_line", "")
                                values = command_info[command].get("values_lines", [])
                                ip_address = command_info[command].get("ip_address", "")

                                if command != "invxgr":
                                    if command == "hget field prod":
                                        header_split = (
                                            re.split(r"\s{1,}", header)
                                            if header
                                            else []
                                        )
                                    else:
                                        header_split = (
                                            re.split(r"\s{2,}", header)
                                            if header
                                            else []
                                        )
                                        value_split = (
                                            re.split(r"\s{1,}", values[0])
                                            if values
                                            else []
                                        )
                                        if len(header_split) > len(value_split):
                                            header_split = header_split[
                                                : len(value_split)
                                            ]
                                else:
                                    header_split = (
                                        re.split(r"\s{1,}", header) if header else []
                                    )
                                    header_split = [
                                        val
                                        for val in header_split
                                        if val not in ["BER1", "BER2"]
                                    ]

                                data_list = []
                                max_columns = 0
                                current_cell = None

                                for value in values:
                                    value = value.strip()
                                    if not value:
                                        continue

                                    if command == "get . sectorc":
                                        if re.match(r"^EUtranCell(FDD|TDD)=", value):
                                            current_cell = re.split(r"\s{2,}", value)[0]

                                        elif value.startswith(">>>") and current_cell:
                                            match = re.search(
                                                r"sectorCarrierRef\s*=\s*(ENodeBFunction=\d+,SectorCarrier=\d+)",
                                                value,
                                            )
                                            if match:
                                                ref_value = match.group(1)
                                                data_list.append(
                                                    [
                                                        node,
                                                        current_cell,
                                                        "sectorCarrierRef",
                                                        ref_value,
                                                    ]
                                                )
                                                max_columns = max(max_columns, 4)

                                    elif command == "hget field prod":
                                        if re.match(
                                            r"^(FieldReplaceableUnit=\d+|FieldReplaceableUnit=RRU-\d+)\s+([A-Za-z]+\s\d+)\s+([A-Z0-9\s]+\/\d+)\s+([A-Z0-9\/]+)\s+(\d+)\s+([A-Z0-9]+)",
                                            value,
                                        ):
                                            match = re.search(
                                                r"^(FieldReplaceableUnit=\d+|FieldReplaceableUnit=RRU-\d+)\s+([A-Za-z]+\s\d+)\s+([A-Z0-9\s]+\/\d+)\s+([A-Z0-9\/]+)\s+(\d+)\s+([A-Z0-9]+)",
                                                value,
                                            )
                                            mo = match.group(1)
                                            productName = f"{match.group(2)}"
                                            productNumber = match.group(3)
                                            productRevision = match.group(4)
                                            productionDate = match.group(5)
                                            serialNumber = match.group(6)
                                            data_list.append(
                                                [
                                                    node,
                                                    mo.strip(),
                                                    productName.strip(),
                                                    productNumber.strip(),
                                                    productRevision.strip(),
                                                    productionDate.strip(),
                                                    serialNumber.strip(),
                                                ]
                                            )
                                            max_columns = max(max_columns, 4)
                                        else:
                                            value_split = re.split(r"\s{2,}", value)
                                            data_list.append([node] + value_split)
                                            max_columns = max(
                                                max_columns, len(value_split)
                                            )

                                    else:
                                        if value.startswith(">>>"):
                                            continue

                                        if command == "invxgr":
                                            value_split = re.split(r"\s+", value)
                                        else:
                                            value_split = re.split(r"\s{2,}", value)

                                        data_list.append([node] + value_split)
                                        max_columns = max(max_columns, len(value_split))

                                if not data_list:
                                    continue

                                if len(header_split) < max_columns:
                                    header_split += [
                                        f"Column_{i+1}"
                                        for i in range(len(header_split), max_columns)
                                    ]

                                header_split.insert(0, "Node")

                                for i in range(len(data_list)):
                                    if len(data_list[i]) < len(header_split):
                                        data_list[i] += [""] * (
                                            len(header_split) - len(data_list[i])
                                        )

                                df = pd.DataFrame(data_list, columns=header_split)

                                if command == "st ret" and not df.empty:
                                    mask_equipment = (
                                        df["Op. State"]
                                        .astype(str)
                                        .str.startswith("Equipment=")
                                    )
                                    df.loc[mask_equipment, "MO"] = df.loc[
                                        mask_equipment, "Op. State"
                                    ]
                                    df.loc[mask_equipment, "Op. State"] = None

                                    mask_state = df["Adm State"].astype(
                                        str
                                    ).str.startswith("1 (ENABLED)") | df[
                                        "Adm State"
                                    ].astype(
                                        str
                                    ).str.startswith(
                                        "0 (DISABLED)"
                                    )
                                    df.loc[mask_state, "Op. State"] = df.loc[
                                        mask_state, "Adm State"
                                    ]
                                    df.loc[mask_state, "Adm State"] = None

                                if command == "get . bsc" and not df.empty:
                                    for idx, row in df.iterrows():
                                        if " " in str(row["Attribute"]):
                                            val = row["Attribute"].split(" ", 1)
                                            df.at[idx, "Attribute"] = val[0]
                                            df.at[idx, "Value"] = (
                                                val[1] if len(val) > 1 else ""
                                            )

                                if command == "get . tac" and not df.empty:
                                    for idx, row in df.iterrows():
                                        if " " in str(row["Attribute"]):
                                            val = row["Attribute"].split(" ", 1)
                                            df.at[idx, "Attribute"] = val[0]
                                            df.at[idx, "Value"] = (
                                                val[1] if len(val) > 1 else ""
                                            )
                                    df = df[
                                        df["MO"].str.contains(
                                            r"EUtranCell(FDD|TDD)=",
                                            na=False,
                                            regex=True,
                                        )
                                        & df["Attribute"].str.contains(
                                            r"tac", na=False, regex=True
                                        )
                                    ]
                                    df["ip address"] = ip_address

                                if command == "get . maxtx" and not df.empty:
                                    for idx, row in df.iterrows():
                                        if " " in str(row["Attribute"]):
                                            val = row["Attribute"].split(" ", 1)
                                            df.at[idx, "Attribute"] = val[0]
                                            df.at[idx, "Value"] = (
                                                val[1] if len(val) > 1 else ""
                                            )
                                    df = df[df["MO"].str.startswith(r"SectorCarrier=")]

                                if command == "get . sectorc" and not df.empty:
                                    df = df[
                                        df["MO"].str.contains(
                                            r"^EUtranCell(FDD|TDD)=",
                                            na=False,
                                            regex=True,
                                        )
                                        & df["Attribute"].str.contains(
                                            r"sectorCarrierRef", na=False, regex=True
                                        )
                                    ]
                                    df.drop(
                                        columns=["Column_4"],
                                        inplace=True,
                                        errors="ignore",
                                    )

                                    df["Value"] = df["Value"].apply(
                                        lambda x: (
                                            str(x).split(",")[1] if "," in str(x) else x
                                        )
                                    )

                                if command == "hget field prod" and not df.empty:
                                    if "productName" in df.columns:
                                        df = df[
                                            df["productName"].str.startswith("Radio", na=False)
                                            | df["productName"].str.startswith("RRUS", na=False)
                                            | df["productName"].str.startswith("Baseband", na=False)
                                            | df["productName"].str.startswith("RAN Processor", na=False)
                                        ]

                                if command == "get . nooftx" and not df.empty:
                                    for idx, row in df.iterrows():
                                        if " " in str(row["MO"]):
                                            ant_val = row["Attribute"]
                                            df.at[idx, "Value"] = ant_val
                                            val = row["MO"].split(" ", 1)
                                            df.at[idx, "Attribute"] = val[1]
                                            df.at[idx, "MO"] = row["MO"].split(" ", 1)[
                                                0
                                            ]
                                    df = df[df["MO"].str.startswith(r"SectorCarrier=")]

                                if command == "get . enroll" and not df.empty:
                                    if "MO" in df.columns:
                                        df = df[
                                            df["MO"].str.startswith("SecM", na=False)
                                            | (
                                                df["Attribute"].str.startswith(
                                                    "enrollment", na=False
                                                )
                                            )
                                        ]
                                        for idx, row in df.iterrows():
                                            if " " in str(row["MO"]):
                                                enr_val = row["Attribute"]
                                                df.at[idx, "Value"] = enr_val
                                                val = row["MO"].split(" ", 1)
                                                df.at[idx, "Attribute"] = val[1]
                                                df.at[idx, "MO"] = row["MO"].split(
                                                    " ", 1
                                                )[0]

                                if command == "st sync" and not df.empty:
                                    if "Adm State" in df.columns:
                                        df = df[
                                            df["Adm State"].str.startswith(
                                                "1", na=False
                                            )
                                            | (
                                                df["Op. State"].str.startswith(
                                                    "Equipment", na=False
                                                )
                                            )
                                        ]
                                        for idx, row in df.iterrows():
                                            if " " in str(row["Adm State"]):
                                                enr_val = row["Op. State"]
                                                df.at[idx, "MO"] = enr_val
                                                val = row["Adm State"].split(" ", 1)
                                                df.at[idx, "Op. State"] = val[1]
                                                df.at[idx, "Adm State"] = row[
                                                    "Adm State"
                                                ].split(" ", 1)[0]
                                if command == "st trx" and not df.empty:
                                    if "Adm State" in df.columns:
                                        df = df[
                                            df["Adm State"].str.startswith(
                                                "1", na=False
                                            )
                                            | df["Op. State"].str.startswith(
                                                "Equipment", na=False
                                            )
                                        ]
                                        for idx, row in df.iterrows():
                                            if " " in str(row["Adm State"]):
                                                val = row["MO"].split(",", 1)
                                                df.at[idx, "MO"] = (
                                                    val[1]
                                                    if len(val) > 1
                                                    else row["Op. State"]
                                                )
                                            gsm_sector_df = df[
                                                df["MO"].str.contains(
                                                    "GsmSector=", na=False
                                                )
                                            ]

                                if command == "get . Gsmsec" and not df.empty:
                                    if "MO" in df.columns:
                                        df = df[
                                            df["MO"].str.startswith(
                                                "GsmSector=", na=False
                                            )
                                        ]
                                        for idx, row in df.iterrows():
                                            if " " in str(row["MO"]):
                                                val = row["MO"].split(" ", 1)
                                                df.at[idx, "MO"] = (
                                                    val[1]
                                                    if len(val) > 1
                                                    else row["MO"]
                                                )
                                                df.at[idx, "Attribute"] = row[
                                                    "MO"
                                                ].split(" ", 1)[0]

                                node_dfs.append(df)

                            if not node_dfs:
                                continue
                            ################################### CONCATING THE ALL NODES DFS ##################################
                            all_node_df = pd.concat(node_dfs, axis=0, ignore_index=True)

                            sheet_name = command[:31]
                            all_node_df.to_excel(
                                writer, sheet_name=sheet_name, index=False
                            )

                            worksheet = writer.sheets[sheet_name]
                            worksheet.autofilter(
                                0, 0, len(all_node_df), len(all_node_df.columns) - 1
                            )
                            worksheet.freeze_panes(1, 1)
                            ###################################################################################################
                    print(f"Excel file created: {excel_filename}")

            except Exception as e:
                print(f"Error processing file {file_path}: {str(e)}")
                continue
        ################################## Making the template file path and template file existance #######################################
        template_file_path = os.path.join(base_media_url, "template_file")

        if not os.path.exists(template_file_path):
            os.makedirs(template_file_path, exist_ok=True)

        
        ####################################################################################################################################
        excel_files_paths = [
            os.path.join(log_excel_folder, file)
            for file in os.listdir(log_excel_folder)
        ]
        print(excel_files_paths)

        for file in excel_files_paths:
            xls = pd.ExcelFile(file)

            template_path = os.path.join(template_file_path, "template.xlsx")
            template_df = pd.ExcelFile(
                template_path,
            ).parse()
            # circle_value = None
            print(xls.sheet_names)
            for sheet_name in xls.sheet_names:
                if sheet_name == "st cell":
                    df = xls.parse(sheet_name)
                    circle = df["MO"].str.extract(r"EUtranCellFDD=([A-Z]{2})_")
                    layer = df["MO"].str.extract(r"EUtranCell(?:FDD|TDD)=\w+([FT]\d)")[
                        0
                    ]
                    if not circle.empty:
                        circle_value = next((x.strip() for x in circle[0].dropna()), "NA")
                        template_df.loc[0, 'Circle'] = circle_value

                        layer_value = '_'.join(layer.dropna().unique()) if not layer.dropna().empty else "NA"
                        # template_df.loc[0, 'Layer'] = layer_value

                        # circle_value = circle.dropna().iloc[0, 0].strip()
                        # template_df.loc[0, "Circle"] = circle_value

                        # layer_value = "_".join(layer.dropna().unique())
                        layer_mapping = {
                            "F1": "L2100",
                            "F3": "L1800",
                            "F8": "L900",
                            "T1": "L2300",
                            "T2": "L2300",
                            "F5": "L850",
                        }
                        # layer_value = [layer_mapping.get(l, l) for l in layer_value.split('_')]
                        # layer_value = '_'.join(set(layer_value))
                        l_layers = [
                            layer_mapping.get(l, l) for l in layer_value.split("_")
                        ]
                        l_layers = list(set(l_layers))
                        template_df.loc[0, "Layers(Other Tech Info)"] = "_".join(
                            l_layers
                        )
                        # print("Layer Value:", l_layers)

                    ant = df["MO"].str.extract(
                        r"EUtranCell(?:FDD|TDD)=[^\s,=]*([A-Z]_[A-Z])\b"
                    ).dropna()
                    ant = [val for val in ant[0].unique() if val.split("_")[0] == val.split("_")[1]]

                    total_antennas = len(ant)
                    # print("Total unique antenna letters:", total_antennas)
                    template_df.loc[0, "Antenna"] = total_antennas

                    # Existing config extraction from MO sheet
                    cell_config = df["MO"].str.extract(
                        r"EUtranCell(?:FDD|TDD)=\w+([FT]\d)"
                    )[0]
                    cell_mapping = {
                        "F1": "L21",
                        "F3": "L18",
                        "F8": "L9",
                        "T1": "L23",
                        "T2": "L23",
                        "F5": "L85",
                    }
                    # Now, count each source code (F1, T1 etc.)
                    source_counts = cell_config.dropna().value_counts()

                    # Create a DataFrame of band counts with both mapped band and count
                    band_counts_df = pd.DataFrame(
                        {
                            "band": cell_config.dropna().map(cell_mapping),
                            "count": cell_config.dropna().map(source_counts),
                        }
                    )

                    # Drop duplicates within each band, keeping the max count per band
                    final_band_counts = (
                        band_counts_df.groupby("band")["count"].max().sort_index()
                    )

                    formatted_config = "+".join(
                        f"{band}({count})" for band, count in final_band_counts.items()
                    )

                    print("Formatted LTE Config:", formatted_config)

                    if "st trx" in xls.sheet_names:
                        trx_df = xls.parse("st trx")
                        trx_data = trx_df["MO"].dropna()
                        trx_data = trx_data[trx_data.str.contains("GsmSector=")]
                        trx_base = trx_data.str.replace(r"-\d+$", "", regex=True)
                        # Drop duplicates — keep one per unique 'GsmSector=X,Trx=G1800'
                        final_trx_data = trx_base.drop_duplicates().sort_values()
                        band_mapping = {"G900": "G9", "G1800": "G18"}
                        bands = final_trx_data.str.extract(r"Trx=(G\d+)")[0].map(
                            band_mapping
                        )
                        band_counts = bands.value_counts().sort_index()
                        trx_config = "+".join(
                            f"{band}({count})" for band, count in band_counts.items()
                        )
                        # print("TRX Config:\n", trx_config)
                        combined_config = (
                            formatted_config + "+" + trx_config
                            if formatted_config
                            else trx_config
                        )
                    else:
                        combined_config = formatted_config

                    template_df.loc[0, "Cells Configuration"] = combined_config
                    print(
                        "Final Cell Configurations:\n",
                        template_df.loc[0, "Cells Configuration"],
                    )

                    site_ids = (
                        df["MO"].str.extract(r"EUtranCellFDD=([\w_]+)")[0].dropna()
                    )
                    for site_value in site_ids:
                        parts = site_value.split("_")
                        if len(parts) >= 5:
                            site = parts[4]
                            if site.startswith("B") or site.startswith("X"):
                                site = site[1:]
                            if site[-1].isalpha():
                                site = site[:-1]
                            template_df.loc[0, "2G Site ID"] = site
                            # print("2G SiteID:",site)

                


                if "st trx" in xls.sheet_names:
                    df = xls.parse("st trx")
                    trx_mask = df["MO"].str.contains("GsmSector=")

                    if trx_mask.any():
                        df_trx = df[trx_mask]
                        trx_values = (
                            df_trx["MO"].str.extract(r"Trx=(G\d+)")[0].dropna().unique()
                        )
                        # print("TRX Values:", trx_values)
                        # Generate GL-prefixed values like GL1800, GL900
                        gl_layers = [
                            f"GL{v[1:]}" for v in trx_values if v in ["G1800", "G900"]
                        ]
                        # print("GL Layers:", gl_layers)
                        gl_freqs = [v[2:] for v in gl_layers]
                        l_layers = [l for l in l_layers if l[1:] not in gl_freqs]
                        combined_layers = "_".join(sorted(gl_layers + l_layers))
                        # print("Combined Layers:", combined_layers)
                        template_df.loc[0, "Layers(Other Tech Info)"] = combined_layers
                    else:
                        template_df.loc[0, "Layers(Other Tech Info)"] = "NA"

                MO_names = []

                if "get 0" in xls.sheet_names:
                    df_0 = xls.parse("get 0", header=None)
                    MO_name_0 = "/".join(
                        cell.split("=")[-1]
                        for cell in df_0.iloc[0]
                        if isinstance(cell, str) and "ManagedElement=" in cell
                    )
                    MO_names.append(MO_name_0)

                    template_df.loc[0, "SW Version"] = df_0[
                        df_0.iloc[:, 1] == "swVersion"
                    ].iloc[0, 2]

                    physical_site = df_0[df_0.iloc[:, 1] == "userLabel"].iloc[0, 2]

                    #     # Check if physical_site contains any of the DL circles
                    #     if any(dl in physical_site for dl in ["DL"]):
                    template_df.loc[0, "Physical Site Id"] = physical_site
                    # print("Physical Site Id:", template_df.loc[0, 'Physical Site Id'])

                #     else:
                #         # Add a new row at the end for other circles
                #         new_row_index = len(template_df)
                #         template_df.loc[new_row_index, 'Physical Site Id'] = physical_site

                if "get . Gsmsec" in xls.sheet_names:
                    if template_df.loc[0, "Circle"] == "DL":
                        df_gsmsec = xls.parse("get . Gsmsec")
                        sector_names = df_gsmsec[
                            df_gsmsec["Attribute"] == "gsmSectorName"
                        ]["Value"]
                        prefixes = (
                            sector_names.dropna()
                            .str.extract(r"([A-Z]+\d+)")[0]
                            .dropna()
                            .unique()
                        )
                        MO_name_gsmsec = ",".join(prefixes)
                        MO_names.append(MO_name_gsmsec)

                        final_MO_name = " / ".join(filter(None, MO_names))
                        # print("Combined MO Name:", final_MO_name)

                        template_df.loc[0, "MO Name"] = final_MO_name
                    else:
                        template_df.loc[0, "MO Name"] = MO_name_0

                if sheet_name == "get . tac":
                    df = xls.parse(sheet_name)
                    tac = df["Value"].unique()
                    ip_address = df["ip address"].unique()
                    if len(tac) > 0 and len(ip_address) > 0:
                        template_df.loc[0, "TAC Name"] = str(tac[0]).replace(",", "")
                        template_df.loc[0, "4G Node IP"] = " / ".join(ip_address)

                elif sheet_name == "get . enroll":
                    df = xls.parse(sheet_name)
                    OSS = df["Attribute"].str.extract(r"OU=([\w\d]+)")
                    if not OSS.empty:
                        OSS = OSS.dropna().iloc[0, 0].strip().upper()
                        OSS = OSS.replace("ENM", " ENM") if "ENM" in OSS else OSS
                        OSS = OSS.replace("DEL", "DL") if "DEL" in OSS else OSS
                        template_df.loc[0, "OSS Name/IP"] = OSS

                elif sheet_name == "get . bsc":
                    df = xls.parse(sheet_name)
                    technology = df["MO"].str.extract(r"EUtranCell(FDD|TDD)")[0]
                    tech_values = "_".join(technology.dropna().unique())
                    if "Gsm" in df.loc[0, "MO"]:
                        tech_values = f"2G_{tech_values}"
                        Bsc = str(df.loc[0, 'Value']).split('_')[0]

                        # Bsc = df.loc[0, "Value"].split("_")[0]
                    else:
                        Bsc = "NA"
                    template_df.loc[0, "Technology"] = tech_values
                    # print("Technology:", tech_values)
                    template_df.loc[0, "BSC (In Case Of NT/2G)"] = Bsc

                if sheet_name == "hget field prod":
                    df = xls.parse(sheet_name)
                    baseband = (
                        df["productName"]
                        .str.extract(r"Baseband\s+(\w+)", expand=False)
                        .dropna()
                    )
                    RAN_Processor = (
                        df["productName"]
                        .str.extract(r"RAN Processor\s+(\w+)", expand=False)
                        .dropna()
                    )
                    bb_str = f"BB{baseband.iloc[0]}" if not baseband.empty else ""
                    ran_str = f"BB{RAN_Processor.iloc[0]}" if not RAN_Processor.empty else ""
                    
                    combined_str = " / ".join(filter(None, [bb_str, ran_str])) or "NA"
                    print(combined_str)
                    template_df.loc[0, "Hardware/BBU"] = combined_str

                    radio = df["productName"].str.extract(r"(?:Radio|RRUS)\s+(\d+)", expand=False)
                    band = df["productNumber"].str.extract(
                        r"(B\d+[A-Z]?)", expand=False
                    )
                    combined = (radio + " " + band).dropna()

                    countRRU = combined.value_counts()
                    result = " + ".join(
                        f"{item}*{count}" for item, count in countRRU.items()
                    )

                    # print("Grouped Radios:\n", result)
                    template_df.loc[0, "Hardware/RRU"] = result if result else "NA"

                elif sheet_name == "st rru":
                    df = xls.parse(sheet_name)
                    template_df.loc[0, "CPRI"] = len(df)

                elif sheet_name == "invxgr":
                    df = xls.parse(sheet_name)
                    # cprilength = df["LENGTH"].str.replace("m", "")

                    # template_df.loc[0, "CPRI length as per Actual"] = "/".join(
                    #     cprilength
                    # )
                    cprilength = df['LENGTH'].dropna().astype(str).str.replace('m', '')
                    template_df.loc[0, 'CPRI length as per Actual'] = '/'.join(cprilength)

                    def round_to_nearest_5(n):
                        remainder = n % 5
                        if remainder >= 3:
                            return n + (5 - remainder)
                        else:
                            return n - remainder

                    cpri_length_as_per_mo = "/".join(
                        [
                            str(round_to_nearest_5(int(value)))
                            for i, value in enumerate(cprilength)
                        ]
                    )

                    template_df.loc[0, "CPRI length as per MO"] = cpri_length_as_per_mo
                    template_df.loc[0, "CPRI length as per Survey"] = (
                        cpri_length_as_per_mo
                    )

                elif sheet_name == "get . sectorc":
                    df = xls.parse(sheet_name)
                    Twin_Beam = df["MO"].to_list()
                    Twin_Beam = [str(val).split("=")[1] for val in Twin_Beam]
                    # print(Twin_Beam)
                    Twin_Beam = [
                        val for val in Twin_Beam if val.endswith(("_M", "_N", "_L"))
                    ]
                    Twin_Beam = [
                        re.sub(
                            r"_(M|N|L)$",
                            lambda m: {"L": "_A", "M": "_B", "N": "_C"}[m.group(1)],
                            val,
                        )
                        for val in Twin_Beam
                    ]
                    if len(Twin_Beam) != 0:
                        template_df.loc[
                            0, "Parent Cell Name (In Case Of Twin Beam)"
                        ] = ", ".join(Twin_Beam)
                    else:
                        template_df.loc[
                            0, "Parent Cell Name (In Case Of Twin Beam)"
                        ] = "NA"

                    # print("Parent Cell Name (In Case Of Twin Beam):", template_df.loc[0, 'Parent Cell Name (In Case Of Twin Beam)'])

                if "st ret" in xls.sheet_names and "get . sectorc" in xls.sheet_names:

                    df_st = xls.parse("st ret")
                    df_st['MO'] = df_st['MO'].astype(str)
                    df_st['AntennaUnitGroup'] = df_st['MO'].str.extract(r'AntennaUnitGroup=(\d+)')

                    # df_st["AntennaUnitGroup"] = df_st["MO"].str.extract(
                    #     r"AntennaUnitGroup=(\d+)"
                    # )
                    valid_groups = df_st["AntennaUnitGroup"].dropna().unique()

                    df_sec = xls.parse("get . sectorc")
                    df_sec["SectorCarrier"] = df_sec["Value"].str.extract(
                        r"SectorCarrier=(\d+)"
                    )
                    df_filtered = df_sec[df_sec["SectorCarrier"].isin(valid_groups)]

                    MO = df_filtered["MO"].str.extract(r"=([\w\d_]+)")
                    MO = MO.dropna().iloc[:, 0].tolist()
                    # print("Filtered MOs:", MO)
                    if MO:
                        base = str(MO[0])[:-3]
                        suffixes = [str(s)[len(base):] for s in MO]
                        result = base + "&".join(suffixes)
                        template_df.loc[0, 'RET Configuration (Cell Name)'] = result
                    else:
                        result = "NA"
                        template_df.loc[0, 'RET Configuration (Cell Name)'] = result

                    # if MO:
                    #     base = str(MO[0])[:-3]
                    #     suffixes = [str(s)[len(base) :] for s in MO]
                    #     result = base + "&".join(suffixes)
                    # template_df.loc[0, "RET Configuration (Cell Name)"] = result
                    # print("RET Configuration (Cell Name):", result)
                    RTT_map = {
                        "F1": "L2100",
                        "F3": "L1800",
                        "F8": "L900",
                        "T1": "L2300",
                        "T2": "L2300",
                        "F5": "L850",
                    }

                    RTT_cell = "NA"
                    for key in RTT_map.keys():
                        if key in result:
                            RTT_cell = RTT_map[key]
                            break

                    template_df.loc[0, "RET Configured on (Layer)"] = RTT_cell

                else:
                    template_df.loc[0, "RET Configured on (Layer)"] = "NA"
                    template_df.loc[0, "RET Configuration (Cell Name)"] = "NA"

                if sheet_name == "get . maxtx":
                    df_maxtx = xls.parse(sheet_name)
                    df_nooftx = xls.parse("get . nooftx")
                    df_sectorc = xls.parse("get . sectorc")
                    output = ""

                    if (
                        not df_maxtx.empty
                        and not df_nooftx.empty
                        and not df_sectorc.empty
                    ):
                        sector_mo = df_maxtx["MO"].unique().tolist()
                        if sector_mo:
                            df_nooftx = df_nooftx[df_nooftx["MO"].isin(sector_mo)]
                            df_sectorc = df_sectorc[df_sectorc["Value"].isin(sector_mo)]

                            print(df_sectorc)
                            # exit(0)
                            watt_values = df_maxtx["Value"].unique().tolist()
                            layer_values = df_sectorc["MO"].unique().tolist()

                            mimo_matches = df_maxtx["MO"].astype(str).str.extract(r'(\d+T\d+R)', expand=False).dropna()
                            if not mimo_matches.empty:
                                MIMO_config = Counter(mimo_matches).most_common(1)[0][0]
                            else:
                                MIMO_config = "2T2R"  # default fallback
                            MIMO_map = {
                                "F1": "L21",
                                "F3": "L18",
                                "F8": "L9",
                                "T1": "L23",
                                "T2": "L23",
                                "F5": "L85",
                            }

                            # Extract band keys from layer_values
                            band_keys = set()
                            for layer in layer_values:
                                match = re.search(r"(F\d|T\d)", layer)
                                if match:
                                    band_keys.add(match.group(1))

                            # Filter unique present MIMO bands
                            present_bands = {
                                key: MIMO_map[key]
                                for key in band_keys
                                if key in MIMO_map
                            }

                            if present_bands:

                                for band_key, band_value in present_bands.items():
                                    print(f"{band_key}: {band_value}")

                            output_parts = []
                            for power in watt_values:
                                power_watt = f"{power//1000}W"
                                for key in present_bands:
                                    combined = f"{power_watt}({MIMO_config}){present_bands[key]}"
                                    output_parts.append(combined)

                            # Make sure output has only unique parts
                            output = ", ".join(sorted(set(output_parts)))
                            print("MIMO Power configuration:", output)
                        template_df.loc[0, "MIMO Power configuration"] = output

                today = datetime.date.today()
                template_df.loc[0, "AT Offering Date"] = today.strftime("%d-%m-%Y")
                template_df.loc[0, "Scenario (In Case Of Swap)"] = "NA"
                template_df.loc[0, "Cell Name (New)"] = "NA"
                template_df.loc[0, "Link ID"] = "NA"

                ####################################### getting folders for final output #########################################
                output_path = os.path.join(base_media_url, "OUTPUT")
                output_filename = f"{file_key}_OUTPUT_{timestamp}.xlsx"
                save_path = os.path.join(output_path, output_filename)

                with pd.ExcelWriter(save_path, engine="xlsxwriter") as writer:
                    template_df.to_excel(writer, index=False)

        ############################################# MAkING THE ZIP FILE #########################################################
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = os.path.join(base_media_url, f"OUTPUT_{timestamp}.zip")
        # Create zip file with all Excel files
        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            logs_excel_folder = os.path.join(base_media_url, "OUTPUT")
            if os.path.exists(logs_excel_folder):
                for root, dirs, files in os.walk(logs_excel_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, base_media_url)
                        zipf.write(file_path, arcname)
        print(f"Output file created: {output_path}")
        print(f"Zip file created: {zip_filename}")
        ###########################################################################################################################
        return Response(
            {
                "status": "OK",
                "message": "Files processed successfully",
                "download_url": zip_filename,
            },
            status=HTTP_200_OK,
        )

    except Exception as e:
        print("error:- ", str(e))
        return Response(
            {"status": "ERROR", "message": str(e)}, status=HTTP_400_BAD_REQUEST
        )