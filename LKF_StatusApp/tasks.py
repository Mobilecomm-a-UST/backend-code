import os
import win32com.client
import pythoncom
import requests
import zipfile
import shutil
from datetime import datetime
from celery import shared_task
from mcom_website.settings import MEDIA_ROOT
from mailapp.tasks import send_email  # make sure this is your Celery email task
import  pandas as pd



save_directory = os.path.join(MEDIA_ROOT, "LKF_StatusApp", "attachments")
LAST_PROCESSED_FILE = os.path.join(MEDIA_ROOT, "LKF_StatusApp", "last_mail.txt")


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


@shared_task(name="LKF_StatusApp.tasks.check_lkf_mail")
def check_lkf_mail(expected_subject="LKF logs Status"):
    # pythoncom.CoInitialize()
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.Folders.Item("Abhinav.Verma@ust.com").Folders["Inbox"]

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
    print(f"📩 Latest mail => {subject}")

    if expected_subject.lower() in subject.lower():
        if latest_mail.Attachments.Count > 0:
            for att in latest_mail.Attachments:
                if att.FileName.endswith(".zip"):
                    if not os.path.exists(save_directory):
                        os.makedirs(save_directory)
                    file_path = os.path.join(save_directory, att.FileName)
                    att.SaveAsFile(file_path)
                    print("✅ Zip downloaded:", file_path)

                    save_last_mail(unique_id)
                    
                    process_lkf_logs(
                        file_path,
                        to_address=latest_mail.TO,
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


def process_lkf_logs(file_path, to_address=None, cc_mails=None):
    print(file_path, "file path..................................")
    today_str = datetime.today().strftime("%Y-%m-%d")
    output_root = os.path.join(MEDIA_ROOT, "LKF_StatusApp", "LKF_log_output")

    # Purane outputs delete karo
    if os.path.exists(output_root):
        shutil.rmtree(output_root)
    os.makedirs(output_root, exist_ok=True)

    # ✅ Extract ZIP
    extract_dir = file_path.replace(".zip", "")
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir, ignore_errors=True)
    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)
    print(f"✅ Extracted to {extract_dir}")

    # ✅ Collect files for API
    files_payload = []
    for root, _, files in os.walk(extract_dir):
        for fname in files:
            if fname.endswith(".log") or fname.endswith(".txt"):
                fpath = os.path.join(root, fname)
                files_payload.append(("files", (fname, open(fpath, "rb"))))

    if not files_payload:
        print("❌ No log files found in extracted folder")
        return

    # ✅ Hit Django API (jo tumne banayi hai)
    response = requests.post("http://localhost:8001/LKF/LKF_status/", files=files_payload)
    print("LKF response:", response.status_code)

    # ✅ Check API response
    if response.status_code != 200:
        print("❌ API Error:", response.text)
        return

    data = response.json()
    download_url = data.get("download_url")
    if not download_url:
        print("❌ No download_url found in API response")
        return

    # ✅ Download Excel from API response
    r = requests.get(download_url)
    output_excel = os.path.join(output_root, f"LKF_Status_{today_str}.xlsx")
    with open(output_excel, "wb") as f:
        f.write(r.content)
    print("✅ Saved Excel:", output_excel)

    # ✅ Send Email with Excel
    reply_subject = f"Re: Processed LKF_Status"
    body = "Hello Team,\n\nPlease find the attached processed LKF_Status.\n\nRegards,\nAutomation Team (Do Not Reply---)"
    
    to_address=';'.join(['Suman.Raman@ust.com','Ashish.Solanki@ust.com','Shashank.Rai@ust.com','Dhiraj.Sharma@ust.com','Amit.Rai@ust.com',
                         'Yogesh.Prajapati@ust.com','Abhinav.Verma@ust.com','Chirag.Bohara@ust.com'])
    cc_mails=';'.join(['Amit.Rai@ust.com','Aashish.Sharma@ust.com','Mohit.Batra@ust.com'])
    
    send_email.delay(
        to_address=to_address,
        cc_mails=cc_mails,
        subject=reply_subject,
        body=body,
        attachment_path=output_excel,
        is_html=False,
    )
