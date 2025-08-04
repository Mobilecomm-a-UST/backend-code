from django.shortcuts import render
from django.db import connection
# Create your views here.
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from openpyxl import load_workbook
import pandas as pd
from .models import IntegrationData, Document
import json
from rest_framework.exceptions import ValidationError
from asgiref.sync import sync_to_async
import os

from django.conf import settings

from .serializers import IntegrationDataSerializer

from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
from SOFT_AT_VINAY.models import Soft_At_Table
from datetime import datetime, timedelta
import pandas as pd
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from .models import fixed_pre_traffic, daily_pre_traffic, daily_post_traffic 

from rest_framework.response import Response
from django.db.models import Count
from .models import IntegrationData
from datetime import datetime, timedelta

from .serializers import New_site_locked_unlocked_date_serializer ,old_site_locked_unlocked_date_serializer
from .models import *





def generate_date_list(start_date):
    # Parse the input date (assuming it's a string in 'YYYY-MM-DD' format)
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    
    # Get the current date
    current_date = datetime.now().date()
    
    # Initialize an empty list to store the dates
    date_list = []
    
    # Generate dates from start_date to current_date
    delta = timedelta(days=1)  # Step by 1 day
    while start_date <= current_date:
        date_list.append(start_date)
        start_date += delta
    
    return date_list
@api_view(['GET'])
def get_excel_temp_link(request):
    #mcom123 temp id.
    # Path to the Excel file
    file_path = os.path.join(settings.MEDIA_ROOT, 'IntegrationTracker', 'Integration_Tracker_Template_V1.8.1.xlsm')

    # Check if the file exists
    if os.path.exists(file_path):
        # Construct the URL to access the file
        file_url = os.path.join(settings.MEDIA_URL ,'IntegrationTracker' , 'Integration_Tracker_Template_V1.8.1.xlsm')              
        return Response({'file_url': file_url,'template_version':'v1.8.1'}, status=status.HTTP_200_OK)
    else:
        # Return a 404 response if the file does not exist
        return Response({'error': 'Excel file not found'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def get_relocation_excel_temp_link(request):
    #mcom123 temp id.
    # Path to the Excel file
    file_path = os.path.join(settings.MEDIA_ROOT, 'RelocationTracker', 'Relocation_Temp_v1.0.xlsx')

    # Check if the file exists
    if os.path.exists(file_path):
        # Construct the URL to access the file
        file_url = os.path.join(settings.MEDIA_URL ,'RelocationTracker' , 'Relocation_Temp_v1.0.xlsx')              
        return Response({'file_url': file_url,'template_version':'v1.0'}, status=status.HTTP_200_OK)
    else:
        # Return a 404 response if the file does not exist
        return Response({'error': 'Excel file not found'}, status=status.HTTP_404_NOT_FOUND)

import openpyxl
from io import BytesIO

def read_excel_cell(file_contents, sheet_name, cell):
    # Load the Excel file from memory
    wb = openpyxl.load_workbook(filename=BytesIO(file_contents))
    
    # Select the specific sheet by name
    sheet = wb[sheet_name]
    
    # Get the value of the specified cell
    cell_value = sheet[cell].value
    
    return cell_value


@api_view(['POST'])
def upload_excel(request):
    print("User: ", request.user.username)
    if 'file' not in request.data:
        return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

    file = request.data['file']
    value_in_cell = read_excel_cell(file.read(), sheet_name='Sheet2', cell='BE37')
    print("cell_value:",value_in_cell)
    if value_in_cell == "mcom_v1.8":
            try:
                df = pd.read_excel(file,sheet_name="Tracker",keep_default_na=False,skiprows=1)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            df.columns=[col.strip() for col in df.columns]
            df["Cell ID"] = df["Cell ID"].astype(str)
        
            allowed_values = {

                'CIRCLE': ['AP', 'BIH', 'CHN', 'ROTN', 'DEL', 'HRY', 'JK', 'JRK', 'KOL', 'MAH', 'MP', 'MUM', 'ORI', 'PUN', 'RAJ', 'UPE', 'UPW', 'WB', 'KK','MAH', 'HP', 'NESA', 'ASM'],
                 'OEM': ['SAMSUNG', 'NOKIA', 'ERICSSON','HUAWEI','ZTE'],
                'Activity Name': ['ULS_HPSC', 'RELOCATION', 'MACRO', 'DE-GROW', 'RET', 'IBS', 'ODSC', 'IDSC', 'HT INCREMENT', 'FEMTO', 'OTHERS', 'UPGRADE','RECTIFICATION','5G SECTOR ADDITION','OPERATIONS','5G RELOCATION','TRAFFIC SHIFTING', 'RRU UPGRADE', '5G RRU SWAP', '5G BW UPGRADE'],
                'Activity Mode (SA/NSA)':['SA','NSA'],
                'Technology (SIWA)': ['2G','FDD','TDD','5G'],
                'Activity Type (SIWA)': ["FDD_SEC_ADDITION", "FDD_TWIN_BEAM", "FDD_UPGRADE", "L2100_UPGRADE", "L900_UPGRADE", "NEW_TOWER", "NEW_TOWER_ULS", "TDD_SEC_ADDITION", "TDD_TWIN_BEAM", "TDD_UPGRADE", "UPGRADE_SW_ONLY", "UPGRADE_ULS", "5G_SEC_ADDITION", "5G_UPGRADE","CPRI ADDITION","SFP CHANGE", "BW UPGRADATION", "BTS SWAP", "IP MODIFICATION", "HOT SWAP", "NOMENCLATURE CHANGE", "2G DELETION", "CARRIER ADDITION"],
                'Band (SIWA)':['G900', 'G1800', 'L850', 'L900', 'L1800', 'L2100', 'L2300', '3500'],
                'Old Site Tech':['G900', 'G1800', 'L850', 'L900', 'L1800', 'L2100', 'L2300', '3500'],
                'Allocated Tech':['G900', 'G1800', 'L850', 'L900', 'L1800', 'L2100', 'L2300', '3500'],
                'Deployed Tech':['G900', 'G1800', 'L850', 'L900', 'L1800', 'L2100', 'L2300', '3500'],
                'NO OF BBU': [str(num) for num in range(0, 20001)] + [''],
                'Cell ID' : [str(num) for num in range(0, 20001)] + ['']
            }

            # Define columns where only emptiness needs to be checked
            # empty_check_columns = ['Integration Date','Site ID','Technology (SIWA)']

            invalid_rows=[]
            def check_multiple_values(value, allowed_list,symbol):
                # print('value:',value)
                if symbol==',':
                    values = [v.strip() for v in value.split(',')]
                    return all(v in allowed_list for v in values)
                # if symbol == '_':
                #     values = [v.strip() for v in value.split('_')]
                #     return all(v in allowed_list for v in values)



            for index, row in df.iterrows():
                if row['Activity Name'].upper() == 'RELOCATION':
                    empty_check_columns = ['Integration Date','Site ID','Technology (SIWA)','Old Site ID','Old Site Tech','Allocated Tech','Deployed Tech','NO OF BBU']
                   
                else:
                    empty_check_columns =  ['Integration Date','Site ID','Technology (SIWA)']
                invalid_cols = []
                for col in allowed_values:
                    if col not in df.columns or pd.isnull(row[col]):
                        invalid_cols.append(col)
                    else:
                        if col in ['Technology (SIWA)','Cell ID','Band (SIWA)','Activity Type (SIWA)','Old Site Tech','Allocated Tech','Deployed Tech']:
                            if ',' in str(row[col]):  # Check for multiple values
                                if not check_multiple_values(str(row[col]).upper(), allowed_values[col],','):
                                    invalid_cols.append(col)    

                            # elif '_' in str(row[col]):  # Check for multiple values
                            #     if not check_multiple_values(str(row[col]).upper(), allowed_values[col],'_'):
                            #         invalid_cols.append(col)               
                        else:
                            if str(row[col]).upper() not in allowed_values[col]:
                                invalid_cols.append(col)

                empty_cols= [col for col in empty_check_columns
                                if col not in df.columns 
                                or pd.isnull(row[col]) 
                                or str(row[col]).strip() == '' 
                                ]
                # print("cell ID:",row['Cell ID'],type(row['Cell ID']))
                invalid_fields= invalid_cols + empty_cols
                unique_combination=f"Integration Date: {row['Integration Date']}, Activity Name: {str(row['Activity Name']).upper()}, Site ID: {row['Site ID']}, Technology (SIWA):{row['Technology (SIWA)']}, CIRCLE: {str(row['CIRCLE']).upper()}, Cell ID: {row['Cell ID']},NO OF BBU: {row['NO OF BBU']}"
                
                if invalid_fields:
                    # Store the employee code and column names for invalid fields
                    invalid_row = {'unique_key': unique_combination, 'invalid_fields': invalid_fields, 'remarks':'These columns are mandatory OR value out of specified options'}
                    invalid_rows.append(invalid_row)
                    continue
                unique_key = str(row['Integration Date']) + str(row['Activity Name']).upper() + str(row['Site ID']) + str(row['Technology (SIWA)']) + str(row['CIRCLE']).upper() + str(row['Cell ID']) + str(row['LNBTS ID']) + str(row['OEM']).upper()+ str(row['NO OF BBU'])
                obj,created = IntegrationData.objects.update_or_create(
                    Integration_Date=row['Integration Date'],
                    Activity_Name=str(row['Activity Name']).upper(),
                    Site_ID=row['Site ID'],
                    Technology_SIWA=row['Technology (SIWA)'],
                    CIRCLE= str(row['CIRCLE']).upper(),
                    Cell_ID= row['Cell ID'],
                    LNBTS_ID= row['LNBTS ID'],
                    OEM = str(row['OEM']).upper(),
                    NO_OF_BBU = row['NO OF BBU'],
                    defaults={       
                        'unique_key': unique_key,                   
                        'MO_NAME': str(row['MO NAME']).upper(),                           
                        'OSS_Details': row['OSS Details'],
                        'CELL_COUNT': row['CELL COUNT'],
                        'TRX_Count': row['TRX Count'],
                        'PRE_ALARM': row['PRE-ALARM'],
                        'GPS_IP_CLK': row['GPS/IP CLK'],
                        'RET': row['RET'],
                        'POST_VSWR': row['POST-VSWR'],
                        'POST_Alarms': row['POST Alarms'],
                        'CELL_STATUS': row['CELL STATUS'],
                        'CTR_STATUS': row['CTR STATUS'],
                        'Integration_Remark': row['Integration Remark'],
                        'T2T4R': row['2T2R/4T4R'],
                        'BBU_TYPE': row['BBU TYPE'],
                        'BB_CARD': row['BB CARD'],
                        'RRU_Type': row['RRU Type'],
                        'Media_Status': row['Media Status'],
                        'Mplane_IP': row['Mplane IP'],
                        'SCF_PREPARED_BY': row['SCF PREPARED BY'],
                        'SITE_INTEGRATE_BY': row['SITE INTEGRATE BY(Integrator Name)'],
                        'Site_Status': row['Site Status'],
                        'External_Alarm_Confirmation': row['External Alarm Confirmation'],
                        'SOFT_AT_STATUS': row['SOFT AT STATUS'],
                        'LICENCE_Status': row['LICENCE Status'],
                        'ESN_NO': row['ESN NO'],
                        'Responsibility_for_alarm_clearance': row['Responsibility for alarm clearance'],
                        'TAC': row['TAC'],
                        'PCI_TDD_20': row['PCI- TDD 20'],
                        'PCI_TDD_10_20': row['PCI TDD 10/20'],
                        'PCI_FDD_2100': row['PCI FDD 2100'],
                        'PCI_FDD_1800': row['PCI FDD 1800'],
                        'PCI_L900': row['PCI L900'],
                        'PCI_5G': row['5G PCI'],
                        'RSI_TDD_20': row['RSI- TDD 20'],
                        'RSI_TDD_10_20': row['RSI TDD 10/20'],
                        'RSI_FDD_2100': row['RSI FDD 2100'],
                        'RSI_FDD_1800': row['RSI FDD 1800'],
                        'RSI_L900': row['RSI L900'],
                        'RSI_5G': row['5G RSI'],
                        'GPL': row['GPL'],
                        'Pre_Post_Check': row['Pre/Post Check'],
                        'Activity_Type_SIWA':row['Activity Type (SIWA)'],
                        'Activity_Mode':row['Activity Mode (SA/NSA)'],
                        'Band_SIWA':row['Band (SIWA)'],
                        'BSC_NAME':row['BSC NAME'],
                        'BCF':row['BCF'],
                        'CRQ':row['CRQ'],
                        'Customer_Approval':row['Customer Approval'],

                        'Old_Site_ID':row['Old Site ID'],
                        'Old_Site_Tech':row['Old Site Tech'],
                        'Allocated_Tech':row['Allocated Tech'],
                        'Deployed_Tech':row['Deployed Tech'],

                        'uploaded_by':request.user.username
                    }
                )
               
                if created and str(row['Activity Name']).upper() in ['UPGRADE', 'RELOCATION', 'ULS_HPSC', 'MACRO', '5G SECTOR ADDITION']:
                    integration_date=row['Integration Date'].date()
                    print('integration date:',integration_date)
                    date_list=generate_date_list(integration_date)
                    for date in date_list:
                        Soft_At_Table.objects.create(
                            unique_key=str(unique_key) +"__" + str(date),
                            combination=unique_key,
                            upload_date=date,
                            IntegrationData=obj,
                            soft_at_status="NOT OFFERED",
                            status_updated_by='integration_Tool',
                            # integration data
                            Integration_Date=row['Integration Date'],
                            Activity_Name=str(row['Activity Name']).upper(),
                            Site_ID=row['Site ID'],
                            Technology_SIWA=row['Technology (SIWA)'],
                            CIRCLE=str(row['CIRCLE']).upper(),
                            Cell_ID=row['Cell ID'],
                            LNBTS_ID=row['LNBTS ID'],
                            OEM=str(row['OEM']).upper(),
                            MO_NAME=str(row['MO NAME']).upper(),
                            OSS_Details=row['OSS Details'],
                            CELL_COUNT=row['CELL COUNT'],
                            TRX_Count=row['TRX Count'],
                            PRE_ALARM=row['PRE-ALARM'],
                            GPS_IP_CLK=row['GPS/IP CLK'],
                            RET=row['RET'],
                            POST_VSWR=row['POST-VSWR'],
                            POST_Alarms=row['POST Alarms'],
                            CELL_STATUS=row['CELL STATUS'],
                            CTR_STATUS=row['CTR STATUS'],
                            Integration_Remark=row['Integration Remark'],
                            T2T4R=row['2T2R/4T4R'],
                            BBU_TYPE=row['BBU TYPE'],
                            BB_CARD=row['BB CARD'],
                            RRU_Type=row['RRU Type'],
                            Media_Status=row['Media Status'],
                            Mplane_IP=row['Mplane IP'],
                            SCF_PREPARED_BY=row['SCF PREPARED BY'],
                            SITE_INTEGRATE_BY=row['SITE INTEGRATE BY(Integrator Name)'],
                            Site_Status=row['Site Status'],
                            External_Alarm_Confirmation=row['External Alarm Confirmation'],
                            SOFT_AT_STATUS=row['SOFT AT STATUS'],
                            LICENCE_Status=row['LICENCE Status'],
                            ESN_NO=row['ESN NO'],
                            Responsibility_for_alarm_clearance=row['Responsibility for alarm clearance'],
                            TAC=row['TAC'],
                            PCI_TDD_20=row['PCI- TDD 20'],
                            PCI_TDD_10_20=row['PCI TDD 10/20'],
                            PCI_FDD_2100=row['PCI FDD 2100'],
                            PCI_FDD_1800=row['PCI FDD 1800'],
                            PCI_L900=row['PCI L900'],
                            PCI_5G=row['5G PCI'],
                            RSI_TDD_20=row['RSI- TDD 20'],
                            RSI_TDD_10_20=row['RSI TDD 10/20'],
                            RSI_FDD_2100=row['RSI FDD 2100'],
                            RSI_FDD_1800=row['RSI FDD 1800'],
                            RSI_L900=row['RSI L900'],
                            RSI_5G=row['5G RSI'],
                            GPL=row['GPL'],
                            Pre_Post_Check=row['Pre/Post Check'],
                            Activity_Type_SIWA=row['Activity Type (SIWA)'],
                            Activity_Mode=row['Activity Mode (SA/NSA)'],
                            Band_SIWA=row['Band (SIWA)'],
                            BSC_NAME=row['BSC NAME'],
                            BCF=row['BCF'],
                        )
                # if created and str(row['Activity Name']).upper() in ['RELOCATION']:
                    
                #             # Create a new Relocation_tracker object
                #                 Relocation_tracker.objects.create(
                #                 circle=str(row['CIRCLE']).upper(),
                #                 old_site_id=row['Old Site ID'],
                #                 new_site_id=row['Site ID'],
                #                 integration_date=row['Integration Date'],
                #                 # ms1_date=row['ms1_date'],
                #                 old_site_technology= row['Old Site Tech'],
                #                 allocated_technology= row['Allocated Tech'],
                #                 deployed_technology= row['Deployed Tech'],
                #                 # deviation=row['deviation'],
                #                 # no_of_deviated_tech=row['no_of_deviated_tech'],
                #                 # old_site_locked_date=row['old_site_locked_date'],
                #                 # new_site_unlock_date=row['new_site_unlock_date'],
                #                 # old_site_traffic=row['old_site_traffic'],
                #                 # existing_traffic=row['existing_traffic'],
                #                 # old_site_admin_status=row['old_site_admin_status'],
                #                 # new_site_admin_status=row['new_site_admin_status'],
                #                 # both_site_unlocked=row['both_site_unlocked'],
                #                 # both_site_locked=row['both_site_locked'],
                #                 # pre_less_than_3_mbps=row['pre_less_than_3_mbps'],
                #                 # current_less_than_3_mbps=row['current_less_than_3_mbps']
                #             )

                #                 print("Relocation Tracker record created succesfully inserted successfully!")
            else:
                    document = Document.objects.create(
                    uploaded_file=file,
                    uploaded_by=request.user,
                    uploaded_by_username=request.user.username
                )
            return Response({'message': 'Data uploaded successfully','error_rows':invalid_rows}, status=status.HTTP_201_CREATED)
    else :
        return Response({'error': 'only tool template can be uploaded, Please also check the template version'}, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['GET'])
# def datewise_integration_data(request):
#     # Get the latest 3 dates
#     latest_dates = IntegrationData.objects.order_by('-Integration_Date').values_list('Integration_Date', flat=True).distinct()[:3]
    
#     # Get the OEM-wise circle-wise count for the latest 3 dates
#     circle_counts = IntegrationData.objects.filter(Integration_Date__in=latest_dates).values('OEM', 'CIRCLE').annotate(count=Count('id'))
    
#     return Response(circle_counts)


@api_view(['GET','POST'])
def datewise_integration_data(request):
    print("User: ", request.user.username)
    date_str = request.POST.get('date')
    # print("date_str:",date_str)    
        # Parse the date string into a datetime object
    if date_str:
            try:
                print("user defined date")
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                date1=date_obj
                date2=date_obj- timedelta(days=1)
                date3=date_obj- timedelta(days=2)
                print(date1,date2,date3)
                year = date_obj.year
            except ValueError:
                return JsonResponse({'error': 'Invalid date format'}, status=400)

    else:
                print("Default Dates")
                latest_date =IntegrationData.objects.latest('Integration_Date').Integration_Date
                print('latest date:',latest_date)
                date1=latest_date
                date2=latest_date- timedelta(days=1)
                date3=latest_date- timedelta(days=2)
                print(date1,date2,date3)

                latest_year = latest_date.year
                print("latest_year:", latest_year)
                year= latest_year



 
    with connection.cursor() as cursor:
        activity_type = [
            '5G SECTOR ADDITION', 
            '5G RELOCATION', 
            'HT INCREMENT', 
            'FEMTO', 
            'DE-GROW', 
            'IBS', 
            'IDSC',
            'MACRO', 
            'ODSC', 
            'OPERATIONS', 
            'RRU UPGRADE', 
            '5G BW UPGRADE', 
            'OTHERS', 
            '5G RRU SWAP',
            'RELOCATION', 
            'RECTIFICATION', 
            'RET', 
            'TRAFFIC SHIFTING', 
            'ULS_HPSC', 
            'UPGRADE'
        ]
        
        activity_columns = [a.replace(' ', '_').replace('-', '_') for a in activity_type]
        dates = [date1, date2, date3]

        join_clauses = []
        alias_list = []

        for index, date in enumerate(dates):
            alias = f"d{index+1}"
            alias_list.append(alias)
            date_tag = f"D{index+1}"
            columns_def = ",".join([f'"{date_tag}_{col}" INTEGER' for col in activity_columns])
            print('date wise data count' , columns_def)
            select_cte = f"""
                SELECT * FROM crosstab($$
                    SELECT 
                        UPPER("CIRCLE") AS "CIRCLE",
                        "Activity_Name",
                        COALESCE(cnt, 0)::INTEGER AS cnt
                    FROM 
                        (SELECT DISTINCT UPPER("CIRCLE") AS "CIRCLE" FROM public."IntegrationTracker_integrationdata") AS "C"
                    CROSS JOIN
                        (SELECT unnest(ARRAY{activity_type}) AS "Activity_Name") AS a
                    LEFT JOIN (
                        SELECT UPPER("CIRCLE") AS "CIRCLE", UPPER("Activity_Name") AS "Activity_Name", COUNT("id") AS cnt
                        FROM public."IntegrationTracker_integrationdata"
                        WHERE "Integration_Date" = '{date}'
                        GROUP BY "CIRCLE", "Activity_Name"
                    ) AS r USING ("CIRCLE", "Activity_Name")
                    ORDER BY 1, 2
                $$) AS ct(cir text, {columns_def})
            """
            join_clauses.append(f"({select_cte}) AS {alias}")

        # Build the full outer joins dynamically
        final_query = join_clauses[0]
        for i in range(1, len(join_clauses)):
            final_query = f"""
                {final_query}
                FULL OUTER JOIN
                {join_clauses[i]}
                USING (cir)
            """

        query = f"SELECT * FROM {final_query};"
        cursor.execute(query)
        results = cursor.fetchall()
        # print(results)
        
    results_as_strings = []
    for row in results:
        # Convert each element in the row to a string
        row_as_string = [str(element) for element in row]
        # Append the row as a string to the list
        results_as_strings.append(row_as_string)
    

    rows_as_dict = [dict(zip([column[0] for column in cursor.description], row)) for row in results_as_strings]


    jsonResult =  json.dumps(rows_as_dict)
    # jsonResult = json.loads(jsonResult)
    ############################ DATE WISE OVER ALL DATA FOR DOWNLOAD ##############################
    objs = IntegrationData.objects.filter(Integration_Date=date1)
    
    # Serialize queryset using serializer
    serializer = IntegrationDataSerializer(objs, many=True)
    # print(jsonResult)
    data={"table_data":jsonResult,"latest_dates":[date1,date2,date3],"download_data":serializer.data}
    return Response(data)







@api_view(["POST"])
def hyperlink_datewise_integration_data(request):
    print("User: ", request.user.username)
    date=request.POST.get("date")
    circle=request.POST.get("circle")
    activity_name=request.POST.get("Activity_Name")
     # Filter IntegrationData objects based on provided parameters
    objs = IntegrationData.objects.filter(Integration_Date=date, CIRCLE=circle, Activity_Name=activity_name)
    
    # Serialize queryset using serializer
    serializer = IntegrationDataSerializer(objs, many=True)
    
    # Return serialized data in Response
    return Response({"data":serializer.data})
    
# -------------------------- DATE RANGE WISE INTEGRATION DATA --------------------------
from datetime import datetime, timedelta

def get_dates():
    # Get the current date
    today = datetime.today()
    
    # Get the 25th of the current month
    # current_month_25 = today.replace(day=25).date()
    current_month_25 = datetime.now().date()
    
    # Calculate the first day of the current month
    first_day_of_current_month = today.replace(day=1)
    
    # Calculate the last day of the previous month
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    
    # Get the 26th of the previous month
    previous_month_26 = last_day_of_previous_month.replace(day=26).date()
    # previous_month_26 = datetime.now().date()
    
    return previous_month_26, current_month_25

import asyncio

@api_view(["POST"])
def date_range_wise_integration_data(request):
    print("User:", request.user.username)

    from_date = request.data.get("from_date")
    to_date = request.data.get("to_date")

    try:
        if from_date and to_date:
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        else:
            from_date, to_date = get_dates()
    except ValueError:
        raise ValidationError("Dates must be in YYYY-MM-DD format.")

    # Ensure unique, cleaned activity types
    raw_activities = [
        '5G SECTOR ADDITION', 
        '5G RELOCATION', 
        'HT INCREMENT', 
        'FEMTO', 
        'DE-GROW', 
        'IBS', 
        'IDSC',
        'MACRO', 
        'ODSC', 
        'OPERATIONS', 
        'RRU UPGRADE', 
        '5G BW UPGRADE', 
        'OTHERS', 
        '5G RRU SWAP',
        'RELOCATION', 
        'RECTIFICATION', 
        'RET', 
        'TRAFFIC SHIFTING', 
        'ULS_HPSC', 
        'UPGRADE',
        '5G AIR SWAP'
        'UPGRADE'
    ]
    activity_type = sorted(set(raw_activities))  # Remove duplicates just in case

    # Create SQL-safe column aliases
    def sql_safe(name):
        return f"D1_{name.upper().replace(' ', '').replace('-', '')}"

    activity_columns = [f'"{sql_safe(a)}" INTEGER' for a in activity_type]

    print('activity columnsa data ' , {', '.join(activity_columns)})

    # Ensure unique, cleaned activity types
    raw_activities = [
        '5G SECTOR ADDITION', 
        '5G RELOCATION', 
        'HT INCREMENT', 
        'FEMTO', 
        'DE-GROW', 
        'IBS', 
        'IDSC',
        'MACRO', 
        'ODSC', 
        'OPERATIONS', 
        'RRU UPGRADE', 
        '5G BW UPGRADE', 
        'OTHERS', 
        '5G RRU SWAP',
        'RELOCATION', 
        'RECTIFICATION', 
        'RET', 
        'TRAFFIC SHIFTING', 
        'ULS_HPSC', 
        'UPGRADE',
        '5G AIR SWAP'
    ]
    activity_type = sorted(set(raw_activities))  # Remove duplicates just in case

    # Create SQL-safe column aliases
    def sql_safe(name):
        return f"D1_{name.upper().replace(' ', '').replace('-', '')}"

    activity_columns = [f'"{sql_safe(a)}" INTEGER' for a in activity_type]

    print('activity columnsa data ' , {', '.join(activity_columns)})

    def fetch_crosstab_data(activity_type: list, activity_columns: list) -> tuple:
        with connection.cursor() as cursor:
            # Escape and format activity list for SQL
            activity_array = ','.join([f"'{a}'" for a in activity_type])
            query = f"""
                SELECT * FROM crosstab($$
                    SELECT 
                        "CIRCLE",
                        "Activity_Name",
                        COALESCE("cnt", 0)::INTEGER AS cnt
                    FROM 
                        (SELECT DISTINCT UPPER("CIRCLE") AS "CIRCLE" FROM public."IntegrationTracker_integrationdata") AS c
                    CROSS JOIN
                        (SELECT unnest(ARRAY[
                                    '5G BW UPGRADE',
                                    '5G RELOCATION',
                                    '5G RRU SWAP',
                                    '5G SECTOR ADDITION',
                                    'DE-GROW',
                                    'FEMTO',
                                    'HT INCREMENT',
                                    'IBS',
                                    'IDSC',
                                    'MACRO',
                                    'ODSC',
                                    'OPERATIONS',
                                    'OTHERS',
                                    'RECTIFICATION',
                                    'RELOCATION',
                                    'RET',
                                    'RRU UPGRADE',
                                    'TRAFFIC SHIFTING',
                                    'ULS_HPSC',
                                    'UPGRADE'
        ]) AS "Activity_Name") AS a
                    LEFT JOIN (
                        SELECT UPPER("CIRCLE") AS "CIRCLE", UPPER("Activity_Name") AS "Activity_Name", COUNT(id) AS cnt
                        FROM public."IntegrationTracker_integrationdata"
                        WHERE "Integration_Date" BETWEEN '{from_date}' AND '{to_date}'
                        GROUP BY "CIRCLE", "Activity_Name"
                    ) r USING ("CIRCLE", "Activity_Name")
                    ORDER BY 1, 2
                $$) AS ct (
                    "cir" TEXT, "D1_5G_BW_UPGRADE" INTEGER,
                "D1_5G_RELOCATION" INTEGER,
                "D1_5G_RRU_SWAP" INTEGER,
                "D1_5G_SECTOR_ADDITION" INTEGER,
                "D1_DE_GROW" INTEGER,
                "D1_FEMTO" INTEGER,
                "D1_HT_INCREMENT" INTEGER,
                "D1_IBS" INTEGER,
                "D1_IDSC" INTEGER,
                "D1_MACRO" INTEGER,
                "D1_ODSC" INTEGER,
                "D1_OPERATIONS" INTEGER,
                "D1_OTHERS" INTEGER,
                "D1_RECTIFICATION" INTEGER,
                "D1_RELOCATION" INTEGER,
                "D1_RET" INTEGER,
                "D1_RRU_UPGRADE" INTEGER,
                "D1_TRAFFIC_SHIFTING" INTEGER,
                "D1_ULS_HPSC" INTEGER,
                "D1_UPGRADE" INTEGER
                )
            """
            cursor.execute(query)
            results = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return results, columns

    async def get_data_async():
        results, columns = await sync_to_async(fetch_crosstab_data)(activity_type, activity_columns)
        rows_as_dict = [dict(zip(columns, row)) for row in results]
        jsonResult = json.dumps(rows_as_dict)

        objs = await sync_to_async(
            lambda: list(IntegrationData.objects.filter(Integration_Date__range=(from_date, to_date)))
        )()
        
        serializer = IntegrationDataSerializer(objs, many=True)

        return {
            "table_data": jsonResult,
            "date_range": [from_date.isoformat(), to_date.isoformat()],
            "download_data": serializer.data
        }

    data = asyncio.run(get_data_async())
    return Response(data)



@api_view(["POST"])
def hyperlink_date_range_integration_data(request):
    print("User: ", request.user.username)
    from_date=request.POST.get("from_date")
    to_date=request.POST.get("to_date")

    circle=request.POST.get("circle")
    activity_name=request.POST.get("Activity_Name")
     # Filter IntegrationData objects based on provided parameters
    objs = IntegrationData.objects.filter(Integration_Date__range=[from_date, to_date], CIRCLE=circle, Activity_Name=activity_name)
    
    # Serialize queryset using serializer
    serializer = IntegrationDataSerializer(objs, many=True)
    
    # Return serialized data in Response
    return Response({"data":serializer.data})
# -----------------------------*********************************************************-----------------------------



from dateutil.relativedelta import relativedelta
def calculate_previous_months(given_month,given_year):
    print("Month1:", given_month)
    print("Year1:", given_year)
    given_date = datetime(given_year, given_month, 1)

    # Calculate previous month
    month2_date = given_date - relativedelta(months=1)
    month3_date = given_date - relativedelta(months=2)
    month4_date = given_date - relativedelta(months=3)
    month5_date = given_date - relativedelta(months=4)
    month6_date = given_date - relativedelta(months=5)

    # Extract the month and year from the previous month date
    month2 =month2_date.month
    year2 = month2_date.year

    month3 =month3_date.month
    year3 = month3_date.year

    month4 =month4_date.month
    year4 = month4_date.year

    month5 =month5_date.month
    year5 = month5_date.year

    month6 =month6_date.month
    year6 = month6_date.year

    print("Previous Month2:", month2)
    print("Previous Year2:", year2)

    print("Previous Month3:", month3)
    print("Previous Year3:", year3)

    return {"Month2":month2,"Month3":month3,"Year2":year2,"Year3":year3,"Month4":month4,"Year4":year4,"Month5":month5,"Year5":year5,"Month6":month6,"Year6":year6}

@api_view(['GET', 'POST'])
def monthwise_integration_data(request):
    print("User: ", request.user.username)
    month = request.POST.get("month")
    year = request.POST.get("year")

    if month and year:
        print("User-defined month/year")
        base_month = int(month)
        base_year = int(year)
    else:
        print("Using default latest month/year")
        latest_date = IntegrationData.objects.latest('Integration_Date').Integration_Date
        base_month = latest_date.month
        base_year = latest_date.year

    date_dict = calculate_previous_months(base_month, base_year)

    ################################################################################ Prepare list of (month, year, index) tuples ########################################################################
    month_year_list = [(base_month, base_year, 1)]
    for i in range(2, 7):
        month_year_list.append((date_dict[f"Month{i}"], date_dict[f"Year{i}"], i))

        activity_list = [
            '5G BW UPGRADE',
            '5G RELOCATION',
            '5G RRU SWAP',
            '5G SECTOR ADDITION',
            'DE-GROW',
            'FEMTO',
            'HT INCREMENT',
            'IBS',
            'IDSC',
            'MACRO',
            'ODSC',
            'OPERATIONS',
            'OTHERS',
            'RECTIFICATION',
            'RELOCATION',
            'RET',
            'RRU UPGRADE',
            'TRAFFIC SHIFTING',
            'ULS_HPSC',
            'UPGRADE'
        ]

    def build_crosstab(month, year, index):
        label = f"M{index}"
        columns = ",".join([f'"{label}_{a.replace(" ", "_").replace("-", "_")}" INTEGER' for a in activity_list])
        array_activities = ",".join([f"'{a}'" for a in activity_list])


        return f"""
            (
                SELECT * FROM crosstab($$
                    SELECT 
                        UPPER("CIRCLE") AS "CIRCLE",
                        "Activity_Name",
                        COALESCE(cnt, 0)::INTEGER AS cnt
                    FROM 
                        (SELECT DISTINCT UPPER("CIRCLE") AS "CIRCLE" FROM public."IntegrationTracker_integrationdata") AS "C"
                    CROSS JOIN
                        (SELECT unnest(ARRAY[{array_activities}]) AS "Activity_Name") AS a
                    LEFT JOIN (
                        SELECT UPPER("CIRCLE") AS "CIRCLE", UPPER("Activity_Name") AS "Activity_Name", COUNT("id") AS cnt
                        FROM public."IntegrationTracker_integrationdata"
                        WHERE EXTRACT(MONTH FROM "Integration_Date") = {month}
                          AND EXTRACT(YEAR FROM "Integration_Date") = {year}
                        GROUP BY "CIRCLE", "Activity_Name"
                    ) AS r USING ("CIRCLE", "Activity_Name")
                    ORDER BY 1, 2
                $$) AS ct(cir TEXT, {columns})
            ) AS d{index}
        """

    ######################################################################### ✅ Build the complete SQL query with full joins ##########################################################################
    join_parts = []
    for i, (month, year, index) in enumerate(month_year_list):
        part = build_crosstab(month, year, index)
        if i == 0:
            join_parts.append(part)
        else:
            join_parts.append(f"FULL OUTER JOIN {part} USING (cir)")

    final_query = " ".join(join_parts)
    full_sql = f"SELECT * FROM {final_query};"

    ########################################################################################### ✅ Execute the query ##################################################################################
    with connection.cursor() as cursor:
        cursor.execute(full_sql)
        results = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

    results_as_dicts = [dict(zip(columns, row)) for row in results]
    jsonResult = json.dumps(results_as_dicts)

    ############################################################################################# Get first (latest) month/year for filtering data ######################################################
    latest_month, latest_year, _ = month_year_list[0]
    ################################################################################################ Fetch data for download #############################################################################
    objs = IntegrationData.objects.filter(
        Integration_Date__year=latest_year,
        Integration_Date__month=latest_month
    )
    serializer = IntegrationDataSerializer(objs, many=True)
    print(month_year_list)
    ############################################################################################################ Return all collected data #################################################################
    data={"table_data":jsonResult,"latest_months":[month for month,_,_ in month_year_list],"latest_year":[year for _,year,_ in month_year_list],"download_data":serializer.data}
    return Response(data)


@api_view(["POST"])
def hyperlink_monthwise_integration_data(request):
    print("User: ", request.user.username)
    month=request.POST.get("month")
    year=request.POST.get("year")
    circle=request.POST.get("circle")
    activity_name=request.POST.get("Activity_Name")
     # Filter IntegrationData objects based on provided parameters
    objs = IntegrationData.objects.filter(Integration_Date__year=year,Integration_Date__month=month, CIRCLE=circle, Activity_Name=activity_name)
    
    # Serialize queryset using serializer
    serializer = IntegrationDataSerializer(objs, many=True)
    
    # Return serialized data in Response
    return Response(serializer.data)




@api_view(['POST'])
def monthly_oemwise_integration_data(request):
    print("User: ", request.user.username) 
    month=request.POST.get("month")
    year=request.POST.get("year")
    if month and year:
        print("user defined......")
        month=int(month)
        year=int(year)

    else:
        print("default months......")
        latest_month = IntegrationData.objects.latest('Integration_Date').Integration_Date.month
        latest_year = IntegrationData.objects.latest('Integration_Date').Integration_Date.year
         
        month=latest_month
        year=latest_year
        

    with connection.cursor() as cursor:

        query = f""" 
        
        select * from crosstab($$
	    SELECT  "CIRCLE","OEM",COALESCE("cnt", 0)::INTEGER as cnt -- Replace 0 with appropriate default value
     FROM 
        (SELECT DISTINCT UPPER("CIRCLE") as "CIRCLE" FROM public."IntegrationTracker_integrationdata") AS "CIRCLE"
     CROSS JOIN
           (
            SELECT unnest(ARRAY['SAMSUNG', 'NOKIA', 'ERICSSON','HUAWEI','ZTE']) AS "OEM"
        ) AS activities
     LEFT JOIN
        (select "CIRCLE","OEM", count("id") as cnt from 
 						(select "id", "CIRCLE", UPPER("OEM") as "OEM" 
						 from public."IntegrationTracker_integrationdata" WHERE EXTRACT(MONTH FROM "Integration_Date") = {month} and EXTRACT(YEAR FROM "Integration_Date") = {year}) in_0
    group by "CIRCLE","OEM") as first_t
        USING ("CIRCLE", "OEM") order by 1,2 $$) as 	 
    ct(cir text, "ERICSSON" INTEGER,"HUAWEI" INTEGER,"NOKIA" INTEGER,"SAMSUNG" INTEGER, "ZTE" INTEGER)
         """
        cursor.execute(query)
        results = cursor.fetchall()
        # print(results)        
    results_as_strings = []
    for row in results:
        # Convert each element in the row to a string
        row_as_string = [str(element) for element in row]
        # Append the row as a string to the list
        results_as_strings.append(row_as_string)
    
    rows_as_dict = [dict(zip([column[0] for column in cursor.description], row)) for row in results_as_strings]

    jsonResult =  json.dumps(rows_as_dict)

    # print(jsonResult)
    data={"table_data":jsonResult,'month':month,'year':year}
    return Response(data)
        



@api_view(['POST'])
def hyperlink_monthly_oemwise_integration_data(request):
    print("User: ", request.user.username)
    month=request.POST.get("month")
    year=request.POST.get("year")
    circle=request.POST.get("circle")
    oem=request.POST.get("oem")
    with connection.cursor() as cursor:

        query = f"""
        select  * from (select * from crosstab($$ SELECT 
        "CIRCLE",
        "Activity_Name",
        COALESCE("cnt", 0)::INTEGER as cnt -- Replace 0 with appropriate default value
     FROM 
                (
            SELECT unnest(ARRAY['{circle}']) AS "CIRCLE"
        ) AS CIRCLES
     CROSS JOIN
       (SELECT unnest(ARRAY['5G BW UPGRADE',
                                    '5G RELOCATION',
                                    '5G RRU SWAP',
                                    '5G SECTOR ADDITION',
                                    'DE-GROW',
                                    'FEMTO',
                                    'HT INCREMENT',
                                    'IBS',
                                    'IDSC',
                                    'MACRO',
                                    'ODSC',
                                    'OPERATIONS',
                                    'OTHERS',
                                    'RECTIFICATION',
                                    'RELOCATION',
                                    'RET',
                                    'RRU UPGRADE',
                                    'TRAFFIC SHIFTING',
                                    'ULS_HPSC',
                                    'UPGRADE',
                                    '5G AIR SWAP']) AS "Activity_Name") AS "Activity_Name"
     LEFT JOIN
        (select "CIRCLE","Activity_Name", count("id") as cnt from 
 						(select "id", "CIRCLE", UPPER("Activity_Name") as "Activity_Name" from public."IntegrationTracker_integrationdata" WHERE EXTRACT(MONTH FROM "Integration_Date") = {month} and EXTRACT(YEAR FROM "Integration_Date") = {year} and "OEM"='{oem}' and "CIRCLE"='{circle}') in_0
 group by "CIRCLE","Activity_Name") as r
     USING ("CIRCLE", "Activity_Name") order by 1,2 $$) as 
ct(cir text, "5G RELOCATION" INTEGER,"5G RRU SWAP" INTEGER,"5G SECTOR ADDITION" INTEGER,"DE-GROW" INTEGER,"FEMTO" INTEGER,"HT INCREMENT" INTEGER,"IBS" INTEGER,"IDSC" INTEGER,"MACRO" INTEGER, "ODSC" INTEGER,"OPERATIONS" INTEGER,"RECTIFICATION" INTEGER,"OTHERS" INTEGER,"RECTIFICATION" INTEGER,"RELOCATION" INTEGER,"RET" INTEGER,"RRU UPGRADE" INTEGER,"TRAFFIC SHIFTING" INTEGER,"ULS_HPSC" INTEGER,"UPGRADE" INTEGER,"5G AIR SWAP" INTEGER)) as m1

        
        
         """
        cursor.execute(query)
        results = cursor.fetchall()
        # print(results)        
    results_as_strings = []
    for row in results:
        # Convert each element in the row to a string
        row_as_string = [str(element) for element in row]
        # Append the row as a string to the list
        results_as_strings.append(row_as_string)
    
    rows_as_dict = [dict(zip([column[0] for column in cursor.description], row)) for row in results_as_strings]

    jsonResult =  json.dumps(rows_as_dict)

    # print(jsonResult)
    data={"table_data":jsonResult}
    return Response(data)
    

@api_view(["POST"])
def hyperlink_hyperlink_monthly_oemwise_integration_data(request):
    print("User: ", request.user.username) 
    oem=request.POST.get("oem")
    month=request.POST.get("month")
    year=request.POST.get("year")
    circle=request.POST.get("circle")
    activity_name=request.POST.get("Activity_Name")
     # Filter IntegrationData objects based on provided parameters
    objs = IntegrationData.objects.filter(Integration_Date__year=year,Integration_Date__month=month, CIRCLE=circle, Activity_Name=activity_name,OEM=oem)
    
    # Serialize queryset using serializer
    serializer = IntegrationDataSerializer(objs, many=True)
    
    # Return serialized data in Response
    return Response(serializer.data)




@api_view(['GET'])
def overall_record_summary(request):
    print("User: ", request.user.username)
  
    with connection.cursor() as cursor:

        query = f"""
                SELECT 
            "OEM",
            MIN("Integration_Date") AS from_integration_date,
            MAX("Integration_Date") AS to_integration_date,
            COUNT(*) AS record_count
        FROM 
            PUBLIC."IntegrationTracker_integrationdata"
        GROUP BY 
            "OEM";

         """
        cursor.execute(query)
        results = cursor.fetchall()
        # print(results)        
    results_as_strings = []
    for row in results:
        # Convert each element in the row to a string
        row_as_string = [str(element) for element in row]
        # Append the row as a string to the list
        results_as_strings.append(row_as_string)
    
    rows_as_dict = [dict(zip([column[0] for column in cursor.description], row)) for row in results_as_strings]

    jsonResult =  json.dumps(rows_as_dict)

    # print(jsonResult)
    data={"table_data":jsonResult}
    return Response(data)

@api_view(["Delete"])
def delete_integration_record(request, pk):
    print("User: ", request.user.username)
    user=request.user.username
    print("pk: ", pk)
    nokia_spocks=['chandan.kumar@mcpsinc.com']
    zte_spocks=['aashish.s@mcpsinc.com']
    huawei_spocks=['rahul.dahiya@mcpsinc.com']
    samsung_spocks=['rahul.dahiya@mcpsinc.com']
    ericsson_spocks=['aashish.s@mcpsinc.com']
    print("here")
    try:
        obj = IntegrationData.objects.get(pk=pk)
    except IntegrationData.DoesNotExist:
        return Response({"status":True,'message': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)
    print(obj)

    if obj.OEM == "NOKIA" and user in nokia_spocks:
        obj.delete()
        print("deleted")
        return Response({"status":True,'message': 'Record deleted successfully'}, status=status.HTTP_200_OK)
    elif obj.OEM == "ZTE" and user in zte_spocks:
        obj.delete()
        print("deleted")
        return Response({"status":True,'message': 'Record deleted successfully'}, status=status.HTTP_200_OK)
    elif obj.OEM == "HUAWEI" and user in huawei_spocks:
        obj.delete()
        print("deleted")
        return Response({"status":True,'message': 'Record deleted successfully'}, status=status.HTTP_200_OK)
    elif obj.OEM == "SAMSUNG" and user in samsung_spocks:
        obj.delete()
        print("deleted")
        return Response({"status":True,'message': 'Record deleted successfully'}, status=status.HTTP_200_OK)
    elif obj.OEM == "ERICSSON" and user in ericsson_spocks:
        obj.delete()
        print("deleted")
        return Response({"status":True,'message': 'Record deleted successfully'}, status=status.HTTP_200_OK)
    else:
        print("exception..")
        return Response({'status':False,'message': 'You are not authorized to delete this record'}, status=status.HTTP_403_FORBIDDEN)

        
@api_view(['PUT'])
def integration_table_update(request, id=None):
    user = request.user.username
    print("username: ", user)
    nokia_spocks=['chandan.kumar@mcpsinc.com','nishant.verma@mcpsinc.in','girraj.singh@mcpsinc.in','mohit.batra@mcpsinc.com','abhishek.gupta']
    zte_spocks=['aashish.s@mcpsinc.com','mohit.batra@mcpsinc.com','abhishek.gupta']
    huawei_spocks=['rahul.dahiya@mcpsinc.com','mohit.batra@mcpsinc.com','harish.singh@ust.com','abhishek.gupta']
    samsung_spocks=['rahul.dahiya@mcpsinc.com','mohit.batra@mcpsinc.com','harish.singh@ust.com', 'abhishek.gupta']
    ericsson_spocks=['aashish.s@mcpsinc.com','mohit.batra@mcpsinc.com','abhishek.gupta']
  
    if request.method == 'PUT':
        try:
            integration_record = IntegrationData.objects.get(pk=id)
        except IntegrationData.DoesNotExist:
            return Response({'message': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)
    print('OEM: ',integration_record.OEM)
    if integration_record.OEM == "NOKIA" and user in nokia_spocks :
        serializer = IntegrationDataSerializer(integration_record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data,"status":True,'message': 'Record deleted successfully'}, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif integration_record.OEM == "ZTE" and user in zte_spocks:
            serializer = IntegrationDataSerializer(integration_record, data=request.data)
            if serializer.is_valid():
             serializer.save()
             return Response({"data":serializer.data,"status":True,'message': 'Record edited successfully'}, status=status.HTTP_200_OK)
    elif integration_record.OEM == "HUAWEI" and user in huawei_spocks:
            serializer = IntegrationDataSerializer(integration_record, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"status":True,'message': 'Record edited successfully'}, status=status.HTTP_200_OK)
    
    elif integration_record.OEM == "SAMSUNG" and user in samsung_spocks:
           serializer = IntegrationDataSerializer(integration_record, data=request.data)
           if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"status":True,'message': 'Record edited successfully'}, status=status.HTTP_200_OK)
        
    elif integration_record.OEM == "ERICSSON" and user in ericsson_spocks:
           serializer = IntegrationDataSerializer(integration_record, data=request.data)
           if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"status":True,'message': 'Record edited successfully'}, status=status.HTTP_200_OK)   
    else:
        print("exception..")
        return Response({'status':False,'message': 'You are not authorized to edit this record'}, status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
def overall_integration_for_perticular_oem(request):
    print("User: ", request.user.username)
    oem=request.POST.get("oem")
    print(oem)
    objs = IntegrationData.objects.filter(OEM=oem)
    serializer = IntegrationDataSerializer(objs, many=True)
    return Response({"table_data":serializer.data})


from .models import *
from .serializers import *
from rest_framework.views import APIView
from datetime import date



def dev_tech(old_site_tech, new_site_tech):
        old_site_tech=old_site_tech.split(",")
        new_site_tech=new_site_tech.split(",")
        if sorted(old_site_tech) == sorted(new_site_tech):
            return ("No", "")  # No changes
        else:
            common_sites = list(set(old_site_tech) ^ set(new_site_tech))  # Intersection
            common_sites=','.join(common_sites)
            return ("Yes", common_sites) 
def both_site_unlocked(old_site_var_trafic, new_site_var_trafic):
    if old_site_var_trafic > 0 and new_site_var_trafic > 0:
        return True
    else:
        return False
def both_site_locked(old_site_var_trafic, new_site_var_trafic):
    if old_site_var_trafic == 0 and new_site_var_trafic == 0:
        return True
    else:
        return False
def payload_dip(old_site_fixed_traffic,new_site_variable_traffic):
    if old_site_fixed_traffic - new_site_variable_traffic > 100:
        return True
    else:
        return False


from .send_relocation_flag_mail import send_email_for_relocation
class Relocation_trackerViewSet(APIView):    # relocation Dashboard
    # queryset = Relocation_tracker.objects.all()
    serializer_class = Relocation_trackerSerializer
    def get(self, request, *args, **kwargs):
        start_date = date(2025, 2, 2)
        previous_date= datetime.now().date() - timedelta(days=1)
        print("Previous Date: ",previous_date)
        Integration_objs=IntegrationData.objects.filter(Integration_Date__gt=start_date,Activity_Name="RELOCATION")
        # previous_date_ix_df = pd.DataFrame(list(Integration_objs.values()))

        if Integration_objs.exists():
            previous_date_ix_df = pd.DataFrame(list(Integration_objs.values()))
            print(previous_date_ix_df.columns)
        else:
            # Extract column names from the model
            column_names = [field.name for field in IntegrationData._meta.get_fields()]
            previous_date_ix_df = pd.DataFrame(columns=column_names)

        fixed_pre_traffic_objs=fixed_pre_traffic.objects.filter(date=previous_date)
        # fixed_pre_traffic_df=pd.DataFrame(list(fixed_pre_traffic_objs.values()))   

        if fixed_pre_traffic_objs.exists():
            fixed_pre_traffic_df = pd.DataFrame(list(fixed_pre_traffic_objs.values()))
            fixed_pre_traffic_df['traffic'] = fixed_pre_traffic_df['traffic'].apply(lambda x: round(x, 2)).fillna('')
        else:
            # Extract column names from the model
            column_names = [field.name for field in fixed_pre_traffic._meta.get_fields()]
            fixed_pre_traffic_df = pd.DataFrame(columns=column_names) 

        daily_pre_traffic_objs=daily_pre_traffic.objects.filter(date= previous_date)
        # daily_pre_traffic_df=pd.DataFrame(list(daily_pre_traffic_objs.values()))

        if daily_pre_traffic_objs.exists():
            daily_pre_traffic_df = pd.DataFrame(list(daily_pre_traffic_objs.values()))
        else:
            # Extract column names from the model
            column_names = [field.name for field in daily_pre_traffic._meta.get_fields()]
            daily_pre_traffic_df = pd.DataFrame(columns=column_names)

        daily_post_traffic_objs=daily_post_traffic.objects.filter(date=previous_date)
        # daily_post_traffic_df=pd.DataFrame(list(daily_post_traffic_objs.values()))

        if daily_post_traffic_objs.exists():
            daily_post_traffic_df = pd.DataFrame(list(daily_post_traffic_objs.values()))
        else:
            # Extract column names from the model
            column_names = [field.name for field in daily_post_traffic._meta.get_fields()]
            daily_post_traffic_df = pd.DataFrame(columns=column_names)

        print("previous_date_ix_df",previous_date_ix_df)
        print("fixed_pre_traffic_df",fixed_pre_traffic_df)
        print("daily_pre_traffic_df",daily_pre_traffic_df)
        print("daily_post_traffic_df",daily_post_traffic_df)

        merged_df = previous_date_ix_df.merge(fixed_pre_traffic_df, how='left', left_on='Old_Site_ID', right_on='siteID', suffixes=('_ix', '_fixed_pre_traffic')).merge(daily_pre_traffic_df, how='left', left_on='Old_Site_ID', right_on='siteID', suffixes=('_fixed_pre_traffic', '_daily_pre_traffic')).merge(daily_post_traffic_df, how='left', left_on='Site_ID', right_on='siteID', suffixes=('_daily_pre_traffic', '_daily_post_traffic'))
        print(merged_df.columns)
        for i, row in merged_df.iterrows():
            print(row['Site_ID'])
            allocated_vs_deployed_tech=dev_tech(row['Allocated_Tech'], row['Deployed_Tech'])
            allocated_vs_deployed_tech_deviation=allocated_vs_deployed_tech[0]
            allocated_vs_deployed_tech=allocated_vs_deployed_tech[1]
            print("allocated_vs_deployed_tech",allocated_vs_deployed_tech)
            print("allocated_vs_deployed_tech_deviation",allocated_vs_deployed_tech_deviation)

            old_vs_deployed_tech=dev_tech(row['Old_Site_Tech'], row['Deployed_Tech'])
            old_vs_deployed_tech_deviation=old_vs_deployed_tech[0]
            old_vs_deployed_tech=old_vs_deployed_tech[1]
            print("old_vs_deployed_tech",old_vs_deployed_tech)
            print("old_vs_deployed_tech_deviation",old_vs_deployed_tech_deviation)

            if both_site_unlocked(row['traffic'], row['traffic_daily_pre_traffic']):  
                both_site_unlocked_sts="Yes"
            else:
                both_site_unlocked_sts="No"

            if both_site_locked(row['traffic'], row['traffic_daily_pre_traffic']):  
                both_site_locked_sts="Yes"
            else:       
                both_site_locked_sts="No"
            if payload_dip(row['traffic_fixed_pre_traffic'], row['traffic']):
                payload_dip_sts="Yes"
            else:
                payload_dip_sts="No"


            obj,created=Relocation_tracker.objects.update_or_create(
                    ix_unique_key= row['unique_key'],  # Replace with actual unique key value
                    defaults={
                        "circle":row['CIRCLE'] ,
                        "old_site_id": row['Old_Site_ID'],
                        "new_site_id": row['Site_ID'],
                        "mo_name": row['MO_NAME'],
                        "no_of_BBUs": row['NO_OF_BBU'],
                        'OEM': row['OEM'],
                        "old_site_technology": row['Old_Site_Tech' ],
                        "allocated_technology": row['Allocated_Tech'],
                        "deployed_technology": row['Deployed_Tech'],
                        "allocated_vs_deployed_tech_deviation":allocated_vs_deployed_tech_deviation,
                        "old_vs_deployed_tech_deviation": old_vs_deployed_tech_deviation,
                        # "old_site_locked_date": None,  # DateFields should have None
                        # "new_site_unlock_date": None,
                        "old_site_traffic_fixed": row['traffic_fixed_pre_traffic'],
                        "old_site_traffic_variable": row['traffic_daily_pre_traffic'],
                        "existing_traffic": row['traffic'],
                        "old_site_admin_status": "",
                        "new_site_admin_status": "",
                        "both_site_unlocked": both_site_unlocked_sts,
                        "both_site_locked": both_site_locked_sts,
                        "pre_less_than_3_mbps": "",
                        "current_less_than_3_mbps": "",
                        "old_vs_deployed_tech": old_vs_deployed_tech,
                        "allocated_vs_deployed_tech": allocated_vs_deployed_tech,
                        "integration_date": row['Integration_Date'],  # DateFields should have None
                        "ms1_date": None,
                        "payload_dip": payload_dip_sts,
                    }
                )
                            



        # for column in list(merged_df.columns):
        #     print(column)

        objs=Relocation_tracker.objects.all().order_by("-integration_date")
        send_email_for_relocation(objs)
        serializer = Relocation_trackerSerializer(objs, many=True)
        # print(serializer.data)
        return Response(serializer.data)
        # # return Response({})



# import datetime

@api_view(["POST"])
# @parser_classes([MultiPartParser, FormParser])
def upload_relocation_excel(request):
    file = request.FILES.get("relocation_file")
    model_key = request.data.get("model_key")  # Get the key from the request

    if not file:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    if not model_key:
        return JsonResponse({"error": "Model key is required"}, status=400)

    # Map keys to models
    model_mapping = {
        "fixed_pre_traffic": fixed_pre_traffic,
        "daily_pre_traffic": daily_pre_traffic,
        "daily_post_traffic": daily_post_traffic
    }

    selected_model = model_mapping.get(model_key)

    if not selected_model:
        return JsonResponse({"error": "Invalid model key"}, status=400)

    try:
        df = pd.read_excel(file)

        required_columns = {"Date", "Site ID", "Traffic"}
        if not required_columns.issubset(df.columns):
            return JsonResponse({"error": f"Missing required columns: {required_columns - set(df.columns)}"}, status=400)

        for _, row in df.iterrows():
            # date_value = datetime.datetime.strptime(str(row["Date"]), "%Y-%m-%d").date()
            date_value = pd.to_datetime(row["Date"]).date()
            site_id_value = row["Site ID"]
            traffic_value = row["Traffic"]

            selected_model.objects.update_or_create(
                date=date_value,
                siteID=site_id_value,
                defaults={"traffic": traffic_value}
            )

        return JsonResponse({"message": "Data uploaded successfully"}, status=201)

    except Exception as e:
        print(e)
        return JsonResponse({"error": str(e)}, status=500)



class New_site_locked_unlocked_dateView(APIView):
    serializer_class =New_site_locked_unlocked_date_serializer
    def post(self, request):
        serializer = New_site_locked_unlocked_date_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def put(self, request, pk=None):  # Accept pk to identify the record
    #     try:
    #         instance = New_site_locked_unlocked_date.objects.get(pk=pk)  # Fetch the existing instance
    #     except New_site_locked_unlocked_date.DoesNotExist:
    #         return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

    #     serializer = New_site_locked_unlocked_date_serializer(instance, data=request.data, partial=True)  
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class old_site_locked_unlocked_dateView(APIView):
    serializer_class =old_site_locked_unlocked_date_serializer
    def post(self, request):
        serializer = old_site_locked_unlocked_date_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def put(self, request, pk=None):  # Accept pk to identify the record
    #     try:
    #         instance = old_site_locked_unlocked_date.objects.get(pk=pk)  # Fetch the existing instance
    #     except old_site_locked_unlocked_date.DoesNotExist:
    #         return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

    #     serializer = old_site_locked_unlocked_date_serializer(instance, data=request.data, partial=True)  
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def get_old_site_locked_unlocked_date(request):
    relocatio_id = request.data.get("Relocation_id")

    if not relocatio_id:
        return Response({"error": "Relocation_id is required."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        relocation_obj = Relocation_tracker.objects.filter(id=relocatio_id).first()
        if not relocation_obj:
            return Response({"error": "Relocation_id not found in Relocation_tracker."}, status=status.HTTP_404_NOT_FOUND)
        objs = old_site_locked_unlocked_date.objects.filter(Relocation_id=relocatio_id).order_by('-created_at')

        if not objs.exists():
            return Response({
                "message": "No records found for the given Relocation_id.",
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = old_site_locked_unlocked_date_serializer(objs, many=True)
        return Response({
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["POST"])
def get_new_site_locked_unlocked_date(request):
    relocatio_id = request.data.get("Relocation_id")

    if not relocatio_id:
        return Response({"error": "Relocation_id is required."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        relocation_obj = Relocation_tracker.objects.filter(id=relocatio_id).first()
        if not relocation_obj:
            return Response({"error": "Relocation_id not found in Relocation_tracker."}, status=status.HTTP_404_NOT_FOUND)
        objs = New_site_locked_unlocked_date.objects.filter(Relocation_id=relocatio_id).order_by('-created_at')

        if not objs.exists():
            return Response({
                "message": "No records found for the given Relocation_id.",
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = New_site_locked_unlocked_date_serializer(objs, many=True)
        return Response({
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#############################################################################


# @api_view(["POST"])
# def get_new_site_locked_unlocked_date(request):
#     print(request.data)

#     relocation_id = request.data.get("Relocation_id")

#     if not relocation_id:
#         return Response({"error": "Relocation_id is required"}, status=status.HTTP_400_BAD_REQUEST)

#     obj = Relocation_tracker.objects.filter(id=relocation_id).order_by('-created_at').first()

#     if not obj:
#         return Response({"error": "No records found for given Relocation_id"}, status=status.HTTP_404_NOT_FOUND)

#     # Ensure 'no_of_BBUs' is an integer; convert empty string to 0
#     no_of_BBUs_value = obj.No_of_BBUs if obj.no_of_BBUs and str(obj.no_of_BBUs).isdigit() else 0

#     mapped_data = {
#         "circle": obj.circle,
#         "OEM": obj.OEM,
#         "no_of_BBUs": no_of_BBUs_value,  # Now safely handled
#         "Technology": obj.allocated_technology,
#         "relocation_id": obj.id,
#         "site_name": request.data.get("site_name"),  # Extra fields from request
#         "locked_date": request.data.get("locked_date"),
#         "unlocked_date": request.data.get("unlocked_date"),
#     }

#     serializer = New_site_locked_unlocked_date_serializer(data=mapped_data)

#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["POST"])
# def get_new_site_locked_unlocked_date(request):
#     print(request.data)
#     relocation_id=request.data.get("Relocation_id")
#     circle=request.data.get("circle")
#     OEM = request.data.get("OEM")
#     no_of_BBUs= request.data.get("No._of_BBUs")
#     Technology= request.data.get("Technology")
#     objs=New_site_locked_unlocked_date.objects.filter(Relocation_id=relocation_id,circle=circle,OEM=OEM,no_of_BBUs=no_of_BBUs,Technology=Technology).order_by('-created_at')
#     serializer = New_site_locked_unlocked_date_serializer(objs, many=True)
#     print(serializer.data)
#     return Response(serializer.data)


# @api_view(["POST"])
# def get_old_site_locked_unlocked_date(request):
#     print(request.data)
#     relocation_id=request.data.get("Relocation_id")
#     circle=request.data.get("circle")
#     OEM = request.data.get("OEM")
#     no_of_BBUs= request.data.get("no_of_BBUs")
#     Technology= request.data.get("Technology")
#     objs=old_site_locked_unlocked_date.objects.filter(Relocation_id=relocation_id,circle=circle,OEM=OEM,no_of_BBUs=no_of_BBUs,Technology=Technology).order_by('-created_at')
#     serializer = old_site_locked_unlocked_date_serializer(objs, many=True)
#     print(serializer.data)
#     return Response(serializer.data)

class Approval_View(APIView):
    serializer_class = Approval_Serializer
    def get(self, request):
        approvals = Approval.objects.all()
        serializer = Approval_Serializer(approvals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = Approval_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None): 
        try:
            approval = Approval.objects.get(pk=pk)
        except Approval.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Approval_Serializer(approval, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Relocation_Remark
# from .serializers import Relocation_RemarkSerializer

# class RemarkForRelocationView(APIView):
#     serializer_class = Relocation_RemarkSerializer

#     def get(self, request):
#         remarks = Relocation_Remark.objects.all()
#         serializer = Relocation_RemarkSerializer(remarks, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = Relocation_RemarkSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, pk=None): 
#         if not pk:
#             return Response({"error": "ID is required for updating"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             remark = Relocation_Remark.objects.get(pk=pk)
#         except Relocation_Remark.DoesNotExist:
#             return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

#         serializer = Relocation_RemarkSerializer(remark, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Approval List by Circle
# approval_given_by_list = {
#     "AP": ["Sai Teja", "Remesh Thota", "Krishna Khant Verma", "Saurabh Rathore"],
#     "JRK": ["Avnish Mishra", "OM", "Vidya", "Sonu Sharma", "Saurabh Rathore"],
#     "BIH": ["Sonu Singh", "Deepak", "Sonu Sharma", "Saurabh Rathore"],
#     "CH": ["Bharateeshwaran", "Prakashpandi", "Shubham Gupta", "Nilesh Jain", "Saurabh Rathore"],
#     "DL": ["Nishant Sharma", "Rajesh Gupta", "Krishna Kant Verma", "Saurabh Rathore"],
#     "HR": ["Manoj Kumar [ZTE]", "Shivam Pandey [Ericsson]", "Aman", "Tarun Rakecha", "Saurabh Rathore"],
#     "JK": ["Rohit Bansal", "Manik Mahajan", "Krishna Kant Verma", "Saurabh Rathore"],
#     "KK": ["Khadir Valli", "Shubham Gupta", "Saurabh Rathore"],
#     "KOL": ["Masud Rana", "Pankaj", "Sonu Sharma", "Saurabh Rathore"],
#     "MP": ["Shashikant Jaiswal", "Amit Sharma", "Nilesh Jain", "Saurabh Rathore"],
#     "MUM": ["Bharat Kamble", "Sai Raj", "Aman Kashyap", "Nilesh Jain", "Saurabh Rathore"],
#     "OR": ["Manish Chobisa", "Jayadeba", "Sonu Sharma", "Saurabh Rathore"],
#     "PB": ["Manoj Kumar [ZTE]", "Himanshu Lokhande [Samsung]", "Aman", "Tarun Rakecha", "Saurabh Rathore"],
#     "RAJ": ["Rahul Charak", "Hemant Sharma", "Krishna Kant Verma", "Saurabh Rathore"],
#     "ROB": ["Masud Rana", "Pankaj", "Sonu Sharma", "Saurabh Rathore"],
#     "ROTN": ["Bharateeshwaran", "Prakashpandi", "Shubham Gupta", "Nilesh Jain", "Saurabh Rathore"],
#     "UPE": ["Rakesh Dubey", "Onkar Soni", "Manish Singh", "Nilesh Jain", "Saurabh Rathore"],
#     "UPW": ["Rajan Agrawal", "Praval Joshi", "Shubham Gupta", "Saurabh Rathore"]
# }

# @api_view(["POST"])
# def get_new_site_locked_unlocked_date(request):
#     relocation_id = request.data.get("Relocation_id")
#     circle = request.data.get("circle")

#     objs = New_site_locked_unlocked_date.objects.filter(
#         Relocation_id=relocation_id, circle=circle
#     ).order_by('-created_at')

#     serializer = New_site_locked_unlocked_date_serializer(objs, many=True)

#     # Get approval list for the given circle
#     approval_given_by = approval_given_by_list.get(circle, [])

#     return Response({"data": serializer.data, "approval_given_by": approval_given_by})


# @api_view(["POST"])
# def get_old_site_locked_unlocked_date(request):
#     relocation_id = request.data.get("Relocation_id")
#     circle = request.data.get("circle")

#     objs = old_site_locked_unlocked_date.objects.filter(
#         Relocation_id=relocation_id, circle=circle
#     ).order_by('-created_at')

#     serializer = old_site_locked_unlocked_date_serializer(objs, many=True)

#     # Get approval list for the given circle
#     approval_given_by = approval_given_by_list.get(circle, [])

#     return Response({"data": serializer.data, "approval_given_by": approval_given_by})



######################## working process #################################

@api_view(['PUT'])
def Remark_for_relocation(request, id=None):  
    # if request.method == 'POST':
    #     print(request.data)
    #     serializer = Relocation_trackerSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"massage": "Remark added successfully"}, serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        print(request.data)
        if not id:
            return Response({"error": "ID is required for update"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = Relocation_tracker.objects.get(pk=id)
        except Relocation_trackerSerializer.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Relocation_trackerSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Remark updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Relocation_tracker
from .serializers import Relocation_trackerSerializer

@api_view(['POST'])
def master_dashboard(request):
    from_date = request.POST.get('from_date')
    to_date = request.POST.get('to_date')

    try:
        if from_date:
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
        if to_date:
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        
        
        if not from_date and not to_date:
            relocation_data = Relocation_tracker.objects.all()
        else:
            if from_date and not to_date:
                to_date = datetime.now().date()

            date_list = []
            current_date = from_date
            while current_date <= to_date:
                date_list.append(current_date.strftime('%Y-%m-%d'))
                current_date += timedelta(days=1)
            

            relocation_data = Relocation_tracker.objects.filter(integration_date__range=[from_date, to_date])


    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

    serialized_data = Relocation_trackerSerializer(relocation_data, many=True).data

    return Response({
        "dates": date_list if from_date and to_date else "All data retrieved",
        "relocation_data": serialized_data
    }, status=200)