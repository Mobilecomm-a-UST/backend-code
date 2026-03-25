from celery import shared_task
# import win32com.client
from mailapp.models import *  # noqa: F403
import os
import requests
 
 
 
# @shared_task
# def send_email(to_address, cc_mails, subject, body, attachment_path=None, is_html=False):
#     try:
#         print("===================Mail-check========================")
#         # # CoInitialize needs to be called before using win32com.client
#         # win32com.client.pythoncom.CoInitialize()
 
#         # # using the win 32 client ...............................
#         # outlook = win32com.client.Dispatch("Outlook.Application")
#         # mail = outlook.CreateItem(0)
#         # mail.To = to_address
#         # mail.CC = cc_mails
#         # mail.Subject = subject
 
#         # if is_html:
#         #     mail.HTMLBody = body
#         # else:
#         #     mail.Body = body
 
#         # if attachment_path:
#         #     attachment_path = os.path.abspath(attachment_path)
#         #     if os.path.exists(attachment_path):
#         #         mail.Attachments.Add(attachment_path)
#         #     else:
#         #         print(f"⚠️ Attachment file not found: {attachment_path}")
 
#         # mail.Send()
#         # print("✅ Email sent via Outlook.")


        
 
#     except Exception as e:
#         return f"Error sending email: {str(e)}"
    

def send_email(to_address, cc_mails, subject, body, attachment_path=None, is_html=False):
    ELASTIC_API_KEY = "BB168477599BBAA81CC0ECDF3871C290653CCA3AD2CD1FBA3A585A1071F511ED597B9FD34980D4093D9C1CC310B4BCFB"
    sender_email = "noreply@mcpspmis.com"

    all_recipients = to_address
    if cc_mails:
        all_recipients = f"{to_address};{cc_mails}"
 

 
    url = "https://api.elasticemail.com/v2/email/send"

    data = {
        "apikey": ELASTIC_API_KEY,
        "from": sender_email,
        "to": all_recipients,
        "subject": subject,
        "isTransactional": False
    }

    if is_html:
        data["bodyHtml"] = body
    else:
        data["bodyText"] = body
 
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("✅ Email sent successfully!")
        else:
            print(f"❌ Failed to send email: {response.status_code}\nResponse: {response.text}")
           
    except Exception as e:
        print(f"⚠️ Error sending email: {e}")