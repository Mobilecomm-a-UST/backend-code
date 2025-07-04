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
import datetime
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL



####################################### Check if file content is empty ################################################
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
                  "bg_color": "#0E034D",
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
                              "bg_color": "#E78978",
                              "font_color": "#FFFFFF",
                              "align": "center",
                              "valign": "center",
                              "bold": True,
                              "border": 1,
                              }
                        )
                  elif cell_value == "nan":
                        format_style = workbook.add_format(
                              {
                                    "bg_color": "#C21D1D",
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
def soft_at_5G_Summary_Ericsson(request):
      # try:
###########################################
      all_files_df = pd.DataFrame()

      circle = request.POST.get("circle")
      files = request.FILES.getlist("files")
      base_name = None
      if not files:
            return Response(
                  {"status": "ERROR", "message": "No files uploaded"},
                  status=HTTP_400_BAD_REQUEST,
            )
############## DEFINEING THE PATH FOR TOOL MEDIA ######################
      base_media_url = os.path.join(MEDIA_ROOT, "soft_at_5G_Summary_Ericsson")
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

##################################################### Save to Excel ################################################
      log_excel_folder = os.path.join(base_media_url, "logs_excel")
      timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

      # Create logs_excel directory if it doesn't exist
      if not os.path.exists(log_excel_folder):
            os.makedirs(log_excel_folder, exist_ok=True)
      else:
            try:
                  shutil.rmtree(log_excel_folder, onexc=on_rm_error)
                  os.makedirs(log_excel_folder, exist_ok=True)
            except PermissionError as e:
                  print("Permission denied:- ", str(e))
########################################################################
      for uploaded_file in saved_files:
            node_name = os.path.splitext(os.path.basename(uploaded_file))[0]
            excel_filename = os.path.join(log_excel_folder, f"{node_name}_{timestamp}.xlsx")
            with open(uploaded_file, "r") as file:
                  file_content = file.readlines()
            St_cell_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sSt\scell',
                  r'(Proxy)\s+(Adm\sState)\s+(Op\.\sState)\s+(MO)',
                  r'\s*(\d+)\s+(\d+\s+\((?:UNLOCKED|LOCKED)\))\s+(\d+\s+\((?:ENABLED|DISABLED)\))\s+(.*)$',
                  r'^Total:\s\d+',
                  file_content
            )

            Latitude_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\s\.\sLatitude',
                  r'MO\s+Attribute\s+Value',
                  r'^\s*(NRSectorCarrier=\S+)\s+(latitude)\s+(\d+)\s*$',
                  r'^Total:\s\d+',
                  file_content
            )

            Longitude_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\s\.\sLongitude',
                  r'MO\s+Attribute\s+Value',
                  r'^\s*(NRSectorCarrier=\S+)\s+(longitude)\s+(\d+)\s*$',
                  r'^Total:\s\d+',
                  file_content
            )

            get0_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\s0',
                  r'^(\d+)\s+([A-Za-z0-9=_\-]+)$',
                  r'^\s*([a-zA-Z0-9]+)\s+(.+?)\s*$',
                  r'^Total:\s\d+',
                  file_content
            )

            Nrtac_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\s\.\sNrtac', 
                  r'MO\s+Attribute\s+Value',     
                  r'^\s*(NRCellDU=\w+|NRCellCU=\w+)\s+(\w+)\s+(\S+)?\s*$',  
                  r'^Total:\s\d+',                       
                  file_content                      
            )

            Gnbid_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\s\.\sGnbid',
                  r'MO\s+Attribute\s+Value',
                  r'^\s*(GNBCUUPFunction=\w+|GNBDUFunction=\w+)\s+(\w+)\s+(\S+)?\s*$',  
                  r'^Total:\s\d+',
                  file_content
            )

            Linkrate_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\s\.\sLinkrate',
                  r'MO\s+Attribute\s+Value',
                  r'^\s*(RiLink=S\d+_N1-1)\s+(\w+)\s+(\S+)?\s*$',  
                  r'^Total:\s\d+',
                  file_content
            )

            Digitaltilt_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\s\.\sDigitaltilt',
                  r'MO\s+Attribute\s+Value',
                  r'^\s*(NRSectorCarrier=[\S]+)\s+(\w+)\s+(\S+)?\s*$', 
                  r'^Total:\s\d+',
                  file_content
            )

            termpointtoenode_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sst\stermpointtoenode',
                  r'(Proxy)\s+(Adm\sState)\s+(Op\.\sState)\s+(MO)',
                  r'\s*(\d+)\s+(\d+\s+\((?:UNLOCKED|LOCKED)\))\s+(\d+\s+\((?:ENABLED|DISABLED)\))\s+(.*)$',
                  r'^Total:\s\d+',
                  file_content
            )
            
            invxr_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\s+invxr',
                  r'(ID)\s+(LINK)\s+(RiL)\s+(WL1)\s+(TEMP1)\s+(TXbs1)\s+(TXdBm1)\s+(RXdBm1)\s+(BER1)\s+(WL2)\s+(TEMP2)\s+(TXbs2)\s+(TXdBm2)\s+(RXdBm2)\s+(BER2)\s+(DlLoss)\s+(UlLoss)\s+(LENGTH)\s+(TT)',
                  r'^\s*(\d+)\s+(\w+)\s+(S\d+_N1-1)?\s+(\d+\.\d+)\s+(\d+C)\s+(\d+%)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)?\s*(\d+\.\d+)?\s+(\d+\.\d+)\s+(\d+C)\s+(\d+%)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)?\s+(-?\d+\.\d+)?\s+(-?\d+\.\d+)?\s+(-?\d+\.\d+)?\s+(\d+m)\s+(\d+)\s*$',
                  r'^-+$',
                  file_content 
            )



            invl_basic_df= explode_data_from_log(
                  r'[A-Z0-9_-]+>\sst\ssync',
                  r'(Proxy)\s+(Adm\sState)\s+(Op\.\sState)\s+(MO)',
                  r'^\s*(\d+)\s+(\d*)\s*\((ENABLED|DISABLED)\)\s+(.*)$',
                  r'^Total:\s\d+',
                  file_content
            )

            Enroll_df  = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\s\.\sEnroll',
                  r'MO\s+Attribute\s+Value',
                  r'^(SecM=.*?)\s+(\S+)\s+(.+)$',
                  r'^Total:\s\d+',
                  file_content
            )

            hget_field_prod_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\shget\sfield\sprod',
                  r'MO\s+productName\s+productNumber\s+productRevision\s+productionDate\s+serialNumber',
                  r'^\s*(FieldReplaceableUnit=\w+-S\d+_N\d+)\s+(\w+\s+\d+\s+\w+)\s+(\w+\s+\d+\s+\d+\/\d+)\s+(\w+)\s+(\d+)\s+(\S+)\s*$',  
                  r'^Total:\s\d+',
                  file_content
            )


            print("st termpointtoenode_df:- ", termpointtoenode_df)
            sheets = {
                  'St cell': St_cell_df,
                  'get . Latitude': Latitude_df,
                  'get . Longitude': Longitude_df,
                  'get 0': get0_df,
                  'Nrtac': Nrtac_df,
                  'Gnbid': Gnbid_df,
                  'Linkrate': Linkrate_df,
                  'Digitaltilt': Digitaltilt_df,
                  'st termpointtoenode': termpointtoenode_df,
                  'invxr': invxr_df,
                  'invl_basic': invl_basic_df,
                  'get . Enroll': Enroll_df,
                  "hget field prod": hget_field_prod_df,

            }
            df_list = sheets.values()
            # print("df_list:- ",[df_list])
            all_files_df = pd.concat([all_files_df,*df_list], axis=0,ignore_index=True)
            # print("all_files_df:- ",all_files_df)
            with pd.ExcelWriter(excel_filename, engine="xlsxwriter") as writer:
                  for sheet_name, df in sheets.items():
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                        format_excel_sheet(writer, sheet_name, df)

################################## Making the template file path and template file existance #######################################
            template_file_path = os.path.join(base_media_url, "template_file")

            if not os.path.exists(template_file_path):
                  os.makedirs(template_file_path, exist_ok=True)


      #######################################################Output##############################################################
            excel_files_paths = [
            os.path.join(log_excel_folder, file)
            for file in os.listdir(log_excel_folder)
            ]
            print(excel_files_paths)

      for file in excel_files_paths:
            base_name = os.path.basename(file).split('_')[0]
            print("Base Name:", base_name)
            xls = pd.ExcelFile(file)
            template_path = os.path.join(template_file_path, "5G_template.xlsx")
            template_df : pd.DataFrame = pd.ExcelFile(template_path,).parse("Summary")
            enbid_df : pd.DataFrame = pd.ExcelFile(template_path,).parse("Anchor Node ENBID")
            # enbid_df : pd.DataFrame = pd.ExcelFile(template_path,).parse()

            print(xls.sheet_names)
            for  sheet_name in xls.sheet_names:
                  print(sheet_name)
                  if sheet_name == "St cell":
                        df = xls.parse(sheet_name)
                        
                        if "MO" in df.columns:
                              # Circle
                              circle = df["MO"].str.extract(r"NRCellDU=([A-Z]{2})_").dropna()
                              template_df.loc[0, "Circle"] = circle.iloc[0, 0].strip() if not circle.empty else "NA"

                              # circle = df["MO"].str.extract(r"NRCellDU=([A-Z]{2})_")
                              # print("Circle:", circle)
                              layer = df["MO"].str.extract(r"NRCellDU=\w+_(F\d|T\d)")[0]
                              # print("layer:", layer)
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
                                    "T1": "5G",
                                    "T2": "5G",
                              }
                              l_layers = [
                                    layer_mapping.get(l, l) for l in layer_value.split("_")
                              ]
                              l_layers = list(set(l_layers))
                              template_df.loc[0, "Technology"] = "_".join(l_layers)
                              print("Technology:", l_layers)
                              
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
                                          template_df.loc[0, "Site ID (2G)"] = site
                                          # print("2G SiteID:",site)

                              cell_name_series = df["MO"].str.extract(r"NRCellDU=([\w_]+)")[0].dropna()
                              print("Cell names :", cell_name_series)
                              template_df.loc[0, "5G Cell name A"] = "NA"
                              template_df.loc[0, "5G Cell name B"] = "NA"
                              template_df.loc[0, "5G Cell name C"] = "NA"
                              for cn in cell_name_series:
                                    if cn.endswith("A"):
                                          template_df.loc[0, "5G Cell name A"] = cn 
                                          # print("5G Cell name A:", cn)
                                    elif cn.endswith("B"):
                                          template_df.loc[0, "5G Cell name B"] = cn
                                    elif cn.endswith("C"):
                                          template_df.loc[0, "5G Cell name C"] = cn 
                                    
                                    else:
                                          template_df.loc[0, "5G Cell name A"] = "NA"
                                          template_df.loc[0, "5G Cell name B"] = "NA"
                                          template_df.loc[0, "5G Cell name C"] = "NA"
                              
                              BB_config = df["MO"].str.extract(r"(?:NRCellDU|EUtranCell(?:FDD|TDD))=\w+_(F\d|T\d)")[0]
                              # print("BB_config:", BB_config)
                              if BB_config.str.contains(r"F1|F2|F3|T1|T2", na=False).any():
                                    template_df.loc[0, "BB Conf."] = "LTE+NR"
                              elif BB_config.str.contains(r"T1|T2", na=False).any():
                                    template_df.loc[0, "BB Conf."] = "NR"
                              
                              cell_count = df['MO'].str.extract(r'(GNBDUFunction)')
                              # print("Cell Count:", cell_count)
                              template_df.loc[0, 'No. Of Cells'] = cell_count.count()[0] if cell_count.count()[0] else "NA"
                              template_df.loc[0, 'No Of RRU'] = cell_count.count()[0] if cell_count.count()[0] else "NA"

                        else:
                              print(f"'MO' column not found in sheet 'St cell' for file: {file}")
                              template_df.loc[0, "Circle"] = "NA"
                              # Fill other MO-related fields as "NA"
                              template_df.loc[0, [
                                    "Technology", "Site ID (2G)", 
                                    "5G Cell name A", "5G Cell name B", "5G Cell name C",
                                    "BB Conf.", "No. Of Cells", "No Of RRU"
                              ]] = "NA"
                        
                  if sheet_name == "get . Latitude":
                        df = xls.parse(sheet_name)
                        if "Value" in df.columns:
                              latitude = df["Value"].dropna().iloc[0] if not df["Value"].dropna().empty else "NA"
                              # print("Latitude:", latitude)      
                        else:
                              print(f"'Value' column not found in sheet '{sheet_name}' for file: {file}")
                              latitude = "NA"
                        template_df.loc[0, "Site Latitude"] = latitude
                  
                  if sheet_name == "get . Longitude":
                        df = xls.parse(sheet_name)
                        if "Value" in df.columns:
                              longitude = df["Value"].dropna().iloc[0] if not df["Value"].dropna().empty else "NA"
                        else:
                              print(f"'Value' column not found in sheet '{sheet_name}' for file: {file}")
                              longitude = "NA"
                        # print("Longitude:", longitude)
                        template_df.loc[0, "Site Longitude"] = longitude
                        
                  if sheet_name == "Nrtac":
                        df = xls.parse(sheet_name)
                        if "Value" in df.columns:
                              tac = df["Value"].dropna().iloc[0] if not df["Value"].dropna().empty else "NA"      
                        else:
                              print(f"'Value' column not found in sheet '{sheet_name}' for file: {file}")
                              tac = "NA"
                        # print("TAC:", tac)
                        template_df.loc[0, "TAC"] = tac

                  
                  if sheet_name == "Gnbid":
                        df = xls.parse(sheet_name)
                        if "Value" in df.columns:
                              gnb_id = df["Value"].dropna().iloc[0] if not df["Value"].dropna().empty else "NA"
                        else:
                              print(f"'Value' column not found in sheet '{sheet_name}' for file: {file}")
                              gnb_id = "NA"
                        # print("GNB ID:", gnb_id)
                        template_df.loc[0, "GNBID"] = gnb_id

                  
                  if sheet_name == "st termpointtoenode":
                        df = xls.parse(sheet_name)
                        df.columns = df.columns.astype(str).str.strip()  # Clean column names

                        required_cols = {"Adm State", "Op. State", "MO"}
                        if required_cols.issubset(df.columns):
                              filtered_df = df[
                                    df["Adm State"].str.contains("UNLOCKED", na=False) &
                                    df["Op. State"].str.contains("ENABLED", na=False)
                              ].copy()

                              if not filtered_df.empty:
                                    filtered_df["enodeid"] = filtered_df["MO"].str.extract(
                                    r'ExternalENodeBFunction=auto404_\d+_\d+_(\d+)')
                                    filtered_df.dropna(subset=["enodeid"], inplace=True)

                                    # Take 15 random enodeids
                                    result_df = filtered_df.sample(
                                    n=min(15, len(filtered_df)), random_state=1)["enodeid"].tolist()

                                    print("Random ENBIDs:", result_df)

                                    for idx, enbid in enumerate(result_df):
                                          enbid_df.loc[idx, "Anchor node (EnbId)"] = enbid
                              else:
                                    print(f"No matching unlocked/enabled ENBs in {file}")
                        else:
                              print(f"Missing required columns in 'st termpointtoenode' for file: {file}")



                  if sheet_name == "invxr":
                        df = xls.parse(sheet_name)
                        df.columns = df.columns.astype(str).str.strip()  # Clean column names

                        if "LENGTH" in df.columns:
                              cprilength = df["LENGTH"].dropna().astype(str).str.replace("m", "", regex=False)
                              template_df.loc[0, "CPRI length as per Actual"] = "/".join(cprilength)

                              def round_to_nearest_5(n):
                                    rem = n % 5
                                    return n + (5 - rem) if rem >= 3 else n - rem

                              cpri_length_as_per_mo = "/".join(
                                    str(round_to_nearest_5(int(val))) for val in cprilength if val.isdigit()
                              )

                              template_df.loc[0, "CPRI length as per MO"] = cpri_length_as_per_mo
                              template_df.loc[0, "CPRI length as per Survey"] = cpri_length_as_per_mo
                        else:
                              print(f"'LENGTH' column not found in 'invxr' sheet for file: {file}")
                              template_df.loc[0, "CPRI length as per Actual"] = "NA"
                              template_df.loc[0, "CPRI length as per MO"] = "NA"
                              template_df.loc[0, "CPRI length as per Survey"] = "NA"

                  if sheet_name == "get . Enroll":
                        df = xls.parse(sheet_name)
                        df.columns = df.columns.astype(str).str.strip()  # Clean column names

                        if "Value" in df.columns:
                              value_series = df["Value"].dropna().astype(str)
                              OSS_match = value_series.str.extract(r"OU=([\w\d]+)")

                              if not OSS_match.empty and OSS_match.notna().any().values[0]:
                                    OSS = OSS_match.dropna().iloc[0, 0].strip().upper()
                                    OSS = OSS.replace("ENM", " ENM") if "ENM" in OSS else OSS
                                    OSS = OSS.replace("DEL", "DL") if "DEL" in OSS else OSS
                                    template_df["OSS Name"] = template_df["OSS Name"].astype(object)
                                    template_df.loc[0, "OSS Name"] = OSS
                              else:
                                    template_df["OSS Name"] = template_df["OSS Name"].astype(object)
                                    template_df.loc[0, "OSS Name"] = "NA"
                        else:
                              print(f"'Value' column not found in sheet 'get . Enroll' for file: {file}")
                              template_df["OSS Name"] = template_df["OSS Name"].astype(object)
                              template_df.loc[0, "OSS Name"] = "NA"
                  
                  if "get 0" in xls.sheet_names:
                        df_0 = xls.parse("get 0", header=None)

                        if not df_0.empty:
                              # Extract MO Name
                              MO_name_0 = "/".join(
                                    cell.split("=")[-1]
                                    for cell in df_0.iloc[0]
                                    if isinstance(cell, str) and "ManagedElement=" in cell
                              )
                              template_df.loc[0, "MO Name"] = MO_name_0
                              template_df.loc[0, "SiteID(5G/)/MRBTSID"] = MO_name_0
                              enbid_df.loc[0, "5G Site ID"] = MO_name_0

                              # Find SW Version
                              sw_version_rows = df_0[df_0.iloc[:, 0] == "swVersion"]
                              if not sw_version_rows.empty:
                                    sw_version = "L" + str(sw_version_rows.iloc[0, 1])
                                    template_df.loc[0, "SW Version"] = sw_version
                              else:
                                    template_df.loc[0, "SW Version"] = "NA"
                        else:
                              print(f"'get 0' sheet is empty in file: {file}")
                              template_df.loc[0, "MO Name"] = "NA"
                              template_df.loc[0, "SiteID(5G/)/MRBTSID"] = "NA"
                              enbid_df.loc[0, "5G Site ID"] = "NA"
                              template_df.loc[0, "SW Version"] = "NA"
                  else:
                        template_df.loc[0, "MO Name"] = "NA"
                        template_df.loc[0, "SiteID(5G/)/MRBTSID"] = "NA"
                        template_df.loc[0, "SW Version"] = "NA"

                  
            if sheet_name == "hget field prod":
                  df = xls.parse(sheet_name)
                  df.columns = df.columns.astype(str).str.strip()  # Clean column names

                  if "productName" in df.columns and not df.empty:
                        first_product = df["productName"].dropna().iloc[0] if not df["productName"].dropna().empty else "NA"
                        count = (df["productName"] == first_product).sum()
                        product_display = f"{first_product}*{count}"
                        print("Result:", product_display)
                        template_df.loc[0, "Other Hardware Related Additional Information"] = product_display
                  else:
                        print(f"'productName' column missing or sheet is empty in file: {file}")
                        template_df.loc[0, "Other Hardware Related Additional Information"] = "NA"


                  today = datetime.date.today()
                  template_df.loc[0, "Offer Date"] = today.strftime("%d-%m-%Y")
                  df.columns = df.columns.astype(str).str.strip()  # Clean column names
                  if "IP_Addr" in df.columns:
                        ip_values = df["IP_Addr"].dropna()
                        template_df.loc[0, "5G Node IP"] = ip_values.iloc[0] if not ip_values.empty else "NA"
                  else:
                        print(f"'IP_Addr' column not found in sheet for file: {file}")
                        template_df.loc[0, "5G Node IP"] = "NA"
                  template_df.loc[0, "AT Type"] = "Soft"
                  template_df.loc[0, "Project Remarks"] = "On-Air"
                  template_df.loc[0, "MME IP"] = "Given in Separate Sheet"
                  template_df.loc[0, "SGW IP"] = "Given in Separate Sheet"
                  template_df.loc[0, "TDD Frame Structure"] = "DDDSUUDDDD"
                  template_df.loc[0, "Nomenclature hygiene"] = "Yes" 
                  template_df.loc[0, "GPL Compliance"] = "Yes" 
                  template_df.loc[0, "LMS Compliance"] = "Yes" 
                  template_df.loc[0, "IFLB Compliance"] = "Yes" 
                  template_df.loc[0, "QoS Compliance"] = "Yes" 
                  template_df.loc[0, "CA compliance"] = "NA" 
                  template_df.loc[0, "Ducting compliance"] = "NA" 
                  template_df.loc[0, "Energy saving fetaures compliance"] = "NA" 
                  template_df.loc[0, "All approved features implemented compliance"] = "Yes" 
                  template_df.loc[0, "Beamset config compliance"] = "NA" 
                  template_df.loc[0, "PCI definition compliance"] = "Yes" 
                  template_df.loc[0, "RSI definition compliance"] = "Yes" 
                  template_df.loc[0, "PRACH definition compliance"] = "Yes" 
                  template_df.loc[0, "Electrical tilt compliance"] = "Yes" 
                  template_df.loc[0, "ENDC compliance"] = "Yes" 
                  template_df.loc[0, "Tx Power compliance"] = "Yes" 
                  template_df.loc[0, "5G cell name nomenclature compliance"] = "Yes" 
                  template_df.loc[0, "BTS Clock Configuration-Primary  (GPS/IP/Top/TDM/NTP)"] = "GPS" 
                  template_df.loc[0, "BTS Clock Configuration-Secondary (GPS/IP/Top/TDM/NTP)"] = "NA" 
                  template_df.loc[0, "Validation of eNB changes for 5G-NSA: Applicable on Anchor layer FDD&TDD bands in eNB"] = "Yes" 
                  template_df.loc[0, "Validation of buffer settings & QoS in CSR / E-band microwave or regular microwave as applicable"] = "NA"
                  template_df.loc[0, "Site should be defined in planned OSS/BSC and ensure to login through MO name ( no duplicate MO in other OSS )"] = "Yes"
                  template_df.loc[0, "QIA Alarms : No active alarm ( except external alarm)/No false alarm in  iOMS or OSS Monitor"] = "No"
                  template_df.loc[0, "X2 Link availability upto first tier neighbour"] = "Yes"
                  template_df.loc[0, "External alarm should be defined on site"] = "NA"
                  template_df.loc[0, "Site should be on Latest Software release"] = "Yes"
                  template_df.loc[0, "Current VSWR value compliance"] = "NA"
                  template_df.loc[0, "5G should be properly configured and  should be enabled and unlocked in core nodes"] = "Yes"
                  template_df.loc[0, "Sync definition (GPS /Clock)  Site should not be on TOPF on priority 1"] = "NA"
                  template_df.loc[0, "TWAMP Parameter Check"] = "Yes"
                  template_df.loc[0, "External alarm check"] = "Yes"
                  template_df.loc[0, "SCTP retransmissions to be checked"] = "Yes"
                  template_df.loc[0, "Ping test towards MME"] = "Yes"
                  template_df.loc[0, "Ping test towards SGW"] = "Yes"
                  template_df.loc[0, "SBR should be properly implemented (All IP Route should be defined with 0.0.0.0)"] = "Yes"
                  template_df.loc[0, "Object should be in Monitor along with Correct Name, Alarm upload & MO & HW upload should be successful"] = "Yes"
                  template_df.loc[0, "All sector and corresponding cells should be enabled and unlocked"] = "Yes"
                  template_df.loc[0, "All RRU’s/RF/AIR Module should be enabled and unlocked"] = "Yes"
                  template_df.loc[0, "Site Class Update in NETACT/ENM/OSS/NIM Update"] = "Yes"
                  template_df.loc[0, "Lat-Long Configuration in OSS"] = "Yes"
                  template_df.loc[0, "Speed and Duplex"] = "Yes"
                  template_df.loc[0, "GPS Out Loss of Time"] = "No"
                  template_df.loc[0, "Vswr Over Threshold"] = "No"
                  template_df.loc[0, "NTP server reachability fault"] = "No"
                  template_df.loc[0, "Clock calibration expiry soon"] = "No"
                  template_df.loc[0, "Resource activation timeout"] = "No"
                  template_df.loc[0, "SFP stability problem"] = "No"     
                  template_df.loc[0, "Temperature Exceptional Taken Out of Service"] = "No"
                  template_df.loc[0, "RF Reflected Power High"] = "No"
                  template_df.loc[0, "Loss of Tracking"] = "No"
                  template_df.loc[0, "TimeSyncIO Reference Failed"] = "No"
                  template_df.loc[0, "Sync Reference Deviation"] = "No"
                  template_df.loc[0, "License Key File Fault"] = "No"
                  template_df.loc[0, "License Key Missing"] = "No"
                  template_df.loc[0, "License Key Not Available"] = "No"
                  template_df.loc[0, "Network Synch Time from GPS Missing"] = "No"
                  template_df.loc[0, "Resource Allocation Failure Service Degraded"] = "No"
                  template_df.loc[0, "Slave TU Out of Synchronization"] = "No"
                  template_df.loc[0, "Linearization Disturbance Performance Degraded"] = "No"
                  template_df.loc[0, "RX path imbalance"] = "No"
                  template_df.loc[0, "RX diversity lost"] = "No"
                  template_df.loc[0, "HW Partial Fault"] = "No"
                  template_df.loc[0, "HW Fault"] = "No"
      


                  ####################################### getting folders for final output #########################################
            output_path = os.path.join(base_media_url, "OUTPUT")

            os.makedirs(output_path, exist_ok=True)

            output_filename = f"_{base_name}_OUTPUT_{timestamp}.xlsx"
            output_path = os.path.join(output_path, output_filename)

            with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
                  
                  template_df.to_excel(writer, sheet_name="Detail", index=False)
                  format_excel_sheet(writer, "Detail", template_df)
                  enbid_df.to_excel(writer, sheet_name="Anchor Node ENBID", index=False)
                  format_excel_sheet(writer, "Anchor Node ENBID", enbid_df)



            ############################################# MAkING THE ZIP FILE #########################################################
      import glob

      # Remove old zip files
      for old_zip in glob.glob(os.path.join(base_media_url, "5gSUMMARY_OUTPUT_*.zip")):
            try:
                  os.remove(old_zip)
                  print(f"Deleted old zip: {old_zip}")
            except Exception as e:
                  print(f"Failed to delete {old_zip}: {e}")



      timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
      zip_filename = os.path.join(base_media_url, f"5gSUMMARY_OUTPUT_{timestamp}.zip")
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

@api_view(["POST", "GET"])
def soft_at_5G_checkpoint(request):
      # try:
###########################################
      all_files_df = pd.DataFrame()

      circle = request.POST.get("circle")
      files = request.FILES.getlist("files")
      base_name = None
      if not files:
            return Response(
                  {"status": "ERROR", "message": "No files uploaded"},
                  status=HTTP_400_BAD_REQUEST,
            )
############## DEFINEING THE PATH FOR TOOL MEDIA ######################
      base_media_url = os.path.join(MEDIA_ROOT, "soft_at_5G_Checklist_Ericsson")
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

##################################################### Save to Excel ################################################
      log_excel_folder = os.path.join(base_media_url, "logs_excel")
      timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

      # Create logs_excel directory if it doesn't exist
      if not os.path.exists(log_excel_folder):
            os.makedirs(log_excel_folder, exist_ok=True)
      else:
            try:
                  shutil.rmtree(log_excel_folder, onexc=on_rm_error)
                  os.makedirs(log_excel_folder, exist_ok=True)
            except PermissionError as e:
                  print("Permission denied:- ", str(e))
########################################################################
      for uploaded_file in saved_files:
            node_name = os.path.splitext(os.path.basename(uploaded_file))[0]
            excel_filename = os.path.join(log_excel_folder, f"{node_name}_{timestamp}.xlsx")
            with open(uploaded_file, "r") as file:
                  file_content = file.readlines()

            Latitude_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\s\.\sLatitude',
                  r'MO\s+Attribute\s+Value',
                  r'^\s*(NRSectorCarrier=\S+)\s+(latitude)\s+(\d+)\s*$',
                  r'^Total:\s\d+',
                  file_content
            )

            Longitude_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\s\.\sLongitude',
                  r'MO\s+Attribute\s+Value',
                  r'^\s*(NRSectorCarrier=\S+)\s+(longitude)\s+(\d+)\s*$',
                  r'^Total:\s\d+',
                  file_content
            )


            Linkrate_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\s\.\sLinkrate',
                  r'MO\s+Attribute\s+Value',
                  r'^\s*(RiLink=S\d+_N1-1)\s+(\w+)\s+(\S+)?\s*$',  
                  r'^Total:\s\d+',
                  file_content
            )

            Digitaltilt_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\s\.\sDigitaltilt',
                  r'MO\s+Attribute\s+Value',
                  r'^\s*(NRSectorCarrier=[\S]+)\s+(\w+)\s+(\S+)?\s*$', 
                  r'^Total:\s\d+',
                  file_content
            )

            invl_basic_df= explode_data_from_log(
                  r'[A-Z0-9_-]+>\sinvl\sbasic',
                  r'(FeatureName)\s+(FeatureKey)\s+(FAJ)\s+(LicenseState)\s+(FeatureState)\s+(ServiceState)\s+(ValidFrom)\s+(ValidUntil)\s+(Description)',
                  r'^\s*(?:(?P<feature>[^\s].*?)\s+)?(?P<cxc>CXC\d{7})\s+(?P<faj>FAJ\d{7})\s+(?P<enabled>\d\s+\([^)]+\))\s+(?P<activated>\d\s+\([^)]+\))\s+(?P<operable>\d\s+\([^)]+\))\s+(?P<valid_from>\d{4}-\d{2}-\d{2})?\s*(?P<valid_until>\d{4}-\d{2}-\d{2})?\s+(?P<description>.+)$',
                  r'^Total:\s\d+',
                  file_content
            )
            print("invl_basic_df:- ", invl_basic_df)

            sheets = {
                  'get . Latitude': Latitude_df,
                  'get . Longitude': Longitude_df,
                  'get . Linkrate': Linkrate_df,
                  'get . Digitaltilt': Digitaltilt_df,
                  'invl basic': invl_basic_df,

            }
            df_list = sheets.values()
            # print("df_list:- ",[df_list])
            all_files_df = pd.concat([all_files_df,*df_list], axis=0,ignore_index=True)
            # print("all_files_df:- ",all_files_df)
            with pd.ExcelWriter(excel_filename, engine="xlsxwriter") as writer:
                  for sheet_name, df in sheets.items():
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                        format_excel_sheet(writer, sheet_name, df)

################################## Making the template file path and template file existance #######################################
            template_file_path = os.path.join(base_media_url, "template_file")

            if not os.path.exists(template_file_path):
                  os.makedirs(template_file_path, exist_ok=True)


      #######################################################Output##############################################################
            excel_files_paths = [
            os.path.join(log_excel_folder, file)
            for file in os.listdir(log_excel_folder)
            ]
            print(excel_files_paths)

      for file in excel_files_paths:
            base_name = os.path.basename(file).split('_')[0]
            print("Base Name:", base_name)
            xls = pd.ExcelFile(file)
            template_path = os.path.join(template_file_path, "5G checklist template.xlsx")
            checklist_df : pd.DataFrame = pd.ExcelFile(template_path,).parse()
            print(xls.sheet_names)
            for idx,sheet_name in enumerate(xls.sheet_names, start=1):
                  print(sheet_name)
                  required_columns_present = lambda df, columns: all(col in df.columns for col in columns)
                  if sheet_name == "get . Latitude":
                        df = xls.parse(sheet_name).copy()
                        if required_columns_present(df, ["Attribute", "Value", "Node_ID"]):
                              df["Attribute"] = df["Attribute"].astype(str).str.strip()
                              df["Value"] = df["Value"].astype(str).str.strip()
                              ok_status_list = df.apply(
                                    lambda x: "OK" if x['Attribute'] == "latitude" and x['Value'] != "0" else "NOT OK",
                                    axis=1
                              ).tolist()
                              checklist_df.at[idx,"Site_ID"] = df['Node_ID'].unique()[0]
                              checklist_df.at[idx,'Remark'] = 'OK' if all(status == 'OK' for status in ok_status_list) else 'NOT OK'
                              checklist_df.at[idx,'Checkpoint'] = str(sheet_name)
                        else:
                              # Sheet not found
                              # template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                              checklist_df.at[idx + 1, 'Remark'] = 'Missing'
                              checklist_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)

                  elif sheet_name == "get . Longitude":
                        df = xls.parse(sheet_name).copy()
                        if required_columns_present(df, ["Attribute", "Value", "Node_ID"]):
                              df["Attribute"] = df["Attribute"].astype(str).str.strip()
                              df["Value"] = df["Value"].astype(str).str.strip()
                              ok_status_list = df.apply(
                                    lambda x: "OK" if x['Attribute'] == "longitude" and x['Value'] != "0" else "NOT OK",
                                    axis=1
                              ).tolist()
                              checklist_df.at[idx,"Site_ID"] = df['Node_ID'].unique()[0]
                              checklist_df.at[idx,'Remark'] = 'OK' if all(status == 'OK' for status in ok_status_list) else 'NOT OK'
                              checklist_df.at[idx,'Checkpoint'] = str(sheet_name)
                        else:
                              # Sheet not found
                              # template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                              checklist_df.at[idx + 1, 'Remark'] = 'Missing'
                              checklist_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)
                  
                  elif sheet_name == "get . Linkrate":
                        df = xls.parse(sheet_name).copy()
                        if required_columns_present(df, ["MO", "Attribute", "Value"]):
                              df["MO"] = df["MO"].astype(str).str.strip()
                              df["Attribute"] = df["Attribute"].astype(str).str.strip()
                              df["Value"] = df["Value"].astype(str).str.strip()
                              ok_status_list = df.apply(
                                    lambda x: "OK" if x['Attribute'] == "linkRate" and x['Value'] == "25700" else "NOT OK",
                                    axis=1
                              ).tolist()
                              checklist_df.at[idx,"Site_ID"] = df['Node_ID'].unique()[0]
                              checklist_df.at[idx,'Remark'] = 'OK' if all(status == 'OK' for status in ok_status_list) else 'NOT OK'
                              checklist_df.at[idx,'Checkpoint'] = str(sheet_name)
                        else:
                              checklist_df.at[idx + 1, 'Remark'] = 'Missing'
                              checklist_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)
                  
                  elif sheet_name == "get . Digitaltilt":
                        df = xls.parse(sheet_name).copy()
                        if required_columns_present(df, ["MO", "Attribute", "Value"]):
                              df["MO"] = df["MO"].astype(str).str.strip()
                              df["Attribute"] = df["Attribute"].astype(str).str.strip()
                              df["Value"] = df["Value"].astype(str).str.strip()
                              ok_status_list = df.apply(
                                    lambda x: "OK" if x['Attribute'] == "digitalTilt" and x['Value'] != "0" else "NOT OK",
                                    axis=1
                              ).tolist()
                              checklist_df.at[idx,"Site_ID"] = df['Node_ID'].unique()[0]
                              checklist_df.at[idx,'Remark'] = 'OK' if any(status == 'OK' for status in ok_status_list) else 'NOT OK'
                              checklist_df.at[idx,'Checkpoint'] = str(sheet_name)
                        else:
                              checklist_df.at[idx + 1, 'Remark'] = 'Missing'
                              checklist_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)
                  
                  elif sheet_name == "invl basic":
                        df = xls.parse(sheet_name).copy()
                        if required_columns_present(df, ["FeatureName", "FeatureKey", "FAJ", "LicenseState", "FeatureState", "ServiceState", "ValidFrom", "ValidUntil", "Description"]):
                              df["FeatureName"] = df["FeatureName"].astype(str).str.strip()
                              df["FeatureKey"] = df["FeatureKey"].astype(str).str.strip()
                              df["FAJ"] = df["FAJ"].astype(str).str.strip()
                              df["LicenseState"] = df["LicenseState"].astype(str).str.strip()
                              df["FeatureState"] = df["FeatureState"].astype(str).str.strip()
                              df["ServiceState"] = df["ServiceState"].astype(str).str.strip()
                              df["ValidFrom"] = df["ValidFrom"].astype(str).str.strip()
                              df["ValidUntil"] = df["ValidUntil"].astype(str).str.strip()
                              df["Description"] = df["Description"].astype(str).str.strip()

                              ok_status_list = df.apply(
                                    lambda x: "OK" if x['FeatureName']=="BasicIntelligentConnectivity" and x['LicenseState'] == "1 (ENABLED)" and x['FeatureState'] == "1 (ACTIVATED)" and x['ServiceState'] == "1 (OPERABLE)" else "NOT OK",
                                    axis=1
                              ).tolist()
                              
                              checklist_df.at[idx,"Site_ID"] = df["Node_ID"].unique()[0] 
                              checklist_df.at[idx,'Remark'] = 'OK' if any(status == 'OK' for status in ok_status_list) else 'NOT OK'
                              checklist_df.at[idx,'Checkpoint'] = str(sheet_name)
                        else:
                              checklist_df.at[idx + 1, 'Remark'] = 'Missing'
                              checklist_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)


                  ####################################### getting folders for final output #########################################
            output_path = os.path.join(base_media_url, "OUTPUT")

            os.makedirs(output_path, exist_ok=True)

            output_filename = f"_{base_name}_OUTPUT_{timestamp}.xlsx"
            output_path = os.path.join(output_path, output_filename)

            with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
                  
                  checklist_df.to_excel(writer, sheet_name="checklist", index=False)
                  format_excel_sheet(writer, "checklist", checklist_df)



            ############################################# MAkING THE ZIP FILE #########################################################
      import glob

      # Remove old zip files
      for old_zip in glob.glob(os.path.join(base_media_url, "5gChecklist_OUTPUT_*.zip")):
            try:
                  os.remove(old_zip)
                  print(f"Deleted old zip: {old_zip}")
            except Exception as e:
                  print(f"Failed to delete {old_zip}: {e}")



      timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
      zip_filename = os.path.join(base_media_url, f"5gChecklist_OUTPUT_{timestamp}.zip")
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

