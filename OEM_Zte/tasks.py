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
import re

current_time = datetime.now().strftime("%d %B %Y, %I:%M %p")

save_directory = os.path.join(MEDIA_ROOT, "ZTE_OUTPUT", "attachments")
LAST_PROCESSED_FILE = os.path.join(MEDIA_ROOT, "ZTE_OUTPUT", "last_mail.txt")

def get_summary_counts(excel_path):
    sheets = pd.read_excel(excel_path, sheet_name=None)

    # ================= SHEETS =================
    cells_4g = sheets.get("4G")
    alarm_df = sheets.get("Alarms")
    old_new_4g_df = sheets.get("4G Old vs New")
    # ================= BOTH LOCK / UNLOCK COUNT =================
    cells_set_4g = set()
    sites_set_4g = set()

    cells_set_5g = set()
    sites_set_5g = set()

    both_locked_cells_4g = set()
    both_unlocked_cells_4g = set()
    both_locked_sites_4g = set()
    both_unlocked_sites_4g = set()

    both_locked_cells_5g = set()
    both_unlocked_cells_5g = set()
    both_locked_sites_5g = set()
    both_unlocked_sites_5g = set()


    # ================= 4G OLD VS NEW =================
    if old_new_4g_df is not None:

        for _, row in old_new_4g_df.iterrows():

            old_cell = str(
                row.get("Cell Name_old", "")
            ).strip()

            new_cell = str(
                row.get("Cell Name_new", "")
            ).strip()

            old_site = str(
                row.get("SiteId_old", "")
            ).strip()

            new_site = str(
                row.get("SiteId_new", "")
            ).strip()

            lock_status = str(
                row.get("Lock Status", "")
            ).strip()

            # total unique new cells
            if new_cell != "":
                cells_set_4g.add(new_cell)

            # total sites
            if old_site != "":
                sites_set_4g.add(old_site)

            if new_site != "":
                sites_set_4g.add(new_site)

            # Both Locked
            if (
                old_cell != ""
                and new_cell != ""
                and lock_status == "Both Locked"
            ):

                both_locked_cells_4g.update(
                    [old_cell, new_cell]
                )

                both_locked_sites_4g.add(
                    (old_site, new_site)
                )

            # Both Unlocked
            elif (
                old_cell != ""
                and new_cell != ""
                and lock_status == "Both Unlocked"
            ):

                both_unlocked_cells_4g.update(
                    [old_cell, new_cell]
                )

                both_unlocked_sites_4g.add(
                    (old_site, new_site)
                )


    print("Total UNIQUE Cells 4G:", len(cells_set_4g))
    print("Both Locked Cells 4G:", len(both_locked_cells_4g))
    print("Both Unlocked Cells 4G:", len(both_unlocked_cells_4g))
    print("Both Locked Sites 4G:", len(both_locked_sites_4g))
    print("Both Unlocked Sites 4G:", len(both_unlocked_sites_4g))

    # ================= 4G UNIQUE NEW SITE =================
    total_sites_4g = set()

    if alarm_df is not None:

        for _, row in alarm_df.iterrows():

            status = str(
                row.get("Site Status", "")
            ).strip().lower()

            if status == "new site":

                site = row.get("SiteId", "")
                # mrbts = row.get("MRBTS", "")

                if (
                    pd.notna(site)
                    # and pd.notna(mrbts)
                ):

                    site = str(site).strip().upper()
                    # mrbts = str(mrbts).strip().upper()

                    if (
                        site != ""
                        # and mrbts != ""
                    ):
                        total_sites_4g.add(
                            # (site, mrbts)
                            (site)
                        )

    print(
        "Total Unique NEW SITE 4G:",
        len(total_sites_4g)
    )
    # ================= 5G UNIQUE NEW SITE =================
    total_sites_5g = set()
    print(
        "Total Unique NEW SITE 5G:",
        len(total_sites_5g)
    )
    # ================= NO ALARM 4G (ONLY NEW SITE) =================
    No_Alarm_4G = 0

    if (
        "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms" in alarm_df.columns
        # and "MRBTS" in alarm_df.columns
        and "Site Status" in alarm_df.columns
    ):

        No_Alarm_4G = alarm_df[
            (
                alarm_df[
                    "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms"
                ]
                .astype(str)
                .str.strip()
                == "No Alarms"
            )
            &
            # (
            #     alarm_df["MRBTS"]
            #     .astype(str)
            #     .str.strip() != ""
            # )
            # &
            (
                alarm_df["Site Status"]
                .astype(str)
                .str.strip()
                == "New Site"
            )
        ]["SiteId"].nunique()


    # ================= NO ALARM 5G (ONLY NEW SITE) =================
    NO_Alarm_5G = 0
    
    # ================= SITE DOWN 4G - NEW SITE =================
    site_down_4g_new = 0

    if (
        "Alarm Type" in alarm_df.columns
        # and "MRBTS" in alarm_df.columns
        and "Site Status" in alarm_df.columns
    ):

        site_down_4g_new = alarm_df[
            (
                alarm_df["Alarm Type"]
                .astype(str)
                .str.contains(
                    "SITE DOWN",
                    case=False,
                    na=False
                )
            )
            # &
            # (
            #     alarm_df["MRBTS"]
            #     .astype(str)
            #     .str.strip() != ""
            # )
            &
            (
                alarm_df["Site Status"]
                .astype(str)
                .str.strip()
                == "New Site"
            )
        ]["SiteId"].nunique()


    # ================= SITE DOWN 4G - OLD SITE =================
    site_down_4g_old = 0

    if (
        "Alarm Type" in alarm_df.columns
        # and "MRBTS" in alarm_df.columns
        and "Site Status" in alarm_df.columns
    ):

        site_down_4g_old = alarm_df[
            (
                alarm_df["Alarm Type"]
                .astype(str)
                .str.contains(
                    "SITE DOWN",
                    case=False,
                    na=False
                )
            )
            # &
            # (
            #     alarm_df["MRBTS"]
            #     .astype(str)
            #     .str.strip() != ""
            # )
            &
            (
                alarm_df["Site Status"]
                .astype(str)
                .str.strip()
                == "OLD Site"
            )
        ]["SiteId"].nunique()


    # ================= SITE DOWN 5G - NEW SITE =================
    site_down_5g_new = 0
    # ================= SITE DOWN 5G - OLD SITE =================
    site_down_5g_old = 0

    print("4G Site Down NEW:", site_down_4g_new)
    print("4G Site Down OLD:", site_down_4g_old)

    print("5G Site Down NEW:", site_down_5g_new)
    print("5G Site Down OLD:", site_down_5g_old)
    
    # ================= SA 4G (NEW SITE ONLY) =================
    sa_4g = 0

    if (
        "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms" in alarm_df.columns
        # and "MRBTS" in alarm_df.columns
        and "Site Status" in alarm_df.columns
    ):

        sa_4g = alarm_df[
            (
                alarm_df[
                    "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms"
                ]
                .astype(str)
                .str.strip()
                == "SA"
            )
            &
            # (
            #     alarm_df["MRBTS"]
            #     .astype(str)
            #     .str.strip() != ""
            # )
            # &
            (
                alarm_df["Site Status"]
                .astype(str)
                .str.strip()
                == "New Site"
            )
        ]["SiteId"].nunique()


    # ================= NSA 4G (NEW SITE ONLY) =================
    nsa_4g = 0

    if (
        "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms" in alarm_df.columns
        # and "MRBTS" in alarm_df.columns
        and "Site Status" in alarm_df.columns
    ):

        nsa_4g = alarm_df[
            (
                alarm_df[
                    "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms"
                ]
                .astype(str)
                .str.strip()
                == "NSA"
            )
            &
            # (
            #     alarm_df["MRBTS"]
            #     .astype(str)
            #     .str.strip() != ""
            # )
            # &
            (
                alarm_df["Site Status"]
                .astype(str)
                .str.strip()
                == "New Site"
            )
        ]["SiteId"].nunique()


    # ================= SA 5G (NEW SITE ONLY) =================
    sa_5g = 0

    
    # # ================= NSA 5G (NEW SITE ONLY) =================
    nsa_5g = 0
        
    # ================= 4G SA Alarm Type (NEW SITE ONLY) =================
    hw_alarm_4g = 0
    soft_alarm_4g = 0
    PWR_4G = 0

    if (
        "Alarm Type" in alarm_df.columns
        # and "MRBTS" in alarm_df.columns
        and "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms" in alarm_df.columns
        and "Site Status" in alarm_df.columns
    ):

        sa_4g_df = alarm_df[
            (
                alarm_df[
                    "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms"
                ]
                .astype(str)
                .str.strip()
                .str.upper()
                == "SA"
            )
            &
            # (
            #     alarm_df["MRBTS"]
            #     .astype(str)
            #     .str.strip()
            #     != ""
            # )
            # &
            (
                alarm_df["Site Status"]
                .astype(str)
                .str.strip()
                == "New Site"
            )
        ]

        site_alarm_map = {}

        for _, row in sa_4g_df.iterrows():

            site_id = str(
                row.get("SiteId", "")
            ).strip()

            alarm_bucket = str(
                row.get("Alarm Type", "")
            ).strip().upper()

            if not site_id:
                continue

            # Priority Logic
            if "HW ALARM" in alarm_bucket:
                site_alarm_map[site_id] = "HW"

            elif (
                "SOFT ALARM" in alarm_bucket
                and site_id not in site_alarm_map
            ):
                site_alarm_map[site_id] = "SOFT"

        hw_alarm_4g = sum(
            1 for v in site_alarm_map.values()
            if v == "HW"
        )

        soft_alarm_4g = sum(
            1 for v in site_alarm_map.values()
            if v == "SOFT"
        )

        PWR_4G = sum(
            1 for v in site_alarm_map.values()
            if v == "POWER"
        )
    # ================= 5G SA Alarm Type (NEW SITE ONLY) =================
    hw_alarm_5g = 0
    soft_alarm_5g = 0
    PWR_5G = 0

    print("HW Alarm 4G:", hw_alarm_4g)
    print("Soft Alarm 4G:", soft_alarm_4g)
    print("Power Alarm 4G:", PWR_4G)

    print("HW Alarm 5G:", hw_alarm_5g)
    print("Soft Alarm 5G:", soft_alarm_5g)
    print("Power Alarm 5G:", PWR_5G)

    # ================= 4G CELL COUNT (NEW SITE) =================
    cells_count_4g = 0

    if cells_4g is not None:

        cells_count_4g = cells_4g[
            (
                cells_4g["Site Status"]
                .astype(str)
                .str.strip()
                .str.lower()
                == "new site"
            )
            &
            (
                cells_4g["Cell Name"]
                .astype(str)
                .str.strip() != ""
            )
        ]["Cell Name"].nunique()

    print("Total NEW SITE Cells 4G:", cells_count_4g)
    # ================= 5G CELL COUNT (NEW SITE) =================
    cells_count_5g = 0

    print("Total NEW SITE Cells 5G:", cells_count_5g)
    # ================= TOTAL LOCKED / UNLOCKED =================

    total_both_locked_cells = len(both_locked_cells_4g) + len(both_locked_cells_5g)
    total_both_unlocked_cells = len(both_unlocked_cells_4g) + len(both_unlocked_cells_5g)

    total_both_locked_sites = len(both_locked_sites_4g) + len(both_locked_sites_5g)
    total_both_unlocked_sites = len(both_unlocked_sites_4g) + len(both_unlocked_sites_5g)
    total_sites_locked_unlocked = total_both_locked_sites + total_both_unlocked_sites
    
    
    return {
        "total_4g_sites": len(total_sites_4g),
        "total_5g_sites": len(total_sites_5g),

        "Cells_4G": int(cells_count_4g),
        "Cells_5G": int(cells_count_5g),

        "no_alarm_4g": int(No_Alarm_4G),
        "no_alarm_5g": int(NO_Alarm_5G),

        # Site Down New / Old Separate
        "site_down_4g": int(site_down_4g_new),
        "old_down_4g": int(site_down_4g_old),

        "site_down_5g": int(site_down_5g_new),
        "old_down_5g": int(site_down_5g_old),

        # SA / NSA
        "sa_4g": int(sa_4g),
        "nsa_4g": int(nsa_4g),

        "sa_5g": int(sa_5g),
        "nsa_5g": int(nsa_5g),

        # HW / SOFT Alarm
        "hw_alarm_4g": int(hw_alarm_4g),
        "soft_alarm_4g": int(soft_alarm_4g),
        "PWR_4G": int(PWR_4G),
        "hw_alarm_5g": int(hw_alarm_5g),
        "soft_alarm_5g": int(soft_alarm_5g),
        "PWR_5G": int(PWR_5G),
        "Both_Locked_Cells": int(total_both_locked_cells),
        "Both_Unlocked_Cells": int(total_both_unlocked_cells),

        "Both_Locked_Sites": int(total_both_locked_sites),
        "Both_Unlocked_Sites": int(total_both_unlocked_sites),
        "Total_Locked_Unlocked_Sites": int(total_sites_locked_unlocked),

        "Total_No_of_Cells": int(cells_count_4g + cells_count_5g)

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
def outlook_mail(expected_subject="ZTE Alarm"):
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

def process_daily_circle_logs(file_path, to_address=None, cc_mails=None):
    print("Processing Huawei Alarm ZIP...")

    output_root = os.path.join(MEDIA_ROOT, "ZTE_OUTPUT")
    if os.path.exists(output_root):
        for item in os.listdir(output_root):
            # Skip attachments folder
            # if item == "attachments":
            # Don't delete important files/folders
            if item in ["attachments", "last_mail.txt"]:
                continue
                    
            item_path = os.path.join(output_root, item)
            try:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                elif os.path.isfile(item_path):
                    os.remove(item_path)
            except Exception as e:
                print(f"Failed to delete {item_path}: {e}")

    extract_dir = os.path.splitext(file_path)[0]
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    os.makedirs(extract_dir, exist_ok=True)
    if file_path.endswith(".zip"):
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

    elif file_path.endswith(".7z"):
        with py7zr.SevenZipFile(file_path, mode="r") as z:
            z.extractall(extract_dir)

    print("ZIP Extracted:", extract_dir)

    alarm_files = []
    for root, dirs, files in os.walk(extract_dir):
        for file_name in files:
            if file_name.endswith((".csv", ".xlsx", ".xls")):
                file_path = os.path.join(root, file_name)
                alarm_files.append(file_path)
    print("Alarm Files Count:", len(alarm_files))
    if not alarm_files:
        print("No alarm files found")
        return

    files_payload = []
    # alarm files
    for alarm_path in alarm_files:
        files_payload.append(
            (
                "alarm_file",
                (
                    os.path.basename(alarm_path),
                    open(alarm_path, "rb")
                )
            )
        )

    response = requests.post(
        "http://127.0.0.1:8001/oem_zte/zte/",
        files=files_payload
    )
    print("API STATUS:", response.status_code)

    try:
        response_data = response.json()
        print(response_data)
    except Exception as e:
        print("Invalid response:", str(e))
        return
    
    if response.status_code == 200:

        print("Circle wise output generated")

        reply_subject = "📊 ZTE Alarm Output"
        circle_mail_map = {
            
            "KK": ["Dipendra.Patel@ust.com", "Harish.Singh@ust.com", "Vijay.Kumawat@ust.com"],
            "KOL": ["Dipendra.Patel@ust.com","Harish.Singh@ust.com", "Vijay.Kumawat@ust.com"],
            "UPW": ["Dipendra.Patel@ust.com", "Harish.Singh@ust.com", "Vijay.Kumawat@ust.com"],
            
        }

        body = (
            "Hi Team,\n\n"
            "PFA ZTE Alarm Circle Wise Output.\n\n"
            "Regards,\n"
            "Developer Team\n"
            "(Automated Mail)"
        )
        
        # Root folder where circle files are saved
        zte_output_root = os.path.join(
            MEDIA_ROOT,
            "ZTE_OUTPUT",
            "OUTPUT"
        )

        # Loop through circle folders
        for circle in os.listdir(zte_output_root):

            circle_path = os.path.join(
                zte_output_root,
                circle
            )

            # skip files like attachments, txt
            if not os.path.isdir(circle_path):
                continue

            # find excel in circle folder
            for file in os.listdir(circle_path):

                if file.endswith(".xlsx"):

                    excel_path = os.path.join(
                        circle_path,
                        file
                    )

                    circle_key = circle.upper().strip()

                    to_address = ";".join(
                        circle_mail_map.get(circle_key, [])
                    )
                    cc_mails = ';'.join([
                        "TES_IN_NH@UST.com",
                        "Shashank.Rai@ust.com",
                        "Mohit.Batra@ust.com",
                        "Rahul.Dahiya@ust.com",
                        "Amit.Rai@ust.com"
                                ])

                    if not to_address:
                        print(f"No mail mapping found for {circle}")
                        continue

                    print(f"Sending mail for {circle}")
                    
                    # ================= SUMMARY =================
                    summary_data = get_summary_counts(
                        excel_path
                    )

                    # ================= TEMPLATE =================
                    template_dir = os.path.join(
                        MEDIA_ROOT,
                        "template"
                    )

                    env = Environment(
                        loader=FileSystemLoader(template_dir)
                    )

                    template = env.get_template(
                        "alarm_mailbody.html"
                    )

                    html_body = template.render(
                        # circle=circle,
                        brand="ZTE",
                        circle_name=circle.upper(),
                        generated_time=datetime.now().strftime(
                            "%d-%b-%Y %I:%M %p"
                        ),
                        # ================= TOTAL SITES =================
                        total_4g_sites=summary_data.get(
                            "total_4g_sites", 0
                        ),
                        total_5g_sites=summary_data.get(
                            "total_5g_sites", 0
                        ),

                        # ================= TOTAL CELLS =================
                        Cells_4G=summary_data.get(
                            "Cells_4G", 0
                        ),

                        Cells_5G=summary_data.get(
                            "Cells_5G", 0
                        ),

                        Total_No_of_Cells=summary_data.get(
                            "Total_No_of_Cells", 0
                        ),

                        # ================= NO ALARM =================
                        no_alarm_4g=summary_data.get(
                            "no_alarm_4g", 0
                        ),
                        no_alarm_5g=summary_data.get(
                            "no_alarm_5g", 0
                        ),

                        # ================= SITE DOWN =================
                        site_down_4g=summary_data.get(
                            "site_down_4g", 0
                        ),
                        old_down_4g=summary_data.get(
                            "old_down_4g", 0
                        ),

                        site_down_5g=summary_data.get(
                            "site_down_5g", 0
                        ),
                        old_down_5g=summary_data.get(
                            "old_down_5g", 0
                        ),

                        # ================= SA / NSA =================
                        sa_4g=summary_data.get(
                            "sa_4g", 0
                        ),
                        nsa_4g=summary_data.get(
                            "nsa_4g", 0
                        ),

                        sa_5g=summary_data.get(
                            "sa_5g", 0
                        ),
                        nsa_5g=summary_data.get(
                            "nsa_5g", 0
                        ),

                        # ================= HW / SOFT =================
                        hw_alarm_4g=summary_data.get(
                            "hw_alarm_4g", 0
                        ),
                        soft_alarm_4g=summary_data.get(
                            "soft_alarm_4g", 0
                        ),

                        hw_alarm_5g=summary_data.get(
                            "hw_alarm_5g", 0
                        ),
                        soft_alarm_5g=summary_data.get(
                            "soft_alarm_5g", 0
                        ),
                        PWR_4G=summary_data.get(
                            "PWR_4G", 0
                        ),
                        PWR_5G=summary_data.get(
                            "PWR_5G", 0
                        ),
                        # ================= LOCK / UNLOCK =================
                        Both_Locked_Cells=summary_data.get(
                            "Both_Locked_Cells", 0
                        ),

                        Both_Unlocked_Cells=summary_data.get(
                            "Both_Unlocked_Cells", 0
                        ),

                        Both_Locked_Sites=summary_data.get(
                            "Both_Locked_Sites", 0
                        ),

                        Both_Unlocked_Sites=summary_data.get(
                            "Both_Unlocked_Sites", 0
                        ),

                        Total_Locked_Unlocked_Sites=summary_data.get(
                            "Total_Locked_Unlocked_Sites", 0
                        )
                    )

                    # inline css for email
                    html_body = transform(
                        html_body
                    )

                    # ================= SEND EMAIL =================
                    send_email.delay(
                        to_address=to_address,
                        cc_mails=cc_mails,
                        subject=f"{reply_subject} - {circle}",
                        body=html_body,
                        attachment_path=excel_path,
                        is_html=True,
                    )
                    
                    print(f"✅ Mail Sent for Circle => {circle}")
