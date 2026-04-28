import os
import win32com.client
import pythoncom
import requests
import zipfile
import py7zr
import shutil
from datetime import datetime
from celery import shared_task
from mcom_website.settings import MEDIA_ROOT
from mailapp.tasks import send_email
import pandas as pd  # make sure this is your Celery email task
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os
from premailer import transform
from universal_alarm.models import OldvsNew
from datetime import datetime

current_time = datetime.now().strftime("%d %B %Y, %I:%M %p")
 
 
save_directory = os.path.join(MEDIA_ROOT, "Universal_alarm", "attachments")
LAST_PROCESSED_FILE = os.path.join(MEDIA_ROOT, "Universal_alarm", "last_mail.txt")

def get_summary_counts(excel_path):
    sheets = pd.read_excel(excel_path, sheet_name=None)

    # ================= SHEETS =================
    cells_4g = sheets.get("4G Cells")
    cells_5g = sheets.get("5G Cells")

    alarm_4g_df = sheets.get("4G Alarms")
    alarm_5g_df = sheets.get("5G Alarms")

    site_down_4g_df = sheets.get("4G Site Down")
    site_down_5g_df = sheets.get("5G Site Down")

    # ================= INITIALIZE =================
    total_sites_4g = set()
    total_sites_5g = set()

    # SA / NSA split
    sa_4g = 0
    nsa_4g = 0
    sa_5g = 0
    nsa_5g = 0

    # Alarm
    alarm_4g = 0
    alarm_5g = 0

    # Site Down
    old_down_5g = 0
    old_down_4g = 0
    down_4g = 0
    down_5g = 0

    hw_4g = 0
    soft_4g = 0
    hw_5g = 0
    soft_5g = 0
    pwr_4g =0
    pwr_5g = 0

    cells_count_5g = 0
    cells_count_4g = 0

    no_alarm_pct_4g = 0
    no_alarm_pct_5g = 0

    both_unlocked = 0
    both_locked = 0

    both_unlocked_5g = 0
    both_locked_5g = 0

    impacted_sites_4g= set()
    impacted_sites_5g= set()
    total_impacted_sites_5g = 0
    total_impacted_sites_4g = 0

    # ================= TOTAL 4G SITES =================
    import re
    if cells_4g is not None:
        for _, row in cells_4g.iterrows():

            # Status check
            status = str(row.get("Alarm Status", "")).strip().lower()

            if status == "new site":

                # Unique Site Count
                site = row.get("4G Site ID", "")
                if pd.notna(site) and str(site).strip() != "":
                    total_sites_4g.add(site)

                # Cell Count
                cells = row.get("Cells", "")
                if pd.notna(cells) and str(cells).strip() != "":
                    cells_count_4g += 1

        for pair in OldvsNew.objects.all():

            # New Site Status
            new_df = cells_4g[cells_4g["4G Site ID"] == pair.new_site]

            new_status = ""
            if not new_df.empty:
                new_status = str(
                    new_df["4G Cell Status - Adm State"].iloc[0]
                ).strip().upper()

            # Old Site Status
            old_df = cells_4g[cells_4g["4G Site ID"] == pair.old_site]

            old_status = ""
            if not old_df.empty:
                old_status = str(
                    old_df["4G Cell Status - Adm State"].iloc[0]
                ).strip().upper()

            # Count
            if new_status == "UNLOCKED" and old_status == "UNLOCKED":
                both_unlocked += 1

            elif new_status == "LOCKED" and old_status == "LOCKED":
                both_locked += 1

                impacted_sites_4g.add(pair.new_site)
                impacted_sites_4g.add(pair.old_site)

    total_impacted_sites_4g = len(impacted_sites_4g)
    
    print("Total Impacted Sites 4G:", total_impacted_sites_4g)
    print("Both Unlocked 4G=", both_unlocked)
    print("Both Locked 4G=", both_locked)

    print("Total NEW SITE Cells 4G:", cells_count_4g)
    print("Total Unique NEW SITE Sites 4G:", len(total_sites_4g))

    # if cells_4g is not None:
    #     for _, row in cells_4g.iterrows():
    #         site = row.get("4G Site ID", "")
    #         if pd.notna(site) and site != "":
    #             total_sites_4g.add(site)
            
    #         cells = row.get("Cells", "")
    #         if pd.notna(cells) and str(cells).strip() != "":
    #             cells_count_4g += 1
                
    # print("total cells 4g:", cells_count_4g)
    # print(f"Total Unique Sites 4g: {len(total_sites_4g)}")
            
    # ================= TOTAL 5G SITES =================
    if cells_5g is not None:
        for _, row in cells_5g.iterrows():

            status = str(row.get("Alarm Status", "")).strip().lower()

            if status == "new site":
                site = row.get("5G Site ID", "")
                if pd.notna(site) and str(site).strip() != "":
                    total_sites_5g.add(site)

                cells = row.get("Cells", "")
                if pd.notna(cells) and str(cells).strip() != "":
                    cells_count_5g += 1

        for pair in OldvsNew.objects.all():

            # New Site
            new_df = cells_5g[cells_5g["5G Site ID"] == pair.new_site]

            # Old Site
            old_df = cells_5g[cells_5g["5G Site ID"] == pair.old_site]

            new_status = ""
            old_status = ""

            if not new_df.empty:
                new_status = str(
                    new_df["5G Cell Status - Adm State"].iloc[0]
                ).strip().upper()

            if not old_df.empty:
                old_status = str(
                    old_df["5G Cell Status - Adm State"].iloc[0]
                ).strip().upper()

            if new_status == "UNLOCKED" and old_status == "UNLOCKED":
                both_unlocked_5g += 1

            elif new_status == "LOCKED" and old_status == "LOCKED":
                both_locked_5g += 1

                impacted_sites_5g.add(pair.new_site)
                impacted_sites_5g.add(pair.old_site)

    total_impacted_sites_5g = len(impacted_sites_5g)

    print("Total Impacted Sites 5G:", total_impacted_sites_5g)
    print("5G Both Unlocked =", both_unlocked_5g)
    print("5G Both Locked =", both_locked_5g)

    print("total cells 5g:", cells_count_5g)
    print(f"Total Unique Sites 5G: {len(total_sites_5g)}")

    # ================= 4G ALARMS =================
    # if alarm_4g_df is not None and "Alarm/No Alarm" in alarm_4g_df.columns:

    #     alarm_4g = alarm_4g_df["Alarm/No Alarm"] \
    #         .astype(str) \
    #         .str.strip() \
    #         .str.upper() \
    #         .eq("NO ALARM") \
    #         .sum()
        
    #     total_4g_records = len(alarm_4g_df)
    #     no_alarm_pct_4g = (alarm_4g / total_4g_records * 100) if total_4g_records else 0
    # ================= 4G ALARM SUMMARY =================

    if alarm_4g_df is not None and "Alarm/No Alarm" in alarm_4g_df.columns:

        # ---------------- NEW SITE FILTER ----------------
        new_site_4g = alarm_4g_df[
            alarm_4g_df["Alarm Status"].astype(str).str.strip().str.lower() == "new site"
        ]

        # ---------------- NO ALARM COUNT ----------------
        alarm_4g = (
            new_site_4g["Alarm/No Alarm"]
            .astype(str)
            .str.strip()
            .str.upper()
            .eq("NO ALARM")
            .sum()
        )

        total_4g_records = len(new_site_4g)

        no_alarm_pct_4g = (
            (alarm_4g / total_4g_records * 100)
            if total_4g_records else 0
        )

        print("Total NEW SITE 4G Records:", total_4g_records)
        print("NO Alarm Count 4G:", alarm_4g)
        print("NO Alarm % 4G:", round(no_alarm_pct_4g, 2), "%")

        # ---------------- SA / NSA COUNT ----------------
        if "SA/NSA" in new_site_4g.columns:

            # Header row remove if exists
            new_site_4g = new_site_4g[
                new_site_4g["SA/NSA"].astype(str).str.strip().str.upper() != "SA/NSA"
            ]

            sa_4g = (
                new_site_4g["SA/NSA"]
                .astype(str)
                .str.strip()
                .str.upper()
                .eq("SA")
                .sum()
            )

            nsa_4g = (
                new_site_4g["SA/NSA"]
                .astype(str)
                .str.strip()
                .str.upper()
                .eq("NSA")
                .sum()
            )

            print("4G SA/NSA Counts:")
            print("SA 4G:", sa_4g)
            print("NSA 4G:", nsa_4g)

        # ---------------- ONLY SA DATA ----------------
        sa_data_4g = new_site_4g[
            new_site_4g["SA/NSA"].astype(str).str.strip().str.upper() == "SA"
        ]

        # ---------------- ALARM BUCKET COUNT ----------------
        if "Alarm Bucket" in sa_data_4g.columns:

            col = sa_data_4g["Alarm Bucket"].astype(str)

            hw_4g = col.str.count(
                r'HW\sAlarm|HW\sALARM',
                flags=re.IGNORECASE
            ).sum()

            soft_4g = col.str.count(
                r'Soft\sAlarm',
                flags=re.IGNORECASE
            ).sum()

            pwr_4g = col.str.count(
                r'Power\sAlarm',
                flags=re.IGNORECASE
            ).sum()

            print("4G SA Alarm Counts:")
            print("HW Alarms 4G:", hw_4g)
            print("Soft Alarms 4G:", soft_4g)
            print("Power Alarms 4G:", pwr_4g)

    # ================= 5G ALARMS =================
    if alarm_5g_df is not None and "Alarm/No Alarm" in alarm_5g_df.columns:

        new_site_5g = alarm_5g_df[
            alarm_5g_df["Alarm Status"].astype(str).str.strip().str.lower() == "new site"
        ]

        alarm_5g = new_site_5g["Alarm/No Alarm"] \
            .astype(str) \
            .str.strip() \
            .str.upper() \
            .eq("NO ALARM") \
            .sum()

        
        total_5g_records = len(new_site_5g)
        no_alarm_pct_5g = (alarm_5g / total_5g_records * 100) if total_5g_records else 0
        print("NO Alarm Count for 5G:", alarm_5g)
        print("Total NEW SITE 5G Records:", total_5g_records)
        print("NO Alarm % for 5G:", round(no_alarm_pct_5g, 2), "%")
        
        # SA / NSA
        if "SA/NSA" in new_site_5g.columns:
            sa_5g = (
                new_site_5g["SA/NSA"]
                .astype(str)
                .str.strip()
                .str.upper()
                .eq("SA")
                .sum()
            )

            nsa_5g = (
                new_site_5g["SA/NSA"]
                .astype(str)
                .str.strip()
                .str.upper()
                .eq("NSA")
                .sum()
            )
        print(f"SA 5g: {sa_5g}")
        print(f"NSA 5g: {nsa_5g}")

        sa_data_5g = new_site_5g[
            new_site_5g["SA/NSA"].astype(str).str.strip().str.upper() == "SA"
        ]

        if "Alarm Bucket" in sa_data_5g.columns:
            col = sa_data_5g["Alarm Bucket"].astype(str)

            hw_5g = col.str.count(r'HW\sAlarm|HW\sALARM', flags=re.IGNORECASE).sum()
            soft_5g = col.str.count(r'Soft\sAlarm', flags=re.IGNORECASE).sum()
            pwr_5g = col.str.count(r'Power\sAlarm', flags=re.IGNORECASE).sum()
            

        print(f"HW Alarms 5g: {hw_5g}")
        print(f"Soft Alarms 5g: {soft_5g}")
        print(f"Power Alarms 5g: {pwr_5g}")

    # ================= 4G SITE DOWN =================
    if site_down_4g_df is not None and "Status" in site_down_4g_df.columns:

        # Sirf NEW SITE data filter
        new_site_down_4g_df = site_down_4g_df[
            site_down_4g_df["Status"].astype(str).str.strip().str.lower() == "new site"
        ]
    
        old_site_down_4g_df = site_down_4g_df[
            site_down_4g_df["Status"].astype(str).str.strip().str.lower() == "old site"
        ]
        
        old_down_4g = (
            old_site_down_4g_df["Remark"]
            .astype(str)
            .str.upper()
            .str.contains("UNABLE TO CONNECT", na=False)
            .sum()
        )
        
        # UNABLE TO CONNECT count
        down_4g = (
            new_site_down_4g_df["Remark"]
            .astype(str)
            .str.upper()
            .str.contains("UNABLE TO CONNECT", na=False)
            .sum()
        )
    print("4G OLD SITE Down Count:", old_down_4g)
    print("4G NEW SITE Down Count:", down_4g)
    
    # if site_down_4g_df is not None and "Status" in site_down_4g_df.columns:
    #     down_4g = (
    #         site_down_4g_df["Status"]
    #         .astype(str)
    #         .str.upper()
    #         .str.contains("UNABLE TO CONNECT")
    #         .sum()
    #     )
    # print("4G Site Down Count:", down_4g)

    if site_down_5g_df is not None and "Status" in site_down_5g_df.columns:
        print("Enter in if condition")

        # Sirf NEW SITE data filter
        # new_site_down_5g = site_down_5g_df[
        #     site_down_5g_df["Status"].astype(str).str.strip().str.lower() == "new site"
        # ]
        
        # old_site_down_5g = site_down_5g_df[
        #     site_down_5g_df["Status"].astype(str).str.strip().str.lower() == "old site"
        # ]
        new_site_down_5g_df = site_down_5g_df[
            site_down_5g_df["Status"].astype(str).str.strip().str.lower() == "new site"
        ]

        old_site_down_5g_df = site_down_5g_df[
            site_down_5g_df["Status"].astype(str).str.strip().str.lower() == "old site"
        ]
            
        # UNABLE TO CONNECT count
        down_5g = (
            new_site_down_5g_df["Remark"]
            .astype(str)
            .str.upper()
            .str.contains("UNABLE TO CONNECT", na=False)
            .sum()
        )

        old_down_5g = (
            old_site_down_5g_df["Remark"]
            .astype(str)
            .str.upper()
            .str.contains("UNABLE TO CONNECT", na=False)
            .sum()
        )




  
    print("5G OLD SITE Down Count:", old_down_5g)
    print("5G NEW SITE Down Count:", down_5g)


    # ================= TOTALS =================
    total_alarm = alarm_4g + alarm_5g
    total_site_down = down_4g + down_5g
    
    

    total_sa = sa_4g + sa_5g
    total_nsa = nsa_4g + nsa_5g

    total_unlocked = both_unlocked + both_unlocked_5g
    total_locked = both_locked + both_locked_5g
    total_impacted_sites = len(impacted_sites_4g.union(impacted_sites_5g))

    # ================= RETURN =================
    return {
        "total_4g_sites": len(total_sites_4g),
        "total_5g_sites": len(total_sites_5g),

        "Total_No_of_Cells": int(cells_count_4g + cells_count_5g),

        "SA_4G": int(sa_4g),
        "NSA_4G": int(nsa_4g),
        "SA_5G": int(sa_5g),
        "NSA_5G": int(nsa_5g),

        "SA": int(total_sa),
        "NSA": int(total_nsa),

        "Alarm_4G": int(alarm_4g),
        "Alarm_5G": int(alarm_5g),
        "Alarm": int(total_alarm),

        "Site_Down_4G": int(down_4g),
        "Site_Down_5G": int(down_5g),
        "old_down_5g": int(old_down_5g),
        "old_down_4g": int(old_down_4g),

        "Site Down": int(total_site_down),

        "HW_4G": int(hw_4g),
        "SOFT_4G": int(soft_4g),
        "PWR_4G": int(pwr_4g),

        "HW_5G": int(hw_5g),
        "SOFT_5G": int(soft_5g),
        "PWR_5G": int(pwr_5g),

        "Cells_4G": int(cells_count_4g),
        "Cells_5G": int(cells_count_5g),

        "No_alarm_Pct_4G": round(no_alarm_pct_4g, 2),
        "No_alarm_Pct_5G": round(no_alarm_pct_5g, 2),

        "Both_Unlocked_4G": int(both_unlocked),
        "Both_Unlocked_5G": int(both_unlocked_5g),
        "Both_Locked_4G": int(both_locked),
        "Both_Locked_5G": int(both_locked_5g),
        "Total_Both_Unlocked": int(total_unlocked),
        "Total_Both_Locked": int(total_locked),
        "total_impacted_sites": int(total_impacted_sites),
    }


def is_new_mail(unique_id):
    if not os.path.exists(LAST_PROCESSED_FILE):
        return True
    with open(LAST_PROCESSED_FILE, "r") as f:
        last_id = f.read().strip()
    return unique_id != last_id
 
 
def save_last_mail(unique_id):
    if not os.path.exists(os.path.dirname(LAST_PROCESSED_FILE)):
        os.makedirs(os.path.dirname(LAST_PROCESSED_FILE))
    with open(LAST_PROCESSED_FILE, "w") as f:
        f.write(unique_id)
 
@shared_task
def check_outlook_mail(expected_subject="MS2 Pending Sites"):
    # pythoncom.CoInitialize()
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.Folders.Item("Prerna.PramodKumar@ust.com").Folders["Inbox"]
 
    messages = inbox.Items
    messages.Sort("[ReceivedTime]", True)
    latest_mail = messages.GetFirst()
 
    if not latest_mail:
        return None
 
    unique_id = f"{latest_mail.Subject}|{latest_mail.SenderEmailAddress}|{latest_mail.ReceivedTime}"
    if not is_new_mail(unique_id):
        print("⚠️ Already processed this mail, skipping...")
        return None
 
    subject = str(latest_mail.Subject)
    print(f"Latest mail => {subject}")

    if expected_subject.lower() in subject.lower():
        if latest_mail.Attachments.Count > 0:
            # 🔹 Clean old attachments before saving new one-----
            if os.path.exists(save_directory):
                for old_file in os.listdir(save_directory):
                    old_path = os.path.join(save_directory, old_file)
                    if os.path.isfile(old_path):
                        os.remove(old_path)
                    elif os.path.isdir(old_path):
                        shutil.rmtree(old_path)

            for att in latest_mail.Attachments:
                if att.FileName.endswith((".zip", ".7z")):
                    if not os.path.exists(save_directory):
                        os.makedirs(save_directory)    
                    file_path = os.path.join(save_directory, att.FileName)
                    att.SaveAsFile(file_path)
                    print(" Zip downloaded:", file_path)

                    save_last_mail(unique_id)
    
                    process_daily_circle_logs(
                        file_path,
                        to_address=latest_mail.To,
                        cc_mails=latest_mail.CC,
                    )

                    return {
                        "file_path": file_path,
                        "to": latest_mail.To,
                        "cc": latest_mail.CC,
                        "subject": subject,
                        "received_time": str(latest_mail.ReceivedTime),
                    }

    return None

def process_daily_circle_logs(file_path,to_address=None, cc_mails=None):
    print("CC called process_daily_circle_logs", cc_mails)
    print(file_path,"file path.................................."   )
    today_str = datetime.today().strftime("%Y-%m-%d")
    output_root = os.path.join(MEDIA_ROOT, "Universal_alarm", "daily_status_alarm")

    if os.path.exists(output_root):
        for item in os.listdir(output_root):
            item_path = os.path.join(output_root, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path) 
            elif item.endswith(".zip"):
                os.remove(item_path)
 
    zip_files = [f for f in os.listdir(save_directory) if f.endswith((".zip", ".7z"))]
    if not zip_files:
        print("No zip files found to process")
        return
 
    zip_file = os.path.join(save_directory, zip_files[-1])
    extract_dir = os.path.splitext(zip_file)[0]
    print(" Processing latest zip:", zip_file)
 
    # extract_dir = zip_file.replace(".zip", "")
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir, ignore_errors=True)   #add this line to remove existing directory before creating a new one
    os.makedirs(extract_dir, exist_ok=True)
   
 
    if zip_file.endswith(".zip"):
        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
    elif zip_file.endswith(".7z"):
        with py7zr.SevenZipFile(zip_file, "r") as archive:
            archive.extractall(extract_dir)
    else:
        raise ValueError(f"Unsupported file format: {zip_file}")
 
    print(f" Extracted to {extract_dir}")
 
    daily_status_folder = os.path.join(MEDIA_ROOT, "Universal_alarm", "daily_status_alarm", today_str)
    os.makedirs(daily_status_folder, exist_ok=True)
 
    circles_path = os.path.join(extract_dir, extract_dir.split("\\")[-1])
    for circle in os.listdir(circles_path):
        circle_path = os.path.join(circles_path, circle)
        print(circle_path,"circle path.....................................")
        if not os.path.isdir(circle_path):
            print("invalid cricle path.....................................")
            continue
 
        log_files = []
        for file_name in os.listdir(circle_path):
            file_path = os.path.join(circle_path, file_name)
            if os.path.isfile(file_path):
                with open(file_path, "rb") as f:
                    log_files.append(("log_files", (file_name, f.read())))
 
        print(f" Uploading logs for circle: {circle}, Files: {len(log_files)}")
        if not log_files:
            continue
 
        response_4G = requests.post(
            "http://127.0.0.1:8001/universal_alarm/upload_4g/",
            files=log_files,
            data={"circle": circle},
        )
        response_5G = requests.post(
            "http://127.0.0.1:8001/universal_alarm/upload_5g/",
            files=log_files,
            data={"circle": circle},
        )
        print(f" API Response for {circle}: 4G={response_4G.status_code}, 5G={response_5G.status_code}")
    # ================= SUMMARY =================
    print("bhai yha tk to shi h code.................")
    circle_summary = {}
    overall_summary = {
        "total_4g_sites": 0,
        "total_5g_sites": 0,
        "SA_4G": 0, "NSA_4G": 0,
        "SA_5G": 0, "NSA_5G": 0,
        "Alarm_4G": 0, "Alarm_5G": 0,
        "Site_Down_4G": 0, "Site_Down_5G": 0,
        "old_down_5g": 0, "old_down_4g": 0,
        "HW_4G": 0, "SOFT_4G": 0, "PWR_4G": 0,
        "HW_5G": 0, "SOFT_5G": 0, "PWR_5G": 0, 
        "Cells_4G": 0, "Cells_5G": 0,
        "No_Alarm_Pct_4G": 0.0, "No_alarm_Pct_5G": 0.0,
        "Total_No_of_Cells": 0,
        "Total_Both_Unlocked": 0,
        "Total_Both_Locked": 0,
        "total_impacted_sites": 0,
    }

    for root, _, files in os.walk(daily_status_folder):

        excel_files = [f for f in files if f.endswith(".xlsx")]
        if not excel_files:
            continue

        circle = os.path.basename(root)

        # 🔹 Initialize per circle
        if circle not in circle_summary:
            circle_summary[circle] = None

        final_summary = None

        # 🔹 Handle multiple excel (merge data)
        for file in excel_files:
            excel_path = os.path.join(root, file)
            summary = get_summary_counts(excel_path)

            if final_summary is None:
                final_summary = summary.copy()
            else:
                for key in summary:
                    if isinstance(summary[key], (int, float)):
                        final_summary[key] += summary[key]

        # ================= TEMPLATE =================
        template_dir = os.path.join(MEDIA_ROOT, "template")
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("alarm_mailbody.html")

        # context = {
        #     **final_summary,
        #     "generated_time": datetime.now().strftime("%d %B %Y, %I:%M %p"),
        #     "circle_summary": {circle: final_summary},
        #     "circle_name": circle,
        # }

        # html = template.render(context)
        context = {
            **final_summary,
            "generated_time": datetime.now().strftime("%d %B %Y, %I:%M %p"),
            "circle_summary": {circle: final_summary},
            "circle_name": circle,
        }
        print("Circle =", circle)
        print("Context =", context["circle_name"])

        html = template.render(**context)
        body = transform(html)

        # ================= ZIP =================
        circle_folder = root
        zip_output_path = f"{circle_folder}.zip"
        shutil.make_archive(circle_folder, "zip", circle_folder)

        print(f" Zipped → {zip_output_path}")

        # ================= EMAIL =================
        reply_subject = f"📊 {circle} Processed Daily Status Alarm"
        
        # to_address=';'.join(['Amit.Rai@ust.com','Yogesh.Prajapati@ust.com','Abhinav.Verma@ust.com','Deepu.Sharma@ust.com','Praveen.Lakra@ust.com','Gulafsha.Bano@ust.com','Priyanshi.Sharma@ust.com'])
        # cc_mails = ';'.join(['Mohit.Batra@ust.com','Aashish.Sharma@ust.com','Shashank.Rai@ust.com','Chirag.Bohara@ust.com','Prerna.PramodKumar@ust.com','Dhiraj.Sharma@ust.com'])
        to_address = ';'.join([
            # 'Abhinav.Verma@ust.com',
            'Prerna.PramodKumar@ust.com'
        ])

        cc_mails = ';'.join([
            # 'Abhishek.Maurya@ust.com'
        ])

        send_email.delay(
            to_address=to_address,
            cc_mails=cc_mails,
            subject=reply_subject,
            body=body,
            attachment_path=zip_output_path,
            is_html=True,
        )

        print(f"✅ Mail Sent for Circle => {circle}")


#ye tera shi code h -------------------------------------

    # for root, _, files in os.walk(daily_status_folder):
    #     for file in files:
    #         if file.endswith(".xlsx"):
    #             excel_path = os.path.join(root, file)
    #             circle = os.path.basename(root)

    #             summary = get_summary_counts(excel_path)

    #             if circle not in circle_summary:
    #                 circle_summary[circle] = {k: 0 for k in summary.keys()}

    #             for key in summary:
    #                 circle_summary[circle][key] += summary[key]
    #                 if key in overall_summary:
    #                     overall_summary[key] += summary[key]

    #     # ================= TEMPLATE =================
    #     template_dir = os.path.join(MEDIA_ROOT, "template")
    #     env = Environment(loader=FileSystemLoader(template_dir))
    #     template = env.get_template("alarm_mailbody.html")

    #     context = {
    #         **overall_summary,
    #         "generated_time": datetime.now().strftime("%d %B %Y, %I:%M %p"),
    #         "circle_summary": circle_summary,
    #     }

    #     html = template.render(context)
    #     body = transform(html)   # html email body


    #     zip_output_path = f"{daily_status_folder}.zip"
    #     shutil.make_archive(daily_status_folder, "zip", daily_status_folder)
    #     print(f" Zipped daily status folder → {zip_output_path}")

    #     # Email notification----------------
    #     reply_subject = f"📊Processed Daily Status Alarm"

    #     to_address=';'.join([
    #         'Abhinav.Verma@ust.com',
    #         'Prerna.PramodKumar@ust.com'
    #     ])

    #     cc_mails=';'.join([
    #         'Abhishek.Maurya@ust.com'
    #     ])

    # send_email.delay(
    #     to_address=to_address,
    #     cc_mails=cc_mails,
    #     subject=reply_subject,
    #     body=body,              
    #     attachment_path=zip_output_path,
    #     is_html=True,             
    # )

#ye tera shi code h -------------------------------------

# import os
# import win32com.client
# import pythoncom
# import requests
# import zipfile
# import py7zr
# import shutil
# from datetime import datetime
# from celery import shared_task
# from mcom_website.settings import MEDIA_ROOT
# from mailapp.tasks import send_email
# import pandas as pd  # make sure this is your Celery email task
# from jinja2 import Environment, FileSystemLoader
# from datetime import datetime
# import os
# from premailer import transform


# save_directory = os.path.join(MEDIA_ROOT, "Universal_alarm", "attachments")
# LAST_PROCESSED_FILE = os.path.join(MEDIA_ROOT, "Universal_alarm", "last_mail.txt")



# def get_summary_counts(excel_path):
#     sheets = pd.read_excel(excel_path, sheet_name=None)

#     # ================= SHEETS =================
#     cells_4g = sheets.get("4G Cells")
#     cells_5g = sheets.get("5G Cells")

#     alarm_4g_df = sheets.get("4G Alarms")
#     alarm_5g_df = sheets.get("5G Alarms")

#     site_down_4g_df = sheets.get("4G Site Down")
#     site_down_5g_df = sheets.get("5G Site Down")

#     # ================= INITIALIZE =================
#     total_sites_4g = set()
#     total_sites_5g = set()

#     # SA / NSA split
#     sa_4g = 0
#     nsa_4g = 0
#     sa_5g = 0
#     nsa_5g = 0

#     # Alarm
#     alarm_4g = 0
#     alarm_5g = 0

#     # Site Down
#     down_4g = 0
#     down_5g = 0

#     hw_4g = 0
#     soft_4g = 0
#     hw_5g = 0
#     soft_5g = 0
#     pwr_4g =0
#     pwr_5g = 0


#     # ================= TOTAL 4G SITES =================
#     if cells_4g is not None:
#         for _, row in cells_4g.iterrows():
#             site = row.get("4G Site ID", "")
#             if pd.notna(site) and site != "":
#                 total_sites_4g.add(site)

#             alarm_bucket = str(row.get("Alarm Bucket", "")).lower()

#             hw_count = 1 if "hw alarm" in alarm_bucket else 0
#             soft_count = 1 if "soft alarm" in alarm_bucket else 0
#             pwr_count = 1 if "power" in alarm_bucket else 0

#             hw_4g += hw_count
#             soft_4g += soft_count
#             pwr_4g += pwr_count

#     # ================= TOTAL 5G SITES =================
#     if cells_5g is not None:
#         for _, row in cells_5g.iterrows():
#             site = row.get("5G Site ID", "")
#             if pd.notna(site) and site != "":
#                 total_sites_5g.add(site)
#             alarm_bucket = str(row.get("Alarm Bucket", "")).lower()
#             hw_count = 1 if "hw alarm" in alarm_bucket else 0
#             soft_count = 1 if "soft alarm" in alarm_bucket else 0

#             hw_5g += hw_count
#             soft_5g += soft_count
#             pwr_5g += 1 if "power" in alarm_bucket else 0

#     # ================= 4G ALARMS =================
#     if alarm_4g_df is not None and "Alarm/No Alarm" in alarm_4g_df.columns:
#         alarm_4g = alarm_4g_df["Alarm/No Alarm"] \
#             .astype(str) \
#             .str.strip() \
#             .str.upper() \
#             .eq("NO ALARM") \
#             .sum()


#         # SA / NSA
#         if "SA/NSA" in alarm_4g_df.columns:
#             sa_4g = (
#                 alarm_4g_df["SA/NSA"]
#                 .astype(str)
#                 .str.strip()
#                 .str.upper()
#                 .eq("SA")
#                 .sum()
#             )

#             nsa_4g = (
#                 alarm_4g_df["SA/NSA"]
#                 .astype(str)
#                 .str.strip()
#                 .str.upper()
#                 .eq("NSA")
#                 .sum()
#             )

#     # ================= 5G ALARMS =================
#     if alarm_5g_df is not None and "Alarm/No Alarm" in alarm_5g_df.columns:
#         alarm_5g = alarm_5g_df["Alarm/No Alarm"] \
#             .astype(str) \
#             .str.strip() \
#             .str.upper() \
#             .eq("NO ALARM") \
#             .sum()
    
#         # SA / NSA
#         if "SA/NSA" in alarm_5g_df.columns:
#             sa_5g = (
#                 alarm_5g_df["SA/NSA"]
#                 .astype(str)
#                 .str.strip()
#                 .str.upper()
#                 .eq("SA")
#                 .sum()
#             )

#             nsa_5g = (
#                 alarm_5g_df["SA/NSA"]
#                 .astype(str)
#                 .str.strip()
#                 .str.upper()
#                 .eq("NSA")
#                 .sum()
#             )

#     # ================= 4G SITE DOWN =================
#     if site_down_4g_df is not None and "Status" in site_down_4g_df.columns:
#         down_4g = (
#             site_down_4g_df["Status"]
#             .astype(str)
#             .str.upper()
#             .str.contains("UNABLE TO CONNECT")
#             .sum()
#         )

#     # ================= 5G SITE DOWN =================
#     if site_down_5g_df is not None and "Status" in site_down_5g_df.columns:
#         down_5g = (
#             site_down_5g_df["Status"]
#             .astype(str)
#             .str.upper()
#             .str.contains("UNABLE TO CONNECT")
#             .sum()
#         )

#     # ================= TOTALS =================
#     total_alarm = alarm_4g + alarm_5g
#     total_site_down = down_4g + down_5g

#     total_sa = sa_4g + sa_5g
#     total_nsa = nsa_4g + nsa_5g

#     # ================= RETURN =================
#     return {
#         "total_4g_sites": len(total_sites_4g),
#         "total_5g_sites": len(total_sites_5g),

#         # SA/NSA split
#         "SA_4G": int(sa_4g),
#         "NSA_4G": int(nsa_4g),
#         "SA_5G": int(sa_5g),
#         "NSA_5G": int(nsa_5g),

#         "SA": int(total_sa),
#         "NSA": int(total_nsa),

#         # Alarm
#         "Alarm_4G": int(alarm_4g),
#         "Alarm_5G": int(alarm_5g),
#         "Alarm": int(total_alarm),

#         # Site Down
#         "Site_Down_4G": int(down_4g),
#         "Site_Down_5G": int(down_5g),
#         "Site Down": int(total_site_down),

#         "HW_4G": int(hw_4g),
#         "SOFT_4G": int(soft_4g),
#         "PWR_4G": int(pwr_4g),

#         "HW_5G": int(hw_5g),
#         "SOFT_5G": int(soft_5g),
#         "PWR_5G": int(pwr_5g),

#     }


# def is_new_mail(unique_id):
#     if not os.path.exists(LAST_PROCESSED_FILE):
#         return True
#     with open(LAST_PROCESSED_FILE, "r") as f:
#         last_id = f.read().strip()
#     return unique_id != last_id

# def save_last_mail(unique_id):
#     if not os.path.exists(os.path.dirname(LAST_PROCESSED_FILE)):
#         os.makedirs(os.path.dirname(LAST_PROCESSED_FILE))
#     with open(LAST_PROCESSED_FILE, "w") as f:
#         f.write(unique_id)

# @shared_task
# def check_outlook_mail(expected_subject="MS2 Pending Sites"):
#     # pythoncom.CoInitialize()
#     outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
#     inbox = outlook.Folders.Item("Prerna.PramodKumar@ust.com").Folders["Inbox"]

#     messages = inbox.Items
#     messages.Sort("[ReceivedTime]", True)
#     latest_mail = messages.GetFirst()

#     if not latest_mail:
#         return None

#     unique_id = f"{latest_mail.Subject}|{latest_mail.SenderEmailAddress}|{latest_mail.ReceivedTime}"
#     if not is_new_mail(unique_id):
#         print("⚠️ Already processed this mail, skipping...")
#         return None

#     subject = str(latest_mail.Subject)
#     print(f"Latest mail => {subject}")

#     if expected_subject.lower() in subject.lower():
#         if latest_mail.Attachments.Count > 0:
#             # 🔹 Clean old attachments before saving new one-----
#             if os.path.exists(save_directory):
#                 for old_file in os.listdir(save_directory):
#                     old_path = os.path.join(save_directory, old_file)
#                     if os.path.isfile(old_path):
#                         os.remove(old_path)
#                     elif os.path.isdir(old_path):
#                         shutil.rmtree(old_path)

#             for att in latest_mail.Attachments:
#                 if att.FileName.endswith((".zip", ".7z")):
#                     if not os.path.exists(save_directory):
#                         os.makedirs(save_directory)    
#                     file_path = os.path.join(save_directory, att.FileName)
#                     att.SaveAsFile(file_path)
#                     print(" Zip downloaded:", file_path)

#                     save_last_mail(unique_id)

#                     process_daily_circle_logs(
#                         file_path,
#                         to_address=latest_mail.To,
#                         cc_mails=latest_mail.CC,
#                     )

#                     return {
#                         "file_path": file_path,
#                         "to": latest_mail.To,
#                         "cc": latest_mail.CC,
#                         "subject": subject,
#                         "received_time": str(latest_mail.ReceivedTime),
#                     }
#     return None
# def process_daily_circle_logs(file_path, to_address=None, cc_mails=None):
#     today_str = datetime.today().strftime("%Y-%m-%d")
#     output_root = os.path.join(MEDIA_ROOT, "Universal_alarm", "daily_status_alarm")

#     # साफ करो पुराना data
#     if os.path.exists(output_root):
#         shutil.rmtree(output_root)

#     os.makedirs(output_root, exist_ok=True)

#     # ZIP extract
#     extract_dir = os.path.splitext(file_path)[0]

#     if os.path.exists(extract_dir):
#         shutil.rmtree(extract_dir)

#     os.makedirs(extract_dir, exist_ok=True)

#     if file_path.endswith(".zip"):
#         with zipfile.ZipFile(file_path, "r") as zip_ref:
#             zip_ref.extractall(extract_dir)
#     elif file_path.endswith(".7z"):
#         with py7zr.SevenZipFile(file_path, "r") as archive:
#             archive.extractall(extract_dir)

#     print(f"Extracted to {extract_dir}")

#     daily_status_folder = os.path.join(output_root, today_str)
#     os.makedirs(daily_status_folder, exist_ok=True)

#     # 🔥 FIXED: direct extract_dir use karo
#     circles_path = extract_dir

#     # ================= API HIT =================
#     for circle in os.listdir(circles_path):
#         circle_path = os.path.join(circles_path, circle)

#         if not os.path.isdir(circle_path):
#             continue

#         log_files = []
#         for file_name in os.listdir(circle_path):
#             file_path_inner = os.path.join(circle_path, file_name)
#             if os.path.isfile(file_path_inner):
#                 with open(file_path_inner, "rb") as f:
#                     log_files.append(("log_files", (file_name, f.read())))

#         if not log_files:
#             continue

#         requests.post(
#             "http://127.0.0.1:8001/universal_alarm/upload_4g/",
#             files=log_files,
#             data={"circle": circle},
#         )

#         requests.post(
#             "http://127.0.0.1:8001/universal_alarm/upload_5g/",
#             files=log_files,
#             data={"circle": circle},
#         )

#     # ================= SUMMARY =================
#     circle_summary = {}
#     overall_summary = {
#         "total_4g_sites": 0,
#         "total_5g_sites": 0,
#         "SA_4G": 0, "NSA_4G": 0,
#         "SA_5G": 0, "NSA_5G": 0,
#         "Alarm_4G": 0, "Alarm_5G": 0,
#         "Site_Down_4G": 0, "Site_Down_5G": 0,
#         "HW_4G": 0, "SOFT_4G": 0, "PWR_4G": 0,
#         "HW_5G": 0, "SOFT_5G": 0, "PWR_5G": 0,
#     }

#     for root, _, files in os.walk(daily_status_folder):
#         for file in files:
#             if file.endswith(".xlsx"):
#                 excel_path = os.path.join(root, file)
#                 circle = os.path.basename(root)

#                 summary = get_summary_counts(excel_path)

#                 if circle not in circle_summary:
#                     circle_summary[circle] = {k: 0 for k in summary.keys()}

#                 for key in summary:
#                     circle_summary[circle][key] += summary[key]
#                     if key in overall_summary:
#                         overall_summary[key] += summary[key]

#     # ================= TEMPLATE =================
#     template_dir = os.path.join(MEDIA_ROOT, "template")
#     env = Environment(loader=FileSystemLoader(template_dir))
#     template = env.get_template("alarm_mailbody.html")

#     context = {
#         **overall_summary,
#         "generated_time": datetime.now().strftime("%d %B %Y, %I:%M %p"),
#         "circle_summary": circle_summary,
#     }

    

#     html = template.render(context)
#     body = transform(html)

    # body = template.render(context)

    # ================= ZIP =================
    # zip_output_path = f"{daily_status_folder}.zip"
    # shutil.make_archive(daily_status_folder, "zip", daily_status_folder)


# def process_daily_circle_logs(file_path,to_address=None, cc_mails=None):
#     print("CC called process_daily_circle_logs", cc_mails)
#     print(file_path,"file path.................................."   )
#     today_str = datetime.today().strftime("%Y-%m-%d")
#     output_root = os.path.join(MEDIA_ROOT, "Universal_alarm", "daily_status_alarm")

#     # 🔹 Purane output zips delete karo
#     if os.path.exists(output_root):
#         for item in os.listdir(output_root):
#             item_path = os.path.join(output_root, item)
#             if os.path.isdir(item_path):
#                 shutil.rmtree(item_path)   # purana folder delete---
#             elif item.endswith(".zip"):
#                 os.remove(item_path)  # purana zip delete

#     zip_files = [f for f in os.listdir(save_directory) if f.endswith((".zip", ".7z"))]
#     if not zip_files:
#         print("No zip files found to process")
#         return

#     zip_file = os.path.join(save_directory, zip_files[-1])
#     # ✅ Use os.path.splitext for safe folder name
#     extract_dir = os.path.splitext(zip_file)[0]
#     print(" Processing latest zip:", zip_file)

#     # extract_dir = zip_file.replace(".zip", "")
#     if os.path.exists(extract_dir):
#         shutil.rmtree(extract_dir, ignore_errors=True)   #add this line to remove existing directory before creating a new one
#     os.makedirs(extract_dir, exist_ok=True)

#     if zip_file.endswith(".zip"):
#         with zipfile.ZipFile(zip_file, "r") as zip_ref:
#             zip_ref.extractall(extract_dir)
#     elif zip_file.endswith(".7z"):
#         with py7zr.SevenZipFile(zip_file, "r") as archive:
#             archive.extractall(extract_dir)
#     else:
#         raise ValueError(f"Unsupported file format: {zip_file}")

#     print(f" Extracted to {extract_dir}")

#     daily_status_folder = os.path.join(MEDIA_ROOT, "Universal_alarm", "daily_status_alarm", today_str)
#     os.makedirs(daily_status_folder, exist_ok=True)

#     circles_path = os.path.join(extract_dir, extract_dir.split("\\")[-1])
#     for circle in os.listdir(circles_path):
#         circle_path = os.path.join(circles_path, circle)
#         print(circle_path,"circle path.....................................")
#         if not os.path.isdir(circle_path):
#             print("invalid cricle path.....................................")
#             continue

#         log_files = []
#         for file_name in os.listdir(circle_path):
#             file_path = os.path.join(circle_path, file_name)
#             if os.path.isfile(file_path):
#                 with open(file_path, "rb") as f:
#                     log_files.append(("log_files", (file_name, f.read())))

#         print(f" Uploading logs for circle: {circle}, Files: {len(log_files)}")
#         if not log_files:
#             continue

#         response_4G = requests.post(
#             "http://127.0.0.1:8001/universal_alarm/upload_4g/",
#             files=log_files,
#             data={"circle": circle},
#         )
#         response_5G = requests.post(
#             "http://127.0.0.1:8001/universal_alarm/upload_5g/",
#             files=log_files,
#             data={"circle": circle},
#         )
#         print(f" API Response for {circle}: 4G={response_4G.status_code}, 5G={response_5G.status_code}")

#     zip_output_path = f"{daily_status_folder}.zip"
#     shutil.make_archive(daily_status_folder, "zip", daily_status_folder)
#     print(f" Zipped daily status folder → {zip_output_path}")

#     template_dir = os.path.join(MEDIA_ROOT, "template")

#     env = Environment(loader=FileSystemLoader(template_dir))
#     template = env.get_template("alarm_mailbody.html")

#     context = {
#         **overall_summary,
#         "generated_time": datetime.now().strftime("%d %B %Y, %I:%M %p"),
#         "total_cells_4g": 0,
#         "total_cells_5g": 0,
#     }

#     body = template.render(context)

#     # ================= SUMMARY =================
#     circle_summary = {}

#     overall_summary = {
#         "total_4g_sites": 0,
#         "total_5g_sites": 0,

#         "SA_4G": 0, "NSA_4G": 0,
#         "SA_5G": 0, "NSA_5G": 0,

#         "Alarm_4G": 0, "Alarm_5G": 0,
#         "Site_Down_4G": 0, "Site_Down_5G": 0,

#         "HW_4G": 0, "SOFT_4G": 0, "PWR_4G": 0,
#         "HW_5G": 0, "SOFT_5G": 0, "PWR_5G": 0,
#     }

#     for root, _, files in os.walk(daily_status_folder):
#         for file in files:
#             if file.endswith(".xlsx"):
#                 excel_path = os.path.join(root, file)
#                 circle = os.path.basename(root)

#                 summary = get_summary_counts(excel_path)

#                 if circle not in circle_summary:
#                     circle_summary[circle] = {k: 0 for k in summary.keys()}

#                 for key in summary:
#                     circle_summary[circle][key] += summary[key]

#                     if key in overall_summary:
#                         overall_summary[key] += summary[key]

#     # ================= TEMPLATE RENDER =================
#     template_dir = os.path.join(MEDIA_ROOT, "template")  # ✅ correct path

#     env = Environment(loader=FileSystemLoader(template_dir))
#     template = env.get_template("alarm_mailbody.html")

#     context = {
#         **overall_summary,
#         "generated_time": datetime.now().strftime("%d %B %Y, %I:%M %p"),
#         "total_cells_4g": 0,
#         "total_cells_5g": 0,
#         "circle_summary": circle_summary,  # 🔥 optional future use
#     }

#     body = template.render(context)

#     # ================= ZIP =================
#     zip_output_path = f"{daily_status_folder}.zip"
#     shutil.make_archive(daily_status_folder, "zip", daily_status_folder)

    # # ================= EMAIL =================
    # send_email.delay(
    #     to_address="Prerna.PramodKumar@ust.com",
    #     cc_mails=cc_mails,
    #     subject="📊 Processed Alarm Report",
    #     body=body,
    #     attachment_path=zip_output_path,
    #     is_html=True,
    # )
    # body =f"""
    #     <html>
    #     <body>
    #     <style>
    #     *{{box-sizing:border-box;margin:0;padding:0;}}
    #     body{{font-family:'Segoe UI',Arial,sans-serif;background:#eef2f7;padding:16px}}
    #     .wrap{{max-width:920px;margin:0 auto;border-radius:16px;overflow:hidden;box-shadow:0 8px 32px rgba(10,30,80,.18),0 1.5px 4px rgba(10,30,80,.08)}}

    #     .hdr{{background:linear-gradient(120deg,#0d2257 0%,#1a4db3 55%,#2563eb 100%);color:#fff;padding:22px 28px;text-align:center;position:relative;overflow:hidden}}
    #     .hdr::before{{content:'';position:absolute;top:-40px;right:-40px;width:180px;height:180px;border-radius:50%;background:rgba(255,255,255,.06)}}
    #     .hdr::after{{content:'';position:absolute;bottom:-30px;left:-20px;width:120px;height:120px;border-radius:50%;background:rgba(255,255,255,.05)}}
    #     .hdr-icon{{font-size:28px;margin-bottom:6px}}
    #     .hdr h1{{font-size:21px;font-weight:800;letter-spacing:.6px}}
    #     .hdr p{{font-size:12px;color:#93c5fd;margin-top:5px}}

    #     .sec-hdr{{display:flex;align-items:center;gap:10px;padding:11px 20px;font-size:12px;font-weight:700;letter-spacing:.7px;color:#fff;text-transform:uppercase}}
    #     .sh-blue{{background:linear-gradient(90deg,#1e3a8a,#2563eb)}}
    #     .sh-green{{background:linear-gradient(90deg,#14532d,#16a34a)}}
    #     .sh-red{{background:linear-gradient(90deg,#7f1d1d,#dc2626)}}
    #     .sh-amber{{background:linear-gradient(90deg,#78350f,#d97706)}}
    #     .sh-indigo{{background:linear-gradient(90deg,#1e1b4b,#4f46e5)}}

    #     .sec-icon{{width:20px;height:20px;flex-shrink:0}}
    #     .body-pad{{padding:16px 20px;background:#f8faff}}

    #     .summary-grid{{display:grid;grid-template-columns:repeat(6,1fr);gap:10px}}
    #     @media(max-width:620px){{summary-grid{{grid-template-columns:repeat(3,1fr)}}}}

    #     .scard{{border-radius:12px;padding:14px 8px 12px;text-align:center;box-shadow:0 2px 10px rgba(0,0,0,.10),0 1px 3px rgba(0,0,0,.07)}}
    #     .scard-icon{{font-size:20px;margin-bottom:6px;display:block}}
    #     .scard .lbl{{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;margin-bottom:5px;opacity:.75}}
    #     .scard .val{{font-size:26px;font-weight:900;line-height:1}}
    #     .scard .sub{{font-size:10px;margin-top:4px;opacity:.65}}

    #     .s4g{{background:linear-gradient(135deg,#d1fae5,#a7f3d0);color:#064e3b}}
    #     .s5g{{background:linear-gradient(135deg,#dbeafe,#bfdbfe);color:#1e3a8a}}
    #     .sa4{{background:linear-gradient(135deg,#fef9c3,#fde68a);color:#78350f}}
    #     .sa5{{background:linear-gradient(135deg,#fce7f3,#fbcfe8);color:#831843}}
    #     .sd4{{background:linear-gradient(135deg,#fee2e2,#fecaca);color:#7f1d1d}}
    #     .sd5{{background:linear-gradient(135deg,#ffedd5,#fed7aa);color:#7c2d12}}

    #     .two-col{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
    #     @media(max-width:540px){{two-col{{grid-template-columns:1fr}}}}

    #     .panel{{border-radius:12px;padding:16px;background:#fff;box-shadow:0 3px 14px rgba(30,58,138,.10),0 1px 3px rgba(30,58,138,.06)}}
    #     .ptitle{{font-size:12px;font-weight:800;text-align:center;letter-spacing:.6px;text-transform:uppercase;padding-bottom:12px;display:flex;align-items:center;justify-content:center;gap:6px}}
    #     .pt4{{color:#15803d}}.pt5{{color:#1d4ed8}}

    #     .gauge-row{{display:flex;align-items:center;gap:12px}}
    #     .gdata{{font-size:12px;line-height:2;color:#374151;flex:1}}
    #     .gdata b{{font-weight:700;color:#111827}}
    #     .gdata .red{{color:#dc2626;font-weight:700}}
    #     .gdata .grn{{color:#16a34a;font-weight:700}}
    #     .gdata .amb{{color:#d97706;font-weight:700}}

    #     .bucket-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}}
    #     .bcard{{border-radius:10px;padding:12px 6px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.13)}}
    #     .bcard .bico{{font-size:18px;margin-bottom:4px;display:block}}
    #     .bcard .btype{{font-size:10px;font-weight:800;letter-spacing:.5px;margin-bottom:4px;opacity:.85}}
    #     .bcard .bval{{font-size:22px;font-weight:900}}
    #     .b-hw{{background:linear-gradient(135deg,#1e3a8a,#2563eb);color:#fff}}
    #     .b-soft{{background:linear-gradient(135deg,#1e1b4b,#4f46e5);color:#fff}}
    #     .b-pwr{{background:linear-gradient(135deg,#7f1d1d,#ef4444);color:#fff}}

    #     .down-grid{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
    #     .dcard{{border-radius:10px;padding:12px 8px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.12)}}
    #     .dcard .dico{{font-size:18px;margin-bottom:4px;display:block}}
    #     .dcard .dtype{{font-size:10px;font-weight:700;margin-bottom:4px;opacity:.85;text-transform:uppercase;letter-spacing:.4px}}
    #     .dcard .dval{{font-size:24px;font-weight:900}}
    #     .d-new{{background:linear-gradient(135deg,#134e4a,#0f766e);color:#fff}}
    #     .d-old{{background:linear-gradient(135deg,#1c1917,#57534e);color:#fff}}

    #     .tbl-wrap{{border-radius:10px;overflow:hidden;box-shadow:0 2px 10px rgba(30,58,138,.09)}}
    #     .tbl{{width:100%;border-collapse:collapse;font-size:12px}}
    #     .tbl thead tr{{background:linear-gradient(90deg,#1e3a8a,#2563eb)}}
    #     .tbl th{{color:#fff;padding:9px 10px;text-align:center;font-weight:700;letter-spacing:.4px}}
    #     .tbl th:first-child{{text-align:left}}
    #     .tbl td{{padding:8px 10px;text-align:center;border-bottom:1px solid #e0e9f7;color:#374151;background:#fff}}
    #     .tbl tr:nth-child(even) td{{background:#f0f5ff}}
    #     .tbl tr:last-child td{{border-bottom:none;font-weight:800;background:linear-gradient(90deg,#e0e9ff,#f0f5ff)}}
    #     .tbl td:first-child{{text-align:left;font-weight:700;color:#1e3a8a}}
    #     .tbl .dn{{color:#dc2626;font-weight:800}}
    #     .tbl .ok{{color:#16a34a;font-weight:700}}

    #     .risk-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}
    #     @media(max-width:580px){{risk-grid{{grid-template-columns:repeat(2,1fr)}}}}
    #     .rcard{{border-radius:12px;padding:16px 10px;text-align:center;box-shadow:0 3px 12px rgba(0,0,0,.10)}}
    #     .rcard .rico{{font-size:22px;margin-bottom:8px;display:block}}
    #     .rcard .rlbl{{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px}}
    #     .rcard .rval{{font-size:28px;font-weight:900}}
    #     .rc1{{background:linear-gradient(135deg,#fee2e2,#fca5a5);color:#7f1d1d}}
    #     .rc2{{background:linear-gradient(135deg,#fef3c7,#fde68a);color:#78350f}}
    #     .rc3{{background:linear-gradient(135deg,#fff7ed,#fed7aa);color:#7c2d12}}
    #     .rc4{{background:linear-gradient(135deg,#dbeafe,#bfdbfe);color:#1e3a8a}}

    #     .footer{{background:linear-gradient(90deg,#1e3a8a 0%,#2563eb 100%);color:#bfdbfe;padding:14px 24px;text-align:center;font-size:12px}}
    #     .footer b{{color:#fff}}
    #     </style>

    #     <div class="wrap">

    #     <div class="hdr">
    #     <div class="hdr-icon">
    #         <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><rect x="2" y="18" width="4" height="12" rx="2" fill="#60a5fa"/><rect x="9" y="12" width="4" height="18" rx="2" fill="#93c5fd"/><rect x="16" y="6" width="4" height="24" rx="2" fill="#bfdbfe"/><rect x="23" y="2" width="4" height="28" rx="2" fill="#dbeafe"/><circle cx="26" cy="3" r="3" fill="#ef4444"/></svg>
    #     </div>
    #     <h1>Network Alarm Status Report</h1>
    #     <p id="rdt">Auto-generated report</p>
    #     </div>

    #     <div class="sec-hdr sh-blue">
    #     <svg class="sec-icon" viewBox="0 0 20 20" fill="white"><path d="M9 2a7 7 0 100 14A7 7 0 009 2zm0 12.5a5.5 5.5 0 110-11 5.5 5.5 0 010 11zM9 6a1 1 0 011 1v3.586l1.707 1.707a1 1 0 01-1.414 1.414l-2-2A1 1 0 018 11V7a1 1 0 011-1z"/></svg>
    #     Overall Network Summary
    #     </div>
    #     <div class="body-pad">
    #     <div class="summary-grid">
    #         <div class="scard s4g">
    #         <span class="scard-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="3" fill="#1d4ed8"/><path d="M6.3 6.3a8 8 0 000 11.4M17.7 6.3a8 8 0 010 11.4M3.5 3.5a13 13 0 000 17M20.5 3.5a13 13 0 010 17" stroke="#1d4ed8" stroke-width="1.8" stroke-linecap="round"/></svg></span>
    #         <div class="lbl">4G Sites</div><div class="val">{{total_sites_4g}}</div><div class="sub">Total Active</div>
    #         </div>
    #         <div class="scard s5g">
    #         <span class="scard-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="3" fill="#1d4ed8"/><path d="M6.3 6.3a8 8 0 000 11.4M17.7 6.3a8 8 0 010 11.4M3.5 3.5a13 13 0 000 17M20.5 3.5a13 13 0 010 17" stroke="#1d4ed8" stroke-width="1.8" stroke-linecap="round"/></svg></span>
    #         <div class="lbl">5G Sites</div><div class="val">{{total_sites_5g}}</div><div class="sub">Total Active</div>
    #         </div>
    #         <div class="scard sa4">
    #         <span class="scard-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9M13.73 21a2 2 0 01-3.46 0" stroke="#9d174d" stroke-width="2" stroke-linecap="round"/></svg></span>
    #         <div class="lbl">4G Alarm</div><div class="val">{{alarm_4g}}</div><div class="sub">Active Alarms</div>
    #         </div>
    #         <div class="scard sa5">
    #         <span class="scard-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9M13.73 21a2 2 0 01-3.46 0" stroke="#9d174d" stroke-width="2" stroke-linecap="round"/></svg></span>
    #         <div class="lbl">5G Alarm</div><div class="val">{{alarm_5g}}</div><div class="sub">Active Alarms</div>
    #         </div>
    #         <div class="scard sd4">
    #         <span class="scard-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M18.364 5.636l-12.728 12.728M5.636 5.636l12.728 12.728" stroke="#991b1b" stroke-width="2.5" stroke-linecap="round"/></svg></span>
    #         <div class="lbl">4G Down</div><div class="val">{{down_4g}}</div><div class="sub">Unreachable</div>
    #         </div>
    #         <div class="scard sd5">
    #         <span class="scard-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" stroke="#9a3412" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
    #         <div class="lbl">5G Down</div><div class="val">{{down_5g}}</div><div class="sub">Unreachable</div>
    #         </div>
    #     </div>
    #     </div>

    #     <div class="sec-hdr sh-blue">
    #     <svg class="sec-icon" viewBox="0 0 20 20" fill="white"><path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm0 6a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1v-2zm0 6a1 1 0 011-1h6a1 1 0 010 2H4a1 1 0 01-1-1z" clip-rule="evenodd"/></svg>
    #     Cell Lock Status
    #     </div>
    #     <div class="body-pad">
    #     <div class="two-col">
    #         <div class="panel">
    #         <div class="ptitle pt4">
    #             <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M1 6l5 5 5-5M6 11V3" stroke="#15803d" stroke-width="2.2" stroke-linecap="round"/><rect x="12" y="8" width="10" height="13" rx="2" stroke="#15803d" stroke-width="2"/></svg>
    #             4G Site Status
    #         </div>
    #         <div class="gauge-row">
    #             <svg width="116" height="74" viewBox="0 0 116 74">
    #             <defs>
    #                 <linearGradient id="g4g" x1="0%" y1="0%" x2="100%" y2="0%">
    #                 <stop offset="0%" stop-color="#16a34a"/>
    #                 <stop offset="100%" stop-color="#86efac"/>
    #                 </linearGradient>
    #             </defs>
    #             <path d="M12,62 A50,50 0 0,1 104,62" fill="none" stroke="#e5e7eb" stroke-width="13" stroke-linecap="round"/>
    #             <path d="M12,62 A50,50 0 0,1 104,62" fill="none" stroke="url(#g4g)" stroke-width="13" stroke-linecap="round" stroke-dasharray="157" stroke-dashoffset="24"/>
    #             <text x="58" y="60" text-anchor="middle" font-size="17" font-weight="900" fill="#15803d">85%</text>
    #             <text x="58" y="72" text-anchor="middle" font-size="9" fill="#6b7280">locked</text>
    #             </svg>
    #             <div class="gdata">
    #             <div><b>Total Sites:</b> total_sites_4g</div>
    #             <div><b>Total Cells:</b> total_cells_4g</div>
    #             <div><b>No Alarm:</b> <span class="grn">alarm_4g</span></div>
    #             <div><b>SA Alarm:</b> <span class="amb">sa_4g</span></div>
    #             <div><b>NSA Alarm:</b> <span class="amb">nsa_4g</span></div>
    #             <div><b>Site Down:</b> <span class="red">down_4g</span></div>
    #             </div>
    #         </div>
    #         </div>
    #         <div class="panel">
    #         <div class="ptitle pt5">
    #             <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="3" fill="#1d4ed8"/><path d="M6.3 6.3a8 8 0 000 11.4M17.7 6.3a8 8 0 010 11.4" stroke="#1d4ed8" stroke-width="2" stroke-linecap="round"/></svg>
    #             5G Site Status
    #         </div>
    #         <div class="gauge-row">
    #             <svg width="116" height="74" viewBox="0 0 116 74">
    #             <defs>
    #                 <linearGradient id="g5g" x1="0%" y1="0%" x2="100%" y2="0%">
    #                 <stop offset="0%" stop-color="#1d4ed8"/>
    #                 <stop offset="100%" stop-color="#93c5fd"/>
    #                 </linearGradient>
    #             </defs>
    #             <path d="M12,62 A50,50 0 0,1 104,62" fill="none" stroke="#e5e7eb" stroke-width="13" stroke-linecap="round"/>
    #             <path d="M12,62 A50,50 0 0,1 104,62" fill="none" stroke="url(#g5g)" stroke-width="13" stroke-linecap="round" stroke-dasharray="157" stroke-dashoffset="44"/>
    #             <text x="58" y="60" text-anchor="middle" font-size="17" font-weight="900" fill="#1d4ed8">72%</text>
    #             <text x="58" y="72" text-anchor="middle" font-size="9" fill="#6b7280">locked</text>
    #             </svg>
    #             <div class="gdata">
    #             <div><b>Total Sites:</b> total_5g_sites</div>
    #             <div><b>Total Cells:</b> total_5g_cells</div>
    #             <div><b>No Alarm:</b> <span class="grn">alarm_5g</span></div>
    #             <div><b>SA Alarm:</b> <span class="amb">sa_5g</span></div>
    #             <div><b>NSA Alarm:</b> <span class="amb">nsa_5g</span></div>
    #             <div><b>Site Down:</b> <span class="red">down_5g</span></div>
    #             </div>
    #         </div>
    #         </div>
    #     </div>
    #     </div>

    #     <div class="sec-hdr sh-amber">
    #     <svg class="sec-icon" viewBox="0 0 20 20" fill="white"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
    #     Alarm Bucket
    #     </div>
    #     <div class="body-pad">
    #     <div class="two-col">
    #         <div class="panel">
    #         <div class="ptitle pt4">
    #             <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 9v4M12 17h.01" stroke="#15803d" stroke-width="2.2" stroke-linecap="round"/><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" stroke="#15803d" stroke-width="2"/></svg>
    #             4G Alarms
    #         </div>
    #         <div class="bucket-grid">
    #             <div class="bcard b-hw">
    #             <span class="bico"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="2" y="6" width="20" height="12" rx="2" stroke="white" stroke-width="2"/><path d="M6 10h.01M10 10h.01" stroke="white" stroke-width="2" stroke-linecap="round"/></svg></span>
    #             <div class="btype">HW Alarm</div><div class="bval">hw_4g</div>
    #             </div>
    #             <div class="bcard b-soft">
    #             <span class="bico"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M9 3H5a2 2 0 00-2 2v4m6-6h10a2 2 0 012 2v4M9 3v18m0 0h10a2 2 0 002-2V9M9 21H5a2 2 0 01-2-2V9m0 0h18" stroke="white" stroke-width="2" stroke-linecap="round"/></svg></span>
    #             <div class="btype">Soft Alarm</div><div class="bval">soft_4g</div>
    #             </div>
    #             <div class="bcard b-pwr">
    #             <span class="bico"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
    #             <div class="btype">Power Alarm</div><div class="bval">pwr_4g</div>
    #             </div>
    #         </div>
    #         </div>
    #         <div class="panel">
    #         <div class="ptitle pt5">
    #             <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 9v4M12 17h.01" stroke="#1d4ed8" stroke-width="2.2" stroke-linecap="round"/><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" stroke="#1d4ed8" stroke-width="2"/></svg>
    #             5G Alarms
    #         </div>
    #         <div class="bucket-grid">
    #             <div class="bcard b-hw">
    #             <span class="bico"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="2" y="6" width="20" height="12" rx="2" stroke="white" stroke-width="2"/><path d="M6 10h.01M10 10h.01" stroke="white" stroke-width="2" stroke-linecap="round"/></svg></span>
    #             <div class="btype">HW Alarm</div><div class="bval">hw_5g</div>
    #             </div>
    #             <div class="bcard b-soft">
    #             <span class="bico"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M9 3H5a2 2 0 00-2 2v4m6-6h10a2 2 0 012 2v4M9 3v18m0 0h10a2 2 0 002-2V9M9 21H5a2 2 0 01-2-2V9m0 0h18" stroke="white" stroke-width="2" stroke-linecap="round"/></svg></span>
    #             <div class="btype">Soft Alarm</div><div class="bval">soft_5g</div>
    #             </div>
    #             <div class="bcard b-pwr">
    #             <span class="bico"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
    #             <div class="btype">Power Alarm</div><div class="bval">pwr_5g</div>
    #             </div>
    #         </div>
    #         </div>
    #     </div>
    #     </div>

    #     <div class="sec-hdr sh-red">
    #     <svg class="sec-icon" viewBox="0 0 20 20" fill="white"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>
    #     Site Down
    #     </div>
    #     <div class="body-pad">
    #     <div class="two-col">
    #         <div class="panel">
    #         <div class="ptitle pt4">
    #             <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M1 6l5 5 5-5M6 11V3" stroke="#15803d" stroke-width="2" stroke-linecap="round"/></svg>
    #             4G Site Down
    #         </div>
    #         <div class="down-grid">
    #             <div class="dcard d-new">
    #             <span class="dico"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12h14" stroke="white" stroke-width="2.5" stroke-linecap="round"/></svg></span>
    #             <div class="dtype">New_Sites</div> <div class="dval"> </div>
    #             </div>
    #             <div class="dcard d-old">
    #             <span class="dico"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M12 8v4l3 3M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke="white" stroke-width="2" stroke-linecap="round"/></svg></span>
    #             <div class="dtype">Old_Sites</div><div class="dval"> </div>
    #             </div>
    #         </div>
    #         </div>
    #         <div class="panel">
    #         <div class="ptitle pt5">
    #             <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="3" fill="#1d4ed8"/><path d="M6.3 6.3a8 8 0 000 11.4M17.7 6.3a8 8 0 010 11.4" stroke="#1d4ed8" stroke-width="2" stroke-linecap="round"/></svg>
    #             5G Site Down
    #         </div>
    #         <div class="down-grid">
    #             <div class="dcard d-new">
    #             <span class="dico"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12h14" stroke="white" stroke-width="2.5" stroke-linecap="round"/></svg></span>
    #             <div class="dtype">New Sites</div><div class="dval"> </div>
    #             </div>
    #             <div class="dcard d-old">
    #             <span class="dico"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M12 8v4l3 3M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke="white" stroke-width="2" stroke-linecap="round"/></svg></span>
    #             <div class="dtype">Old Sites</div><div class="dval"> </div>
    #             </div>
    #         </div>
    #         </div>
    #     </div>
    #     </div>

    #     # <div class="sec-hdr sh-green">
    #     # <svg class="sec-icon" viewBox="0 0 20 20" fill="white"><path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/></svg>
    #     # 4G Circle-wise Summary
    #     # </div>
    #     # <div class="body-pad">
    #     # <div class="tbl-wrap">
    #     #     <table class="tbl">
    #     #     <thead><tr><th>Circle</th><th>4G Sites</th><th>SA</th><th>NSA</th><th>Alarm</th><th>Site Down</th></tr></thead>
    #     #     <tbody>
    #     #         <tr><td>AP</td><td>180</td><td class="ok">60</td><td class="ok">45</td><td>28</td><td class="dn">3</td></tr>
    #     #         <tr><td>MH</td><td>210</td><td class="ok">80</td><td class="ok">55</td><td>32</td><td class="dn">4</td></tr>
    #     #         <tr><td>UP East</td><td>160</td><td class="ok">50</td><td class="ok">40</td><td>22</td><td class="dn">2</td></tr>
    #     #         <tr><td>UP West</td><td>140</td><td class="ok">45</td><td class="ok">35</td><td>18</td><td class="dn">3</td></tr>
    #     #         <tr><td>KA</td><td>195</td><td class="ok">70</td><td class="ok">50</td><td>30</td><td class="dn">6</td></tr>
    #     #         <tr><td>Total</td><td>1,240</td><td class="ok">305</td><td class="ok">225</td><td>130</td><td class="dn">18</td></tr>
    #     #     </tbody>
    #     #     </table>
    #     # </div>
    #     # </div>

    #     # <div class="sec-hdr sh-indigo">
    #     # <svg class="sec-icon" viewBox="0 0 20 20" fill="white"><path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/></svg>
    #     # 5G Circle-wise Summary
    #     # </div>
    #     # <div class="body-pad">
    #     # <div class="tbl-wrap">
    #     #     <table class="tbl">
    #     #     <thead><tr><th>Circle</th><th>5G Sites</th><th>SA</th><th>NSA</th><th>Alarm</th><th>Site Down</th></tr></thead>
    #     #     <tbody>
    #     #         <tr><td>AP</td><td>120</td><td class="ok">44</td><td class="ok">30</td><td>18</td><td class="dn">2</td></tr>
    #     #         <tr><td>MH</td><td>185</td><td class="ok">65</td><td class="ok">42</td><td>24</td><td class="dn">3</td></tr>
    #     #         <tr><td>UP East</td><td>110</td><td class="ok">38</td><td class="ok">26</td><td>15</td><td class="dn">2</td></tr>
    #     #         <tr><td>UP West</td><td>105</td><td class="ok">35</td><td class="ok">24</td><td>12</td><td class="dn">1</td></tr>
    #     #         <tr><td>KA</td><td>140</td><td class="ok">50</td><td class="ok">36</td><td>17</td><td class="dn">3</td></tr>
    #     #         <tr><td>Total</td><td>860</td><td class="ok">232</td><td class="ok">158</td><td>86</td><td class="dn">11</td></tr>
    #     #     </tbody>
    #     #     </table>
    #     # </div>
    #     # </div>

    #     <div class="sec-hdr sh-red">
    #     <svg class="sec-icon" viewBox="0 0 20 20" fill="white"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
    #     Old VS New Site Status
    #     </div>
    #     <div class="body-pad" style="background:#fff">
    #     <div class="risk-grid">
    #         <div class="rcard rc1">
    #         <span class="rico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="#991b1b" stroke-width="2"/><path d="M12 8v4M12 16h.01" stroke="#991b1b" stroke-width="2" stroke-linecap="round"/></svg></span>
    #         <div class="rlbl">Total NO. of Cells</div>
    #         <div class="rval"></div>
    #         <div style="font-size:11px;margin-top:5px;opacity:.75">Over 7 Days</div>
    #         </div>
    #         <div class="rcard rc2">
    #         <span class="rico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M1 6l5 5 5-5M6 11V3" stroke="#92400e" stroke-width="2.2" stroke-linecap="round"/><rect x="12" y="8" width="10" height="13" rx="2" stroke="#92400e" stroke-width="2"/></svg></span>
    #         <div class="rlbl">Both Cell Locked(New VS Old)</div>
    #         <div class="rval"> </div>
    #         <div style="font-size:11px;margin-top:5px;opacity:.75">High Impact</div>
    #         </div>
    #         <div class="rcard rc3">
    #         <span class="rico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" stroke="#9a3412" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
    #         <div class="rlbl">Both Cell Unlocked(New VS Old)</div>
    #         <div style="font-size:13px;font-weight:800;color:#7c2d12;margin-top:5px;line-height:1.3">Escalate<br>Power Issue</div>
    #         </div>
    #         <div class="rcard rc4">
    #         <span class="rico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none"><rect x="3" y="4" width="18" height="18" rx="2" stroke="#1e3a8a" stroke-width="2"/><path d="M16 2v4M8 2v4M3 10h18" stroke="#1e3a8a" stroke-width="2" stroke-linecap="round"/><path d="M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01" stroke="#1e3a8a" stroke-width="2" stroke-linecap="round"/></svg></span>
    #         <div class="rlbl">Total Impacted Sites</div>
    #         <div style="font-size:13px;font-weight:800;color:#7c2d12;margin-top:5px;line-height:1.3">Escalate<br>Power Issue</div>

    #         # <div style="font-size:14px;font-weight:900;color:#1e3a8a;margin-top:5px">May 30, 2024</div>
    #         # <div style="font-size:10px;margin-top:4px;opacity:.7">Full Closure</div>
    #         </div>
    #     </div>
    #     </div>

    #     <div class="footer">
    #     <p>PFA the detailed alarm report as attachment.</p>
    #     <p style="margin-top:6px">Regards &nbsp;·&nbsp; <b>Developer Team</b> &nbsp;·&nbsp; <b>(Auto Mail)</b></p>
    #     </div>

    #     </div>
    #     <script>
    #     document.getElementById('rdt').textContent = 'Auto-generated · ' + new Date().toLocaleString('en-IN',dateStyle:'long',timeStyle:'short');
    #     </script>


    #     </body>
    #     </html>
    #     """









# import os
# import win32com.client
# import pythoncom
# import requests
# import zipfile
# import py7zr
# import shutil
# from datetime import datetime
# from celery import shared_task
# from mcom_website.settings import MEDIA_ROOT
# from mailapp.tasks import send_email
# import pandas as pd  # make sure this is your Celery email task

# save_directory = os.path.join(MEDIA_ROOT, "Universal_alarm", "attachments")
# LAST_PROCESSED_FILE = os.path.join(MEDIA_ROOT, "Universal_alarm", "last_mail.txt")

# import pandas as pd

# def get_summary_counts(excel_path):
#     sheets = pd.read_excel(excel_path, sheet_name=None)

#     # ================= SHEETS =================
#     cells_4g = sheets.get("4G Cells")
#     cells_5g = sheets.get("5G Cells")

#     alarm_4g_df = sheets.get("4G Alarms")
#     alarm_5g_df = sheets.get("5G Alarms")

#     site_down_4g_df = sheets.get("4G Site Down")
#     site_down_5g_df = sheets.get("5G Site Down")

#     # ================= INITIALIZE =================
#     total_sites_4g = set()
#     total_sites_5g = set()

#     # SA / NSA split
#     sa_4g = 0
#     nsa_4g = 0
#     sa_5g = 0
#     nsa_5g = 0

#     # Alarm
#     alarm_4g = 0
#     alarm_5g = 0

#     # Site Down
#     down_4g = 0
#     down_5g = 0

#     # ================= TOTAL 4G SITES =================
#     if cells_4g is not None:
#         for _, row in cells_4g.iterrows():
#             site = row.get("4G Site ID", "")
#             if pd.notna(site) and site != "":
#                 total_sites_4g.add(site)

#     # ================= TOTAL 5G SITES =================
#     if cells_5g is not None:
#         for _, row in cells_5g.iterrows():
#             site = row.get("5G Site ID", "")
#             if pd.notna(site) and site != "":
#                 total_sites_5g.add(site)

#     # ================= 4G ALARMS =================
#     if alarm_4g_df is not None and "Alarm/No Alarm" in alarm_4g_df.columns:
#         alarm_4g = alarm_4g_df["Alarm/No Alarm"] \
#             .astype(str) \
#             .str.strip() \
#             .str.upper() \
#             .eq("ALARM") \
#             .sum()


#         # SA / NSA
#         if "SA/NSA" in alarm_4g_df.columns:
#             sa_4g = (
#                 alarm_4g_df["SA/NSA"]
#                 .astype(str)
#                 .str.strip()
#                 .str.upper()
#                 .eq("SA")
#                 .sum()
#             )

#             nsa_4g = (
#                 alarm_4g_df["SA/NSA"]
#                 .astype(str)
#                 .str.strip()
#                 .str.upper()
#                 .eq("NSA")
#                 .sum()
#             )

#     # ================= 5G ALARMS =================
#     if alarm_5g_df is not None and "Alarm/No Alarm" in alarm_5g_df.columns:
#         alarm_5g = alarm_5g_df["Alarm/No Alarm"] \
#             .astype(str) \
#             .str.strip() \
#             .str.upper() \
#             .eq("ALARM") \
#             .sum()
    
#         # SA / NSA
#         if "SA/NSA" in alarm_5g_df.columns:
#             sa_5g = (
#                 alarm_5g_df["SA/NSA"]
#                 .astype(str)
#                 .str.strip()
#                 .str.upper()
#                 .eq("SA")
#                 .sum()
#             )

#             nsa_5g = (
#                 alarm_5g_df["SA/NSA"]
#                 .astype(str)
#                 .str.strip()
#                 .str.upper()
#                 .eq("NSA")
#                 .sum()
#             )

#     # ================= 4G SITE DOWN =================
#     if site_down_4g_df is not None and "Status" in site_down_4g_df.columns:
#         down_4g = (
#             site_down_4g_df["Status"]
#             .astype(str)
#             .str.upper()
#             .str.contains("UNABLE TO CONNECT")
#             .sum()
#         )

#     # ================= 5G SITE DOWN =================
#     if site_down_5g_df is not None and "Status" in site_down_5g_df.columns:
#         down_5g = (
#             site_down_5g_df["Status"]
#             .astype(str)
#             .str.upper()
#             .str.contains("UNABLE TO CONNECT")
#             .sum()
#         )

#     # ================= TOTALS =================
#     total_alarm = alarm_4g + alarm_5g
#     total_site_down = down_4g + down_5g

#     total_sa = sa_4g + sa_5g
#     total_nsa = nsa_4g + nsa_5g

#     # ================= RETURN =================
#     return {
#         "total_4g_sites": len(total_sites_4g),
#         "total_5g_sites": len(total_sites_5g),

#         # SA/NSA split
#         "SA_4G": int(sa_4g),
#         "NSA_4G": int(nsa_4g),
#         "SA_5G": int(sa_5g),
#         "NSA_5G": int(nsa_5g),

#         "SA": int(total_sa),
#         "NSA": int(total_nsa),

#         # Alarm
#         "Alarm_4G": int(alarm_4g),
#         "Alarm_5G": int(alarm_5g),
#         "Alarm": int(total_alarm),

#         # Site Down
#         "Site_Down_4G": int(down_4g),
#         "Site_Down_5G": int(down_5g),
#         "Site Down": int(total_site_down),
#     }


# def is_new_mail(unique_id):
#     if not os.path.exists(LAST_PROCESSED_FILE):
#         return True
#     with open(LAST_PROCESSED_FILE, "r") as f:
#         last_id = f.read().strip()
#     return unique_id != last_id

# def save_last_mail(unique_id):
#     if not os.path.exists(os.path.dirname(LAST_PROCESSED_FILE)):
#         os.makedirs(os.path.dirname(LAST_PROCESSED_FILE))
#     with open(LAST_PROCESSED_FILE, "w") as f:
#         f.write(unique_id)

# @shared_task
# def check_outlook_mail(expected_subject="MS2 Pending Sites"):
#     # pythoncom.CoInitialize()
#     outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
#     inbox = outlook.Folders.Item("Prerna.PramodKumar@ust.com").Folders["Inbox"]

#     messages = inbox.Items
#     messages.Sort("[ReceivedTime]", True)
#     latest_mail = messages.GetFirst()

#     if not latest_mail:
#         return None

#     unique_id = f"{latest_mail.Subject}|{latest_mail.SenderEmailAddress}|{latest_mail.ReceivedTime}"
#     if not is_new_mail(unique_id):
#         print("⚠️ Already processed this mail, skipping...")
#         return None

#     subject = str(latest_mail.Subject)
#     print(f"Latest mail => {subject}")

#     if expected_subject.lower() in subject.lower():
#         if latest_mail.Attachments.Count > 0:
#             # 🔹 Clean old attachments before saving new one-----
#             if os.path.exists(save_directory):
#                 for old_file in os.listdir(save_directory):
#                     old_path = os.path.join(save_directory, old_file)
#                     if os.path.isfile(old_path):
#                         os.remove(old_path)
#                     elif os.path.isdir(old_path):
#                         shutil.rmtree(old_path)

#             for att in latest_mail.Attachments:
#                 if att.FileName.endswith((".zip", ".7z")):
#                     if not os.path.exists(save_directory):
#                         os.makedirs(save_directory)    
#                     file_path = os.path.join(save_directory, att.FileName)
#                     att.SaveAsFile(file_path)
#                     print(" Zip downloaded:", file_path)

#                     save_last_mail(unique_id)

#                     process_daily_circle_logs(
#                         file_path,
#                         to_address=latest_mail.To,
#                         cc_mails=latest_mail.CC,
#                     )

#                     return {
#                         "file_path": file_path,
#                         "to": latest_mail.To,
#                         "cc": latest_mail.CC,
#                         "subject": subject,
#                         "received_time": str(latest_mail.ReceivedTime),
#                     }
#     return None

# def process_daily_circle_logs(file_path,to_address=None, cc_mails=None):
#     print("CC called process_daily_circle_logs", cc_mails)
#     print(file_path,"file path.................................."   )
#     today_str = datetime.today().strftime("%Y-%m-%d")
#     output_root = os.path.join(MEDIA_ROOT, "Universal_alarm", "daily_status_alarm")

#     # 🔹 Purane output zips delete karo
#     if os.path.exists(output_root):
#         for item in os.listdir(output_root):
#             item_path = os.path.join(output_root, item)
#             if os.path.isdir(item_path):
#                 shutil.rmtree(item_path)   # purana folder delete---
#             elif item.endswith(".zip"):
#                 os.remove(item_path)  # purana zip delete

#     zip_files = [f for f in os.listdir(save_directory) if f.endswith((".zip", ".7z"))]
#     if not zip_files:
#         print("No zip files found to process")
#         return

#     zip_file = os.path.join(save_directory, zip_files[-1])
#     # ✅ Use os.path.splitext for safe folder name
#     extract_dir = os.path.splitext(zip_file)[0]
#     print(" Processing latest zip:", zip_file)

#     # extract_dir = zip_file.replace(".zip", "")
#     if os.path.exists(extract_dir):
#         shutil.rmtree(extract_dir, ignore_errors=True)   #add this line to remove existing directory before creating a new one
#     os.makedirs(extract_dir, exist_ok=True)

#     if zip_file.endswith(".zip"):
#         with zipfile.ZipFile(zip_file, "r") as zip_ref:
#             zip_ref.extractall(extract_dir)
#     elif zip_file.endswith(".7z"):
#         with py7zr.SevenZipFile(zip_file, "r") as archive:
#             archive.extractall(extract_dir)
#     else:
#         raise ValueError(f"Unsupported file format: {zip_file}")

#     print(f" Extracted to {extract_dir}")

#     daily_status_folder = os.path.join(MEDIA_ROOT, "Universal_alarm", "daily_status_alarm", today_str)
#     os.makedirs(daily_status_folder, exist_ok=True)

#     circles_path = os.path.join(extract_dir, extract_dir.split("\\")[-1])
#     for circle in os.listdir(circles_path):
#         circle_path = os.path.join(circles_path, circle)
#         print(circle_path,"circle path.....................................")
#         if not os.path.isdir(circle_path):
#             print("invalid cricle path.....................................")
#             continue

#         log_files = []
#         for file_name in os.listdir(circle_path):
#             file_path = os.path.join(circle_path, file_name)
#             if os.path.isfile(file_path):
#                 with open(file_path, "rb") as f:
#                     log_files.append(("log_files", (file_name, f.read())))

#         print(f" Uploading logs for circle: {circle}, Files: {len(log_files)}")
#         if not log_files:
#             continue

#         response_4G = requests.post(
#             "http://127.0.0.1:8001/universal_alarm/upload_4g/",
#             files=log_files,
#             data={"circle": circle},
#         )
#         response_5G = requests.post(
#             "http://127.0.0.1:8001/universal_alarm/upload_5g/",
#             files=log_files,
#             data={"circle": circle},
#         )
#         print(f" API Response for {circle}: 4G={response_4G.status_code}, 5G={response_5G.status_code}")

#     zip_output_path = f"{daily_status_folder}.zip"
#     shutil.make_archive(daily_status_folder, "zip", daily_status_folder)
#     print(f" Zipped daily status folder → {zip_output_path}")


#     # ================= SUMMARY =================
#     circle_summary = {}

#     overall_summary = {
#         "total_4g_sites": 0,
#         "total_5g_sites": 0,

#         "SA_4G": 0, "NSA_4G": 0,
#         "SA_5G": 0, "NSA_5G": 0,

#         "Alarm_4G": 0, "Alarm_5G": 0,
#         "Site_Down_4G": 0, "Site_Down_5G": 0,
#     }

#     for root, _, files in os.walk(daily_status_folder):
#         for file in files:
#             if file.endswith(".xlsx"):
#                 excel_path = os.path.join(root, file)
#                 circle = os.path.basename(root)

#                 summary = get_summary_counts(excel_path)

#                 if circle not in circle_summary:
#                     circle_summary[circle] = {k: 0 for k in summary.keys()}

#                 for key in summary:
#                     circle_summary[circle][key] += summary[key]

#                     if key in overall_summary:
#                         overall_summary[key] += summary[key]
    
#     zip_output_path = f"{daily_status_folder}.zip"
#     shutil.make_archive(daily_status_folder, "zip", daily_status_folder)

#     body = f"""
#     <html>
#     <body style="font-family: Arial, sans-serif;">

#     <p>Hi Team,</p>

#     <h2 style="color:#2E86C1;">📊 Overall Network Summary</h2>

#     <table cellspacing="10">
#     <tr>

#     <td style="background:#E8F6F3;padding:15px;border-radius:10px;">
#     <b>📶 4G Sites</b><br>
#     <span style="font-size:20px;">{overall_summary['total_4g_sites']}</span>
#     </td>

#     <td style="background:#EBF5FB;padding:15px;border-radius:10px;">
#     <b>📡 5G Sites</b><br>
#     <span style="font-size:20px;">{overall_summary['total_5g_sites']}</span>
#     </td>

#     <td style="background:#FEF9E7;padding:15px;border-radius:10px;">
#     <b>🚨 4G Alarm</b><br>
#     <span style="font-size:20px;">{overall_summary['Alarm_4G']}</span>
#     </td>

#     <td style="background:#FDEDEC;padding:15px;border-radius:10px;">
#     <b>🚨 5G Alarm</b><br>
#     <span style="font-size:20px;">{overall_summary['Alarm_5G']}</span>
#     </td>

#     <td style="background:#FADBD8;padding:15px;border-radius:10px;">
#     <b>🔴 4G Down</b><br>
#     <span style="font-size:20px;color:red;">
#     <b>{overall_summary['Site_Down_4G']}</b>
#     </span>
#     </td>

#     <td style="background:#F5B7B1;padding:15px;border-radius:10px;">
#     <b>🔴 5G Down</b><br>
#     <span style="font-size:20px;color:red;">
#     <b>{overall_summary['Site_Down_5G']}</b>
#     </span>
#     </td>

#     </tr>
#     </table>

#     <br>

#     <h3 style="color:#117A65;">📶 4G Circle Summary</h3>

#     <table border="1" cellspacing="0" cellpadding="8" style="border-collapse:collapse;width:80%;">
#     <tr style="background-color:#117A65; color:white;">
#     <th>Circle</th>
#     <th>4G Sites</th>
#     <th>SA</th>
#     <th>NSA</th>
#     <th>Alarm</th>
#     <th>Site Down</th>
#     </tr>
#     """

#     for i, (circle, data) in enumerate(circle_summary.items()):
#         row_color = "#f9f9f9" if i % 2 == 0 else "#ffffff"

#         body += f"""
#     <tr style="background-color:{row_color};">
#     <td><b>{circle}</b></td>
#     <td>{data.get('total_4g_sites',0)}</td>
#     <td style="color:green;"><b>{data.get('SA_4G',0)}</b></td>
#     <td style="color:green;"><b>{data.get('NSA_4G',0)}</b></td>
#     <td>{data.get('Alarm_4G',0)}</td>
#     <td style="color:red;"><b>{data.get('Site_Down_4G',0)}</b></td>
#     </tr>
#     """

#     body += """
#     </table>

#     <br>

#     <h3 style="color:#1F618D;">📡 5G Circle Summary</h3>

#     <table border="1" cellspacing="0" cellpadding="8" style="border-collapse:collapse;width:90%;">
#     <tr style="background-color:#1F618D; color:white;">
#     <th>Circle</th>
#     <th>5G Sites</th>
#     <th>SA</th>
#     <th>NSA</th>
#     <th>Alarm</th>
#     <th>Site Down</th>
#     </tr>
#     """

#     for i, (circle, data) in enumerate(circle_summary.items()):
#         row_color = "#f2f6fc" if i % 2 == 0 else "#ffffff"

#         body += f"""
#     <tr style="background-color:{row_color};">
#     <td><b>{circle}</b></td>
#     <td>{data.get('total_5g_sites',0)}</td>
#     <td style="color:green;"><b>{data.get('SA_5G',0)}</b></td>
#     <td style="color:green;"><b>{data.get('NSA_5G',0)}</b></td>
#     <td>{data.get('Alarm_5G',0)}</td>
#     <td style="color:red;"><b>{data.get('Site_Down_5G',0)}</b></td>
#     </tr>
#     """

#     body += """
#     </table>

#     <br>

#     <p style="color:gray;">PFA the detailed report.</p>

#     <p>
#     Regards,<br>
#     <b>Developer Team</b><br>
#     (Auto Mail)
#     </p>

#     </body>
#     </html>
#     """

#     to_address=';'.join(['Amit.Rai@ust.com','Abhinav.Verma@ust.com','Deepu.Sharma@ust.com','Praveen.Lakra@ust.com','Gulafsha.Bano@ust.com','Priyanshi.Sharma@ust.com'])
#     cc_mails = ';'.join(['Mohit.Batra@ust.com','Shashank.Rai@ust.com','Chirag.Bohara@ust.com','Prerna.PramodKumar@ust.com'])

#     send_email.delay(
#         to_address=to_address,
#         cc_mails=cc_mails,
#         subject="📊 Processed Alarm Report",
#         body=body,
#         attachment_path=zip_output_path,
#         is_html=True,
#     )

