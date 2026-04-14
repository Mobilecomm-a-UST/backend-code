from mailapp.tasks import send_email
import pandas as pd
import os
from django.conf import settings
from mcom_website.settings import MEDIA_ROOT
from degrowDismental.models import *
from .utils import format_excel,delete_existing_files



def send_survey_done_email(circle, siteId):
    circle_qs = DismantleCircleData.objects.all().values(
        "circle",
        "site_id",
        "partner_code",
        "partner",
        "is_approved",
        "is_surveyed",
        "is_srn_done",
        "remarks"
    )

    model_qs = DismantleModelData.objects.all().values(
        "zone",
        "site_id",
        "model_name",
        "serial_number",
        "expected_quantity",
        "is_in_mobinet",
        "is_found",
        "approval_date",
        "srn_number"
    )

    circle_df = pd.DataFrame(list(circle_qs))
    model_df = pd.DataFrame(list(model_qs))

    df = pd.merge(
        circle_df,
        model_df,
        left_on=["circle", "site_id"],
        right_on=["zone", "site_id"],
        how="left"
    )
    df = df[
        (df["circle"] == circle) &
        (df["site_id"] == siteId)
    ]

    if df.empty:
        return "No data found"

    df = df.rename(columns={
        "circle": "Circle",
        "site_id": "Site ID",
        "partner": "Partner",
        "partner_code": "Partner Code",
        "model_name": "NMS Model",
        "serial_number": "Serial Number",
        "expected_quantity": "NMS Quantity",
        "is_in_mobinet": "NMS Remarks",
        "is_found": "Is Material Found in Survey",
        "is_approved": "NMS Fetch Date",
        "is_surveyed": "Survey Date",
        "srn_number": "SRN Number",
        "is_srn_done": "SRN Date",
        "remarks": "Current Status"
    })

    df = df[
        [
            "Circle",
            "Site ID",
            "NMS Model",
            "Serial Number",
            "NMS Quantity",
            "NMS Remarks",
            "Is Material Found in Survey",
            "NMS Fetch Date",
            "Survey Date",
        ]
    ]
    df["Is Material Found in Survey"] = df["Is Material Found in Survey"].map({
        True: "Yes",
        False: "No"
    })

    df["NMS Remarks"] = df["NMS Remarks"].map({
        True: "No change",
        False: "Additional"
    })

    df = df.fillna("")
    
    mail_output = os.path.join(settings.MEDIA_ROOT,"degrow_dismantle","mail_excel")
    os.makedirs(mail_output, exist_ok=True)
    delete_existing_files(mail_output)

    file_path = os.path.join(mail_output, f"{siteId}_Survey_File.xlsx")

    df.to_excel(file_path, index=False)
    format_excel(file_path)
        



    subject = f"Submission of Survey-Report–>{siteId} ({circle} Circle)"
 
    body = f"""
    Dear Sir,<br><br>
 
    Please find attached the survey report for Site ID <b>{siteId}</b> of the <b>{circle}</b> circle.<br><br>
 
    We are also sharing the report comparing NMS modules versus the modules available during the survey.  
    The same is attached herewith for your ready reference.<br><br>
 
    Kindly acknowledge receipt of this email.<br><br>
 
    Thank you.<br>
    """


#     to_mails = [
#     "Shankar.Choudhary@airtel.com","Ravi1.Saxena@airtel.com","SRNDelhi.MNGWarehouse@Airtel.com",
#     "Pankaj.Srivastava@airtel.com","Shivpoojan.Agnihotri@airtel.com","Hitesh2.Kumar@airtel.com",
#     "ANUJ1.TYAGI@airtel.com","Arvind8.Singh@airtel.com","Manoj50.Kumar@airtel.com",
#     "Munesh2.Kumar@airtel.com","Hariom.Trivedi@airtel.com","Satraj.Yadav@airtel.com",
#     "Rajender@airtel.com","Naveen@airtel.com","Rahul6@airtel.com","Sukhbir1@airtel.com",
#     "rakesh2.yadav@airtel.com","narender3.kumar@airtel.com", "rajender@airtel.com",
#     "raman6.kumar@airtel.com","vikash7.sharma@airtel.com","shivpoojan.agnihotri@airtel.com",
#     "narendra.yadav@airtel.com","vikas1.bhardwaj@airtel.com"
# ]

#     cc_mails = [
#         "Prateek.Saxena@ust.com","Vijay.Kumar2@ust.com","Purnendra.Pandey@ust.com",
#         "Gaurav.Agrawal@ust.com","Yogesh.Kumar4@ust.com","Khudabaks.Saifi@ust.com", "Deepak.Singh2@ust.com",
#         "Ramveer.Singh@ust.com","Abhinav.Verma@ust.com"
#     ]
    to_mails = list(EmailList.objects.filter(email_type="TO").values_list("email", flat=True))
    cc_mails = list(EmailList.objects.filter(email_type="CC").values_list("email", flat=True))

    # to_mails =["Abhinav.Verma@ust.com"]
    # cc_mails=["Abhinav.Verma@ust.com",]


    to_mail = ";".join(to_mails)
    cc_mail = ";".join(cc_mails)
 
    try:
        print(f"Sending Survey Mail → {circle} | {siteId}")
        send_email.delay(
            to_mail,
            cc_mail,
            subject,
            body,
            attachment_path=file_path,
            is_html=True
        )
        print("Site Servery Mail Send Sucessfully-")
 
    except Exception as e:
        print(f"Email failed: {e}")
 
   