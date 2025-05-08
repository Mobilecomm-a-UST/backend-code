from celery import shared_task
import win32com.client
from django.core.mail import send_mail
from mailapp.models import *

# from Soft_AT_Rejected.views import  soft_At_Rejection_Database_save
@shared_task
def send_email(to_address, cc_mails ,subject, body):
    try:
        # CoInitialize needs to be called before using win32com.client
        win32com.client.pythoncom.CoInitialize()
        outlook = win32com.client.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)
        mail.To = to_address
        mail.CC = cc_mails
        mail.Subject = subject
        mail.Body = body
        mail.Send()
        return "Email sent successfully"
    except Exception as e:
        return f"Error sending email: {str(e)}"
    











