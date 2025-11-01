from celery import shared_task
import win32com.client
from mailapp.models import *  # noqa: F403
import os
 
 
 
@shared_task
def send_email(to_address, cc_mails, subject, body, attachment_path=None, is_html=False):
    try:
        # CoInitialize needs to be called before using win32com.client
        win32com.client.pythoncom.CoInitialize()
 
        # using the win 32 client ...............................
        outlook = win32com.client.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)
        mail.To = to_address
        mail.CC = cc_mails
        mail.Subject = subject
 
        if is_html:
            mail.HTMLBody = body
        else:
            mail.Body = body
 
        if attachment_path:
            attachment_path = os.path.abspath(attachment_path)
            if os.path.exists(attachment_path):
                mail.Attachments.Add(attachment_path)
            else:
                print(f"⚠️ Attachment file not found: {attachment_path}")
 
        mail.Send()
        print("✅ Email sent via Outlook.")
 
    except Exception as e:
        return f"Error sending email: {str(e)}"