from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Border, Font, Alignment, Side
from rest_framework.response import Response
from rest_framework.decorators import api_view
import os
import re
import pandas as pd
import numpy as np
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
from rest_framework import status
import shutil
from datetime import datetime
from Alarm_old_new_Tool.tasks import send_email_for_Alarm

def format_excel_sheet(writer, sheet_name, df, startrow=0, startcol=0):
    """
    Format an Excel sheet using xlsxwriter:
    - Custom header colors for New/Old columns
    - Conditional formatting for OK/NOT OK/Missing
    - Centered alignment
    - Auto column widths
    """
    workbook = writer.book
    worksheet = writer.sheets.get(sheet_name)
    if worksheet is None:
        return

    # Default header format
    default_header_format = workbook.add_format(
        {
            "bold": True,
            "bg_color": "#000957",
            "border": 1,
            "font_color": "#ffffff",
            "align": "center",
            "valign": "vcenter",
        }
    )

    # Cell formats
    center_format = workbook.add_format({"align": "center", "valign": "vcenter", "border": 0})
    # ok_format = workbook.add_format({"bg_color": "#90EE90", "font_color": "#000000", "align": "center", "valign": "vcenter"})
    # not_ok_format = workbook.add_format({"bg_color": "#FF0000", "font_color": "#FFFFFF", "align": "center", "valign": "vcenter"})
    missing_format = workbook.add_format({"bg_color": "#FF6347", "font_color": "#FFFFFF", "align": "center", "valign": "vcenter"})

    # Header row height
    worksheet.set_row(startrow, 23)

    # Write headers with New/Old coloring
    for col_num, col_name in enumerate(df.columns):
        col_lower = str(col_name).lower()
        if "_new" in col_lower:
            header_format = workbook.add_format(
                {
                    "bold": True,
                    "bg_color": "#F79646",  # Green
                    "border": 1,
                    "font_color": "#ffffff",
                    "align": "center",
                    "valign": "vcenter",
                }
            )
        elif "_old" in col_lower:
            header_format = workbook.add_format(
                {
                    "bold": True,
                    "bg_color": "#4F81BD",  # Blue
                    "border": 1,
                    "font_color": "#ffffff",
                    "align": "center",
                    "valign": "vcenter",
                }
            )
        else:
            header_format = default_header_format

        worksheet.write(startrow, startcol + col_num, str(col_name), header_format)

    # Set column widths based on max content
    for col_num, col_name in enumerate(df.columns):
        col_series = df[col_name].astype(str).fillna("")
        max_length = max(col_series.str.len().max(), len(str(col_name))) if len(col_series) > 0 else len(str(col_name))
        max_length = min(max_length, 255)
        worksheet.set_column(startcol + col_num, startcol + col_num, max_length + 5)

    # Write data rows with conditional formatting
    for row_idx in range(len(df)):
        worksheet.set_row(startrow + row_idx + 1, 15)  # Row height
        for col_idx in range(len(df.columns)):
            cell_value = str(df.iat[row_idx, col_idx])
            style = center_format
            # if cell_value == "OK":
            #     style = ok_format
            # elif cell_value == "NOT OK":
            #     style = not_ok_format
            if cell_value == "Missing":
                style = missing_format
            worksheet.write(startrow + row_idx + 1, startcol + col_idx, cell_value, style)



def delete_existing_files(folder_path):
    """Remove all files inside folder_path (not the folder itself)."""
    if not os.path.exists(folder_path):
        return
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            
# Prepare folders---
base_folder = os.path.join(MEDIA_ROOT, "Alarm_New_Old_Data")       
os.makedirs(base_folder, exist_ok=True)     

#function and process logic for 4g logs for new and old----------------------------------------------------------------------------------------
def get_band(cell_name):
    band_map = {
        "F8": "L900",
        "F1": "L2100",
        "F3": "L1800",
        "T1": "L2300",
        "T2": "L2300",
    }
    match = re.search(r'_([FT]\d)_', cell_name)
    if match:
        return band_map.get(match.group(1), "")
    return ""


def extract_4g_sync_status(content_4g):
    sync_ok = False
    for line in content_4g.splitlines():
        if "TimeSyncIO=1" in line and "1 (ENABLED)" in line:
            sync_ok = True
            break
    return "OK" if sync_ok else "NOT OK"


def extract_4g_site_id_from_cell_name(cell_name):
    match = re.search(r'_([A-Za-z0-9]{5,12})[A-Z]_', cell_name)
    return match.group(1) if match else ""


def extract_4g_circle_from_cell_name(cell_name):
    match = re.match(r'([A-Z]+)_', cell_name)
    return match.group(1) if match else "Unknown"


def site_down_4g(content_4g):
    ip_match = re.search(r'Logging to file .+?/([a-fA-F0-9:.]+)\.log', content_4g)
    ip_address = ip_match.group(1) if ip_match else "IP Not Found"
    status = "OK" if "Checking ip contact...OK" in content_4g else "NOT OK"
    return {"Status": status, "IP Address": ip_address}




def extract_4galarms_from_alt(content, site_id="Unknown"):
    alarms = []
    
    node_id_match = re.search(r'(\S+)>[\s]*altk', content)
    node_id = node_id_match.group(1).strip() if node_id_match else "NA"
    site=node_id[1:] if node_id.startswith('L') else node_id
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
            "Site ID": site,
            "Node ID": node_id,
            "Date & Time": m.group("dt"),
            "Severity": m.group("sev"),
            "Specific Problem": m.group("prob").strip(),
            "MO": m.group("mo").strip(),
            "Additional": (m.group("add") or "").strip()
        })
    return alarms


def extract_all_2g_trx_status(content):
    pattern = re.compile(
        r'GsmSector=\d+,Trx=([A-Z0-9-]+)\s+abisTsState\s+i\[\d+\]\s*=\s*[\d\s]+\(([A-Z\s]+)\)',
        re.IGNORECASE
    )
    trx_status_dict = {}
    for match in pattern.finditer(content):
        trx_name = match.group(1)
        raw_statuses = match.group(2).split()
        unique_statuses = set(s.upper() for s in raw_statuses)
        if "ENABLED" in unique_statuses:
            final_status = "UNLOCKED"
        elif "DISABLED" in unique_statuses:
            final_status = "LOCKED"
        elif "RESET" in unique_statuses:
            final_status = "DOWN"
        else:
            final_status = "UNKNOWN"
        trx_status_dict[trx_name] = final_status
    return [(trx, status) for trx, status in trx_status_dict.items()]


def parse_4g_st_cell_output(content_4g):
    """
    Returns list of dicts: each dict contains Cell Name, Site ID, Circle, Band, Adm State, Op. State
    """
    pattern = re.compile(
        r'\d+\s+\d+ \((?P<adm_state>UNLOCKED|LOCKED)\)\s+'
        r'\d+ \((?P<op_state>ENABLED|DISABLED)\)\s+'
        r'(?:ENodeBFunction|GNBDUFunction)=\d+,(?:EUtranCellFDD|EUtranCellTDD|NRCellCU)=(?P<cell_name>[\w\-\:]+)',
        re.IGNORECASE
    )

    cells = []
    for match in pattern.finditer(content_4g):
        cell_name = match.group("cell_name")
        adm_state = match.group("adm_state")
        op_state = match.group("op_state")
        circle = extract_4g_circle_from_cell_name(cell_name)
        site_id = extract_4g_site_id_from_cell_name(cell_name)
        band = get_band(cell_name)
        cells.append({
            "Cell Name": cell_name,
            "Site ID": site_id,
            "site" : re.sub(r'^[A-Z]+', '', site_id),
            "Circle": circle,
            "Band": band,
            "Adm State": adm_state,
            "Op. State": op_state
        })
    return cells



def process_log_files(saved_files_folder):
   
    rows = []
    alarms = []
    site_down_list = []

    for filename in os.listdir(saved_files_folder):
        file_path = os.path.join(saved_files_folder, filename)
        if not os.path.isfile(file_path):
            continue

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as fh:
            content = fh.read()

        # ip/node fallback extraction
        ip_match = re.search(r'([\w:.]+)(?=>\s*lt all)', content)
        ip_addr = ip_match.group(1) if ip_match else "No IP found"

        node_match = re.search(r'([\w:-]+)(?=>\s*alt)', content)
        node_id = node_match.group(1) if node_match else "No ID found"

        plmm_status = {}
        # extract plmnr cellwise
        pattern_plm = re.compile(r"(EUtranCellFDD=\S+|EUtranCellTDD=\S+|NRCellCU=\S+).*?\s(true|false)", re.IGNORECASE)
        for m in pattern_plm.finditer(content):
            mo = m.group(1).strip()
            value = m.group(2).lower()
            if mo not in plmm_status:
                plmm_status[mo] = []
            plmm_status[mo].append(value)
        for mo in list(plmm_status.keys()):
            plmm_status[mo] = "true" if "true" in plmm_status[mo] else "false"

        sync_status = extract_4g_sync_status(content)
        cells = parse_4g_st_cell_output(content)
        trx_status_list = extract_all_2g_trx_status(content)
        trx_status_str = "; ".join([f"{trx} - {status}" for trx, status in trx_status_list]) if trx_status_list else ""

        for cell in cells:
            cell_name = cell["Cell Name"]
            possible_keys = [f"EUtranCellFDD={cell_name}", f"EUtranCellTDD={cell_name}", f"NRCellCU={cell_name}"]
            plmm_value = "NA"
            for k in possible_keys:
                if k in plmm_status:
                    plmm_value = plmm_status[k]
                    break

            row = {
                "Circle": cell.get("Circle", ""),
                "Site ID": cell.get("site", ""),
                "2G Site ID": cell.get("Site ID", ""),
                "4G Site ID": cell.get("Site ID", ""),
                "4G Node IP": ip_addr,
                "4G Node ID": node_id,
                "4G Cell Status - Adm State": cell.get("Adm State", ""),
                "4G Cell Status - Op. State": cell.get("Op. State", ""),
                "Cells": cell_name,
                "PLMNR Status": plmm_value,
                "2G Cell(TRX) Status": trx_status_str,
                "SYNC Status": sync_status,
                "Band": cell.get("Band", ""),
            }
            rows.append(row)

        # alarms for this file
        alarms_for_file = extract_4galarms_from_alt(content, site_id="Unknown")
        for a in alarms_for_file:
         alarms.extend(alarms_for_file)

        # site down info
        site_down_list.append(site_down_4g(content))

    return rows, alarms, site_down_list


@api_view(['POST'])
def upload_4g_new_old(request):
    circle = request.POST.get("circle")
    if not circle:
        return Response({"error": "circle not found in input"}, status=status.HTTP_400_BAD_REQUEST)

    old_files = request.FILES.getlist('old_logs')
    new_files = request.FILES.getlist('new_logs')

    if not old_files and not new_files:
        return Response({"error": "No files uploaded in old_logs or new_logs"}, status=status.HTTP_400_BAD_REQUEST)
    
    site_file = request.FILES.get('site_file')
    if not site_file:
        return Response({"error": "Site file is required for 4G logs"}, status=status.HTTP_400_BAD_REQUEST)

    # Read mapping file (OldSite - NewSite)
    site_mapping_df = pd.read_excel(site_file, engine='openpyxl', usecols=["OldSite", "NewSite"])
    site_mapping_df["OldSite"] = site_mapping_df["OldSite"].astype(str).str.replace(r"\.0$", "", regex=True)
    site_mapping_df["NewSite"] = site_mapping_df["NewSite"].astype(str).str.replace(r"\.0$", "", regex=True)

    # Setup folders
    output_folder = os.path.join(base_folder, "output_4g")
    log_folder = os.path.join(base_folder, "log_files_4g")
    old_folder = os.path.join(log_folder, "old_logs")
    new_folder = os.path.join(log_folder, "new_logs")
     
    os.makedirs(log_folder, exist_ok=True)
    os.makedirs(old_folder, exist_ok=True)
    os.makedirs(new_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    delete_existing_files(old_folder)
    delete_existing_files(new_folder)

    # Save uploaded logs
    for f in old_files:
        with open(os.path.join(old_folder, f.name), "wb+") as dest:
            for chunk in f.chunks():
                dest.write(chunk)

    for f in new_files:
        with open(os.path.join(new_folder, f.name), "wb+") as dest:
            for chunk in f.chunks():
                dest.write(chunk)

    # Process log files
    if os.listdir(old_folder):
        rows_old, alarms_old, site_down_old = process_log_files(old_folder)
    else:
        rows_old, alarms_old, site_down_old = [], [], []

    if os.listdir(new_folder):
        rows_new, alarms_new, site_down_new = process_log_files(new_folder)
    else:
        rows_new, alarms_new, site_down_new = [], [], []

    df_old = pd.DataFrame(rows_old)
    df_new = pd.DataFrame(rows_new)

    # Filter logs by Site IDs in mapping file
    if not df_old.empty:
        df_old["Site ID"] = df_old["Site ID"].astype(str).str.replace(r"\.0$", "", regex=True)
        df_old = df_old[df_old["Site ID"].isin(site_mapping_df["OldSite"])]

    if not df_new.empty:
        df_new["Site ID"] = df_new["Site ID"].astype(str).str.replace(r"\.0$", "", regex=True)
        df_new = df_new[df_new["Site ID"].isin(site_mapping_df["NewSite"])]

    # Merge site mapping to logs
    if not df_old.empty:
        df_old = df_old.merge(site_mapping_df, how='left', left_on="Site ID", right_on="OldSite")
    if not df_new.empty:
        df_new = df_new.merge(site_mapping_df, how='left', left_on="Site ID", right_on="NewSite")

    # Add suffix for clarity
    if not df_old.empty:
        df_old = df_old.add_suffix("_old")
    if not df_new.empty:
        df_new = df_new.add_suffix("_new")

    # Merge old and new logs side by side using mapping
    if not df_old.empty and not df_new.empty:
        df_combined = pd.merge(
            df_old, df_new,
            left_on="NewSite_old", right_on="NewSite_new",
            how="outer"
        )
    elif not df_old.empty:
        df_combined = df_old.copy()
    else:
        df_combined = df_new.copy()
    print(df_combined)

    # Alarms
    df_alarms_old = pd.DataFrame(alarms_old)
    df_alarms_new = pd.DataFrame(alarms_new)
    if not df_alarms_old.empty:
        df_alarms_old = df_alarms_old.add_suffix("_old")
    if not df_alarms_new.empty:
        df_alarms_new = df_alarms_new.add_suffix("_new")

    if not df_alarms_old.empty and not df_alarms_new.empty:
        df_alarms = pd.concat([df_alarms_old, df_alarms_new], axis=1)
    elif not df_alarms_old.empty:
        df_alarms = df_alarms_old.copy()
    else:
        df_alarms = df_alarms_new.copy()

    # Site Down
    df_site_down_old = pd.DataFrame(site_down_old).drop_duplicates()
    df_site_down_new = pd.DataFrame(site_down_new).drop_duplicates()
    if not df_site_down_old.empty:
        df_site_down_old = df_site_down_old.add_suffix("_old")
    if not df_site_down_new.empty:
        df_site_down_new = df_site_down_new.add_suffix("_new")

    if not df_site_down_old.empty and not df_site_down_new.empty:
        df_site_down = pd.concat([df_site_down_old, df_site_down_new], axis=1)
    elif not df_site_down_old.empty:
        df_site_down = df_site_down_old.copy()
    else:
        df_site_down = df_site_down_new.copy()

    # Clean data
    for df_var in ["df_combined", "df_alarms", "df_site_down"]:
        if df_var in locals():
            df = locals()[df_var]
            if not df.empty:
                df.replace({pd.NA: None, np.nan: None}, inplace=True)
                df.fillna("", inplace=True)

    # Create output Excel
    circle_folder = os.path.join(output_folder, circle)
    if os.path.exists(circle_folder):
        shutil.rmtree(circle_folder)
    os.makedirs(circle_folder, exist_ok=True)

    output_filename = f"4G_Alarm_Logs_{circle}.xlsx"
    output_path = os.path.join(circle_folder, output_filename)

    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        if not df_combined.empty:
            df_combined.to_excel(writer, index=False, sheet_name="Status")
            format_excel_sheet(writer, "Status", df_combined)
        if not df_alarms.empty:
            df_alarms.to_excel(writer, index=False, sheet_name="Alarms")
            format_excel_sheet(writer, "Alarms", df_alarms)
        if not df_site_down.empty:
            df_site_down.to_excel(writer, index=False, sheet_name="Site Down")
            format_excel_sheet(writer, "Site Down", df_site_down)

    # Email send
    send_email_for_Alarm(df_combined,output_path)
    print("Email sent successfully")

    # Build download URL
    relative_path = os.path.join(MEDIA_URL.strip("/"), "Alarm_New_Old_Data", "output_4g", circle, output_filename)
    download_url = request.build_absolute_uri("/" + relative_path.replace("\\", "/"))

    print("----- End of 4G Logs Processing -----")

    return Response({
        "status": True,
        "message": "4G Logs Processed Successfully",
        "download_url": download_url,
    }, status=status.HTTP_200_OK)

    
    #End process of 4g logs----------------------------------------------------------------------------------------
    
    
    
    
    
#function and process logic for 5g logs for new and old----------------------------------------------------------------------------------------
# ---------- 5G processing code (aligned with your 4G view) ----------

import os
import re
import shutil
import numpy as np
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

# Helper: extract sync
def extract_5g_sync_status(content):
    sync_ok = False
    for line in content.splitlines():
        if "TimeSyncIO=1" in line and "1 (ENABLED)" in line:
            sync_ok = True
            break
    return "OK" if sync_ok else "NOT OK"

# Extract site id and circle from cell name (keeps same rules as 4G)
def extract_5g_site_id_from_cell_name(cell_name):
    match = re.search(r'_([A-Za-z0-9]{5,12})[A-Z]_', cell_name)
    return match.group(1) if match else ""

def extract_5g_circle_from_cell_name(cell_name):
    match = re.match(r'([A-Z]+)_', cell_name)
    return match.group(1) if match else "Unknown"

# Site-down detection for 5G (similar approach as 4G)
def site_down_5g(content_5g):
    ip_match = re.search(r'Logging to file .+?/([a-fA-F0-9:.]+)\.log', content_5g)
    ip_address = ip_match.group(1) if ip_match else "IP Not Found"
    status = "OK" if "Checking ip contact...OK" in content_5g else "NOT OK"
    return {"Status": status, "IP Address": ip_address}

# Parse cell blocks in 5G log - support NRCellDU and fallback to EUtranCell* if present
def parse_5g_cell_block(content):
    """
    Returns list of dicts: 'Cell Name','Site ID','site','Circle','Adm State','Op. State','Cell Type'
    Pattern chosen to mirror your 4G parser but include NRCellDU detection.
    """
    pattern = re.compile(
        r'\d+\s+\d+ \((?P<adm_state>UNLOCKED|LOCKED)\)\s+'  # adm state
        r'\d+ \((?P<op_state>ENABLED|DISABLED)\)\s+'        # op state
        r'(?:GNBDUFunction|ENodeBFunction)=\d+,'            # function id segment
        r'(?P<cell_type>NRCellDU|EUtranCellFDD|EUtranCellTDD)=(?P<cell_name>[\w\-\:]+)',  # cell
        re.IGNORECASE
    )

    cells = []
    for match in pattern.finditer(content):
        adm_state = match.group("adm_state")
        op_state = match.group("op_state")
        cell_name = match.group("cell_name")
        cell_type_str = match.group("cell_type")

        site_id = extract_5g_site_id_from_cell_name(cell_name)
        circle = extract_5g_circle_from_cell_name(cell_name)
        cell_type = "5G" if "NRCellDU" in cell_type_str.upper() else "4G"

        cells.append({
            "Cell Name": cell_name,
            "Site ID": site_id,
            "site": re.sub(r'^[A-Z]+', '', site_id),
            "Circle": circle,
            "Adm State": adm_state,
            "Op. State": op_state,
            "Cell Type": cell_type
        })
    return cells

# Extract alarms from 'alt' output for 5G (mirrors 4G alarm regex)
def extract_5g_alarms_from_alt(content, site_id="Unknown"):
    alarms = []

    node_id_match = re.search(r'(\S+)>[\s]*alt', content)
    node_id = node_id_match.group(1).strip() if node_id_match else "NA"

    # timestamp + IP pattern similar to 4G
    ip_match = re.search(r'\d{6}-\d{2}:\d{2}:\d{2}[+\-]\d{4}\s+([a-fA-F0-9:.]+)', content)
    ip = ip_match.group(1) if ip_match else "No IP found"

    alarm_pattern = re.compile(r'''
        ^\s*
        (?P<dt>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})   # datetime
        \s+(?P<sev>[A-Za-z])                            # single-letter severity
        \s+(?P<prob>.+?)                                # problem text (non-greedy)
        \s+(?P<mo>[^()]+?)                              # managed object text
        (?:\s*\(\s*(?P<add>.*?)\))?                     # optional additional
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

# Process all 5G log files in a folder (returns rows, alarms, site_down_list)
def process_5g_log_files(saved_folder):
    rows = []
    alarms = []
    site_down_list = []

    for fname in os.listdir(saved_folder):
        fpath = os.path.join(saved_folder, fname)
        if not os.path.isfile(fpath):
            continue
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as fh:
            content = fh.read()

        # ip/node fallback extraction (same approach as 4G)
        ip_match = re.search(r'([\w:.]+)(?=>\s*lt all)', content)
        ip_5g = ip_match.group(1) if ip_match else "No IP found"

        node_match = re.search(r'([\w:-]+)(?=>\s*alt)', content)
        node_id = node_match.group(1) if node_match else "No ID found"

        sync = extract_5g_sync_status(content)
        cells = parse_5g_cell_block(content)

        # build rows for each cell found

        for cell in cells:
            row = {
                "Circle": cell.get("Circle", ""),
                "2G Site ID": cell.get("Site ID", ""),
                "5G Site ID": cell.get("Site ID", ""),
                "5G Node IP": ip_5g,
                "5G Node ID": node_id,
                "5G Cell Status - Adm State": cell.get("Adm State", ""),
                "5G Cell Status - Op. State": cell.get("Op. State", ""),
                "Cells": cell.get("Cell Name", ""),
                "SYNC Status": sync,
                "Cell Type": cell.get("Cell Type", "")
            }
            rows.append(row)

        # alarms: attempt to attach by site ids present in file, fallback to "Unknown"
        site_ids = [cell.get("Site ID") for cell in cells if cell.get("Site ID")]
        if site_ids:
            for sid in site_ids:
                alarms_for_file = extract_5g_alarms_from_alt(content, site_id=sid)
                if alarms_for_file:
                    alarms.extend(alarms_for_file)
        else:
            alarms_for_file = extract_5g_alarms_from_alt(content, site_id="Unknown")
            if alarms_for_file:
                alarms.extend(alarms_for_file)

        # site down info
        site_down_list.append(site_down_5g(content))

    return rows, alarms, site_down_list

# ---------- 5G Upload View (mirrors upload_4g_new_old) ----------
@api_view(['POST'])
def upload_5g_new_old(request):
    circle = request.POST.get("circle")
    if not circle:
        return Response({"error": "Circle not provided"}, status=status.HTTP_400_BAD_REQUEST)

    old_files = request.FILES.getlist('old_logs')
    new_files = request.FILES.getlist('new_logs')
    site_file = request.FILES.get('site_file')
    if not site_file:
        return Response({"error": "Site file is required for 5G logs"}, status=status.HTTP_400_BAD_REQUEST)

    # Read site mapping
    try:
        site_mapping_df = pd.read_excel(site_file, engine='openpyxl', usecols=["OldSite", "NewSite"])
    except Exception as e:
        return Response({"error": f"Error reading site file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    # Normalize mapping columns
    for col in ["OldSite", "NewSite"]:
        site_mapping_df[col] = site_mapping_df[col].astype(str).str.strip().str.upper().str.replace(r"\.0$", "", regex=True)

    # Prepare folders
    output_folder = os.path.join(base_folder, "output_5g")
    log_folder = os.path.join(base_folder, "log_files_5g")
    old_folder = os.path.join(log_folder, "old_logs")
    new_folder = os.path.join(log_folder, "new_logs")

    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(old_folder, exist_ok=True)
    os.makedirs(new_folder, exist_ok=True)

    delete_existing_files(old_folder)
    delete_existing_files(new_folder)

    # save uploaded logs
    def save_files(file_list, target_folder):
        for f in file_list:
            file_path = os.path.join(target_folder, f.name)
            with open(file_path, "wb+") as dest:
                for chunk in f.chunks():
                    dest.write(chunk)

    save_files(old_files, old_folder)
    save_files(new_files, new_folder)

    # Process log files
    if os.listdir(old_folder):
        rows_old, alarms_old, site_down_old = process_5g_log_files(old_folder)
    else:
        rows_old, alarms_old, site_down_old = [], [], []

    if os.listdir(new_folder):
        rows_new, alarms_new, site_down_new = process_5g_log_files(new_folder)
    else:
        rows_new, alarms_new, site_down_new = [], [], []

    df_old = pd.DataFrame(rows_old)
    df_new = pd.DataFrame(rows_new)
    
    # Filter logs by Site IDs in mapping file (normalize column names)
    if not df_old.empty:
        df_old["Site ID"] = (df_old["5G Site ID"].astype(str).str.strip().str.upper().str.replace(r"\.0$", "", regex=True).str.replace(r"^X+", "", regex=True))
        df_old = df_old[df_old["Site ID"].isin(site_mapping_df["OldSite"])]

    if not df_new.empty:
        df_new["Site ID"] = df_new["5G Site ID"].astype(str).str.strip().str.upper().str.replace(r"\.0$", "", regex=True).str.replace(r"^X+", "", regex=True)
        df_new = df_new[df_new["Site ID"].isin(site_mapping_df["NewSite"])]

    # Merge site mapping to logs
    if not df_old.empty:
        df_old = df_old.merge(site_mapping_df, how='left', left_on="Site ID", right_on="OldSite")
        df_old.drop_duplicates(inplace=True)
    if not df_new.empty:
        df_new = df_new.merge(site_mapping_df, how='left', left_on="Site ID", right_on="NewSite")
        df_new.drop_duplicates(inplace=True)
    

    # Add suffix for clarity (keeps same approach as 4G view)
    if not df_old.empty:
        df_old = df_old.add_suffix("_old")
    if not df_new.empty:
        df_new = df_new.add_suffix("_new")

    # Merge old and new logs side by side using mapping
    if not df_old.empty and not df_new.empty:
        df_combined_5g = pd.merge(
            df_old, df_new,
            left_on="NewSite_old", right_on="NewSite_new",
            how="outer"
        )

        df_combined_5g.drop_duplicates(inplace=True)

    elif not df_old.empty:
        df_combined_5g = df_old.copy()
    else:
        df_combined_5g = df_new.copy()

    # Alarms
    df_alarms_old = pd.DataFrame(alarms_old).add_suffix("_old") if alarms_old else pd.DataFrame()
    df_alarms_new = pd.DataFrame(alarms_new).add_suffix("_new") if alarms_new else pd.DataFrame()

    if not df_alarms_old.empty and not df_alarms_new.empty:
        df_alarms = pd.concat([df_alarms_old, df_alarms_new], axis=1)
    elif not df_alarms_old.empty:
        df_alarms = df_alarms_old.copy()
    else:
        df_alarms = df_alarms_new.copy()

    # Site Down
    df_site_down_old = pd.DataFrame(site_down_old).drop_duplicates() if site_down_old else pd.DataFrame()
    df_site_down_new = pd.DataFrame(site_down_new).drop_duplicates() if site_down_new else pd.DataFrame()
    if not df_site_down_old.empty:
        df_site_down_old = df_site_down_old.add_suffix("_old")
    if not df_site_down_new.empty:
        df_site_down_new = df_site_down_new.add_suffix("_new")

    if not df_site_down_old.empty and not df_site_down_new.empty:
        df_site_down = pd.concat([df_site_down_old, df_site_down_new], axis=1)
    elif not df_site_down_old.empty:
        df_site_down = df_site_down_old.copy()
    else:
        df_site_down = df_site_down_new.copy()

    print("5G DataFrames prepared",df_combined_5g)
    # Clean dataframes
    for df in [df_combined_5g, df_alarms, df_site_down]:
        if isinstance(df, pd.DataFrame) and not df.empty:
            df.replace({pd.NA: None, np.nan: None}, inplace=True)
            df.fillna("", inplace=True)

    # Create output excel (same behavior as 4G)
    circle_folder = os.path.join(output_folder, circle)
    if os.path.exists(circle_folder):
        shutil.rmtree(circle_folder)
    os.makedirs(circle_folder, exist_ok=True)

    output_filename = f"5G_Alarm_Logs_{circle}.xlsx"
    output_path = os.path.join(circle_folder, output_filename)

    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        if isinstance(df_combined_5g, pd.DataFrame) and not df_combined_5g.empty:
            df_combined_5g.to_excel(writer, index=False, sheet_name="Status")
            format_excel_sheet(writer, "Status", df_combined_5g)
        if isinstance(df_alarms, pd.DataFrame) and not df_alarms.empty:
            df_alarms.to_excel(writer, index=False, sheet_name="Alarms")
            format_excel_sheet(writer, "Alarms", df_alarms)
        if isinstance(df_site_down, pd.DataFrame) and not df_site_down.empty:
            df_site_down.to_excel(writer, index=False, sheet_name="Site Down")
            format_excel_sheet(writer, "Site Down", df_site_down)

    # optionally send email (same helper as 4G)
    try:
        send_email_for_Alarm(df_combined_5g)
    except Exception:
        # avoid crashing the response if email fails; log/print for debugging
        print("Warning: send_email_for_Alarm failed for 5G. Check email helper.")

    # Build download URL
    relative_path = os.path.join(MEDIA_URL.strip("/"), "Alarm_New_Old_Data", "output_5g", circle, output_filename)
    download_url = request.build_absolute_uri("/" + relative_path.replace("\\", "/"))

    return Response({
        "status": True,
        "message": "5G Logs Processed Successfully",
        "download_url": download_url,
    }, status=status.HTTP_200_OK)
