from django.db.models.signals import post_save
from mailapp.tasks import send_email
from django.dispatch import receiver, Signal
from Soft_AT_Rejected.models import *
import pandas as pd


# to_address = "nishant.verma@mcpsinc.in"
subject= "soft at rejaction app testing"


signal = Signal()



@receiver(post_save, sender=Soft_AT_NOKIA_Rejected_Table)
def nokia_send_email_on_save(sender, instance, created, **kwargs):
    print("inside nok auto mail.....")
    if created and instance.AT_STATUS.upper() in ["REJECT", "REJECTED"]:

        print("Sending mail into the soft_at-nokia", instance.AT_STATUS)
        Rejection_Remark=instance.AT_REMARK.upper()
        circle=instance.Circle.upper()
        oem=instance.OEM.upper()
        print("Rejection_Remark:",Rejection_Remark,"circle:",circle,"oem:",oem)
        if not Rejection_Remarks.objects.filter(Rejection_Remark__iexact= Rejection_Remark).exists():
            Rejection_Remarks.objects.create(Rejection_Remark=Rejection_Remark,Alarm_Bucket= "", OEM=oem, Final_Responsibility="Circle Team,NOC Team")
        
        final_responsibilities = Rejection_Remarks.objects.filter(Rejection_Remark__iexact= Rejection_Remark)[0].Final_Responsibility
        final_responsibilities = final_responsibilities.split(',')

            
        for responsible_team in final_responsibilities:
            if responsible_team == "Circle Team":
            
                Centeral_Responsible_Spoc_Mail_obj =  Circle_Responsible_Spoc.objects.filter(Circle__iexact=circle,OEM__iexact=oem)
                
                to_mails = Centeral_Responsible_Spoc_Mail_obj.values("Circle_Soft_At_Spoc_Mail")
                print("to mails....",to_mails)
                df = pd.DataFrame(to_mails)
                to_email_list = df['Circle_Soft_At_Spoc_Mail'].tolist()
                print("to_email_list :",to_email_list)
                to_emails = ";".join(to_email_list)
                print("to_mails: ",to_emails)
    
                ################circle pm  mails ######################
                Circle_PM_obj =  Circle_PM.objects.filter(Circle__iexact=circle,OEM__iexact=oem)
                
                to_circle_pm_mails = Circle_PM_obj.values("Circle_PM_Mail")
                print("to circle pm mails....",to_circle_pm_mails)
                df = pd.DataFrame(to_circle_pm_mails)
                to_circle_pm_email_list = df['Circle_PM_Mail'].tolist()
                print("to_circle_pm_email_list :",to_circle_pm_email_list)
                to_circle_pm_emails = ";".join(to_circle_pm_email_list)
                print("to circle pm mails: ",to_circle_pm_emails)
                
                to_mails = to_emails +";"+ to_circle_pm_emails
                print("to_mails:",to_mails)
                ################ to_cc #########################
                Central_Management_obj =  Central_Management.objects.filter(Circle__iexact=circle,OEM__iexact=oem)
                
                to_cc_mails = Central_Management_obj.values("Central_Management_Mails")
                print("to circle pm mails....",to_cc_mails)
                df = pd.DataFrame(to_cc_mails)
                to_cc_email_list = df['Central_Management_Mails'].tolist()
                print("to_cc_email_list :",to_cc_email_list[0])
                to_cc_emails = ";".join(to_cc_email_list[0])
                print("to_ CC mails: ",to_cc_emails)
                
            if responsible_team == "NOC Team":
                
                Centeral_Responsible_Spoc_Mail_obj =  Centeral_Responsible_Spoc_Mail.objects.filter(Circle__iexact=circle,OEM__iexact=oem)
                
                to_mails = Centeral_Responsible_Spoc_Mail_obj.values("Central_Soft_At_Spoc_Mail")
                print("to mails....",to_mails)
                df = pd.DataFrame(to_mails)
                to_email_list = df['Central_Soft_At_Spoc_Mail'].tolist()
                print("to_email_list :",to_email_list)
                to_mails = ";".join(to_email_list[0])
                print("to_mails: ",to_mails)
                ################ to_cc #########################
                Central_Management_obj =  Central_Management.objects.filter(Circle__iexact=circle,OEM__iexact=oem)
                
                to_cc_mails = Central_Management_obj.values("Central_Management_Mails")
                print("to circle mails....",to_cc_mails)
                df = pd.DataFrame(to_cc_mails)
                to_cc_email_list = df['Central_Management_Mails'].tolist()
                print("to_cc_email_list :",to_cc_email_list)
                to_cc_emails = ";".join(to_cc_email_list[0])
                print("to_ CC mails: ",to_cc_emails)
                
            body=instance.AT_REMARK 
            send_email(to_mails, to_cc_emails, subject, body)

# Connect the nokia_signal to the signal handler
# signal.connect(nokia_send_email_on_save, sender=Soft_AT_NOKIA_Rejected_Table)

# ############################### For Ericcsion #############################
@receiver(post_save, sender=Soft_AT_ERI_Rejected_Table)
def eri_send_email_on_save(sender, instance, created, **kwargs):
    if created and instance.AT_STATUS.upper() in ["REJECT", "REJECTED"]:
        print("Sending mail into the soft_at-Ericcsion", instance.AT_STATUS)
        Rejection_Remark=instance.AT_Remarks
        circle=instance.Circle
        oem=instance.OEM
        print("Rejection_Remark:",Rejection_Remark,"circle:",circle,"oem:",oem)
        if not Rejection_Remarks.objects.filter(Rejection_Remark__iexact= Rejection_Remark).exists():
            Rejection_Remarks.objects.create(Rejection_Remark=Rejection_Remark,Alarm_Bucket= "", OEM=oem, Final_Responsibility="Circle Team,NOC Team")
        
        final_responsibilities = Rejection_Remarks.objects.filter(Rejection_Remark__iexact= Rejection_Remark)[0].Final_Responsibility
        final_responsibilities = final_responsibilities.split(',')

            
        for responsible_team in final_responsibilities:

            if responsible_team == "Circle Team":
                Centeral_Responsible_Spoc_Mail_obj =  Circle_Responsible_Spoc.objects.filter(Circle__iexact=circle,OEM__iexact=oem)

                to_mails = Centeral_Responsible_Spoc_Mail_obj.values("Circle_Soft_At_Spoc_Mail")
                print("to mails....",to_mails)
                df = pd.DataFrame(to_mails)
                to_email_list = df['Circle_Soft_At_Spoc_Mail'].tolist()
                print("to_email_list :",to_email_list)
                to_emails = ";".join(to_email_list)
                print("to_mails: ",to_emails)

                ################circle pm  mails ######################
                Circle_PM_obj =  Circle_PM.objects.filter(Circle__iexact=circle,OEM__iexact=oem)

                to_circle_pm_mails = Circle_PM_obj.values("Circle_PM_Mail")
                print("to circle pm mails....",to_circle_pm_mails)
                df = pd.DataFrame(to_circle_pm_mails)
                to_circle_pm_email_list = df['Circle_PM_Mail'].tolist()
                print("to_circle_pm_email_list :",to_circle_pm_email_list)
                to_circle_pm_emails = ";".join(to_circle_pm_email_list)
                print("to circle pm mails: ",to_circle_pm_emails)

                to_mails = to_emails +";"+ to_circle_pm_emails
                print("to_mails:",to_mails)
                ################ to_cc #########################
                Central_Management_obj =  Central_Management.objects.filter(Circle__iexact=circle,OEM__iexact=oem)

                to_cc_mails = Central_Management_obj.values("Central_Management_Mail")
                print("to circle pm mails....",to_cc_mails)
                df = pd.DataFrame(to_cc_mails)
                to_cc_email_list = df['Central_Management_Mail'].tolist()
                print("to_cc_email_list :",to_cc_email_list)
                to_cc_emails = ";".join(to_cc_email_list)
                print("to_ CC mails: ",to_cc_emails)


            if responsible_team == "NOC Team":

                Centeral_Responsible_Spoc_Mail_obj =  Centeral_Responsible_Spoc_Mail.objects.filter(Circle__iexact=circle,OEM__iexact=oem)

                to_mails = Centeral_Responsible_Spoc_Mail_obj.values("Central_Soft_At_Spoc_Mail")
                print("to mails....",to_mails)
                df = pd.DataFrame(to_mails)
                to_email_list = df['Central_Soft_At_Spoc_Mail'].tolist()
                print("to_email_list :",to_email_list)
                to_mails = ";".join(to_email_list)
                print("to_mails: ",to_mails)
                ################ to_cc #########################
                Central_Management_obj =  Central_Management.objects.filter(Circle__iexact=circle,OEM__iexact=oem)

                to_cc_mails = Central_Management_obj.values("Central_Management_Mail")
                print("to circle mails....",to_cc_mails)
                df = pd.DataFrame(to_cc_mails)
                to_cc_email_list = df['Central_Management_Mail'].tolist()
                print("to_cc_email_list :",to_cc_email_list)
                to_cc_emails = ";".join(to_cc_email_list)
                print("to_ CC mails: ",to_cc_emails)

            body=instance.AT_Remarks
            send_email(to_mails, to_cc_emails, subject, body)


signal.connect(eri_send_email_on_save, sender=Soft_AT_ERI_Rejected_Table)

# ############################## FOR huawei ################################
@receiver(post_save, sender=Soft_AT_HUAWEI_Rejected_Table)
def hua_send_email_on_save(sender, instance, created, **kwargs):
    if created and instance.AT_STATUS.upper() in ["REJECT", "REJECTED"]:
        print("Sending mail into the soft_at-huawei", instance.AT_STATUS)
        Rejection_Remark=instance.AT_Remarks
        circle=instance.Circle
        oem=instance.OEM
        print("Rejection_Remark:",Rejection_Remark,"circle:",circle,"oem:",oem)
        if not Rejection_Remarks.objects.filter(Rejection_Remark__iexact= Rejection_Remark).exists():
            Rejection_Remarks.objects.create(Rejection_Remark=Rejection_Remark,Alarm_Bucket= "", OEM=oem, Final_Responsibility="Circle Team,NOC Team")
        
        final_responsibilities = Rejection_Remarks.objects.filter(Rejection_Remark__iexact= Rejection_Remark)[0].Final_Responsibility
        final_responsibilities = final_responsibilities.split(',')

            
        for responsible_team in final_responsibilities:
            if responsible_team == "Circle Team":
                Centeral_Responsible_Spoc_Mail_obj =  Circle_Responsible_Spoc.objects.filter(Circle__iexact=circle,OEM__iexact=oem)

                to_mails = Centeral_Responsible_Spoc_Mail_obj.values("Circle_Soft_At_Spoc_Mail")
                print("to mails....",to_mails)
                df = pd.DataFrame(to_mails)
                to_email_list = df['Circle_Soft_At_Spoc_Mail'].tolist()
                print("to_email_list :",to_email_list)
                to_emails = ";".join(to_email_list)
                print("to_mails: ",to_emails)

                ################circle pm  mails ######################
                Circle_PM_obj =  Circle_PM.objects.filter(Circle__iexact=circle,OEM__iexact=oem)

                to_circle_pm_mails = Circle_PM_obj.values("Circle_PM_Mail")
                print("to circle pm mails....",to_circle_pm_mails)
                df = pd.DataFrame(to_circle_pm_mails)
                to_circle_pm_email_list = df['Circle_PM_Mail'].tolist()
                print("to_circle_pm_email_list :",to_circle_pm_email_list)
                to_circle_pm_emails = ";".join(to_circle_pm_email_list)
                print("to circle pm mails: ",to_circle_pm_emails)

                to_mails = to_emails +";"+ to_circle_pm_emails
                print("to_mails:",to_mails)
                ################ to_cc #########################
                Central_Management_obj =  Central_Management.objects.filter(Circle__iexact=circle,OEM__iexact=oem)

                to_cc_mails = Central_Management_obj.values("Central_Management_Mail")
                print("to circle pm mails....",to_cc_mails)
                df = pd.DataFrame(to_cc_mails)
                to_cc_email_list = df['Central_Management_Mail'].tolist()
                print("to_cc_email_list :",to_cc_email_list)
                to_cc_emails = ";".join(to_cc_email_list)
                print("to_ CC mails: ",to_cc_emails)


            if responsible_team == "NOC Team":

                Centeral_Responsible_Spoc_Mail_obj =  Centeral_Responsible_Spoc_Mail.objects.filter(Circle__iexact=circle,OEM__iexact=oem)

                to_mails = Centeral_Responsible_Spoc_Mail_obj.values("Central_Soft_At_Spoc_Mail")
                print("to mails....",to_mails)
                df = pd.DataFrame(to_mails)
                to_email_list = df['Central_Soft_At_Spoc_Mail'].tolist()
                print("to_email_list :",to_email_list)
                to_mails = ";".join(to_email_list)
                print("to_mails: ",to_mails)
                ################ to_cc #########################
                Central_Management_obj =  Central_Management.objects.filter(Circle__iexact=circle,OEM__iexact=oem)

                to_cc_mails = Central_Management_obj.values("Central_Management_Mail")
                print("to circle mails....",to_cc_mails)
                df = pd.DataFrame(to_cc_mails)
                to_cc_email_list = df['Central_Management_Mail'].tolist()
                print("to_cc_email_list :",to_cc_email_list)
                to_cc_emails = ";".join(to_cc_email_list)
                print("to_ CC mails: ",to_cc_emails)

            body=instance.AT_Remarks
            send_email(to_mails, to_cc_emails, subject, body)


signal.connect(hua_send_email_on_save, sender=Soft_AT_HUAWEI_Rejected_Table)

# ################## For Samsung ###################################

@receiver(post_save, sender=Soft_AT_SAMSUNG_Rejected_Table)
def samsung_send_email_on_save(sender, instance, created, **kwargs):
    if created and instance.AT_STATUS.upper() in ["REJECT", "REJECTED"]:
        print("Sending mail into the soft_at-samsung", instance.AT_STATUS)
        Rejection_Remark=instance.AT_Remarks
        circle=instance.Circle
        oem=instance.OEM
        print("Rejection_Remark:",Rejection_Remark,"circle:",circle,"oem:",oem)
        if not Rejection_Remarks.objects.filter(Rejection_Remark__iexact= Rejection_Remark).exists():
            Rejection_Remarks.objects.create(Rejection_Remark=Rejection_Remark,Alarm_Bucket= "", OEM=oem, Final_Responsibility="Circle Team,NOC Team")
        
        final_responsibilities = Rejection_Remarks.objects.filter(Rejection_Remark__iexact= Rejection_Remark)[0].Final_Responsibility
        final_responsibilities = final_responsibilities.split(',')

            
        for responsible_team in final_responsibilities:
            if responsible_team == "Circle Team":
                Centeral_Responsible_Spoc_Mail_obj =  Circle_Responsible_Spoc.objects.filter(Circle__iexact=circle,OEM__iexact=oem)
                
                to_mails = Centeral_Responsible_Spoc_Mail_obj.values("Circle_Soft_At_Spoc_Mail")
                print("to mails....",to_mails)
                df = pd.DataFrame(to_mails)
                to_email_list = df['Circle_Soft_At_Spoc_Mail'].tolist()
                print("to_email_list :",to_email_list)
                to_emails = ";".join(to_email_list)
                print("to_mails: ",to_emails)
    
                ################circle pm  mails ######################
                
                Circle_PM_obj =  Circle_PM.objects.filter(Circle__iexact=circle,OEM__iexact=oem)
                print("Samsung circle PM:",Circle_PM_obj)
                to_circle_pm_mails = Circle_PM_obj.values("Circle_PM_Mail")
                print("to circle pm mails....",to_circle_pm_mails)
                df = pd.DataFrame(to_circle_pm_mails)
                to_circle_pm_email_list = df['Circle_PM_Mail'].tolist()
                print("to_circle_pm_email_list :",to_circle_pm_email_list)
                to_circle_pm_emails = ";".join(to_circle_pm_email_list)
                print("to circle pm mails: ",to_circle_pm_emails)
                
                to_mails = to_emails +";"+ to_circle_pm_emails
                print("to_mails:",to_mails)
                ################ to_cc #########################
                Central_Management_obj =  Central_Management.objects.filter(Circle__iexact=circle,OEM__iexact=oem)
                
                to_cc_mails = Central_Management_obj.values("Central_Management_Mail")
                print("to circle pm mails....",to_cc_mails)
                df = pd.DataFrame(to_cc_mails)
                to_cc_email_list = df['Central_Management_Mail'].tolist()
                print("to_cc_email_list :",to_cc_email_list)
                to_cc_emails = ";".join(to_cc_email_list)
                print("to_ CC mails: ",to_cc_emails)
                
                
            if responsible_team == "NOC Team":
                
                Centeral_Responsible_Spoc_Mail_obj =  Centeral_Responsible_Spoc_Mail.objects.filter(Circle__iexact=circle,OEM__iexact=oem)
                
                to_mails = Centeral_Responsible_Spoc_Mail_obj.values("Central_Soft_At_Spoc_Mail")
                print("to mails....",to_mails)
                df = pd.DataFrame(to_mails)
                to_email_list = df['Central_Soft_At_Spoc_Mail'].tolist()
                print("to_email_list :",to_email_list)
                to_mails = ";".join(to_email_list)
                print("to_mails: ",to_mails)
                ################ to_cc #########################
                Central_Management_obj =  Central_Management.objects.filter(Circle__iexact=circle,OEM__iexact=oem)
                
                to_cc_mails = Central_Management_obj.values("Central_Management_Mail")
                print("to circle mails....",to_cc_mails)
                df = pd.DataFrame(to_cc_mails)
                to_cc_email_list = df['Central_Management_Mail'].tolist()
                print("to_cc_email_list :",to_cc_email_list)
                to_cc_emails = ";".join(to_cc_email_list)
                print("to_ CC mails: ",to_cc_emails)
                
            body=instance.AT_Remarks
            send_email(to_mails, to_cc_emails, subject, body)


signal.connect(samsung_send_email_on_save, sender=Soft_AT_SAMSUNG_Rejected_Table)

# ################## For Zte ###################################

# @receiver(post_save, sender=Soft_AT_ZTE_Rejected_Table)
# def zte_send_email_on_save(sender, instance, created, **kwargs):
#     if created and instance.AT_STATUS.upper() in ["REJECT", "REJECTED"]:
#         print("Sending mail into the soft_at-zte", instance.AT_STATUS)
#         Rejection_Remark=instance.AT_Remarks
#         circle=instance.Circle
#         oem=instance.OEM
#         print("Rejection_Remark:",Rejection_Remark,"circle:",circle,"oem:",oem)
#         if not Rejection_Remarks.objects.filter(Rejection_Remark__iexact= Rejection_Remark).exists():
#             Rejection_Remarks.objects.create(Rejection_Remark=Rejection_Remark,Alarm_Bucket= "", OEM=oem, Final_Responsibility="Circle Team,NOC Team")
        
#         final_responsibilities = Rejection_Remarks.objects.filter(Rejection_Remark__iexact= Rejection_Remark)[0].Final_Responsibility
#         final_responsibilities = final_responsibilities.split(',')

            
#         for responsible_team in final_responsibilities:
#             if responsible_team == "Circle Team":
#                 Centeral_Responsible_Spoc_Mail_obj =  Circle_Responsible_Spoc.objects.filter(Circle__iexact=circle,OEM__iexact=oem)

#                 to_mails = Centeral_Responsible_Spoc_Mail_obj.values("Circle_Soft_At_Spoc_Mail")
#                 print("to mails....",to_mails)
#                 df = pd.DataFrame(to_mails)
#                 to_email_list = df['Circle_Soft_At_Spoc_Mail'].tolist()
#                 print("to_email_list :",to_email_list)
#                 to_emails = ";".join(to_email_list)
#                 print("to_mails: ",to_emails)

#                 ################circle pm  mails ######################
#                 Circle_PM_obj =  Circle_PM.objects.filter(Circle__iexact=circle,OEM__iexact=oem)
#                 to_circle_pm_mails = Circle_PM_obj.values("Circle_PM_Mail")
#                 print("to circle pm mails....",to_circle_pm_mails)
#                 df = pd.DataFrame(to_circle_pm_mails)
#                 to_circle_pm_email_list = df['Circle_PM_Mail'].tolist()
#                 print("to_circle_pm_email_list :",to_circle_pm_email_list)
#                 to_circle_pm_emails = ";".join(to_circle_pm_email_list)
#                 print("to circle pm mails: ",to_circle_pm_emails)
#                 to_mails = to_emails +";"+ to_circle_pm_emails
#                 print("to_mails:",to_mails)
#                 ################ to_cc #########################
#                 Central_Management_obj =  Central_Management.objects.filter(Circle__iexact=circle,OEM__iexact=oem)
#                 to_cc_mails = Central_Management_obj.values("Central_Management_Mail")
#                 print("to circle pm mails....",to_cc_mails)
#                 df = pd.DataFrame(to_cc_mails)
#                 to_cc_email_list = df['Central_Management_Mail'].tolist()
#                 print("to_cc_email_list :",to_cc_email_list)
#                 to_cc_emails = ";".join(to_cc_email_list)
#                 print("to_ CC mails: ",to_cc_emails)


#             if responsible_team == "NOC Team":

#                 Centeral_Responsible_Spoc_Mail_obj =  Centeral_Responsible_Spoc_Mail.objects.filter(Circle__iexact=circle,OEM__iexact=oem)

#                 to_mails = Centeral_Responsible_Spoc_Mail_obj.values("Central_Soft_At_Spoc_Mail")
#                 print("to mails....",to_mails)
#                 df = pd.DataFrame(to_mails)
#                 to_email_list = df['Central_Soft_At_Spoc_Mail'].tolist()
#                 print("to_email_list :",to_email_list)
#                 to_mails = ";".join(to_email_list)
#                 print("to_mails: ",to_mails)
#                 ################ to_cc #########################
#                 Central_Management_obj =  Central_Management.objects.filter(Circle__iexact=circle,OEM__iexact=oem)

#                 to_cc_mails = Central_Management_obj.values("Central_Management_Mail")
#                 print("to circle mails....",to_cc_mails)
#                 df = pd.DataFrame(to_cc_mails)
#                 to_cc_email_list = df['Central_Management_Mail'].tolist()
#                 print("to_cc_email_list :",to_cc_email_list)
#                 to_cc_emails = ";".join(to_cc_email_list)
#                 print("to_ CC mails: ",to_cc_emails)

#             body=instance.AT_Remarks
#             send_email(to_mails, to_cc_emails, subject, body)


# signal.connect(zte_send_email_on_save, sender=Soft_AT_ZTE_Rejected_Table)











    



