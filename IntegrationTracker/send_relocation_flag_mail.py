from mailapp.tasks import send_email
from .models import *
import pandas as pd

def send_email_for_relocation(objs):
    """
    Sends formatted emails to the respective SPOC based on the given data.
    
    Args:
        objs (QuerySet): QuerySet containing relocation records.
    """
    df = pd.DataFrame(list(objs.values()))

    to_mails = [
                'Chandan.Kumar2@ust.com',
                'Abhishek.Gupta@ust.com',
                'Rahul.Dahiya@ust.com',
                'Aashish.Sharma@ust.com',
                'krishna.kantverma@ust.com',
                'Amit.Rai@ust.com',
                ]
    
    to_email = ";".join(to_mails)

    cc_mails = ['Abhinav.Verma@ust.com',
                'Prerna.PramodKumar@ust.com',
                # 'Vinay.Duklan@ust.com'
                ]
    
    cc_mails_str = ";".join(cc_mails)

    to_email_second = ['Mohit.Batra@ust.com',
                                    'saurabh.rathore@ust.com']
    
    to_email_str = ";".join(to_email_second)

    for _, row in df.iterrows():
        record = Relocation_tracker.objects.get(id=row["id"])  

     
        if record.mail_sent:
            print(f"Skipping email for record {record.id} (already sent)")
            continue

        subject = None
        body = None

        if row.get("both_site_locked") == "Yes":
            subject = "Relocation flag/both site locked"
            body = f"""
                Both site locked
                New Site ID: {row["new_site_id"]}
                Old Site ID: {row["old_site_id"]}

                Please review the details and take necessary action.

                Note: This is an automated email. *Please do not reply to this mail.*

                Regards,  
                RCA Genie
            """
        elif row.get("both_site_unlocked") == "Yes":
            subject = "Relocation flag/both site unlocked"
            body = f"""
                Both site unlocked
                New Site ID: {row["new_site_id"]}
                Old Site ID: {row["old_site_id"]}

                Please review the details and take necessary action.

                Note: This is an automated email. *Please do not reply to this mail.*

                Regards,  
                RCA Genie
            """
        elif row.get("allocated_vs_deployed_tech_deviation") == "Yes":
            subject = "Relocation flag/allocated vs deployed tech deviation"
            body = f"""
                Allocated vs deployed tech deviation
                New Site ID: {row["new_site_id"]}
                Old Site ID: {row["old_site_id"]}
                Allocated vs deployed tech: {row["allocated_vs_deployed_tech"]}

                Please review the details and take necessary action.

                Note: This is an automated email. *Please do not reply to this mail.*

                Regards,  
                RCA Genie
            """
        elif row.get("old_vs_deployed_tech_deviation") == "Yes":
            subject = "Relocation flag/old vs deployed tech deviation"
            body = f"""
                Old vs deployed tech deviation
                New Site ID: {row["new_site_id"]}
                Old Site ID: {row["old_site_id"]}
                Old vs deployed tech: {row["old_vs_deployed_tech"]}

                Please review the details and take necessary action.

                Note: This is an automated email. *Please do not reply to this mail.*

                Regards,  
                RCA Genie
            """

        if subject and body:
            print(f"Sending email: {subject}")
            send_email.delay(to_email, cc_mails_str, subject, body)
            print(f"Email sent to {to_email}")


            print(f"Scheduling second email to {to_email_str} in 1 hour")
            send_email.apply_async((to_email_str,cc_mails_str, subject, body), countdown=3600)
            print(f"Second email scheduled for {to_email_str}")
           
            record.mail_sent = True
            # record.save(update_fields=["email_sent"])
            record.save()

    print("Emails sent successfully")



# from mailapp.tasks import send_email
# from .models import *
# import pandas as pd
# def send_email_for_relocation(objs):
#     """
#     Sends formatted emails to the respective SPOC based on the given data.
    
#     Args:
#         df (DataFrame): Data containing ticket details.
#         spoc_dict (dict): Dictionary containing SPOC details (Name, Email) for each circle.
#     """
#     # df= pd.DataFrame(objs)
#     df = pd.DataFrame(list(objs.values()))
#     print(df.columns)

#     for index, row in df.iterrows():
#         # print(row)
#         subject = ' '
#         body = ''
#         if row["both_site_locked"] == "Yes":
#             old_site_id= row["old_site_id"]
#             new_site_id= row["new_site_id"]
#             subject = "Relocation flag/both site locked"
#             body = f"""
#                         Both site locked
#                         New Site ID: {new_site_id}
#                         Old Site ID: {old_site_id}

#                         Please review the details and take necessary action.

#                         Note: This is an automated email. *Please do not reply to this mail.*

#                         Regards,  
#                         RCA Genie
#                     """
#             print("sending mail from both site locked", old_site_id, new_site_id)
#         if row["both_site_unlocked"] == "Yes":
#              new_site_id= row["new_site_id"]
#              old_site_id= row["old_site_id"]
#              subject = "Relocation flag/both site unlocked"
#              body = f"""
#                         Both site unlocked
#                         New Site ID: {new_site_id}
#                         Old Site ID: {old_site_id}
                        
#                         Please review the details and take necessary action.

#                         Note: This is an automated email. *Please do not reply to this mail.*

#                         Regards,  
#                         RCA Genie
#                     """
#              print("sending mail from both site unlocked", old_site_id, new_site_id)
        
#         if row["allocated_vs_deployed_tech_deviation"] == "Yes":
#              new_site_id= row["new_site_id"]
#              old_site_id= row["old_site_id"]
#              subject = "Relocation flag/allocated vs deployed tech deviation"
#              body = f"""
#                         Allocated vs deployed tech deviation
#                         New Site ID: {new_site_id}
#                         Old Site ID: {old_site_id}
#                         Allocated vs deployed tech : {row["allocated_vs_deployed_tech"]}
#                         Please review the details and take necessary action.

#                         Note: This is an automated email. *Please do not reply to this mail.*

#                         Regards,
#                         RCA Genie
#                     """
#              print("sending mail from allocated vs deployed tech deviation", old_site_id, new_site_id)

#         if row["old_vs_deployed_tech_deviation"] == "Yes":  
#              new_site_id= row["new_site_id"]
#              old_site_id= row["old_site_id"]
#              subject = "Relocation flag/old vs deployed tech deviation"
#              body = f"""
#                         Old vs deployed tech deviation
#                         New Site ID: {new_site_id}
#                         Old Site ID: {old_site_id}
#                         Old vs deployed tech : {row["old_vs_deployed_tech"]}
#                         Please review the details and take necessary action.

#                         Note: This is an automated email. *Please do not reply to this mail.*

#                         Regards,
#                         RCA Genie
#                     """
#              print("sending mail from old vs deployed tech deviation", old_site_id, new_site_id)
#         # Email body
#         # Email subject

#         # subject = "Relocation flag"
#         # Email body with the note

#         to_mails = [
#             # "Mohit.Batra@ust.com",
#             # "Nishant.Verma@ust.com",
#             # "saurabh.rathore@mcpsinc.com",
#             'Abhinav.Verma@ust.com',
#             'Prerna.PramodKumar@ust.com'
#         ]
#         to_email = ";".join(to_mails)
#         # CC emails
#         cc_mails = [ 
#             # 'Mohit.Batra@ust.com',
#             # 'Nishant.Verma@ust.com',
#             # 'saurabh.rathore@mcpsinc.com',
#             # 'Nilesh.Jain@ust.com'
#             'Abhinav.Verma@ust.com',
#             'Vinay.Duklan@ust.com',
#             # 'Nikita.Singh@ust.com'
#         ]
#         cc_mails_str = ';'.join(cc_mails)
        
#         print("cc:- ",cc_mails_str)
#         # Send the email asynchronously
#         send_email.delay(to_email, cc_mails_str, subject, body)
#         print(f"Email sent to {to_email}")

