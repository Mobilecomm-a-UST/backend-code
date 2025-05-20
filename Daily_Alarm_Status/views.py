from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from collections import defaultdict
import pandas as pd
import json
import re
import os
import subprocess
from rest_framework import status
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL


def explode_data_from_log(command, start_point, row_patteren, end_point, file_content):
    command_found = False
    header_found = False
    header_values = []
    values = []
    ip_add = None
    date_time = None
    Node_ID = None

    ############################## Pattern for the log timestamp and IP information #################################
    log_pattern = re.compile(
        r"(\d{6}-\d{2}:\d{2}:\d{2}\+\d{4})\s+([\da-fA-F:.]+)\s+(\d+\.\d+[a-zA-Z]*)\s+([\w.-]+)\s+(stopfile=[/\w\d]+)"
    )

    ############################################## Compiled row pattern (rows to extract) ###########################
    row_pattern = re.compile(row_patteren)

    for line in file_content:
        line = line.strip()

        if not command_found and re.match(rf"{command}", line):
            print("[INFO] Command found:", line)
            command_found = True
            Node_ID = re.split(r">", line)[0].strip()
            continue

        if command_found:
            log_match = log_pattern.match(line)
            if log_match:
                date_time, ip_add, _, _, _ = log_match.groups()

            ################################## Check for header #################################################
            if not header_found:
                header_match = re.match(rf"{start_point}", line)
                if header_match:
                    header_found = True
                    header_values = (
                        list(header_match.groups())
                        if header_match.groups()
                        else header_match.group(0).split()
                    )
                    print("[INFO] Header found:", header_values)
                    continue

            ######################################### Check for end of block ####################################
            if header_found and re.match(rf"{end_point}", line):
                print("[INFO] End point matched, stopping...")
                break

            ######################################### Match actual data rows ###################################
            if header_found and not line.startswith("==="):
                row_match = row_pattern.search(line)
                if row_match:
                    values.append(list(row_match.groups()))
                else:
                    print("[DEBUG] Skipped line:", line)

    ##################################### Create DataFrame if values found #####################################
    if values and header_values:
        df = pd.DataFrame(values, columns=header_values)
        df["IP ADDR"] = ip_add
        df["Node_ID"] = Node_ID
        return df
    else:
        print("[WARN] No matching rows or headers found")
        return pd.DataFrame()


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
            elif cell_value == "Missing" or cell_value == "Missing in Post":
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

            # workbook.__save()


@api_view(["POST", "GET"])
def process_sdir_and_rru_status(request):
    try:
        all_files_df = pd.DataFrame()

        if request.method != "POST":
            return Response(
                {"error": "GET method not supported"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        files = request.FILES.getlist("sdir_files")
        for uploaded_file in files:
            file_content = [
                line.strip()
                for line in uploaded_file.read().decode("utf-8").splitlines()
            ]
            
            print(f"Processing file: {uploaded_file.name}")

            # Extract sdir command data
            sdir_df = explode_data_from_log(
                r"[A-Z0-9_-]+>\ssdir",
                r"(ID)\s+(RiL)\s+(Type)\s+(Res)\s(MO1-MO2)\s+(BOARD1-BOARD2)\s+(AlmIDs\sCells\s\(States\))\s+(Issue\s\(Failed\schecks\))",
                r"^\s*(\d+)\s+([A-Z_0-9\-]+)\s+([A-Z0-9]+)\s+(OK|NOK|OKW)\s+([A-Z0-9\(\)]+\s+[A-Z\-\d\(\)\_]+)\s+([A-Z0-9]+\s+[A-Z0-9]+)\s+((?:(?:TDD|FDD|NRC|GT)=[^()]+\s+)*(?:GT=[^()]+\s+)*(?:\([^)]+\)))?\s*(.*)$",
                r"^----{2,}+",
                file_content,
            )

            if sdir_df.empty:
                sdir_df = pd.DataFrame(columns=['ID', 'RiL', 'Type', 'Res', 'MO1-MO2', 'BOARD1', 'BOARD2', 'AlmIDs Cells (States)', 'Issue (Failed checks)', 'IP ADDR', 'Node_ID', 'RRU CELL MO'])

            sdir_df["RRU CELL MO"] = sdir_df["MO1-MO2"].apply(
                lambda x: re.search(r"(RRU-\d+)", x).group(1) if re.search(r"RRU-(\d+)", x) else None
            )

            # Extract st rru command data
            st_rru_df = explode_data_from_log(
                r"[A-Z0-9_-]+>\sst\srru",
                r"(Proxy)\s+(Adm\sState)\s+(Op\.\sState)\s+(MO)",
                r"\s*(\d+)\s+(\d+\s+\((?:UNLOCKED|LOCKED)\))\s+(\d+\s+\((?:ENABLED|DISABLED)\))\s+(.*)$",
                r"^Total:\s\d+",
                file_content,
            )

            if st_rru_df.empty:
                print(f"st_rru_df is empty for file: {uploaded_file.name}")
                st_rru_df = pd.DataFrame(columns=["Proxy", "Adm State", "Op. State", "MO", "RRU CELL MO"])
            else:
                st_rru_df["RRU CELL MO"] = st_rru_df["MO"].apply(
                    lambda x: x.split(",")[1].split("=")[1] if "," in x and "=" in x.split(",")[1] else x
                )

            ################################################################### Merge DataFrames ######################################################
            merge_cols = ["RRU CELL MO"] + [col for col in ["Node_ID", "IP ADDR"] if col in sdir_df.columns and col in st_rru_df.columns]

            result_df = pd.merge(sdir_df, st_rru_df, on=merge_cols, how="outer")

            if result_df.empty:
                result_df = pd.DataFrame(columns=['ID', 'RiL', 'Type', 'Res', 'MO1-MO2', 'BOARD1', 'BOARD2', 'AlmIDs Cells (States)', 'Issue (Failed checks)', 'IP ADDR', 'Node_ID', 'RRU CELL MO', 'Proxy', 'Adm State', 'Op. State', 'MO', 'RRU DOWN STATUS'])

            ####################################################################### Split BOARD1-BOARD2 ###################################################
            if "BOARD1-BOARD2" in result_df.columns:
                result_df.rename(columns={"BOARD1-BOARD2": "BOARD1"}, inplace=True)
                result_df[["BOARD1", "BOARD2"]] = result_df["BOARD1"].str.split(" ", n=1, expand=True).fillna("")

            ################################################################# RRU DOWN STATUS Calculation #######################################################
            result_df["RRU DOWN STATUS"] = result_df["Op. State"].apply(
                lambda x: "OK" if str(x).startswith("1") else None
            )
            result_df["RRU DOWN STATUS"] = result_df.apply(
                lambda row: row["RRU DOWN STATUS"] if row["RRU DOWN STATUS"] else f"NOT OK",
                axis=1
            )

            all_files_df = pd.concat([all_files_df, result_df], axis=0)
            all_files_df.fillna("", inplace=True).replace('nan', '', inplace=True)

        ################################################################ Save to Excel #######################################################
        timestamp = datetime.now().strftime("%Y-%m-%d %H_%M_%S")
        output_directory = os.path.join(settings.MEDIA_ROOT, "OUTPUT")
        os.makedirs(output_directory, exist_ok=True)
        file_name = f"ALARM_LOGS_V1.6_RRU_CONFIG_{timestamp}.xlsx"
        full_file_path = os.path.join(output_directory, file_name)

        with pd.ExcelWriter(full_file_path, engine="xlsxwriter") as writer:
            all_files_df.to_excel(writer, sheet_name="RRU ALARM DOWN", index=False)
            format_excel_sheet(writer, "RRU ALARM DOWN", all_files_df)

        download_url = os.path.join(settings.MEDIA_URL, "OUTPUT", file_name)
        return Response(
            {
                "status": True,
                "message": "Successfully fetched the rru status...",
                "download_url": download_url
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
