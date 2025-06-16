from celery import shared_task
from datetime import datetime, timedelta
# from django.core.mail import send_mail
from .models import Daily_4G_KPI,AlarmNotification,Tantitive_Counters_24_Hours
from mailapp.tasks import send_email

############################################### for alarm dump data missing ############################################################
alarmdump_to_address =''
# alarmdump_to_address = 'nishant.verma@ust.com'
alarmdump_cc_mails=""
# alarmdump_cc_mails='nishant.verma@ust.com'
alarmdump_subject='RCA Genie | Alarm Dump Data Missing for Daily RCA Generation'

alarmdump_body ="""Dear NOC Support Team,

This is an automated reminder from RCA Genie. The AlarmDump data required for today’s RCA generation has not been uploaded. Without this data, RCA Genie cannot complete its automated tasks and analyses as scheduled.

Please ensure the data is uploaded at the earliest to avoid delays. If you have already uploaded it, no further action is required.

This is a system-generated email. For any assistance, please contact the support team.

Best regards,
RCA Genie
"""
alarmdump_reminder_subject="RCA Genie | Follow-Up: AlarmDump Data Still Missing for RCA Generation"

alarmdump_reminder_body="""
Dear NOC Support Team,

This is a follow-up reminder from RCA Genie. The AlarmDump data required for today’s RCA generation is still missing. Without this data, RCA Genie cannot execute its scheduled tasks and analyses, which may impact downstream processes.

Please upload the data immediately to ensure smooth operations. If the data has already been uploaded, kindly confirm by responding to this email.

This is a system-generated email. For assistance, please contact the support team.

Best regards,
RCA Genie """

@shared_task
def alarmdump_check_data_and_notify():
    nMinus1_date = datetime.now().date() - timedelta(days=1)
    data_exists = AlarmNotification.objects.filter(Upload_date=nMinus1_date).exists()

    if not data_exists:
        send_email.delay(alarmdump_to_address, alarmdump_cc_mails ,alarmdump_subject, alarmdump_body)
        # alarmdump_schedule_reminder_email()


@shared_task
def alarmdump_reminder_email_task():
    nMinus1_date = datetime.now().date() - timedelta(days=1)
    data_exists = AlarmNotification.objects.filter(Upload_date=nMinus1_date).exists()

    if not data_exists:

        send_email(alarmdump_to_address, alarmdump_cc_mails ,alarmdump_reminder_subject, alarmdump_reminder_body)

def alarmdump_schedule_reminder_email():
    # Schedule reminder email after 1 hour
    alarmdump_reminder_email_task.apply_async(eta=datetime.now() + timedelta(minutes=27))

############################## ****************************** ######################################


################################# for 4G KPI data missing ############################################################
kpi_4g_to_address =''
# kpi_4g_to_address = 'nishant.verma@ust.com'
kpi_4g_cc_mails=''
# kpi_4g_cc_mails='nishant.verma@ust.com'

kpi_4g_subject='RCA Genie | 24hrs 4G KPI Data Missing for Daily RCA Generation'

kpi_4g_body =""" 
Dear Quality Team,

This is an automated reminder from RCA Genie. The 24-hour 4G KPI data required for today’s processing has not been uploaded. Without this data, RCA Genie cannot execute its scheduled tasks and analyses.

Please ensure the data is uploaded at the earliest to avoid delays. If the data has already been uploaded, no further action is required.

This is a system-generated email. For assistance, please contact the support team.

Best regards,
RCA Genie"""

kpi_4g_reminder_subject = "RCA Genie | Follow-Up: 24hrs 4G KPI Data Still Missing for RCA Generation"

kpi_4g_reminder_body="""
Dear Quality Team,

This is a follow-up reminder from RCA Genie. The 24-hour 4G KPI data required for today’s processing is still missing. Without this data, RCA Genie cannot complete its automated tasks and analyses, which may affect downstream operations.

Please upload the data immediately to ensure smooth processing. If the data has already been uploaded, kindly confirm by responding to this email.

This is a system-generated email. For assistance, please contact the support team.

Best regards,
RCA Genie
 """


@shared_task
def KPI_4G_check_data_and_notify():
    nMinus1_date = datetime.now().date() - timedelta(days=1)
    data_exists = Daily_4G_KPI.objects.filter(Date=nMinus1_date).exists()

    if not data_exists:
        send_email.delay(kpi_4g_to_address, kpi_4g_cc_mails ,kpi_4g_subject, kpi_4g_body)
        # KPI_4G_schedule_reminder_email()


@shared_task
def KPI_4G_reminder_email_task():
    nMinus1_date = datetime.now().date() - timedelta(days=1)
    data_exists = Daily_4G_KPI.objects.filter(Date=nMinus1_date).exists()

    if not data_exists:

        send_email(kpi_4g_to_address, kpi_4g_cc_mails ,kpi_4g_reminder_subject, kpi_4g_reminder_body)

def KPI_4G_schedule_reminder_email():
    # Schedule reminder email after 1 hour
    KPI_4G_reminder_email_task.apply_async(eta=datetime.now() + timedelta(minutes=27))



################################################# for Tantitive Counters data missing ############################################################

TantitiveCounter_to_address =''
# TantitiveCounter_to_address = 'nishant.verma@ust.com'  
TantitiveCounter_cc_mails=''
# TantitiveCounter_cc_mails='nishant.verma@ust.com'
TantitiveCounter_subject='RCA Genie | 24hrs Tantitive Counters Data Missing for Daily RCA Generation'

TantitiveCounter_body ="""
Dear Quality Team,

This is an automated reminder from RCA Genie. The 24hrs Tantitive Counters Data required for today’s processing has not been uploaded. Without this data, RCA Genie cannot execute its scheduled tasks and analyses.

Please ensure the data is uploaded at the earliest to avoid delays. If the data has already been uploaded, no further action is required.

This is a system-generated email. For assistance, please contact the support team.

Best regards,
RCA Genie 
"""
TantitiveCounter_reminder_subject = "RCA Genie | Follow-Up: 24hrs Tantitive Counters Data Still Missing for RCA Generation"

TantitiveCounter_reminder_body="""
Dear Quality Team,

This is a follow-up reminder from RCA Genie. The 24hrs Tantitive Counters Data required for today’s processing is still missing. Without this data, RCA Genie cannot complete its automated tasks and analyses, which may affect downstream operations.

Please upload the data immediately to ensure smooth processing. If the data has already been uploaded, kindly confirm by responding to this email.

This is a system-generated email. For assistance, please contact the support team.

Best regards,
RCA Genie
"""


@shared_task
def TantitiveCounter_check_data_and_notify():
    nMinus1_date = datetime.now() - timedelta(days=1)
    data_exists = Tantitive_Counters_24_Hours.objects.filter(DateTime=nMinus1_date).exists()

    if not data_exists:
        send_email.delay(TantitiveCounter_to_address, TantitiveCounter_cc_mails ,TantitiveCounter_subject, TantitiveCounter_body)
        # TentitiveCounter_schedule_reminder_email()


@shared_task
def TentitiveCounter_reminder_email_task():
    nMinus1_date = datetime.now()  - timedelta(days=1)
    data_exists = Tantitive_Counters_24_Hours.objects.filter(DateTime=nMinus1_date).exists()

    if not data_exists:

        send_email(TantitiveCounter_to_address, TantitiveCounter_cc_mails ,TantitiveCounter_reminder_subject, TantitiveCounter_reminder_body)

def TentitiveCounter_schedule_reminder_email():
    # Schedule reminder email after 1 hour
    TentitiveCounter_reminder_email_task.apply_async(eta=datetime.now() + timedelta(minutes=27))