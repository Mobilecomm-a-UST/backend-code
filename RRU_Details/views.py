from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from collections import defaultdict
import pandas as pd
import json
import re
import os
import zipfile
import stat
import shutil
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL




def on_rm_error(func, path, exc_info):
    # Change the permission and retry
    os.chmod(path, stat.S_IWRITE)
    func(path)
    

def explode_data_from_log(command, start_pattern, row_pattern, end_pattern, file_content):
    command_found = False
    header_found = False
    header_values = []
    data_rows = []
    node_id = None
    ip_addr = None
    timestamp = None

      #################################### Compile patterns ###############################################################
    command_regex = re.compile(command)
    start_regex = re.compile(start_pattern)
    row_regex = re.compile(row_pattern)
    end_regex = re.compile(end_pattern)
    log_info_regex = re.compile(
        r'(\d{6}-\d{2}:\d{2}:\d{2}\+\d{4})\s+([\da-fA-F:.]+)\s+(\d+\.\d+[a-zA-Z]*)\s+([\w.-]+)\s+(stopfile=[/\w\d]+)'
    )

    for line in file_content:
        line = line.strip()
######################################## Detect command line ##################################################################
        if not command_found and command_regex.match(line):
                print(f"[INFO] Command found: {line}")
                command_found = True
                node_id = line.split('>')[0].strip()
                continue

################################## If we encounter a new prompt before finding header or finishing ##############################
        if command_found and header_found==False and re.match(r'^[A-Z0-9_-]+>', line):
                print(f"[INFO] New prompt detected, ending block for {node_id}")
                break

        ################################### Optional log info extraction ######################################################
        log_match = log_info_regex.match(line)
        if log_match:
                timestamp, ip_addr, *_ = log_match.groups()

        #################################### Detect header #########################################
        if command_found and not header_found:
                header_match = start_regex.match(line)
                if header_match:
                    header_found = True
                    header_values = list(header_match.groups()) or header_match.group(0).split()
                    print(f"[INFO] Header found: {header_values}")
                    continue

        ####################################### Detect end of the block ###############################
        if command_found and header_found and end_regex.match(line):
                print(f"[INFO] End pattern matched. Stopping data collection for {node_id}.")
                break

        ####################################### Collect row data ####################################
        if command_found and header_found and not line.startswith('==='):
                row_match = row_regex.search(line)
                if row_match:
                    data_rows.append(list(row_match.groups()))
                else:
                    print(f"[DEBUG] Skipped line: {line}")

    ############################################ Return DataFrame #################################
    if data_rows and header_values:
        df = pd.DataFrame(data_rows, columns=header_values)
        df['Site_ID'] = node_id
        # df['IP_Addr'] = ip_addr
        # df['Timestamp'] = timestamp
        return df
    else:
        if not header_found:
                print(f"[ERROR] Command found but header pattern did not match.")
        print("[WARN] No matching data rows or headers found.")
        return pd.DataFrame()


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
def rru_details_upload(request):

    # Start with empty dataframe to hold combined data
    all_files_df = pd.DataFrame()

    circle = request.POST.get("circle")
    files = request.FILES.getlist("files")

    if not files:
        return Response(
            {"status": "ERROR", "message": "No files uploaded"},
            status=HTTP_400_BAD_REQUEST,
        )

    # Setup directories
    base_media_url = os.path.join(MEDIA_ROOT, "RRU_Details")
    output_path = os.path.join(base_media_url, "OUTPUT")
    log_folder = os.path.join(base_media_url, "circle_LOGS")
    log_excel_folder = os.path.join(base_media_url, "logs_excel")

    os.makedirs(log_folder, exist_ok=True)
    os.makedirs(output_path, exist_ok=True)
    
    # Delete old files
    delete_existing_files(log_folder)
    delete_existing_files(output_path)
    delete_existing_files(log_excel_folder)

    # Save uploaded files to disk
    saved_files = []
    for file in files:
        file_path = os.path.join(log_folder, file.name)
        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        saved_files.append(file_path)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Recreate logs_excel folder cleanly
    try:
        if os.path.exists(log_excel_folder):
            shutil.rmtree(log_excel_folder, onerror=on_rm_error)
        os.makedirs(log_excel_folder, exist_ok=True)
    except PermissionError as e:
        print("Permission denied while deleting log_excel_folder:", str(e))

    # Process each uploaded file
    for uploaded_file in saved_files:
        node_name = os.path.splitext(os.path.basename(uploaded_file))[0]
        excel_filename = os.path.join(log_excel_folder, f"{node_name}_{timestamp}.xlsx")

        try:
            with open(uploaded_file, "r") as file:
                file_content = file.readlines()

            # Use your regex here
            hget_field_prod_df = explode_data_from_log(
                r'[A-Z0-9_-]+>\shget\sfi\sprod',
                r'MO\s+productName\s+productNumber\s+productRevision\s+productionDate\s+serialNumber',
                r'(FieldReplaceableUnit=[\w\-]+)\s+([\w\s]+?)\s+(K[A-Z]{1,2}\s*\d+\s*\d*\/\d+|KDU\d+\/\d+)\s+(\S+[A-Z])\s+(\d{8})\s+(\S+)$',
                r'^Total:\s\d+',
                file_content
            )

            if not hget_field_prod_df.empty:
                # Write to individual Excel file
                with pd.ExcelWriter(excel_filename, engine="xlsxwriter") as writer:
                    hget_field_prod_df.to_excel(writer, sheet_name="sheet1", index=False)
                    format_excel_sheet(writer, "sheet1", hget_field_prod_df)

                # Add this file's data to combined df
                all_files_df = pd.concat([all_files_df, hget_field_prod_df], ignore_index=True)

        except Exception as e:
            print(f"❌ Error processing file {uploaded_file}: {e}")
            continue  # Skip to next file if error occurs

    # Write combined output file
    output_filename = f"{circle}RRU_OUTPUT_{timestamp}.xlsx"
    output_filepath = os.path.join(output_path, output_filename)

    with pd.ExcelWriter(output_filepath, engine="xlsxwriter") as writer:
        all_files_df.to_excel(writer, index=False, sheet_name="RRU Details")
        format_excel_sheet(writer, "RRU Details", all_files_df)

    # Download URL
    download_link = request.build_absolute_uri(
        os.path.join(MEDIA_URL, "RRU_Details", "OUTPUT", output_filename)
    )

    return Response(
        {
            "status": True,
            "message": "Files processed successfully",
            "download_url": download_link,
            "processed_files": len(saved_files),
            "total_rrus": len(all_files_df),
        },
        status=HTTP_200_OK,
    )
