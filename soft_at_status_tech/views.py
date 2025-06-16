from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from pathlib import Path
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
            column_series.fillna("").astype(str).str.len().max(skipna=True) or 0,
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
            elif cell_value == "NOT OK" or cell_value == "NOK":
                format_style = not_ok_format
            elif cell_value == "Missing" or cell_value=="Missing in Post":
                format_style = workbook.add_format(
                    {
                        "bg_color": "#FF6347",
                        "font_color": "#FFFFFF",
                        "align": "center",
                        "valign": "center",
                        "bold": True,
                        "border": 1,
                    }
                )
            elif cell_value == "NA":
                format_style = workbook.add_format(
                    {
                        "bg_color": "#FCF259",
                        "font_color": "#222831",
                        "align": "center",
                        "valign": "center",
                        "bold": True,
                        "border": 1,
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

#################################################################################################
@api_view(["POST", "GET"])
def extract_data_from_log(request):
    # try:
        circle = request.POST.get("circle")
        files = request.FILES.getlist("files")
        base_name = None

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
        os.makedirs(log_folder, exist_ok=True)

        ##################################### DELETING THE PREVIOUS PROCESSED FILE AND SAVED NEW FILE #########################
        delete_existing_files(log_folder)
        delete_existing_files(output_path)
        delete_existing_files(log_excel_folder)
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
            try:
                base_name = os.path.basename(file_path)
                nodes = read_and_write_func(file_path)

                print(f"{file_path}:- ", len(nodes))

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
                    "get . gsmsec",
                    "get . fing"
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

                        elif command == "get . gsmsec":
                            header_line, values_lines, ip_address = get_data_from_log(
                                r"^[A-Z0-9_-]+>\sget\s\.\sgsmsec",
                                r"^MO  ",
                                r"Total:",
                                node,
                            )
                        elif command == "get . fing":
                            header_line, values_lines, ip_address = get_data_from_log(
                                r"^[A-Z0-9_-]+>\sget\s\.\sfing",
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
                file_key = Path(file_path).stem
                all_files_data[file_key] = node_data

                ############################################ LOGS EXCEL FILE #####################################################
                log_excel_folder = os.path.join(base_media_url, "logs_excel")
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

                # Create logs_excel directory if it doesn't exist
                if not os.path.exists(log_excel_folder):
                    os.makedirs(log_excel_folder, exist_ok=True)
                else:
                    try:
                        shutil.rmtree(log_excel_folder, onerror=on_rm_error)
                        os.makedirs(log_excel_folder, exist_ok=True)
                    except PermissionError as e:
                        print("Permission denied:- ", str(e))
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
                                            r"^(FieldReplaceableUnit=\d+|FieldReplaceableUnit=RRU-\d+)\s+([A-Za-z]+\s\d+\w+)\s+([A-Z0-9\s]+\/\d+)\s+([A-Z0-9\/]+)\s+(\d+)\s+([A-Z0-9]+)",
                                            value,
                                        ):
                                            match = re.search(
                                                r"^(FieldReplaceableUnit=\d+|FieldReplaceableUnit=RRU-\d+)\s+([A-Za-z]+\s\d+\w+)\s+([A-Z0-9\s]+\/\d+)\s+([A-Z0-9\/]+)\s+(\d+)\s+([A-Z0-9]+)",
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
                                            r"EUtranCell(FDD|TDD)=",
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
                                        lambda x: (str(x).split(",")[1] if "," in str(x) else x)
                                    )
                                    df = df.drop_duplicates(subset=["Node", "MO", "Attribute"])


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
                                            df["Adm State"].str.startswith("1", na=False)
                                            | df["Adm State"].str.startswith("0", na=False)
                                            | df["Op. State"].str.startswith("Equipment", na=False)
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

                                if command == "get . gsmsec" and not df.empty:
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
                                
                                if command == "invxgr":
                                    # df = df[df["RiL"].str.match(r"^\d+", na=False)]
                                    df = df[~df["RiL"].str.match(r"S[0-9]_N1-1", na=False)]
                                
                                if command == "get . fing":
                                    df = df[df["Attribute"].str.contains("fingerprint", na=False)]
                                print(df)
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
        # exit(0)
        excel_files_paths = [
            os.path.join(log_excel_folder, file)
            for file in os.listdir(log_excel_folder)
        ]
        print(excel_files_paths)

        for file in excel_files_paths:
            base_name = os.path.basename(file).split('_')[0]
            xls = pd.ExcelFile(file)

            template_path = os.path.join(template_file_path, "template.xlsx")
            template_df = pd.ExcelFile(
                template_path,
            ).parse()
            l_layers = [] 
            l_layers_replaced = []
            print(xls.sheet_names)
            for sheet_name in xls.sheet_names:
                if sheet_name == "st cell":
                    df = xls.parse(sheet_name)
                    circle = df["MO"].str.extract(r"EUtranCell(?:FDD|TDD)=([A-Z]{2})_")
                    layer = df["MO"].str.extract(r"EUtranCell(?:FDD|TDD)=\w+_(F\d|T\d)")[0]
                    print("layer:", layer)  
                    circle_clean = circle.dropna()

                    if not circle_clean.empty:
                        circle_value = circle_clean.iloc[0, 0].strip()
                    else:
                        circle_value = None
                    template_df.loc[0, 'Circle'] = circle_value
                    print("Circle:", circle_value)
                    layer_value = '_'.join(layer.dropna().unique()) if not layer.dropna().empty else "NA"
                    print("Layer Value:", layer_value)
                    layer_mapping = {
                        "F1": "L2100",
                        "F3": "L1800",
                        "F8": "L900",
                        "T1": "L2300",
                        "T2": "L2300",
                        "F5": "L850",
                    }
                    l_layers = [
                        layer_mapping.get(l, l) for l in layer_value.split("_")
                    ]
                    l_layers = list(set(l_layers))
                    template_df.loc[0, "Layers(Other Tech Info)"] = "_".join(l_layers)
                    print("Layer Value:", l_layers)
                
                site_ids = (
                    df["MO"].str.extract(r"EUtranCell(?:FDD|TDD)=([\w_]+)")[0].dropna()
                )
                for site_value in site_ids:
                    parts = site_value.split("_")
                    if len(parts) >= 5:
                        site = parts[4]
                        if site.startswith("X"):
                        # or site.startswith("X"):
                            site = site[1:]
                        if site[-1].isalpha():
                            site = site[:-1]
                        template_df.loc[0, "2G Site ID"] = site
                        # print("2G SiteID:",site)

                ant = df["MO"].str.extract(
                    r"EUtranCell(?:FDD|TDD)=[^\s,=]*([A-Z]_[A-Z])\b"
                ).dropna()
                ant = [val for val in ant[0].unique() if val.split("_")[0] == val.split("_")[1]]

                total_antennas = len(ant)
                print("Total unique antenna letters:", total_antennas)
                template_df.loc[0, "Antenna"] = (total_antennas)
                print("Antenna:", template_df.loc[0, "Antenna"])
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
                source_counts = cell_config.dropna().value_counts()
                band_counts_df = pd.DataFrame(
                    {
                        "band": cell_config.dropna().map(cell_mapping),
                        "count": cell_config.dropna().map(source_counts),
                    }
                )
                final_band_counts = (
                    band_counts_df.groupby("band")["count"].max().sort_index()
                )

                formatted_config = "+".join(
                    f"{band}({count})" for band, count in final_band_counts.items()
                )

                # print("Formatted LTE Config:", formatted_config)
                combined_config = formatted_config  # default to formatted_config


                if "st trx" in xls.sheet_names:
                    trx_df = xls.parse("st trx")
                    trx_data = trx_df["MO"].dropna()
                    trx_data = trx_data[trx_data.str.contains("GsmSector=")]

                    if not trx_data.empty:
                        # TRX exists → perform replacement
                        combined_config = formatted_config.replace("L18", "GL18").replace("L9", "GL9")

                template_df.loc[0, "Cells Configuration"] = combined_config


                if "st trx" in xls.sheet_names:
                    df = xls.parse("st trx")

                    # Check both TRX formats
                    mask_trx_numeric = df["MO"].str.contains(r"(Trx=\d+)", na=False)
                    mask_trx_alphanumeric = df["MO"].str.contains(r"(Trx=G\d+)", na=False)
                    if mask_trx_alphanumeric.any():
                        # other circle format (e.g., Trx=G1800-1)
                        l_layers_replaced = []
                        for layer in l_layers:
                            if layer == "L1800":
                                l_layers_replaced.append("GL1800")
                            elif layer == "L900":
                                l_layers_replaced.append("GL900")
                            else:
                                l_layers_replaced.append(layer)
                    elif mask_trx_numeric.any():
                        # other circle format (e.g., Trx=0, Trx=4)
                        l_layers_replaced = []
                        for layer in l_layers:
                            if layer == "L1800":
                                l_layers_replaced.append("GL1800")
                            elif layer == "L900":
                                l_layers_replaced.append("GL900")
                            else:
                                l_layers_replaced.append(layer)
                    else:
                        # No TRX info found
                        l_layers_replaced = l_layers if l_layers else []
                    # ADDITION: Check for presence of G1800/G900 etc. in the MO column even if not in l_layers
                    # if mask_trx_alphanumeric.any() or mask_trx_numeric.any():
                    #     trx_layers = set()
                    #     trx_matches = df["MO"].str.extract(r"Trx=G(\d+)", expand=False)
                    #     for band in trx_matches.dropna().unique():
                    #         trx_layers.add(f"GL{band}")
                    #     for layer in trx_layers:
                    #         if layer not in l_layers_replaced:
                    #             l_layers_replaced.append(layer)
                        
                    circle_value = template_df.loc[0, "Circle"] if "Circle" in template_df.columns else None

                    # Ensure GL1800 is included for TN
                    if circle_value == "TN":
                        if "G1800" not in l_layers_replaced:
                            l_layers_replaced.append("G1800")
                        
                        # Replace GL900 with L900
                        if "GL900" in l_layers_replaced:
                            l_layers_replaced.remove("GL900")
                            if "L900" not in l_layers_replaced:
                                l_layers_replaced.append("L900")
                                        
                    # Final output to template
                    combined_layers = "_".join(sorted(set(l_layers_replaced))) if l_layers_replaced else "NA"
                    template_df.loc[0, "Layers(Other Tech Info)"] = combined_layers
                    print("Layers(Other Tech Info):", combined_layers)

                MO_names = []

                if "get 0" in xls.sheet_names:
                    df_0 = xls.parse("get 0", header=None)

                    MO_name_0 = "/".join(
                        cell.split("=")[-1]
                        for cell in df_0.iloc[0]
                        if isinstance(cell, str) and "ManagedElement=" in cell
                    )
                    MO_names.append(MO_name_0)
                    print("MO Name 0:", MO_name_0)
                    template_df.loc[0, "MO Name"] = MO_name_0

                    # Fill in software version and physical site ID
                    template_df.loc[0, "SW Version"] = df_0[df_0.iloc[:, 1] == "swVersion"].iloc[0, 2]
                    physical_site = df_0[df_0.iloc[:, 1] == "userLabel"].iloc[0, 2]
                    template_df.loc[0, "Physical Site Id"] = physical_site

                    # Check for GSMSEC data
                    if "get . gsmsec" in xls.sheet_names:
                        if template_df.loc[0, "Circle"] == "DL":
                            df_gsmsec = xls.parse("get . gsmsec")
                            sector_names = df_gsmsec[df_gsmsec["Attribute"] == "gsmSectorName"]["Value"]

                            prefixes = (
                                sector_names.dropna()
                                .str.extract(r"([A-Z]+\d+)")[0]
                                .dropna()
                                .unique()
                            )

                            MO_name_gsmsec = ",".join(prefixes)
                            MO_names.append(MO_name_gsmsec)

                            final_MO_name = " / ".join(filter(None, MO_names))
                            print("Final MO Name:", final_MO_name)

                            template_df.loc[0, "MO Name"] = final_MO_name
                else:
                    template_df.loc[0, "MO Name"] = MO_name_0

                
                        
                if "get . fing" in xls.sheet_names :
                    df_fing = xls.parse("get . fing")
                    fing_value_series = df_fing[df_fing["Attribute"] == "fingerprint"]["Value"]
                    if not fing_value_series.empty:
                        fingerprint_mo = fing_value_series.iloc[0].strip() 
                        print("Fingerprint MO:", fingerprint_mo)
                        if fingerprint_mo == MO_name_0:
                            template_df.loc[0, "Project Remarks"] = f" On-Aired-“4G GPL parameter as per the guidelines are ok”"
                        else:
                            template_df.loc[0, "Project Remarks"] = f"On-Aired-“4G GPL parameter as per the guidelines are ok/Renaming site”"

                if sheet_name == "get . tac":
                    df = xls.parse(sheet_name)
                    tac = df["Value"].unique()
                    ip_address = df["ip address"].unique()
                    if len(tac) > 0 and len(ip_address) > 0:
                        template_df.loc[0, "TAC Name"] = str(tac[0]).replace(",", "")
                        template_df.loc[0, "4G Node IP"] = " / ".join(ip_address)
                    
                elif sheet_name == "get . enroll":
                    df = xls.parse(sheet_name)
                    OSS_match = df["Attribute"].str.extract(r"OU=([\w\d]+)")
                    if OSS_match.notna().any().values[0]:  # check if there's at least one match
                        OSS = OSS_match.dropna().iloc[0, 0].strip().upper()
                        OSS = OSS.replace("ENM", " ENM") if "ENM" in OSS else OSS
                        OSS = OSS.replace("DEL", "DL") if "DEL" in OSS else OSS
                        template_df["OSS Name/IP"] = template_df["OSS Name/IP"].astype(object)
                        template_df.loc[0, "OSS Name/IP"] = OSS
                    else:
                        template_df["OSS Name/IP"] = template_df["OSS Name/IP"].astype(object)
                        template_df.loc[0, "OSS Name/IP"] = "NA"
                    print("OSS Name/IP:", template_df.loc[0, "OSS Name/IP"])

                elif sheet_name == "get . bsc":
                    df = xls.parse(sheet_name)
                    technology = df["MO"].str.extract(r"EUtranCell(FDD|TDD)")[0]
                    tech_values = "_".join(technology.dropna().unique())
                    if df["MO"].str.contains("Gsm", na=False).any():
                        tech_values = f"2G_{tech_values}"
                        Bsc = str(df.loc[df["MO"].str.contains("Gsm", na=False), "Value"].iloc[0]).split("_")[0]
                    else:
                        Bsc = "NA"
                    template_df.loc[0, "Technology"] = tech_values
                    # print("Technology:", tech_values)
                    template_df.loc[0, "BSC (In Case Of NT/2G)"] = Bsc

                if sheet_name == "hget field prod":
                    df = xls.parse(sheet_name)
                    baseband = (
                        df["productName"]
                        .str.extract(r"Baseband\s+(\d+)", expand=False)
                        .dropna()
                    )
                    RAN_Processor = (
                        df["productName"]
                        .str.extract(r"RAN Processor\s+(\w+)", expand=False)
                        .dropna()
                    )
                    BB_count = baseband.count()
                    bb_str = f"BB{baseband.iloc[0]}*{BB_count}" if BB_count > 1 else (
                        f"BB{baseband.iloc[0]}" if not baseband.empty else ""
                    )
                    print("BB str:", bb_str)

                    ran_count = RAN_Processor.count()
                    ran_str = f"BB{RAN_Processor.iloc[0]}*{ran_count}" if ran_count > 1 else (
                        f"BB{RAN_Processor.iloc[0]}" if not RAN_Processor.empty else ""
                    )
                    print("ran str:", ran_str)

                    combined_str = " / ".join(filter(None, [bb_str, ran_str])) or "NA"
                    print(combined_str)
                    template_df.loc[0, "Hardware/BBU"] = combined_str

                    radio = df["productName"].str.extract(r"(?:Radio|RRUS)\s+(\d+\w+)", expand=False)
                    print("radio:", radio)
                    band = df["productNumber"].str.extract(r"(B\d+[A-Z]?)", expand=False)
                    print("band:", band)
                    combined = (radio + " " + band).dropna()
                    print("combined:", combined)

                    countRRU = combined.value_counts()
                    result = " + ".join(
                        f"{item}*{count}" for item, count in countRRU.items()
                    )

                    print("Grouped Radios:\n", result)
                    template_df.loc[0, "Hardware/RRU"] = result if result else "NA"


                elif sheet_name == "st rru":
                    df = xls.parse(sheet_name)
                    template_df.loc[0, "CPRI"] = len(df)

                elif sheet_name == "invxgr":
                    df = xls.parse(sheet_name)
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

                if "get . sectorc" in xls.sheet_names:
                    df = xls.parse("get . sectorc")
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

                    template_df["Parent Cell Name (In Case Of Twin Beam)"] = template_df["Parent Cell Name (In Case Of Twin Beam)"].astype(object)

                    if len(Twin_Beam) != 0:
                        template_df.loc[
                            0, "Parent Cell Name (In Case Of Twin Beam)"
                        ] = ", ".join(Twin_Beam)
                    else:
                        template_df.loc[
                            0, "Parent Cell Name (In Case Of Twin Beam)"
                        ] = "NA"

                    print("Parent Cell Name (In Case Of Twin Beam):", template_df.loc[0, 'Parent Cell Name (In Case Of Twin Beam)'])
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 3307b961670114346edbc8be3491fa24ee028c65
                else:
                    template_df.loc[0, "Parent Cell Name (In Case Of Twin Beam)"] = "NA"
                    print("Sheet 'get . sectorc' not found. Twin Beam set to NA.")
                                    
<<<<<<< HEAD
=======
=======

                    
>>>>>>> e9fbb2f0ffd83a86be30e3221846390e911f826f
>>>>>>> 3307b961670114346edbc8be3491fa24ee028c65
                if "st ret" in xls.sheet_names and "get . sectorc" in xls.sheet_names:
                    # Parse "st ret" sheet
                    df_st = xls.parse("st ret")
                    df_st['MO'] = df_st['MO'].astype(str)
                    df_st['AntennaUnitGroup'] = df_st['MO'].str.extract(r'AntennaUnitGroup=(\d+)')
                    valid_groups = df_st["AntennaUnitGroup"].dropna().unique()

                    # Parse "get . sectorc" sheet
                    df_sec = xls.parse("get . sectorc")
                    df_sec["SectorCarrier"] = df_sec["Value"].str.extract(r"SectorCarrier=(\d+)")
                    df_filtered = df_sec[df_sec["SectorCarrier"].isin(valid_groups)]

                    # Extract MO values
                    MO = df_filtered["MO"].str.extract(r"=([\w\d_]+)")
                    MO = MO.dropna().iloc[:, 0].tolist()
                    print("Filtered MOs:", MO)

                    if MO:
                        # Group MOs by base name (excluding last 3 characters)
                        grouped = {}
                        for mo in MO:
                            base = mo[:-3]
                            suffix = mo[-3:]
                            if base not in grouped:
                                grouped[base] = [suffix]
                            else:
                                grouped[base].append(suffix)

                        # Reconstruct MOs with grouped suffixes
                        result_list = [base + "&".join(suffixes) for base, suffixes in grouped.items()]
                        result = ",".join(result_list)
                        template_df.loc[0, "RET Configuration (Cell Name)"] = result
                    else:
                        result = "NA"
                        template_df.loc[0, 'RET Configuration (Cell Name)'] = result

                    print("RET Configuration (Cell Name):", result)

                    # Map frequency layer
                    RTT_map = {
                        "F1": "L2100",
                        "F3": "L1800",
                        "F8": "L900",
                        "T1": "L2300",
                        "T2": "L2300",
                        "F5": "L850",
                    }
                    # Extract unique layer types from grouped result
                    layers_found = set()
                    for base in grouped.keys():
                        for key in RTT_map:
                            if key in base:
                                layers_found.add(RTT_map[key])
                                break

                    if layers_found:
                        RTT_cell = "_".join(sorted(layers_found))
                    else:
                        RTT_cell = "NA"

                    template_df.loc[0, "RET Configured on (Layer)"] = RTT_cell
                    print("RET Configured on (Layer):", RTT_cell)

                else:
                    template_df.loc[0, "RET Configured on (Layer)"] = "NA"
                    template_df.loc[0, "RET Configuration (Cell Name)"] = "NA"
<<<<<<< HEAD
=======

<<<<<<< HEAD
=======
                # if "st ret" in xls.sheet_names and "get . sectorc" in xls.sheet_names:

                #     df_st = xls.parse("st ret")
                #     df_st['MO'] = df_st['MO'].astype(str)
                #     df_st['AntennaUnitGroup'] = df_st['MO'].str.extract(r'AntennaUnitGroup=(\d+)')
                #     # df_st["AntennaUnitGroup"] = df_st["MO"].str.extract(
                #     #     r"AntennaUnitGroup=(\d+)"
                #     # )
                #     valid_groups = df_st["AntennaUnitGroup"].dropna().unique()

                #     df_sec = xls.parse("get . sectorc")
                #     df_sec["SectorCarrier"] = df_sec["Value"].str.extract(
                #         r"SectorCarrier=(\d+)"
                #     )
                #     df_filtered = df_sec[df_sec["SectorCarrier"].isin(valid_groups)]

                #     MO = df_filtered["MO"].str.extract(r"=([\w\d_]+)")
                #     MO = MO.dropna().iloc[:, 0].tolist()
                #     print("Filtered MOs:", MO)

                #     if MO:
                #         base = str(MO[0])[:-3]
                #         print("base:", base)
                #         suffixes = [str(s)[len(base) :] for s in MO]
                #         print("suffixes:", suffixes)
                #         result = base + "&".join(suffixes)
                #         template_df.loc[0, "RET Configuration (Cell Name)"] = result
                #     else:
                #         result = "NA"
                #         template_df.loc[0, 'RET Configuration (Cell Name)'] = result
                #     print("RET Configuration (Cell Name):", result)
                #     RTT_map = {
                #         "F1": "L2100",
                #         "F3": "L1800",
                #         "F8": "L900",
                #         "T1": "L2300",
                #         "T2": "L2300",
                #         "F5": "L850",
                #     }

                #     RTT_cell = "NA"
                #     for key in RTT_map.keys():
                #         if key in result:
                #             RTT_cell = RTT_map[key]
                #             break

                #     template_df.loc[0, "RET Configured on (Layer)"] = RTT_cell

                # else:
                #     template_df.loc[0, "RET Configured on (Layer)"] = "NA"
                #     template_df.loc[0, "RET Configuration (Cell Name)"] = "NA"
>>>>>>> e9fbb2f0ffd83a86be30e3221846390e911f826f

>>>>>>> 3307b961670114346edbc8be3491fa24ee028c65
              
                if sheet_name == "get . maxtx":
                    df_maxtx = xls.parse(sheet_name)
                    df_nooftx = xls.parse("get . nooftx")
                    df_sectorc = xls.parse("get . sectorc")
                    output = ""

                    if not df_maxtx.empty and not df_nooftx.empty and not df_sectorc.empty:
                        # Step 1: Filter by common SectorCarrier (MO)
                        common_mo = df_maxtx["MO"].unique().tolist()
                        df_nooftx = df_nooftx[df_nooftx["MO"].isin(common_mo)]
                        df_sectorc = df_sectorc[df_sectorc["Value"].isin(common_mo)]

                        # Step 2: Map MO -> (Power, Tx)
                        power_tx_map = {}
                        for mo in common_mo:
                            power = df_maxtx[df_maxtx["MO"] == mo]["Value"].values
                            tx = df_nooftx[df_nooftx["MO"] == mo]["Value"].values
                            if power.size > 0 and tx.size > 0:
                                power_tx_map[mo] = (int(power[0]), int(tx[0]))

                        # Step 3: Map MO to Layer using sectorc and band mapping
                        MIMO_map = {
                            "F1": "L21",
                            "F3": "L18",
                            "F8": "L9",
                            "T1": "L23",
                            "T2": "L23",
                            "F5": "L85",
                        }

                        output_parts = []
                        for _, row in df_sectorc.iterrows():
                            mo = row["Value"]  # This is MO in sectorc
                            layer = row["MO"]  # This contains F1, F3, etc.
                            match = re.search(r"(F\d|T\d)", layer)
                            if match and mo in power_tx_map:
                                band = match.group(1)
                                mimo_layer = MIMO_map.get(band)
                                if mimo_layer:
                                    power, tx = power_tx_map[mo]
                                    power_watt = f"{power//1000}W"
                                    mimo_config = f"{tx}T{tx}R"
                                    combined = f"{power_watt}({mimo_config}){mimo_layer}"
                                    output_parts.append(combined)

                        output = ", ".join(sorted(set(output_parts)))
                        print("MIMO Power configuration:", output)
                        template_df.loc[0, "MIMO Power configuration"] = output if output else "NA"


                if sheet_name == "get . fing":
                    df = xls.parse(sheet_name)
                    fingerprint = df["Value"].unique()
                    # template_df.loc[0, "Fingerprint"] = fingerprint

                today = datetime.date.today()
                template_df.loc[0, "AT Offering Date"] = today.strftime("%d-%m-%Y")
                template_df.loc[0, "Scenario (In Case Of Swap)"] = "NA"
                template_df.loc[0, "Cell Name (New)"] = "NA"
                template_df.loc[0, "Link ID"] = "NA"

                ####################################### getting folders for final output #########################################
                output_path = os.path.join(base_media_url, "OUTPUT")

                os.makedirs(output_path, exist_ok=True)

                output_filename = f"_{base_name}_OUTPUT_{timestamp}.xlsx"
                output_path = os.path.join(output_path, output_filename)

                with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
                    
                    template_df.to_excel(writer, index=False)
                    format_excel_sheet(writer, "Sheet1", template_df)

        ############################################# MAkING THE ZIP FILE #########################################################
        import glob

        # Remove old zip files
        for old_zip in glob.glob(os.path.join(base_media_url, "OUTPUT_*.zip")):
            try:
                os.remove(old_zip)
                print(f"Deleted old zip: {old_zip}")
            except Exception as e:
                print(f"Failed to delete {old_zip}: {e}")



        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = os.path.join(base_media_url, f"SUMMARY_OUTPUT_{timestamp}.zip")
        # Create zip file with all Excel files
        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            logs_excel_folder = os.path.join(base_media_url, "OUTPUT")
            if os.path.exists(logs_excel_folder):
                for root, dirs, files in os.walk(logs_excel_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, base_media_url)
                        zipf.write(file_path, arcname)
        
        download_link = request.build_absolute_uri(MEDIA_URL + zip_filename)
        print(f"Output file created: {output_path}")
        print(f"Zip file created: {zip_filename}")
        ###########################################################################################################################
        return Response(
            {
                "status": True,
                "message": "Files processed successfully",
                "download_url": download_link,
            },
            status=HTTP_200_OK,
        )

    # except Exception as e:
    #     print("error:- ", str(e))
    #     return Response(
    #         {"status": "ERROR", "message": str(e)}, status=HTTP_400_BAD_REQUEST
    #     )