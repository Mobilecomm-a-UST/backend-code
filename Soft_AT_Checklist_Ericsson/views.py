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
def soft_at_checkpoint(request):
      # try:

###########################################
      all_files_df = pd.DataFrame()
      # St_cell_df = pd.DataFrame()
      # latitude_df = pd.DataFrame()
      # longitude_df = pd.DataFrame()
      # st_mme_df = pd.DataFrame()
      # Vswrsupervision_df = pd.DataFrame()
      # snmp_df = pd.DataFrame()
      # twamp_df = pd.DataFrame()
      # Pathmaxrtx_df = pd.DataFrame()
      # assocMaxRtx_df = pd.DataFrame()
      # heartbeatInterval_df = pd.DataFrame()
      # st_sync_df = pd.DataFrame()
      # sync_df = pd.DataFrame()
      # ret_user_df = pd.DataFrame()
      # st_ret_df = pd.DataFrame()
      # FeatureState_CXC4011958_df = pd.DataFrame()
      # FeatureState_CXC4011808_df = pd.DataFrame()
      # FeatureState_CXC4011803_df = pd.DataFrame()
      # FeatureState_CXC4011983_df = pd.DataFrame()
      # FeatureState_CXC4011378_df = pd.DataFrame()
      # stz_df = pd.DataFrame()
      # alarm_df = pd.DataFrame()
#################################################### 
      circle = request.POST.get("circle")
      files = request.FILES.getlist("files")
      base_name = None
      if not files:
            return Response(
                  {"status": "ERROR", "message": "No files uploaded"},
                  status=HTTP_400_BAD_REQUEST,
            )
############## DEFINEING THE PATH FOR TOOL MEDIA ######################
      base_media_url = os.path.join(MEDIA_ROOT, "soft_at_checkpoint_Ericsson")
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
      timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

      # Create logs_excel directory if it doesn't exist
      if not os.path.exists(log_excel_folder):
            os.makedirs(log_excel_folder, exist_ok=True)
      else:
            try:
                  shutil.rmtree(log_excel_folder, onerror=on_rm_error)
                  os.makedirs(log_excel_folder, exist_ok=True)
            except PermissionError as e:
                  print("Permission denied:- ", str(e))
########################################################################
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

            latitude_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\s\.\slatitude',
                  r'MO\s+Attribute\s+Value',
                  r'^\s*(EUtranCell(?:FDD|TDD)=\S+)\s+(latitude)\s+(\d+)\s*$',
                  r'^Total:\s\d+',
                  file_content
            )

            longitude_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\s\.\slongitude',
                  r'MO\s+Attribute\s+Value',
                  r'^\s*(EUtranCell(?:FDD|TDD)=\S+)\s+(longitude)\s+(\d+)\s*$',
                  r'^Total:\s\d+',
                  file_content
            )

            st_mme_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sst\scell',
                  r'(Proxy)\s+(Adm\sState)\s+(Op\.\sState)\s+(MO)',
                  r'\s*(\d+)\s+(\d+\s+\((?:UNLOCKED|LOCKED)\))\s+(\d+\s+\((?:ENABLED|DISABLED)\))\s+(.*)$',
                  r'^Total:\s\d+',
                  file_content
            )

            Vswrsupervision_df = explode_data_from_log(
                        r'[A-Z0-9_-]+>\sget\s\.\svswrsuper',                  # Start pattern (e.g., prompt + command)
                        r'MO\s+Attribute\s+Value',                            # Header pattern
                        r'^\s*(FieldReplaceableUnit=[^,]+,RfPort=\S+)\s+(vswrSupervisionActive|vswrSupervisionSensitivity)\s+(\S+)\s*$',  # Data line pattern
                        r'^Total:\s\d+',     
                  file_content
            )

            snmp_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\s\.\ssnmp',
                  r'MO\s+Attribute\s+Value',
                  r'^\s*(SysM=\S+.*?)\s+(snmp\w+)\s+(.*?)\s*$',
                  r'^Total:\s\d+',
                  file_content
            )

            twamp_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\s\.\stwamp',
                  r'MO\s+Attribute\s+Value',
                  r'^\s*(Router=\S+.*?)\s+(twampResponderId)\s+(.*?)\s*$',
                  r'^Total:\s\d+',
                  file_content
            )

            Pathmaxrtx_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\s\.\spathmaxrtx',
                  r'MO\s+Attribute\s+Value',
                  r'^\s*(SctpProfile=\S+)\s+(\S+)\s+(.*?)\s*$',
                  r'^Total:\s\d+',
                  file_content
            )

            assocMaxRtx_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\s\.\sassocMaxRtx',
                  r'MO\s+Attribute\s+Value',
                  r'^\s*(SctpProfile=\S+)\s+(\S+)\s+(.*?)\s*$',
                  r'^Total:\s\d+',
                  file_content
            )
            
            heartbeatInterval_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\sFm=1\sheartbeatInterval',
                  r'MO\s+Attribute\s+Value',
                  r'^\s*(Fm=\S+)\s+(heartbeatInterval)\s+(.*?)\s*$',
                  r'^Total:\s\d+',
                  file_content
            )

            st_sync_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sst\ssync',
                  r'(Proxy)\s+(Adm\sState)\s+(Op\.\sState)\s+(MO)',
                  r'^\s*(\d+)\s+(\d*)\s*\((ENABLED|DISABLED)\)\s+(.*)$',
                  r'^Total:\s\d+',
                  file_content
            )

            sync_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\s\.\ssync',
                  r'MO\s+Attribute\s+Value',
                  r'^\s*(\S.*?)\s{2,}(\S+)\s+(.*?)\s*$',
                  r'^Total:\s\d+',
                  file_content
            )

            ret_user_df = explode_data_from_log(
                  r'^[A-Z0-9_-]+>\sHget\sret\suser',
                  r'MO\s+userLabel',
                  r'^\s*(AntennaUnitGroup=\d+,[^,]+,RetSubUnit=\d+)\s+(.*?)\s*$',
                  r'^Total:\s\d+',
                  file_content
            )

            st_ret_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sst\sret',
                  r'(Proxy)\s+(Adm\sState)\s+(Op\.\sState)\s+(MO)',
                  r'^\s*(\d+)\s+(\d*\s*\(?(?:UNLOCKED|LOCKED|DISABLED|ENABLED)?\)?)\s+(\d+\s+\((?:DISABLED|ENABLED)\))\s+(.*)$',
                  r'^Total:\s+\d+\s+MOs',
                  file_content
)
            

            print("st ret- ",st_ret_df)

            FeatureState_CXC4011958_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\sLm=1,FeatureState=CXC4011958',
                  r'^\s*(\d+)\s+([A-Za-z0-9=,]+)\s*$',
                  r'^\s*([a-zA-Z0-9]+)\s+(.+?)\s*$',
                  r'^Total:\s\d+\sMOs',
                  file_content
            )
            print("FeatureState_CXC4011958_df.columns:- ",FeatureState_CXC4011958_df.columns)
            if not FeatureState_CXC4011958_df.empty:
                  expected_cols = FeatureState_CXC4011958_df.columns.tolist()
                  if len(expected_cols) >= 2:
                        FeatureState_CXC4011958_df.columns = ['MO', 'Attribute'] + expected_cols[2:]

            # FeatureState_CXC4011958_df.columns = ['MO', 'Attribute', *FeatureState_CXC4011958_df.columns.tolist()[2:]]
            

            FeatureState_CXC4011808_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\sLm=1,FeatureState=CXC4011808',
                  r'^\s*(\d+)\s+([A-Za-z0-9=,]+)\s*$',
                  r'^\s*([a-zA-Z0-9]+)\s+(.+?)\s*$',
                  r'^Total:\s\d+',
                  file_content
            )
            if not FeatureState_CXC4011808_df.empty:
                  expected_cols = FeatureState_CXC4011808_df.columns.tolist()
                  if len(expected_cols) >= 2:
                        FeatureState_CXC4011808_df.columns = ['MO', 'Attribute'] + expected_cols[2:]
#
            # FeatureState_CXC4011808_df.columns = ['MO', 'Attribute', *FeatureState_CXC4011808_df.columns.tolist()[2:]]


            FeatureState_CXC4011803_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\sLm=1,FeatureState=CXC4011803',
                  r'^(\d+)\s+([A-Za-z0-9=,]+)\s*',
                  r'^([a-zA-Z0-9]+)\s+(.+?)\s*$',
                  r'Total:\s\d+',
                  file_content
            )
            # FeatureState_CXC4011803_df.columns = ['MO', 'Attribute', *FeatureState_CXC4011803_df.columns.tolist()[2:]] if not FeatureState_CXC4011803_df.columns else pd.DataFrame(columns=['MO', 'Attribute'])
            if not FeatureState_CXC4011803_df.empty:
                  expected_cols = FeatureState_CXC4011803_df.columns.tolist()
                  if len(expected_cols) >= 2:
                        FeatureState_CXC4011803_df.columns = ['MO', 'Attribute'] + expected_cols[2:]



            FeatureState_CXC4011983_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\sLm=1,FeatureState=CXC4011983',
                  r'^\s*(\d+)\s+([A-Za-z0-9=,]+)\s*$',
                  r'^\s*([a-zA-Z0-9]+)\s+(.+?)\s*$',
                  r'^Total:\s',
                  file_content
            )
            if not FeatureState_CXC4011983_df.empty:
                  expected_cols = FeatureState_CXC4011983_df.columns.tolist()
                  if len(expected_cols) >= 2:
                        FeatureState_CXC4011983_df.columns = ['MO', 'Attribute'] + expected_cols[2:]

            # FeatureState_CXC4011983_df.columns = ['MO', 'Attribute', *FeatureState_CXC4011983_df.columns.tolist()[2:]]


            FeatureState_CXC4011378_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sget\sLm=1,FeatureState=CXC4011378',
                  r'^\s*(\d+)\s+([A-Za-z0-9=,]+)\s*$',
                  r'^\s*([a-zA-Z0-9]+)\s+(.+?)\s*$',
                  r'^Total:\s\d+',
                  file_content
            )
            if not FeatureState_CXC4011378_df.empty:
                  expected_cols = FeatureState_CXC4011378_df.columns.tolist()
                  if len(expected_cols) >= 2:
                        FeatureState_CXC4011378_df.columns = ['MO', 'Attribute'] + expected_cols[2:]

            # FeatureState_CXC4011378_df.columns = ['MO', 'Attribute', *FeatureState_CXC4011378_df.columns.tolist()[2:]]


            stz_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\s+stz',                                                                                     
                  r'Id\s+LTECell\s+S\s+TABREMDF\s+Alm\s+UEs\s+cId\s+tac\s+pci\s+rsi\s+eci\s+arfcnDL\s+arfcnUL\s+freqDL\s+freqUL\s+dlBW\s+ulBW\s+Band\s+cnfP\s+maxP\s+C-T/R\s+U-T/R\s+M-T\s+Ess\s+Fru',  # table_header_pattern
                  r'(\d+)\s+([^\s]+)\s+([A-Z\d]+)\s+([^\s]+)\s+(-|\d+|\d+,\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+/\d+)\s+(-?\d+/-?\d+)\s+(\d+)\s+(-|\d+)\s+(\d+)',
                  # r'(\d+)\s+([^\s]+)\s+(\d+)\s+([^\s]+)\s+(-|\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+/\d+)\s+(\d+/\d+)\s+(\d+)\s+(-|\d+)\s+(\d+)',  # data_row_pattern
                  r'^Total:\s+\d+\s+Cells\s+\(\d+\s+up\)',                                                               
                  file_content                                                                                                 
            )
            

            alarm_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\sst\salarmport',
                  r'(Proxy)\s+(Adm\sState)\s+(Op\.\sState)\s+(MO)',
                  r'^\s*(\d+)\s+(\d+\s+\((?:UNLOCKED|LOCKED)\))\s+(\d+\s+\((?:ENABLED|DISABLED)\))\s+(.*)$',
                  r'^Total:\s\d+',
                  file_content
            )
            print("st cell df:- ",st_cell_df)
            sheets = {
                  'St Cell': st_cell_df,
                  'get . latitude': latitude_df,
                  'get . longitude': longitude_df,
                  'St mme': st_mme_df,
                  'get . Vswrsupervision': Vswrsupervision_df,
                  'get . Snmp': snmp_df,
                  'get . Twamp': twamp_df,
                  'get . Pathmaxrtx': Pathmaxrtx_df,
                  'get . assocMaxRtx': assocMaxRtx_df,
                  'get Fm=1 heartbeatInterval': heartbeatInterval_df,
                  'St Sync': st_sync_df,
                  'get . Sync': sync_df,
                  'Hget Ret User': ret_user_df,
                  'st Ret': st_ret_df,
                  'FeatureState_CXC4011958': FeatureState_CXC4011958_df,
                  'FeatureState_CXC4011808': FeatureState_CXC4011808_df,
                  'FeatureState_CXC4011803': FeatureState_CXC4011803_df,
                  'FeatureState_CXC4011983': FeatureState_CXC4011983_df,
                  'FeatureState_CXC4011378': FeatureState_CXC4011378_df,
                  'Stz': stz_df,
                  'St alarmport': alarm_df,
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
            xls = pd.ExcelFile(file)
            template_path = os.path.join(template_file_path, "template.xlsx")
            template_df : pd.DataFrame = pd.ExcelFile(template_path,).parse()
            print(xls.sheet_names)
            for idx,sheet_name in enumerate(xls.sheet_names, start=1):
                  print(sheet_name)
                  required_columns_present = lambda df, columns: all(col in df.columns for col in columns)

                  if sheet_name == "St Cell":
                        df = xls.parse(sheet_name).copy()
                        if required_columns_present(df, ["Adm State", "Op. State", "Node_ID"]):
                              df['Adm State'] = df['Adm State'].astype(str).str.strip()
                              df['Op. State'] = df['Op. State'].astype(str).str.strip()
                              ok_status_list = df.apply(
                                    lambda x: "OK" if x['Adm State'] == "1 (UNLOCKED)" and x['Op. State'] == "1 (ENABLED)" else "NOT OK",
                                    axis=1
                              ).tolist()
                              template_df.at[idx,"Site_ID"] = df['Node_ID'].unique()[0]
                              template_df.at[idx,'Remark '] = 'OK' if all(status == 'OK' for status in ok_status_list) else 'NOT OK'
                              template_df.at[idx,'Checkpoint'] = str(sheet_name)
                        else:
                              # Sheet not found
                              # template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx + 1, 'Remark '] = 'Missing'
                              template_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)

                  elif sheet_name == "get . latitude":
                        df = xls.parse(sheet_name).copy()
                        if required_columns_present(df, ["Attribute", "Value", "Node_ID"]):
                              df["Attribute"] = df["Attribute"].astype(str).str.strip()
                              df["Value"] = df["Value"].astype(str).str.strip()
                              ok_status_list = df.apply(
                                    lambda x: "OK" if x['Attribute'] == "latitude" and x['Value'] != "0" else "NOT OK",
                                    axis=1
                              ).tolist()
                              template_df.at[idx,"Site_ID"] = df['Node_ID'].unique()[0]
                              template_df.at[idx,'Remark '] = 'OK' if all(status == 'OK' for status in ok_status_list) else 'NOT OK'
                              template_df.at[idx,'Checkpoint'] = str(sheet_name)
                        else:
                              # Sheet not found
                              # template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx + 1, 'Remark '] = 'Missing'
                              template_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)

                  elif sheet_name == "get . longitude":
                        df = xls.parse(sheet_name).copy()
                        if required_columns_present(df, ["Attribute", "Value", "Node_ID"]):
                              df["Attribute"] = df["Attribute"].astype(str).str.strip()
                              df["Value"] = df["Value"].astype(str).str.strip()
                              ok_status_list = df.apply(
                                    lambda x: "OK" if x['Attribute'] == "longitude" and x['Value'] != "0" else "NOT OK",
                                    axis=1
                              ).tolist()
                              template_df.at[idx,"Site_ID"] = df['Node_ID'].unique()[0]
                              template_df.at[idx,'Remark '] = 'OK' if all(status == 'OK' for status in ok_status_list) else 'NOT OK'
                              template_df.at[idx,'Checkpoint'] = str(sheet_name)
                        else:
                              # Sheet not found
                              # template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx + 1, 'Remark '] = 'Missing'
                              template_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)

                  elif sheet_name == "St mme":
                        df = xls.parse(sheet_name).copy()
                        if required_columns_present(df, ["Adm State", "Op. State", "Node_ID"]):
                              df["Adm State"] = df["Adm State"].astype(str).str.strip()
                              df["Op. State"] = df["Op. State"].astype(str).str.strip()
                              ok_status_list = df.apply(
                                    lambda x: "OK" if x['Adm State'] == "1 (UNLOCKED)" and x['Op. State'] == "1 (ENABLED)" else "NOT OK",
                                    axis=1
                              ).tolist()
                              template_df.at[idx,"Site_ID"] = df['Node_ID'].unique()[0]
                              template_df.at[idx,'Remark '] = 'OK' if all(status == 'OK' for status in ok_status_list) else 'NOT OK'
                              template_df.at[idx,'Checkpoint'] = str(sheet_name)
                        else:
                              # Sheet not found
                              # template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx + 1, 'Remark '] = 'Missing'
                              template_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)

                  elif sheet_name == "get . Vswrsupervision":
                        df = xls.parse(sheet_name).copy()
                        if required_columns_present(df, ["Attribute", "Value", "MO", "Node_ID"]):
                              df["Attribute"] = df["Attribute"].astype(str).str.strip()
                              df["Value"] = df["Value"].astype(str).str.strip().str.lower()
                              df["MO"] = df["MO"].astype(str)

                              # Extract RRU and RfPort
                              df['RRU'] = df['MO'].str.extract(r'(RRU-\d+)')
                              df['RfPort'] = df['MO'].str.extract(r'RfPort=([A-Z])')

                              # Normalize value types
                              df["Value"] = df.apply(
                                    lambda row: int(row["Value"]) if row["Attribute"] == "vswrSupervisionSensitivity" and row["Value"].isdigit() else row["Value"],
                                    axis=1
                              )

                              final_status = 'OK'
                              for rru, group in df.groupby('RRU'):
                                    # Check that non-R ports have vswrSupervisionActive = true
                                    active_check = group[
                                    (group['Attribute'] == 'vswrSupervisionActive') & (group['RfPort'] != 'R')
                                    ]['Value'].eq('true').all()

                                    # Check that R ports have vswrSupervisionActive = false
                                    r_check = group[
                                    (group['Attribute'] == 'vswrSupervisionActive') & (group['RfPort'] == 'R')
                                    ]['Value'].eq('false').all()

                                    # Check that all ports have vswrSupervisionSensitivity = 100
                                    sensitivity_check = group[
                                    group['Attribute'] == 'vswrSupervisionSensitivity'
                                    ]['Value'].eq(100).all()

                                    if not (active_check and r_check and sensitivity_check):
                                          final_status = 'NOT OK'
                                          break 

                              template_df.at[idx, "Site_ID"] = df['Node_ID'].unique()[0]
                              template_df.at[idx, 'Remark '] = final_status
                              template_df.at[idx, 'Checkpoint'] = str(sheet_name)
                        else:
                              template_df.at[idx + 1, 'Remark '] = 'Missing'
                              template_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)


                  elif sheet_name == "get . Snmp":
                        df = xls.parse(sheet_name).copy()
                        
                        if required_columns_present(df, ["Attribute", "Value", "Node_ID"]):
                              df["Attribute"] = df["Attribute"].astype(str).str.strip()
                              df["Value"] = df["Value"].astype(str).str.strip()
                              
                              expected_values = {
                                    "snmpId": "1",
                                    "snmpTargetV2CId": "ENMFM",
                                    "snmpSecurityLevel": "1 (NO_AUTH_NO_PRIV)",
                                    "snmpTargetV3Id": "1"
                              }
                              
                              filtered_df = df[df["Attribute"].isin(expected_values.keys())]
                              actual_values = dict(zip(filtered_df["Attribute"], filtered_df["Value"]))
                              
                              all_match = all(actual_values.get(attr) == expected for attr, expected in expected_values.items())
                              
                              template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx, 'Remark '] = "OK" if all_match else "NOT OK"
                              template_df.at[idx, 'Checkpoint'] = str(sheet_name)
                        else:
                              # Sheet not found or required columns missing
                              template_df.at[idx + 1, 'Remark '] = 'Missing'
                              template_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)

                  elif sheet_name == "get . Twamp":
                        df = xls.parse(sheet_name).copy()
                        
                        if required_columns_present(df, ["MO", "Attribute", "Value", "Node_ID"]):
                              df['MO'] = df['MO'].astype(str).str.strip()
                              df["Attribute"] = df["Attribute"].astype(str).str.strip()
                              df["Value"] = df["Value"].astype(str).str.strip()

                              expected = {
                                    "Router=LTEUP,TwampResponder=1": "1",
                                    "Router=LTEUP,TwampResponder=NR": "NR"
                              }

                              # Add status column using lambda
                              df["Status"] = df.apply(
                                    lambda x: "OK" if (
                                    x["Attribute"] == "twampResponderId" and 
                                    x["MO"] in expected and 
                                    x["Value"] == expected[x["MO"]]
                                    ) else (
                                    "SKIP" if x["MO"] not in expected else "NOT OK"
                                    ), axis=1
                              )

                              # Print only MOs present in expected
                              for mo in expected:
                                    rows = df[df["MO"] == mo]
                                    if not rows.empty:
                                          for _, row in rows.iterrows():
                                                print(f"{mo}: {row['Status']}")

                              # Collect overall status for final template
                              ok_status_list = df[df["MO"].isin(expected.keys())]["Status"].tolist()
                              final_status = "OK" if all(s == "OK" for s in ok_status_list) else "NOT OK"

                              template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx, 'Remark '] = final_status
                              template_df.at[idx, 'Checkpoint'] = str(sheet_name)
                        else:
                              # Sheet not found
                              # template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx + 1, 'Remark '] = 'Missing'
                              template_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)

                  elif sheet_name == "get . Pathmaxrtx":
                        df = xls.parse(sheet_name).copy()
                        if required_columns_present(df, ["Attribute", "Value", "Node_ID"]):
                              df["Attribute"] = df["Attribute"].astype(str).str.strip()
                              df["Value"] = df["Value"].astype(str).str.strip()
                              ok_status_list = df.apply(
                              lambda x: "OK" if 
                              (x['Attribute'] == "pathMaxRtx" and x['Value'] == "4") or 
                              (x['Attribute'] == "primaryPathMaxRtx" and x['Value'] == "0")
                              else "NOT OK",
                              axis=1
                              ).tolist()
                              template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx, 'Remark '] = 'OK' if all(status == 'OK' for status in ok_status_list)  else 'NOT OK'
                              template_df.at[idx, 'Checkpoint'] = str(sheet_name)
                        else:
                              # Sheet not found
                              # template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx + 1, 'Remark '] = 'Missing'
                              template_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)
                                          
                  elif sheet_name == "get . assocMaxRtx":
                        df = xls.parse(sheet_name).copy()
                        if required_columns_present(df, ["Attribute", "Value", "Node_ID"]):
                              df["Attribute"] = df["Attribute"].astype(str).str.strip()
                              df["Value"] = df["Value"].astype(str).str.strip()
                              ok_status_list = df.apply(
                              lambda x: "OK" if x['Attribute'] == "assocMaxRtx" and x['Value'] == "8" else "NOT OK",
                              axis=1
                              ).tolist()
                              # print(ok_status_list)
                              template_df.at[idx,'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx,'Remark '] = 'OK' if all(status == 'OK' for status in ok_status_list if status)  else 'NOT OK'
                              template_df.at[idx,'Checkpoint'] = str(sheet_name)
                        else:
                              # Sheet not found
                              # template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx + 1, 'Remark '] = 'Missing'
                              template_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)
                        
                  elif sheet_name == "get Fm=1 heartbeatInterval":
                        df = xls.parse(sheet_name).copy()
                        if required_columns_present(df, ["Attribute", "Value", "Node_ID"]):
                              df["Attribute"] = df["Attribute"].astype(str).str.strip()
                              df["Value"] = df["Value"].astype(str).str.strip()
                              ok_status_list = df.apply(
                              lambda x: "OK" if x['Attribute'] == "heartbeatInterval" and x['Value'] == "100" else "NOT OK",
                              axis=1
                              ).tolist()
                              # print(ok_status_list)
                              template_df.at[idx,'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx,'Remark '] = 'OK' if any(status == 'OK' for status in ok_status_list) else 'NOT OK'
                              template_df.at[idx,'Checkpoint'] = str(sheet_name)
                        else:
                              # Sheet not found
                              # template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx + 1, 'Remark '] = 'Missing'
                              template_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)


                  elif sheet_name == "St Sync":
                        df = xls.parse(sheet_name).copy()
                        if required_columns_present(df, ["Op. State", "MO", "Node_ID"]):
                              df["Op. State"] = df["Op. State"].astype(str).str.strip()
                              df["MO"] = df["MO"].astype(str).str.strip()
                              expected_mo ={ 
                              "Equipment=1,FieldReplaceableUnit=DU-1,SyncPort=1",
                              "Transport=1,Synchronization=1,TimeSyncIO=1"
                              }
                              ok_status_list = df.apply(
                              lambda x: "OK" if (x['Op. State'] == "ENABLED" and any(mo in x['MO'] for mo in expected_mo)) else "NOT OK",
                              axis=1
                              ).tolist()
                              # print(ok_status_list)
                              template_df.at[idx,'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx,'Remark '] = 'OK' if any(status == 'OK' for status in ok_status_list) else 'NOT OK'
                              template_df.at[idx,'Checkpoint'] = str(sheet_name)
                        else:
                              # Sheet not found
                              # template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx + 1, 'Remark '] = 'Missing'
                              template_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)
                        
                  
                  elif sheet_name == "get . Sync":
                        df = xls.parse(sheet_name).copy()
                        if required_columns_present(df, ["Attribute", "Value", "Node_ID"]):
                              df["Attribute"] = df["Attribute"].astype(str).str.strip()
                              df["Value"] = df["Value"].astype(str).str.strip()
                              expected_pairs = {
                              "timeAndPhaseSynchAlignment": "true",
                              "timeSyncIOStatus": "0 (NO_FAULT)"
                              }
                              df["Status"] = df.apply(
                              lambda x: "OK" if x["Attribute"] in expected_pairs and x["Value"] == expected_pairs[x["Attribute"]] else "NOT OK",
                              axis=1
                              )
                              filtered_status = df[df["Attribute"].isin(expected_pairs.keys())]["Status"].tolist()
                              final_status = "OK" if all(s == "OK" for s in filtered_status) and len(filtered_status) == len(expected_pairs) else "NOT OK"    
                              template_df.at[idx,'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx, 'Remark '] = final_status
                              template_df.at[idx, 'Checkpoint'] = str(sheet_name)
                        else:
                              # Sheet not found
                              # template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx + 1, 'Remark '] = 'Missing'
                              template_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)
                              
                  elif sheet_name == "Hget Ret User":
                        df = xls.parse(sheet_name).copy()
                        if required_columns_present(df, ["MO", "userLabel", "Node_ID"]):
                              df["MO"] = df["MO"].astype(str).str.strip()
                              df["userLabel"] = df["userLabel"].astype(str).str.strip()
                              df["AntennaUnitGroup"] = df["MO"].str.extract(r"AntennaUnitGroup=(\d+)")
                              group_checks = df.groupby("AntennaUnitGroup").apply(
                              lambda g: any(g["userLabel"] == "FREE PORT") and
                                          any(
                                          label.endswith(chr(64 + int(g.name)))
                                          for label in g["userLabel"]
                                          if label != "FREE PORT"
                                          )
                              )
                              template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0] if not df.empty else ""
                              template_df.at[idx, 'Remark '] = 'OK' if all(status =='OK' for status in group_checks) else 'NOT OK'
                              template_df.at[idx, 'Checkpoint'] = str(sheet_name)
                        else:
                              # Sheet not found
                              # template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx + 1, 'Remark '] = 'Missing'
                              template_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)

                  elif sheet_name == "St Ret":
                        df = xls.parse(sheet_name).copy()
                        if required_columns_present(df, ["Adm State", "Op. State", "Node_ID"]):
                              # Handle case when DataFrame is empty
                              if df.empty:
                                    template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                                    template_df.at[idx, 'Remark '] = 'OK'
                                    template_df.at[idx, 'Checkpoint'] = str(sheet_name)
                              else:
                                    df["Adm State"] = df["Adm State"].ffill().astype(str).str.strip()
                                    df["Op. State"] = df["Op. State"].ffill().astype(str).str.strip()
                                    ok_status_list = df.apply(
                                    lambda x: "OK" if x['Adm State'] == "1 (UNLOCKED)" and x['Op. State'] == "1 (ENABLED)" else "NOT OK",
                                    axis=1
                                    ).tolist()
                                    print(ok_status_list)
                                    template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                                    template_df.at[idx, 'Remark '] = 'OK' if all(status == 'OK' for status in ok_status_list) else 'NOT OK'
                                    template_df.at[idx, 'Checkpoint'] = str(sheet_name)
                        else:
                              template_df.at[idx + 1, 'Remark '] = 'Missing'
                              template_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)

                  elif sheet_name == "FeatureState_CXC4011958":
                        df = xls.parse(sheet_name).copy()
                        # print(df)
                        if required_columns_present(df, ["MO", "Attribute","Node_ID"]):
                              df.columns = df.columns.astype(str).str.strip()
                              # print(df.columns)
                              df["MO"] = df["MO"].astype(str).str.strip()
                              df["Attribute"] = df["Attribute"].astype(str).str.strip()
                              expected = {
                              "featureState": "1 (ACTIVATED)",
                              "licenseState": "1 (ENABLED)",
                              "serviceState": "1 (OPERABLE)",
                              }
                              ok_status_list = df.apply(
                              lambda x: "OK" if x['MO'] in expected and x['Attribute'] == expected[x['MO']] else "NOT OK" if x['MO'] in expected else None,
                              axis=1
                              ).dropna().tolist()
                              print(ok_status_list)
                              template_df.at[idx,'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx,'Remark '] = 'OK' if any(status == 'OK' for status in ok_status_list) else 'NOT OK'
                              template_df.at[idx,'Checkpoint'] = str(sheet_name)
                        else:
                              # Sheet not found
                              # template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx + 1, 'Remark '] = 'Missing'
                              template_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)
                        
                  elif sheet_name == "FeatureState_CXC4011808":
                        df = xls.parse(sheet_name).copy()
                        if required_columns_present(df, [ "MO","Attribute", "Node_ID"]):
                              df.columns = df.columns.astype(str).str.strip()
                              df["MO"] = df["MO"].astype(str).str.strip()
                              df["Attribute"] = df["Attribute"].astype(str).str.strip()
                              expected = {
                              "featureState": "1 (ACTIVATED)",
                              "licenseState": "1 (ENABLED)",
                              "serviceState": "1 (OPERABLE)",
                              }
                              ok_status_list = df.apply(
                              lambda x: "OK" if x['MO'] in expected and x['Attribute'] == expected[x['MO']] else "NOT OK" if x['MO'] in expected else None,
                              axis=1
                              ).dropna().tolist()

                              print(ok_status_list)
                              template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0] 
                              template_df.at[idx, 'Remark '] = 'OK' if all(status == 'OK' for status in ok_status_list) else 'NOT OK'
                              template_df.at[idx, 'Checkpoint'] = str(sheet_name)
                        else:
                              # Sheet not found
                              # template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx + 1, 'Remark '] = 'Missing'
                              template_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)

                  elif sheet_name in ["FeatureState_CXC4011803", "FeatureState_CXC4011803"]:
                        df = xls.parse(sheet_name).copy()
                        if required_columns_present(df, ["MO","Attribute", "Node_ID"]):
                              df.columns = df.columns.astype(str).str.strip()
                              print(df.columns.tolist())
                              required_cols = {"MO", "Attribute"}
                              has_required_cols = required_cols.issubset(df.columns)
                              if not df.empty and has_required_cols:
                                    df["MO"] = df["MO"].astype(str).str.strip()
                                    df["Attribute"] = df["Attribute"].astype(str).str.strip()
                                    expected = {
                                          "featureState": "1 (ACTIVATED)",
                                          "licenseState": "1 (ENABLED)",
                                          "serviceState": "1 (OPERABLE)",
                                    }
                                    ok_status_list = df.apply(
                                          lambda x: "OK" if x['MO'] in expected and x['Attribute'] == expected[x['MO']] else "NOT OK" if x['MO'] in expected else None,
                                          axis=1
                                    ).dropna().tolist()
                                    print(f"OK Status List: {ok_status_list}")
                                    template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0] 
                                    template_df.at[idx, 'Remark '] = 'OK' if all(status == 'OK' for status in ok_status_list) else 'NOT OK'
                                    template_df.at[idx, 'Checkpoint'] = str(sheet_name)
                              else:
                                    # template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                                    template_df.at[idx, 'Remark '] = 'OK'
                                    template_df.at[idx, 'Checkpoint'] = sheet_name
                        else:
                              # Sheet not found
                              # template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx + 1, 'Remark '] = 'Missing'
                              template_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)



                  elif sheet_name == "FeatureState_CXC4011983":
                        df = xls.parse(sheet_name).copy()
                        if required_columns_present(df, ["MO", "Attribute", "Node_ID"]):
                              df.columns = df.columns.astype(str).str.strip()
                              df["MO"] = df["MO"].astype(str).str.strip()
                              df["Attribute"] = df["Attribute"].astype(str).str.strip()
                              expected = {
                              "featureState": "1 (ACTIVATED)",
                              "licenseState": "1 (ENABLED)",
                              "serviceState": "1 (OPERABLE)",
                              }
                              ok_status_list = df.apply(
                              lambda x: "OK" if x['MO'] in expected and x['Attribute'] == expected[x['MO']] else "NOT OK" if x['MO'] in expected else None,
                              axis=1
                              ).dropna().tolist()
                              print(ok_status_list)
                              template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0] 
                              template_df.at[idx, 'Remark '] = 'OK' if all(status == 'OK' for status in ok_status_list) else 'NOT OK'
                              template_df.at[idx, 'Checkpoint'] = str(sheet_name)
                        else:
                              # Sheet not found
                              # template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx + 1, 'Remark '] = 'Missing'
                              template_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)
                        

                  elif sheet_name == "FeatureState_CXC4011378":
                        df = xls.parse(sheet_name).copy()
                        if required_columns_present(df, ["MO","Attribute", "Node_ID"]):
                              df.columns = df.columns.astype(str).str.strip()
                              df["MO"] = df["MO"].astype(str).str.strip()
                              df["Attribute"] = df["Attribute"].astype(str).str.strip()
                              expected = {
                              "featureState": "1 (ACTIVATED)",
                              "licenseState": "1 (ENABLED)",
                              "serviceState": "1 (OPERABLE)",
                              }
                              ok_status_list = df.apply(
                              lambda x: "OK" if x['MO'] in expected and x['Attribute'] == expected[x['MO']] else "NOT OK" if x['MO'] in expected else None,
                              axis=1
                              ).dropna().tolist()
                              print(ok_status_list)
                              template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0] 
                              template_df.at[idx, 'Remark '] = 'OK' if all(status == 'OK' for status in ok_status_list) else 'NOT OK'
                              template_df.at[idx, 'Checkpoint'] = str(sheet_name)
                        else:
                              # Sheet not found
                              # template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx + 1, 'Remark '] = 'Missing'
                              template_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)


                  elif sheet_name == "Stz":
                        df = xls.parse(sheet_name).copy()

                        if required_columns_present(df, ["tac", "arfcnDL", "Node_ID"]):
                              # Clean up fields
                              df["tac"] = df["tac"].astype(str).str.strip()
                              df["arfcnDL"] = df["arfcnDL"].astype(str).str.strip()

                              site_id = df["Node_ID"].unique()[0] if not df["Node_ID"].empty else "NA"

                              # TAC Check
                              tac_status = "OK" if df["tac"].nunique() == 1 else "NOT OK"
                              template_df.loc[idx, "Site_ID"] = site_id
                              template_df.loc[idx, "Remark "] = tac_status
                              template_df.loc[idx, "Checkpoint"] = f"{sheet_name}_tac"

                              # ARFCNDL Check
                              if "LTECell" in df.columns:
                                    df["Tech"] = df["LTECell"].str.extract(r"(F\d+|T\d+)", expand=False)

                                    # Group by Tech and check unique arfcnDL
                                    ok_status_dict = df.groupby("Tech").apply(
                                    lambda x: "OK" if x["arfcnDL"].nunique() == 1 else "NOT OK"
                                    ).to_dict()

                                    arfcn_status = "OK" if all(status == "OK" for status in ok_status_dict.values()) else "NOT OK"

                                    template_df.loc[idx + 1, "Site_ID"] = site_id
                                    template_df.loc[idx + 1, "Remark "] = arfcn_status
                                    template_df.loc[idx + 1, "Checkpoint"] = f"{sheet_name}_arfcnDL"              
                        else:
                              # Required columns are missing
                              # template_df.loc[idx, "Site_ID"] = "NA"
                              template_df.loc[idx, "Remark "] = 'Missing'
                              template_df.loc[idx, "Checkpoint"] = f"{sheet_name}_tac"
                              # template_df.loc[idx + 1, "Site_ID"] = site_id
                              template_df.loc[idx + 1, "Remark "] = 'Missing'
                              template_df.loc[idx + 1, "Checkpoint"] = f"{sheet_name}_arfcnDL"
                  
                  elif sheet_name == "St alarmport":
                        df = xls.parse(sheet_name).copy()
                        if required_columns_present(df, ["Adm State", "Op. State", "Node_ID"]):
                              df["Adm State"] = df["Adm State"].astype(str).str.strip()
                              df["Op. State"] = df["Op. State"].astype(str).str.strip()
                              ok_status_list = df.apply(
                                    lambda x: "OK" if x['Adm State'] == "1 (UNLOCKED)" and x['Op. State'] == "1 (ENABLED)" else "NOT OK",
                                    axis=1
                              ).tolist()
                              # Assign result to template
                              template_df.at[idx + 1, 'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx + 1, 'Remark '] = 'OK' if all(status == 'OK' for status in ok_status_list) else 'NOT OK'
                              template_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)
                        else:
                              # Sheet not found
                              # template_df.at[idx, 'Site_ID'] = df['Node_ID'].unique()[0]
                              template_df.at[idx + 1, 'Remark '] = 'Missing'
                              template_df.at[idx + 1, 'Checkpoint'] = str(sheet_name)
                  print(template_df,"template_df")

            ####################################### getting folders for final output #########################################
            output_path = os.path.join(base_media_url, "OUTPUT")

            os.makedirs(output_path, exist_ok=True)

            output_filename = f"{base_name}_OUTPUT_{timestamp}.xlsx"
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


      timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
      zip_filename = os.path.join(base_media_url, f"CHECKLIST_OUTPUT_{timestamp}.zip")
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
      #       print("error:- ", str(e))
      #       return Response(
      #             {"status": "ERROR", "message": str(e)}, status=HTTP_400_BAD_REQUEST
      #       )

