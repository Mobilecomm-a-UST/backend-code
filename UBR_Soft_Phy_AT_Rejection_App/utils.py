import re
import numpy as np
from pathlib import Path
import pythoncom
import win32com.client
import datetime
import os
from datetime import datetime as dt
import logging
import pandas as pd
from UBR_Soft_Phy_AT_Rejection_App.serializers import * 
from UBR_Soft_Phy_AT_Rejection_App.models import *
from django.db.models import Min, Max
from django.db.models import Max, F,Subquery, OuterRef
from django.db.models.functions import Coalesce
from django.db import connection
import pytz
import json
from django.db import connection

def call_stored_procedure():
    with connection.cursor() as cursor:
        cursor.execute('CALL learning()')
        # Fetch all rows from the cursor
        rows = cursor.fetchall()
        # Fetch column names
        columns = [col[0] for col in cursor.description]
    # Prepare a list of dictionaries where each dictionary represents a row
    data = [dict(zip(columns, row)) for row in rows]
    # Convert the list of dictionaries to JSON
    json_data = json.dumps(data)
    return json_data




target_senders = ["nishant.verma@mcpsinc.in","alpana.k@mcpsinc.com", "vinay.duklan@mcpsinc.in"]

oem_dict={}

def subject_filteration(all_messages):

      

    list_of_subjects_rx = [
                        re.compile(r'^.*FW: UBR_RADWIN_JK_MOBILECOMM$'),
                    ]
    
    list1=["Ericcsion"]
    for i,x in enumerate(list_of_subjects_rx):
        oem_dict[x.pattern]=list1[i]
       

    filtered_messages = []
    
    oem=[]
    
    for message in all_messages:
        print("message_________",message)
        subject = message.Subject.strip()
        print("subject....",subject)
        print(f"message{i}.............subject",subject)
        logging.debug(f"Processing subject: {subject}")

        for subject_filter_regex in list_of_subjects_rx:
            try:
                if subject_filter_regex.match(subject):
                    
                    oem.append(oem_dict[subject_filter_regex.pattern])
                    logging.debug("Match found.")
                    print("Match found.")
                    filtered_messages.append(message)
            except re.error as e:
                logging.error(f"Error in regex pattern: {e}")
    print("filtered_message...........", filtered_messages)
    print("list_of_oems...............",oem)
        # exit(0)
    return filtered_messages,oem

def get_min_max_date_time(soft_obj):
    # Initialize with None values
    soft_min_date = soft_max_date = None
    min_date_list=[]
    max_date_list=[]
    # Check if data exists for Huawei

    

    # Check if data exists for Nokia
    if soft_obj.exists():
        soft_min_date = soft_obj.aggregate(min_date=Min('Date_Time'))['min_date']
        soft_max_date = soft_obj.aggregate(max_date=Max('Date_Time'))['max_date']
        min_date_list.append(soft_min_date)
        max_date_list.append(soft_max_date)


    # Combine the results
    overall_min_date = min(filter(None, min_date_list))
    overall_max_date = max(filter(None, max_date_list))



    overall_min_date_formatted = overall_min_date.strftime('%Y-%m-%d %H:%M %S')  # Adjust the format as needed
    overall_max_date_formatted = overall_max_date.strftime('%Y-%m-%d %H:%M %S')


    print(f"Min Date: {overall_min_date}")
    print(f"Max Date: {overall_max_date}")

    return overall_min_date, overall_max_date

    ##### format for 12hrs for timing##########################################

    # overall_min_date_formatted = overall_min_date.strftime('%Y-%m-%d %I:%M %p')  # Adjust the format as needed
    # overall_max_date_formatted = overall_max_date.strftime('%Y-%m-%d %I:%M %p')

    # Print and return the results
   
    # print(f"Minimum Date: {overall_min_date_formatted}")
    # print(f"Maximum Date: {overall_max_date_formatted}")

    # return overall_min_date_formatted, overall_max_date_formatted
    ##########################################################################
def process_and_save_to_database(df, received_date_time):
   for i, d in df.iterrows():
        print("inside test")
        if  not pd.isnull(d['OFFERED DATE']):
            Offered_Date = pd.to_datetime(d['OFFERED DATE'], format='%d-%b-%y').date()
            print("Offered_Date",Offered_Date)
        else:
            Offered_Date=None

        obj= UBR_Soft_Phy_AT_Rejection_Table.objects.create(
                    Circle = str(d["CIRCLE"]),
                    Site_ID	= str(d["SITE ID"]),
                    Site_Type = str(d["SITE TYPE"]),
                    TSP = str(d["TSP"]),
                    Link_Id = str(d["LINK ID"]),
                    RA_Number = str(d["RA NUMBER"]),
                    CKT_ID =str(d["CKT ID"]),
                    UBR_Make_OEM = 	str(d["UBR MAKE/OEM"]),
                    UBR_Model = str(d["UBR MODEL"]),
                    Site_A_IP =str(d["SITE A IP"]) ,
                    Site_B_IP =str(d["SITE B IP"]) ,
                    Re_offer = str(d["RE-OFFER"]),
                    Soft_Physical = str(d["SOFT /PHYSICAL"])	,
                    Offered_Date = Offered_Date,
                    AT_Status = str(d["AT STATUS"]),
                    Reasons=str(d["REASONS"]),
                    Date_Time = received_date_time,
        )
        print("OBJ: ",obj)
      
        




def UBR_Soft_AT_Rejected_save(multiple,all_items):
    pythoncom.CoInitialize()
    # Create output folder
    output_dir = Path.cwd() / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Specify the sender's email addresses to filter (separated by ';'
   
    filtered_messages = []
    if multiple == True:
        print("inside it..")
        # Connect to Outlook
        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")
        # Connect to Inbox folder
        accounts=namespace.Accounts
        print("using_loogined_account:",accounts.Item(1).SmtpAddress)
        inbox = accounts.Item(1).DeliveryStore.GetDefaultFolder(6)  # 6 corresponds to the Inbox
        print(inbox.Items.Count)
        # Get today's date
        today_date = datetime.datetime.now().date()
        print("todays_date...",today_date)
        filter_condition = "[ReceivedTime] >= '" + today_date.strftime('%m/%d/%Y') + "'"
        all_messages = inbox.Items.Restrict(filter_condition)
        # print(all_messages.Count)
        print("all_messages..........",all_messages.Count)
    else:
        all_messages =all_items


    tup_meessage_oem = subject_filteration(all_messages)
    filtered_messages = tup_meessage_oem[0]
    oem_list= tup_meessage_oem[1]
    

    print("line execution")

    for i,message in enumerate(filtered_messages):
        # try:
            # received_time = message.ReceivedTime
        received_time = message.ReceivedTime
        # received_date_time=received_time
        received_date_time = dt.utcfromtimestamp(received_time.timestamp())
        utc_timezone = pytz.timezone('UTC')

        # Convert the ReceivedTime to a datetime object without adjusting the time zone offset
        received_time_utc = utc_timezone.localize(received_date_time)
        print("received_time_utc",received_time_utc)
        print(received_time)
        # print("print................................", type(received_date_time))
        print("print................................", received_date_time)
        received_date_time =received_time_utc
        
        transport_headers = message.PropertyAccessor.GetProperty("http://schemas.microsoft.com/mapi/proptag/0x007D001E")
        match = re.search(r"From:.*?<([^>]+)>", transport_headers)
        sender_email = match.group(1) if match else "Unknown Sender"
        print("sender_mail",sender_email)
        
        
        if any(target_sender.lower() == sender_email.lower() for target_sender in target_senders):
            subject = sanitize_filename(message.Subject)
            print("______________________________just test_________________")
        
        
            # try:
            body = message.Body

            # Extract tabular data from the body
            start_marker = "Circle"
            end_marker = "Reasons"
            start_index = body.find(start_marker)
            end_index = body.find(end_marker, start_index + len(start_marker))
        
        
            if start_index != -1 and end_index != -1:
                # Extract headers
                headers_text = body[start_index + len(start_marker):end_index].strip()
                headers = re.split(r'\r\n\r\n|\r\n', headers_text)
                headers = ['Circle'] + headers + ['Reasons']
                print("header",headers)
                # Extract data
                data_text = body[end_index + len(end_marker):].strip()
                data_lines = []
                skip_next_lines = False
                skip_https = False

                for line in data_text.split('\n'):
                        if "From:" in line:
                            skip_next_lines = True
                        elif skip_next_lines:
                            if not line.strip():  # Break if an empty line is encountered
                                break
                        if "<https:" in line:
                            skip_https = True
                        elif skip_https:
                            if not line.strip():  # Break if an empty line is encountered
                                break    
                        else:
                            data_lines.append(line)

                print("data_text___________",data_text)
                unwanted_patterns = ["Signature", "www.mcpsinc.com",'Alpana kumari','MobileComm Technologies India Pvt. Ltd |','758 Udyog Vihar Phase 5 |','P.O. Box 122016 | Gurgaon','BR//','Abhinay Barnwal',
                                            'Regards','Neelima Singh','AT Team']
                # email_pattern = re.compile(r'From:\s+([^\s<>]+@[^\s<>]+)')
                data = []
                for line in data_lines:

                    if line.strip('\r') and not any(pattern in line for pattern in unwanted_patterns):
                        # Split the line, handling blank cells
                        row_data = [col.strip() if col.strip() else None for col in line.strip().split('\r')]
                        data.append(row_data)
                        if "From:" in line:
                                # skip_line = True
                                break
                        # print("______________________", data)

                # Check if the length of each row matches the length of headers
                for i, row in enumerate(data):

                    if len(row) < len(headers):
                        # Pad the row with None values to match the length of headers
                        data[i] += [None] * (len(headers) - len(row))
                        # print("_____________data_____________",data)

                # Transpose the data to distribute across all columns
                transposed_data = list(map(list, zip(*data)))

                body_mail = [item if item is not None else None for sublist in transposed_data for item in sublist]
                # print("__________body__________mail___________",body_mail)

                # Reshape the data into a 2D array
                reshaped_data = np.array(body_mail).reshape(-1, len(headers))
                # reshaped_data = reshaped_data.replace("", "NA")
                print("reshaped________________data",reshaped_data)

                # Create DataFrame
                table_df = pd.DataFrame(reshaped_data, columns=headers)

                # Create a folder for each message
                target_folder = output_dir / subject
                target_folder.mkdir(parents=True, exist_ok=True)

                # Save the DataFrame to an Excel file
                excel_file_path = target_folder / f"{subject}_data.xlsx"
                print(excel_file_path, "__________hi_______________")
                table_df.to_excel(excel_file_path, index=False, header=True, sheet_name='UBR')
                df = pd.read_excel(excel_file_path)
                df.dropna(subset=['Circle'], inplace=True)
                df.columns = df.columns.str.upper().str.strip()
                df = df.applymap(lambda x: x.upper().strip() if isinstance(x, str) else x)
                print("df_____",df)



                process_and_save_to_database(df, received_date_time) 

                     

                print(f"Table data saved to Excel: {excel_file_path}")

   

                        
  

                        
def get_latest_record_per_site(oem_table):
    # Assuming Soft_AT_NOKIA_Rejected_Table and Soft_AT_HUAWEI_Rejected_Table are Django models

    site_id_field = "Site_ID" if oem_table == UBR_Soft_Phy_AT_Rejection_Table else "Site_ID_2G"

    # Step 1: Get primary keys of the latest records per site
    latest_records_subquery = (
        oem_table.objects
        .filter(**{site_id_field: OuterRef(site_id_field)})  # Filter by site_id
        .order_by('-Date_Time')  # Order by Date_Time descending
        .values('pk')  # Get primary key
        [:1]  # Take only the first record (latest)
    )

    # Step 2: Use subquery result to fetch complete records
    latest_records = oem_table.objects.filter(pk__in=Subquery(latest_records_subquery))

    # Step 3: Print or process the complete records
    for record in latest_records:
        print(record)

    return latest_records


def sanitize_filename(name):
    # Replace invalid characters with underscores
    cleaned_name = re.sub(r'[<>:"/\\|?*]', '_', name)

    # Remove leading and trailing whitespaces
    return cleaned_name.strip()

