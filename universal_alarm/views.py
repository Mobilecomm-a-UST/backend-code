from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Border, Font, Alignment, Side
from rest_framework.response import Response
from rest_framework.decorators import api_view
import os
import re
import pandas as pd
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
from rest_framework import status
import shutil
from datetime import datetime
 
 
 
 
 
 
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
            "border": 0,
            "border_color": "#000000",
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
            elif cell_value == "NOT OK":
                format_style = not_ok_format
            elif cell_value == "Missing":
                format_style = workbook.add_format(
                    {
                        "bg_color": "#FF6347",
                        "font_color": "#FFFFFF",
                        "align": "center",
                        "valign": "center",
                    }
                )
 
            worksheet.write(
                startrow + row_num + 1, startcol + col_num, cell_value, format_style
            )
 
            writer._save()
 
 
def delete_existing_files(upload_files):
    for file_name in os.listdir(upload_files):
        file_path = os.path.join(upload_files, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
 
 
@api_view(['POST'])
def upload_5g_log_file(request):
    if request.method != 'POST':
        return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
 
    log_files = request.FILES.getlist('log_files')
   
    if not log_files:
        return Response({"error": "5G log file must not be empty"}, status=status.HTTP_400_BAD_REQUEST)
 
    circle = request.POST.get("circle")
   
    if not circle:
        return Response({"error": "circle not found in input"}, status=status.HTTP_400_BAD_REQUEST)
   
    base_folder = os.path.join(MEDIA_ROOT, "Universal_alarm")
    if not os.path.exists(base_folder):
        os.makedirs(base_folder, exist_ok=True)
 
    output_folder = os.path.join(base_folder, "daily_status_alarm")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)
 
    log_folder = os.path.join(base_folder, "log_files_5g")
    os.makedirs(log_folder, exist_ok=True)
    delete_existing_files(log_folder)
################################################# empty output with circle folder ####################################################################################
    today=datetime.now().strftime("%Y-%m-%d")
    circle_based_output_path = os.path.join(output_folder, today, circle)

#######################################################################################################################################################################
 
    for file in log_files:
        file_path = os.path.join(log_folder, file.name)
        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
 
    def extract_sync_status(content):
        sync_ok = False
        sync_lines = []
        for line in content.splitlines():
            if "TimeSyncIO=1" in line and "1 (ENABLED)" in line:
                sync_ok = True
                sync_lines.append(line.strip())
        return "OK" if sync_ok else "NOT OK"
 
    def extract_site_id_from_cell_name(cell_name):
        match = re.search(r'_([A-Za-z0-9]{5,12})[A-Z]_', cell_name)
        return match.group(1) if match else ""
 
    def extract_circle_from_cell_name(cell_name):
        match = re.match(r'([A-Z]+)_', cell_name)
        return match.group(1) if match else "Unknown"
 
    def parse_cell_block(content):
        pattern = re.compile(
            r'\d+\s+\d+ \((?P<adm_state>UNLOCKED|LOCKED)\)\s+'
            r'\d+ \((?P<op_state>ENABLED|DISABLED)\)\s+'
            r'(ENodeBFunction|GNBDUFunction)=\d+,(?P<cell_type>EUtranCellFDD|EUtranCellTDD|NRCellDU)=(?P<cell_name>[\w\-]+)'
        )
        cells = []
        for match in pattern.finditer(content):
            adm_state = match.group("adm_state")
            op_state = match.group("op_state")
            cell_name = match.group("cell_name")
            cell_type_str = match.group("cell_type")
 
            site_id = extract_site_id_from_cell_name(cell_name)
            circle = extract_circle_from_cell_name(cell_name)
            cell_type = "5G" if "NRCellDU" in cell_type_str else "4G"
 
            cells.append({
                'Adm State': adm_state,
                'Op. State': op_state,
                'Cell Name': cell_name,
                'Site ID': site_id,
                'Circle': circle,
                'Cell Type': cell_type
            })
        return cells
 
    def extract_alarms_from_alt(content, site_id="Unknown"):
        alarms = []
        node_id_match = re.search(r'(\S+)>[\s]*alt', content)
        node_id = node_id_match.group(1).strip() if node_id_match else "Unknown"
 
        ip_match = re.search(r'\d{6}-\d{2}:\d{2}:\d{2}[+|-]\d{4}\s+([a-fA-F0-9:.]+)', content)
        ip = ip_match.group(1) if ip_match else "No IP found"
 
        alarm_pattern = re.compile(r'''
            ^\s*
            (?P<dt>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})
            \s+(?P<sev>[Mm])
            \s+(?P<prob>.+?)
            \s+(?P<mo>[^()]+?)
            (?:\s*\(\s*(?P<add>.*?)\))?
            \s*$
        ''', re.MULTILINE | re.VERBOSE)
 
        for m in alarm_pattern.finditer(content):
            alarms.append({
                "IP": ip,
                "Site ID": site_id,
                "Node ID": node_id,
                "Date & Time": m.group("dt"),
                "Severity": m.group("sev"),
                "Specific Problem": m.group("prob").strip(),
                "MO": m.group("mo").strip(),
                "Additional": (m.group("add") or "").strip()
            })
        return alarms
 
    all_rows = []
    all_alarms = []
 
    for log_file in os.listdir(log_folder):
        log_file_path = os.path.join(log_folder, log_file)
        with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content_5g = file.read()
 
        ip_match = re.search(r'([\w:.]+)(?=>\s*lt all)', content_5g)
        ip_5g = ip_match.group(1) if ip_match else "No IP found"
 
        node_match = re.search(r'([\w:-]+)(?=>\s*alt)', content_5g)
        node_id = node_match.group(1) if node_match else "No ID found"
 
        sync_status = extract_sync_status(content_5g)
        cells_5g = parse_cell_block(content_5g)
 
        for cell in cells_5g:
            row = {
                ("Circle", ""): cell['Circle'],
                ("2G Site ID", ""): cell['Site ID'],
                ("5G Site ID", ""): cell['Site ID'],
                ("5G Node IP", ""): ip_5g,
                ("5G Node ID", ""): node_id,
                ("5G Cell Status", "Adm State"): cell['Adm State'],
                ("5G Cell Status", "Op. State"): cell['Op. State'],
                ("Cells", ""): cell['Cell Name'],
                ("SYNC", "Status"): sync_status,
                ("Cell Type", ""): cell["Cell Type"]
            }
            all_rows.append(row)
            site_id = cell['Site ID']
            alarms = extract_alarms_from_alt(content_5g, site_id)
            all_alarms.extend(alarms)
 
    columns = [
        ("Circle", ""), ("2G Site ID", ""), ("5G Site ID", ""), ("5G Node IP", ""),
        ("5G Node ID", ""), ("5G Cell Status", "Adm State"), ("5G Cell Status", "Op. State"),
        ("Cells", ""), ("SYNC", "Status"), ("Cell Type", "")
    ]
    multi_index = pd.MultiIndex.from_tuples(columns)
    df_5g = pd.DataFrame(all_rows, columns=multi_index)
    df_5g.columns = [' - '.join(filter(None, col)).strip() for col in df_5g.columns.values]
 
    df_alarms = pd.DataFrame(all_alarms)
 
    if not df_alarms.empty:
        grouped_rows = []
        grouped = df_alarms.groupby(["IP", "Site ID", "Node ID"])
 
        for (ip, site_id, node_id), group in grouped:
            combined = {
                "IP": ip,
                "Site ID": site_id,
                "Node ID": node_id,
                "Date & Time": '/ '.join(group["Date & Time"].dropna().unique()),
                "Severity": '/ '.join(group["Severity"].dropna().unique()),
                "Specific Problem": '/ '.join(group["Specific Problem"].dropna().unique()),
                "MO": '/ '.join(group["MO"].dropna().unique()),
                "Additional": '/ '.join(group["Additional"].dropna().unique()),
            }
            grouped_rows.append(combined)
 
        df_alarms = pd.DataFrame(grouped_rows)
    else:
        df_alarms = pd.DataFrame(columns=[
            "IP", "Site ID", "Node ID", "Date & Time", "Severity",
            "Specific Problem", "MO", "Additional"
        ])
 
 
    circles = sorted(set(
        row[('Circle', '')].strip().upper().replace(" ", "_")
        for row in all_rows if row.get(('Circle', ''))
    ))
    circle_name = "".join(circles) if len(circles) > 1 else circles[0]
    output_filename = f"5G_Alarm_Logs_{circle}.xlsx"
    output_path = os.path.join(circle_based_output_path, output_filename)
 
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        df_5g.to_excel(writer, index=False, sheet_name="5G Cells")
        df_alarms.to_excel(writer, index=False, sheet_name="Alarms")
        format_excel_sheet(writer, '5G Cells', df_5g)
        format_excel_sheet(writer, 'Alarms', df_alarms)
 
    relative_path = os.path.join("media", "Universal_alarm", output_filename)
    download_link = request.build_absolute_uri("/" + relative_path.replace("\\", "/"))
 
    print("✅ Excel saved:", output_path)
    return Response({
        "message": f"Report generated successfully for circle: {circle_name}",
        "download_link": download_link,
        "status": True
    })
 
############################################################################################################################
 
 
def delete_existing_files(upload_files):  # noqa: F811
    for file_name in os.listdir(upload_files):
        file_path = os.path.join(upload_files, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
 
 
 
 
@api_view(['POST'])
def upload_4g_log_file(request):
    if request.method != 'POST':
        return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
 
    log_files = request.FILES.getlist('log_files')
   
    if not log_files:
        return Response({"error": "4G log file must not be empty"}, status=status.HTTP_400_BAD_REQUEST)
 
    circle = request.POST.get("circle")
   
    if not circle:
        return Response({"error": "circle not found in input"}, status=status.HTTP_400_BAD_REQUEST)
   
    base_folder = os.path.join(MEDIA_ROOT, "Universal_alarm")
    if not os.path.exists(base_folder):
        os.makedirs(base_folder, exist_ok=True)
 
    output_folder = os.path.join(base_folder, "daily_status_alarm")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)
 
    log_folder = os.path.join(base_folder, "log_files_4g")
    os.makedirs(log_folder, exist_ok=True)
    delete_existing_files(log_folder)
################################################# empty output with circle folder ####################################################################################
    today=datetime.now().strftime("%Y-%m-%d")
    circle_based_output_path = os.path.join(output_folder,today, circle)
    if os.path.exists(circle_based_output_path):
        shutil.rmtree(circle_based_output_path)
        print(f"{circle_based_output_path} deleted successfully")
    else:
        os.makedirs(circle_based_output_path, exist_ok=True)
 
    for file in log_files:
        file_path = os.path.join(log_folder, file.name)
        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
 
   
 
    def get_band(cell_name):
        band_map = {
            "F8": "L900",
            "F1": "L2100",
            "F3": "L1800",
            "T1": "L2300",
            "T2": "L2300",
        }
 
        # Use regex to extract the band code from cell name (e.g., F8, F1, etc.)
        match = re.search(r'_([FT]\d)_', cell_name)
        if match:
            band_code = match.group(1)
            return band_map.get(band_code, "")
        return ""
    def extract_4g_sync_status(content_4g):
        sync_ok = False
        sync_lines = []
 
        for line in content_4g.splitlines():
            if "TimeSyncIO=1" in line and "1 (ENABLED)" in line:
                sync_ok = True
                sync_lines.append(line.strip())
 
        print("🧪 Sync lines found:", sync_lines)
 
        return "OK" if sync_ok else "NOT OK"
    def extract_4g_site_id_from_cell_name(cell_name):
   
        match = re.search(r'_([A-Za-z0-9]{5,12})[A-Z]_', cell_name)
        return match.group(1) if match else ""
   
   
    def extract_4g_circle_from_cell_name(cell_name):
        match = re.match(r'([A-Z]+)_', cell_name)
        return match.group(1) if match else "Unknown"
 

 
 
    def site_down_4g(content_4g, site_id="Unknown"):
       
    #   def site_down_4g(content_4g, site_id="Unknown"):
        site_down=[]
        ip_match = re.search(
        # r'\d{6}-\d{2}:\d{2}:\d{2}[+|-]\d{4}\s+([a-fA-F0-9:.]+)',
         r'Logging to file .+?/([a-fA-F0-9:.]+)\.log',
       
        content_4g)
        ip_address = ip_match.group(1) if ip_match else "IP Not Found"
        status = "OK" if "Checking ip contact...OK" in content_4g else "NOT OK"
       
        site_down.append(
            {
                "Status": status,
                "IP Address": ip_address,
           
            }
        )
        return site_down
   
    def extract_4galarms_from_alt(content, site_id="Unknown"):
        alarms = []
 
        # Extract Node ID
        node_id_match = re.search(r'(\S+)>[\s]*alt', content)
        node_id = node_id_match.group(1).strip() if node_id_match else "Unknown"
 
        # Extract IP (IPv4 or IPv6) from line after 'alt'
        ip_match = re.search(
        r'\d{6}-\d{2}:\d{2}:\d{2}[+|-]\d{4}\s+([a-fA-F0-9:.]+)',
        content)
        ip = ip_match.group(1) if ip_match else "No IP found"
 
       
        alarm_pattern = re.compile(r'''
            ^\s*
            (?P<dt>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})  
            \s+(?P<sev>[Mm])                              
            \s+(?P<prob>.+?)                              
            \s+(?P<mo>[^()]+?)                            
            (?:\s*\(\s*(?P<add>.*?)\))?                  
            \s*$
        ''', re.MULTILINE | re.VERBOSE)
 
        for m in alarm_pattern.finditer(content):
            alarms.append({
                "IP":               ip,
                "Site ID":          site_id,
                "Node ID":          node_id,
                "Date & Time":      m.group("dt"),
                "Severity":         m.group("sev"),
                "Specific Problem": m.group("prob").strip(),
                "MO":               m.group("mo").strip(),
                "Additional":       (m.group("add") or "").strip()
            })
 
        print(f"✅ Extracted {len(alarms)} alarms for IP: {ip}")
        return alarms
    ##############################################################
 
    def extract_all_2g_trx_status(content):
        pattern = re.compile(
            r'GsmSector=\d+,Trx=([A-Z0-9-]+)\s+abisTsState\s+i\[\d+\]\s*=\s*[\d\s]+\(([A-Z\s]+)\)',
            # r'GsmSector=\d+,Trx=([A-Z0-9-]+)\s+abisTsState\s+i\[\d+\]\s*=\s*[\d\s]+\(([A-Z\s]+)\)',
            re.IGNORECASE
        )
 
        # trx_status_list = []
        trx_status_dict = {}
 
        for match in pattern.finditer(content):
            trx_name = match.group(1)
            raw_statuses = match.group(2).split()
 
            # Assume majority value or just pick first (can adjust logic here)
            # unique_statuses = set(s.upper() for s in raw_statuses)
            unique_statuses = set(s.upper() for s in raw_statuses)
 
            if "ENABLED" in unique_statuses:
                final_status = "UNLOCKED"
            elif "DISABLED" in unique_statuses:
                final_status = "LOCKED"
            elif "RESET" in unique_statuses:
                final_status = "DOWN"
            else:
                final_status = "UNKNOWN"
 
            # trx_status_list.append((trx_name, final_status))
            trx_status_dict[trx_name] = final_status
        trx_status_list = [(trx_name, status) for trx_name, status in trx_status_dict.items()]
        # trx_status_str = "\n".join([f"{trx} - {status}" for trx, status in trx_status_dict.items()])
       
        # trx_status_str = "\n".join(trx_status_list)
 
        return trx_status_list
        # print("2G TRX Status Extracted ➤", extract_all_2g_trx_status(content_4g))
       
 
    def parse_4g_st_cell_output(content_4g):
        pattern = re.compile(
            r'\d+\s+\d+ \((?P<adm_state>UNLOCKED|LOCKED)\)\s+'
            r'\d+ \((?P<op_state>ENABLED|DISABLED)\)\s+'
            r'(ENodeBFunction|GNBDUFunction)=\d+,(?:EUtranCellFDD|EUtranCellTDD)=(?P<cell_name>[\w\-]+)'
        )
 
        cells= []
        for match in pattern.finditer(content_4g):
            cell_name = match.group("cell_name")
            adm_state = match.group("adm_state")
            op_state = match.group("op_state")
            circle =  extract_4g_circle_from_cell_name(cell_name)
            site_id = extract_4g_site_id_from_cell_name(cell_name)
 
            band = get_band(cell_name)
            print(f"📡 Cell Name: {cell_name} ➤ 🏷️ Site ID: {site_id} ")
            cells.append({
                ("4G Cell Status", "Adm State"): adm_state,
                ("4G Cell Status", "Op. State"): op_state,
                # ("Cells", ""): cell_name,
                # ("Circle", ""): circle,
                # ("Site ID", ""): site_id,
                # ("BAND", ""): [get_band(cell) for cell in cell_name],
                # ("Band", ""): band,
                # 'Adm State': adm_state,
                # 'Op. State': op_state,
                'Cell Name': cell_name,
                'Site ID': site_id,
                'Circle': circle,
                'Band': band
            })
        return cells
    all_rows = []
    all_alarms = []
    site_down = []
    for log_file in os.listdir(log_folder):
        log_file_path = os.path.join(log_folder, log_file)
        with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content_4g = file.read()
        ip_match = re.search(r'([\w:.]+)(?=>\s*lt all)', content_4g)
        ip_4g = ip_match.group(1) if ip_match else "No IP found"
 
        node_match = re.search(r'([\w:-]+)(?=>\s*alt)', content_4g)
        node_id = node_match.group(1) if node_match else "No ID found"
 
        sync_status = extract_4g_sync_status(content_4g)
        cells_4g = parse_4g_st_cell_output(content_4g)
        trx_status_list = extract_all_2g_trx_status(content_4g)
        trx_status_str = "; ".join([f"{trx} - {status}" for trx, status in trx_status_list])
        for cell in cells_4g:
            row = {
                ('Circle', ''): cell['Circle'],
                ('2G Site ID', ''): cell['Site ID'],
                ('4G Site ID', ''): cell['Site ID'],  # Assuming naming rule
                ('4G Node IP', ''): ip_4g,
                ('4G Node ID', ''): node_id,
                ('4G Cell Status', 'Adm State'): cell[('4G Cell Status', 'Adm State')],
                ('4G Cell Status', 'Op. State'): cell[('4G Cell Status', 'Op. State')],
                ('Cells', ''): cell['Cell Name'],
                # ('2G Cell(TRX) Status', ''): [extract_all_2g_trx_status(content_4g)] ,
                ("2G Cell(TRX) Status", "Status"): trx_status_str,
                # ('2G Cell(TRX) Status', ''): "; ".join([f"{trx} - {status}" for trx, status in extract_all_2g_trx_status(content_4g)]),
                ('SYNC', 'Status'): sync_status,  
                ('Band', ''): cell['Band']
            }
            all_rows.append(row)
 
        for cell in cells_4g:
            site_id = cell['Site ID']
            alarms = extract_4galarms_from_alt(content_4g, site_id)
            all_alarms.extend(alarms)
            site_down.extend(site_down_4g(content_4g, site_id))
 
    columns = [
        ("Circle", ""),
        ("2G Site ID", ""),
        ("4G Site ID", ""),
        ("4G Node IP", ""),
        ("4G Node ID", ""),
        ("4G Cell Status", "Adm State"),
        ("4G Cell Status", "Op. State"),
        ("Cells", ""),
        ("2G Cell(TRX) Status", "Status"),
        ("SYNC", "Status"),
        ("Band", ""),
    ]
    multi_index = pd.MultiIndex.from_tuples(columns)
    df_4g = pd.DataFrame(all_rows, columns=multi_index)
 
# ❗ Flatten before saving to Excel
    df_4g.columns = [' - '.join(filter(None, col)).strip() for col in df_4g.columns.values]
 
# Alarm sheet
    if all_alarms:
        alarm_df = pd.DataFrame(all_alarms)
       
        # Group by IP + Site ID + Node ID and merge columns
        agg_alarms = alarm_df.groupby(["IP", "Site ID", "Node ID"]).agg({
            "Date & Time": lambda x: "/ ".join(sorted(set(x))),
            "Severity": lambda x: "/ ".join(sorted(set(x))),
            "Specific Problem": lambda x: "/".join(sorted(set(x))),
            "MO": lambda x: "/".join(sorted(set(x))),
            "Additional": lambda x: "/".join(sorted(set(filter(None, x))))
        }).reset_index()
        df_alarms = agg_alarms
    else:
        df_alarms = pd.DataFrame()
    site_down_df = pd.DataFrame(site_down).drop_duplicates()
 
    circles = sorted(set(
    row[('Circle', '')].strip().upper().replace(" ", "_")
    for row in all_rows if row.get(('Circle', ''))
    ))
 
        # Join all circle names (like TNCH or TN_ORI_CH)
    circle_name = "".join(circles) if len(circles) > 1 else circles[0]
    output_filename = f"4G_Alarm_Logs_{circle}.xlsx"
    output_path = os.path.join(circle_based_output_path, output_filename)
    ##################################
    # with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        df_4g.to_excel(writer, index=False, sheet_name="4G Cells")
        df_alarms.to_excel(writer, index=False, sheet_name="Alarms")
        site_down_df.to_excel(writer, sheet_name="Site Down", index=False)
        format_excel_sheet(writer, 'Alarms', df_alarms ,)
 
    relative_path = os.path.join("media", "Universal_alarm", output_filename)
    download_link = request.build_absolute_uri("/" + relative_path.replace("\\", "/"))
 
    wb = load_workbook(output_path)
    ws = wb.active
    for sheet_name in wb.sheetnames:
        ws = wb["4G Cells"]
 
        header_fill = PatternFill(start_color="259aa8", end_color="4682B4", fill_type="solid")
        header_font = Font(color="FFFFFF", bold=True)
        header_align = Alignment(horizontal="center", vertical="center")
 
        thin_border = Border(
            left=Side(style='thin'), right=Side(style='thin'),
            top=Side(style='thin'), bottom=Side(style='thin')
        )
        prev_value = None
        start_col = 1
        for col in range(1, ws.max_column + 1):
            top_cell = ws.cell(row=1, column=col)
            sub_cell = ws.cell(row=2, column=col)
            top_val = top_cell.value
            sub_val = sub_cell.value  # noqa: F841
            # Detect merged header range
            if top_val != prev_value:
                if col > start_col:
                    if prev_value not in (None, ""):
                        ws.merge_cells(
                            start_row=1, start_column=start_col,
                            end_row=1, end_column=col - 1
                        )
                start_col = col
                prev_value = top_val
        # Final merge for last group
        if prev_value not in (None, "") and start_col <= ws.max_column:
            ws.merge_cells(
                start_row=1, start_column=start_col,
                end_row=1, end_column=ws.max_column
            )
        # Styling headers
        for row in [1, 1]:
            for col in range(1, ws.max_column + 1):
                cell = ws.cell(row=row, column=col)
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = header_align
                cell.border = thin_border
        # Style entire data range
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
            for cell in row:
                cell.border = thin_border
        wb.save(output_path)
        print("✅ Excel saved:", output_path)
    return Response({
        # "message": "4G log file processed successfully",
        "message": f"Report generated successfully for circle: {circle_name}",
        "download_link": download_link,
        "status": True
    }, status=200)
###############################################  updated code ############################################################



# from openpyxl import load_workbook
# from openpyxl.styles import PatternFill, Border, Font, Alignment, Side
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# import os
# import re
# import pandas as pd
# from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
# from rest_framework import status
 
 
 
 
 
 
# def format_excel_sheet(writer, sheet_name, df, startrow=0, startcol=0):
#     """Apply formatting to an Excel sheet with adjustable start positions."""
#     workbook = writer.book
#     worksheet = writer.sheets[sheet_name]
 
#     header_format = workbook.add_format(
#         {
#             "bold": True,
#             "bg_color": "#000957",
#             "border": 2,
#             "font_color": "#ffffff",
#             "align": "center",
#             "valign": "vcenter",
#         }
#     )
#     center_format = workbook.add_format(
#         {
#             "align": "center",
#             "valign": "center",
#             "border": 0,
#             "border_color": "#000000",
#         }
#     )
#     ok_format = workbook.add_format(
#         {
#             "bg_color": "#90EE90",
#             "font_color": "#000000",
#             "align": "center",
#             "valign": "center",
#         }
#     )
#     not_ok_format = workbook.add_format(
#         {
#             "bg_color": "#FF0000",
#             "font_color": "#FFFFFF",
#             "align": "center",
#             "valign": "center",
#         }
#     )
 
#     worksheet.set_row(startrow, 23)
 
#     for col_num, col_name in enumerate(df.columns):
#         worksheet.write(startrow, startcol + col_num, str(col_name), header_format)
 
#         column_series = df[col_name]
#         if isinstance(column_series, pd.DataFrame):
#             column_series = column_series.iloc[:, 0]
 
#         max_length = max(
#             column_series.fillna("").astype(str).str.len().max(skipna=True) or 0,
#             len(str(col_name)),
#         )
#         max_length = min(max_length, 255)
#         worksheet.set_column(startcol + col_num, startcol + col_num, max_length + 5)
 
#     for row_num in range(len(df)):
#         worksheet.set_row(startrow + row_num + 1, 15)
 
#         for col_num in range(len(df.columns)):
#             cell_value = str(df.iloc[row_num, col_num])
#             format_style = center_format
#             if cell_value == "OK":
#                 format_style = ok_format
#             elif cell_value == "NOT OK":
#                 format_style = not_ok_format
#             elif cell_value == "Missing":
#                 format_style = workbook.add_format(
#                     {
#                         "bg_color": "#FF6347",
#                         "font_color": "#FFFFFF",
#                         "align": "center",
#                         "valign": "center",
#                     }
#                 )
 
#             worksheet.write(
#                 startrow + row_num + 1, startcol + col_num, cell_value, format_style
#             )
 
#             writer._save()
 
 
# def delete_existing_files(upload_files):
#     for file_name in os.listdir(upload_files):
#         file_path = os.path.join(upload_files, file_name)
#         if os.path.isfile(file_path):
#             os.remove(file_path)
 
 
# @api_view(['POST'])
# def upload_5g_log_file(request):
#     if request.method != 'POST':
#         return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
 
#     log_files = request.FILES.getlist('log_files')
#     if not log_files:
#         return Response({"error": "5G log file must not be empty"}, status=status.HTTP_400_BAD_REQUEST)
 
#     log_folder = os.path.join(MEDIA_ROOT, "Universal_alarm", "log_files_5g")
#     os.makedirs(log_folder, exist_ok=True)
#     delete_existing_files(log_folder)
 
#     for file in log_files:
#         file_path = os.path.join(log_folder, file.name)
#         with open(file_path, "wb+") as destination:
#             for chunk in file.chunks():
#                 destination.write(chunk)
 
#     def extract_sync_status(content):
#         sync_ok = False
#         sync_lines = []
#         for line in content.splitlines():
#             if "TimeSyncIO=1" in line and "1 (ENABLED)" in line:
#                 sync_ok = True
#                 sync_lines.append(line.strip())
#         return "OK" if sync_ok else "NOT OK"
 
#     def extract_site_id_from_cell_name(cell_name):
#         match = re.search(r'_([A-Za-z0-9]{5,12})[A-Z]_', cell_name)
#         return match.group(1) if match else ""
 
#     def extract_circle_from_cell_name(cell_name):
#         match = re.match(r'([A-Z]+)_', cell_name)
#         return match.group(1) if match else "Unknown"
 
#     def parse_cell_block(content):
#         pattern = re.compile(
#             r'\d+\s+\d+ \((?P<adm_state>UNLOCKED|LOCKED)\)\s+'
#             r'\d+ \((?P<op_state>ENABLED|DISABLED)\)\s+'
#             r'(ENodeBFunction|GNBDUFunction)=\d+,(?P<cell_type>EUtranCellFDD|EUtranCellTDD|NRCellDU)=(?P<cell_name>[\w\-]+)'
#         )
#         cells = []
#         for match in pattern.finditer(content):
#             adm_state = match.group("adm_state")
#             op_state = match.group("op_state")
#             cell_name = match.group("cell_name")
#             cell_type_str = match.group("cell_type")
 
#             site_id = extract_site_id_from_cell_name(cell_name)
#             circle = extract_circle_from_cell_name(cell_name)
#             cell_type = "5G" if "NRCellDU" in cell_type_str else "4G"
 
#             cells.append({
#                 'Adm State': adm_state,
#                 'Op. State': op_state,
#                 'Cell Name': cell_name,
#                 'Site ID': site_id,
#                 'Circle': circle,
#                 'Cell Type': cell_type
#             })
#         return cells
 
#     def extract_alarms_from_alt(content, site_id="Unknown"):
#         alarms = []
#         node_id_match = re.search(r'(\S+)>[\s]*alt', content)
#         node_id = node_id_match.group(1).strip() if node_id_match else "Unknown"
 
#         ip_match = re.search(r'\d{6}-\d{2}:\d{2}:\d{2}[+|-]\d{4}\s+([a-fA-F0-9:.]+)', content)
#         ip = ip_match.group(1) if ip_match else "No IP found"
 
#         alarm_pattern = re.compile(r'''
#             ^\s*
#             (?P<dt>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})
#             \s+(?P<sev>[Mm])
#             \s+(?P<prob>.+?)
#             \s+(?P<mo>[^()]+?)
#             (?:\s*\(\s*(?P<add>.*?)\))?
#             \s*$
#         ''', re.MULTILINE | re.VERBOSE)
 
#         for m in alarm_pattern.finditer(content):
#             alarms.append({
#                 "IP": ip,
#                 "Site ID": site_id,
#                 "Node ID": node_id,
#                 "Date & Time": m.group("dt"),
#                 "Severity": m.group("sev"),
#                 "Specific Problem": m.group("prob").strip(),
#                 "MO": m.group("mo").strip(),
#                 "Additional": (m.group("add") or "").strip()
#             })
#         return alarms
 
#     all_rows = []
#     all_alarms = []
 
#     for log_file in os.listdir(log_folder):
#         log_file_path = os.path.join(log_folder, log_file)
#         with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
#             content_5g = file.read()
 
#         ip_match = re.search(r'([\w:.]+)(?=>\s*lt all)', content_5g)
#         ip_5g = ip_match.group(1) if ip_match else "No IP found"
 
#         node_match = re.search(r'([\w:-]+)(?=>\s*alt)', content_5g)
#         node_id = node_match.group(1) if node_match else "No ID found"
 
#         sync_status = extract_sync_status(content_5g)
#         cells_5g = parse_cell_block(content_5g)
 
#         for cell in cells_5g:
#             row = {
#                 ("Circle", ""): cell['Circle'],
#                 ("2G Site ID", ""): cell['Site ID'],
#                 ("5G Site ID", ""): cell['Site ID'],
#                 ("5G Node IP", ""): ip_5g,
#                 ("5G Node ID", ""): node_id,
#                 ("5G Cell Status", "Adm State"): cell['Adm State'],
#                 ("5G Cell Status", "Op. State"): cell['Op. State'],
#                 ("Cells", ""): cell['Cell Name'],
#                 ("SYNC", "Status"): sync_status,
#                 ("Cell Type", ""): cell["Cell Type"]
#             }
#             all_rows.append(row)
#             site_id = cell['Site ID']
#             alarms = extract_alarms_from_alt(content_5g, site_id)
#             all_alarms.extend(alarms)
 
#     columns = [
#         ("Circle", ""), ("2G Site ID", ""), ("5G Site ID", ""), ("5G Node IP", ""),
#         ("5G Node ID", ""), ("5G Cell Status", "Adm State"), ("5G Cell Status", "Op. State"),
#         ("Cells", ""), ("SYNC", "Status"), ("Cell Type", "")
#     ]
#     multi_index = pd.MultiIndex.from_tuples(columns)
#     df_5g = pd.DataFrame(all_rows, columns=multi_index)
#     df_5g.columns = [' - '.join(filter(None, col)).strip() for col in df_5g.columns.values]
 
#     df_alarms = pd.DataFrame(all_alarms)
 
#     if not df_alarms.empty:
#         grouped_rows = []
#         grouped = df_alarms.groupby(["IP", "Site ID", "Node ID"])
 
#         for (ip, site_id, node_id), group in grouped:
#             combined = {
#                 "IP": ip,
#                 "Site ID": site_id,
#                 "Node ID": node_id,
#                 "Date & Time": '/ '.join(group["Date & Time"].dropna().unique()),
#                 "Severity": '/ '.join(group["Severity"].dropna().unique()),
#                 "Specific Problem": '/ '.join(group["Specific Problem"].dropna().unique()),
#                 "MO": '/ '.join(group["MO"].dropna().unique()),
#                 "Additional": '/ '.join(group["Additional"].dropna().unique()),
#             }
#             grouped_rows.append(combined)
 
#         df_alarms = pd.DataFrame(grouped_rows)
#     else:
#         df_alarms = pd.DataFrame(columns=[
#             "IP", "Site ID", "Node ID", "Date & Time", "Severity",
#             "Specific Problem", "MO", "Additional"
#         ])
 
 
#     circles = sorted(set(
#         row[('Circle', '')].strip().upper().replace(" ", "_")
#         for row in all_rows if row.get(('Circle', ''))
#     ))
#     circle_name = "".join(circles) if len(circles) > 1 else circles[0]
#     output_filename = f"5G_Alarm_Logs_{circle_name}.xlsx"
#     output_path = os.path.join(MEDIA_ROOT, "Universal_alarm", output_filename)
 
#     with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
#         df_5g.to_excel(writer, index=False, sheet_name="5G Cells")
#         df_alarms.to_excel(writer, index=False, sheet_name="Alarms")
#         format_excel_sheet(writer, '5G Cells', df_5g)
#         format_excel_sheet(writer, 'Alarms', df_alarms)
 
#     relative_path = os.path.join("media", "Universal_alarm", output_filename)
#     download_link = request.build_absolute_uri("/" + relative_path.replace("\\", "/"))
 
#     print("✅ Excel saved:", output_path)
#     return Response({
#         "message": f"Report generated successfully for circle: {circle_name}",
#         "download_link": download_link,
#         "status": True
#     })
 
# ############################################################################################################################
 
 
# def delete_existing_files(upload_files):  # noqa: F811
#     for file_name in os.listdir(upload_files):
#         file_path = os.path.join(upload_files, file_name)
#         if os.path.isfile(file_path):
#             os.remove(file_path)
 
 
 
 
# @api_view(['POST'])
# def upload_4g_log_file(request):
#     if request.method != 'POST':
#         return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
   
   
   
 
#     log_files = request.FILES.getlist('log_files')
#     print("requested from the frontend:- ",log_files)
#     print("requested from the frontend:- ", request.data)
#     if not log_files:
#         return Response({"error": "4G log file must not be empty"}, status=status.HTTP_400_BAD_REQUEST)
 
#     log_folder = os.path.join(MEDIA_ROOT, "Universal_alarm", "log_files_4g")
#     os.makedirs(log_folder, exist_ok=True)
 
#     delete_existing_files(log_folder)
 
#     for file in log_files:
#         file_path = os.path.join(log_folder, file.name)
#         with open(file_path, "wb+") as destination:
#             for chunk in file.chunks():
#                 destination.write(chunk)
 
   
 
#     def get_band(cell_name):
#         band_map = {
#             "F8": "L900",
#             "F1": "L2100",
#             "F3": "L1800",
#             "T1": "L2300",
#             "T2": "L2300",
#         }
 
#         # Use regex to extract the band code from cell name (e.g., F8, F1, etc.)
#         match = re.search(r'_([FT]\d)_', cell_name)
#         if match:
#             band_code = match.group(1)
#             return band_map.get(band_code, "")
#         return ""
#     def extract_4g_sync_status(content_4g):
#         sync_ok = False
#         sync_lines = []
 
#         for line in content_4g.splitlines():
#             if "TimeSyncIO=1" in line and "1 (ENABLED)" in line:
#                 sync_ok = True
#                 sync_lines.append(line.strip())
 
#         print("🧪 Sync lines found:", sync_lines)
 
#         return "OK" if sync_ok else "NOT OK"
#     def extract_4g_site_id_from_cell_name(cell_name):
   
#         match = re.search(r'_([A-Za-z0-9]{5,12})[A-Z]_', cell_name)
#         return match.group(1) if match else ""
   
   
#     def extract_4g_circle_from_cell_name(cell_name):
#         match = re.match(r'([A-Z]+)_', cell_name)
#         return match.group(1) if match else "Unknown"
 
 
#     import re
 
 
 
#     def site_down_4g(content_4g, site_id="Unknown"):
       
#     #   def site_down_4g(content_4g, site_id="Unknown"):
#         site_down=[]
#         ip_match = re.search(
#         # r'\d{6}-\d{2}:\d{2}:\d{2}[+|-]\d{4}\s+([a-fA-F0-9:.]+)',
#          r'Logging to file .+?/([a-fA-F0-9:.]+)\.log',
       
#         content_4g)
#         ip_address = ip_match.group(1) if ip_match else "IP Not Found"
#         status = "OK" if "Checking ip contact...OK" in content_4g else "NOT OK"
       
#         site_down.append(
#             {
#                 "Status": status,
#                 "IP Address": ip_address,
           
#             }
#         )
#         return site_down
   
#     def extract_4galarms_from_alt(content, site_id="Unknown"):
#         alarms = []
 
#         # Extract Node ID
#         node_id_match = re.search(r'(\S+)>[\s]*alt', content)
#         node_id = node_id_match.group(1).strip() if node_id_match else "Unknown"
 
#         # Extract IP (IPv4 or IPv6) from line after 'alt'
#         ip_match = re.search(
#         r'\d{6}-\d{2}:\d{2}:\d{2}[+|-]\d{4}\s+([a-fA-F0-9:.]+)',
#         content)
#         ip = ip_match.group(1) if ip_match else "No IP found"
 
       
#         alarm_pattern = re.compile(r'''
#             ^\s*
#             (?P<dt>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})  
#             \s+(?P<sev>[Mm])                              
#             \s+(?P<prob>.+?)                              
#             \s+(?P<mo>[^()]+?)                            
#             (?:\s*\(\s*(?P<add>.*?)\))?                  
#             \s*$
#         ''', re.MULTILINE | re.VERBOSE)
 
#         for m in alarm_pattern.finditer(content):
#             alarms.append({
#                 "IP":               ip,
#                 "Site ID":          site_id,
#                 "Node ID":          node_id,
#                 "Date & Time":      m.group("dt"),
#                 "Severity":         m.group("sev"),
#                 "Specific Problem": m.group("prob").strip(),
#                 "MO":               m.group("mo").strip(),
#                 "Additional":       (m.group("add") or "").strip()
#             })
 
#         print(f"✅ Extracted {len(alarms)} alarms for IP: {ip}")
#         return alarms
#     ##############################################################
 
#     def extract_all_2g_trx_status(content):
#         pattern = re.compile(
#             r'GsmSector=\d+,Trx=([A-Z0-9-]+)\s+abisTsState\s+i\[\d+\]\s*=\s*[\d\s]+\(([A-Z\s]+)\)',
#             # r'GsmSector=\d+,Trx=([A-Z0-9-]+)\s+abisTsState\s+i\[\d+\]\s*=\s*[\d\s]+\(([A-Z\s]+)\)',
#             re.IGNORECASE
#         )
 
#         # trx_status_list = []
#         trx_status_dict = {}
 
#         for match in pattern.finditer(content):
#             trx_name = match.group(1)
#             raw_statuses = match.group(2).split()
 
#             # Assume majority value or just pick first (can adjust logic here)
#             # unique_statuses = set(s.upper() for s in raw_statuses)
#             unique_statuses = set(s.upper() for s in raw_statuses)
 
#             if "ENABLED" in unique_statuses:
#                 final_status = "UNLOCKED"
#             elif "DISABLED" in unique_statuses:
#                 final_status = "LOCKED"
#             elif "RESET" in unique_statuses:
#                 final_status = "DOWN"
#             else:
#                 final_status = "UNKNOWN"
 
#             # trx_status_list.append((trx_name, final_status))
#             trx_status_dict[trx_name] = final_status
#         trx_status_list = [(trx_name, status) for trx_name, status in trx_status_dict.items()]
#         # trx_status_str = "\n".join([f"{trx} - {status}" for trx, status in trx_status_dict.items()])
       
#         # trx_status_str = "\n".join(trx_status_list)
 
#         return trx_status_list
#         # print("2G TRX Status Extracted ➤", extract_all_2g_trx_status(content_4g))
       
 
#     def parse_4g_st_cell_output(content_4g):
#         pattern = re.compile(
#             r'\d+\s+\d+ \((?P<adm_state>UNLOCKED|LOCKED)\)\s+'
#             r'\d+ \((?P<op_state>ENABLED|DISABLED)\)\s+'
#             r'(ENodeBFunction|GNBDUFunction)=\d+,(?:EUtranCellFDD|EUtranCellTDD)=(?P<cell_name>[\w\-]+)'
#         )
 
#         cells= []
#         for match in pattern.finditer(content_4g):
#             cell_name = match.group("cell_name")
#             adm_state = match.group("adm_state")
#             op_state = match.group("op_state")
#             circle =  extract_4g_circle_from_cell_name(cell_name)
#             site_id = extract_4g_site_id_from_cell_name(cell_name)
 
#             band = get_band(cell_name)
#             print(f"📡 Cell Name: {cell_name} ➤ 🏷️ Site ID: {site_id} ")
#             cells.append({
#                 ("4G Cell Status", "Adm State"): adm_state,
#                 ("4G Cell Status", "Op. State"): op_state,
#                 # ("Cells", ""): cell_name,
#                 # ("Circle", ""): circle,
#                 # ("Site ID", ""): site_id,
#                 # ("BAND", ""): [get_band(cell) for cell in cell_name],
#                 # ("Band", ""): band,
#                 # 'Adm State': adm_state,
#                 # 'Op. State': op_state,
#                 'Cell Name': cell_name,
#                 'Site ID': site_id,
#                 'Circle': circle,
#                 'Band': band
#             })
#         return cells
#     all_rows = []
#     all_alarms = []
#     site_down = []
#     for log_file in os.listdir(log_folder):
#         log_file_path = os.path.join(log_folder, log_file)
#         with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
#             content_4g = file.read()
#         ip_match = re.search(r'([\w:.]+)(?=>\s*lt all)', content_4g)
#         ip_4g = ip_match.group(1) if ip_match else "No IP found"
 
#         node_match = re.search(r'([\w:-]+)(?=>\s*alt)', content_4g)
#         node_id = node_match.group(1) if node_match else "No ID found"
 
#         sync_status = extract_4g_sync_status(content_4g)
#         cells_4g = parse_4g_st_cell_output(content_4g)
#         trx_status_list = extract_all_2g_trx_status(content_4g)
#         trx_status_str = "; ".join([f"{trx} - {status}" for trx, status in trx_status_list])
#         for cell in cells_4g:
#             row = {
#                 ('Circle', ''): cell['Circle'],
#                 ('2G Site ID', ''): cell['Site ID'],
#                 ('4G Site ID', ''): cell['Site ID'],  # Assuming naming rule
#                 ('4G Node IP', ''): ip_4g,
#                 ('4G Node ID', ''): node_id,
#                 ('4G Cell Status', 'Adm State'): cell[('4G Cell Status', 'Adm State')],
#                 ('4G Cell Status', 'Op. State'): cell[('4G Cell Status', 'Op. State')],
#                 ('Cells', ''): cell['Cell Name'],
#                 # ('2G Cell(TRX) Status', ''): [extract_all_2g_trx_status(content_4g)] ,
#                 ("2G Cell(TRX) Status", "Status"): trx_status_str,
#                 # ('2G Cell(TRX) Status', ''): "; ".join([f"{trx} - {status}" for trx, status in extract_all_2g_trx_status(content_4g)]),
#                 ('SYNC', 'Status'): sync_status,  
#                 ('Band', ''): cell['Band']
#             }
#             all_rows.append(row)
 
#         for cell in cells_4g:
#             site_id = cell['Site ID']
#             alarms = extract_4galarms_from_alt(content_4g, site_id)
#             all_alarms.extend(alarms)
#             site_down.extend(site_down_4g(content_4g, site_id))
 
#     columns = [
#         ("Circle", ""),
#         ("2G Site ID", ""),
#         ("4G Site ID", ""),
#         ("4G Node IP", ""),
#         ("4G Node ID", ""),
#         ("4G Cell Status", "Adm State"),
#         ("4G Cell Status", "Op. State"),
#         ("Cells", ""),
#         ("2G Cell(TRX) Status", "Status"),
#         ("SYNC", "Status"),
#         ("Band", ""),
#     ]
#     multi_index = pd.MultiIndex.from_tuples(columns)
#     df_4g = pd.DataFrame(all_rows, columns=multi_index)
 
# # ❗ Flatten before saving to Excel
#     df_4g.columns = [' - '.join(filter(None, col)).strip() for col in df_4g.columns.values]
 
# # Alarm sheet
#     if all_alarms:
#         alarm_df = pd.DataFrame(all_alarms)
       
#         # Group by IP + Site ID + Node ID and merge columns
#         agg_alarms = alarm_df.groupby(["IP", "Site ID", "Node ID"]).agg({
#             "Date & Time": lambda x: "/ ".join(sorted(set(x))),
#             "Severity": lambda x: "/ ".join(sorted(set(x))),
#             "Specific Problem": lambda x: "/".join(sorted(set(x))),
#             "MO": lambda x: "/".join(sorted(set(x))),
#             "Additional": lambda x: "/".join(sorted(set(filter(None, x))))
#         }).reset_index()
#         df_alarms = agg_alarms
#     else:
#         df_alarms = pd.DataFrame()
#     site_down_df = pd.DataFrame(site_down).drop_duplicates()
 
#     circles = sorted(set(
#     row[('Circle', '')].strip().upper().replace(" ", "_")
#     for row in all_rows if row.get(('Circle', ''))
#     ))
 
#         # Join all circle names (like TNCH or TN_ORI_CH)
#     circle_name = "".join(circles) if len(circles) > 1 else circles[0]
#     output_filename = f"4G_Alarm_Logs_{circle_name}.xlsx"
#     output_path = os.path.join(MEDIA_ROOT, "Universal_alarm", output_filename)
#     ##################################
#     # with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
#     with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
#         df_4g.to_excel(writer, index=False, sheet_name="4G Cells")
#         df_alarms.to_excel(writer, index=False, sheet_name="Alarms")
#         site_down_df.to_excel(writer, sheet_name="Site Down", index=False)
#         format_excel_sheet(writer, 'Alarms', df_alarms ,)
 
#     relative_path = os.path.join("media", "Universal_alarm", output_filename)
#     download_link = request.build_absolute_uri("/" + relative_path.replace("\\", "/"))
 
#     wb = load_workbook(output_path)
#     ws = wb.active
#     for sheet_name in wb.sheetnames:
#         ws = wb["4G Cells"]
 
#         header_fill = PatternFill(start_color="259aa8", end_color="4682B4", fill_type="solid")
#         header_font = Font(color="FFFFFF", bold=True)
#         header_align = Alignment(horizontal="center", vertical="center")
 
#         thin_border = Border(
#             left=Side(style='thin'), right=Side(style='thin'),
#             top=Side(style='thin'), bottom=Side(style='thin')
#         )
#         prev_value = None
#         start_col = 1
#         for col in range(1, ws.max_column + 1):
#             top_cell = ws.cell(row=1, column=col)
#             sub_cell = ws.cell(row=2, column=col)
#             top_val = top_cell.value
#             sub_val = sub_cell.value  # noqa: F841
#             # Detect merged header range
#             if top_val != prev_value:
#                 if col > start_col:
#                     if prev_value not in (None, ""):
#                         ws.merge_cells(
#                             start_row=1, start_column=start_col,
#                             end_row=1, end_column=col - 1
#                         )
#                 start_col = col
#                 prev_value = top_val
#         # Final merge for last group
#         if prev_value not in (None, "") and start_col <= ws.max_column:
#             ws.merge_cells(
#                 start_row=1, start_column=start_col,
#                 end_row=1, end_column=ws.max_column
#             )
#         # Styling headers
#         for row in [1, 1]:
#             for col in range(1, ws.max_column + 1):
#                 cell = ws.cell(row=row, column=col)
#                 cell.fill = header_fill
#                 cell.font = header_font
#                 cell.alignment = header_align
#                 cell.border = thin_border
#         # Style entire data range
#         for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
#             for cell in row:
#                 cell.border = thin_border
#         wb.save(output_path)
#         print("✅ Excel saved:", output_path)
#     return Response({
#         # "message": "4G log file processed successfully",
#         "message": f"Report generated successfully for circle: {circle_name}",
#         "download_link": download_link,
#         "status": True
#     }, status=200)