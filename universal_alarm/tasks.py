import os
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

import imaplib
import email
import io
import smtplib
from email.mime.text import MIMEText
from email.header import decode_header


EMAIL       = "noreply@mcpspmis.com"
PASSWORD    = "Mcom@#2027"
IMAP_SERVER = "imap.secureserver.net"
IMAP_PORT   = 993


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
    print("This function is call")
    # try:
        # ── Connect to Titan IMAP ──────────────────────────
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL, PASSWORD)
    mail.select("INBOX")

    # ── Search latest mail with subject ───────────────

    # today = date.today().strftime("%d-%b-%Y")
    today = datetime.now().strftime("%d-%b-%Y")
    status, messages = mail.search(None, f'ON {today} SUBJECT "MS2 PENDING SITES"')

    if status != "OK" or not messages[0]:
        print("No matching mail found today.")
        mail.logout()
        return None

    # Latest mail (last in list)
    mail_ids = messages[0].split()
    latest_id = mail_ids[-1]

    # ── Fetch the mail ─────────────────────────────────
    status, msg_data = mail.fetch(latest_id, "(RFC822)")
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)

    # ── Extract fields ─────────────────────────────────
    subject = decode_header(msg["Subject"])[0][0]
    if isinstance(subject, bytes):
        subject = subject.decode()

    sender = msg.get("From", "")
    to_address = msg.get("To", "")
    cc_mails = msg.get("Cc", "")
    received_time = msg.get("Date", "")

    print(f"Latest mail => {subject}")

    # ── Duplicate check ────────────────────────────────
    unique_id = f"{subject}|{sender}|{received_time}"
    if not is_new_mail(unique_id):
        print("⚠️ Already processed this mail, skipping...")
        mail.logout()
        return None

    # ── Process attachments ────────────────────────────
    if expected_subject.lower() in subject.lower():

        # Clean old attachments
        if os.path.exists(save_directory):
            for old_file in os.listdir(save_directory):
                old_path = os.path.join(save_directory, old_file)
                if os.path.isfile(old_path):
                    os.remove(old_path)
                elif os.path.isdir(old_path):
                    shutil.rmtree(old_path)

        for part in msg.walk():
            filename = part.get_filename()
            if not filename:
                continue

            # Decode filename if needed
            decoded = decode_header(filename)[0][0]
            if isinstance(decoded, bytes):
                filename = decoded.decode()

            if filename.endswith((".zip", ".7z")):
                if not os.path.exists(save_directory):
                    os.makedirs(save_directory)

                file_path = os.path.join(save_directory, filename)
                with open(file_path, "wb") as f:
                    f.write(part.get_payload(decode=True))

                print("Zip downloaded:", file_path)
                save_last_mail(unique_id)

                mail.logout()

                process_daily_circle_logs(file_path,to_address=to_address,cc_mails=cc_mails,)

                return {
                    "file_path": file_path,
                    "to": to_address,
                    "cc": cc_mails,
                    "subject": subject,
                    "received_time": received_time,
                }

    mail.logout()
    return None

    # except Exception as e:
    #     print(f"❌ IMAP Error: {e}")
    # return None




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
            "https://commtoolapi.mcpspmis.com/universal_alarm/upload_4g/",
            files=log_files,
            data={"circle": circle},
        )
        response_5G = requests.post(
            "https://commtoolapi.mcpspmis.com/universal_alarm/upload_5g/",
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
        "sa_4g": 0, "nsa_4g": 0,
        "sa_5g": 0, "nsa_5g": 0,
        "no_alarm_4g": 0, "no_alarm_5g": 0,
        "site_down_4g": 0, "site_down_5g": 0,
        "old_down_5g": 0, "old_down_4g": 0,
        "hw_alarm_4g": 0, "soft_alarm_4g": 0, "PWR_4G": 0,
        "hw_alarm_5g": 0, "soft_alarm_5g": 0, "PWR_5G": 0,
        "Cells_4G": 0, "Cells_5G": 0,
        "No_Alarm_Pct_4G": 0.0, "No_alarm_Pct_5G": 0.0,
        "Total_No_of_Cells": 0,
        "Total_Both_Unlocked": 0,
        "Total_Both_Locked": 0,
        "total_impacted_sites": 0,
    }
 
    circle_email_map = {
       
        "AP": [
            "Chirag.Bohara@ust.com",
            "Priyanshi.Sharma@ust.com",
            "TES_IN_PAG@UST.com",
            "Praveen.Lakra@ust.com",
            "Deepu.Sharma@ust.com",
            "Gulafsha.Bano@ust.com",
            "Amit.Rai@ust.com",
            "Aashish.Sharma@ust.com",
            "Ramesh.ThodaDurga@ust.com",
            "LingisettyVenkata.Kumar@ust.com",
            "Munuru.Babu@ust.com",
            "RudraHari.Krishna@ust.com",
            "Shashank.Rai@ust.com",
            "TES_IN_SOFT_AT@UST.com",
            "NeerajKumar.Mishra@ust.com",
            "Naresh.Kumar@ust.com",
        ],
 
        "JK": [
            "Chirag.Bohara@ust.com",
            "Priyanshi.Sharma@ust.com",
            "TES_IN_PAG@UST.com",
            "Praveen.Lakra@ust.com",
            "Deepu.Sharma@ust.com",
            "Gulafsha.Bano@ust.com",
            "Amit.Rai@ust.com",
            "Aashish.Sharma@ust.com",
            "Ramesh.ThodaDurga@ust.com",
            "LingisettyVenkata.Kumar@ust.com",
            "Munuru.Babu@ust.com",
            "RudraHari.Krishna@ust.com",
            "Shashank.Rai@ust.com",
            "TES_IN_SOFT_AT@UST.com",
           
        ],
 
        "DL": [
            "Chirag.Bohara@ust.com",
            "Priyanshi.Sharma@ust.com",
            "TES_IN_PAG@UST.com",
            "Praveen.Lakra@ust.com",
            "Deepu.Sharma@ust.com",
            "Gulafsha.Bano@ust.com",
            "Amit.Rai@ust.com",
            "Aashish.Sharma@ust.com",
            "Prateek.Saxena@ust.com",
            "Vijay.Kumar2@ust.com",
            "Shri.Kumar@ust.com",
            "Shashank.Rai@ust.com",
            "TES_IN_SOFT_AT@UST.com",
            "Suman.Raman@ust.com",
            "Satyam.Singh3@ust.com",
        ],
 
        "HRY": [
            "Chirag.Bohara@ust.com",
            "Priyanshi.Sharma@ust.com",
            "TES_IN_PAG@UST.com",
            "Praveen.Lakra@ust.com",
            "Deepu.Sharma@ust.com",
            "Gulafsha.Bano@ust.com",
            "Amit.Rai@ust.com",
            "Aashish.Sharma@ust.com",
            "Umair.Wali@ust.com",
            "Anil.Sharma@ust.com",
            "Somnath.OmParkash@ust.com",
            "Shashank.Rai@ust.com",
            "TES_IN_SOFT_AT@UST.com",
            "Anoop.SheshveerSingh@ust.com",
        ],
 
        "RJ": [
            "Chirag.Bohara@ust.com",
            "Priyanshi.Sharma@ust.com",
            "TES_IN_PAG@UST.com",
            "Praveen.Lakra@ust.com",
            "Deepu.Sharma@ust.com",
            "Gulafsha.Bano@ust.com",
            "Amit.Rai@ust.com",
            "Aashish.Sharma@ust.com",
            "Manoj.Vishwakarma@ust.com",
            "Raju.Maheshwari@ust.com",
            "Pushkar.VimaljaKantShukla@ust.com",
            "Shashank.Rai@ust.com",
            "TES_IN_SOFT_AT@UST.com",
            "Amit.SomDutt@ust.com",
            "Shubham.Kaushik@ust.com",
           
        ],
 
        "KK": [
            "Chirag.Bohara@ust.com",
            "Priyanshi.Sharma@ust.com",
            "TES_IN_PAG@UST.com",
            "Praveen.Lakra@ust.com",
            "Deepu.Sharma@ust.com",
            "Gulafsha.Bano@ust.com",
            "Amit.Rai@ust.com",
            "Aashish.Sharma@ust.com",
            "Shashank.Rai@ust.com",
            "Santosh.Arsid@ust.com",
            "Gaurav.Ranjan@ust.com",
            "TES_IN_SOFT_AT@UST.com",
            "Amit.SomDutt@ust.com",
            "Shubham.Kaushik@ust.com",
        ],
 
        "NESA": [
            "Chirag.Bohara@ust.com",
            "Priyanshi.Sharma@ust.com",
            "TES_IN_PAG@UST.com",
            "Praveen.Lakra@ust.com",
            "Deepu.Sharma@ust.com",
            "Gulafsha.Bano@ust.com",
            "Amit.Rai@ust.com",
            "Aashish.Sharma@ust.com",
            "Shashank.Rai@ust.com",
            "Rakesh.Sarma@ust.com",
            "Sumit.Das@ust.com",
            "Ranjit.Kumar@ust.com",
            "TES_IN_SOFT_AT@UST.com",
            "Shubham.Kaushik@ust.com",
        ],
 
        "CHN": [
            "Chirag.Bohara@ust.com",
            "Priyanshi.Sharma@ust.com",
            "TES_IN_PAG@UST.com",
            "Praveen.Lakra@ust.com",
            "Deepu.Sharma@ust.com",
            "Gulafsha.Bano@ust.com",
            "Amit.Rai@ust.com",
            "Aashish.Sharma@ust.com",
            "Shashank.Rai@ust.com",
            "A.Hariharasudhan@ust.com",
            "Ajith.Thiyagarajesh@ust.com",
            "Arunprasad.Palanisamy@ust.com",
            "Saravanan.Jeyaramamn@ust.com",
            "TES_IN_SOFT_AT@UST.com",
            "Anoop.SheshveerSingh@ust.com",
            "AjayKumar.Patel@ust.com"
        ],
 
        "UPW": [
            "Chirag.Bohara@ust.com",
            "Priyanshi.Sharma@ust.com",
            "TES_IN_PAG@UST.com",
            "Praveen.Lakra@ust.com",
            "Deepu.Sharma@ust.com",
            "Gulafsha.Bano@ust.com",
            "Amit.Rai@ust.com",
            "Aashish.Sharma@ust.com",
            "Shashank.Rai@ust.com",
            "Sanjay.Pandey2@ust.com",
            "Devendar.Kumar@ust.com",
            "Praval.Joshi@ust.com",
            "TES_IN_SOFT_AT@UST.com",
            "Ankit.Yadav@ust.com",
        ],
    }
 
    for root, _, files in os.walk(daily_status_folder):
 
        excel_files = [f for f in files if f.endswith(".xlsx")]
        if not excel_files:
            continue
 
        circle = os.path.basename(root).upper()
 
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
 
        context = {
            **final_summary,
            "generated_time": datetime.now().strftime("%d %B %Y, %I:%M %p"),
            "circle_summary": {circle: final_summary},
            "circle_name": circle.upper(),
            "brand":"Ericsson"
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
 
        # ================= FIXED MAIL LOGIC =================
        emails = circle_email_map.get(circle, [])
 
        if not emails:
            print(f"No emails configured for circle {circle}")
            continue
 
        reply_subject = (
            f"📊Ericsson Alarm Status-{circle}"
        )
 
        to_address = ';'.join(emails)
 
        cc_mails = ';'.join([
                "TES_IN_NH@UST.com",
            ])
        to_address = "Vishal.Yadav@ust.com"
        cc_mails = "Prerna.PramodKumar@ust.com"
        send_email(
            to_address=to_address,
            cc_mails=cc_mails,
            subject=reply_subject,
            body=body,
            attachment_path=zip_output_path,
            is_html=True,
        )
 
        print(f"✅ Mail Sent for Circle => {circle}")

