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
 
 
@api_view(["POST"])
def relocation_configration(request):
    all_files_df = pd.DataFrame()
    final_output_df = pd.DataFrame()
 
    files = request.FILES.getlist("files")
    if not files:
        return Response(
                {"status": "ERROR", "message": "No files uploaded"},
                status=HTTP_400_BAD_REQUEST,
            )
    base_media_url = os.path.join(MEDIA_ROOT, "Relocation_Configration")
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
 
###################################################################################
 
    # Process each file and accumulate data--
    for uploaded_file in saved_files:
        node_name = os.path.splitext(os.path.basename(uploaded_file))[0]
        excel_filename = os.path.join(log_excel_folder, f"{node_name}_{timestamp}.xlsx")
 
        with open(uploaded_file, "r") as file:
            file_content = file.readlines()


        st_cell_df = explode_data_from_log(
            r'[A-Z0-9_-]+>\sst\scell',
            r'(Proxy)\s+(Adm\sState)\s+(Op\.\sState)\s+(MO)',
            r'\s*(\d+)\s+(\d+\s+\((?:UNLOCKED|LOCKED)\))\s+(\d+\s+\((?:ENABLED|DISABLED)\))\s+(.*)$',
            r'^Total:\s\d+',
            file_content
        )
 
        alt_df = explode_data_from_log(
        r'[A-Z0-9_-]+>\salt',
        r'(Date\s&\sTime\s+\(UTC\))\s+(S)\s+(Specific\sProblem)\s+(MO\s\(AdditionalText\/PC,\s*AI\))',
        r'^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+([MmCc])\s+(.+?)\s+((?:[A-Za-z0-9=,]+\s*\(.+\))|(?:FieldReplaceableUnit=[^()]+(?:,[^()]+)*\s*\(.+))$',
        r'^Total:\s\d+',
        file_content
        )

        st_trx_df = explode_data_from_log(
            r'[A-Z0-9_-]+>\sst\strx',
            r'(Proxy)\s+(Adm\sState)\s+(Op\.\sState)\s+(MO)',
            r'^\s*(\d+)\s+(\d+\s+\((?:UNLOCKED|LOCKED)\))\s*(\d+\s+\((?:ENABLED|DISABLED)\))?\s+(.*)$',
            r'^Total:\s\d+',
            file_content
        )

        linkrate_df = explode_data_from_log(
            r'[A-Z0-9_-]+>\sget\s.\slinkrate',
            r'(MO)\s+(Attribute)\s+(Value)',
            r'(\S+)\s+(\S+)\s+(\d+)$',
            r'^Total:\s\d+',
            file_content
        )
        hget_field_prod_df = explode_data_from_log(
            r'[A-Z0-9_-]+>\shget\sfi\sprod',
            r'MO\s+productName\s+productNumber\s+productRevision\s+productionDate\s+serialNumber',
            r'(FieldReplaceableUnit=[\w\-]+)\s+([\w\s]+?)\s+(K[A-Z]{1,2}\s*\d+\s*\d*\/\d+|KDU\d+\/\d+)\s+(\S+[A-Z])\s+(\d{8})\s+(\S+)$',
            r'^Total:\s\d+',
            file_content
        )

        # print("df:- ",hget_field_prod_df)
        # print("alt df:- ",alt_df)
        # print("st trx df:- ",st_trx_df)
        sheets = {
                'St Cell': st_cell_df,
                'alt'   : alt_df,
                'st trx':st_trx_df,
                'linkrate':linkrate_df,
                'hget field prod':hget_field_prod_df,
        }
 
        df_list = sheets.values()
        # print("df_list:- ",[df_list])
        all_files_df = pd.concat([all_files_df,*df_list], axis=0,ignore_index=True)
        # print("all_files_df:- ",all_files_df)
        with pd.ExcelWriter(excel_filename, engine="xlsxwriter") as writer:
            for sheet_name, df in sheets.items():
                if not df.empty:
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    format_excel_sheet(writer, sheet_name, df)
                else:
                    print(f"[INFO] Skipping sheet '{sheet_name}' as it's empty.")
        #template file path------    
        template_file_path = os.path.join(base_media_url, "template_file")
 
        if not os.path.exists(template_file_path):
            os.makedirs(template_file_path, exist_ok=True)
 
    # Process each Excel file in logs_excel--
        excel_files_paths = [
            os.path.join(log_excel_folder, file)
            for file in os.listdir(log_excel_folder)
        ]
        print(excel_files_paths)
 
    for file in excel_files_paths:
        base_name = os.path.basename(file).split('_')[0]
        print("Base Name:", base_name)
        xls = pd.ExcelFile(file)
        template_path = os.path.join(template_file_path, "template.xlsx")
        template_df : pd.DataFrame = pd.ExcelFile(template_path,).parse()
        template_df.loc[0, "S.No"] = final_output_df["S.No"].max() + 1 if not final_output_df.empty else 1
        # print(xls.sheet_names)
 
        for sheet_name in xls.sheet_names:
            if sheet_name == "St Cell" and not xls.parse(sheet_name).empty:
                df = xls.parse(sheet_name)
 
                if "MO" in df.columns:
                   #find layer series-----
                    layer_series = df["MO"].str.extract(r"EUtranCell(?:FDD|TDD)=\w+_(F\d|T\d)")[0]
                    #site_id-----
                    site = df["MO"].str.extract(r"EUtranCell(?:FDD|TDD)=.*_(\w+)[A-Z]_")[0]
                    site_id = site.dropna().unique()[0] if not site.dropna().empty else "NA"
                    print("Site ID:", site_id)
                    template_df.loc[0, "Site ID"] = site_id
 
                   
                    desired_layers = ['F1', 'F3', 'F8', 'T1', 'T2']
                    layer_series = layer_series[layer_series.isin(desired_layers)]
 
                    layer_counts = layer_series.value_counts()
                    sector_count_str = '+'.join(map(str, layer_counts.values))
 
                    print("Sector Count String:", sector_count_str)
 
                    template_df.loc[0, "Sector Count"] = sector_count_str if sector_count_str else "NA"
                   
                    template_df.loc[0, "Old ID"] = (
                                        df["Node_ID"].unique()[0]
                                        if len(df["Node_ID"].unique()) > 0 and pd.notna(df["Node_ID"].unique()[0])
                                        else "NA"
)

                    layer = df["MO"].str.extract(r"EUtranCell(?:FDD|TDD)=\w+_(F\d|T\d)")[0]
                    layer_value = '_'.join(layer.dropna().unique()) if not layer.dropna().empty else "NA"
                    print("Layer Value:", layer_value)

                    template_df.loc[0, "Layer Available"] = layer_value if layer_value else "NA"
                    template_df.loc[0, "OEM Available"] = "Yes"
            
            if sheet_name == "alt" and not xls.parse(sheet_name).empty:
                df = xls.parse(sheet_name)
                if "Specific Problem" in df.columns:
                    alarm = df["Specific Problem"].unique()
                    print("Alarm:", alarm)
                    filtered_alarm = [a for a in alarm if a != "Security Log Export Service Unavailable" and pd.notna(a)]
                    template_df.loc[0, "Alarm Present"] = ', '.join(filtered_alarm) if len(filtered_alarm) > 0 else "NA"

            if sheet_name == "linkrate" and not xls.parse(sheet_name).empty:
                df = xls.parse(sheet_name)
                linkrate = df['Value'].astype(str).unique()
                template_df.loc[0, 'Link Rate'] = ', '.join(linkrate) if len(linkrate) > 0 else 'NA'
            
            if sheet_name == "hget field prod" and not xls.parse(sheet_name).empty:
                df = xls.parse(sheet_name)
                base = df['productName'].str.extract(r'(?:Baseband|RAN Processor)\s+(\w+)', expand=False).dropna()
                baseband = base.iloc[0] if not base.empty else "NA"
                template_df.loc[0, 'Baseband'] = baseband
                if 'MO' in df.columns:
                    extracted_rrus = df['MO'].astype(str).str.extract(r'FieldReplaceableUnit=(\w+-\d+)', expand=False)
                    if extracted_rrus is not None and not extracted_rrus.empty:
                        rru_models = extracted_rrus.dropna().astype(str).tolist()
                        template_df.loc[0, 'RRU'] = ', '.join(rru_models)
                    else:
                        template_df.loc[0, 'RRU'] = "NA"
                else:
                    template_df.loc[0, 'RRU'] = "NA"

                final_output_df = pd.concat([final_output_df, template_df], ignore_index=True)
 
        #output file path--------------
        os.makedirs(output_path, exist_ok=True)
        output_filename = f"RCC_OUTPUT_{timestamp}.xlsx"
        output_filepath = os.path.join(output_path, output_filename)
       
        with pd.ExcelWriter(output_filepath, engine="xlsxwriter") as writer:
            final_output_df.to_excel(writer, index=False, sheet_name="RCC Results")
            format_excel_sheet(writer, "RCC Results", final_output_df)
 
       
       
        download_url = request.build_absolute_uri(
            os.path.join(MEDIA_URL, "RCC", "OUTPUT", output_filename).replace("\\", "/")
        )
       
    return Response(
        {
            "status": True,
            "message": "Files processed successfully",
            "download_url": download_url,
        },
        status=HTTP_200_OK,
    )