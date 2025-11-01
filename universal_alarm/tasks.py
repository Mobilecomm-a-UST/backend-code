import os
import win32com.client
import pythoncom
import requests
import zipfile
import shutil
from datetime import datetime
from celery import shared_task
from mcom_website.settings import MEDIA_ROOT
from mailapp.tasks import send_email 



save_directory = os.path.join(MEDIA_ROOT, "Universal_alarm", "attachments")
LAST_PROCESSED_FILE = os.path.join(MEDIA_ROOT, "Universal_alarm", "last_mail.txt")


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
    inbox = outlook.Folders.Item("nocsupport@mcpsinc.com").Folders["Inbox"]

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
                    
                    process_daily_circle_logs(
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


def process_daily_circle_logs(file_path,to_address=None, cc_mails=None):
    print(file_path,"file path.................................."   )
    today_str = datetime.today().strftime("%Y-%m-%d")
    output_root = os.path.join(MEDIA_ROOT, "Universal_alarm", "daily_status_alarm")

    # 🔹 Purane output zips delete karo
    if os.path.exists(output_root):
        for item in os.listdir(output_root):
            item_path = os.path.join(output_root, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)   # purana folder delete
            elif item.endswith(".zip"):
                os.remove(item_path)  # purana zip delete

    zip_files = [f for f in os.listdir(save_directory) if f.endswith(".zip")]
    if not zip_files:
        print("❌ No zip files found to process")
        return

    zip_file = os.path.join(save_directory, zip_files[-1])
    print("📂 Processing latest zip:", zip_file)

    extract_dir = zip_file.replace(".zip", "")
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir, ignore_errors=True)   #add this line to remove existing directory before creating a new one
    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(extract_dir)
    print(f"✅ Extracted to {extract_dir}")

    daily_status_folder = os.path.join(MEDIA_ROOT, "Universal_alarm", "daily_status_alarm", today_str)
    os.makedirs(daily_status_folder, exist_ok=True)

    circles_path = os.path.join(extract_dir, extract_dir.split("\\")[-1])
    for circle in os.listdir(circles_path):
        circle_path = os.path.join(circles_path, circle)
        print(circle_path,"circle path.....................................")
        if not os.path.isdir(circle_path):
            print("bhai tu idher to nahi aara hai.....................................")
            continue

        log_files = []
        for file_name in os.listdir(circle_path):
            file_path = os.path.join(circle_path, file_name)
            if os.path.isfile(file_path):
                with open(file_path, "rb") as f:
                    log_files.append(("log_files", (file_name, f.read())))

        print(f"🚀 Uploading logs for circle: {circle}, Files: {len(log_files)}")
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
        print(f"📡 API Response for {circle}: 4G={response_4G.status_code}, 5G={response_5G.status_code}")

    zip_output_path = f"{daily_status_folder}.zip"
    shutil.make_archive(daily_status_folder, "zip", daily_status_folder)
    print(f"📦 Zipped daily status folder → {zip_output_path}")

    # Email notification
    reply_subject = f"Re: Processed Daily Logs"
    body = "Hello Team,\n\nPFA the daily processed logs output.\n\nRegards,\nAutomation Team (Do Not Reply)"
    
    send_email.delay(
        to_address=to_address,  
        cc_mails=cc_mails,
        subject=reply_subject,
        body=body,
        attachment_path=zip_output_path,
        is_html=False,
    )

