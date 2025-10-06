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
        df['Node_ID'] = node_id
        df['IP_Addr'] = ip_addr
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
def upload_hsn(request):
    all_files_df = pd.DataFrame()
    final_output_df = pd.DataFrame()  # This will accumulate all template data

    files = request.FILES.getlist("files")
    if not files:
        return Response(
                {"status": "ERROR", "message": "No files uploaded"},
                status=HTTP_400_BAD_REQUEST,
        )
    
    base_media_url = os.path.join(MEDIA_ROOT, "Hardware_Serial_No")
    output_path = os.path.join(base_media_url, "OUTPUT")
    log_folder = os.path.join(base_media_url, "circle_LOGS")
    log_excel_folder = os.path.join(base_media_url, "logs_excel")
    os.makedirs(log_folder, exist_ok=True)

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

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create logs_excel directory if it doesn't exist
    if not os.path.exists(log_excel_folder):
        os.makedirs(log_excel_folder, exist_ok=True)
    else:
        try:
                shutil.rmtree(log_excel_folder, onexc=on_rm_error)
                os.makedirs(log_excel_folder, exist_ok=True)
        except PermissionError as e:
                print("Permission denied:- ", str(e))

    template_file_path = os.path.join(base_media_url, "template_file")
    if not os.path.exists(template_file_path):
        os.makedirs(template_file_path, exist_ok=True)

    # Process each file and accumulate data
    for uploaded_file in saved_files:
        node_name = os.path.splitext(os.path.basename(uploaded_file))[0]
        excel_filename = os.path.join(log_excel_folder, f"{node_name}_{timestamp}.xlsx")

        with open(uploaded_file, "r") as file:
                file_content = file.readlines()
            
        hget_field_df = explode_data_from_log(
                r'[A-Z0-9_-]+>\shget\s+field\s+prod',                                            
                r'(MO)\s+(productName)\s+(productNumber)\s+(productRevision)\s+(productionDate)\s+(serialNumber)',
                r'(FieldReplaceableUnit=\S+)\s+(\S+\s+\S+\s+\S+)\s+([A-Z]{3}\s?\d+(?:\s\d+)?\/\d+)\s+(\S+)\s+(\S+)\s+(\S+)',
                r'^Total:\s\d+',
                file_content
                )

            
        print(hget_field_df)
        with pd.ExcelWriter(excel_filename, engine="xlsxwriter") as writer:
                hget_field_df.to_excel(writer, sheet_name="sheet1", index=False)
                format_excel_sheet(writer, "sheet1", hget_field_df)
        
        # Process the data and add to final output
        if not hget_field_df.empty:
            df = hget_field_df.copy()
            df.columns = df.columns.astype(str).str.strip()

            # Just keep needed columns, no join
            expanded_df = df[["Node_ID", "MO", "productNumber", "serialNumber"]]
            expanded_df.rename(columns={"Node_ID": "Site_ID"}, inplace=True)

            final_output_df = pd.concat([final_output_df, expanded_df], ignore_index=True)



    # Create single output file
    os.makedirs(output_path, exist_ok=True)
    output_filename = f"HW_Serial_NO_OUTPUT_{timestamp}.xlsx"
    output_filepath = os.path.join(output_path, output_filename)
    
    with pd.ExcelWriter(output_filepath, engine="xlsxwriter") as writer:
        final_output_df.to_excel(writer, index=False, sheet_name="HSN")
        format_excel_sheet(writer, "HSN", final_output_df)

    # Create download link for the single output file
    download_link = request.build_absolute_uri(
        os.path.join(MEDIA_URL, "Hardware_Serial_No", "OUTPUT", output_filename)
    )
    
    return Response(
        {
                "status": True,
                "message": "Files processed successfully",
                "download_url": download_link,
        },
        status=HTTP_200_OK,
    )