from celery import shared_task
from .models import *
from .views import circle_spoc_dict
from mailapp.tasks import send_email

priority_dict = {
        'P0':'Critical ',
        'P1':'High',
        'P2':'Moderate',
        'P3':'Low',    
    }
@shared_task
def level_wise_mail_notification():
        threshold_P0=Threshold.objects.get(priority="P0")
        threshold_P1=Threshold.objects.get(priority="P1")
        threshold_P2=Threshold.objects.get(priority="P2")
 
 
        open_records= Ticket_Counter_Table_Data.objects.filter(Status="OPEN")
        p0_records= open_records.filter(priority="P0")
        p1_records= open_records.filter(priority="P1")
        p2_records= open_records.filter(priority="P2")

        # p3_records= open_records.objects.filter(priority="P3")
        print("p0_records_count: ",p0_records.count())
        print("p1_records_count: ",p1_records.count())
        print("p2_records_count: ",p2_records.count())
        for p0_record in p0_records:
                circle=p0_record.Circle
                spoc_email = level1.objects.filter(circle=circle).values_list('email', flat=True)
                # Combine emails into a single string separated by ";"
                spoc_email= ";".join(spoc_email)
                l2_management_email = level2.objects.filter(circle=circle).values_list('email', flat=True)
                # Combine emails into a single string separated by ";"  
                l2_management_email = ";".join(l2_management_email)

                l3_management_email = level3.objects.filter(circle=circle).values_list('email', flat=True)
                # Combine emails into a single string separated by ";"
                l3_management_email = ";".join(l3_management_email)

                l4_management_email = level4.objects.filter(circle=circle).values_list('email', flat=True)
                # Combine emails into a single string separated by ";"
                l4_management_email = ";".join(l4_management_email)

                # spoc_details=circle_spoc_dict.get(circle,{})
                # spoc_email=spoc_details.get('Email')
                # l2_management_email=spoc_details.get('l2_management_email')
                # l3_management_email=spoc_details.get('l3_management_email')
                # l4_management_email=spoc_details.get('l4_management_email')

                if p0_record.aging == threshold_P0.threshold_aging_level_1:
                        print("inside ageing 3.........")
                        subject = "RCA Genie - L2 Escalation / Payload Dip Ticket/Priority: {priority}".format(priority=p0_record.priority)
                        body = f"""

                                Hi Team,

                                This is an automatically generated ticket raised by the RCA Genie. Below are the details:

                                Ticket ID: {p0_record.ticket_id}
                                Circle: {p0_record.Circle}      
                                Short Name: {p0_record.Short_name}
                                Site ID: {p0_record.Site_ID}
                                Status: {p0_record.Status}
                                Auto RCA: {p0_record.auto_rca}
                                Proposed Solution: {p0_record.proposed_solution}
                                Open Date: {p0_record.Open_Date}
                                Ageing: {p0_record.aging}
                                Date: {p0_record.Date}
                                Priority: {p0_record.priority}
                                TOOL LINK: "http://103.242.225.195:3000/"

                                Please review the details and take necessary action.

                                Note: This is an automated email. *Please do not reply to this mail.*

                                Regards,  
                                RCA Genie


                                """
                        to_mails=[spoc_email, l2_management_email]
                        cc_mails = [
                                    'Mohit.Batra@ust.com',
                                #     'Vinay.Duklan@ust.com',
                                    'Nishant.Verma@ust.com',
                                    'saurabh.rathore@mcpsinc.com',
                                    # 'Saurabh.Rathore@ust.com',
                                    'Nilesh.Jain@ust.com',
                                    l3_management_email,
                                    l4_management_email
                                ]
                        cc_mails_str = ';'.join(cc_mails)
                        to_mails_str = ';'.join(to_mails)
                        print("to: ",to_mails_str)
                        print("cc: ",cc_mails_str)
                        send_email.delay(to_mails_str, cc_mails_str ,subject, body)    
                        
                if p0_record.aging == threshold_P0.threshold_aging_level_3:
                        print("inside ageing 4.........")
                        subject = "RCA Genie - L3 Escalation / Payload Dip Ticket/Priority: {priority}".format(priority=p0_record.priority)
                        body = f"""

                                Hi Team,

                                This is an automatically generated ticket raised by the RCA Genie. Below are the details:

                                Ticket ID: {p0_record.ticket_id}
                                Circle: {p0_record.Circle}      
                                Short Name: {p0_record.Short_name}
                                Site ID: {p0_record.Site_ID}
                                Status: {p0_record.Status}
                                Auto RCA: {p0_record.auto_rca}
                                Proposed Solution: {p0_record.proposed_solution}
                                Open Date: {p0_record.Open_Date}
                                Ageing: {p0_record.aging}
                                Date: {p0_record.Date}
                                Priority: {p0_record.priority}
                                TOOL LINK: "http://103.242.225.195:3000/"

                                Please review the details and take necessary action.

                                Note: This is an automated email. *Please do not reply to this mail.*

                                Regards,  
                                RCA Genie       

                                """
                        to_mails=[spoc_email, l3_management_email,l2_management_email]
                        cc_mails = [
                                    'Mohit.Batra@ust.com',
                                #     'Vinay.Duklan@ust.com',
                                    'Nishant.Verma@ust.com',
                                    'saurabh.rathore@mcpsinc.com',
                                    # 'Saurabh.Rathore@ust.com',
                                    'Nilesh.Jain@ust.com',
                                    l4_management_email
                                ]
                        cc_mails_str = ';'.join(cc_mails)
                        to_mails_str = ';'.join(to_mails)
                        print("to: ",to_mails_str)
                        print("cc: ",cc_mails_str)
                        send_email.delay(to_mails_str, cc_mails_str ,subject, body)    
                        
                if p0_record.aging == threshold_P0.threshold_aging_level_4:
                        print("inside ageing 6.........")
                        subject = "RCA Genie - L4 Escalation / Payload Dip Ticket/Priority: {priority}".format(priority=p0_record.priority)
                        body = f"""

                                Hi Team,

                                This is an automatically generated ticket raised by the RCA Genie. Below are the details:

                                Ticket ID: {p0_record.ticket_id}
                                Circle: {p0_record.Circle}      
                                Short Name: {p0_record.Short_name}
                                Site ID: {p0_record.Site_ID}
                                Status: {p0_record.Status}
                                Auto RCA: {p0_record.auto_rca}
                                Proposed Solution: {p0_record.proposed_solution}
                                Open Date: {p0_record.Open_Date}
                                Ageing: {p0_record.aging}
                                Date: {p0_record.Date}
                                Priority: {p0_record.priority}
                                TOOL LINK: "http://103.242.225.195:3000/"

                                Please review the details and take necessary action.

                                Note: This is an automated email. *Please do not reply to this mail.*

                                Regards,  
                                RCA Genie

                                """
                        to_mails=[l4_management_email, l3_management_email,l2_management_email,spoc_email]
                        cc_mails = [
                                    'Mohit.Batra@ust.com',
                                #     'Vinay.Duklan@ust.com',
                                    'Nishant.Verma@ust.com',
                                    'saurabh.rathore@mcpsinc.com',
                                    # 'Saurabh.Rathore@ust.com',
                                    'Nilesh.Jain@ust.com',
                                ]
                        cc_mails_str = ';'.join(cc_mails)
                        to_mails_str = ';'.join(to_mails)   
                        print("to: ",to_mails_str)
                        print("cc: ",cc_mails_str)
                        send_email.delay(to_mails_str, cc_mails_str ,subject, body)    
                        





        for p1_record in p1_records:
                circle=p1_record.Circle
                spoc_email = level1.objects.filter(circle=circle).values_list('email', flat=True)
                # Combine emails into a single string separated by ";"
                spoc_email= ";".join(spoc_email)
                l2_management_email = level2.objects.filter(circle=circle).values_list('email', flat=True)
                # Combine emails into a single string separated by ";"  
                l2_management_email = ";".join(l2_management_email)

                l3_management_email = level3.objects.filter(circle=circle).values_list('email', flat=True)
                # Combine emails into a single string separated by ";"
                l3_management_email = ";".join(l3_management_email)

                l4_management_email = level4.objects.filter(circle=circle).values_list('email', flat=True)
                # Combine emails into a single string separated by ";"
                l4_management_email = ";".join(l4_management_email)

                # spoc_details=circle_spoc_dict.get(circle,{})
                # spoc_email=spoc_details.get('Email')
                # l2_management_email=spoc_details.get('l2_management_email')
                # l3_management_email=spoc_details.get('l3_management_email')
                # l4_management_email=spoc_details.get('l4_management_email')

                if p1_record.aging == threshold_P1.threshold_aging_level_2:
                        print("inside ageing 3.........")
                        subject = "RCA Genie - L2 Escalation / Payload Dip Ticket/Priority: {priority}".format(priority=p1_record.priority)
                        body = f"""

                                Hi Team,

                                This is an automatically generated ticket raised by the RCA Genie. Below are the details:

                                Ticket ID: {p1_record.ticket_id}
                                Circle: {p1_record.Circle}      
                                Short Name: {p1_record.Short_name}
                                Site ID: {p1_record.Site_ID}
                                Status: {p1_record.Status}
                                Auto RCA: {p1_record.auto_rca}
                                Proposed Solution: {p1_record.proposed_solution}
                                Open Date: {p1_record.Open_Date}
                                Ageing: {p1_record.aging}
                                Date: {p1_record.Date}
                                Priority: {p1_record.priority}
                                TOOL LINK: "http://103.242.225.195:3000/"

                                Please review the details and take necessary action.

                                Note: This is an automated email. *Please do not reply to this mail.*

                                Regards,  
                                RCA Genie


                                """
                        to_mails=[spoc_email, l2_management_email]
                        cc_mails = [
                                    'Mohit.Batra@ust.com',
                                #     'Vinay.Duklan@ust.com',
                                    'Nishant.Verma@ust.com',
                                    'saurabh.rathore@mcpsinc.com',
                                    # 'Saurabh.Rathore@ust.com',
                                    'Nilesh.Jain@ust.com',
                                    l3_management_email,
                                    l4_management_email
                                ]
                        cc_mails_str = ';'.join(cc_mails)
                        to_mails_str = ';'.join(to_mails)
                        print("to: ",to_mails_str)
                        print("cc: ",cc_mails_str)
                        send_email.delay(to_mails_str, cc_mails_str ,subject, body)    
                        
                if p1_record.aging == threshold_P1.threshold_aging_level_3:
                        print("inside ageing 4.........")
                        subject = "RCA Genie - L3 Escalation / Payload Dip Ticket/Priority: {priority}".format(priority=p1_record.priority)
                        body = f"""

                                Hi Team,

                                This is an automatically generated ticket raised by the RCA Genie. Below are the details:

                                Ticket ID: {p1_record.ticket_id}
                                Circle: {p1_record.Circle}      
                                Short Name: {p1_record.Short_name}
                                Site ID: {p1_record.Site_ID}
                                Status: {p1_record.Status}
                                Auto RCA: {p1_record.auto_rca}
                                Proposed Solution: {p1_record.proposed_solution}
                                Open Date: {p1_record.Open_Date}
                                Ageing: {p1_record.aging}
                                Date: {p1_record.Date}
                                Priority: {p1_record.priority}
                                TOOL LINK: "http://103.242.225.195:3000/"

                                Please review the details and take necessary action.

                                Note: This is an automated email. *Please do not reply to this mail.*

                                Regards,  
                                RCA Genie       

                                """
                        to_mails=[spoc_email, l3_management_email,l2_management_email]
                        cc_mails = [
                                    'Mohit.Batra@ust.com',
                                #     'Vinay.Duklan@ust.com',
                                    'Nishant.Verma@ust.com',
                                    'saurabh.rathore@mcpsinc.com',
                                    # 'Saurabh.Rathore@ust.com',
                                    'Nilesh.Jain@ust.com',
                                    l4_management_email
                                ]
                        cc_mails_str = ';'.join(cc_mails)
                        to_mails_str = ';'.join(to_mails)
                        print("to: ",to_mails_str)
                        print("cc: ",cc_mails_str)
                        send_email.delay(to_mails_str, cc_mails_str ,subject, body)    
                        
                if p1_record.aging == threshold_P1.threshold_aging_level_4:
                        print("inside ageing 6.........")
                        subject = "RCA Genie - L4 Escalation / Payload Dip Ticket/Priority: {priority}".format(priority=p1_record.priority)
                        body = f"""

                                Hi Team,

                                This is an automatically generated ticket raised by the RCA Genie. Below are the details:

                                Ticket ID: {p1_record.ticket_id}
                                Circle: {p1_record.Circle}      
                                Short Name: {p1_record.Short_name}
                                Site ID: {p1_record.Site_ID}
                                Status: {p1_record.Status}
                                Auto RCA: {p1_record.auto_rca}
                                Proposed Solution: {p1_record.proposed_solution}
                                Open Date: {p1_record.Open_Date}
                                Ageing: {p1_record.aging}
                                Date: {p1_record.Date}
                                Priority: {p1_record.priority}
                                TOOL LINK: "http://103.242.225.195:3000/"

                                Please review the details and take necessary action.

                                Note: This is an automated email. *Please do not reply to this mail.*

                                Regards,  
                                RCA Genie

                                """
                        to_mails=[l4_management_email, l3_management_email,l2_management_email,spoc_email]
                        cc_mails = [
                                    'Mohit.Batra@ust.com',
                                #     'Vinay.Duklan@ust.com',
                                    'Nishant.Verma@ust.com',
                                    'saurabh.rathore@mcpsinc.com',
                                    # 'Saurabh.Rathore@ust.com',
                                    'Nilesh.Jain@ust.com',
                                ]
                        cc_mails_str = ';'.join(cc_mails)
                        to_mails_str = ';'.join(to_mails)   
                        print("to: ",to_mails_str)
                        print("cc: ",cc_mails_str)
                        send_email.delay(to_mails_str, cc_mails_str ,subject, body)    
                        

        

        for p2_record in p2_records:
                circle=p2_record.Circle
                spoc_email = level1.objects.filter(circle=circle).values_list('email', flat=True)
                # Combine emails into a single string separated by ";"
                spoc_email= ";".join(spoc_email)
                l2_management_email = level2.objects.filter(circle=circle).values_list('email', flat=True)
                # Combine emails into a single string separated by ";"  
                l2_management_email = ";".join(l2_management_email)

                l3_management_email = level3.objects.filter(circle=circle).values_list('email', flat=True)
                # Combine emails into a single string separated by ";"
                l3_management_email = ";".join(l3_management_email)

                l4_management_email = level4.objects.filter(circle=circle).values_list('email', flat=True)
                # Combine emails into a single string separated by ";"
                l4_management_email = ";".join(l4_management_email)

                # spoc_details=circle_spoc_dict.get(circle,{})
                # spoc_email=spoc_details.get('Email')
                # l2_management_email=spoc_details.get('l2_management_email')
                # l3_management_email=spoc_details.get('l3_management_email')
                # l4_management_email=spoc_details.get('l4_management_email')

                if p2_record.aging == threshold_P2.threshold_aging_level_2:
                        print("inside ageing 3.........")
                        subject = "RCA Genie - L2 Escalation / Payload Dip Ticket/Priority: {priority}".format(priority=p2_record.priority)
                        body = f"""

                                Hi Team,

                                This is an automatically generated ticket raised by the RCA Genie. Below are the details:

                                Ticket ID: {p2_record.ticket_id}
                                Circle: {p2_record.Circle}      
                                Short Name: {p2_record.Short_name}
                                Site ID: {p2_record.Site_ID}
                                Status: {p2_record.Status}
                                Auto RCA: {p2_record.auto_rca}
                                Proposed Solution: {p2_record.proposed_solution}
                                Open Date: {p2_record.Open_Date}
                                Ageing: {p2_record.aging}
                                Date: {p2_record.Date}
                                Priority: {p2_record.priority}
                                TOOL LINK: "http://103.242.225.195:3000/"

                                Please review the details and take necessary action.

                                Note: This is an automated email. *Please do not reply to this mail.*

                                Regards,  
                                RCA Genie


                                """
                        to_mails=[spoc_email, l2_management_email]
                        cc_mails = [
                                    'Mohit.Batra@ust.com',
                                #     'Vinay.Duklan@ust.com',
                                    'Nishant.Verma@ust.com',
                                    'saurabh.rathore@mcpsinc.com',
                                    # 'Saurabh.Rathore@ust.com',
                                    'Nilesh.Jain@ust.com',
                                    l3_management_email,
                                    l4_management_email
                                ]
                        cc_mails_str = ';'.join(cc_mails)
                        to_mails_str = ';'.join(to_mails)
                        print("to: ",to_mails_str)
                        print("cc: ",cc_mails_str)
                        send_email.delay(to_mails_str, cc_mails_str ,subject, body)    
                        
                if p2_record.aging == threshold_P2.threshold_aging_level_3:
                        print("inside ageing 4.........")
                        subject = "RCA Genie - L3 Escalation / Payload Dip Ticket/Priority: {priority}".format(priority=p2_record.priority)
                        body = f"""

                                Hi Team,

                                This is an automatically generated ticket raised by the RCA Genie. Below are the details:

                                Ticket ID: {p2_record.ticket_id}
                                Circle: {p2_record.Circle}      
                                Short Name: {p2_record.Short_name}
                                Site ID: {p2_record.Site_ID}
                                Status: {p2_record.Status}
                                Auto RCA: {p2_record.auto_rca}
                                Proposed Solution: {p2_record.proposed_solution}
                                Open Date: {p2_record.Open_Date}
                                Ageing: {p2_record.aging}
                                Date: {p2_record.Date}
                                Priority: {p2_record.priority}
                                TOOL LINK: "http://103.242.225.195:3000/"

                                Please review the details and take necessary action.

                                Note: This is an automated email. *Please do not reply to this mail.*

                                Regards,  
                                RCA Genie       

                                """
                        to_mails=[spoc_email, l3_management_email,l2_management_email]
                        cc_mails = [
                                    'Mohit.Batra@ust.com',
                                #     'Vinay.Duklan@ust.com',
                                    'Nishant.Verma@ust.com',
                                    'saurabh.rathore@mcpsinc.com',
                                    # 'Saurabh.Rathore@ust.com',
                                    'Nilesh.Jain@ust.com',
                                    l4_management_email
                                ]
                        cc_mails_str = ';'.join(cc_mails)
                        to_mails_str = ';'.join(to_mails)
                        print("to: ",to_mails_str)
                        print("cc: ",cc_mails_str)
                        send_email.delay(to_mails_str, cc_mails_str ,subject, body)    
                        
                if p2_record.aging == threshold_P2.threshold_aging_level_4:
                        print("inside ageing 6.........")
                        subject = "RCA Genie - L4 Escalation / Payload Dip Ticket/Priority: {priority}".format(priority=p2_record.priority)
                        body = f"""

                                Hi Team,

                                This is an automatically generated ticket raised by the RCA Genie. Below are the details:

                                Ticket ID: {p2_record.ticket_id}
                                Circle: {p2_record.Circle}      
                                Short Name: {p2_record.Short_name}
                                Site ID: {p2_record.Site_ID}
                                Status: {p2_record.Status}
                                Auto RCA: {p2_record.auto_rca}
                                Proposed Solution: {p2_record.proposed_solution}
                                Open Date: {p2_record.Open_Date}
                                Ageing: {p2_record.aging}
                                Date: {p2_record.Date}
                                Priority: {p2_record.priority}
                                TOOL LINK: "http://103.242.225.195:3000/"

                                Please review the details and take necessary action.

                                Note: This is an automated email. *Please do not reply to this mail.*

                                Regards,  
                                RCA Genie

                                """
                        to_mails=[l4_management_email, l3_management_email,l2_management_email,spoc_email]
                        cc_mails = [
                                    'Mohit.Batra@ust.com',
                                #     'Vinay.Duklan@ust.com',
                                    'Nishant.Verma@ust.com',
                                    'saurabh.rathore@mcpsinc.com',
                                    # 'Saurabh.Rathore@ust.com',
                                    'Nilesh.Jain@ust.com',
                                ]
                        cc_mails_str = ';'.join(cc_mails)
                        to_mails_str = ';'.join(to_mails)   
                        print("to: ",to_mails_str)
                        print("cc: ",cc_mails_str)
                        send_email.delay(to_mails_str, cc_mails_str ,subject, body)    
                        
