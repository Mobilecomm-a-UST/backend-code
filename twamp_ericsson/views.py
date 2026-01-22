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
def twamp_data(request):
      all_files_df = pd.DataFrame()
      final_output_df = pd.DataFrame()  # This will accumulate all template data

      circle = request.POST.get("circle")
      files = request.FILES.getlist("files")
      if not files:
            return Response(
                  {"status": "ERROR", "message": "No files uploaded"},
                  status=HTTP_400_BAD_REQUEST,
            )
      
      base_media_url = os.path.join(MEDIA_ROOT, "TWAMP_Ericsson")
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
            
            # hget_address_address_df = explode_data_from_log(
            #       r'[A-Z0-9_-]+>\shget\s+address\s+address',
            #       r'(MO)\s+(address)\s+(addressIPv4Id|addressIPv6Id)\s+(primaryAddress)\s+(usedAddress)',
            #       r'(Router=\S+?,Interface(?:IPv4|IPv6)=\S+?,Address(?:IPv4|IPv6)=\S+)\s+([\d.:a-fA-F]+/\d+)\s+(\S+)\s+(true|false)\s+([\d.:a-fA-F]+/\d+)',
            #       r'^Total:\s\d+',
            #       file_content
            # )

                        
            hget_address_ipv4_df = explode_data_from_log(
                  r'[A-Z0-9_-]+>\shget\s+address|Address\s+address|Address',
                  r'(MO)\s+(address)\s+(addressIPv4Id)\s+(primaryAddress)\s+(usedAddress)',
                  r'\s*(Router=\S+,InterfaceIPv4=\S+,AddressIPv4=\S+)\s+(\d{1,3}(?:\.\d{1,3}){3}\/\d+)\s+(\S+)\s+(true|false)\s+(\d{1,3}(?:\.\d{1,3}){3}\/\d+)$',
                  r'^Total:\s\d+',
                  file_content
                  )
      
            
            hget_address_ipv6_df = explode_data_from_log(
                  r'Added\s+\d+\s+MOs\s+to\s+group:\s+hget_group',
                  r'(MO)\s+(address)\s+(addressIPv6Id)\s+(primaryAddress)\s+(usedAddress)',
                  r'\s*(Router=\S+,InterfaceIPv6=\S+,AddressIPv6=\S+)\s+([\da-fA-F:]+\/\d+)\s+(\S+)\s+(true|false)\s+([\da-fA-F:]+\/\d+)$',
                  r'^Total:\s\d+',
                  file_content
                  )
            
            
            hget_address_address_df = pd.concat([hget_address_ipv4_df, hget_address_ipv6_df], ignore_index=True)

            
            with pd.ExcelWriter(excel_filename, engine="xlsxwriter") as writer:
                  hget_address_address_df.to_excel(writer, sheet_name="sheet1", index=False)
                  format_excel_sheet(writer, "sheet1", hget_address_address_df)

            # Process the data and add to final output
            if not hget_address_address_df.empty:
                  template_path = os.path.join(template_file_path, "twamp_template.xlsx")
                  template_df = pd.ExcelFile(template_path).parse()
                  
                  df = hget_address_address_df
                  df.columns = df.columns.astype(str).str.strip()
                  
                  if "MO" in df.columns:
                        # Filter rows where MO column contains 'AddressIPv4=TN_B_CP'
                        ControlPlane = df["MO"].str.contains(r"AddressIPv4=\S+_CP", na=False)
                        print("____________________________________",ControlPlane)
                        if ControlPlane.any():
                              matched_address = df.loc[ControlPlane, "address"].str.split("/").str[0].values[0]
                              template_df.loc[0, "ControlPlane"] = matched_address
                        else:
                              template_df.loc[0, "ControlPlane"] = "Missing"

                        # Filter rows where MO column contains 'AddressIPv4=TN_B_UP'
                        UserPlane = df["MO"].str.contains(r"AddressIPv4=\S+_UP", na=False)
                        if UserPlane.any():
                              matched_address = df.loc[UserPlane, "address"].str.split("/").str[0].values[0]
                              template_df.loc[0, "UserPlane"] = matched_address
                        else:
                              template_df.loc[0, "UserPlane"] = "Missing"

                        # Filter rows where MO column contains 'AddressIPv4|AddressIPv6=TN_B_OAM'
                        OAM = df["MO"].str.contains(r"AddressIPv4|AddressIPv6=\S+_OAM", na=False)
                        if OAM.any():
                              matched_address = df.loc[OAM, "address"].str.split("/").str[0].values[0]
                              template_df.loc[0, "Mplane IP"] = matched_address
                        else:
                              template_df.loc[0, "Mplane IP"] = "Missing"
                  else:
                        template_df.loc[0, "ControlPlane"] = "Missing"
                        template_df.loc[0, "UserPlane"] = "Missing"
                        template_df.loc[0, "Mplane IP"] = "Missing"


                  if circle == "KK":
                        all_plane = df["MO"].str.contains(r"AddressIPv6=X2_ENDC", na=False)
                        if all_plane.any():
                              matched_address = df.loc[all_plane, "address"].str.split("/").str[0].values[0]
                              template_df.loc[0, "ControlPlane"] = matched_address
                              template_df.loc[0, "UserPlane"] = matched_address
                              template_df.loc[0, "Mplane IP"] = matched_address
                        else:
                              template_df.loc[0, "ControlPlane"] = "Missing"
                              template_df.loc[0, "UserPlane"] = "Missing"
                              template_df.loc[0, "Mplane IP"] = "Missing"

                  template_df.loc[0, "Circle"] = circle
                  if 'Node_ID' in df.columns:
                        template_df.loc[0, "SiteID"] = df['Node_ID'].unique()[0]
                  else:
                        template_df.loc[0, "SiteID"] = "Missing"
                  
                  # Append this node's data to the final output
                  final_output_df = pd.concat([final_output_df, template_df], ignore_index=True)

      # Create single output file
      os.makedirs(output_path, exist_ok=True)
      output_filename = f"TWAMP_OUTPUT_{timestamp}.xlsx"
      output_filepath = os.path.join(output_path, output_filename)
      
      with pd.ExcelWriter(output_filepath, engine="xlsxwriter") as writer:
            final_output_df.to_excel(writer, index=False, sheet_name="TWAMP Results")
            format_excel_sheet(writer, "TWAMP Results", final_output_df)

      # Create download link for the single output file
      download_link = request.build_absolute_uri(
            os.path.join(MEDIA_URL, "TWAMP_Ericsson", "OUTPUT", output_filename)
      )
      
      return Response(
            {
                  "status": True,
                  "message": "Files processed successfully",
                  "download_url": download_link,
            },
            status=HTTP_200_OK,
      )