from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from pathlib import Path
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
import os
import pandas as pd
import re
from pathlib import Path
import stat
import shutil
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Alignment, Font
from collections import Counter
from datetime import datetime
from openpyxl.utils import get_column_letter

def format_and_autofit_excel(file_path):
    wb = load_workbook(file_path)
    ws = wb.active

    # Header formatting
    header_fill = PatternFill(start_color="215967", end_color="215967", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    center_alignment = Alignment(horizontal="center", vertical="center")

    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_alignment

    # Data cell formatting
    yellow_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
    bold_font = Font(bold=True)

    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
        for cell in row:
            cell.alignment = center_alignment
            cell.font = bold_font
            if str(cell.value).strip().upper() == "NA":
                cell.fill = yellow_fill

    # Autofit columns
    for col in ws.columns:
        max_length = 0
        column = col[0].column  # 1-based
        column_letter = get_column_letter(column)

        for cell in col:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass

        ws.column_dimensions[column_letter].width = max_length + 2

    wb.save(file_path)


#split line--------
SPLIT_PATTEREN = r"(?=\[N_PROJECT|\[N_PROF05)"

# find the node-----------------------
def read_and_write_func(file_path):
    with open(file_path, "r") as file:
        log_content = file.readlines()
    joined_content = "".join(log_content)
    nodes = re.split(rf"{SPLIT_PATTEREN}", joined_content)
    nodes = [node.strip().split("\n") for node in nodes if node.strip()]
    return nodes

def on_rm_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)
 
 # function to get data from log-------------------------------
def get_data_from_log(command, start_point, end_point, node_lines):
    values_lines = []
    header_line = None
    command_found = False
    header_found = False
    ip_address = None
    site_id = None

    for line in node_lines:
        line = line.strip()
        site_match = re.match(r'^([\w-]+)>', line)

        if site_match:
            site_id = site_match.group(1)

        if re.match(fr'{command}', line):
            command_found = True
            continue

        if command_found and not ip_address:
            ip_match = re.match(
                r"(\d{6}-\d{2}:\d{2}:\d{2}\+\d{4})\s+([\da-fA-F:.]+)\s+(\d+\.\d+[a-zA-Z]*)\s+([\w.-]+)\s+(stopfile=[/\w\d]+)",
                line)
            if ip_match:
                ip_address = ip_match.group(2)

        if command_found:
            if re.match(fr'{start_point}', line):
                header_found = True
                header_line = line
                continue

            if header_found and re.match(fr'{end_point}', line):
                break

            if header_found and not re.match(r'^=+$', line):
                values_lines.append(line)

    return header_line, values_lines, ip_address, site_id



def delete_existing_files(folder_path):
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

#_-_-_post api__________
@api_view(["POST"])
def LKF_Upload(request):
    try:
        files = request.FILES.getlist("files")
        if not files:
            return Response(
                {"status": "false", "message": "No files uploaded"},
                status=HTTP_404_NOT_FOUND,
            )
#--make folder in media folder--------------------
        base_media_url = os.path.join(MEDIA_ROOT, "LKF_StatusApp")
        output_path_tem = os.path.join(base_media_url, "tempary_log_output")
        log_folder = os.path.join(base_media_url, "logs_files")
        log_excel_folder = os.path.join(base_media_url,"logs_excel")
    
        
        os.makedirs(log_folder, exist_ok=True)
        os.makedirs(output_path_tem, exist_ok=True)
        os.makedirs(log_excel_folder, exist_ok=True)
        

        delete_existing_files(log_folder)
        delete_existing_files(output_path_tem)
        delete_existing_files(log_excel_folder)

        saved_files = []
        for file in files:
            file_path = os.path.join(log_folder, file.name)
            with open(file_path, "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            saved_files.append(file_path)
#fatch data from log----------------
        all_files_data = {}
        for file_path in saved_files:
            try:
                nodes = read_and_write_func(file_path)
                commands = [
                    "st cell", "hget field prod","st trx",
                    "get . maxtx", "get . fingerprint", "get . sectorcarrier"
                ]
                node_data = {}

                for node_index, node in enumerate(nodes):
                    node_key = f"node_{node_index + 1}"
                    node_data[node_key] = {}

                    for command in commands:
                        if command == "st cell":
                            header_line, values_lines, ip_address, site_id = get_data_from_log(
                                r"^[A-Z0-9_-]+>\sst\scell", r"^Proxy", r"^Total:", node
                            )
                        elif command == "hget field prod":
                            header_line, values_lines, ip_address, site_id = get_data_from_log(
                                r"^[A-Z0-9_-]+>\shget\sfield\sprod", r"^MO  ", r"Total:", node
                            )
                        elif command == "get . maxtx":
                            header_line, values_lines, ip_address, site_id = get_data_from_log(
                                r"^[A-Z0-9_-]+>\sget\s\.\smaxtx", r"^MO  ", r"Total:", node
                            )
                        elif command == "get . fingerprint":
                            header_line, values_lines, ip_address, site_id = get_data_from_log(
                                r"^[A-Z0-9_-]+>\sget\s\.\sfingerprint", r"^MO  ", r"Total:", node
                            )
                        elif command == "get . sectorcarrier":
                            header_line, values_lines, ip_address, site_id = get_data_from_log(
                                r"^[A-Z0-9_-]+>\sget\s\.\ssectorcarrier", r"^MO  ", r"Total:", node
                            )
                            
                        elif command == "st trx":
                            header_line, values_lines, ip_address,site_id= get_data_from_log(
                                r"^[A-Z0-9_-]+>\sst\strx", r"^Proxy", r"Total:", node
                            )


                        node_data[node_key][command] = {
                            "header_line": header_line,
                            "values_lines": values_lines,
                            "ip_address": ip_address,
                            "site_id": site_id
                        }

                file_key = Path(file_path).stem
                all_files_data[file_key] = node_data
                
                print(f"File {file_path} processed successfully.")
            except Exception as e:
                
                print(f"Error processing file {file_path}: {str(e)}")
                continue
            

           
            

        try:
            shutil.rmtree(log_excel_folder, onerror=on_rm_error)
            os.makedirs(log_excel_folder, exist_ok=True)
        except PermissionError as e:
            print(f"Permission denied: {str(e)}")
                
 

        for file_key, node_data in all_files_data.items():
            
            excel_filename = os.path.join(log_excel_folder, f"{file_key}_.xlsx")
            with pd.ExcelWriter(excel_filename, engine="xlsxwriter") as writer:
                
                for command in commands:
                    node_dfs = []
                    for node, command_info in node_data.items():
                        if command not in command_info:
                            continue

                        header = command_info[command].get("header_line", "")
                        
                        values = command_info[command].get("values_lines", [])
                        ip_address = command_info[command].get("ip_address", "")
                        site_id = command_info[command].get("site_id", "")

                        if command != 'invxgr':
                            if command == "hget field prod":
                                header_split = re.split(r'\s{1,}', header) if header else []
                                
                            else:
                                header_split = re.split(r'\s{2,}', header) if header else []
                                value_split = re.split(r'\s{1,}', values[0]) if values else []
                                if len(header_split) > len(value_split):
                                    header_split = header_split[:len(value_split)]
                                    
                        else:
                            header_split = re.split(r'\s{1,}', header) if header else []
                            header_split = [val for val in header_split if val not in ['BER1', "BER2"]]

                        data_list = []
                        max_columns = 0
                        current_cell = None

                        for value in values:
                            value = value.strip()
                            if not value:
                                continue

                          
                            if command == "get . sectorcarrier":
                                if re.match(r'^EUtranCell(FDD|TDD)=', value):  # 4G format
                                    current_cell = re.split(r'\s{2,}', value)[0]

                                elif value.startswith('>>>') and current_cell:
                                    # 4G sectorCarrierRef
                                    match_4g = re.search(r'sectorCarrierRef\s*=\s*(ENodeBFunction=\d+,SectorCarrier=\d+)', value)
                                    if match_4g:
                                        ref_value = match_4g.group(1)
                                        data_list.append([node, current_cell, 'sectorCarrierRef', ref_value])
                                        max_columns = max(max_columns, 4)

                                    match_5g = re.search(r'nRSectorCarrierRef\s*=\s*(GNBDUFunction=\d+,NRSectorCarrier=\S+)', value)
                                    if match_5g:
                                        ref_value = match_5g.group(1)
                                        data_list.append([node, current_cell, 'nRSectorCarrierRef', ref_value])
                                        max_columns = max(max_columns, 4)

                                elif value.startswith("NRCellDU="):  
                                    current_cell = re.split(r'\s{2,}', value)[0]

                                        
                            elif command == "hget field prod":
                             if value.startswith("FieldReplaceableUnit="):
                                match = re.match(
                                    r'^FieldReplaceableUnit=([\w\-/]+)\s+(.+?)\s+([A-Z]{3}\s?\d{3}\s?\d{3}/\d+)\s+([A-Z0-9/]+)\s+(\d{8})\s+([A-Z0-9]+)',
                                    value
                                )
                                if match:
                                    mo = match.group(1)
                                    productName = match.group(2)
                                    productNumber = match.group(3)
                                    productRevision = match.group(4)
                                    productionDate = match.group(5)
                                    serialNumber = match.group(6)
                                    data_list.append([
                                        node,
                                        mo.strip(), productName.strip(),
                                        productNumber.strip(), productRevision.strip(),
                                        productionDate.strip(), serialNumber.strip()
                                    ])
                                else:
                                    # Fallback parsing for partial/irregular FieldReplaceableUnit lines
                                    value = value.replace("FieldReplaceableUnit=", "")
                                    parts = value.split()
                                    mo = parts[0] if len(parts) > 0 else ""
                                    productName = " ".join(parts[1:-4]) if len(parts) >= 6 else ""
                                    productNumber = parts[-4] if len(parts) >= 4 else ""
                                    productRevision = parts[-3] if len(parts) >= 3 else ""
                                    productionDate = parts[-2] if len(parts) >= 2 else ""
                                    serialNumber = parts[-1] if len(parts) >= 1 else ""
                                    data_list.append([
                                        node,
                                        mo.strip(), productName.strip(),
                                        productNumber.strip(), productRevision.strip(),
                                        productionDate.strip(), serialNumber.strip()
                                    ])
                                max_columns = max(max_columns, 6)
                            else:
                                value_split = re.split(r'\s{2,}', value)
                                data_list.append([node] + value_split)
                                max_columns = max(max_columns, len(value_split))

                        if not data_list:
                            continue



                        if len(header_split) < max_columns:
                            header_split += [f"Column_{i+1}" for i in range(len(header_split), max_columns)]
                        header_split.insert(0, "Node")

                        for i in range(len(data_list)):
                            if len(data_list[i]) < len(header_split):
                                data_list[i] += [""] * (len(header_split) - len(data_list[i]))

                        df = pd.DataFrame(data_list, columns=header_split)
                        if command == "get . maxtx" and not df.empty:
                            for idx, row in df.iterrows():
                                if " " in str(row['Attribute']):
                                    val = row['Attribute'].split(" ", 1)
                                    df.at[idx, 'Attribute'] = val[0]
                                    df.at[idx, 'Value'] = val[1] if len(val) > 1 else ""
                                    
                                    
                                    
                        if command == "get . sectorcarrier" and not df.empty:
                            df = df[df['MO'].str.contains(r'EUtranCell(FDD|TDD)=', na=False, regex=True) &
                                    df['Attribute'].str.contains(r'sectorCarrierRef', na=False, regex=True)]
                            df.drop(columns=['Column_4'], inplace=True, errors='ignore')
                            df['Value'] = df['Value'].apply(lambda x: str(x).split(',')[1] if ',' in str(x) else x)
                            df = df.drop_duplicates(subset=['MO', 'Attribute'])
                            
                      
                        if command == "st cell" and not df.empty:
                            df['ip_address'] = ip_address
                            df['site_value'] = site_id



                        node_dfs.append(df)


                    if not node_dfs:
                        continue
                    all_node_df = pd.concat(node_dfs, axis=0, ignore_index=True)
                    sheet_name = command[:31]
                    all_node_df.to_excel(writer, sheet_name=sheet_name, index=False)
                    worksheet = writer.sheets[sheet_name]
                    worksheet.autofilter(0, 0, len(all_node_df), len(all_node_df.columns) - 1)
                    worksheet.freeze_panes(1, 1)
                    
                    
#find the template file----
        template_file_path = os.path.join(base_media_url, "template_file")
        if not os.path.exists(template_file_path):
            os.makedirs(template_file_path, exist_ok=True)

        excel_files_paths = [os.path.join(log_excel_folder, file) for file in os.listdir(log_excel_folder)]
        #find the final output file....
        output_path_final = os.path.join(base_media_url, "LKF_Final_Output")
        os.makedirs(output_path_final, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M")
        final_output = os.path.join(output_path_final, f'LKF_Status_output_{timestamp}.xlsx')
        delete_existing_files(output_path_final)

        all_dfs = []
        for excel_file in excel_files_paths:
            template_path = os.path.join(template_file_path, "template.xlsx")
            template_df = pd.read_excel(template_path)
            xls = pd.ExcelFile(excel_file)


            for sheet_name in xls.sheet_names:
                
       #find the fingerprint         
                if sheet_name == "get . fingerprint":
                    df = xls.parse(sheet_name)
                    mask = ((df['Attribute'] == 'fingerprint') & (df['Value'].notna()) & (~df['Value'].str.contains(":", na=False)))
                    fingerprint_row = df[mask]
                    finger_print = fingerprint_row['Value'].iloc[0] if not fingerprint_row.empty else "NA"
                    template_df.loc[0, 'New FINGER PRINT'] = finger_print
                    
                    
       #find the baseband and rru              
                if sheet_name == "hget field prod":
                    df = xls.parse(sheet_name)
                    base = df['productName'].str.extract(r'(?:Baseband|RAN Processor)\s+(\w+)', expand=False).dropna()
                    baseband = base.iloc[0] if not base.empty else "NA"
                    template_df.loc[0, 'Baseband'] = baseband
                    
                    
                    

                    rru_df = df[df['productName'].str.contains(r'(AIR\s\d+\sB\d+[A-Z]*|Radio\s\d+\sB\d+[A-Z]*|RRUS\s\d+\sB\d+[A-Z]*)', na=False)]
                    model_band = rru_df['productName'].str.extract(r'(AIR\s\d+\sB\d+[A-Z]*|Radio\s\d+\sB\d+[A-Z]*|RRUS\s\d+\sB\d+[A-Z]*)', expand=False)
                    countRRU = model_band.value_counts()
                    result = '+'.join(f"{item}*{count}" for item, count in countRRU.items())
                    template_df.loc[0, 'RRU Model'] = result if result else "NA"
                    
                    
           #`find the site id and mo`       
                if sheet_name == "st cell":
                    df = xls.parse(sheet_name)
               
                    df['ip_address'] = df['ip_address'].astype(str).fillna('NA')
                    ip_address = df['ip_address'].dropna().unique()
                    template_df.loc[0, 'Node IP'] = ip_address[0] if len(ip_address) > 0 else "NA"

               
                    df['site_value'] = df['site_value'].astype(str).fillna('NA')
                    mo = df['site_value'].unique()
                    template_df.loc[0, 'MO Name'] = mo[0] if len(mo) > 0 else "NA"

                    df['site_id'] = df['site_value'].str.extractall(r'[A-Z]+(\d+)').groupby(level=0).last()
                    site_id = df['site_id'].iloc[0] if not df['site_id'].empty and pd.notna(df['site_id'].iloc[0]) else "NA"
                    template_df.loc[0, "Site Id"] = site_id

           #find the trx       
           
                if sheet_name == "st trx":
                    df = xls.parse(sheet_name)
                    trx = len(df)-1
                    trx = None if trx == 0 else trx
                    template_df.loc[0, "TRX"] = trx

              
                 
                    
                
        # find the 5g count and power      
                if sheet_name == "get . maxtx":
                    df = xls.parse(sheet_name)
                    count5g = df['MO'].str.extract(r'(NRSectorCarrier=S\d+_N11)')
                    template_df.loc[0, '5G'] = count5g.count()[0] if count5g.count()[0] else None
                    power5G_rows = df[df['MO'].str.contains(r'NRSectorCarrier=S\d+_N11')]
                    if not power5G_rows.empty:
                        power5G = power5G_rows['Value'].iloc[0]
                        power5G = power5G // 1000
                        template_df.loc[0, '5G Power'] = f"{power5G}W"

                    df_maxtx = xls.parse(sheet_name)
                    try:
                        df_sectorc = xls.parse("get . sectorcarrier")
                    except Exception as e:
                        print(f" Sheet 'get . sectorcarrier' not found: {e}")
                        df_sectorc = pd.DataFrame()
                    output = ""

                    if not df_maxtx.empty and not df_sectorc.empty:
                        common_mo = df_maxtx["MO"].unique().tolist()
                        df_sectorc = df_sectorc[df_sectorc["Value"].isin(common_mo)]
                        power_tx_map = {}
                        for mo in common_mo:
                            power_vals = df_maxtx[df_maxtx["MO"] == mo]["Value"].values
                            tx_vals = df_maxtx[df_maxtx["MO"] == mo]["TxPower"].values if "TxPower" in df_maxtx.columns else [0]
                            if len(power_vals) > 0 and len(tx_vals) > 0:
                                if pd.notna(power_vals[0]) and pd.notna(tx_vals[0]):
                                    power_tx_map[mo] = (int(power_vals[0]), int(tx_vals[0]))
                        MIMO_map = {
                            "F1": "L2100",
                            "F3": "L1800",
                            "F8": "L900",
                            "T1": "L23001",
                            "T2": "L23002",
                            "F5": "L85",
                        }
                    layer_counter = Counter()

                    for _, row in df_sectorc.iterrows():
                        mo = row["Value"]
                        band_info = row["MO"]
                        match = re.search(r"(F\d|T\d)", band_info)
                        if match:
                            band = match.group(1)
                            mimo_layer = MIMO_map.get(band)
                            if mimo_layer and mo in power_tx_map:
                                power, _ = power_tx_map[mo]
                                power_watt = f"{power // 1000}W"
                                key = f"{power_watt}{mimo_layer}"
                                layer_counter[key] += 1
                    # Process layer_counter correctly
                    for key, count in layer_counter.items():
                        match = re.match(r"(\d+)W(L\d+)", key)
                        if match:
                            power = match.group(1)
                            layer = match.group(2)

                            if layer == "L900" and count > 0:
                                template_df.loc[0, "L900"] = count
                                template_df.loc[0, "L900 Power"] = f"{power}W"

                            elif layer == "L1800" and count > 0:
                                template_df.loc[0, "FDD-L1800"] = count
                                template_df.loc[0, "FDD-Power"] = f"{power}W"

                            elif layer == "L2100" and count > 0:
                                template_df.loc[0, "L2100"] = count
                                template_df.loc[0, "L2100 Power"] = f"{power}W"

                            elif layer == "L23001" and count > 0:
                                existing_value = template_df.loc[0, "TDD-20Mz"] if "TDD-20Mz" in template_df.columns else None
                                if pd.isna(existing_value):
                                    template_df.loc[0, "TDD-20Mz"] = count
                                else:
                                    template_df.loc[0, "TDD-20Mz"] += count

                            elif layer == "L23002" and count > 0:
                          
                                existing_value = template_df.loc[0, "TDD-10Mhz"] if "TDD-10Mhz" in template_df.columns else None
                                if pd.isna(existing_value):
                                    template_df.loc[0, "TDD-10Mhz"] = count
                                else:
                                    template_df.loc[0, "TDD-10Mhz"] += count
                                template_df.loc[0, "TDD Power"] = f"{power}W"
                                 
         #save the output log file----
            base_name = os.path.splitext(os.path.basename(excel_file))[0]
            output_filename = f"{base_name}_output.xlsx"
            individual_output_path = os.path.join(output_path_tem, output_filename)

            template_df.to_excel(individual_output_path, index=False)
            all_dfs.append(template_df)

        # Merge all processed DataFrames into one
        merged_df = pd.concat(all_dfs, ignore_index=True)
        merged_df.to_excel(final_output, index=False)
        
        format_and_autofit_excel(final_output)
        
        relative_path = os.path.join(f"LKF_StatusApp/LKF_Final_Output/LKF_Status_output_{timestamp}.xlsx").replace("\\", "/")
        download_url = request.build_absolute_uri(MEDIA_URL + relative_path)

        return Response(
            {
                "status": True,
                "message": "Files processed successfully",
                "download_url": download_url,
            },
            status=HTTP_200_OK,
        )

    except Exception as e:
        return Response(
            {
                "status": False,
                "message": f"An error occurred: {str(e)}",
            },
            status=HTTP_400_BAD_REQUEST,
        )
