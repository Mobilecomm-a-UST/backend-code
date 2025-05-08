from mailapp.tasks import send_email
from .models import *
def send_email_spoc_circle(df, spoc_dict):
    """
    Sends formatted emails to the respective SPOC based on the given data.
    
    Args:
        df (DataFrame): Data containing ticket details.
        spoc_dict (dict): Dictionary containing SPOC details (Name, Email) for each circle.
    """
    print('Enter into the send mail function.')
    priority_dict = {
        'P0':'Critical ',
        'P1':'High',
        'P2':'Moderate',
        'P3':'Low',
    }
    for index, row in df.iterrows():
        circle = row['Circle']
        # spoc_details = spoc_dict.get(circle, {})
        # spoc_name = spoc_details.get('Name', 'SPOC')
        # spoc_email = spoc_details.get('Email')
        spoc_name = level1.objects.filter(circle=circle).values_list('person_name', flat=True)
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

        ticket_type = row['ticket_type']
        if not spoc_email:
            print(f"No email found for Circle: {circle}. Skipping...")
            continue
        if ticket_type == 'Payload':
        
        # Email subject
            subject = "RCA Genie - Payload Dip Ticket/Priority: {priority}".format(priority=priority_dict[row['priority']])
        if ticket_type == 'Sleeping Cell':
            subject = "RCA Genie - Sleeping Cell Ticket/Priority: {priority}".format(priority=priority_dict[row['priority']])
        # Email body with the note
        body = f"""
            Hi {spoc_name},
            
            This is an automatically generated ticket raised by the RCA Genie. Below are the details:

            Ticket ID: {row['ticket_id']}
            Circle: {row['Circle']}
            Cell Name: {row['Short_name']}
            Site ID: {row['Site_ID']}
            Status: {row['Status']}
            AUTO RCA: {row['auto_rca']}
            Proposed Solution: {row['proposed_solution']}
            Open Date: {row['Open_Date']}
            Aging: {row['aging']}
            Date: {row['Date']}
            Priority: {row['priority']}
            TOOL LINK: "http://103.242.225.195:3000/"

            Please review the details and take necessary action.

            Note: This is an automated email. *Please do not reply to this mail.*

            Regards,  
            RCA Genie
        """

        # CC emails
        cc_mails = [ l2_management_email, l3_management_email, l4_management_email,
            'Mohit.Batra@ust.com',
            'Vinay.Duklan@ust.com',
            'Nishant.Verma@ust.com',
            'saurabh.rathore@mcpsinc.com',
            'Nilesh.Jain@ust.com'
        ]
        cc_mails_str = ';'.join(cc_mails)
        
        print(cc_mails_str)

        # Send the email asynchronously
        send_email.delay(spoc_email, cc_mails_str, subject, body)
        print(f"Email sent to {spoc_email} for Circle: {circle}.")
