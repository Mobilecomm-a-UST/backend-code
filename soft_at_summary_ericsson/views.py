from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

import os
import re
import stat
import shutil
import zipfile
import pandas as pd
from datetime import datetime
import datetime
import xlsxwriter

from mcom_website.settings import MEDIA_ROOT ,MEDIA_URL


# ============================= Constants =============================

SPLIT_PATTEREN = r"Checking ip contact...OK"

# =================== File Processing Utils ===================

def read_and_write_func(file_path):
      with open(file_path, "r") as file:
            file_content = file.readlines()

            # FIX: join list into string before applying regex
            joined_content = "".join(file_content)
            nodes = re.split(rf"{SPLIT_PATTEREN}", joined_content)

            # split each block into lines
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
      

def delete_existing_files(folder_path):
      if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                  file_path = os.path.join(folder_path, file)
                  try:
                        if os.path.isfile(file_path):
                              os.unlink(file_path)
                  except Exception as e:
                        print(f"Error deleting {file_path}: {e}")


def explode_data_from_log(command, start_pattern, row_pattern, end_pattern, file_content):
      command_found = False
      header_found = False
      header_values = []
      data_rows = []
      node_id = None
      # Node = None
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
            df['IP_Address'] = ip_addr
            return df
      else:
            if not header_found:
                  print(f"[ERROR] Command found but header pattern did not match.")
            print("[WARN] No matching data rows or headers found.")
            return pd.DataFrame()

############################### Excel Formatting Function ##########################################################

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
############################ Main View##############################################################
@api_view(["POST", "GET"])
def extract_data_from_log(request):
      # try:
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

######################################################################################################################
            for file_path in saved_files:
                  base_name = os.path.basename(file_path)
            nodes = read_and_write_func(file_path)
            print(f"{file_path}:- ", len(nodes))

            ############ if we have two nodes#############################
            node_data = {}
            for node_index, node in enumerate(nodes):
                  node_key = f"node_{node_index+1}"
                  print(f"Processing {node_key}...")
                  node_data[node_key] = {}

                  st_cell_df = explode_data_from_log(
                        r'[A-Z0-9_-]+>\sst\scell',
                        r'(Proxy)\s+(Adm\sState)\s+(Op\.\sState)\s+(MO)',
                        r'\s*(\d+)\s+(\d+\s+\((?:UNLOCKED|LOCKED)\))\s+(\d+\s+\((?:ENABLED|DISABLED)\))\s+(.*)$',
                        r'^Total:\s\d+',
                        node
                  )
                  print(st_cell_df)

                  get_0 = explode_data_from_log(
                        r'[A-Z0-9_-]+>\sget\s0',
                        r'^(\d+)\s+(ManagedElement=[A-Z0-9_-]+)',
                        r'^(?P<key>[a-zA-Z0-9_]+)\s+(?P<value>.*?)$',
                        r'^Total:\s\d+',
                        node
                  )
                  print(get_0)

                  st_ret = explode_data_from_log(
                        r'[A-Z0-9_-]+>\sst\sret',
                        r'(Proxy)\s+(Adm\sState)\s+(Op\.\sState)\s+(MO)', 
                        r'^\s*(\d+)\s+(\d*\s*\(?(?:UNLOCKED|LOCKED|DISABLED|ENABLED)?\)?)\s+(\d+\s+\((?:DISABLED|ENABLED)\))\s+(.*)$', 
                        r'^Total:\s+\d+\s+MOs', 
                        node
                  )
                  print(st_ret)

                  get_sectorc = explode_data_from_log(
                        r'[A-Z0-9_-]+>\sget\s.\ssectorc',
                        r'MO\s+Attribute\s+Value',
                        r'^\s*(\S+)\s+(\S+)\s+(.*)$'  ,
                        r'^Total:\s\d+',
                        node              
                  )
                  print(get_sectorc)

                  get_enroll = explode_data_from_log(
                        r'[A-Z0-9_-]+>\sget\s.\senroll',
                        r'^\s*Enroll\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)$',
                        r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)$',
                        r'^Total:\s\d+',
                        node
                  )
                  print(get_enroll)

                  get_bsc = explode_data_from_log(
                        r'[A-Z0-9_-]+>\sget\s.\sbsc',
                        r'^\s*BSC\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)$',
                        r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)$',
                        r'^Total:\s\d+',
                        node
                  )
                  print(get_bsc)

                  get_tac = explode_data_from_log(
                        r'[A-Z0-9_-]+>\sget\s.\stac',
                        r'^\s*TAC\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)$',
                        r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)$',
                        r'^Total:\s\d+',
                        node
                  )
                  print(get_tac)

                  hget_field_prod = explode_data_from_log(
                        r'[A-Z0-9_-]+>\shget\sfield\sprod',
                        r'^\s*Field\s+Prod\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)$',
                        r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)$',
                        r'^Total:\s\d+',
                        node
                  )
                  print(hget_field_prod)

                  st_rru = explode_data_from_log(
                        r'[A-Z0-9_-]+>\sst\srru',
                        r'^\s*RRU\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)$',
                        r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)$',
                        r'^Total:\s\d+',
                        node
                  )
                  print(st_rru)

                  get_maxtx = explode_data_from_log(
                        r'[A-Z0-9_-]+>\sget\s.\smaxtx',
                        r'^\s*MaxTx\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)$',
                        r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)$',
                        r'^Total:\s\d+',
                        node
                  )
                  print(get_maxtx)

                  get_nooftx = explode_data_from_log(
                        r'[A-Z0-9_-]+>\sget\s.\snooftx',
                        r'^\s*NoOfTx\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)$',
                        r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)$',
                        r'^Total:\s\d+',
                        node
                  )
                  print(get_nooftx)

                  invxgr = explode_data_from_log(
                        r'[A-Z0-9_-]+>\sinvxgr',
                        r'^\s*InvXGR\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)$',
                        r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)$',
                        r'^Total:\s\d+',
                        node
                  )
                  print(invxgr)

                  st_sync = explode_data_from_log(
                        r'[A-Z0-9_-]+>\sst\ssync',
                        r'^\s*Sync\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)$',
                        r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)$',
                        r'^Total:\s\d+',
                        node
                  )
                  print(st_sync)

                  st_trx = explode_data_from_log(
                        r'[A-Z0-9_-]+>\sst\strx',
                        r'^\s*TRX\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)$',
                        r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)$',
                        r'^Total:\s\d+',
                        node
                  )
                  print(st_trx)

                  get_gsmsec = explode_data_from_log(
                        r'[A-Z0-9_-]+>\sget\s.\sgsmsec',
                        r'^\s*GSMSEC\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)$',
                        r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)$',
                        r'^Total:\s\d+',
                        node
                  )
                  print(get_gsmsec)

                  get_fing = explode_data_from_log(
                        r'[A-Z0-9_-]+>\sget\s.\sfing',
                        r'^\s*Fing\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)$',
                        r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)$',
                        r'^Total:\s\d+',
                        node
                  )
                  print(get_fing)

                  sheets ={

                        'st_cell': st_cell_df,
                        'get_0': get_0,
                        'st_ret': st_ret,
                        'get_sectorc': get_sectorc,
                        'get_enroll': get_enroll,
                        'get_bsc': get_bsc,
                        'get_tac': get_tac,
                        'hget_field_prod': hget_field_prod,
                        'st_rru': st_rru,
                        'get_maxtx': get_maxtx,
                        'get_nooftx': get_nooftx,
                        'invxgr': invxgr,
                        'st_sync': st_sync,
                        'st_trx': st_trx,
                        'get_gsmsec': get_gsmsec,
                        'get_fing': get_fing,

                  }
                  df_list = sheets.values()
                  # print("df_list:- ",[df_list])
                  all_files_df = pd.concat([all_files_df,*df_list], axis=0,ignore_index=True)
                  # print("all_files_df:- ",all_files_df)
                  
                  node_name = os.path.splitext(os.path.basename(file_path))[0]
                  excel_filename = os.path.join(log_excel_folder, f"{node_name}_{timestamp}.xlsx")
                  with pd.ExcelWriter(excel_filename, engine="xlsxwriter") as writer:
                        for sheet_name, df in sheets.items():
                              df.to_excel(writer, sheet_name=sheet_name, index=False)
                              format_excel_sheet(writer, sheet_name, df)
                  print(f"Excel file saved: {excel_filename}")
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

            # for file in excel_files_paths:
            #       base_name = os.path.basename(file).split('_')[0]
            #       xls = pd.ExcelFile(file)
            #       template_path = os.path.join(template_file_path, "template.xlsx")
            #       template_df : pd.DataFrame = pd.ExcelFile(template_path,).parse()
            #       print(xls.sheet_names)
            #       for idx,sheet_name in enumerate(xls.sheet_names, start=1):
            #             print(sheet_name)
            #             required_columns_present = lambda df, columns: all(col in df.columns for col in columns)

            #             if sheet_name == "st cell":
            #                   df = xls.parse(sheet_name)
            #                   circle = df["MO"].str.extract(r"EUtranCellFDD=([A-Z]{2})_")
            #                   layer = df["MO"].str.extract(r"EUtranCell(?:FDD|TDD)=\w+([FT]\d)")[
            #                         0
            #                   ]
            #                   if not circle.empty:
            #                         circle_value = next((x.strip() for x in circle[0].dropna()), "NA")
            #                         template_df.loc[0, 'Circle'] = circle_value

            #                         layer_value = '_'.join(layer.dropna().unique()) if not layer.dropna().empty else "NA"
            #                         # circle_value = circle.dropna().iloc[0, 0].strip()
            #                         # template_df.loc[0, "Circle"] = circle_value

            #                         # layer_value = "_".join(layer.dropna().unique())
            #                         layer_mapping = {
            #                         "F1": "L2100",
            #                         "F3": "L1800",
            #                         "F8": "L900",
            #                         "T1": "L2300",
            #                         "T2": "L2300",
            #                         "F5": "L850",
            #                         }
            #                         # layer_value = [layer_mapping.get(l, l) for l in layer_value.split('_')]
            #                         # layer_value = '_'.join(set(layer_value))
            #                         l_layers = [
            #                         layer_mapping.get(l, l) for l in layer_value.split("_")
            #                         ]
            #                         l_layers = list(set(l_layers))
            #                         template_df.loc[0, "Layers(Other Tech Info)"] = "_".join(
            #                         l_layers
            #                         )
            #                         # print("Layer Value:", l_layers)
                              
            #                   site_ids = (
            #                         df["MO"].str.extract(r"EUtranCellFDD=([\w_]+)")[0].dropna()
            #                   )
            #                   for site_value in site_ids:
            #                         parts = site_value.split("_")
            #                         if len(parts) >= 5:
            #                               site = parts[4]
            #                         if site.startswith("X"):
            #                         # or site.startswith("X"):
            #                               site = site[1:]
            #                         if site[-1].isalpha():
            #                               site = site[:-1]
            #                         template_df.loc[0, "2G Site ID"] = site
            #                         # print("2G SiteID:",site)

            #                   ant = df["MO"].str.extract(
            #                         r"EUtranCell(?:FDD|TDD)=[^\s,=]*([A-Z]_[A-Z])\b"
            #                   ).dropna()
            #                   ant = [val for val in ant[0].unique() if val.split("_")[0] == val.split("_")[1]]

            #                   total_antennas = len(ant)
            #                   print("Total unique antenna letters:", total_antennas)
            #                   template_df.loc[0, "Antenna"] = (total_antennas)
            #                   print("Antenna:", template_df.loc[0, "Antenna"])
            #                   cell_config = df["MO"].str.extract(
            #                         r"EUtranCell(?:FDD|TDD)=\w+([FT]\d)"
            #                   )[0]
            #                   cell_mapping = {
            #                         "F1": "L21",
            #                         "F3": "L18",
            #                         "F8": "L9",
            #                         "T1": "L23",
            #                         "T2": "L23",
            #                         "F5": "L85",
            #                   }
            #                   source_counts = cell_config.dropna().value_counts()
            #                   band_counts_df = pd.DataFrame(
            #                         {
            #                         "band": cell_config.dropna().map(cell_mapping),
            #                         "count": cell_config.dropna().map(source_counts),
            #                         }
            #                   )
            #                   final_band_counts = (
            #                         band_counts_df.groupby("band")["count"].max().sort_index()
            #                   )

            #                   formatted_config = "+".join(
            #                         f"{band}({count})" for band, count in final_band_counts.items()
            #                   )

            #                   # print("Formatted LTE Config:", formatted_config)
            #                   combined_config = formatted_config  # default to formatted_config


            #             if "st trx" in xls.sheet_names:
            #                   trx_df = xls.parse("st trx")
            #                   trx_data = trx_df["MO"].dropna()
            #                   trx_data = trx_data[trx_data.str.contains("GsmSector=")]

            #                   if not trx_data.empty:
            #                         # TRX exists → perform replacement
            #                         combined_config = formatted_config.replace("L18", "GL18").replace("L9", "GL9")

            #             template_df.loc[0, "Cells Configuration"] = combined_config

                        
            #             if "st trx" in xls.sheet_names:
            #                   df = xls.parse("st trx")

            #                   # Check both TRX formats
            #                   mask_trx_numeric = df["MO"].str.contains(r"Trx=\d+", na=False)
            #                   mask_trx_alphanumeric = df["MO"].str.contains(r"Trx=G\d+", na=False)

            #                   if mask_trx_alphanumeric.any():
            #                         # DL circle format (e.g., Trx=G1800-1)
            #                         l_layers_replaced = []
            #                         for layer in l_layers:
            #                               if layer == "L1800":
            #                                     l_layers_replaced.append("GL1800")
            #                               elif layer == "L900":
            #                                     l_layers_replaced.append("GL900")
            #                               else:
            #                                     l_layers_replaced.append(layer)
            #                   elif mask_trx_numeric.any():
            #                         # Non-DL format (e.g., Trx=0, Trx=4)
            #                         l_layers_replaced = []
            #                         for layer in l_layers:
            #                               if layer == "L1800":
            #                                     l_layers_replaced.append("GL1800")
            #                               elif layer == "L900":
            #                                     l_layers_replaced.append("GL900")
            #                               else:
            #                                     l_layers_replaced.append(layer)
            #                   else:
            #                         # No TRX info found
            #                         l_layers_replaced = l_layers if l_layers else []

            #                   # Final output to template
            #                   combined_layers = "_".join(sorted(set(l_layers_replaced))) if l_layers_replaced else "NA"
            #                   template_df.loc[0, "Layers(Other Tech Info)"] = combined_layers
            #                   print("Layers(Other Tech Info):", combined_layers)


            #             MO_names = []

            #             if "get 0" in xls.sheet_names:
            #                   df_0 = xls.parse("get 0", header=None)
            #                   # MO_name_0 = "/".join(
            #                   #     cell.split("=")[-1]
            #                   #     for cell in df_0.iloc[0]
            #                   #     if isinstance(cell, str) and "ManagedElement=" in cell
            #                   # )
            #                   # MO_names.append(MO_name_0)
            #                   MO_name_0 = df_0[df_0.iloc[:, 1] == "managedElementId"].iloc[0, 2]
            #                   print("MO Name 0:", MO_name_0)
            #                   template_df.loc[0, "MO Name"] = MO_name_0

                              
            #                   template_df.loc[0, "SW Version"] = df_0[
            #                         df_0.iloc[:, 1] == "swVersion"
            #                   ].iloc[0, 2]

            #                   physical_site = df_0[df_0.iloc[:, 1] == "userLabel"].iloc[0, 2]

            #                   #     # Check if physical_site contains any of the DL circles
            #                   #     if any(dl in physical_site for dl in ["DL"]):
            #                   template_df.loc[0, "Physical Site Id"] = physical_site
            #                   # print("Physical Site Id:", template_df.loc[0, 'Physical Site Id'])

            #             #     else:
            #             #         # Add a new row at the end for other circles
            #             #         new_row_index = len(template_df)
            #             #         template_df.loc[new_row_index, 'Physical Site Id'] = physical_site

            #             if "get . Gsmsec" in xls.sheet_names:

            #                   if template_df.loc[0, "Circle"] == "DL":
            #                         df_gsmsec = xls.parse("get . Gsmsec")
            #                         sector_names = df_gsmsec[
            #                         df_gsmsec["Attribute"] == "gsmSectorName"
            #                         ]["Value"]
            #                         prefixes = (
            #                         sector_names.dropna()
            #                         .str.extract(r"([A-Z]+\d+)")[0]
            #                         .dropna()
            #                         .unique()
            #                         )
            #                         MO_name_gsmsec = ",".join(prefixes)
            #                         MO_names.append(MO_name_gsmsec)

            #                         final_MO_name = " / ".join(filter(None, MO_names))
            #                         print("Combined MO Name:", final_MO_name)

            #                         template_df.loc[0, "MO Name"] = final_MO_name
            #             # else:
            #                         # template_df.loc[0, "MO Name"] = MO_name_0
                                    
            #             if "get . Fing" in xls.sheet_names :
            #                   df_fing = xls.parse("get . Fing")
            #                   # Extract fingerprint value
            #                   fing_value_series = df_fing[df_fing["Attribute"] == "fingerprint"]["Value"]
            #                   if not fing_value_series.empty:
            #                         fingerprint_mo = fing_value_series.iloc[0].strip()  # assuming one match
            #                         # print("Fingerprint MO:", fingerprint_mo)

            #                         # Match with MO_name_0 (or whatever is being used as the baseline)
            #                         if fingerprint_mo == MO_name_0:
            #                               template_df.loc[0, "Project Remarks"] = f" On-Aired-“4G GPL parameter as per the guidelines are ok”"
            #                         else:
            #                               template_df.loc[0, "Project Remarks"] = f"On-Aired-“4G GPL parameter as per the guidelines are ok/Renaming site”"

            #             if sheet_name == "get . tac":
            #                   df = xls.parse(sheet_name)
            #                   tac = df["Value"].unique()
            #                   ip_address = df["ip address"].unique()
            #                   if len(tac) > 0 and len(ip_address) > 0:
            #                         template_df.loc[0, "TAC Name"] = str(tac[0]).replace(",", "")
            #                         template_df.loc[0, "4G Node IP"] = " / ".join(ip_address)
                              
            #             elif sheet_name == "get . enroll":
            #                   df = xls.parse(sheet_name)
            #                   OSS_match = df["Attribute"].str.extract(r"OU=([\w\d]+)")
            #                   if OSS_match.notna().any().values[0]:  # check if there's at least one match
            #                         OSS = OSS_match.dropna().iloc[0, 0].strip().upper()
            #                         OSS = OSS.replace("ENM", " ENM") if "ENM" in OSS else OSS
            #                         OSS = OSS.replace("DEL", "DL") if "DEL" in OSS else OSS
            #                         template_df["OSS Name/IP"] = template_df["OSS Name/IP"].astype(object)
            #                         template_df.loc[0, "OSS Name/IP"] = OSS
            #                   else:
            #                         template_df["OSS Name/IP"] = template_df["OSS Name/IP"].astype(object)
            #                         template_df.loc[0, "OSS Name/IP"] = "NA"
            #                   print("OSS Name/IP:", template_df.loc[0, "OSS Name/IP"])

            #             # elif sheet_name == "get . enroll":
            #             #     df = xls.parse(sheet_name)
            #             #     OSS = df["Attribute"].str.extract(r"OU=([\w\d]+)")
            #             #     if not OSS.empty:
            #             #         OSS = OSS.dropna().iloc[0, 0].strip().upper()
            #             #         OSS = OSS.replace("ENM", " ENM") if "ENM" in OSS else OSS
            #             #         OSS = OSS.replace("DEL", "DL") if "DEL" in OSS else OSS
            #             #         template_df.loc[0, "OSS Name/IP"] = OSS

            #             elif sheet_name == "get . bsc":
            #                   df = xls.parse(sheet_name)
            #                   technology = df["MO"].str.extract(r"EUtranCell(FDD|TDD)")[0]
            #                   tech_values = "_".join(technology.dropna().unique())
            #                   if df["MO"].str.contains("Gsm", na=False).any():
            #                         tech_values = f"2G_{tech_values}"
            #                         Bsc = str(df.loc[df["MO"].str.contains("Gsm", na=False), "Value"].iloc[0]).split("_")[0]
            #                   else:
            #                         Bsc = "NA"

            #                   # if "Gsm" in df.loc[0, "MO"]:
            #                   #     tech_values = f"2G_{tech_values}"
            #                   #     Bsc = str(df.loc[0, 'Value']).split('_')[0]

            #                         # Bsc = df.loc[0, "Value"].split("_")[0]
            #                   # else:
            #                   #     Bsc = "NA"
            #                   template_df.loc[0, "Technology"] = tech_values
            #                   # print("Technology:", tech_values)
            #                   template_df.loc[0, "BSC (In Case Of NT/2G)"] = Bsc

            #             if sheet_name == "hget field prod":
            #                   df = xls.parse(sheet_name)
            #                   baseband = (
            #                         df["productName"]
            #                         .str.extract(r"Baseband\s+(\w+)", expand=False)
            #                         .dropna()
            #                   )
            #                   RAN_Processor = (
            #                         df["productName"]
            #                         .str.extract(r"RAN Processor\s+(\w+)", expand=False)
            #                         .dropna()
            #                   )
            #                   BB_count = baseband.count()
            #                   bb_str = f"BB{baseband.iloc[0]}*{BB_count}" if BB_count > 1 else (
            #                         f"BB{baseband.iloc[0]}" if not baseband.empty else ""
            #                   )
            #                   print("BB str:", bb_str)

            #                   ran_count = RAN_Processor.count()
            #                   ran_str = f"BB{RAN_Processor.iloc[0]}*{ran_count}" if ran_count > 1 else (
            #                         f"BB{RAN_Processor.iloc[0]}" if not RAN_Processor.empty else ""
            #                   )
            #                   combined_str = " / ".join(filter(None, [bb_str, ran_str])) or "NA"
            #                   # print(combined_str)
            #                   template_df.loc[0, "Hardware/BBU"] = combined_str

            #                   radio = df["productName"].str.extract(r"(?:Radio|RRUS)\s+(\d+)", expand=False)
            #                   band = df["productNumber"].str.extract(
            #                         r"(B\d+[A-Z]?)", expand=False
            #                   )
            #                   combined = (radio + " " + band).dropna()

            #                   countRRU = combined.value_counts()
            #                   result = " + ".join(
            #                         f"{item}*{count}" for item, count in countRRU.items()
            #                   )

            #                   # print("Grouped Radios:\n", result)
            #                   template_df.loc[0, "Hardware/RRU"] = result if result else "NA"


            #             elif sheet_name == "st rru":
            #                   df = xls.parse(sheet_name)
            #                   template_df.loc[0, "CPRI"] = len(df)

            #             elif sheet_name == "invxgr":
            #                   df = xls.parse(sheet_name)
            #                   # cprilength = df["LENGTH"].str.replace("m", "")

            #                   # template_df.loc[0, "CPRI length as per Actual"] = "/".join(
            #                   #     cprilength
            #                   # )
            #                   cprilength = df['LENGTH'].dropna().astype(str).str.replace('m', '')
            #                   template_df.loc[0, 'CPRI length as per Actual'] = '/'.join(cprilength)

            #                   def round_to_nearest_5(n):
            #                         remainder = n % 5
            #                         if remainder >= 3:
            #                               return n + (5 - remainder)
            #                         else:
            #                               return n - remainder

            #                   cpri_length_as_per_mo = "/".join(
            #                         [
            #                         str(round_to_nearest_5(int(value)))
            #                         for i, value in enumerate(cprilength)
            #                         ]
            #                   )

            #                   template_df.loc[0, "CPRI length as per MO"] = cpri_length_as_per_mo
            #                   template_df.loc[0, "CPRI length as per Survey"] = (
            #                         cpri_length_as_per_mo
            #                   )

            #             elif sheet_name == "get . sectorc":
            #                   df = xls.parse(sheet_name)
            #                   Twin_Beam = df["MO"].to_list()
            #                   Twin_Beam = [str(val).split("=")[1] for val in Twin_Beam]
            #                   # print(Twin_Beam)
            #                   Twin_Beam = [
            #                         val for val in Twin_Beam if val.endswith(("_M", "_N", "_L"))
            #                   ]
            #                   Twin_Beam = [
            #                         re.sub(
            #                         r"_(M|N|L)$",
            #                         lambda m: {"L": "_A", "M": "_B", "N": "_C"}[m.group(1)],
            #                         val,
            #                         )
            #                         for val in Twin_Beam
            #                   ]

            #                   template_df["Parent Cell Name (In Case Of Twin Beam)"] = template_df["Parent Cell Name (In Case Of Twin Beam)"].astype(object)

            #                   if len(Twin_Beam) != 0:
            #                         template_df.loc[
            #                         0, "Parent Cell Name (In Case Of Twin Beam)"
            #                         ] = ", ".join(Twin_Beam)
            #                   else:
            #                         template_df.loc[
            #                         0, "Parent Cell Name (In Case Of Twin Beam)"
            #                         ] = "NA"

            #                   print("Parent Cell Name (In Case Of Twin Beam):", template_df.loc[0, 'Parent Cell Name (In Case Of Twin Beam)'])

            #             if "st ret" in xls.sheet_names and "get . sectorc" in xls.sheet_names:

            #                   df_st = xls.parse("st ret")
            #                   df_st['MO'] = df_st['MO'].astype(str)
            #                   df_st['AntennaUnitGroup'] = df_st['MO'].str.extract(r'AntennaUnitGroup=(\d+)')
            #                   # df_st["AntennaUnitGroup"] = df_st["MO"].str.extract(
            #                   #     r"AntennaUnitGroup=(\d+)"
            #                   # )
            #                   valid_groups = df_st["AntennaUnitGroup"].dropna().unique()

            #                   df_sec = xls.parse("get . sectorc")
            #                   df_sec["SectorCarrier"] = df_sec["Value"].str.extract(
            #                         r"SectorCarrier=(\d+)"
            #                   )
            #                   df_filtered = df_sec[df_sec["SectorCarrier"].isin(valid_groups)]

            #                   MO = df_filtered["MO"].str.extract(r"=([\w\d_]+)")
            #                   MO = MO.dropna().iloc[:, 0].tolist()
            #                   # print("Filtered MOs:", MO)

            #                   if MO:
            #                         base = str(MO[0])[:-3]
            #                         suffixes = [str(s)[len(base) :] for s in MO]
            #                         result = base + "&".join(suffixes)
            #                         template_df.loc[0, "RET Configuration (Cell Name)"] = result
            #                   else:
            #                         result = "NA"
            #                         template_df.loc[0, 'RET Configuration (Cell Name)'] = result
            #                   # print("RET Configuration (Cell Name):", result)
            #                   RTT_map = {
            #                         "F1": "L2100",
            #                         "F3": "L1800",
            #                         "F8": "L900",
            #                         "T1": "L2300",
            #                         "T2": "L2300",
            #                         "F5": "L850",
            #                   }

            #                   RTT_cell = "NA"
            #                   for key in RTT_map.keys():
            #                         if key in result:
            #                               RTT_cell = RTT_map[key]
            #                         break

            #                   template_df.loc[0, "RET Configured on (Layer)"] = RTT_cell

            #             else:
            #                   template_df.loc[0, "RET Configured on (Layer)"] = "NA"
            #                   template_df.loc[0, "RET Configuration (Cell Name)"] = "NA"

            #             if sheet_name == "get . maxtx":
            #                   df_maxtx = xls.parse(sheet_name)
            #                   df_nooftx = xls.parse("get . nooftx")
            #                   df_sectorc = xls.parse("get . sectorc")
            #                   output = ""

            #                   if not df_maxtx.empty and not df_nooftx.empty and not df_sectorc.empty:
            #                         # Step 1: Filter by common SectorCarrier (MO)
            #                         common_mo = df_maxtx["MO"].unique().tolist()
            #                         df_nooftx = df_nooftx[df_nooftx["MO"].isin(common_mo)]
            #                         df_sectorc = df_sectorc[df_sectorc["Value"].isin(common_mo)]

            #                         # Step 2: Map MO -> (Power, Tx)
            #                         power_tx_map = {}
            #                         for mo in common_mo:
            #                               power = df_maxtx[df_maxtx["MO"] == mo]["Value"].values
            #                               tx = df_nooftx[df_nooftx["MO"] == mo]["Value"].values
            #                               if power.size > 0 and tx.size > 0:
            #                                     power_tx_map[mo] = (int(power[0]), int(tx[0]))

            #                               # Step 3: Map MO to Layer using sectorc and band mapping
            #                               MIMO_map = {
            #                               "F1": "L21",
            #                               "F3": "L18",
            #                               "F8": "L9",
            #                               "T1": "L23",
            #                               "T2": "L23",
            #                               "F5": "L85",
            #                               }

            #                               output_parts = []
            #                               for _, row in df_sectorc.iterrows():
            #                                     mo = row["Value"]  # This is MO in sectorc
            #                                     layer = row["MO"]  # This contains F1, F3, etc.
            #                                     match = re.search(r"(F\d|T\d)", layer)
            #                                     if match and mo in power_tx_map:
            #                                           band = match.group(1)
            #                                           mimo_layer = MIMO_map.get(band)
            #                                           if mimo_layer:
            #                                                 power, tx = power_tx_map[mo]
            #                                                 power_watt = f"{power//1000}W"
            #                                                 mimo_config = f"{tx}T{tx}R"
            #                                                 combined = f"{power_watt}({mimo_config}){mimo_layer}"
            #                                                 output_parts.append(combined)

            #                               output = ", ".join(sorted(set(output_parts)))
            #                               print("MIMO Power configuration:", output)
            #                               template_df.loc[0, "MIMO Power configuration"] = output

            #             if sheet_name == "get . fing":
            #                   df = xls.parse(sheet_name)
            #                   fingerprint = df["Value"].unique()
            #                   template_df.loc[0, "Fingerprint"] = fingerprint

            #             today = datetime.date.today()
            #             template_df.loc[0, "AT Offering Date"] = today.strftime("%d-%m-%Y")
            #             template_df.loc[0, "Scenario (In Case Of Swap)"] = "NA"
            #             template_df.loc[0, "Cell Name (New)"] = "NA"
            #             template_df.loc[0, "Link ID"] = "NA"


            #             ####################################### getting folders for final output #########################################
            #             output_path = os.path.join(base_media_url, "OUTPUT")

            #             os.makedirs(output_path, exist_ok=True)

            #             output_filename = f"{circle_value}_{base_name}_OUTPUT_{timestamp}.xlsx"
            #             output_path = os.path.join(output_path, output_filename)

            #             with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
                              
            #                   template_df.to_excel(writer, index=False)
            #                   format_excel_sheet(writer, "Sheet1", template_df)

                  ############################################# MAkING THE ZIP FILE #########################################################
                  # timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                  # zip_filename = os.path.join(base_media_url, f"OUTPUT_{timestamp}.zip")
                  # # Create zip file with all Excel files
                  # with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
                  #       logs_excel_folder = os.path.join(base_media_url, "OUTPUT")
                  #       if os.path.exists(logs_excel_folder):
                  #                   for root, dirs, files in os.walk(logs_excel_folder):
                  #                         for file in files:
                  #                               file_path = os.path.join(root, file)
                  #                               arcname = os.path.relpath(file_path, base_media_url)
                  #                               zipf.write(file_path, arcname)
                                    
                  #       print(f"Output file created: {output_path}")
                  #       print(f"Zip file created: {zip_filename}")
###########################################################################################################################
                  # return Response(
                  #       {
                  #       "status": "OK",
                  #       "message": "Files processed successfully",
                  #       "download_url": zip_filename,
                  #       },
                  #       status=HTTP_200_OK,
                  # )

            # except Exception as e:
            #     print("error:- ", str(e))
            #     return Response(
            #         {"status": "ERROR", "message": str(e)}, status=HTTP_400_BAD_REQUEST
            #     )
                                          
