from django.db.models import F, DateField
from django.db.models import IntegerField
from django.db.models.functions import ExtractMonth
from django.shortcuts import render
from django.db.models import F, ExpressionWrapper, fields
from django.db.models.query import QuerySet
from django.db import connection
import re
from django.db.models import Max
from django.db.models import Q

# Create your views here.

from django.shortcuts import render
from rest_framework.decorators import api_view
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncWeek
from django.db.models import Count, Case, When, Value, IntegerField

from django.core.files.storage import FileSystemStorage
from django.db.models import Q, Sum

import pandas as pd
import os
from .models import *
from datetime import datetime, timedelta

# Create your views here.

import json
from .serializers import *

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes

# from commom_utilities.utils import *
from IntegrationTracker.models import IntegrationData
import openpyxl
from .serializers import *
def process_save_to_database(df, upload_date):

    #print("df: ", df.columns)
    for i, d in df.iterrows():
        pk = (
            str(d["CIRCLE"])
            + str(d["SITE_ID"])
            + str(d["BAND"])
            + str(d["UNIQUE ID"])
            + str(upload_date)
            + str(i)
        )

        Date = (
            pd.to_datetime(str(d.get("Date", "")), errors="coerce").strftime("%Y-%m-%d")
            if d.get("Date")
            else None
        )

        project_dict = {"PROJECT": "CIRCLE PROJECT"}
        if "PROJECT" in df.columns:
            project = str(d[project_dict["PROJECT"]])
        else:
            project = str(d["CIRCLE PROJECT"])

        try:
            obj, created = Soft_At_Table.objects.update_or_create(
                id=pk,
                upload_date=upload_date,
                defaults={
                    "CIRCLE": str(d["CIRCLE"]),
                    "SITE_ID": str(d["SITE_ID"]),
                    "BAND": str(d["BAND"]),
                    "UNIQUE_ID": str(d["UNIQUE ID"]),
                    "ENODEB_ID": str(d["ENODEB_ID"]),
                    "Circle_Project": project,
                    "Alarm_Bucket": str(d["ALARM BUCKET"]),
                    "Status": str(d["STATUS"]),
                    "Date": Date,
                    "BTS_TYPE": str(d["BTS_TYPE"]),
                    "OEM_NAME": str(d["OEM_NAME (NOKIA/ZTE/ERICSSON/HUAWEI/SAMSUNG)"]),
                    "TOCO_NAME": str(d["TOCO_NAME"]),
                    "PHYSICAL_AT_Status": str(
                        d[
                            "PHYSICAL_AT_STATUS( ACCEPTED/REJECTED/OFFERED/PENDING/DISMANTLE)"
                        ]
                    ),
                    "Soft_AT_Status": str(
                        d[
                            "SOFT_AT_STATUS( ACCEPTED/REJECTED/OFFERED/PENDING/DISMANTLE)"
                        ]
                    ),
                    "Performance_AT_Status": str(
                        d[
                            "PERFORMANCE_AT_STATUS( ACCEPTED/REJECTED/OFFERED/PENDING/DISMANTLE)"
                        ]
                    ),
                    "CURRENT_STATUS_OF_SITE": str(d["CURRENT_STATUS_OF_SITE"]),
                    "ATP_Name": str(d["ATP NAME"]),
                    "ATP_Status": str(d["ATP STATUS"]),
                    "ATP_Count": str(d["ATP COUNT"]),
                    "Internal_Ms1_Vs_Ms2_In_days": str(
                        d["INTERNAL MS1 VS MS2-IN DAYS"]
                    ),
                    "Total_Allocation": str(d["TOTAL  ALLOCATION"]),
                    "Media_Type": str(
                        d["MEDIA TYPE (UBR/MW/FIBER) RELOCATION/ULS PROJECT ONLY"]
                    ),
                    "Media_Owner": str(d["MEDIA OWNER (MCOMM/OTHER PARTNER)"]),
                    "SPOC": str(d["SPOC"]),
                    "Alarm_Bucket": str(d["ALARM BUCKET"]).upper(),
                    "Alarms_Details": str(d["ALARMS DETAILS"]),
                    "Priority": str(d["PRIORITY"]),
                    "TAT_Details": str(d["TAT DETAILS"]),
                    "UBR_AT_Status_VIPIN": str(d["UBR AT STATUS (VIPIN)"]),
                    "UBR_AT_Status_E": str(d["UBR AT STATUS (E//)"]),
                    "TWAMP_Status": str(d["TWAMP STATUS"]),
                    "Media": str(d["MEDIA"]),
                    "Support_required_from_UBR_Team": str(
                        d["SUPPORT REQUIRED FROM UBR TEAM"]
                    ),
                    "Support_required_from_Circle_Team": str(
                        d["SUPPORT REQUIRED FROM CIRCLE TEAM"]
                    ),
                    "Support_required_from_NOC_Team": str(
                        d["SUPPORT REQUIRED FROM NOC TEAM"]
                    ),
                    "Final_Responsibility": str(
                        d["FINAL RESPONSIBILITY (CIRCLE TEAM/UBR TEAM/NOC TEAM)"]
                    ),
                    "Category": str(d["CATEGORY (HW/MEDIA/INFRA)"]),
                    "Problem_Statement_in_detail": str(
                        d["PROBLEM STATEMENT IN DETAIL"]
                    ),
                    "Final_Remarks": str(d["FINAL REMARKS"]),
                },
            )

            #print("OBJ:", obj)

        except Exception as e:
            #print("error", e)
            error = str(e)
            Soft_At_upload_status.objects.create(
                id=pk,
                Site_id=d["SITE_ID"],
                update_status="Not Uploaded",
                Remark=error,
            )
            return Response({"Status": False, "error": error})


def circle_list(objs):
    cir = []

    for obj in objs:
        cir.append(obj.CIRCLE)

    cir_set = set(cir)
    cir = list(cir_set)
    return cir


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

from rest_framework import status

@api_view(["POST"])
def SoftAt_Report_Upload(request):
    #print("Current_User---------------", request.user)
    if 'soft_at_status' not in request.data:
        return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

    file = request.data['soft_at_status']
    df = pd.read_excel(file,sheet_name="Tracker",keep_default_na=False)
    # except Exception as e:
    #     return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    df.columns=[col.strip() for col in df.columns]
    df = df[df['Unique Key(Auto Generated)'].notna() & (df['Unique Key(Auto Generated)'] != '')]
    
    invalid_rows=[]
    allowed_values={
        'Soft AT Status':["Accepted", "Rejected", "Offered", "Need to be offer", "Dismantle", "Pending", ''],
    }
     
    rejection_allowed_values={
    'Alarm Bucket':["UBR AT Dependency",
    "Sites Locked/Down/Ping Not OK/Upload Failed/Login Failed",
    "Sync Issue - GPS/TOP",
    "HW Alarms",
    "Service Affecting Alarms",
    "VSWR High/Config Issue",
    "GTPU/Trxmn/S1 Link Alarm",
    "Configuration Issue",
    "Sync Issue - GPS/TOP",
    "Incomplete AT details",
    "TWAMP Issue"],

     'Final Responsibility (Circle Team/UBR Team/NOC Team)':["Circle Team",
    "UBR Team",
    "NOC Team"]}

    rejection_empty_check_columns=['Alarm Details']
    def check_multiple_values(value, allowed_list,symbol):
                # #print('value:',value)
                if symbol==',':
                    values = [v.strip() for v in value.split(',')]
                    return all(v in allowed_list for v in values)
                if symbol == '_':
                    values = [v.strip() for v in value.split('_')]
                    return all(v in allowed_list for v in values)

    for index, row in df.iterrows():
    # Filter by unique_key and update multiple fields at once using the `update()` method
        #print("soft_at_status: ",type(row['Soft AT Status']),row['Soft AT Status'])
        if row['First Offering Date'] == '' or pd.isna(row['First Offering Date']):
            first_offering_date = None
        else:
            first_offering_date = row['First Offering Date']

        if row['Offering Date'] == '' or pd.isna(row['Offering Date']):
            offering_date = None
        else:
            offering_date = row['Offering Date']

        if row['Acceptance / Rejection Date'] == '' or pd.isna(row['Acceptance / Rejection Date']):
            acceptance_rejection_date = None
        else:
            acceptance_rejection_date = row['Acceptance / Rejection Date']

        if row['Status Check Date'] == '' or pd.isna(row['Status Check Date']):
            status_check_date = None
        else:
            status_check_date = row['Status Check Date']

        if row['Ageing (in days)'] == '' or pd.isna(row['Ageing (in days)']):
            ageing_in_days = None
        else:
            ageing_in_days = row['Ageing (in days)']
        
        if row['Actual Ageing'] == '' or pd.isna(row['Actual Ageing']):
            actual_ageing = None
        else:
            actual_ageing = row['Actual Ageing']
        
        unique_combination=f"Integration Date: {row['Integration Date']}, Activity Name: {str(row['Activity Name']).upper()}, Site ID: {row['Site ID']}, Technology (SIWA):{row['Technology (SIWA)']}, CIRCLE: {str(row['CIRCLE']).upper()}, Cell ID: {row['Cell ID']}"
        invalid_fields = []
        remarks=[]
        # below code is to check if the status in the excel file is in ['Accepted','Rejected','Need to be offer','Dismantle','Pending']
        if row['Soft AT Status'] not in allowed_values['Soft AT Status']:
            invalid_fields.append('Soft AT Status')
            remarks.append('Value out of specified options')
            invalid_row = {'unique_key': unique_combination, 'invalid_fields': invalid_fields, 'remarks':remarks}
            invalid_rows.append(invalid_row) 
            continue

        combination = row['Unique Key(Auto Generated)'].split('__')[0]
        latest_date = Soft_At_Table.objects.filter(combination=combination).latest('upload_date').upload_date
        latest_date_obj = Soft_At_Table.objects.get(combination=combination,upload_date=latest_date)
        if latest_date_obj.soft_at_status == 'Dismantle':
            invalid_fields.append('Soft AT Status')
            remarks.append('Dismantle status cannot be changed')
            invalid_row = {'unique_key': unique_combination, 'invalid_fields': invalid_fields, 'remarks':remarks}
            invalid_rows.append(invalid_row) 
            continue

# checking if the new status in the excel input is for acceptance
        if row['Soft AT Status'] == 'Accepted':
            #print("inside accepted")
            # below code to check if the acceptance date is not empty
            if  row['Acceptance / Rejection Date'] == '':
                invalid_fields.append('Acceptance / Rejection Date')
                remarks.append('Acceptance Date is mandatory')
                invalid_row = {'unique_key': unique_combination, 'invalid_fields': invalid_fields, 'remarks':remarks}
                invalid_rows.append(invalid_row) 
                continue
            acceptance_date = row['Acceptance / Rejection Date'].date()
            
            
            new_key = row['Unique Key(Auto Generated)'].split('__')[0] + '__' + str(acceptance_date)
            combination = row['Unique Key(Auto Generated)'].split('__')[0]
            try:
                accepect_date_obj = Soft_At_Table.objects.get(unique_key=new_key)
            except Soft_At_Table.DoesNotExist:
                invalid_fields.append('Acceptance / Rejection Date')
                remarks.append('Acceptance Date should be greater than or equal to Integration Date | Acceptance date obj does not exist')
                invalid_row = {'unique_key': unique_combination, 'invalid_fields': invalid_fields, 'remarks':remarks}
                invalid_rows.append(invalid_row)
                continue
            #print(new_key)
            # below code to check if the acceptance date is greater than or equal to the integration date
            if acceptance_date < accepect_date_obj.Integration_Date:
                invalid_fields.append('Acceptance / Rejection Date')
                remarks.append('Acceptance Date should be greater than or equal to Integration Date')
                invalid_row = {'unique_key': unique_combination, 'invalid_fields': invalid_fields, 'remarks':remarks}
                invalid_rows.append(invalid_row)
                continue

            if accepect_date_obj.soft_at_status == 'Offered':

                #print('acceptance_date:',acceptance_date,type(acceptance_date))

                Soft_At_Table.objects.filter(unique_key=new_key).update(
                # IntegrationData=IntegrationTracker_obj,
                soft_at_status=str(row['Soft AT Status']).capitalize(),
                acceptance_rejection_date= acceptance_rejection_date,
                soft_delete=False              
            )

                Soft_At_Table.objects.filter(combination = combination,upload_date__gt=acceptance_date).update(soft_delete=True,soft_at_status='Accepted',acceptance_rejection_date=acceptance_rejection_date)
                # Soft_At_Table.objects.filter(combination = combination,upload_date__gt=acceptance_date).delete()
            else:
                invalid_fields.append('Soft AT Status')
                remarks.append(' Site already Accepted. Should be in Offered status to update to Accepted status')
                invalid_row = {'unique_key': unique_combination, 'invalid_fields': invalid_fields, 'remarks':remarks}   
                invalid_rows.append(invalid_row)
                continue
# checking if the new status in the excel input is for rejected                
        if row['Soft AT Status'] == 'Rejected':
            #print("inside rejected")
            if  row['Acceptance / Rejection Date'] == '':
                invalid_fields.append('Acceptance / Rejection Date')
                remarks.append('Acceptance Date is mandatory')
                invalid_row = {'unique_key': unique_combination, 'invalid_fields': invalid_fields, 'remarks':remarks}
                invalid_rows.append(invalid_row) 
                continue
            # print(row['Acceptance / Rejection Date'], type(row['Acceptance / Rejection Date']))
            rejection_date = row['Acceptance / Rejection Date'].date()
            new_key = row['Unique Key(Auto Generated)'].split('__')[0] + '__' + str(rejection_date)
            try:
                 rejection_date_obj = Soft_At_Table.objects.get(unique_key=new_key)
            except Soft_At_Table.DoesNotExist:
                invalid_fields.append('Acceptance / Rejection Date')
                remarks.append('Acceptance Date should be greater than or equal to Integration Date | Rejection date obj does not exist')
                invalid_row = {'unique_key': unique_combination, 'invalid_fields': invalid_fields, 'remarks':remarks}
                invalid_rows.append(invalid_row)
                continue
            #print(new_key)
            
            # below code to check if the rejection date is greater than or equal to the integration date
            if rejection_date < rejection_date_obj.Integration_Date:
                invalid_fields.append('Acceptance / Rejection Date')
                remarks.append('Acceptance Date should be greater than or equal to Integration Date')
                invalid_row = {'unique_key': unique_combination, 'invalid_fields': invalid_fields, 'remarks':remarks}
                invalid_rows.append(invalid_row)
                continue

            error_field=[]
            error_remark=[]
            for col in rejection_allowed_values:
                if row[col] not in rejection_allowed_values[col]:
                    error_field.append(col)
                    error_remark.append('Value out of specified options')
            # empty_cols= [col for col in rejection_empty_check_columns
            #             if col not in df.columns 
            #             or pd.isnull(row[col]) 
            #             or str(row[col]).strip() == '' 
            #             ]
            for col in rejection_empty_check_columns:
                if pd.isnull(row[col]) or str(row[col]).strip() == '':
                    error_field.append(col)
                    error_remark.append('Value is mandatory')

            if len(error_field)>0:
                invalid_fields.extend(error_field)
                remarks.extend(error_remark)
                invalid_row = {'unique_key': unique_combination, 'invalid_fields': invalid_fields, 'remarks':remarks}
                invalid_rows.append(invalid_row) 
                continue
            
            if rejection_date_obj.soft_at_status == 'Offered':
                rejection_date = row['Acceptance / Rejection Date'].date()
                new_key = row['Unique Key(Auto Generated)'].split('__')[0] + '__' + str(rejection_date)
                combination = row['Unique Key(Auto Generated)'].split('__')[0]

                Soft_At_Table.objects.filter(unique_key=new_key).update(
                # IntegrationData=IntegrationTracker_obj,     
                soft_at_status=str(row['Soft AT Status']).capitalize(),
             
                acceptance_rejection_date= acceptance_rejection_date,
                alarm_bucket=row['Alarm Bucket'],
                alarm_details=row['Alarm Details'],
                final_responsibility=row['Final Responsibility (Circle Team/UBR Team/NOC Team)'],
                
                )
                updated_obj = Soft_At_Table.objects.get(unique_key=new_key)
                Soft_At_Table.objects.filter(combination = combination,upload_date__gt=rejection_date).update(soft_at_status='Pending',
                                                                                                              spoc_name=updated_obj.spoc_name,
                                                                                                              offering_type=updated_obj.offering_type,
                                                                                                              first_offering_date=updated_obj.first_offering_date,
                                                                                                              offering_date=updated_obj.offering_date,
                                                                                                              acceptance_rejection_date= updated_obj.acceptance_rejection_date,
                                                                                                              alarm_bucket=updated_obj.alarm_bucket,
                                                                                                              alarm_details= updated_obj.alarm_details,
                                                                                                              final_responsibility=updated_obj.final_responsibility,
                                                                                                              workable_non_workable= updated_obj.workable_non_workable,
                                                                                                              ubr_ms2_status= updated_obj.ubr_ms2_status,
                                                                                                              ubr_link_id= updated_obj.ubr_link_id,
                                                                                                              twamp_status= updated_obj.twamp_status,
                                                                                                              status_check_date= updated_obj.status_check_date,
                                                                                                              ageing_in_days= updated_obj.ageing_in_days,
                                                                                                              actual_ageing= updated_obj.actual_ageing,
                                                                                                              toco_partner= updated_obj.toco_partner,
                                                                                                              support_required_ubr_team= updated_obj.support_required_ubr_team,
                                                                                                              support_required_circle_team= updated_obj.support_required_circle_team,
                                                                                                              support_required_noc_team= updated_obj.support_required_noc_team,
                                                                                                              category= updated_obj.category,
                                                                                                              problem_statement= updated_obj.problem_statement,
                                                                                                              final_remarks= updated_obj.final_remarks,
                                                                                                              ms1= updated_obj.ms1,)
            else:
                invalid_fields.append('Soft AT Status')
                remarks.append(' Site should be in Offered status to update to Rejected status')
                invalid_row = {'unique_key': unique_combination, 'invalid_fields': invalid_fields, 'remarks':remarks}
                invalid_rows.append(invalid_row)
                continue
# checking if the new status in the excel input is for offered
        if row['Soft AT Status'] == 'Offered':
            if  row['Offering Date'] == '':
                invalid_fields.append('Offering Date')
                remarks.append('Offering Date is mandatory')
                invalid_row = {'unique_key': unique_combination, 'invalid_fields': invalid_fields, 'remarks':remarks}
                invalid_rows.append(invalid_row)
                continue

            offered_date = row['Offering Date'].date()


            new_key = row['Unique Key(Auto Generated)'].split('__')[0] + '__' + str(offered_date)
            combination = row['Unique Key(Auto Generated)'].split('__')[0] 
            try:
                offered_date_obj = Soft_At_Table.objects.get(unique_key=new_key)
            except Soft_At_Table.DoesNotExist:
                invalid_fields.append('Offering Date')
                remarks.append('Offering Date obj does not exist')
                invalid_row = {'unique_key': unique_combination, 'invalid_fields': invalid_fields, 'remarks':remarks}
                invalid_rows.append(invalid_row)
                continue

            # below code to check if the offered date is greater than or equal to the integration date
            if offered_date < offered_date_obj.Integration_Date:
                invalid_fields.append('Offering Date')
                remarks.append('Offering Date should be greater than or equal to Integration Date')
                invalid_row = {'unique_key': unique_combination, 'invalid_fields': invalid_fields, 'remarks':remarks}
                invalid_rows.append(invalid_row)
                continue

            if offered_date_obj.soft_at_status in ['Pending', 'NOT OFFERED','Need to be offer','Rejected']:
                if offered_date_obj.soft_at_status == 'NOT OFFERED':
                    # below code is to check for first offering date if provided or not
                    if row['First Offering Date'] == '':
                        invalid_fields.append('First Offering Date')
                        remarks.append('First Offering Date is mandatory')
                        invalid_row = {'unique_key': unique_combination, 'invalid_fields': invalid_fields, 'remarks':remarks}
                        invalid_rows.append(invalid_row)
                        continue
                    else:
                        first_offering_date = row['First Offering Date'].date()

                    #print("for none")
                    Soft_At_Table.objects.filter(unique_key = new_key).update(
                    # IntegrationData=IntegrationTracker_obj,
                    spoc_name=row['SPOC NAME'],
                    offering_type=row['Offering Type'],
                    first_offering_date=first_offering_date,
                    soft_at_status=str(row['Soft AT Status']).capitalize(),
                    offering_date=offering_date,
                    
                                             ) 
                    updated_obj = Soft_At_Table.objects.get(unique_key=new_key)

                    Soft_At_Table.objects.filter( combination=combination, upload_date__gt = offered_date).update(soft_at_status='Offered',
                                                                                                                  spoc_name=updated_obj.spoc_name,
                                                                                                                  offering_type=updated_obj.offering_type,
                                                                                                                  first_offering_date= updated_obj.first_offering_date,
                                                                                                                  offering_date=updated_obj.offering_date,
                                                                                                                  acceptance_rejection_date= updated_obj.acceptance_rejection_date,
                                                                                                                  alarm_bucket= updated_obj.alarm_bucket,
                                                                                                                  alarm_details= updated_obj.alarm_details,
                                                                                                                  final_responsibility= updated_obj.final_responsibility,
                                                                                                                  workable_non_workable= updated_obj.workable_non_workable,
                                                                                                                  ubr_ms2_status= updated_obj.ubr_ms2_status,
                                                                                                                  ubr_link_id= updated_obj.ubr_link_id,
                                                                                                                  twamp_status= updated_obj.twamp_status,
                                                                                                                  status_check_date= updated_obj.status_check_date,
                                                                                                                  ageing_in_days= updated_obj.ageing_in_days,
                                                                                                                  actual_ageing= updated_obj.actual_ageing,
                                                                                                                  toco_partner= updated_obj.toco_partner,
                                                                                                                  support_required_ubr_team= updated_obj.support_required_ubr_team,
                                                                                                                  support_required_circle_team= updated_obj.support_required_circle_team,
                                                                                                                  support_required_noc_team= updated_obj.support_required_noc_team,
                                                                                                                  category= updated_obj.category,
                                                                                                                  problem_statement= updated_obj.problem_statement,
                                                                                                                  final_remarks= updated_obj.final_remarks,
                                                                                                                  ms1= updated_obj.ms1,)

                elif offered_date_obj.soft_at_status == 'Pending' or offered_date_obj.soft_at_status == 'Rejected':
                    #print("when ")
                    Soft_At_Table.objects.filter(unique_key=new_key).update(
                        # IntegrationDate=IntegrationTracker_obj,
                        spoc_name=row['SPOC NAME'],
                        offering_type=row['Offering Type'],
                        soft_at_status=str(row['Soft AT Status']).capitalize(),
                        offering_date=offering_date,
                       
                    )
                    updated_obj = Soft_At_Table.objects.get(unique_key=new_key)
                    Soft_At_Table.objects.filter(combination=combination,upload_date__gt = offered_date).update(soft_at_status='Offered',
                                                                                                                  spoc_name=updated_obj.spoc_name,
                                                                                                                  offering_type=updated_obj.offering_type,
                                                                                                                  first_offering_date= updated_obj.first_offering_date,
                                                                                                                  offering_date=updated_obj.offering_date,
                                                                                                                  acceptance_rejection_date= updated_obj.acceptance_rejection_date,
                                                                                                                  alarm_bucket= updated_obj.alarm_bucket,
                                                                                                                  alarm_details= updated_obj.alarm_details,
                                                                                                                  final_responsibility= updated_obj.final_responsibility,
                                                                                                                  workable_non_workable= updated_obj.workable_non_workable,
                                                                                                                  ubr_ms2_status= updated_obj.ubr_ms2_status,
                                                                                                                  ubr_link_id= updated_obj.ubr_link_id,
                                                                                                                  twamp_status= updated_obj.twamp_status,
                                                                                                                  status_check_date= updated_obj.status_check_date,
                                                                                                                  ageing_in_days= updated_obj.ageing_in_days,
                                                                                                                  actual_ageing= updated_obj.actual_ageing,
                                                                                                                  toco_partner= updated_obj.toco_partner,
                                                                                                                  support_required_ubr_team= updated_obj.support_required_ubr_team,
                                                                                                                  support_required_circle_team= updated_obj.support_required_circle_team,
                                                                                                                  support_required_noc_team= updated_obj.support_required_noc_team,
                                                                                                                  category= updated_obj.category,
                                                                                                                  problem_statement= updated_obj.problem_statement,
                                                                                                                  final_remarks= updated_obj.final_remarks,
                                                                                                                  ms1= updated_obj.ms1)

                elif offered_date_obj.soft_at_status == 'Need to be offer':
                    combination=row['Unique Key(Auto Generated)'].split('__')[0]
                    previous_state_obj = Soft_At_Table.objects.filter(combination = combination , upload_date__lt = offered_date).exclude(soft_at_status=offered_date_obj.soft_at_status).order_by('-upload_date').first()
                    previous_state = previous_state_obj.soft_at_status
                    #print("previous state",previous_state)
                    if previous_state == 'NOT OFFERED':
                            if row['First Offering Date'] == '':
                                invalid_fields.append('First Offering Date')
                                remarks.append('First Offering Date is mandatory')
                                invalid_row = {'unique_key': unique_combination, 'invalid_fields': invalid_fields, 'remarks':remarks}
                                invalid_rows.append(invalid_row)
                                continue
                            else:
                                first_offering_date = row['First Offering Date'].date()
                            #print("for none")
                            Soft_At_Table.objects.filter(unique_key = new_key).update(
                            # IntegrationData=IntegrationTracker_obj,
                            spoc_name=row['SPOC NAME'],
                            offering_type=row['Offering Type'],
                            soft_at_status=str(row['Soft AT Status']).capitalize(),
                            offering_date=offering_date,
                            first_offering_date=first_offering_date
                             ) 
                            updated_obj = Soft_At_Table.objects.get(unique_key=new_key)
                            Soft_At_Table.objects.filter(combination=combination, upload_date__gt = offered_date).update(soft_at_status='Offered',
                                                                                                                  spoc_name=updated_obj.spoc_name,
                                                                                                                  offering_type=updated_obj.offering_type,
                                                                                                                  first_offering_date= updated_obj.first_offering_date,
                                                                                                                  offering_date=updated_obj.offering_date,
                                                                                                                  acceptance_rejection_date= updated_obj.acceptance_rejection_date,
                                                                                                                  alarm_bucket= updated_obj.alarm_bucket,
                                                                                                                  alarm_details= updated_obj.alarm_details,
                                                                                                                  final_responsibility= updated_obj.final_responsibility,
                                                                                                                  workable_non_workable= updated_obj.workable_non_workable,
                                                                                                                  ubr_ms2_status= updated_obj.ubr_ms2_status,
                                                                                                                  ubr_link_id= updated_obj.ubr_link_id,
                                                                                                                  twamp_status= updated_obj.twamp_status,
                                                                                                                  status_check_date= updated_obj.status_check_date,
                                                                                                                  ageing_in_days= updated_obj.ageing_in_days,
                                                                                                                  actual_ageing= updated_obj.actual_ageing,
                                                                                                                  toco_partner= updated_obj.toco_partner,
                                                                                                                  support_required_ubr_team= updated_obj.support_required_ubr_team,
                                                                                                                  support_required_circle_team= updated_obj.support_required_circle_team,
                                                                                                                  support_required_noc_team= updated_obj.support_required_noc_team,
                                                                                                                  category= updated_obj.category,
                                                                                                                  problem_statement= updated_obj.problem_statement,
                                                                                                                  final_remarks= updated_obj.final_remarks,
                                                                                                                  ms1= updated_obj.ms1)
                    elif previous_state == 'Pending':
                            #print("when ")
                            Soft_At_Table.objects.filter(unique_key=new_key).update(
                                # IntegrationDate=IntegrationTracker_obj,
                                 spoc_name=row['SPOC NAME'],
                                offering_type=row['Offering Type'],
                                soft_at_status=str(row['Soft AT Status']).capitalize(),
                                offering_date=offering_date,
                                first_offering_date=first_offering_date
                                
                            )
                            updated_obj = Soft_At_Table.objects.get(unique_key=new_key)
                            Soft_At_Table.objects.filter(combination=combination, upload_date__gt = offered_date).update(soft_at_status='Offered',
                                                                                                                  spoc_name=updated_obj.spoc_name,
                                                                                                                  offering_type=updated_obj.offering_type,
                                                                                                                  first_offering_date= updated_obj.first_offering_date,
                                                                                                                  offering_date=updated_obj.offering_date,
                                                                                                                  acceptance_rejection_date= updated_obj.acceptance_rejection_date,
                                                                                                                  alarm_bucket= updated_obj.alarm_bucket,
                                                                                                                  alarm_details= updated_obj.alarm_details,
                                                                                                                  final_responsibility= updated_obj.final_responsibility,
                                                                                                                  workable_non_workable= updated_obj.workable_non_workable,
                                                                                                                  ubr_ms2_status= updated_obj.ubr_ms2_status,
                                                                                                                  ubr_link_id= updated_obj.ubr_link_id,
                                                                                                                  twamp_status= updated_obj.twamp_status,
                                                                                                                  status_check_date= updated_obj.status_check_date,
                                                                                                                  ageing_in_days= updated_obj.ageing_in_days,
                                                                                                                  actual_ageing= updated_obj.actual_ageing,
                                                                                                                  toco_partner= updated_obj.toco_partner,
                                                                                                                  support_required_ubr_team= updated_obj.support_required_ubr_team,
                                                                                                                  support_required_circle_team= updated_obj.support_required_circle_team,
                                                                                                                  support_required_noc_team= updated_obj.support_required_noc_team,
                                                                                                                  category= updated_obj.category,
                                                                                                                  problem_statement= updated_obj.problem_statement,
                                                                                                                  final_remarks= updated_obj.final_remarks,
                                                                                                                  ms1= updated_obj.ms1)
            else:
                invalid_fields.append('Soft AT Status')
                remarks.append(' Site should be in Pending | NOT OFFERED | Need to be offer status to update to Offered status')
                invalid_row = {'unique_key': unique_combination, 'invalid_fields': invalid_fields, 'remarks':remarks}
                invalid_rows.append(invalid_row)
                continue
# checking if the new status in the excel input is for need to be offer 
        if row['Soft AT Status'] == 'Need to be offer':
            print("Inside need to be offer")
            unique_key = row['Unique Key(Auto Generated)'].split("__")[0] + "__" + str(datetime.now().date())
            print(unique_key)
            obj=Soft_At_Table.objects.get(unique_key=unique_key)
            if obj.soft_at_status == 'Accepted':
                invalid_fields.append('Soft AT Status')
                remarks.append('Accepted site can\'t be updated to Need to be offer')
                invalid_row = {'unique_key': unique_combination, 'invalid_fields': invalid_fields, 'remarks':remarks}
                invalid_rows.append(invalid_row)
                continue
            Soft_At_Table.objects.filter(unique_key=unique_key,soft_delete=False).update(
                # IntegrationDate=IntegrationTracker_obj,
            
                soft_at_status=str(row['Soft AT Status']).capitalize(),

            )
# checking if the new status in the excel input is for pending        
        if row['Soft AT Status'] == 'Pending':
            #print("Inside Pending...........")
            unique_key = row['Unique Key(Auto Generated)'].split("__")[0] + "__" + str(datetime.now().date())
            Soft_At_Table.objects.filter(unique_key=unique_key,soft_delete=False).update(
                # IntegrationDate=IntegrationTracker_obj,
                soft_at_status=str(row['Soft AT Status']).capitalize(),
                workable_non_workable=row['Workable/Non-Workable'],
                ubr_ms2_status=row['UBR MS2 Status'],
                ubr_link_id=row['UBR Link ID'],
                twamp_status=row['TWAMP Status'],
                status_check_date= status_check_date,
                ageing_in_days=ageing_in_days,
                actual_ageing=actual_ageing,
                toco_partner=row['TOCO Partner'],
                support_required_ubr_team=row['Support required from UBR Team'],
                support_required_circle_team=row['Support required from Circle Team'],
                support_required_noc_team=row['Support required from NOC Team'],
                category=row['Category (HW/Media/Infra)'],
                problem_statement=row['Problem Statement in detail'],
                final_remarks=row['Final Remarks'],
                ms1=row['MS1']
            ) 
# checking if the new status in the excel input is for dismantle
        if row['Soft AT Status'] == 'Dismantle':
            #print("Inside Dismantle...........")
            unique_key = row['Unique Key(Auto Generated)'].split("__")[0] + "__" + str(datetime.now().date())
            Soft_At_Table.objects.filter(unique_key=unique_key,soft_delete=False).update(
                # IntegrationDate=IntegrationTracker_obj,
                
                soft_at_status=str(row['Soft AT Status']).capitalize(),
               
            )
# checking if the new status in the excel input is for No AT Required
        if row['Soft AT Status'] == 'No AT Required':
            #print("Inside No AT Required...........")
            unique_key = row['Unique Key(Auto Generated)'].split("__")[0] + "__" + str(datetime.now().date())
            Soft_At_Table.objects.filter(unique_key=unique_key,soft_delete=False).update(
                # IntegrationDate=IntegrationTracker_obj,
                
                soft_at_status=str(row['Soft AT Status']).capitalize(),
            )
    return Response(
            {
                "status": True,
                "message": "Report uploaded Successfully .",
                "error_rows": invalid_rows,
            }
        )






@api_view(["POST"])
def SoftAt_Report_create(request):
    #print("Current_User---------------", request.user)
    if 'soft_at_status' not in request.data:
        return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

    file = request.data['soft_at_status']
    

    
    df = pd.read_excel(file,sheet_name="Tracker",keep_default_na=False,)
    # except Exception as e:
    #     return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    df.columns=[col.strip() for col in df.columns]
    # df = df[df['Unique Key(Auto Generated)'].notna() & (df['Unique Key(Auto Generated)'] != '')]
    #print(df)
    for index, row in df.iterrows():
        #print(index)
    # Filter by unique_key and update multiple fields at once using the `update()` method
        if row['First Offering Date'] == '' or pd.isna(row['First Offering Date']):
            first_offering_date = None
        else:
            first_offering_date = row['First Offering Date']

        if row['Offering Date'] == '' or pd.isna(row['Offering Date']):
            offering_date = None
        else:
            offering_date = row['Offering Date']

        if row['Acceptance / Rejection Date'] == '' or pd.isna(row['Acceptance / Rejection Date']):
            acceptance_rejection_date = None
        else:
            acceptance_rejection_date = row['Acceptance / Rejection Date']

        if row['Status Check Date'] == '' or pd.isna(row['Status Check Date']):
            status_check_date = None
        else:
            status_check_date = row['Status Check Date']

        if row['Ageing (in days)'] == '' or pd.isna(row['Ageing (in days)']):
            ageing_in_days = None
        else:
            ageing_in_days = row['Ageing (in days)']
        
        if row['Actual Ageing'] == '' or pd.isna(row['Actual Ageing']):
            actual_ageing = None
        else:
            actual_ageing = row['Actual Ageing']
        # obj=Soft_At_Table.objects.get(unique_key=row['Unique Key(Auto Generated)'])
        
        # ix_unq = str(row['Integration Date']) + str(row['Activity Name']).upper() + str(row['Site ID']) + str(row['Technology (SIWA)']) + str(row['CIRCLE']).upper() + str(row['Cell ID']) + str(row['LNBTS ID']) + str(row['OEM']).upper()
        ix_unq = str(row['Integration Date']) + str(row['Activity Name']).upper() + str(row['Site ID']) + str(row['Technology (SIWA)']) + str(row['CIRCLE']).upper() + str(row['Cell ID']) + str(row['LNBTS ID']) + str(row['OEM']).upper()
        try:
            IntegrationTracker_obj=IntegrationData.objects.get(unique_key= ix_unq)
            # IntegrationTracker_obj=None
        except IntegrationData.DoesNotExist:
            IntegrationTracker_obj = None
            #print("No integration Object...")

 
      
        upload_date = datetime(2024,10,24).date()
        unique_key = str(row['Integration Date']) + str(row['Activity Name']).upper() + str(row['Site ID']) + str(row['Technology (SIWA)']) + str(row['CIRCLE']).upper() + str(row['Cell ID']) + str(row['LNBTS ID']) + str(row['OEM']).upper() + "__" + str(upload_date)
        # unique_key = row['Unique Key(Auto Generated)']
        # upload_date = row['Unique Key(Auto Generated)'].split("__")[1]

        # upload_date = datetime.strptime(upload_date, "%Y-%m-%d").date()
        #print(type(upload_date),upload_date)
        
        Soft_At_Table.objects.update_or_create(
            unique_key=unique_key,  # LookUp field
            defaults={
            'combination':ix_unq,
            'upload_date': upload_date,
            'soft_at_status': row['Soft AT Status'],
            'IntegrationData': IntegrationTracker_obj,
            'spoc_name': row['SPOC NAME'],
            'offering_type': row['Offering Type'],
            'first_offering_date': first_offering_date,
            'soft_at_status': row['Soft AT Status'],
            'offering_date': offering_date,
            'acceptance_rejection_date': acceptance_rejection_date,
            'alarm_bucket': row['Alarm Bucket'],
            'alarm_details': row['Alarm Details'],
            'final_responsibility': row['Final Responsibility (Circle Team/UBR Team/NOC Team)'],
            'workable_non_workable': row['Workable/Non-Workable'],
            'ubr_ms2_status': row['UBR MS2 Status'],
            'ubr_link_id': row['UBR Link ID'],
            'twamp_status': row['TWAMP Status'],
            'status_check_date': status_check_date,
            'ageing_in_days': ageing_in_days,
            'actual_ageing': actual_ageing,
            'toco_partner': row['TOCO Partner'],
            'support_required_ubr_team': row['Support required from UBR Team'],
            'support_required_circle_team': row['Support required from Circle Team'],
            'support_required_noc_team': row['Support required from NOC Team'],
            'category': row['Category (HW/Media/Infra)'],
            'problem_statement': row['Problem Statement in detail'],
            'final_remarks': row['Final Remarks'],
            'ms1': row['MS1'],

            # integration data
            'MO_NAME': str(row['MO NAME']).upper(),  
            'Integration_Date': row['Integration Date'], 
            'CIRCLE': row['CIRCLE'].upper(),
            'Activity_Name': row['Activity Name'].upper(),
            'Site_ID': row['Site ID'],
            'Technology_SIWA': row['Technology (SIWA)'], 
            'Cell_ID': row['Cell ID'],
            'LNBTS_ID': row['LNBTS ID'],
            'OEM': row['OEM'].upper(),              
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
            'status_updated_by':'ATP Sites',
        }
        )
    else:

        return Response({"status": True, "message": "Data uploaded successfully"})


# @api_view(["POST"])
# def SoftAt_Delete_Report(request):
#     date_to_delete = request.POST.get("date_to_delete")

#     if not date_to_delete:
#         return Response(
#             {"status": False, "message": "Please provide a valid date for deletion."}
#         )

#     try:
#         Soft_At_Table.objects.filter(upload_date=date_to_delete).delete()
#         return Response(
#             {
#                 "status": True,
#                 "message": f"Reports for {date_to_delete} deleted successfully.",
#             }
#         )
#     except Exception as e:
#         return Response(
#             {
#                 "status": False,
#                 "message": f"Failed to delete reports for {date_to_delete}. Error: {str(e)}",
#             }
#         )

# adding the total column sum in the total column
def df_raw_column_total(data):
    # Create a DataFrame from the input data
    df = pd.DataFrame(data)

    # Transpose the DataFrame (swap rows and columns)
    df = df.T

    # Add a sum row at the bottom of the DataFrame
    df.loc["Total"] = df.sum()

    # Add a sum column at the right end of the DataFrame
    df["Total"] = df.sum(axis=1)

    # Convert the DataFrame to a JSON string
    json_data = df.to_json(orient="index")

    # Convert the JSON string to a dictionary in Python
    json_data = json.loads(json_data)

    # Print the DataFrame for debugging
    #print(df)

    return json_data

# adding the total row  in the total raw
def df_raw_column_total_circle_wise(data):
    #print("_________________circle_wise_data_____________________________________")
    #print(data)
    df = pd.DataFrame(data)
    df = df.T
    #print("---------------------------dataframe------------------------", df)
    # add a sum row at the bottom of the dataframe
    df.loc["Total"] = df.sum()
    # add a sum column at the right end of the dataframe
    df["Total"] = (
        df["Accepted"]
        + df["Rejected"]
        + df["Dismantle"]
        + df["Pending"]
        + df["Need_to_be_offer"]
        + df["Offered"]
        + df["NOT_OFFERED"]
    )
    json_data = df.to_json(
        orient="index"
    )  # here json_data  converts the dataframe to a string json
    json_data = json.loads(
        json_data
    )  # json.loads - Which converts the string form of json data to a dictionary in python.
    #print(df)
    return json_data


# def pending_sites_bucketization_week(objs):
#     ################### code for pending sites bucketization ###################

#     #print("bhai ovj kyua hai__________", objs)

#     # Retrieve the last day of the week for each week
#     last_day_of_weeks = (
#         objs.annotate(week=TruncWeek("upload_date"))
#         .values("week")
#         .annotate(last_day_of_week=Max("upload_date"))
#     )

#     Circle_Team = objs.filter(
#         Status__in=["Pending"],
#         Final_Responsibility="Circle Team".upper(),
#         upload_date__in=last_day_of_weeks.values("last_day_of_week"),
#     ).count()

#     Circle_Team_NOC_Team = objs.filter(
#         Status__in=["Pending"],
#         Final_Responsibility="NOC Team".upper(),
#         upload_date__in=last_day_of_weeks.values("last_day_of_week"),
#     ).count()

#     NOC_Team = objs.filter(
#         Status__in=["Pending"],
#         Final_Responsibility="UBR Team".upper(),
#         upload_date__in=last_day_of_weeks.values("last_day_of_week"),
#     ).count()

#     pending_sites_bucketization = {}
#     pending_sites_bucketization["Pending"] = {
#         "Circle_Team": Circle_Team,
#         "Circle_Team_NOC_Team": Circle_Team_NOC_Team,
#         "NOC_Team": NOC_Team,
#     }

#     pending_sites_bucketization = df_raw_column_total(pending_sites_bucketization)
#     return pending_sites_bucketization


def pending_sites_bucketization(objs):
    ################### code for pending sites bucketization ###################

    #print("", objs)

    Circle_Team = objs.filter(
        soft_at_status__in=["Pending"], final_responsibility__iexact="Circle Team".upper()
    ).count()
    Circle_Team_NOC_Team = objs.filter(
        soft_at_status__in=["Pending"], final_responsibility__iexact="NOC Team".upper()
    ).count()
    # circle_Team_Media_team = objs.filter(
    #     Status="Pending", Final_Responsibility="Circle/Media team"
    # ).count()
    NOC_Team = objs.filter(
        soft_at_status__in=["Pending"], final_responsibility__iexact="UBR Team".upper()
    ).count()

    Airtel_Team = objs.filter(
        soft_at_status__in=["Pending"], final_responsibility__iexact="Airtel".upper()
    ).count()

    MWTM = objs.filter(
        soft_at_status__in=["Pending"], final_responsibility__iexact="mwtm".upper()
    ).count()

    pending_sites_bucketization = {}
    pending_sites_bucketization["Pending"] = {
        "Circle_Team": Circle_Team,
        "Circle_Team_NOC_Team": Circle_Team_NOC_Team,
        # "circle_Team_Media_team": circle_Team_Media_team,
        "NOC_Team": NOC_Team,
        "Airtel": Airtel_Team,
        "MWTM": MWTM,
    }

    #print("Pending Site Buckets: ", pending_sites_bucketization)
    pending_sites_bucketization = df_raw_column_total(pending_sites_bucketization)
    return pending_sites_bucketization



def Alarm_Bucket(objs):
    ################## Alarm_Bucket Code #########################
    objs = objs.filter(soft_at_status__in=["Pending"])
    df = pd.DataFrame(list(objs.values()))
    Configuration_issue = objs.filter(
        alarm_bucket="Configuration Issue" 
    ).count()

    GTPU_Trxmn_S1_Link_Alarm = objs.filter(
        alarm_bucket="GTPU/Trxmn/S1 Link Alarm"
    ).count()

    HW_Alarms = objs.filter(alarm_bucket="HW Alarms").count()

    Need_to_check = objs.filter(alarm_bucket="Need to check").count()

    Service_affecting_alarm = objs.filter(
        alarm_bucket="Service Affecting Alarms"
    ).count()

    Sites_Locked_Down_Ping_Not_OK_Upload_Failed_Login_Failed = objs.filter(
        alarm_bucket="Sites Locked/Down/Ping Not OK/Upload Failed/Login Failed" 
    ).count()

    Sync_Issue_GPS_TOP = objs.filter(
        alarm_bucket="Sync Issue - GPS/TOP"
    ).count()

    TWAMP_Issue = objs.filter(alarm_bucket="TWAMP Issue").count()

    UBR_AT_Dependency = objs.filter(
        alarm_bucket__in=[x for x in ["UBR AT Dependency", "Media issue"]]
    ).count()

    Incomplete_AT_details = objs.filter(
        alarm_bucket__in=[x for x in ["Incomplete AT details"]]
    ).count()

    VSWR_High_Config_Issue = objs.filter(
        alarm_bucket="VSWR High/Config Issue"
    ).count()
    total = (
        Configuration_issue
        + GTPU_Trxmn_S1_Link_Alarm
        + HW_Alarms
        + Need_to_check
        + Service_affecting_alarm
        + Sites_Locked_Down_Ping_Not_OK_Upload_Failed_Login_Failed
        + Sync_Issue_GPS_TOP
        + TWAMP_Issue
        + UBR_AT_Dependency
        + VSWR_High_Config_Issue
        + Incomplete_AT_details
    )

    alarm_bucketization = {}

    alarm_bucketization["Configuration Issue"] = {
        "Count_of_Alarm_Bucket": Configuration_issue
    }
    alarm_bucketization["GTPU/Trxmn/S1 Link Alarm"] = {
        "Count_of_Alarm_Bucket": GTPU_Trxmn_S1_Link_Alarm
    }
    alarm_bucketization["HW Alarms"] = {"Count_of_Alarm_Bucket": HW_Alarms}
    alarm_bucketization["Need to check"] = {"Count_of_Alarm_Bucket": Need_to_check}

    alarm_bucketization["Service Affecting Alarms"] = { 
        "Count_of_Alarm_Bucket": Service_affecting_alarm
    }
    alarm_bucketization["Sites Locked/Down/Ping Not OK/Upload Failed/Login Failed"] = {
        "Count_of_Alarm_Bucket": Sites_Locked_Down_Ping_Not_OK_Upload_Failed_Login_Failed
    }
    alarm_bucketization["Sync Issue - GPS/TOP"] = {
        "Count_of_Alarm_Bucket": Sync_Issue_GPS_TOP
    }
    alarm_bucketization["TWAMP Issue"] = {"Count_of_Alarm_Bucket": TWAMP_Issue}
    alarm_bucketization["VSWR High/Config Issue"] = {
        "Count_of_Alarm_Bucket": VSWR_High_Config_Issue
    }
    alarm_bucketization["UBR AT Dependency"] = {
        "Count_of_Alarm_Bucket": UBR_AT_Dependency
    }
    alarm_bucketization["Incomplete AT details"] = {
        "Count_of_Alarm_Bucket": Incomplete_AT_details
    }
    alarm_bucketization["Grand Total"] = {"Count_of_Alarm_Bucket": total}
    


    return alarm_bucketization


def pending_ageing(objs):
    circles = circle_list(objs)
    ageing_circleWise = {}

    for circle in circles:
        obj = objs.filter(CIRCLE=circle)
        ageing_0_15 = obj.filter(
            soft_at_status__in=["Pending"], actual_ageing="0-15"
        ).count()
        ageing_16_30 = obj.filter(
            soft_at_status__in=["Pending"], actual_ageing="16-30"
        ).count()
        ageing_31_60 = obj.filter(
            soft_at_status__in=["Pending"], actual_ageing="31-60"
        ).count()
        ageing_61_90 = obj.filter(
            soft_at_status__in=["Pending"],
            actual_ageing__in=["61-90"],
        ).count()
        ageing_GT90 = obj.filter(
            soft_at_status__in=["Pending"], actual_ageing__in=["GT90", "91-120"]
        ).count()
        ageing_GT120 = obj.filter(
            soft_at_status__in=["Pending"], actual_ageing="GT120"
        ).count()

        ageing_circleWise[circle] = {
            "ageing_0_15": ageing_0_15,
            "ageing_16_30": ageing_16_30,
            "ageing_31_60": ageing_31_60,
            "ageing_61_90": ageing_61_90,
            "ageing_GT90": ageing_GT90,
            "ageing_GT120": ageing_GT120,
        }

    # Check if ageing_circleWise is not empty before calling df_raw_column_total
    if ageing_circleWise:
        ageing_circleWise_data = df_raw_column_total(ageing_circleWise)
        #print("ageing_circle_data..............", ageing_circleWise_data)
        return ageing_circleWise_data
    else:
        # Handle the case when ageing_circleWise is empty
        #print("ageing_circleWise is empty")
        return {}
    
def Alarm_Bucket_all_data(objs, unique_alarm):
    #print(objs)
    df = pd.DataFrame(list(objs.values()))
    df = df[["CIRCLE","SITE_ID","Alarm_Bucket", "Alarms_Details","Internal_Ms1_Vs_Ms2_In_days","Status"]]
    df=df.rename(columns={"Internal_Ms1_Vs_Ms2_In_days":"Aging"})
    #print(df)
    # exit(0)
    all_alarm_data = {}
    for alarm in unique_alarm:
        all_alarm_data[alarm] = df[df['Alarm_Bucket']==alarm].to_dict(orient='records')
    
    return all_alarm_data


# def Alarm_Bucket_week(objs):
#     ################## Alarm_Bucket Code #########################

#     objs = objs.filter(Status__in=["Pending"])

#     # Retrieve the last day of the week for each week
#     last_day_of_weeks = (
#         objs.annotate(week=TruncWeek("upload_date"))
#         .values("week")
#         .annotate(last_day_of_week=Max("upload_date"))
#     )

#     Configuration_issue = objs.filter(
#         Alarm_Bucket="Configuration issue",
#         upload_date__in=last_day_of_weeks.values("last_day_of_week"),
#     ).count()

#     GTPU_Trxmn_S1_Link_Alarm = objs.filter(
#         Alarm_Bucket="GTPU/Trxmn/S1 Link Alarm",
#         upload_date__in=last_day_of_weeks.values("last_day_of_week"),
#     ).count()

#     HW_Alarms = objs.filter(
#         Alarm_Bucket="HW Alarms",
#         upload_date__in=last_day_of_weeks.values("last_day_of_week"),
#     ).count()

#     Need_to_check = objs.filter(
#         Alarm_Bucket="Need to check",
#         upload_date__in=last_day_of_weeks.values("last_day_of_week"),
#     ).count()

#     Service_affecting_alarm = objs.filter(
#         Alarm_Bucket="Service affecting alarm",
#         upload_date__in=last_day_of_weeks.values("last_day_of_week"),
#     ).count()

#     Sites_Locked_Down_Ping_Not_OK_Upload_Failed_Login_Failed = objs.filter(
#         Alarm_Bucket="Sites Locked/Down/Ping Not OK/Upload Failed/Login Failed",
#         upload_date__in=last_day_of_weeks.values("last_day_of_week"),
#     ).count()

#     Sync_Issue_GPS_TOP = objs.filter(
#         Alarm_Bucket="Sync Issue - GPS/TOP",
#         upload_date__in=last_day_of_weeks.values("last_day_of_week"),
#     ).count()

#     TWAMP_Issue = objs.filter(
#         Alarm_Bucket="TWAMP Issue",
#         upload_date__in=last_day_of_weeks.values("last_day_of_week"),
#     ).count()

#     UBR_AT_Dependency = objs.filter(
#         Alarm_Bucket__in=[x for x in ["UBR AT Dependency", "Media issue"]],
#         upload_date__in=last_day_of_weeks.values("last_day_of_week"),
#     ).count()

#     VSWR_High_Config_Issue = objs.filter(
#         Alarm_Bucket="VSWR High/Config Issue",
#         upload_date__in=last_day_of_weeks.values("last_day_of_week"),
#     ).count()

#     total = (
#         Configuration_issue
#         + GTPU_Trxmn_S1_Link_Alarm
#         + HW_Alarms
#         + Need_to_check
#         + Service_affecting_alarm
#         + Sites_Locked_Down_Ping_Not_OK_Upload_Failed_Login_Failed
#         + Sync_Issue_GPS_TOP
#         + TWAMP_Issue
#         + UBR_AT_Dependency
#         + VSWR_High_Config_Issue
#     )

#     alarm_bucketization = {}

#     alarm_bucketization["Configuration issue"] = {
#         "Count_of_Alarm_Bucket": Configuration_issue
#     }
#     alarm_bucketization["GTPU/Trxmn/S1 Link Alarm"] = {
#         "Count_of_Alarm_Bucket": GTPU_Trxmn_S1_Link_Alarm
#     }
#     alarm_bucketization["HW Alarms"] = {"Count_of_Alarm_Bucket": HW_Alarms}
#     alarm_bucketization["Need to check"] = {"Count_of_Alarm_Bucket": Need_to_check}

#     alarm_bucketization["Service affecting alarm"] = {
#         "Count_of_Alarm_Bucket": Service_affecting_alarm
#     }
#     alarm_bucketization["Sites Locked/Down/Ping Not OK/Upload Failed/Login Failed"] = {
#         "Count_of_Alarm_Bucket": Sites_Locked_Down_Ping_Not_OK_Upload_Failed_Login_Failed
#     }
#     alarm_bucketization["Sync Issue - GPS/TOP"] = {
#         "Count_of_Alarm_Bucket": Sync_Issue_GPS_TOP
#     }
#     alarm_bucketization["TWAMP Issue"] = {"Count_of_Alarm_Bucket": TWAMP_Issue}
#     alarm_bucketization["VSWR High/Config Issue"] = {
#         "Count_of_Alarm_Bucket": VSWR_High_Config_Issue
#     }

#     alarm_bucketization["UBR AT Dependency"] = {
#         "Count_of_Alarm_Bucket": UBR_AT_Dependency
#     }
#     alarm_bucketization["Grand Total"] = {"Count_of_Alarm_Bucket": total}

#     return alarm_bucketization


# def pending_ageing_week(objs):
#     circles = circle_list(objs)
#     ageing_circleWise = {}

#     for circle in circles:
#         obj = objs.filter(CIRCLE=circle)

#         # Retrieve the last day of the week for each week
#         last_day_of_weeks = (
#             obj.annotate(week=TruncWeek("upload_date"))
#             .values("week")
#             .annotate(last_day_of_week=Max("upload_date"))
#         )

#         ageing_0_15 = obj.filter(
#             Status__in=["Pending"],
#             Internal_Ms1_Vs_Ms2_In_days="0-15",
#             upload_date__in=last_day_of_weeks.values("last_day_of_week"),
#         ).count()

#         ageing_16_30 = obj.filter(
#             Status__in=["Pending"],
#             Internal_Ms1_Vs_Ms2_In_days="16-30",
#             upload_date__in=last_day_of_weeks.values("last_day_of_week"),
#         ).count()

#         ageing_31_60 = obj.filter(
#             Status__in=["Pending"],
#             Internal_Ms1_Vs_Ms2_In_days="31-60",
#             upload_date__in=last_day_of_weeks.values("last_day_of_week"),
#         ).count()

#         ageing_61_90 = obj.filter(
#             Status__in=["Pending"],
#             Internal_Ms1_Vs_Ms2_In_days="61-90",
#             upload_date__in=last_day_of_weeks.values("last_day_of_week"),
#         ).count()

#         ageing_GT90 = obj.filter(
#             Status__in=["Pending"],
#             Internal_Ms1_Vs_Ms2_In_days__in=["GT90", "91-120"],
#             upload_date__in=last_day_of_weeks.values("last_day_of_week"),
#         ).count()

#         ageing_GT120 = obj.filter(
#             Status__in=["Pending"],
#             Internal_Ms1_Vs_Ms2_In_days="GT120",
#             upload_date__in=last_day_of_weeks.values("last_day_of_week"),
#         ).count()

#         ageing_circleWise[circle] = {
#             "ageing_0_15": ageing_0_15,
#             "ageing_16_30": ageing_16_30,
#             "ageing_31_60": ageing_31_60,
#             "ageing_61_90": ageing_61_90,
#             "ageing_GT90": ageing_GT90,
#             "ageing_GT120": ageing_GT120,
#         }

#     # Check if ageing_circleWise is not empty before calling df_raw_column_total
#     if ageing_circleWise:
#         ageing_circleWise_data = df_raw_column_total(ageing_circleWise)
#         #print("ageing_circle_data..............", ageing_circleWise_data)
#         return ageing_circleWise_data
#     else:
#         # Handle the case when ageing_circleWise is empty
#         #print("ageing_circleWise is empty")
#         return {}

 
@api_view(["GET", "POST"])
def SoftAt_Circlewise_Dashboard(request):
    #print("Current_User---------------", request.user)
    str_Date = request.POST.get("Date")
    month = request.POST.get("month")
    week = request.POST.get("week")
    year = request.POST.get("year")
    str_from_date = request.POST.get("from_date")
    str_to_date = request.POST.get("to_date")
    Project = request.POST.get("project")
    Projects = Project.split(",")
    
    objs =Soft_At_Table.objects.all()
    circles = circle_list(objs)
    #print("Circle_list: ", circles)
    data = {}
    if year != "":
         year = int(year)
    # unique_alarm_bucket = list(Soft_At_Table.objects.exclude(Alarm_Bucket = "NAN").values_list("Alarm_Bucket", flat=True).distinct())
    for circle in circles:
        if Project != "":
            obj = Soft_At_Table.objects.filter(
                CIRCLE=circle, Activity_Name__in=Projects, soft_delete=False
            )
        else:
            obj = Soft_At_Table.objects.filter(CIRCLE=circle, soft_delete=False)
            
        if str_Date != "":
            #print("___________Inside Date___________")
            Date = datetime.strptime(str_Date, "%Y-%m-%d").date()
            #print(Date)
            Accepted = obj.filter(soft_at_status__iexact="Accepted", upload_date=Date).count()
            Dismantle = obj.filter(soft_at_status__iexact="Dismantle", upload_date=Date).count()
            offered = obj.filter(soft_at_status__iexact="Offered", upload_date=Date).count()
            Rejected = obj.filter(soft_at_status__iexact="Rejected", upload_date=Date).count()
            NOT_OFFERED = obj.filter(soft_at_status__iexact="NOT OFFERED", upload_date=Date).count()
            Need_to_be_offer = obj.filter(
                soft_at_status__iexact="Need to be offer", upload_date=Date
            ).count()
            Pending = obj.filter(soft_at_status__iexact="Pending", upload_date=Date).count()

        elif month != "":

            #print("___________Inside Month___________")
            #print(month)

            Accepted = obj.filter(
                soft_at_status__iexact="Accepted",
                upload_date__month=month,
                upload_date__year=year,
            ).count()
            Rejected = obj.filter(
                soft_at_status__iexact="Rejected",
                upload_date__month=month,
                upload_date__year=year,
            ).count()

            month_obj = obj.filter(upload_date__month=month, upload_date__year=year)

            if len(month_obj) != 0:
                obj = month_obj.filter(
                    upload_date=month_obj.latest("upload_date").upload_date
                )

                Dismantle = obj.filter(soft_at_status__iexact="Dismantle").count()
                offered = obj.filter(soft_at_status__iexact="Offered").count()
                # Rejected=month_obj.filter(Status__iexact="Rejected").count()
                Need_to_be_offer = obj.filter(soft_at_status__iexact="Need to be offer").count()
                NOT_OFFERED = obj.filter(soft_at_status__iexact="NOT OFFERED").count()
                Pending = obj.filter(soft_at_status__iexact="Pending").count()
            else:
                Dismantle = 0
                offered = 0
                Rejected = 0
                Need_to_be_offer = 0
                Pending = 0

        elif week != "":

            #print("___________Inside week___________")
            week = int(week)
            Accepted = obj.filter(
                soft_at_status__iexact="Accepted",
                upload_date__week=week,
                upload_date__year=year,
            ).count()
            week_obj = obj.filter(upload_date__week=week, upload_date__year=year)
            if len(week_obj) != 0:

                obj = week_obj.filter(
                    upload_date=week_obj.latest("upload_date").upload_date
                )
                Dismantle = obj.filter(soft_at_status__iexact="Dismantle").count()
                offered = obj.filter(soft_at_status__iexact="Offered").count()
                Rejected = week_obj.filter(soft_at_status__iexact="Rejected").count()
                Need_to_be_offer = obj.filter(soft_at_status__iexact="Need to be offer").count()
                Pending = obj.filter(soft_at_status__iexact="Pending").count()
                NOT_OFFERED = obj.filter(soft_at_status__iexact="NOT OFFERED").count()
            else:
                Dismantle = 0
                offered = 0
                Rejected = 0
                NOT_OFFERED = 0
                Need_to_be_offer = 0
                Pending = 0
        elif str_from_date != "" and str_to_date != "":
            #print("___________Inside from and to ___________")
            from_date = datetime.strptime(str_from_date, "%Y-%m-%d").date()
            to_date = datetime.strptime(str_to_date, "%Y-%m-%d").date()
            #print("from_date", from_date)
            #print("to_date", to_date)
            # Get the latest date within the given range
            latest_date_within_range = obj.filter(
                upload_date__range=(from_date, to_date)
            ).aggregate(Max("upload_date"))["upload_date__max"]

            # Filter the data for the latest date within the range
            Accepted = obj.filter(
                soft_at_status__iexact="Accepted", upload_date__range=(from_date, to_date)
            ).count()
            Dismantle = obj.filter(
                soft_at_status__iexact="Dismantle", upload_date=latest_date_within_range
            ).count()
            offered = obj.filter(
                soft_at_status__iexact="Offered", upload_date=latest_date_within_range
            ).count()
            Rejected = obj.filter(soft_at_status__iexact="Rejected", upload_date=latest_date_within_range).count()
            Need_to_be_offer = obj.filter(
                soft_at_status__iexact="Need to be offer", upload_date=latest_date_within_range
            ).count()
            NOT_OFFERED = obj.filter(
                soft_at_status__iexact="NOT OFFERED", upload_date=latest_date_within_range
            ).count()
            Pending = obj.filter(
                soft_at_status__iexact="Pending", upload_date=latest_date_within_range
            ).count()

        else:
            # #print("onj_______", obj)
            #print("_________________Inside All_______________")
            # obj=Soft_At_Table.objects.filter(IntegrationData__CIRCLE__iexact=circle)
            Accepted = obj.filter(soft_at_status__iexact="Accepted").count()
            Dismantle = obj.filter(
                soft_at_status__iexact="Dismantle",
                upload_date=Soft_At_Table.objects.latest("upload_date").upload_date,

            ).count()
            # Dismantle=obj.filter(Status__iexact="Dismantle").count()
            offered = obj.filter(
                soft_at_status__iexact="Offered",
                upload_date=Soft_At_Table.objects.latest("upload_date").upload_date,

            ).count()
            # offered=obj.filter(Status__iexact="Offered").count()
            Rejected = obj.filter(
                soft_at_status__iexact="Rejected",
                upload_date=Soft_At_Table.objects.latest("upload_date").upload_date,

            ).count()
            # Rejected=obj.filter(Status__iexact="Rejected").count()
            # Need_to_be_offer=obj.filter(Status__iexact="Need to be offer",upload_date=Soft_At_Table.objects.latest('upload_date').upload_date).count()
            Need_to_be_offer=obj.filter(soft_at_status__iexact="Need to be offer",upload_date=Soft_At_Table.objects.latest('upload_date').upload_date).count()
            NOT_OFFERED=obj.filter(soft_at_status__iexact="NOT OFFERED",upload_date=Soft_At_Table.objects.latest('upload_date').upload_date).count()
            # Need_to_be_offer = 0
            Pending = obj.filter(
                soft_at_status__iexact="Pending",
                upload_date=Soft_At_Table.objects.latest("upload_date").upload_date,
                # upload_date=Soft_At_Table.objects.latest("upload_date").upload_date,
            ).count()
            # Pending=obj.filter(Status__iexact= "Pending").count()
            No_At_Required = obj.filter(
                soft_at_status__iexact="No At Required",
                upload_date=Soft_At_Table.objects.latest("upload_date").upload_date,
            ).count()
        total = Accepted + Dismantle + offered + Rejected + Need_to_be_offer + Pending + NOT_OFFERED + No_At_Required
        #print(circle, total)
        if total != 0:
            Acceptance_percent = round(Accepted / total, 2)
            Rejection_percent = round(Rejected / total, 2)
        else:
            Acceptance_percent = 0
            Rejection_percent = 0
            
        data[circle] = {
            "Accepted": Accepted,
            "Dismantle": Dismantle,
            "Offered": offered,
            "Rejected": Rejected,
            "Pending": Pending,
            "NOT_OFFERED": NOT_OFFERED,
            "Need_to_be_offer": Need_to_be_offer,
            "No_At_Required": No_At_Required,
            "Accepted_per": Acceptance_percent,
            "Rejection_per": Rejection_percent,
        }
    if len(data) != 0:
        data1 = df_raw_column_total_circle_wise(data)
    else:
        return Response({"status": False, "message": "Database is empty"})

    ######################################### code for filtering of pending_sites/ alarm_bucket / ageing Circle_wise ########################################

    if Project != "":
        main_obj = Soft_At_Table.objects.filter(Activity_Name__in =Projects)
    else:
        main_obj = Soft_At_Table.objects.all()
    if str_Date != "":
        Date = datetime.strptime(str_Date, "%Y-%m-%d").date()
        #print(Date)
        Date_objs = main_obj.filter(upload_date=Date)
        #print(Date_objs)
        pending_sites_bucketization_data = pending_sites_bucketization(Date_objs)
        alarm_bucketization_data = Alarm_Bucket(Date_objs)
        # alarm_bucketization_data_all = Alarm_Bucket_all_data(Date_objs)
        ageing_circleWise_data = pending_ageing(Date_objs)

    elif month != "":
        #print(month)
        last_report = objs.filter(
            upload_date__month=month, upload_date__year=year, soft_at_status="Pending"
        ).aggregate(latest_date=Max("upload_date"))["latest_date"]

        if last_report:
            last_day_of_month = last_report.day
            month_objs = objs.filter(
                upload_date__day=last_day_of_month,
                upload_date__month=month,
                upload_date__year=year,
                soft_at_status="Pending",
            )

            #print(month_objs.count())
            pending_sites_bucketization_data = pending_sites_bucketization(month_objs)
            # alarm_bucketization_data = Alarm_Bucket_New(month_objs)
            alarm_bucketization_data = Alarm_Bucket(month_objs)
            # alarm_bucketization_data_all = Alarm_Bucket_all_data(month_objs, unique_alarm_bucket)
            ageing_circleWise_data = pending_ageing(month_objs)
        else:
            # No reports found for the specified month, year, and status "Pending"
            #print("No reports found for the specified month, year, and status 'Pending'")
            pass

    elif week != "":

        week = int(week)
        # week_objs=obj.filter(upload_date__week=week,upload_date__year=year).filter(upload_date=Soft_At_Table.objects.latest('upload_date').upload_date)
        week_objs = main_obj.annotate(week=TruncWeek("upload_date")).filter(
            week__week=week, week__year=year
        )
        #print(week_objs)
        # pending_sites_bucketization_data = pending_sites_bucketization_week(week_objs)
        pending_sites_bucketization_data = pending_sites_bucketization(week_objs)
        # alarm_bucketization_data = Alarm_Bucket_New(week_objs)
        alarm_bucketization_data = Alarm_Bucket(week_objs)
        # alarm_bucketization_data_all = Alarm_Bucket_all_data(week_objs, unique_alarm_bucket)
        ageing_circleWise_data = pending_ageing(week_objs)
    elif str_from_date != "" and str_to_date != "":
        #print("___________Inside from and to ___________")
        from_date = datetime.strptime(str_from_date, "%Y-%m-%d").date()
        to_date = datetime.strptime(str_to_date, "%Y-%m-%d").date()
        #print("from_date", from_date)
        #print("to_date", to_date)

        latest_obj_within_range = objs.filter(
            soft_at_status__iexact="Pending", upload_date__range=(from_date, to_date)
        ).latest("upload_date")

        if latest_obj_within_range:
            #print("latest_date_within_range", latest_obj_within_range.upload_date)
            range_objs = objs.filter(
                soft_at_status__iexact="Pending",
                upload_date=latest_obj_within_range.upload_date,
            )
            #print("range_obj______________", range_objs.count())
            pending_sites_bucketization_data = pending_sites_bucketization(range_objs)
            alarm_bucketization_data = Alarm_Bucket(range_objs)
            # alarm_bucketization_data_all = Alarm_Bucket_all_data(range_objs, unique_alarm_bucket)
            # alarm_bucketization_data = Alarm_Bucket(range_objs)
            ageing_circleWise_data = pending_ageing(range_objs)
        else:
            # No objects found within the specified date range
            #print("No objects found within the specified date range.")
            pass

    else:
        overAll_objs = Soft_At_Table.objects.filter(upload_date=Soft_At_Table.objects.latest("upload_date").upload_date)
        pending_sites_bucketization_data = pending_sites_bucketization(overAll_objs)
        # alarm_bucketization_data = Alarm_Bucket_New(overAll_objs)
        alarm_bucketization_data = Alarm_Bucket(overAll_objs)
        # alarm_bucketization_data_all = Alarm_Bucket_all_data(overAll_objs, unique_alarm_bucket)
        ageing_circleWise_data = pending_ageing(overAll_objs)
        # hyperlink_alarm_bucket = Alarm_Bucket_New(overAll_objs)
        pass
    Latest_date = Soft_At_Table.objects.latest("upload_date").upload_date
    return Response(
        {
            "status": True,
            "Data": data1,
            "pending_sites_bucketization": pending_sites_bucketization_data,
            "alarm_bucketization": alarm_bucketization_data,
            # "hyperlink_for_alarm": alarm_bucketization_data_all,
            "ageing_circleWise": ageing_circleWise_data,
            "Latest_date": Latest_date,
        }
    )


# @api_view(["GET", "POST"])
# def SoftAt_Circlewise_Dashboard(request):
#     #print("Current_User---------------", request.user)

#     str_Date = request.POST.get("Date")
#     month = request.POST.get("month")
#     week = request.POST.get("week")
#     year = int(request.POST.get("year"))
#     str_from_date = request.POST.get("from_date")
#     str_to_date = request.POST.get("to_date")
#     Project = request.POST.get("circle_project")
#     Projects = request.POST.get(Project, "").split(",")

#     #print("date", str_Date)
#     #print("month", month)
#     #print("week", week)
#     #print("year", year)
#     #print("date from ", str_from_date, "to ", str_to_date)
#     #print("project", Project)
#     #print("projects  ", Projects)

#     objs = Soft_At_Table.objects.all()
#     circles = circle_list(objs)
#     #print("Circle_list: ", circles)

#     data = {}

#     main_obj = (
#         Soft_At_Table.objects.filter(Circle_Project__in=Projects)
#         if Project
#         else Soft_At_Table.objects.all()
#     )
#     #print("main_obj.............", main_obj)
#     for circle in circles:
#         #print("for loop entering....")
#         obj = (
#             objs.filter(CIRCLE=circle, Circle_Project__in=Projects)
#             if Project
#             else objs.filter(CIRCLE=circle)
#         )

#         counts = None

#         if str_Date:
#             Date = datetime.datetime.strptime(str_Date, "%Y-%m-%d").date()
#             counts = obj.filter(upload_date= Date).aggregate(
#                 accepted_count=Count("id", filter=Q(Status__iexact="Accepted")),
#                 dismantle_count=Count("id", filter=Q(Status__iexact="Dismantle")),
#                 offered_count=Count("id", filter=Q(Status__iexact="Offered")),
#                 rejected_count=Count("id", filter=Q(Status__iexact="Rejected")),
#                 need_to_be_offer_count=Count(
#                     "id", filter=Q(Status__iexact="Need to be offer")
#                 ),
#                 pending_count=Count("id", filter=Q(Status__iexact="Pending")),
#             )

#             # #print("coutns data value......",counts)
#             process_counts(counts)

#         elif month:
#             # #print("entering month ............")
#             # try:
#             #     # Attempt to convert month to an integer
#             #     month = int(month)
#             # except ValueError:
#             #     return Response({"status": False, "message": "Invalid month value"})

#             # month_objs = main_obj.annotate(month=TruncMonth("upload_date")).filter(
#             #     month__month=month, month__year=year
#             # )
#             # #print(month_objs)
#             # process_date_or_week_obj(month_objs)

#             # Date = datetime.datetime.strptime(str_Date, "%Y-%m-%d").date()
#             counts = obj.annotate(month=TruncMonth("upload_date")).filter(upload_date__month = month).aggregate(
#                 accepted_count=Count("id", filter=Q(Status__iexact="Accepted")),
#                 dismantle_count=Count("id", filter=Q(Status__iexact="Dismantle")),
#                 offered_count=Count("id", filter=Q(Status__iexact="Offered")),
#                 rejected_count=Count("id", filter=Q(Status__iexact="Rejected")),
#                 need_to_be_offer_count=Count(
#                     "id", filter=Q(Status__iexact="Need to be offer")
#                 ),
#                 pending_count=Count("id", filter=Q(Status__iexact="Pending")),
#             )

#             # #print("coutns data value......",counts)
#             process_counts(counts)

#         elif week:
#             week = int(week)
#             week_obj = obj.annotate(week=TruncWeek("upload_date")).filter(
#                 week__week=week, week__year=year
#             )

#             #print("Please check the ______________________________________________",week_obj)
#             process_date_or_week_obj(week_obj)

#         elif str_from_date and str_to_date:
#             from_date = datetime.datetime.strptime(str_from_date, "%Y-%m-%d").date()
#             to_date = datetime.datetime.strptime(str_to_date, "%Y-%m-%d").date()
#             counts = obj.filter(upload_date__range=(from_date, to_date)).aggregate(
#                 accepted_count=Count("id", filter=Q(Status__iexact="Accepted")),
#                 dismantle_count=Count("id", filter=Q(Status__iexact="Dismantle")),
#                 offered_count=Count("id", filter=Q(Status__iexact="Offered")),
#                 rejected_count=Count("id", filter=Q(Status__iexact="Rejected")),
#                 need_to_be_offer_count=Count(
#                     "id", filter=Q(Status__iexact="Need to be offer")
#                 ),
#                 pending_count=Count("id", filter=Q(Status__iexact="Pending")),
#             )
#             process_counts(counts)

#         else:
#             counts = obj.aggregate(
#                 accepted_count=Count("id", filter=Q(Status__iexact="Accepted")),
#                 dismantle_count=Count("id", filter=Q(Status__iexact="Dismantle")),
#                 offered_count=Count("id", filter=Q(Status__iexact="Offered")),
#                 rejected_count=Count("id", filter=Q(Status__iexact="Rejected")),
#                 need_to_be_offer_count=Count(
#                     "id", filter=Q(Status__iexact="Need to be offer")
#                 ),
#                 pending_count=Count("id", filter=Q(Status__iexact="Pending")),
#             )
#             process_counts(counts)

#         if counts:
#             total = sum(counts.values())
#             data[circle] = calculate_percentages(counts, total)
#             #print(data)

#     if data:
#         data1 = df_raw_column_total_circle_wise(data)
#     else:
#         return Response({"status": False, "message": "Database is empty"})

#     # Code for filtering of pending_sites/ alarm_bucket / ageing Circle_wise

#     objs = get_objects_by_date_week_month_range(
#         main_obj, str_Date, month, week, year, str_from_date, str_to_date
#     )

#     pending_sites_bucketization_data = pending_sites_bucketization(objs)
#     alarm_bucketization_data = Alarm_Bucket(objs)
#     ageing_circleWise_data = pending_ageing(objs)

#     Latest_date = Soft_At_Table.objects.latest("upload_date").upload_date
#     return Response(
#         {
#             "status": True,
#             "Data": data1,
#             "pending_sites_bucketization": pending_sites_bucketization_data,
#             "alarm_bucketization": alarm_bucketization_data,
#             "ageing_circleWise": ageing_circleWise_data,
#             "Latest_date": Latest_date,
#         }
#     )


def process_counts(counts):

    #print(counts)
    if counts:
        accepted_count = counts.get("accepted_count", 0)
        dismantle_count = counts.get("dismantle_count", 0)
        offered_count = counts.get("offered_count", 0)
        rejected_count = counts.get("rejected_count", 0)
        need_to_be_offer_count = counts.get("need_to_be_offer_count", 0)
        pending_count = counts.get("pending_count", 0)

        #print("Accepted Count:", accepted_count)
        #print("Dismantle Count:", dismantle_count)
        #print("Offered Count:", offered_count)
        #print("Rejected Count:", rejected_count)
        #print("Need to be Offer Count:", need_to_be_offer_count)
        #print("Pending Count:", pending_count)

        # Calculate percentages
        total = (
            accepted_count
            + dismantle_count
            + offered_count
            + rejected_count
            + need_to_be_offer_count
            + pending_count
        )


# ... (previous code)


def process_date_or_week_obj(date_or_week_obj):
    result = {}
    #print("entering the Process_date_or_week_obj____________________")
    if date_or_week_obj.exists():
        # Filter the queryset based on date or week
        date_or_week_obj = date_or_week_obj.order_by("-upload_date")

        # Print a subset of the queryset
        #print("Subset of date_or_week_obj:", date_or_week_obj[:10])

        #print("Before values:", date_or_week_obj.count())  # Check data existence
        counts = date_or_week_obj.filter(week=TruncWeek("upload_date")).aggregate(
            accepted_count=Count("id", filter=Q(Status__iexact="Accepted")),
            dismantle_count=Count("id", filter=Q(Status__iexact="Dismantle")),
            offered_count=Count("id", filter=Q(Status__iexact="Offered")),
            rejected_count=Count("id", filter=Q(Status__iexact="Rejected")),
            need_to_be_offer_count=Count(
                "id", filter=Q(Status__iexact="Need to be offer")
            ),
            pending_count=Count("id", filter=Q(Status__iexact="Pending")),
        )

        process_counts(counts)

        result["date_or_week_obj"] = date_or_week_obj  # Include the filtered queryset
        result["counts"] = counts  # Include the counts
    else:
        result["date_or_week_obj"] = date_or_week_obj
        result["counts"] = None

    #print("result______________,", result)

    return result


def calculate_percentages(counts, total):
    accepted_count = counts.get("accepted_count", 0)
    dismantle_count = counts.get("dismantle_count", 0)
    offered_count = counts.get("offered_count", 0)
    rejected_count = counts.get("rejected_count", 0)
    need_to_be_offer_count = counts.get("need_to_be_offer_count", 0)
    pending_count = counts.get("pending_count", 0)

    acceptance_percent = round(accepted_count / total, 2) if total != 0 else 0
    rejection_percent = round(rejected_count / total, 2) if total != 0 else 0

    return {
        "Accepted": accepted_count,
        "Dismantle": dismantle_count,
        "Offered": offered_count,
        "Rejected": rejected_count,
        "Pending": pending_count,
        "Need_to_be_offer": need_to_be_offer_count,
        "Accepted_per": acceptance_percent,
        "Rejection_per": rejection_percent,
    }


def get_objects_by_date_week_month_range(
    main_obj, str_Date, month, week, year, str_from_date, str_to_date
):
    if str_Date:
        Date = datetime.datetime.strptime(str_Date, "%Y-%m-%d").date()
        return main_obj.filter(upload_date=Date)
    elif month:
        month_objs = main_obj.annotate(month=TruncMonth("upload_date")).filter(
            month__month=month, month__year=year
        )
        return process_date_or_week_obj(month_objs)
    elif week:
        week = int(week)
        week_objs = main_obj.annotate(week=TruncWeek("upload_date")).filter(
            week__week=week, week__year=year
        )
        return process_date_or_week_obj(week_objs)
    elif str_from_date and str_to_date:
        from_date = datetime.datetime.strptime(str_from_date, "%Y-%m-%d").date()
        to_date = datetime.datetime.strptime(str_to_date, "%Y-%m-%d").date()
        return main_obj.filter(upload_date__range=(from_date, to_date))
    else:
        return main_obj


@api_view(["GET"])
def View_Soft_At_Report(request):
    #print("Current_User---------------", request.user)
    objs = Soft_At_Table.objects.all()
    path = "media/Soft_AT/Soft_At_Reports/OverAllSoftAtRreport.xlsx"
    pd.DataFrame(list(objs.values())).to_excel(path, index=False)
    ser = ser_Soft_At_Table(objs, many=True)

    upload_date_array = Soft_At_Table.objects.values_list(
        "upload_date", flat=True
    ).distinct()

    upload_date_array = list(upload_date_array)

    upload_date_array.sort()
    #print(upload_date_array)
    return Response(
        {
            "status": True,
            "data": ser.data,
            "Download_url": path,
            "upload_date": upload_date_array,
        }
    )


@api_view(["POST"])
def weeklyComparision(request):
    #print("Current_User---------------", request.user)

    # Get the current date
    current_date = datetime.now().date()
    current_year, current_week, _ = current_date.isocalendar()

    # Get the year and week from the request if available, otherwise use current year and week
    year = request.POST.get("year", current_year)
    week = request.POST.get("week", current_week)

    #print("Weekly comparison week:", week)
    week = int(week)

    objs = Soft_At_Table.objects.all()
    current_week_Accepted = objs.filter(
        Q(Status__iexact="Accepted")
        & Q(upload_date__week=week)
        & Q(upload_date__year=year)
    ).count()

    #print("Check issue:", current_week_Accepted)
    previous_week = week - 1

    # Code for pending sites in the current week
    week_obj = objs.filter(upload_date__week=week, upload_date__year=year)
    if week_obj.exists():
        obj = week_obj.filter(upload_date=week_obj.latest("upload_date").upload_date)
        Pendency_of_current_week = obj.filter(Status__iexact="Pending").count()
    else:
        Pendency_of_current_week = 0

    # Code for the pending sites in the previous week
    week_obj = objs.filter(upload_date__week=previous_week, upload_date__year=year)
    if week_obj.exists():
        obj = week_obj.filter(upload_date=week_obj.latest("upload_date").upload_date)
        Pendency_of_previous_week = obj.filter(Status__iexact="Pending").count()
    else:
        Pendency_of_previous_week = 0

    #print("Pendency of current week:", Pendency_of_current_week)
    #print("Pendency of previous week:", Pendency_of_previous_week)

    # Calculate pendency change percentage
    if Pendency_of_previous_week != 0:
        Pendency_change_per = round(
            (
                (Pendency_of_current_week - Pendency_of_previous_week)
                / Pendency_of_previous_week
            )
            * 100,
            2,
        )
    else:
        Pendency_change_per = 0

    pendency_comp_data = {
        "Pendency_change_per": Pendency_change_per,
        "Pendency_of_previous_week": Pendency_of_previous_week,
        "Pendency_of_current_week": Pendency_of_current_week,
    }

    # Code for top 3 circles with highest acceptance
    ############################## code for top 3 circles with highest acceptance ##################################################
    objs = Soft_At_Table.objects.all()
    circles = circle_list(objs)
    #print("Circle_list: ", circles)
    data = {}
    for circle in circles:
        obj = Soft_At_Table.objects.filter(CIRCLE=circle)
        Accepted = obj.filter(
            Status__iexact="Accepted", upload_date__week=week, upload_date__year=year
        ).count()

        data[circle] = Accepted

    # Sort the dictionary items by their values in descending order
    sorted_dict = sorted(data.items(), key=lambda x: x[1], reverse=True)

    # Get the top 3 values
    top_3_circles = sorted_dict[:3]
    #print(top_3_circles)

    ################################### code for top 3 circles on the basis of accepted percentage #####################################
    # Code for top 3 circles based on accepted percentage
    latest_upload_date = Soft_At_Table.objects.aggregate(
        latest_date=Max("upload_date")
    )["latest_date"]
    last_day_of_week = latest_upload_date - timedelta(days=latest_upload_date.weekday())

    # Code for percentage change in the highest ageing change
    previous_week_obj = Soft_At_Table.objects.filter(
        upload_date__week=previous_week, upload_date__year=year
    )
    previous_week_obj = Soft_At_Table.objects.filter(
        upload_date__week=previous_week, upload_date__year=year
    )
    #print("previous_week_obj__________________________", previous_week_obj)
    if len(previous_week_obj) != 0:
        obj = previous_week_obj.filter(
            upload_date=previous_week_obj.latest("upload_date").upload_date
        )
        ageing_0_15 = obj.filter(
            Status="Pending", Internal_Ms1_Vs_Ms2_In_days="0-15"
        ).count()
        ageing_16_30 = obj.filter(
            Status="Pending", Internal_Ms1_Vs_Ms2_In_days="16-30"
        ).count()
        ageing_31_60 = obj.filter(
            Status="Pending", Internal_Ms1_Vs_Ms2_In_days="31-60"
        ).count()
        ageing_61_90 = obj.filter(
            Status="Pending", Internal_Ms1_Vs_Ms2_In_days="61-90"
        ).count()
        ageing_GT90 = obj.filter(
            Status="Pending", Internal_Ms1_Vs_Ms2_In_days="GT90"
        ).count()
        ageing_GT120 = obj.filter(
            Status="Pending", Internal_Ms1_Vs_Ms2_In_days="GT120"
        ).count()
        previous_ageing_dict = {
            "ageing_0_15": ageing_0_15,
            "ageing_16_30": ageing_16_30,
            "ageing_31_60": ageing_31_60,
            "ageing_61_90": ageing_61_90,
            "ageing_GT90": ageing_GT90,
            "ageing_GT120": ageing_GT120,
        }

        #print("this is my dict.............", previous_ageing_dict)

        sorted_dict = sorted(
            previous_ageing_dict.items(), key=lambda x: x[1], reverse=True
        )

        # Get the top 3 values
        greates_ageing_previous_week = sorted_dict[:1][0][0]
        greates_ageing_previous_week_value = sorted_dict[:1][0][1]
        #print("greates_ageing_previous_week-------------------",greates_ageing_previous_week,)
    else:
        return Response(
            {"status": False, "message": f"No data of {previous_week} week is present "}
        )
    week_obj = objs.filter(upload_date__week=week, upload_date__year=year)
    if len(week_obj) != 0:
        obj = week_obj.filter(upload_date=week_obj.latest("upload_date").upload_date)
        ageing_0_15 = obj.filter(
            Status="Pending", Internal_Ms1_Vs_Ms2_In_days="0-15"
        ).count()
        ageing_16_30 = obj.filter(
            Status="Pending", Internal_Ms1_Vs_Ms2_In_days="16-30"
        ).count()
        ageing_31_60 = obj.filter(
            Status="Pending", Internal_Ms1_Vs_Ms2_In_days="31-60"
        ).count()
        ageing_61_90 = obj.filter(
            Status="Pending", Internal_Ms1_Vs_Ms2_In_days="61-90"
        ).count()
        ageing_GT90 = obj.filter(
            Status="Pending", Internal_Ms1_Vs_Ms2_In_days="GT90"
        ).count()
        ageing_GT120 = obj.filter(
            Status="Pending", Internal_Ms1_Vs_Ms2_In_days="GT120"
        ).count()
        current_ageing_dict = {
            "ageing_0_15": ageing_0_15,
            "ageing_16_30": ageing_16_30,
            "ageing_31_60": ageing_31_60,
            "ageing_61_90": ageing_61_90,
            "ageing_GT90": ageing_GT90,
            "ageing_GT120": ageing_GT120,
        }
        corresponding_current_ageing_value = current_ageing_dict[
            greates_ageing_previous_week
        ]
    else:
        return Response(
            {"status": False, "message": f"No data of {week} week is present "}
        )
    ageing_change_per = round(
        (
            (corresponding_current_ageing_value - greates_ageing_previous_week_value)
            / greates_ageing_previous_week_value
        )
        * 100,
        2,
    )

    ageing_comp_data = {
        "ageing_change_per": ageing_change_per,
        "greates_ageing_previous_week": greates_ageing_previous_week,
        "greates_ageing_previous_week_value": greates_ageing_previous_week_value,
        "corresponding_current_ageing_value": corresponding_current_ageing_value,
    }
    # Calculate percentage change in ageing

    # Code for pendency comparison graph
    weekly_pendency_graph = {}
    for circle in circles:
        circle_obj = Soft_At_Table.objects.filter(CIRCLE=circle)
        week_obj = circle_obj.filter(upload_date__week=week, upload_date__year=year)
        if week_obj.exists():
            obj = week_obj.filter(
                upload_date=week_obj.latest("upload_date").upload_date
            )
            current_week_pendency = obj.filter(Status__iexact="Pending").count()
        else:
            current_week_pendency = 0

        previous_week_obj = circle_obj.filter(
            upload_date__week=previous_week, upload_date__year=year
        )
        if previous_week_obj.exists():
            obj = previous_week_obj.filter(
                upload_date=previous_week_obj.latest("upload_date").upload_date
            )
            previous_week_pendency = obj.filter(Status__iexact="Pending").count()
        else:
            previous_week_pendency = 0

        weekly_pendency_graph[circle] = {
            "current_week_pendency": current_week_pendency,
            "previous_week_pendency": previous_week_pendency,
        }

    return Response(
        {
            "status": True,
            "Accepted": current_week_Accepted,
            "Pendency_comp_data": pendency_comp_data,
            "top_3_values": top_3_circles,
            "ageing_comp_data": ageing_comp_data,
            "weekly_pendency_graph": weekly_pendency_graph,
        }
    )


@api_view(["GET", "POST"])
def SoftAt_Aging_Count(request):
    week_start = request.GET.get("week_start")
    week_end = request.GET.get("week_end")

    # Implement logic to get ageing data for the specified weeks
    ageing_data = get_weekly_ageing_counts(week_start, week_end)

    #print(ageing_data)

    # Initialize a dictionary to store counts
    count_data = {}

    # Check if ageing_data is a QuerySet and convert it to a dictionary
    if isinstance(ageing_data, QuerySet):
        ageing_data = ageing_data.values()

    # Loop through each circle's aging data
    for entry in ageing_data:
        circle = entry.get("CIRCLE")  # Adjust field name as per your model
        start_age = entry.get("start_age", 0)
        end_age = entry.get("end_age", 0)

        # Count the occurrences of sites moving from under 30 to above 30
        if circle not in count_data:
            count_data[circle] = 0

        if start_age < 30 and end_age >= 30:
            count_data[circle] += 1

    # Include the counts in the response
    response_data = {
        "status": True,
        "weekly_ageing_counts": count_data,
    }

    return Response(response_data)


# views.py (continuation)


def get_weekly_ageing_counts(week_start, week_end):
    ageing_counts = (
        Soft_At_Table.objects.annotate(
            week=TruncWeek("upload_date"),
            ageing_change=ExpressionWrapper(
                Case(
                    When(Internal_Ms1_Vs_Ms2_In_days__gt=30, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                ),
                output_field=IntegerField(),
            ),
        )
        .filter(week__range=(week_start, week_end))
        .values("CIRCLE")
        .annotate(count_sites=F("ageing_change"))
    )

    #print(ageing_counts)

    return ageing_counts


@api_view(["GET", "POST"])
def week_wise_accepted_sites(request):
    # Week-wise count of all records
    week_counts_all = (
        Soft_At_Table.objects.annotate(week_all=TruncWeek("upload_date"))
        .values("week_all")
        .annotate(count=Count("id"))
        .order_by("week_all")
    )

    # Week-wise count of accepted records
    accepted_status_weekly = (
        Soft_At_Table.objects.filter(Status="Accepted")
        .annotate(week_accepted=TruncWeek("upload_date"))
        .values("week_accepted")
        .annotate(count=Count("id"))
        .order_by("week_accepted")
    )

    # Prepare the response data
    data = []
    for entry in accepted_status_weekly:
        data.append(
            {
                "week_number": entry["week_accepted"].isocalendar()[
                    1
                ],  # Get ISO week number
                "accepted_status_count": entry["count"],
            }
        )

    return Response(
        {
            "status": True,
            "message": "Week-wise accepted status count",
            "data": data,
            # "week_counts_all": week_counts_all,
        }
    )


@api_view(["GET"])
def ageing_wise_pending_sites(request):
    objs = Soft_At_Table.objects.all()

    # Calculate pending status for each week (based on the last day of the week)
    week_results = {}

    for week in range(1, 53):  # Assuming weeks range from 1 to 52
        week_objs = (
            objs.annotate(week=TruncWeek("upload_date"))
            .filter(week__week=week)
            .order_by("-upload_date")
        )  # Order by upload_date in descending order to get the last day of the week

        if week_objs.exists():
            last_day_of_week = week_objs[0].upload_date
            # Calculate pending status for Internal_Ms1_Vs_Ms2_In_days under 30 and above 30
            pending_under_30 = week_objs.filter(
                Status__iexact="Pending",
                Internal_Ms1_Vs_Ms2_In_days__lt=30,
                upload_date=last_day_of_week,
            ).count()

            pending_above_30 = week_objs.filter(
                Status__iexact="Pending",
                Internal_Ms1_Vs_Ms2_In_days__gte=30,
                upload_date=last_day_of_week,
            ).count()

            week_results[f"Week {week}"] = {
                "Pending_Under_30": pending_under_30,
                "Pending_Above_30": pending_above_30,
            }
        # else:
        #     week_results[f"Week {week}"] = {"Pending_Under_30": 0, "Pending_Above_30": 0}

    return Response({"status": True, "data": week_results})


@api_view(["GET"])
def overallAcceptedRejected(request):
    latest_date = Soft_At_Table.objects.aggregate(latest_date=Max("upload_date"))[
        "latest_date"
    ]

    if latest_date:
        accepted_count = Soft_At_Table.objects.filter(
            Status__iexact="Accepted", upload_date__lte=latest_date
        ).count()
        dismantle_count = Soft_At_Table.objects.filter(
            Status__iexact="Dismantle", upload_date=latest_date
        ).count()
        offered_count = Soft_At_Table.objects.filter(
            Status__iexact="Offered", upload_date=latest_date
        ).count()
        rejected_count = Soft_At_Table.objects.filter(
            Status__iexact="Rejected", upload_date=latest_date
        ).count()
        need_to_be_offer_count = Soft_At_Table.objects.filter(
            Status__iexact="Need to be offer", upload_date=latest_date
        ).count()
        pending_count = Soft_At_Table.objects.filter(
            Status__iexact="Pending", upload_date=latest_date
        ).count()

        total_count = (
            accepted_count
            + dismantle_count
            + offered_count
            + rejected_count
            + need_to_be_offer_count
            + pending_count
        )

        accepted_percentage = round(((accepted_count / total_count) * 100), 2)
        rejected_percentage = round((((rejected_count) / total_count) * 100), 2)
        pending_percentage = round((((pending_count) / total_count) * 100), 2)

        return Response(
            {
                "Status": True,
                "message": "Successfully Fetched data from database......",
                "data": [
                    {
                        "latest_date": latest_date,
                        "accepted_count": accepted_count,
                        # "dismantle_count": dismantle_count,
                        # "offered_count": offered_count,
                        # "pending_rejected_count": rejected_count+pending_count,
                        "rejected_count": rejected_count,
                        # "need_to_be_offer_count": need_to_be_offer_count,
                        "pending_count": pending_count,
                        "total_count": total_count,
                        "accepted_percentage": accepted_percentage,
                        "pending_percentage": pending_percentage,
                        "rejected_percentage": rejected_percentage,
                    }
                ],
            }
        )
    else:
        return Response(
            {"status": False, "message": "No data found for the latest date."}
        )


@api_view(["GET", "POST"])
def week_ageing_wise_accepted_pending_sites(request):
    transitioning_sites = {}

    for week in range(1, 52):
        objs_week1 = Soft_At_Table.objects.annotate(
            week=TruncWeek("upload_date")
        ).filter(week__week=week, Internal_Ms1_Vs_Ms2_In_days__lt=30)

        # Check if there are any objects for week + 1
        objs_week2_count = (
            Soft_At_Table.objects.annotate(week=TruncWeek("upload_date"))
            .filter(week__week=week + 1, Internal_Ms1_Vs_Ms2_In_days__gte=30)
            .count()
        )

        if objs_week1.exists() and objs_week2_count > 0:
            objs_week2 = Soft_At_Table.objects.annotate(
                week=TruncWeek("upload_date")
            ).filter(week__week=week + 1, Internal_Ms1_Vs_Ms2_In_days__gte=30)
            objs_week2 = objs_week2.values_list("SITE_ID", flat=True)
            accepted_count = objs_week2.filter(Status="Accepted")
            count = len(set(objs_week2))

            transitioning_site_ids = list(
                set(objs_week1.values_list("SITE_ID", flat=True))
                & set(objs_week2.values_list("SITE_ID", flat=True))
            )

            week_2_added_new_site = count - len(transitioning_site_ids)

            transitioning_site_count = len(transitioning_site_ids)

            transitioning_sites[f"Week {week} to Week {week + 1}"] = {
                "transitioning_site_count": transitioning_site_count,
                "Week_2_added_site": week_2_added_new_site,
                "accepted_count": accepted_count.count(),
            }

    return Response({"status": True, "data": transitioning_sites})


# @api_view(["POST","GET"])
# def top_3_circle_status_count(request):
#     objs = Soft_At_Table.objects.all()
#     circles = circle_list(objs)
#     #print("Circle_list: ", circles)
#     data = {}
#     for circle in circles:
#         obj = Soft_At_Table.objects.filter(CIRCLE=circle)
#         Accepted = obj.filter(
#             Status__iexact="Accepted", upload_date__week=week, upload_date__year=year
#         ).count()

#         data[circle] = Accepted

#     # Sort the dictionary items by their values in descending order
#     sorted_dict = sorted(data.items(), key=lambda x: x[1], reverse=True)

#     # Get the top 3 values
#     top_3_circles = sorted_dict[:3]
#     #print(top_3_circles)

#     # Print the top 3 values
#     for key, value in top_3_circles:
#         #print(key, value)

from IntegrationTracker.models import IntegrationData
@api_view(['POST'])
def responsibility_pending_site(request):
        # Fetch the instance of Soft_At_Table and related IntegrationData using select_related
    model_two_instance = Soft_At_Table.objects.select_related('unique_key').all()
    
    #print(model_two_instance)
    
    # Process data as needed
    data = {
        # 'soft_at_data': model_two_instance.unique_key,
        'integration_data': model_two_instance.unique_key,
    }
    
    return Response(data, status=200)







import xlwings as xw
def get_excel_template():
    template_path = os.path.join(MEDIA_ROOT,'Soft_AT','Templates','SoftAt_status_upload_template.xlsx')
    wb = xw.Book(template_path)
    return wb

@api_view(['GET'])
def get_soft_at_status_blank_template(request):
    # path = os.path.join(MEDIA_ROOT,'Soft_AT','Templates','SoftAt_status_upload_template.xlsx')
    ulr = os.path.join(MEDIA_URL,'Soft_AT','Templates','SoftAt_status_upload_template.xlsx')
    return Response({"Download_url":ulr}, status=200)


@api_view(['GET','POST'])
def softAt_status_upload_template_download(request):
    print(request.data)
    
    circle_oem_str = request.POST.get("circle_oem")
    try:
        circle_oem_dict = json.loads(circle_oem_str)
    except json.JSONDecodeError:
        circle_oem_dict = {}

    from_date = request.POST.get("from_date")
    to_date = request.POST.get("to_date")
    date = request.POST.get("date")
    site_ID = request.POST.get("site_id")

    if len(Soft_At_Table.objects.all()) > 0:
        latest_date=Soft_At_Table.objects.latest('upload_date').upload_date
    # latest_date=Soft_At_Table.objects.latest('upload_date').upload_date
    else:
        return Response({"status": False, "message": "No data found"}, status=400)
    # Start building the SQL query
    sql = 'SELECT * FROM public."SOFT_AT_VINAY_soft_at_table" WHERE "soft_at_status" != \'Accepted\' and "soft_delete" = \'False\' and "upload_date" = \'{}\' '.format(latest_date)
    conditions = []
    
    # Step 1: Filter by date using the "IntegrationData" field
    if from_date != '' and to_date != '':
        from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        conditions.append(f'"Integration_Date" BETWEEN \'{from_date}\' AND \'{to_date}\'')
    elif date != '':
        date = datetime.strptime(date, '%Y-%m-%d').date()
        conditions.append(f'"Integration_Date" = \'{date}\'')

    # Step 2: Filter by "CIRCLE" and "OEM"
    if circle_oem_dict != {}:
        circle_oem_conditions = []
        for circle, oems in circle_oem_dict.items():
            # Format OEMs as a string for the IN clause
            if len(oems) > 0:
                oem_list = ', '.join([f"'{oem.split()[0].upper()}'" for oem in oems])
                circle_oem_conditions.append(f'("CIRCLE" = \'{circle}\' AND "OEM" IN ({oem_list}))')
            else:
                circle_oem_conditions.append(f'("CIRCLE" = \'{circle}\')')
                
        
        if circle_oem_conditions:
            circle_oem_filter = " OR ".join(circle_oem_conditions)
            conditions.append(f"({circle_oem_filter})")

    # Step 3: Filter by "Site_ID"
    if site_ID != '':
        # Convert site_ID to a list if it's not already one
        if isinstance(site_ID, str):
            site_ID = [site_ID]  # If single value, convert to a list
        site_list= site_ID[0].strip().split(',')
        print(site_list)
        site_id_list = ', '.join([f"'{site_id}'" for site_id in site_list])
        conditions.append(f'"Site_ID" IN ({site_id_list})')

    # Join all conditions with ' AND '
    if conditions:
        sql += " AND "+ " AND ".join(conditions)
        sql = sql + ' union SELECT * FROM public."SOFT_AT_VINAY_soft_at_table" where "soft_at_status" = \'Accepted\'  and "soft_delete"=\'false\'and "upload_date" < \'{}\''.format(latest_date) + " AND "+ " AND ".join(conditions)
    else:
        print('this conditions are empty')
        sql = sql + ' union SELECT * FROM public."SOFT_AT_VINAY_soft_at_table" where "soft_at_status" = \'Accepted\' and "soft_delete"=\'false\''
    print(sql)
    # Execute the query using a cursor
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()  # Fetch all results

    columns=[tp[0]for tp in cursor.description]
    df=pd.DataFrame(rows,columns=columns)
    if df.empty:
        print("No data found")
        return Response({"message":'No data found'},status=status.HTTP_404_NOT_FOUND)
    database_columns = [
        # integrations columns
    'unique_key',                # Unique Key (Auto Generated)
    'OEM',                       # OEM
    'Integration_Date',          # Integration Date
    'CIRCLE',                    # CIRCLE
    'Activity_Name',             # Activity Name
    'Site_ID',                   # Site ID
    'MO_NAME',                   # MO NAME
    'LNBTS_ID',                  # LNBTS ID
    'Technology_SIWA',           # Technology (SIWA)
    'OSS_Details',               # OSS Details
    'Cell_ID',                   # Cell ID
    'CELL_COUNT',                # CELL COUNT
    'BSC_NAME',                  # BSC NAME
    'BCF',                       # BCF
    'TRX_Count',                 # TRX Count
    'PRE_ALARM',                 # PRE-ALARM
    'GPS_IP_CLK',                # GPS/IP CLK
    'RET',                       # RET
    'POST_VSWR',                 # POST-VSWR
    'POST_Alarms',               # POST Alarms
    'Activity_Mode',             # Activity Mode (SA/NSA)
    'Activity_Type_SIWA',        # Activity Type (SIWA)
    'Band_SIWA',                 # Band (SIWA)
    'CELL_STATUS',               # CELL STATUS
    'CTR_STATUS',                # CTR STATUS
    'Integration_Remark',        # Integration Remark
    'T2T4R',                     # 2T2R/4T4R
    'BBU_TYPE',                  # BBU TYPE
    'BB_CARD',                   # BB CARD
    'RRU_Type',                  # RRU Type
    'Media_Status',              # Media Status
    'Mplane_IP',                 # Mplane IP
    'SCF_PREPARED_BY',           # SCF PREPARED BY
    'SITE_INTEGRATE_BY',         # SITE INTEGRATE BY (Integrator Name)
    'Site_Status',               # Site Status
    'External_Alarm_Confirmation', # External Alarm Confirmation
    'SOFT_AT_STATUS',            # SOFT AT STATUS
    'LICENCE_Status',            # LICENCE Status
    'ESN_NO',                    # ESN NO
    'Responsibility_for_alarm_clearance', # Responsibility for alarm clearance
    'TAC',                       # TAC
    'PCI_TDD_20',                # PCI- TDD 20
    'PCI_TDD_10_20',             # PCI TDD 10/20
    'PCI_FDD_2100',              # PCI FDD 2100
    'PCI_FDD_1800',              # PCI FDD 1800
    'PCI_L900',                  # PCI L900
    'PCI_5G',                    # 5G PCI
    'RSI_TDD_20',                # RSI- TDD 20
    'RSI_TDD_10_20',             # RSI TDD 10/20
    'RSI_FDD_2100',              # RSI FDD 2100
    'RSI_FDD_1800',              # RSI FDD 1800
    'RSI_L900',                  # RSI L900
    'RSI_5G',                    # 5G RSI
    'GPL',                       # GPL
    'Pre_Post_Check',            # Pre/Post Check
    #soft at columns
    'spoc_name', 
    'offering_type', 
    'first_offering_date', 
    'soft_at_status',
    'offering_date', 
    'acceptance_rejection_date', 
    'alarm_bucket', 
    'alarm_details',
    'final_responsibility', 
    'workable_non_workable', 
    'ubr_ms2_status', 
    'ubr_link_id',
    'twamp_status', 
    'status_check_date', 
    'ageing_in_days', 
    'actual_ageing', 
    'toco_partner',
    'support_required_ubr_team', 
    'support_required_circle_team', 
    'support_required_noc_team',
    'category', 
    'problem_statement', 
    'final_remarks', 
    'ms1'
  ]

    ordered_columns_df = df[database_columns]
    # ordered_columns_df['Integration_Date'] = ordered_columns_df['Integration_Date'].astype(str)
    # ordered_columns_df['first_offering_date'] = ordered_columns_df['first_offering_date'].astype(str)
    # ordered_columns_df['offering_date'] = ordered_columns_df['offering_date'].astype(str)
    # ordered_columns_df['acceptance_rejection_date'] = ordered_columns_df['acceptance_rejection_date'].astype(str)
    # ordered_columns_df['status_check_date'] = ordered_columns_df['status_check_date'].astype(str)
    # ordered_columns_df.fillna("", inplace=True)
    # print(ordered_columns_df['Integration_Date'][0],type(ordered_columns_df['Integration_Date'][0]))
    # date_columns=['Integration_Date','first_offering_date','offering_date','acceptance_rejection_date','status_check_date']
    # ordered_columns_df[date_columns] = ordered_columns_df[date_columns].fillna('')
    # ordered_columns_df = ordered_columns_df.replace(['None', 'nan', 'NaN'], '')
    # print(ordered_columns_df[date_columns])
    json_data = ordered_columns_df.to_json(orient='records', date_format='iso')
    json_data = json.loads(json_data)
    return Response({'data':json_data }, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_integration_circle(request):
    circle =IntegrationData.objects.all().values_list('CIRCLE',flat=True).distinct()

    return Response({"message":'fetched sucessfully',"circle":circle})

########################################################### OFFERING TEMPLATES ###########################################################
# this function is user for the offering template
def fill_excel_template(df, template_path, mapping_dict, fixed_dict):
    # Load the Excel template
    wb = openpyxl.load_workbook(template_path)
    sheet = wb["Sheet1"]  # Replace with the actual sheet name

    # Write DataFrame to Excel starting from row 2 (assuming row 1 contains headers in the template)
    start_row = 2

    # Write DataFrame columns to the corresponding Excel columns
    for idx, row in df.iterrows():
        for df_col, excel_col in mapping_dict.items():
            excel_cell = f"{excel_col}{start_row + idx}"
            sheet[excel_cell] = row[df_col]

        # Fill fixed values in specific columns
        for excel_col, value in fixed_dict.items():
            excel_cell = f"{excel_col}{start_row + idx}"
            sheet[excel_cell] = value

    # Define a unique name for the saved file and its directory
    output_filename = 'filled_template.xlsx'
    output_dir = os.path.join(settings.MEDIA_ROOT, 'Soft_AT','Templates','filled_offering_templates')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)

    # Save the filled Excel file
    wb.save(output_path)
    wb.close()

    # Return the URL to access the file
    output_url = os.path.join(settings.MEDIA_URL, 'Soft_AT','Templates','filled_offering_templates', output_filename)
  
    return output_url



@api_view(['GET','POST'])
def softAT_offering_template_download(request):

    from_date=request.POST.get("from_date")
    to_date=request.POST.get("to_date")
    date=request.POST.get("date")
    circle=request.POST.get("circle")
    site_ID=request.POST.get("site_ID")
    oem = request.POST.get("oem")
    with connection.cursor() as cursor:
        if from_date != '' and to_date != '':
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date= datetime.strptime(to_date, '%Y-%m-%d').date()
            query= f"""select * from public."IntegrationTracker_integrationdata"
            where "Integration_Date" between '{from_date}' and '{to_date}' and "Activity_Name" in ('UPGRADE', 'RELOCATION', 'ULS_HPSC', 'MACRO', '5G SECTOR ADDITION') and "OEM"='{oem}' """ 

            if site_ID:
                query +=  """and "Site_ID" ='{site_ID}' """
            if circle:
                query +=  """and "CIRCLE" ='{circle}' """

        elif date !='':
            date=datetime.strptime(date, '%Y-%m-%d').date()
            query= f"""select * from public."IntegrationTracker_integrationdata"
            where "Integration_Date" = '{date}' and "Activity_Name" in ('UPGRADE', 'RELOCATION', 'ULS_HPSC', 'MACRO', '5G SECTOR ADDITION') and "OEM"='{oem}' """ 
            if site_ID:
                query +=  """and "Site_ID" ='{site_ID}' """
            if circle:
                query +=  """and "CIRCLE" ='{circle}' """
            
        else:
            pass

        cursor.execute(query)
        results = cursor.fetchall()
    columns=[tp[0]for tp in cursor.description]
    df=pd.DataFrame(results,columns=columns)
    #print(df)
    if oem == 'NOKIA':
        df['Reference_Id'] = df['CIRCLE'] +"_" + df['Site_ID'] + "_" + df['Technology_SIWA'] + "_" + df['Cell_ID']
        temp_path= os.path.join(MEDIA_ROOT,'Soft_AT','Templates','offering_templates','nokia.xlsx')
        mapping_dict={
                    'Reference_Id': 'A',
                    'CIRCLE': 'C',
                    'OEM': 'D',
                    'Site_ID': 'H',
                    'LNBTS_ID': 'I',
                    'Cell_ID': 'L',
                    'MO_NAME': 'M',
                    'OSS_Details': 'N',
                    'Technology_SIWA': 'P',
                    'Activity_Type_SIWA': 'Q',
                    'Band_SIWA': 'R',
                    'Activity_Type_SIWA': 'S',
                    'Integration_Date': 'T',
                    'Mplane_IP': 'V',
                    'BSC_NAME': 'Y',
                    'BCF': 'Z',
                    'TAC': 'AC'
                }
        fixed_dict={'E': 'Mobilecomm',
                    'G': 'Soft',
                    'K': 'NA',
                    'W': 'GPS',
                    'AO': 'Mobilecomm'}
        url=fill_excel_template(df, temp_path, mapping_dict, fixed_dict)

    elif oem == 'SAMSUNG':
        temp_path= os.path.join(MEDIA_ROOT,'Soft_AT','Templates','offering_templates','samsung.xlsx')  
        mapping_dict={
            "CIRCLE": "B",
            "OEM": "C",
            
            "Technology_SIWA": "J",
            "Band_SIWA": "K",
            "Activity_Type_SIWA": "J",
            "T2T4R": "BA",
            "Integration_Date": "L",
            "Integration_Date": "AL",
            "LNBTS_ID": "S",
            "CELL_COUNT": "X",
            "TAC": "AC",
            "BBU_TYPE": "AG",
            "OSS_Details": "R",
            "Mplane_IP": "P",
        }

        fixed_dict={
     "D":'Mobilecomm',
    "C": "SAMSUNG",
    "D": "Mobile COMM",
    "F": "SOFT AT 4G",
    "Q": "USM",
    "T": "NA",
    "V": "NA",
    "W": "NA",
    "Y": "NA",
    "Z": "YES",
    "AB": "YES",
    "AD": "Given in Separate sheet",
    "AE": "Given in Separate sheet",
    "AF": "1.2",
    "AH": "OD",
    "AJ": "NO ALARMS",
    "AN": "GPS",
    "AO": "YES",
    "AP": "YES",
    "AQ": "YES",
    "AR": "YES",
    "AS": "YES",
    "AT": "YES",
    "AU": "NA",
    "AV": "NA",
    "AW": "YES",
    "AX": "YES",
    "AY": "YES",
    "AZ": "YES",
    "BC": "Shared",
    "BD": "NO",
    "BF": "YES",
    "BI": "NA",
    "BJ": "LTE",
    "BK":"YES",
    }
        url=fill_excel_template(df, temp_path, mapping_dict, fixed_dict)
    elif oem == 'ZTE':
        temp_path= os.path.join(MEDIA_ROOT,'Soft_AT','Templates','offering_templates','zte.xlsx')   
        mapping_dict={
            'CIRCLE': 'B',
            'OEM': 'C',
            'Site_ID': 'E',
            'CELL_COUNT': 'F',
            'Activity_Type_SIWA': 'I',
            'Band_SIWA': 'J',
            'OSS_Details': 'M',
            'BSC_NAME': 'N',
            'TAC': 'S',
            'LNBTS_ID': 'U'
        }
        fixed_dict={
            'D': 'Mobilecomm',
            'Q': 'SOFT AT',
            'Y': 'INFRA/OD',
            'Z': 'NA',
            'AA': 'NA',
            'AB': 'NA',
            'AC': 'NA',
            'AD': 'NA',
            'AE': 'NA',
            'AF': 'NA'
        }
        url=fill_excel_template(df, temp_path, mapping_dict, fixed_dict)
    elif oem == 'HUAWEI':
        temp_path= os.path.join(MEDIA_ROOT,'Soft_AT','Templates','offering_templates','huawei.xlsx')    
        mapping_dict={"unique_key":"A"}
        fixed_dict={"B":"nishant"}
        url=fill_excel_template(df, temp_path, mapping_dict, fixed_dict)

    elif oem == 'ERICSSON':
        temp_path= os.path.join(MEDIA_ROOT,'Soft_AT','Templates','offering_templates','ericsson.xlsx')
        mapping_dict={
        'CIRCLE': 'B',
        'OEM': 'C',
        'Site_ID': 'F',
        'Technology_SIWA': 'G',
        'Band_SIWA': 'H',
        'Activity_Type_SIWA': 'I',
        'MO_NAME': 'N',
        'Mplane_IP': 'O',
        'BSC_NAME': 'Q',
        'TAC': 'S',
        'RRU_Type': 'V',
        'BBU_TYPE': 'W',
    }

        fixed_dict={
                'A': '24-25',
                'C': 'Mobilecomm',
                'D': 'Offered AT Type',
                'AB': 'GPS OK',
                'AF': 'NA',
                'D': 'SoftAT'
            }
        url=fill_excel_template(df, temp_path, mapping_dict, fixed_dict)

    return Response({'url':url}, status=status.HTTP_200_OK)



################################################################## ****************************************************** ################################################

@api_view(['GET','POST'])
def create_combination(request):
    objects = Soft_At_Table.objects.all()
    for obj in objects:
        combination = obj.unique_key.split('__')[0]
        #print(combination)
        obj.combination = combination
        obj.save()
    return Response({'message': 'success'}, status=status.HTTP_200_OK)


@api_view(['GET','POST'])
def copying_oneday_record_to_next_day(request):
    from_date =request.POST.get("from_date")
    to_date =request.POST.get("to_date")
    from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
    to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
    def update_key_with_date(key,date):
        # Split the key at "__" to isolate the date at the end
        key_parts = key.rsplit("__", 1)
        
        # Get the current date in the same format
        
        
        # Replace the old date with the current date and return the updated key
        updated_key = f"{key_parts[0]}__{date}"
        return updated_key

  
    # current_date=datetime.datetime.now()
    # previous_date=current_date-datetime.timedelta(days=1)
    # #print(current_date,previous_date)

    objs=Soft_At_Table.objects.filter(upload_date=from_date)
    date=to_date
    #print(len(objs),objs)
    for obj in objs:
        unique_key = update_key_with_date(obj.unique_key,date)
        if obj.soft_at_status == 'Rejected':
            new_record, created = Soft_At_Table.objects.update_or_create(
            unique_key=unique_key,  # Lookup field for the record
            defaults={
                'upload_date': date,
                'combination': obj.combination,
                'IntegrationData': obj.IntegrationData,
                'spoc_name': obj.spoc_name,
                'offering_type': obj.offering_type,
                'first_offering_date': obj.first_offering_date,
                'soft_at_status': 'Pending',  # Change the status to 'pending'
                'offering_date': obj.offering_date,
                'acceptance_rejection_date': obj.acceptance_rejection_date,
                'alarm_bucket': obj.alarm_bucket,
                'alarm_details': obj.alarm_details,
                'final_responsibility': obj.final_responsibility,
                'workable_non_workable': obj.workable_non_workable,
                'ubr_ms2_status': obj.ubr_ms2_status,
                'ubr_link_id': obj.ubr_link_id,
                'twamp_status': obj.twamp_status,
                'status_check_date': obj.status_check_date,
                'ageing_in_days': obj.ageing_in_days,
                'actual_ageing': obj.actual_ageing,
                'toco_partner': obj.toco_partner,
                'support_required_ubr_team': obj.support_required_ubr_team,
                'support_required_circle_team': obj.support_required_circle_team,
                'support_required_noc_team': obj.support_required_noc_team,
                'category': obj.category,
                'problem_statement': obj.problem_statement,
                'final_remarks': obj.final_remarks,
                'ms1': obj.ms1,
                'status_updated_by': obj.status_updated_by, 

                # Integration data
                'OEM': obj.OEM,
                'Integration_Date': obj.Integration_Date,
                'CIRCLE': obj.CIRCLE,
                'Activity_Name': obj.Activity_Name,
                'Site_ID': obj.Site_ID,
                'MO_NAME': obj.MO_NAME,
                'LNBTS_ID': obj.LNBTS_ID,
                'Technology_SIWA': obj.Technology_SIWA,
                'OSS_Details': obj.OSS_Details,
                'Cell_ID': obj.Cell_ID,
                'CELL_COUNT': obj.CELL_COUNT,
                'TRX_Count': obj.TRX_Count,
                'PRE_ALARM': obj.PRE_ALARM,
                'GPS_IP_CLK': obj.GPS_IP_CLK,
                'RET': obj.RET,
                'POST_VSWR': obj.POST_VSWR,
                'POST_Alarms': obj.POST_Alarms,
                'Activity_Mode': obj.Activity_Mode,
                'CELL_STATUS': obj.CELL_STATUS,
                'CTR_STATUS': obj.CTR_STATUS,
                'Integration_Remark': obj.Integration_Remark,
                'T2T4R': obj.T2T4R,
                'BBU_TYPE': obj.BBU_TYPE,
                'BB_CARD': obj.BB_CARD,
                'RRU_Type': obj.RRU_Type,
                'Media_Status': obj.Media_Status,
                'Mplane_IP': obj.Mplane_IP,
                'SCF_PREPARED_BY': obj.SCF_PREPARED_BY,
                'SITE_INTEGRATE_BY': obj.SITE_INTEGRATE_BY,
                'Site_Status': obj.Site_Status,
                'External_Alarm_Confirmation': obj.External_Alarm_Confirmation,
                'SOFT_AT_STATUS': obj.SOFT_AT_STATUS,
                'LICENCE_Status': obj.LICENCE_Status,
                'ESN_NO': obj.ESN_NO,
                'Responsibility_for_alarm_clearance': obj.Responsibility_for_alarm_clearance,
                'TAC': obj.TAC,
                'PCI_TDD_20': obj.PCI_TDD_20,
                'PCI_TDD_10_20': obj.PCI_TDD_10_20,
                'PCI_FDD_2100': obj.PCI_FDD_2100,
                'PCI_FDD_1800': obj.PCI_FDD_1800,
                'PCI_L900': obj.PCI_L900,
                'PCI_5G': obj.PCI_5G,
                'RSI_TDD_20': obj.RSI_TDD_20,
                'RSI_TDD_10_20': obj.RSI_TDD_10_20,
                'RSI_FDD_2100': obj.RSI_FDD_2100,
                'RSI_FDD_1800': obj.RSI_FDD_1800,
                'RSI_L900': obj.RSI_L900,
                'RSI_5G': obj.RSI_5G,
                'GPL': obj.GPL,
                'Pre_Post_Check': obj.Pre_Post_Check,
                'Activity_Type_SIWA': obj.Activity_Type_SIWA,
                'Band_SIWA': obj.Band_SIWA,
                'BSC_NAME': obj.BSC_NAME,
                'BCF': obj.BCF,
                'soft_delete': obj.soft_delete,
            }
        )
                      
            
        else:
            new_record, created = Soft_At_Table.objects.update_or_create(
            unique_key=unique_key,  # Lookup field to identify record
            defaults={
                'upload_date': date,
                'combination': obj.combination,
                'IntegrationData': obj.IntegrationData,
                'spoc_name': obj.spoc_name,
                'offering_type': obj.offering_type,
                'first_offering_date': obj.first_offering_date,
                'soft_at_status': obj.soft_at_status,  # Change the status to 'pending' if needed
                'offering_date': obj.offering_date,
                'acceptance_rejection_date': obj.acceptance_rejection_date,
                'alarm_bucket': obj.alarm_bucket,
                'alarm_details': obj.alarm_details,
                'final_responsibility': obj.final_responsibility,
                'workable_non_workable': obj.workable_non_workable,
                'ubr_ms2_status': obj.ubr_ms2_status,
                'ubr_link_id': obj.ubr_link_id,
                'twamp_status': obj.twamp_status,
                'status_check_date': obj.status_check_date,
                'ageing_in_days': obj.ageing_in_days,
                'actual_ageing': obj.actual_ageing,
                'toco_partner': obj.toco_partner,
                'support_required_ubr_team': obj.support_required_ubr_team,
                'support_required_circle_team': obj.support_required_circle_team,
                'support_required_noc_team': obj.support_required_noc_team,
                'category': obj.category,
                'problem_statement': obj.problem_statement,
                'final_remarks': obj.final_remarks,
                'ms1': obj.ms1,
                'status_updated_by': obj.status_updated_by,  # Example field to track update

                # Integration data
                'OEM': obj.OEM,
                'Integration_Date': obj.Integration_Date,
                'CIRCLE': obj.CIRCLE,
                'Activity_Name': obj.Activity_Name,
                'Site_ID': obj.Site_ID,
                'MO_NAME': obj.MO_NAME,
                'LNBTS_ID': obj.LNBTS_ID,
                'Technology_SIWA': obj.Technology_SIWA,
                'OSS_Details': obj.OSS_Details,
                'Cell_ID': obj.Cell_ID,
                'CELL_COUNT': obj.CELL_COUNT,
                'TRX_Count': obj.TRX_Count,
                'PRE_ALARM': obj.PRE_ALARM,
                'GPS_IP_CLK': obj.GPS_IP_CLK,
                'RET': obj.RET,
                'POST_VSWR': obj.POST_VSWR,
                'POST_Alarms': obj.POST_Alarms,
                'Activity_Mode': obj.Activity_Mode,
                'CELL_STATUS': obj.CELL_STATUS,
                'CTR_STATUS': obj.CTR_STATUS,
                'Integration_Remark': obj.Integration_Remark,
                'T2T4R': obj.T2T4R,
                'BBU_TYPE': obj.BBU_TYPE,
                'BB_CARD': obj.BB_CARD,
                'RRU_Type': obj.RRU_Type,
                'Media_Status': obj.Media_Status,
                'Mplane_IP': obj.Mplane_IP,
                'SCF_PREPARED_BY': obj.SCF_PREPARED_BY,
                'SITE_INTEGRATE_BY': obj.SITE_INTEGRATE_BY,
                'Site_Status': obj.Site_Status,
                'External_Alarm_Confirmation': obj.External_Alarm_Confirmation,
                'SOFT_AT_STATUS': obj.SOFT_AT_STATUS,
                'LICENCE_Status': obj.LICENCE_Status,
                'ESN_NO': obj.ESN_NO,
                'Responsibility_for_alarm_clearance': obj.Responsibility_for_alarm_clearance,
                'TAC': obj.TAC,
                'PCI_TDD_20': obj.PCI_TDD_20,
                'PCI_TDD_10_20': obj.PCI_TDD_10_20,
                'PCI_FDD_2100': obj.PCI_FDD_2100,
                'PCI_FDD_1800': obj.PCI_FDD_1800,
                'PCI_L900': obj.PCI_L900,
                'PCI_5G': obj.PCI_5G,
                'RSI_TDD_20': obj.RSI_TDD_20,
                'RSI_TDD_10_20': obj.RSI_TDD_10_20,
                'RSI_FDD_2100': obj.RSI_FDD_2100,
                'RSI_FDD_1800': obj.RSI_FDD_1800,
                'RSI_L900': obj.RSI_L900,
                'RSI_5G': obj.RSI_5G,
                'GPL': obj.GPL,
                'Pre_Post_Check': obj.Pre_Post_Check,
                'Activity_Type_SIWA': obj.Activity_Type_SIWA,
                'Band_SIWA': obj.Band_SIWA,
                'BSC_NAME': obj.BSC_NAME,
                'BCF': obj.BCF,
                'soft_delete': obj.soft_delete,
            }
        )


    return Response({"message": "success"}, status=status.HTTP_200_OK)



@api_view(["GET"])
def update_the_missing_offered_date(request):
    site_list = Soft_At_Table.objects.filter(soft_at_status='Offered').values_list('Site_ID', flat=True).distinct() 
    #print(site_list)
    #print(len(site_list))

    for site in site_list:
        objs = Soft_At_Table.objects.filter(Site_ID=site, soft_at_status='Offered')
        offered_date_obj = Soft_At_Table.objects.filter(Site_ID=site, soft_at_status='Offered',upload_date = datetime(2024,9,30)).first()
        if offered_date_obj:
            offered_date = offered_date_obj.offering_date
            #print(site,offered_date)
        else:
            offered_date = None
            #print(site,offered_date)
        obj_gt_30 = Soft_At_Table.objects.filter(Site_ID=site, soft_at_status='Offered', upload_date__gt=datetime(2024,9,30)).update(offering_date=offered_date)
    return Response({"message": len(site_list)}, status=status.HTTP_200_OK)


@api_view(["GET", "POST","PUT"])
def edit_soft_at_report(request, unique_key):
    if request.method == "POST":
        unique_key = request.POST.get("unique_key")
        spoc_name = request.POST.get("spoc_name")
        offering_type = request.POST.get("offering_type")
        first_offering_date = request.POST.get("first_offering_date")
        soft_at_status = request.POST.get("soft_at_status")
        offering_date = request.POST.get("offering_date")
        acceptance_rejection_date = request.POST.get("acceptance_rejection_date")
        alarm_bucket = request.POST.get("alarm_bucket")
        alarm_details = request.POST.get("alarm_details")
        final_responsibility = request.POST.get("final_responsibility")
        workable_non_workable = request.POST.get("workable_non_workable")
        ubr_ms2_status = request.POST.get("ubr_ms2_status")
        ubr_link_id = request.POST.get("ubr_link_id")
        twamp_status = request.POST.get("twamp_status")
        status_check_date = request.POST.get("status_check_date")
        ageing_in_days = request.POST.get("ageing_in_days")
        actual_ageing = request.POST.get("actual_ageing")
        toco_partner = request.POST.get("toco_partner")
        support_required_ubr_team = request.POST.get("support_required_ubr_team")
        support_required_circle_team = request.POST.get("support_required_circle_team")
        support_required_noc_team = request.POST.get("support_required_noc_team")
        category = request.POST.get("category")
        problem_statement = request.POST.get("problem_statement")
        final_remarks = request.POST.get("final_remarks")
        ms1 = request.POST.get("ms1")
        combination=request.POST.get("combination")
        obj = Soft_At_Table.objects.filter(unique_key=unique_key)
        combination = unique_key.split('__')[0]

        if obj.soft_at_status == 'Accepted':
            if soft_at_status == 'Accepted':
                if acceptance_rejection_date == obj.acceptance_rejection_date:
                    pass
                elif acceptance_rejection_date > obj.acceptance_rejection_date:
                    till_date = acceptance_rejection_date - timedelta(days=1)
                    Soft_At_Table.objects.filter(combination=combination,upload_date__range=[obj.acceptance_rejection_date,till_date]).update(soft_at_status = 'Offered') 
                    Soft_At_Table.objects.filter(combination=combination,upload_date = acceptance_rejection_date ).update(soft_at_status = 'Accpeted',soft_delete = False)
                elif acceptance_rejection_date < obj.acceptance_rejection_date:
                    Soft_At_Table.objects.filter(combination=combination,upload_date__gt = acceptance_rejection_date).update(soft_at_status = 'Accepted',soft_delete = True)
                    Soft_At_Table.objects.filter(combination = combination,upload_date = acceptance_rejection_date).update(soft_at_status = 'Accpeted',soft_delete = False)

            elif soft_at_status == 'Rejected':
                if acceptance_rejection_date == obj.acceptance_rejection_date:
                    Soft_At_Table.objects.filter(combination=combination,upload_date = acceptance_rejection_date).update(soft_at_status = 'Rejected',soft_delete = False)
                elif acceptance_rejection_date > obj.acceptance_rejection_date:
                    till_date = acceptance_rejection_date - timedelta(days=1)
                
            elif soft_at_status == 'Dismantle':
                pass
            elif soft_at_status == 'Offered':
                pass
            elif soft_at_status == 'Need to be offer':
                pass
            else:
                pass
        elif obj.soft_at_status == 'Rejected':
            if soft_at_status == 'Rejected':
                pass
            elif soft_at_status == 'Offered':
                pass
            elif soft_at_status == 'Need to be offer':    
                pass 
        
    else:
        return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "POST"])
def hyperlink_circle_wise_dashboard(request):
    if request.method == "POST":
        circle = request.POST.get("circle")
        soft_at_status = request.POST.get("status")
        str_Date = request.POST.get("Date")
        month = request.POST.get("month")
        week = request.POST.get("week")
        year = request.POST.get("year")
        str_from_date = request.POST.get("from_date")
        str_to_date = request.POST.get("to_date")
        Project = request.POST.get("project")
        Projects = Project.split(",")

        print("circle:", circle)
        print("soft_at_status:", soft_at_status)
        print("Date:", str_Date)
        print("month:", month)
        print("week:", week)
        print("year:", year)
        print("from_date:", str_from_date)
        print("to_date:", str_to_date)
        print("project:", Project)
        print("Projects:", Projects)
        
        latest_date = Soft_At_Table.objects.aggregate(Max('upload_date'))['upload_date__max']

        print("latest_date:",latest_date)

        obj=Soft_At_Table.objects.filter(CIRCLE=circle, soft_at_status = soft_at_status, soft_delete = False)



        if Project != "":
            obj = obj.filter(
              Activity_Name__in=Projects, soft_delete=False)
            
        if str_Date != "":
            print("in date condition")
            Date = datetime.strptime(str_Date, "%Y-%m-%d").date()
            obj = obj.filter(upload_date=Date)
        elif str_from_date != "" and str_to_date != "":
            print("in date range condition")
            from_date = datetime.strptime(str_from_date, "%Y-%m-%d").date()
            to_date = datetime.strptime(str_to_date, "%Y-%m-%d").date()
            obj = obj.filter(upload_date__range=[from_date, to_date])
        elif month != "":
            if year != "":
                year = int(year)
                obj = obj.filter(upload_date__year=year)
            print("in month condition")
            obj = obj.filter(upload_date__month=month)
        elif week != "":
            if year != "":
                year = int(year)
                obj = obj.filter(upload_date__year=year)
            print("in week condition")
            obj = obj.filter(upload_date__week=week)

        if str_from_date == "" and str_to_date == "" and str_Date == "" and month == "" and week == "":
            print("here innthis comdition")
            if soft_at_status == 'Accepted':
                obj = obj
            else:
                obj = obj.filter(upload_date=latest_date)

        serializer = ser_Soft_At_Table(obj, many=True)
        return Response({"data":serializer.data}, status=status.HTTP_200_OK)
 
    else:
        return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(["GET", "POST","PUT"])
def reset_to_previous_state(request, unique_key):
    

        obj = Soft_At_Table.objects.get(unique_key=unique_key)
        
        combination = obj.combination
        print(combination)
        if True:
            previous_state_obj = Soft_At_Table.objects.filter(combination = combination).exclude(soft_at_status=obj.soft_at_status).order_by('-upload_date').first()
            if previous_state_obj:
                pre_obj_upload_date = previous_state_obj.upload_date
                print(previous_state_obj.soft_at_status)
                Soft_At_Table.objects.filter(combination = combination,upload_date__gt = pre_obj_upload_date).update(soft_at_status=previous_state_obj.soft_at_status,
                                                                                                                    spoc_name= previous_state_obj.spoc_name,
                                                                                                                    offering_type= previous_state_obj.offering_type,
                                                                                                                    first_offering_date= previous_state_obj.first_offering_date,
                                                                                                                    offering_date= previous_state_obj.offering_date,
                                                                                                                    acceptance_rejection_date= previous_state_obj.acceptance_rejection_date,
                                                                                                                    alarm_bucket= previous_state_obj.alarm_bucket,
                                                                                                                    alarm_details= previous_state_obj.alarm_details,
                                                                                                                    final_responsibility= previous_state_obj.final_responsibility,
                                                                                                                    workable_non_workable= previous_state_obj.workable_non_workable,
                                                                                                                    ubr_ms2_status= previous_state_obj.ubr_ms2_status,
                                                                                                                    ubr_link_id= previous_state_obj.ubr_link_id,
                                                                                                                    twamp_status= previous_state_obj.twamp_status,
                                                                                                                    status_check_date= previous_state_obj.status_check_date,
                                                                                                                    ageing_in_days= previous_state_obj.ageing_in_days,
                                                                                                                    actual_ageing= previous_state_obj.actual_ageing,
                                                                                                                    toco_partner= previous_state_obj.toco_partner,
                                                                                                                    support_required_ubr_team= previous_state_obj.support_required_ubr_team,
                                                                                                                    support_required_circle_team= previous_state_obj.support_required_circle_team,
                                                                                                                    support_required_noc_team= previous_state_obj.support_required_noc_team,
                                                                                                                    category= previous_state_obj.category,
                                                                                                                    problem_statement= previous_state_obj.problem_statement,
                                                                                                                    final_remarks= previous_state_obj.final_remarks,
                                                                                                                    ms1=  previous_state_obj.ms1,
                                                                                                                    soft_delete = False

                                                                                                                    )
                return Response({"message": "success"}, status=status.HTTP_200_OK)   
            
            elif obj.soft_at_status != "NOT OFFERED":
                Soft_At_Table.objects.filter(combination = combination).update(soft_at_status="NOT OFFERED",
                                                                                                                    spoc_name= "",
                                                                                                                    offering_type= "",
                                                                                                                    first_offering_date= None,
                                                                                                                    offering_date= None,
                                                                                                                    acceptance_rejection_date= None,
                                                                                                                    alarm_bucket= "",
                                                                                                                    alarm_details= "",
                                                                                                                    final_responsibility= "",
                                                                                                                    workable_non_workable= "",
                                                                                                                    ubr_ms2_status= "",
                                                                                                                    ubr_link_id= "",
                                                                                                                    twamp_status= "",
                                                                                                                    status_check_date= None,
                                                                                                                    ageing_in_days= None,
                                                                                                                    actual_ageing= "",
                                                                                                                    toco_partner= "",
                                                                                                                    support_required_ubr_team= "",
                                                                                                                    support_required_circle_team= "",
                                                                                                                    support_required_noc_team= "",
                                                                                                                    category= "",
                                                                                                                    problem_statement= "",
                                                                                                                    final_remarks= "",
                                                                                                                    ms1=  "",
                                                                                                                    soft_delete = False
                                                                                                                    )
                return Response({"message": "success"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No previous state found"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
def complete_missing_data(request):
    combination_list = Soft_At_Table.objects.values_list('combination', flat=True).distinct()
    for combination in combination_list:
        obj = Soft_At_Table.objects.filter(combination = combination).first()
        integration_date=obj.Integration_Date
        date_list=generate_date_list(integration_date)

        for date in date_list:
            if Soft_At_Table.objects.filter(combination = combination,upload_date=date).exists():
                print('record already exists for ',combination,date)
                continue
            else:
                new_key = combination + "__" + str(date)
                print('creating missing record for ',combination,date)
                new_record = Soft_At_Table.objects.create(
                upload_date=date,
                unique_key=new_key,  # Copy fields as required
                combination=obj.combination,
                IntegrationData=obj.IntegrationData,
                spoc_name=obj.spoc_name,
                offering_type=obj.offering_type,
                first_offering_date=obj.first_offering_date,
                soft_at_status="NOT OFFERED",  # Change the status to 'pending'
                offering_date=obj.offering_date,
                acceptance_rejection_date=obj.acceptance_rejection_date,
                alarm_bucket=obj.alarm_bucket,
                alarm_details=obj.alarm_details,
                final_responsibility=obj.final_responsibility,
                workable_non_workable=obj.workable_non_workable,
                ubr_ms2_status=obj.ubr_ms2_status,
                ubr_link_id=obj.ubr_link_id,
                twamp_status=obj.twamp_status,
                status_check_date=obj.status_check_date,
                ageing_in_days=obj.ageing_in_days,
                actual_ageing=obj.actual_ageing,
                toco_partner=obj.toco_partner,
                support_required_ubr_team=obj.support_required_ubr_team,
                support_required_circle_team=obj.support_required_circle_team,
                support_required_noc_team=obj.support_required_noc_team,
                category=obj.category,
                problem_statement=obj.problem_statement,
                final_remarks=obj.final_remarks,
                ms1=obj.ms1,
                status_updated_by='auto_system', 
                 
                # integration data
                OEM=obj.OEM,
                Integration_Date=obj.Integration_Date,
                CIRCLE=obj.CIRCLE,
                Activity_Name=obj.Activity_Name,
                Site_ID=obj.Site_ID,
                MO_NAME=obj.MO_NAME,
                LNBTS_ID=obj.LNBTS_ID,
                Technology_SIWA=obj.Technology_SIWA,
                OSS_Details=obj.OSS_Details,
                Cell_ID=obj.Cell_ID,
                CELL_COUNT=obj.CELL_COUNT,
                TRX_Count=obj.TRX_Count,
                PRE_ALARM=obj.PRE_ALARM,
                GPS_IP_CLK=obj.GPS_IP_CLK,
                RET=obj.RET,
                POST_VSWR=obj.POST_VSWR,
                POST_Alarms=obj.POST_Alarms,
                Activity_Mode=obj.Activity_Mode,
                CELL_STATUS=obj.CELL_STATUS,
                CTR_STATUS=obj.CTR_STATUS,
                Integration_Remark=obj.Integration_Remark,
                T2T4R=obj.T2T4R,
                BBU_TYPE=obj.BBU_TYPE,
                BB_CARD=obj.BB_CARD,
                RRU_Type=obj.RRU_Type,
                Media_Status=obj.Media_Status,
                Mplane_IP=obj.Mplane_IP,
                SCF_PREPARED_BY=obj.SCF_PREPARED_BY,
                SITE_INTEGRATE_BY=obj.SITE_INTEGRATE_BY,
                Site_Status=obj.Site_Status,
                External_Alarm_Confirmation=obj.External_Alarm_Confirmation,
                SOFT_AT_STATUS=obj.SOFT_AT_STATUS,
                LICENCE_Status=obj.LICENCE_Status,
                ESN_NO=obj.ESN_NO,
                Responsibility_for_alarm_clearance=obj.Responsibility_for_alarm_clearance,
                TAC=obj.TAC,
                PCI_TDD_20=obj.PCI_TDD_20,
                PCI_TDD_10_20=obj.PCI_TDD_10_20,
                PCI_FDD_2100=obj.PCI_FDD_2100,
                PCI_FDD_1800=obj.PCI_FDD_1800,
                PCI_L900=obj.PCI_L900,
                PCI_5G=obj.PCI_5G,
                RSI_TDD_20=obj.RSI_TDD_20,
                RSI_TDD_10_20=obj.RSI_TDD_10_20,
                RSI_FDD_2100=obj.RSI_FDD_2100,
                RSI_FDD_1800=obj.RSI_FDD_1800,
                RSI_L900=obj.RSI_L900,
                RSI_5G=obj.RSI_5G,
                GPL=obj.GPL,
                Pre_Post_Check=obj.Pre_Post_Check,
                Activity_Type_SIWA=obj.Activity_Type_SIWA,
                Band_SIWA=obj.Band_SIWA,
                BSC_NAME=obj.BSC_NAME,
                BCF=obj.BCF,    
                soft_delete=obj.soft_delete,
                


            )


    return Response({"message": "success"}, status=status.HTTP_200_OK)
   