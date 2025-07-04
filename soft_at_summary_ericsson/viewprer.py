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
import datetime
import xlsxwriter

from mcom_website.settings import MEDIA_ROOT, MEDIA_URL

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
    ip_addr = None
    timestamp = None

    command_regex = re.compile(command)
    start_regex = re.compile(start_pattern)
    row_regex = re.compile(row_pattern)
    end_regex = re.compile(end_pattern)
    log_info_regex = re.compile(
        r'(\d{6}-\d{2}:\d{2}:\d{2}\+\d{4})\s+([\da-fA-F:.]+)\s+(\d+\.\d+[a-zA-Z]*)\s+([\w.-]+)\s+(stopfile=[/\w\d]+)'
    )

    for line in file_content:
        line = line.strip()

        if not command_found and command_regex.match(line):
            print(f"[INFO] Command found: {line}")
            command_found = True
            node_id = line.split('>')[0].strip()
            continue

        if command_found and not header_found and re.match(r'^[A-Z0-9_-]+>', line):
            print(f"[INFO] New prompt detected, ending block for {node_id}")
            break

        log_match = log_info_regex.match(line)
        if log_match:
            timestamp, ip_addr, *_ = log_match.groups()

        if command_found and not header_found:
            header_match = start_regex.match(line)
            if header_match:
                header_found = True
                header_values = list(header_match.groups()) or header_match.group(0).split()
                print(f"[INFO] Header found: {header_values}")
                continue

        if command_found and header_found and end_regex.match(line):
            print(f"[INFO] End pattern matched. Stopping data collection for {node_id}.")
            break

        if command_found and header_found and not line.startswith('==='):
            row_match = row_regex.search(line)
            if row_match:
                data_rows.append(list(row_match.groups()))
            else:
                print(f"[DEBUG] Skipped line: {line}")

    if data_rows and header_values:
        df = pd.DataFrame(data_rows, columns=header_values)
        df['Node_ID'] = node_id
        return df
    else:
        if not header_found:
            print(f"[ERROR] Command found but header pattern did not match.")
        print("[WARN] No matching data rows or headers found.")
        return pd.DataFrame()

# ============================= Main View =============================

@api_view(["POST", "GET"])
def extract_data_from_log(request):
    all_files_df = pd.DataFrame()

    circle = request.POST.get("circle")
    files = request.FILES.getlist("files")
    base_name = None

    if not files:
        return Response(
            {"status": "ERROR", "message": "No files uploaded"},
            status=HTTP_400_BAD_REQUEST,
        )

    # Define media folders
    base_media_url = os.path.join(MEDIA_ROOT, "soft_at_status")
    output_path = os.path.join(base_media_url, "OUTPUT")
    log_folder = os.path.join(base_media_url, "circle_LOGS")
    log_excel_folder = os.path.join(base_media_url, "logs_excel")

    os.makedirs(log_folder, exist_ok=True)

    # Delete existing files in output folders
    delete_existing_files(log_folder)
    delete_existing_files(output_path)
    delete_existing_files(log_excel_folder)

    # Save uploaded files
    saved_files = []
    for file in files:
        file_path = os.path.join(log_folder, file.name)
        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
            saved_files.append(file_path)

    # Prepare Excel log folder
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    if not os.path.exists(log_excel_folder):
        os.makedirs(log_excel_folder, exist_ok=True)
    else:
        try:
            shutil.rmtree(log_excel_folder, onerror=on_rm_error)
            os.makedirs(log_excel_folder, exist_ok=True)
        except PermissionError as e:
            print("Permission denied:", str(e))

    # Process each saved log file
    for file_path in saved_files:
        base_name = os.path.basename(file_path)
        nodes = read_and_write_func(file_path)
        print(f"{file_path}:- ", len(nodes))

        node_data = {}

        for node_index, node in enumerate(nodes):
            node_key = f"node_{node_index+1}"
            node_data[node_key] = {}  # Placeholder for future logic

    return Response(
        {"status": "OK", "message": "Log files processed successfully."},
        status=HTTP_200_OK,
    )
