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
      workbook = writer.book
      worksheet = writer.sheets[sheet_name]

      YELLOW = "#FFC000"
      SKY_BLUE = "#94DCF8"

      worksheet.set_row(startrow, 23)

      # ---------- HEADER ----------
      for col_num, col_name in enumerate(df.columns):
            block = (col_num // 4) % 2
            header_bg = YELLOW if block == 0 else SKY_BLUE

            header_format = workbook.add_format({
                  "bold": True,
                  "bg_color": header_bg,
                  "border": 2,
                  "font_color": "#000000",
                  "align": "center",
                  "valign": "vcenter",
            })

            worksheet.write(startrow, startcol + col_num, str(col_name), header_format)

            column_series = df[col_name]
            if isinstance(column_series, pd.DataFrame):
                  column_series = column_series.iloc[:, 0]

            max_length = max(
                  column_series.fillna("").astype(str).str.len().max(skipna=True) or 0,
                  len(str(col_name)),
            )
            worksheet.set_column(startcol + col_num, startcol + col_num, max_length + 5)

      # ---------- BODY ----------
      center_format = workbook.add_format({
            "align": "center",
            "valign": "center",
            "border": 1,
            "border_color": "#000000",
            "bold": True,
      })

      ok_format = workbook.add_format({
            "bg_color": "#90EE90",
            "font_color": "#000000",
            "align": "center",
            "valign": "center",
      })

      not_ok_format = workbook.add_format({
            "bg_color": "#FF0000",
            "font_color": "#FFFFFF",
            "align": "center",
            "valign": "center",
      })

      for row_num in range(len(df)):
            worksheet.set_row(startrow + row_num + 1, 15)

            for col_num in range(len(df.columns)):
                  cell_raw = df.iloc[row_num, col_num]
                  cell_value = "" if pd.isna(cell_raw) else str(cell_raw)

                  format_style = center_format

                  if cell_value == "OK":
                        format_style = ok_format
                  elif cell_value in ["NOT OK", "NOK"]:
                        format_style = not_ok_format
                  elif cell_value in ["Missing", "Missing in Post"]:
                        format_style = workbook.add_format({
                        "bg_color": "#E78978",
                        "font_color": "#FFFFFF",
                        "align": "center",
                        "valign": "center",
                        "bold": True,
                        "border": 1,
                  })
                  elif "|" in cell_value:
                        format_style = workbook.add_format({
                        "font_color": "#FF0000",
                        "align": "center",
                        "valign": "center",
                        "bold": True,
                        "border": 1,
                        "border_color": "#000000",
                  })

                  worksheet.write(
                  startrow + row_num + 1,
                  startcol + col_num,
                  cell_value,
                  format_style
                  )



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
                  r'\s*(\d+)\s+(\d+\s+\((?:UNLOCKED)\))\s+(\d+\s+\((?:ENABLED)\))\s+(.*)$',
                  r'^Total:\s\d+',
                  file_content
            )
            
            invxr_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\s+invxr',
                  r'(ID)\s+(LINK)\s+(RiL)\s+(WL1)\s+(TEMP1)\s+(TXbs1)\s+(TXdBm1)\s+(RXdBm1)\s+(BER1)\s+(WL2)\s+(TEMP2)\s+(TXbs2)\s+(TXdBm2)\s+(RXdBm2)\s+(BER2)\s+(DlLoss)\s+(UlLoss)\s+(LENGTH)\s+(TT)',
                  # r'^\s*(\d+)\s+(\w+)\s+(S\d+_N1-1)?\s+(\d+\.\d+)\s+(\d+C)\s+(\d+%)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)?\s*(\d+\.\d+)?\s+(\d+\.\d+)\s+(\d+C)\s+(\d+%)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)?\s+(-?\d+\.\d+)?\s+(-?\d+\.\d+)?\s+(-?\d+\.\d+)?\s+(\d+m)\s+(\d+)\s*$',
                  r'^\s*(\d+)\s+(\S+)\s+(S\d+_N1(?:-1)?)\s+(\d+\.\d+)\s+(\d+C)\s+(\d+%)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s*(-?\d+\.\d+)?\s*(\d+\.\d+)\s+(\d+C)\s+(\d+%)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s*(-?\d+\.\d+)?\s*(-?\d+\.\d+|\d+)?\s+(-?\d+\.\d+|\d+)?\s+(\d+m)\s+(\d+)\s*$',
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
                  r'^\s*(FieldReplaceableUnit=\S+)\s+(.+?)\s+([A-Z]{3}\s+\d+\s+\d+\/\d+)\s+([A-Z0-9\/]+)\s+(\d{8})\s+(\S+)\s*$',
                  r'^Total:\s\d+',
                  file_content
            )

            hget_amf_add_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\s*hget\s+amf\s+add',
                  r'MO\s+ipv4Address1\s+ipv4Address2\s+ipv6Address1\s+ipv6Address2\s+usedIpAddress',
                  r'^\s*(TermPointToAmf=1)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s*$',
                  r'^Total:\s*\d+',
                  file_content
            )


            print("invxr_df================:- ", invxr_df)
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
                  "hget amf add": hget_amf_add_df,

            }
            df_list = sheets.values()
            # print("df_list:- ",[df_list])
            all_files_df = pd.concat([all_files_df,*df_list], axis=0,ignore_index=True)
            # print("all_files_df:- ",all_files_df)
            with pd.ExcelWriter(excel_filename, engine="xlsxwriter") as writer:
                  for sheet_name, df in sheets.items():
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                        # format_excel_sheet(writer, sheet_name, df)

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
            # template_path = os.path.join(template_file_path, "5G_template.xlsx")
            # SA_5G_df : pd.DataFrame = pd.ExcelFile(template_path,).parse("5G SA")
            # enbid_df : pd.DataFrame = pd.ExcelFile(template_path,).parse("Anchor Node ENBID")
            # template_df : pd.DataFrame = pd.ExcelFile(template_path,).parse("Summary")
            template_path = os.path.join(template_file_path, "5G_template.xlsx")
            tpl_xls = pd.ExcelFile(template_path)

            SA_5G_df = tpl_xls.parse("5G SA")
            enbid_df = tpl_xls.parse("Anchor Node ENBID")
            template_df = tpl_xls.parse("Summary")


            print(xls.sheet_names)
            for  sheet_name in xls.sheet_names:
                  print(sheet_name)
                  if sheet_name == "St cell":
                        df = xls.parse(sheet_name)
                        
                        if "MO" in df.columns:
                              # Extract the 'circle' part from 'MO' column
                              circle = df["MO"].str.extract(r"NRCellDU=([A-Z]{2})_").dropna()

                              circle = circle.replace("UW", "UPW")
                              if not circle.empty:
                                    circle_value = circle.iloc[0, 0].strip()
                              else:
                                    circle_value = "NA"
                              template_df.loc[0, "Circle"] = circle_value
                              SA_5G_df.loc[0, "Circle"] = circle_value
                              layer = df["MO"].str.extract(r"NRCellDU=\w+_(F\d|T\d)")[0]
                              layer_value = '_'.join(layer.dropna().unique()) if not layer.dropna().empty else "NA"
                              print("Layer Value:", layer_value)
                              layer_mapping = {
                                    "T1": "5G_Upgrade",
                                    "T2": "5G_Upgrade",
                              }
                              l_layers = [
                                    layer_mapping.get(l, l) for l in layer_value.split("_")
                              ]
                              l_layers = list(set(l_layers))
                              template_df.loc[0, "Technology"] = "_".join(l_layers)
                              print("Technology:", l_layers)
                              
                              site_ids = (
                              df["MO"]
                              .str.extract(r"NRCellDU=([\w_]+)")[0]
                              .dropna()
                              )

                              for site_value in site_ids:
                                    parts = site_value.split("_")
                                    if len(parts) >= 7:
                                          raw_site = parts[6]          
                                          site = raw_site.lstrip("x") 

                                          # safety cleanup
                                          site = site.rstrip("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

                                          template_df.loc[0, "Site ID (2G)"] = site
                                          print("2G SiteID:", site)
                                          SA_5G_df.loc[0, "Site ID"] = site


                              cell_name_series = df["MO"].str.extract(r"NRCellDU=([\w_]+)")[0].dropna()
                              print("Cell names :", cell_name_series)
                              template_df.loc[0, "5G Cell name A"] = "NA"
                              template_df.loc[0, "5G Cell name B"] = "NA"
                              template_df.loc[0, "5G Cell name C"] = "NA"
                              SA_5G_df.loc[0, "5G Cell name A"] = "NA"
                              SA_5G_df.loc[0, "5G Cell name B"] = "NA"
                              SA_5G_df.loc[0, "5G Cell name C"] = "NA"
                              SA_5G_df.loc[0, "5G Cell name D"] = "NA"
                              SA_5G_df.loc[0, "5G Cell name E"] = "NA"
                              SA_5G_df.loc[0, "5G Cell name F"] = "NA"
                              SA_5G_df.loc[0, "5G Cell name G"] = "NA"
                              SA_5G_df.loc[0, "5G Cell name H"] = "NA"
                              SA_5G_df.loc[0, "5G Cell name I"] = "NA"
                              for cn in cell_name_series:

                                    if cn.endswith("A"):
                                          template_df.loc[0, "5G Cell name A"] = cn 
                                          SA_5G_df.loc[0, "5G Cell name A"] = cn
                                          # print("5G Cell name A:", cn)
                                    elif cn.endswith("B"):
                                          template_df.loc[0, "5G Cell name B"] = cn
                                          SA_5G_df.loc[0, "5G Cell name B"] = cn
                                    elif cn.endswith("C"):
                                          template_df.loc[0, "5G Cell name C"] = cn
                                          SA_5G_df.loc[0, "5G Cell name C"] = cn
                                    elif cn.endswith("D"):
                                          SA_5G_df.loc[0, "5G Cell name D"] = cn
                                    elif cn.endswith("E"):
                                          SA_5G_df.loc[0, "5G Cell name E"] = cn
                                    elif cn.endswith("F"):
                                          SA_5G_df.loc[0, "5G Cell name F"] = cn
                                    elif cn.endswith("G"):
                                          SA_5G_df.loc[0, "5G Cell name G"] = cn
                                    elif cn.endswith("H"):
                                          SA_5G_df.loc[0, "5G Cell name H"] = cn
                                    elif cn.endswith("I"):
                                          SA_5G_df.loc[0, "5G Cell name I"] = cn
                                    
                                    else:
                                          template_df.loc[0, "5G Cell name A"] = "NA"
                                          template_df.loc[0, "5G Cell name B"] = "NA"
                                          template_df.loc[0, "5G Cell name C"] = "NA"
                                          SA_5G_df.loc[0, "5G Cell name A"] = "NA"
                                          SA_5G_df.loc[0, "5G Cell name B"] = "NA"
                                          SA_5G_df.loc[0, "5G Cell name C"] = "NA"
                                          SA_5G_df.loc[0, "5G Cell name D"] = "NA"
                                          SA_5G_df.loc[0, "5G Cell name E"] = "NA"
                                          SA_5G_df.loc[0, "5G Cell name F"] = "NA"
                                          SA_5G_df.loc[0, "5G Cell name G"] = "NA"
                                          SA_5G_df.loc[0, "5G Cell name H"] = "NA"
                                          SA_5G_df.loc[0, "5G Cell name I"] = "NA"

                              BB_config = df["MO"].str.extract(r"(?:NRCellDU|EUtranCell(?:FDD|TDD))=\w+_(F\d|T\d)")[0]
                              # print("BB_config:", BB_config)
                              if BB_config.str.contains(r"F1|F2|F3|T1|T2", na=False).any():
                                    SA_5G_df.loc[0, "5G BB Config"] = "LTE+NR"
                                    template_df.loc[0, "5G BB Config"] = "LTE+NR"
                              elif BB_config.str.contains(r"5_EE_T1", na=False).any():
                                    SA_5G_df.loc[0, "5G BB Config"] = "NR+NR"
                                    template_df.loc[0, "5G BB Config."] = "NR"
                              
                              cell_count = df['MO'].str.extract(r'(GNBDUFunction)')
                              # print("Cell Count:", cell_count)
                              SA_5G_df.loc[0, "No. Of Cells"] = cell_count.count()[0] if cell_count.count()[0] else "NA"
                              SA_5G_df.loc[0, "No Of RRU"] = cell_count.count()[0] if cell_count.count()[0] else "NA"

                              template_df.loc[0, 'No of Cell'] = cell_count.count()[0] if cell_count.count()[0] else "NA"
                              template_df.loc[0, 'No Of RRU'] = cell_count.count()[0] if cell_count.count()[0] else "NA"

                        else:
                              print(f"'MO' column not found in sheet 'St cell' for file: {file}")
                              template_df.loc[0, "Circle"] = "NA"
                              # Fill other MO-related fields as "NA"
                              template_df.loc[0, [
                                    "Technology", "Site ID (2G)", 
                                    "5G Cell name A", "5G Cell name B", "5G Cell name C",
                                    "5G BB Config", "No of Cell","No. Of Cells", "No Of RRU"
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

                        SA_5G_df.loc[0, "Site Lat/Long"] = f"{latitude}, {longitude}"
                        
                  if sheet_name == "Nrtac":
                        df = xls.parse(sheet_name)
                        if "Value" in df.columns:
                              tac = df["Value"].dropna().iloc[0] if not df["Value"].dropna().empty else "NA"      
                        else:
                              print(f"'Value' column not found in sheet '{sheet_name}' for file: {file}")
                              tac = "NA"
                        # print("TAC:", tac)
                        SA_5G_df.loc[0, "TAC"] = tac
                        template_df.loc[0, "TAC"] = tac

                  
                  if sheet_name == "Gnbid":
                        df = xls.parse(sheet_name)
                        if "Value" in df.columns:
                              gnb_id = df["Value"].dropna().iloc[0] if not df["Value"].dropna().empty else "NA"
                        else:
                              print(f"'Value' column not found in sheet '{sheet_name}' for file: {file}")
                              gnb_id = "NA"
                        # print("GNB ID:", gnb_id)
                        template_df.loc[0, "GNodebID"] = gnb_id

                  if sheet_name == "st termpointtoenode":
                        df = xls.parse(sheet_name)
                        df.columns = df.columns.astype(str).str.strip()

                        required_cols = {"Adm State", "Op. State", "MO"}
                        if required_cols.issubset(df.columns):

                              filtered_df = df[
                                    df["Adm State"].str.contains("UNLOCKED", na=False) &
                                    df["Op. State"].str.contains("ENABLED", na=False)
                              ].copy()

                              if not filtered_df.empty:

                                    # ---- Extract ENBID ----
                                    filtered_df["Enbid"] = filtered_df["MO"].str.extract(
                                    r'ExternalENodeBFunction=auto404_\d+_\d+_(\d+)'
                                    ).astype(int)

                                    # ---- COUNT CELLS PER ENBID ----
                                    enbid_count_df = (
                                    filtered_df
                                    .groupby("Enbid")
                                    .size()
                                    .reset_index(name="Count")
                                    )

                                    # ---- Take max 15 ENBIDs randomly ----
                                    enbid_count_df = (
                                    enbid_count_df
                                    .sample(n=min(15, len(enbid_count_df)), random_state=1)
                                    .sort_values("Enbid")
                                    .reset_index(drop=True) 
                                    )

                                    print(enbid_count_df)

                                    # ---- Fill enbid_df ----
                                    for idx, row in enbid_count_df.iterrows():
                                          enbid_df.loc[idx, "Enbid"] = row["Enbid"]
                                          enbid_df.loc[idx, "Count"] = row["Count"]

                              else:
                                    print(f"No matching unlocked/enabled ENBs in {file}")
                        else:
                              print(f"Missing required columns in 'st termpointtoenode' for file: {file}")


                  
                  # if sheet_name == "st termpointtoenode":
                  #       df = xls.parse(sheet_name)
                  #       df.columns = df.columns.astype(str).str.strip()  # Clean column names

                  #       required_cols = {"Adm State", "Op. State", "MO"}
                  #       if required_cols.issubset(df.columns):
                  #             filtered_df = df[
                  #                   df["Adm State"].str.contains("UNLOCKED", na=False) &
                  #                   df["Op. State"].str.contains("ENABLED", na=False)
                  #             ].copy()

                  #             if not filtered_df.empty:
                  #                   filtered_df["Enbid"] = filtered_df["MO"].str.extract(
                  #                   r'ExternalENodeBFunction=auto404_\d+_\d+_(\d+)')
                  #                   filtered_df.dropna(subset=["Enbid"], inplace=True)

                  #                   # Take 15 random enbids
                  #                   result_df = (filtered_df.sample(
                  #                   n=min(15, len(filtered_df)), random_state=1)["Enbid"].astype(int).sort_values().tolist())

                  #                   print("Random ENBIDs:", result_df)


                  #                   for idx, enbid in enumerate(result_df):
                  #                         enbid_df.loc[idx, "Enbid"] = enbid

                  #             else:
                  #                   print(f"No matching unlocked/enabled ENBs in {file}")
                  #       else:
                  #             print(f"Missing required columns in 'st termpointtoenode' for file: {file}")



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
                                    SA_5G_df.loc[0, "OSS Name"] = OSS
                                    template_df["OSS/ENM Name"] = template_df["OSS/ENM Name"].astype(object)
                                    template_df.loc[0, "OSS/ENM Name"] = OSS
                              else:
                                    SA_5G_df.loc[0, "OSS Name"] = SA_5G_df.loc["OSS Name"].astype(object)
                                    SA_5G_df.loc[0, "OSS Name"] = "NA"
                                    template_df["OSS/ENM Name"] = template_df["OSS/ENM Name"].astype(object)
                                    template_df.loc[0, "OSS/ENM Name"] = "NA"
                        else:
                              print(f"'Value' column not found in sheet 'get . Enroll' for file: {file}")
                              # SA_5G_df.loc[0, "OSS Name"] = SA_5G_df.loc["OSS Name"].astype(object)
                              SA_5G_df.loc[0, "OSS Name"] = "NA"
                              template_df["OSS/ENM Name"] = template_df["OSS/ENM Name"].astype(object)
                              template_df.loc[0, "OSS/ENM Name"] = "NA"
                              
                  if sheet_name == "hget field prod":
                        print("Processing hget field prod")

                        df = xls.parse(sheet_name)
                        df.columns = df.columns.astype(str).str.strip()

                        print("Columns:", df.columns.tolist())
                        print(df.head())

                        if "productName" in df.columns and not df.empty:

                              air_products = df[
                                    df["productName"].astype(str).str.contains("AIR", case=False, na=False)
                              ]["productName"]

                              print("AIR Products:")
                              print(air_products)

                              if not air_products.empty:
                                    first_air = air_products.iloc[0]
                                    count = (df["productName"] == first_air).sum()

                                    product_display = f"{first_air}*{count}"
                              else:
                                    product_display = "NA"

                              print("Result:", product_display)

                              template_df.loc[
                                    0,
                                    "Other Hardware Related Additional Information"
                              ] = product_display

                        else:
                              print("productName column not found")
                              template_df.loc[
                                    0,
                                    "Other Hardware Related Additional Information"
                              ] = "NA"
                  
                  if sheet_name == "hget amf add":
                        df = xls.parse(sheet_name)
                        df.columns = df.columns.astype(str).str.strip()

                        amf_ip = " , ".join(
                              pd.concat([
                                    df.get("ipv6Address1", pd.Series()),
                                    df.get("ipv6Address2", pd.Series())
                              ])
                              .dropna()
                              .astype(str)
                              .tolist()
                        )

                        SA_5G_df.loc[0, "AMF IP"] = amf_ip if amf_ip else "NA"

                  if "get 0" in xls.sheet_names:
                        df_0 = xls.parse("get 0", header=None)

                        if not df_0.empty:
                              # Extract MO Name
                              MO_name_0 = "/".join(
                                    cell.split("=")[-1]
                                    for cell in df_0.iloc[0]
                                    if isinstance(cell, str) and "ManagedElement=" in cell
                              )
                              SA_5G_df.loc[0, "Site ID (5G/)/MRBTS ID"] = MO_name_0
                              SA_5G_df.loc[0, "MO Name"] = MO_name_0
                              template_df.loc[0, "MO Name"] = MO_name_0
                              template_df.loc[0, "SiteID(5G/)/MRBTSID"] = MO_name_0
                              enbid_df["5G Site Id"] = (
                                    MO_name_0 if isinstance(MO_name_0, str)
                                    else MO_name_0.dropna().iloc[0] if not MO_name_0.dropna().empty
                                    else "NA"
                              )
                              enbid_df["5G Site Id"] = enbid_df["5G Site Id"].ffill()

                              # Find SW Version
                              sw_version_rows = df_0[df_0.iloc[:, 0] == "swVersion"]
                              if not sw_version_rows.empty:
                                    sw_version = "L" + str(sw_version_rows.iloc[0, 1])
                                    SA_5G_df.loc[0, "SW Version"] = sw_version
                                    template_df.loc[0, "SW Version"] = sw_version
                              else:
                                    SA_5G_df.loc[0, "SW Version"] = "NA"
                                    template_df.loc[0, "SW Version"] = "NA"
                        else:
                              print(f"'get 0' sheet is empty in file: {file}")
                              template_df.loc[0, "MO Name"] = "NA"
                              template_df.loc[0, "SiteID(5G/)/MRBTSID"] = "NA"
                              enbid_df.loc[0, "5G Site Id"] = "NA"
                              SA_5G_df.loc[0, "5G Site Id"] = "NA"
                              template_df.loc[0, "SW Version"] = "NA"
                  else:
                        template_df.loc[0, "MO Name"] = "NA"
                        template_df.loc[0, "SiteID(5G/)/MRBTSID"] = "NA"
                        enbid_df.loc[0, "5G Site Id"] = "NA"
                        SA_5G_df.loc[0, "5G Site Id"] = "NA"
                        template_df.loc[0, "SW Version"] = "NA"

            # if sheet_name == "hget field prod":
            #       df = xls.parse(sheet_name)
            #       df.columns = df.columns.astype(str).str.strip()  # Clean column names

            #       if "productName" in df.columns and not df.empty:
            #             first_product = df["productName"].dropna().iloc[0] if not df["productName"].dropna().empty else "NA"
            #             count = (df["productName"] == first_product).sum()
            #             product_display = f"{first_product}*{count}"
            #             print("Result:", product_display)
            #             template_df.loc[0, "Other Hardware Related Additional Information"] = product_display
            #       else:
            #             print(f"'productName' column missing or sheet is empty in file: {file}")
            #             template_df.loc[0, "Other Hardware Related Additional Information"] = "NA"

            



                  today = datetime.date.today()
                  template_df.loc[0, "Offer Date"] = today.strftime("%d-%m-%Y")
                  df.columns = df.columns.astype(str).str.strip()  # Clean column names
                  if "IP_Addr" in df.columns:
                        ip_values = df["IP_Addr"].dropna()
                        print("IP Values:", ip_values)
                        SA_5G_df.loc[0, "5G Node IP"] = ip_values.iloc[0] if not ip_values.empty else "NA"
                        template_df.loc[0, "5G Node IP"] = ip_values.iloc[0] if not ip_values.empty else "NA"

                  else:
                        print(f"'IP_Addr' column not found in sheet for file: {file}")
                        SA_5G_df.loc[0, "5G Node IP"] = "NA"
                        template_df.loc[0, "5G Node IP"] = "NA"
                  SA_5G_df.loc[0,"AT Type"] = "Soft"
                  SA_5G_df.loc[0,"OEM"] = "Ericsson"
                  SA_5G_df.loc[0,"TSP"] = "Mobilecomm"
                  SA_5G_df.loc[0,"Technology"] = "5G - Standalone"
                  SA_5G_df.loc[0,"Ping command"] = "mcc Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR "
                  SA_5G_df.loc[0,"Integration Date"] = datetime.date.today().strftime("%d-%m-%Y")
                  SA_5G_df.loc[0,"On-Air Date"] = datetime.date.today().strftime("%d-%m-%Y")
                  SA_5G_df.loc[0,"Offer Date"] = datetime.date.today().strftime("%d-%m-%Y")
                  SA_5G_df.loc[0,"5G cell name nomenclature compliance"] = "YES"
                  SA_5G_df.loc[0,"QIA Alarms : No active alarm ( except external alarm)/No false alarm in  iOMS or OSS Monitor"] = "NO"
                  SA_5G_df.loc[0,"Xn interface Configuration check "] = "YES"
                  SA_5G_df.loc[0, "Site should be on Latest Software release"] = "YES"
                  SA_5G_df.loc[0, "5G should be properly configured and  should be enabled and unlocked in core nodes"] = "YES"
                  SA_5G_df.loc[0, "Ping test towards AMF"] = "YES"
                  SA_5G_df.loc[0, "Ping test towards UPF"] = "YES"
                  SA_5G_df.loc[0, "CCTR / EBS Profile validation"] = "YES"
                  SA_5G_df.loc[0, "SCTP Association should be UP"] = "YES"
                  
                  
                  template_df.loc[0,"AT Type"] = "Soft"
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

            # with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
                  
            #       SA_5G_df.to_excel(writer, sheet_name="5G SA", index=False)
            #       format_excel_sheet(writer, "5G SA", SA_5G_df)
            #       enbid_df.to_excel(writer, sheet_name="Anchor Node ENBID", index=False)
            #       format_excel_sheet(writer, "Anchor Node ENBID", enbid_df)
            #       template_df.to_excel(writer, sheet_name="Detail", index=False)
            #       format_excel_sheet(writer, "Detail", template_df)
            
            with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
                  SA_5G_df.to_excel(writer, sheet_name="5G SA", index=False)
                  format_excel_sheet(writer, "5G SA", SA_5G_df)
                  enbid_df.to_excel(writer, sheet_name="Anchor Node ENBID", index=False)
                  format_excel_sheet(writer, "Anchor Node ENBID", enbid_df)
                  template_df.to_excel(writer, sheet_name="Detail", index=False)
                  format_excel_sheet(writer, "Detail", template_df)




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
                              
      zip_filename = f"soft_at_5G_Summary_Ericsson/5gSUMMARY_OUTPUT_{timestamp}.zip"
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
            
            featureState_CXC4012559_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\sCXC4012559',
                  r'^\s*(\d+)\s+([A-Za-z0-9=,]+)\s*$',
                  r'^\s*([a-zA-Z0-9]+)\s+(.+?)\s*$',
                  r'^Total:\s\d+\sMOs',
                  file_content
            )
            # if not featureState_CXC4012559_df.empty:
            #       expected_cols = featureState_CXC4012559_df.columns.tolist()
            #       if len(expected_cols) >= 2:
            #             featureState_CXC4012559_df.columns = ['MO', 'Attribute'] + expected_cols[2:]

            featureState_CXC4012379_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\sCXC4012379',
                  r'^\s*(\d+)\s+([A-Za-z0-9=,]+)\s*$',
                  r'^\s*([a-zA-Z0-9]+)\s+(.+?)\s*$',
                  r'^Total:\s\d+\sMOs',
                  file_content
            )

            featureState_CXC4012475_df = explode_data_from_log(   
                  r'[A-Z0-9_-]+>\sget\sCXC4012475',
                  r'^\s*(\d+)\s+([A-Za-z0-9=,]+)\s*$',
                  r'^\s*([a-zA-Z0-9]+)\s+(.+?)\s*$',
                  r'^Total:\s\d+\sMOs',
                  file_content
            )
            featureState_CXC4012531_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\sCXC4012531',
                  r'^\s*(\d+)\s+([A-Za-z0-9=,]+)\s*$',
                  r'^\s*([a-zA-Z0-9]+)\s+(.+?)\s*$',
                  r'^Total:\s\d+\sMOs',
                  file_content

            )
            featureState_CXC4012659_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\sCXC4012659',
                  r'^\s*(\d+)\s+([A-Za-z0-9=,]+)\s*$',
                  r'^\s*([a-zA-Z0-9]+)\s+(.+?)\s*$',
                  r'^Total:\s\d+\sMOs',
                  file_content
            )
            featureState_CXC4012729_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\sCXC4012729',
                  r'^\s*(\d+)\s+([A-Za-z0-9=,]+)\s*$',
                  r'^\s*([a-zA-Z0-9]+)\s+(.+?)\s*$',
                  r'^Total:\s\d+\sMOs',
                  file_content
            )
            feature_dfs = {
                  "CXC4012559": featureState_CXC4012559_df,
                  "CXC4012379": featureState_CXC4012379_df,
                  "CXC4012475": featureState_CXC4012475_df,
                  "CXC4012531": featureState_CXC4012531_df,
                  "CXC4012659": featureState_CXC4012659_df,
                  "CXC4012729": featureState_CXC4012729_df,
                  }

            for key, df in feature_dfs.items():
                  if not df.empty and len(df.columns) >= 2:
                        df.columns = ['MO', 'Attribute'] + df.columns.tolist()[2:]

            # get_sNSSAIList_df = explode_data_from_log(
            #       r'[A-Z0-9_-]+>\s*get\s+\.\s*sNSSAIList',
            #       r'^(MO)\s+(Attribute)\s+(Value)$',
            #       r'^\s*((?:NRCellCU|NRCellDU|GNBCUUPFunction)=[^\s]+)\s+'
            #       r'(sNSSAIList)\s+'
            #       r'(t\[\d+\]\s*=)',
            #       r'^Total:\s+\d+\s+MOs',
            #       file_content
            #       )
            # # -------- Struct Value Add ----------
            # struct_text = " ".join([l.strip() for l in file_content if "Struct[" in l or ".sd" in l or ".sst" in l])
 
            # struct_text = struct_text.replace(">>>","")
            # struct_text = struct_text.replace("has 2 members:","")
            # struct_text = struct_text.replace("1.","")
            # struct_text = struct_text.replace("2.","")
            # get_sNSSAIList_df["Value"] = get_sNSSAIList_df["Value"] + " " + struct_text
            # print("get_sNSSAIList_df", get_sNSSAIList_df)
            get_sNSSAIList_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\s*get\s+\.\s*sNSSAIList',
                  r'^(MO)\s+(Attribute)\s+(Value)$',
                  r'^\s*((?:NRCellCU|NRCellDU|GNBCUUPFunction)=[^\s]+)\s+'
                  r'(sNSSAIList)\s+'
                  r'(t\[\d+\]\s*=)',
                  r'^Total:\s+\d+\s+MOs',
                  file_content
                  )


            if get_sNSSAIList_df is None or get_sNSSAIList_df.empty:
                  get_sNSSAIList_df = pd.DataFrame()
            else:
                  if "Value" not in get_sNSSAIList_df.columns:
                        get_sNSSAIList_df["Value"] = ""


                  # -------- Struct Value Add ----------
                  struct_text = " ".join(
                  [l.strip() for l in file_content if "Struct[" in l or ".sd" in l or ".sst" in l]
                  )

                  struct_text = struct_text.replace(">>>", "")
                  struct_text = struct_text.replace("has 2 members:", "")
                  struct_text = struct_text.replace("1.", "")
                  struct_text = struct_text.replace("2.", "")

                  get_sNSSAIList_df["Value"] = get_sNSSAIList_df["Value"] + " " + struct_text


                  # -------- SIMPLE CLEANING ----------
                  get_sNSSAIList_df["Value"] = (
                  get_sNSSAIList_df["Value"]
                  .str.replace(r't\[\d+\]\s*=', '', regex=True)      # remove t[4] =
                  .str.replace(r'Struct\[\d+\]', '', regex=True)    # remove Struct[3]
                  .str.replace(r'\s+', ' ', regex=True)             # remove extra spaces
                  .str.strip()
                  )
                  # keep only complete sd-sst pairs
                  get_sNSSAIList_df["Value"] = get_sNSSAIList_df["Value"].str.findall(
                  r'sd\s*=\s*\d+\s+sst\s*=\s*\d+'
                  )

                  # remove duplicates (keep order)
                  get_sNSSAIList_df["Value"] = get_sNSSAIList_df["Value"].apply(
                  lambda x: " ".join(dict.fromkeys(x))
                  )
                  print("get_sNSSAIList_df")
                  print(get_sNSSAIList_df)

            sheets = {
                  'get . Latitude': Latitude_df,
                  'get . Longitude': Longitude_df,
                  'get . Linkrate': Linkrate_df,
                  'get . Digitaltilt': Digitaltilt_df,
                  'invl basic': invl_basic_df,

                  'get CXC4012559': featureState_CXC4012559_df,
                  'get CXC4012379': featureState_CXC4012379_df,
                  'get CXC4012475': featureState_CXC4012475_df,
                  'get CXC4012531': featureState_CXC4012531_df,
                  'get CXC4012659': featureState_CXC4012659_df,
                  'get CXC4012729': featureState_CXC4012729_df,
                  'get . sNSSAIList': get_sNSSAIList_df,
                  }
            df_list = sheets.values()
            # print("df_list:- ",[df_list])
            all_files_df = pd.concat([all_files_df,*df_list], axis=0,ignore_index=True)
            # print("all_files_df:- ",all_files_df)
            with pd.ExcelWriter(excel_filename, engine="xlsxwriter") as writer:
                  for sheet_name, df in sheets.items():
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                        # format_excel_sheet(writer, sheet_name, df)

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

                  elif sheet_name == "get CXC4012559":
                        df = xls.parse(sheet_name).copy()

                        if required_columns_present(df, ["MO", "Attribute", "Node_ID"]):

                              df.columns = df.columns.astype(str).str.strip()
                              df["MO"] = df["MO"].astype(str).str.strip()
                              df["Attribute"] = df["Attribute"].astype(str).str.strip()

                              expected = {
                                    "featureState": "1 (ACTIVATED)"
                              }

                              ok_status_list = df.apply(
                                    lambda x: "OK" 
                                    if x['MO'] in expected and x['Attribute'] == expected[x['MO']]
                                    else "NOT OK" if x['MO'] in expected
                                    else None,
                                    axis=1
                              ).dropna().tolist()

                              site_id = df['Node_ID'].unique()[0] if 'Node_ID' in df.columns else None

                              checklist_df.at[idx, 'Site_ID'] = site_id
                              checklist_df.at[idx, 'Remark'] = 'OK' if any(status == 'OK' for status in ok_status_list) else 'NOT OK'
                              checklist_df.at[idx, 'Checkpoint'] = str(sheet_name)

                        else:
                              checklist_df.at[idx + 1, 'Remark'] = 'Missing'
                              checklist_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)
                  
                  
                  elif sheet_name == "get CXC4012379":
                        df = xls.parse(sheet_name).copy()

                        if required_columns_present(df, ["MO", "Attribute", "Node_ID"]):

                              df.columns = df.columns.astype(str).str.strip()
                              df["MO"] = df["MO"].astype(str).str.strip()
                              df["Attribute"] = df["Attribute"].astype(str).str.strip()

                              expected = {
                                    "featureState": "1 (ACTIVATED)"
                              }

                              ok_status_list = df.apply(
                                    lambda x: "OK" 
                                    if x['MO'] in expected and x['Attribute'] == expected[x['MO']]
                                    else "NOT OK" if x['MO'] in expected
                                    else None,
                                    axis=1
                              ).dropna().tolist()

                              site_id = df['Node_ID'].unique()[0] if 'Node_ID' in df.columns else None

                              checklist_df.at[idx, 'Site_ID'] = site_id
                              checklist_df.at[idx, 'Remark'] = 'OK' if any(status == 'OK' for status in ok_status_list) else 'NOT OK'
                              checklist_df.at[idx, 'Checkpoint'] = str(sheet_name)

                        else:
                              checklist_df.at[idx + 1, 'Remark'] = 'Missing'
                              checklist_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)
                  
                  
                  elif sheet_name == "get CXC4012475":
                        df = xls.parse(sheet_name).copy()

                        if required_columns_present(df, ["MO", "Attribute", "Node_ID"]):

                              df.columns = df.columns.astype(str).str.strip()
                              df["MO"] = df["MO"].astype(str).str.strip()
                              df["Attribute"] = df["Attribute"].astype(str).str.strip()

                              expected = {
                                    "featureState": "1 (ACTIVATED)"
                              }

                              ok_status_list = df.apply(
                                    lambda x: "OK" 
                                    if x['MO'] in expected and x['Attribute'] == expected[x['MO']]
                                    else "NOT OK" if x['MO'] in expected
                                    else None,
                                    axis=1
                              ).dropna().tolist()

                              site_id = df['Node_ID'].unique()[0] if 'Node_ID' in df.columns else None

                              checklist_df.at[idx, 'Site_ID'] = site_id
                              checklist_df.at[idx, 'Remark'] = 'OK' if any(status == 'OK' for status in ok_status_list) else 'NOT OK'
                              checklist_df.at[idx, 'Checkpoint'] = str(sheet_name)

                        else:
                              checklist_df.at[idx + 1, 'Remark'] = 'Missing'
                              checklist_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)
                  
                  
                  elif sheet_name == "get CXC4012531":
                        df = xls.parse(sheet_name).copy()

                        if required_columns_present(df, ["MO", "Attribute", "Node_ID"]):

                              df.columns = df.columns.astype(str).str.strip()
                              df["MO"] = df["MO"].astype(str).str.strip()
                              df["Attribute"] = df["Attribute"].astype(str).str.strip()

                              expected = {
                                    "featureState": "1 (ACTIVATED)"
                              }

                              ok_status_list = df.apply(
                                    lambda x: "OK" 
                                    if x['MO'] in expected and x['Attribute'] == expected[x['MO']]
                                    else "NOT OK" if x['MO'] in expected
                                    else None,
                                    axis=1
                              ).dropna().tolist()

                              site_id = df['Node_ID'].unique()[0] if 'Node_ID' in df.columns else None

                              checklist_df.at[idx, 'Site_ID'] = site_id
                              checklist_df.at[idx, 'Remark'] = 'OK' if any(status == 'OK' for status in ok_status_list) else 'NOT OK'
                              checklist_df.at[idx, 'Checkpoint'] = str(sheet_name)

                        else:
                              checklist_df.at[idx + 1, 'Remark'] = 'Missing'
                              checklist_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)
                  
                  
                  elif sheet_name == "get CXC4012659":
                        df = xls.parse(sheet_name).copy()

                        if required_columns_present(df, ["MO", "Attribute", "Node_ID"]):

                              df.columns = df.columns.astype(str).str.strip()
                              df["MO"] = df["MO"].astype(str).str.strip()
                              df["Attribute"] = df["Attribute"].astype(str).str.strip()

                              expected = {
                                    "featureState": "1 (ACTIVATED)"
                              }

                              ok_status_list = df.apply(
                                    lambda x: "OK" 
                                    if x['MO'] in expected and x['Attribute'] == expected[x['MO']]
                                    else "NOT OK" if x['MO'] in expected
                                    else None,
                                    axis=1
                              ).dropna().tolist()

                              site_id = df['Node_ID'].unique()[0] if 'Node_ID' in df.columns else None

                              checklist_df.at[idx, 'Site_ID'] = site_id
                              checklist_df.at[idx, 'Remark'] = 'OK' if any(status == 'OK' for status in ok_status_list) else 'NOT OK'
                              checklist_df.at[idx, 'Checkpoint'] = str(sheet_name)

                        else:
                              checklist_df.at[idx + 1, 'Remark'] = 'Missing'
                              checklist_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)
                  
                  
                  elif sheet_name == "get . sNSSAIList":

                        df = xls.parse(sheet_name).copy()
                        if required_columns_present(df, ["MO", "Attribute","Value", "Node_ID"]):
                              df.columns = df.columns.str.strip()
                              print("=======", df.columns.tolist())
                              
                              df["MO"] = df["MO"].astype(str).str.strip()
                              df["Attribute"] = df["Attribute"].astype(str).str.strip()
                              df["Value"] = df["Value"].astype(str).str.strip()

                              # Expected SD/SST combinations per MO
                              expected = {
                                    "NRCellDU": ["sd = 1 sst = 1", "sd = 2 sst = 1", "sd = 3 sst = 1", "sd = 4 sst = 1"],
                                    "NRCellCU": ["sd = 1 sst = 1", "sd = 2 sst = 1", "sd = 3 sst = 1", "sd = 4 sst = 1"],
                                    "GNBCUUPFunction": ["sd = 1 sst = 1", "sd = 2 sst = 1", "sd = 3 sst = 1", "sd = 4 sst = 1"]
                              }

                              # Function to determine status per row
                              def check_status(row):
                                    mo_base = row['MO'].split('=')[0]
                                    if mo_base in expected:
                                          return "OK" if all(ev in row['Value'] for ev in expected[mo_base]) else "NOT OK"
                                    else:
                                          return "UNKNOWN"

                              ok_status_list = df.apply(check_status, axis=1).tolist()

                              # Get unique site ID
                              site_id = df['Node_ID'].unique()[0] if 'Node_ID' in df.columns else None

                              # Update checklist_df
                              checklist_df.at[idx, 'Site_ID'] = site_id
                              checklist_df.at[idx, 'Remark'] = 'OK' if any(status == 'OK' for status in ok_status_list) else 'NOT OK'
                              checklist_df.at[idx, 'Checkpoint'] = str(sheet_name)

                        else:
                              checklist_df.at[idx + 1, 'Remark'] = 'Missing'
                              checklist_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)

                  ####################################### getting folders for final output #########################################
            output_path = os.path.join(base_media_url, "OUTPUT")

            os.makedirs(output_path, exist_ok=True)

            output_filename = f"_{base_name}{timestamp}.xlsx"
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
      
      zip_filename = f"soft_at_5G_Summary_Ericsson/5gChecklist_OUTPUT_{timestamp}.zip"
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

