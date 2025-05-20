from django.shortcuts import render

# Create your views here.
import traceback
from django.shortcuts import render
from rest_framework.decorators import api_view
from mcom_website.settings import MEDIA_ROOT,MEDIA_URL
from rest_framework.response import Response

from django.core.files.storage import FileSystemStorage
import pandas as pd
import os
from .models import *   
import datetime
# Create your views here.
import json
from .serializers import * 
from .models import *   

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes,permission_classes


import json
from django.db import connection
from django.core.serializers import serialize
from django.http import JsonResponse

def circle_list(objs):
    cir=[]
    
    for obj in objs:
        cir.append(obj.CIRCLE)

    cir_set=set(cir)
    cir=list(cir_set)
    return cir


def all_circle_list():
    objs=WPR_DPR2_Table.objects.all()
    cir=[]
    
    for obj in objs:
        cir.append(obj.CIRCLE)
    cir_set=set(cir)
    cir=list(cir_set)
    return cir

def project_list(objs):
    projects=[]
    
    for obj in objs:
        projects.append(obj.Project)

    project_set=set(projects)
    projects=list(project_set)
    return projects

@ api_view(["GET"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def softAtTemplate(request):
    print("Current_User---------------",request.user)
    download_path= os.path.join(MEDIA_URL,"Soft_AT","templates","Soft_At_Template.xlsx")
    return Response({"status":True, "message":"Downloaded Sucessfully","Download_url":download_path})

def df_column_total(data):
        # print("_________________circle_wise_data_____________________________________")
        print(data)
        df=pd.DataFrame(data)
        df=df.T
        # add a sum row at the bottom of the dataframe
        df.loc['Total'] = df.sum()
      #   # add a sum column at the right end of the dataframe
      #   df['Total'] = df.sum(axis=1)
        json_data = df.to_json(orient='index') # here json_data  converts the dataframe to a string json
        json_data=json.loads(json_data) # json.loads - Which converts the string form of json data to a dictionary in python.
        print(df)
        return(json_data)

def df_raw_column_total(data):
        # print("_________________circle_wise_data_____________________________________")
        print(data)
        df=pd.DataFrame(data)
        df=df.T
        # add a sum row at the bottom of the dataframe
        df.loc['Total'] = df.sum()
        # add a sum column at the right end of the dataframe
        df['Total'] = df.sum(axis=1)
        json_data = df.to_json(orient='index') # here json_data  converts the dataframe to a string json
        json_data=json.loads(json_data) # json.loads - Which converts the string form of json data to a dictionary in python.
        print(df)
        return(json_data)
def df_raw_column_total_circle_wise(data):
        print("_________________circle_wise_data_____________________________________")
        print(data)
        df=pd.DataFrame(data)
        df=df.T
        print("---------------------------dataframe------------------------",df)
        # add a sum row at the bottom of the dataframe
        df.loc['Total'] = df.sum()
        # add a sum column at the right end of the dataframe
        df['Total'] = df["Accepted"] + df["Rejected"] +df["Dismantle"] + df["Pending"] + df["Need_to_be_offer"] +df["offered"]
        json_data = df.to_json(orient='index') # here json_data  converts the dataframe to a string json
        json_data=json.loads(json_data) # json.loads - Which converts the string form of json data to a dictionary in python.
        print(df)
        return(json_data)


@ api_view(["POST"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def WPR_DPR2_Upload(request):
    print("Current_User---------------",request.user)
    WPR_DPR2_Table_upload_status.objects.all().delete()
    WPR_DPR2_report_file = request.FILES["WPR_DPR2_report_file"] if 'WPR_DPR2_report_file' in request.FILES else None
    if WPR_DPR2_report_file:
            location = MEDIA_ROOT + r"\WPR_DPR2\temporary_files"
            fs = FileSystemStorage(location=location)
            file = fs.save(WPR_DPR2_report_file.name, WPR_DPR2_report_file)
            # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
            filepath = fs.path(file)
            print("file_path:-",filepath)
            df=pd.read_excel(filepath,sheet_name="Data") # should do something if a csv file is coming from the frontend and the csv file should be deleted from the temp files
            os.remove(path=filepath)
            print(filepath,"deleted........")
            print(df)
            upload_week=request.POST.get("upload_week")
            print("upload week is......................",upload_week)
            
            ############################### Code for checking  if the report upoaded have all the necessary columns or not ######################
            df_header_list= df.columns.tolist()
            print("Header Name-------------------",df_header_list)
            required_header_list=["CIRCLE",
                                  "NOMINAL_AOP",
                                  "NOMINAL_QUARTER",
                                  "SITE_ID",
                                  "UNIQUE ID",
                                  "ENODEB_ID",
                                  "BAND",
                                  "Churn/Non Churn/Super Churn",
                                  "Incase of Relocation (Old TOCO)",
                                  "Circle Project","BTS_TYPE",
                                  'Allocation-Date',"OEM_NAME (Nokia/ZTE/Ericsson/Huawei)",
                                  "TOCO_NAME","LOCATOR_ID",
                                  "RFAI","POST_RFAI_SURVEY_DATE",
                                  "RFAI_REJECTION_DATE","RFAI_REGENERATION_DATE",
                                  "MO_PUNCHING_DATE","MATERIAL_DISPATCH_(MD)_DATE",
                                  "INSTALLATION_START_DATE","INSTALLATION_END_DATE",
                                  "POST_MEDIA_ISSUE_OPEN_DATE","POST_MEDIA_ISSUE_CLOSE_DATE",
                                  "Integration Date","SACFA_APPLIED_DATE",
                                  "SACFA_APPLICATION_ID","DEVIATION_APPROVAL_MAIL_RX_DATE_(IF_APPLICABLE)",
                                  "WPC_ACCEPTANCE_DATE","WPC_ACCEPTANCE_ID",
                                  "EMF_SUBMISSION_DATE","SCFT_COMPLETION_DATE","MS1","Rfai vs MS1",
                                  "Reason for Delay over period of more than 14 Days",
                                  "RFAI VS MS1- Responsibility","Physical AT Offered Date",
                                  "PHYSICAL_AT_ACCEPTANCE_DATE",
                                  "PHYSICAL_AT_Status( Accepted/Rejected/Offered/Pending/Dismantle)",
                                  "MS1 Vs PHY AT Acceptance- Ageing",
                                  "Reason for PHY AT Rejection/ Not offered beyond 5 days","Soft AT Offered Date",
                                  "SOFT_AT_ACCEPTANCE_DATE",
                                  "Soft_AT_Status( Accepted/Rejected/Offered/Pending/Dismantle)",
                                  "MS1 Vs Soft AT Acceptance- Ageing",
                                  "Reason for Soft AT Rejection/ Not offered beyond 5 days",
                                  "PERFORMANCE_AT_Offered_DATE",
                                  "PERFORMANCE_AT_ACCEPTANCE_DATE2",
                                  "Performance_AT_Status( Accepted/Rejected/Offered/Pending/Dismantle)",
                                  "MS1 Vs Performance AT Acceptance- Ageing",
                                  "Reason for Performance AT Rejection/ Not offered beyond 7 days",
                                  "MAPA","MS1 Vs MS2 Ageing","Reason for delay more than 15 days",
                                  "MS1 VS MS2 Responsibility","Addition MS2 Remarks","CURRENT_STATUS_OF_SITE",
                                  "Circle Reamarks","PRI_CATEGORY_(ACCESS/INFRA)",
                                  "PRI_CATEGORY_(ACCESS/INFRA)- Last Discussion Date","ATP Name","ATP Status",
                                  "ATP Count","Internal RFAI Vs Ms1-In Days",
                                  "Internal Ms1 Vs Ms2-In days","RFAI Vs MS1","Ms1 Vs Ms2",
                                  "Total  Allocation","High Ageing Remark_1",
                                  "Project","RFAI Week","MS1 -week","MS2-Week",
                                  "E// Site Id","Band","E// Project","Media Type",
                                  "UBR/MW ATP Final Status",
                                  "UBR/MW ATP Phy AT Status","UBR/MW ATP Soft AT Status",
                                  "Additional DPR Remarks","Media Done By","Sub Project"]
            for header_name in required_header_list:
                if header_name in df_header_list:
                     pass
                else:
                     message= "Did not get " + header_name + " Column in the uploaded Report"
                     return Response({"status":False,"message":message})
                
            ######################################################################################################################################

            for i, d in df.iterrows():
                
                    pk=str(d["CIRCLE"])+str(d["SITE_ID"])+str(d["BAND"])+str(d["OEM_NAME (Nokia/ZTE/Ericsson/Huawei)"]) +str(upload_week)
                   
                    if pd.isnull(d['Allocation-Date']) or isinstance(d['Allocation-Date'], str):
                           Allocation_Date=None
                    else:
                           Allocation_Date=(d["Allocation-Date"])

                    if pd.isnull(d['RFAI']) or isinstance(d['RFAI'], str):
                          RFAI=None
                    else:
                           RFAI=(d["RFAI"])

                    if pd.isnull(d['POST_RFAI_SURVEY_DATE']) or isinstance(d['POST_RFAI_SURVEY_DATE'], str):
                          POST_RFAI_SURVEY_DATE=None
                    else:
                           POST_RFAI_SURVEY_DATE=(d["POST_RFAI_SURVEY_DATE"]) 

                    if pd.isnull(d['RFAI_REJECTION_DATE']) or isinstance(d['RFAI_REJECTION_DATE'], str):
                          RFAI_REJECTION_DATE=None
                    else:
                           RFAI_REJECTION_DATE=(d["RFAI_REJECTION_DATE"])

                    if pd.isnull(d['RFAI_REGENERATION_DATE']) or isinstance(d['RFAI_REGENERATION_DATE'], str):
                          RFAI_REGENERATION_DATE=None
                    else:
                          RFAI_REGENERATION_DATE=(d["RFAI_REGENERATION_DATE"])

                    if pd.isnull(d['MO_PUNCHING_DATE']) or isinstance(d['MO_PUNCHING_DATE'], str):
                          MO_PUNCHING_DATE=None
                    else:
                          MO_PUNCHING_DATE=(d["MO_PUNCHING_DATE"])

                    if pd.isnull(d['MATERIAL_DISPATCH_(MD)_DATE']) or isinstance(d['MATERIAL_DISPATCH_(MD)_DATE'], str):
                          MATERIAL_DISPATCH_MD_DATE=None
                    else:
                          MATERIAL_DISPATCH_MD_DATE=(d["MATERIAL_DISPATCH_(MD)_DATE"])

                    if pd.isnull(d['MATERIAL_DELIVERY_(MOS)_DATE']) or isinstance(d['MATERIAL_DELIVERY_(MOS)_DATE'], str):
                          MATERIAL_DELIVERY_MOS_DATE=None
                    else:
                          MATERIAL_DELIVERY_MOS_DATE=(d["MATERIAL_DELIVERY_(MOS)_DATE"])

                    if pd.isnull(d['INSTALLATION_START_DATE']) or isinstance(d['INSTALLATION_START_DATE'], str):
                          INSTALLATION_START_DATE=None
                    else:
                          INSTALLATION_START_DATE=(d["INSTALLATION_START_DATE"])

                    if pd.isnull(d['INSTALLATION_END_DATE']) or isinstance(d['INSTALLATION_END_DATE'], str):
                          INSTALLATION_END_DATE=None
                    else:
                          INSTALLATION_END_DATE=(d["INSTALLATION_END_DATE"]) 

                    if pd.isnull(d['POST_MEDIA_ISSUE_OPEN_DATE']) or isinstance(d['POST_MEDIA_ISSUE_OPEN_DATE'], str):
                         POST_MEDIA_ISSUE_OPEN_DATE=None
                    else:
                         POST_MEDIA_ISSUE_OPEN_DATE=(d["POST_MEDIA_ISSUE_OPEN_DATE"])

                    if pd.isnull(d['POST_MEDIA_ISSUE_CLOSE_DATE']) or isinstance(d['POST_MEDIA_ISSUE_CLOSE_DATE'], str):
                         POST_MEDIA_ISSUE_CLOSE_DATE=None
                    else:
                          POST_MEDIA_ISSUE_CLOSE_DATE=(d["POST_MEDIA_ISSUE_CLOSE_DATE"])

                    if pd.isnull(d['Integration Date']) or isinstance(d['Integration Date'], str):
                         Integration_Date=None
                    else:
                          Integration_Date=(d["Integration Date"])

                    if pd.isnull(d['SACFA_APPLIED_DATE']) or isinstance(d['SACFA_APPLIED_DATE'], str):
                         SACFA_APPLIED_DATE=None
                    else:
                         SACFA_APPLIED_DATE=(d["SACFA_APPLIED_DATE"]) 

                    if pd.isnull(d['DEVIATION_APPROVAL_MAIL_RX_DATE_(IF_APPLICABLE)']) or isinstance(d['DEVIATION_APPROVAL_MAIL_RX_DATE_(IF_APPLICABLE)'], str):
                         DEVIATION_APPROVAL_MAIL_RX_DATE_IF_APPLICABLE=None
                    else:
                         DEVIATION_APPROVAL_MAIL_RX_DATE_IF_APPLICABLE=(d["DEVIATION_APPROVAL_MAIL_RX_DATE_(IF_APPLICABLE)"]) 

                    if pd.isnull(d['WPC_ACCEPTANCE_DATE']) or  isinstance(d['WPC_ACCEPTANCE_DATE'], str):
                         WPC_ACCEPTANCE_DATE=None
                    else:
                        WPC_ACCEPTANCE_DATE=(d["WPC_ACCEPTANCE_DATE"])

                    if pd.isnull(d['EMF_SUBMISSION_DATE']) or  isinstance(d['EMF_SUBMISSION_DATE'], str):
                        EMF_SUBMISSION_DATE=None
                    else:
                        EMF_SUBMISSION_DATE=(d["EMF_SUBMISSION_DATE"]) 

                    if pd.isnull(d['SCFT_COMPLETION_DATE']) or  isinstance(d['SCFT_COMPLETION_DATE'], str):
                        SCFT_COMPLETION_DATE=None
                    else:
                        SCFT_COMPLETION_DATE=(d["SCFT_COMPLETION_DATE"]) 

                    if pd.isnull(d['MS1']) or  isinstance(d['MS1'], str):
                        MS1=None
                    else:
                        MS1=(d["MS1"]) 

                    if pd.isnull(d['Physical AT Offered Date']) or  isinstance(d['Physical AT Offered Date'], str):
                        Physical_AT_Offered_Date=None
                    else:
                        Physical_AT_Offered_Date=(d["Physical AT Offered Date"])    

                    if pd.isnull(d['PHYSICAL_AT_ACCEPTANCE_DATE']) or  isinstance(d['PHYSICAL_AT_ACCEPTANCE_DATE'], str):
                       PHYSICAL_AT_ACCEPTANCE_DATE=None
                    else:
                       PHYSICAL_AT_ACCEPTANCE_DATE=(d["PHYSICAL_AT_ACCEPTANCE_DATE"]) 

                    if pd.isnull(d['Soft AT Offered Date']) or isinstance(d['Soft AT Offered Date'], str):
                       Soft_AT_Offered_Date=None
                    else:
                      Soft_AT_Offered_Date=(d["Soft AT Offered Date"])

                    if pd.isnull(d['SOFT_AT_ACCEPTANCE_DATE']) or  isinstance(d['SOFT_AT_ACCEPTANCE_DATE'], str):
                       SOFT_AT_ACCEPTANCE_DATE=None
                    else:
                      SOFT_AT_ACCEPTANCE_DATE=(d["SOFT_AT_ACCEPTANCE_DATE"]) 

                    if pd.isnull(d['MS1 Vs Soft AT Acceptance- Ageing']) or isinstance(d['MS1 Vs Soft AT Acceptance- Ageing'], str):
                        MS1_Vs_Soft_AT_Acceptance_Ageing=None
                    else:
                       MS1_Vs_Soft_AT_Acceptance_Ageing=(d["MS1 Vs Soft AT Acceptance- Ageing"])   

                    if pd.isnull(d['PERFORMANCE_AT_Offered_DATE']) or isinstance(d['PERFORMANCE_AT_Offered_DATE'], str):
                       PERFORMANCE_AT_Offered_DATE=None
                    else:
                      PERFORMANCE_AT_Offered_DATE=(d["PERFORMANCE_AT_Offered_DATE"])

                    if pd.isnull(d['PERFORMANCE_AT_ACCEPTANCE_DATE2']) or isinstance(d['PERFORMANCE_AT_ACCEPTANCE_DATE2'], str):
                       PERFORMANCE_AT_ACCEPTANCE_DATE2=None
                    else:
                     PERFORMANCE_AT_ACCEPTANCE_DATE2=(d["PERFORMANCE_AT_ACCEPTANCE_DATE2"]) 

                    if pd.isnull(d['MAPA']) or isinstance(d['MAPA'], str):
                      MAPA=None
                    else:
                      MAPA=(d["MAPA"]) 

                    if pd.isnull(d['MAPA']) or isinstance(d['MAPA'], str):
                      MAPA=None
                    else:
                      MAPA=(d["MAPA"]) 

                    if pd.isnull(d['PRI_CATEGORY_(ACCESS/INFRA)- Last Discussion Date']) or isinstance(d['PRI_CATEGORY_(ACCESS/INFRA)- Last Discussion Date'], str):
                      PRI_CATEGORY_ACCESS_INFRA_Last_Discussion_Date=None
                    else:
                      PRI_CATEGORY_ACCESS_INFRA_Last_Discussion_Date=(d["PRI_CATEGORY_(ACCESS/INFRA)- Last Discussion Date"]) 

                    # if pd.isnull(d['RFAI Vs MS1']):
                    #   RFAI_Vs_MS1=None
                    # else:
                    #   RFAI_Vs_MS1=(d["RFAI Vs MS1"])      
                    if pd.isnull(d["MS1 Vs Performance AT Acceptance- Ageing"]) or isinstance(d['MS1 Vs Performance AT Acceptance- Ageing'], str):
                      MS1_Vs_Performance_AT_Acceptance_Ageing=None
                    else:
                      MS1_Vs_Performance_AT_Acceptance_Ageing=(d["MS1 Vs Performance AT Acceptance- Ageing"] )    
                   

                    if pd.isnull(d["MS1 Vs PHY AT Acceptance- Ageing"]) or isinstance(d['MS1 Vs PHY AT Acceptance- Ageing'], str):
                      MS1_Vs_PHY_AT_Acceptance_Ageing=None
                    else:
                      MS1_Vs_PHY_AT_Acceptance_Ageing=(d["MS1 Vs PHY AT Acceptance- Ageing"] )    
                    # MS1_Vs_Performance_AT_Acceptance_Ageing
                                        #  MS1 Vs PHY AT Acceptance- Ageing
                    try:
                        obj,created=WPR_DPR2_Table.objects.update_or_create(id=pk,WEEK=upload_week,
                                                     defaults={"CIRCLE":str(d["CIRCLE"]),
                                                               "WEEK":upload_week,
                                                        "NOMINAL_AOP":str(d["NOMINAL_AOP"]),
                                                        "NOMINAL_QUARTER":str(d["NOMINAL_QUARTER"]),
                                                        "SITE_ID":str(d["SITE_ID"]),
                                                        "UNIQUE_ID":str(d["UNIQUE ID"]),
                                                        "ENODEB_ID":str(d["ENODEB_ID"]),  #changed from circle project to project
                                                        "BAND":str(d["BAND"]),
                                                        "Churn_Non_Churn_Super_Churn":str(d["Churn/Non Churn/Super Churn"]),
                                                        "Incase_of_Relocation_Old_TOCO":str(d["Incase of Relocation (Old TOCO)"]),
                                                        "Circle_Project":str(d["Circle Project"]),
                                                        "BTS_TYPE":str(d["BTS_TYPE"]),
                                                        "Allocation_Date":Allocation_Date,
                                                        "TOCO_NAME":str(d["TOCO_NAME"]),
                                                        "RFAI":RFAI,
                                                        
                                                        "POST_RFAI_SURVEY_DATE":POST_RFAI_SURVEY_DATE,
                                                        "RFAI_REJECTION_DATE":RFAI_REJECTION_DATE,
                                                        "RFAI_REGENERATION_DATE":RFAI_REGENERATION_DATE,
                                                        "MO_PUNCHING_DATE":MO_PUNCHING_DATE,
                                                        "MATERIAL_DISPATCH_MD_DATE":MATERIAL_DISPATCH_MD_DATE,
                                                        "MATERIAL_DELIVERY_MOS_DATE":MATERIAL_DELIVERY_MOS_DATE,
                                                        "INSTALLATION_START_DATE":INSTALLATION_START_DATE,
                                                        "INSTALLATION_END_DATE":INSTALLATION_END_DATE,
                                                        "POST_MEDIA_ISSUE_OPEN_DATE":POST_MEDIA_ISSUE_OPEN_DATE,
                                                        "POST_MEDIA_ISSUE_CLOSE_DATE":POST_MEDIA_ISSUE_CLOSE_DATE,

                                                        "Integration_Date":Integration_Date,
                                                        "SACFA_APPLIED_DATE":SACFA_APPLIED_DATE,
                                                        "SACFA_APPLICATION_ID":str(d["SACFA_APPLICATION_ID"]),
                                                        "DEVIATION_APPROVAL_MAIL_RX_DATE_IF_APPLICABLE":DEVIATION_APPROVAL_MAIL_RX_DATE_IF_APPLICABLE,
                                                        "WPC_ACCEPTANCE_DATE":WPC_ACCEPTANCE_DATE,
                                                        "WPC_ACCEPTANCE_ID":str(d["WPC_ACCEPTANCE_ID"]),
                                                        "EMF_SUBMISSION_DATE":EMF_SUBMISSION_DATE,
                                                        "SCFT_COMPLETION_DATE":SCFT_COMPLETION_DATE,
                                                        "MS1":MS1,

                                                        "Rfai_vs_MS1":str(d["Rfai vs MS1"]),
                                                        "Reason_for_Delay_over_period_of_more_than_14_Days":str(d["Reason for Delay over period of more than 14 Days"]),
                                                        "RFAI_VS_MS1_Responsibility":str(d["RFAI VS MS1- Responsibility"]),
                                                        "Physical_AT_Offered_Date":Physical_AT_Offered_Date,
                                                        "PHYSICAL_AT_ACCEPTANCE_DATE":PHYSICAL_AT_ACCEPTANCE_DATE,
                                                        "PHYSICAL_AT_Status_Accepted_Rejected_Offered_Pending_Dismantle":str(d["PHYSICAL_AT_Status( Accepted/Rejected/Offered/Pending/Dismantle)"]),
                                                        "MS1_Vs_PHY_AT_Acceptance_Ageing": MS1_Vs_PHY_AT_Acceptance_Ageing,
                                                        "Reason_for_PHY_AT_Rejection_Not_offered_beyond_5_days":str(d["Reason for PHY AT Rejection/ Not offered beyond 5 days"]),
                                                        "Soft_AT_Offered_Date":Soft_AT_Offered_Date,
                                                        "SOFT_AT_ACCEPTANCE_DATE":SOFT_AT_ACCEPTANCE_DATE,
                                                        "Soft_AT_Status_Accepted_Rejected_Offered_Pending_Dismantle":str(d["Soft_AT_Status( Accepted/Rejected/Offered/Pending/Dismantle)"]),
                                                        "MS1_Vs_Soft_AT_Acceptance_Ageing": MS1_Vs_Soft_AT_Acceptance_Ageing,
                                                        "Reason_for_Soft_AT_Rejection_Not_offered_beyond_5_days":str(d["Reason for Soft AT Rejection/ Not offered beyond 5 days"]),
                                                        "PERFORMANCE_AT_Offered_DATE":PERFORMANCE_AT_Offered_DATE,
                                                        "PERFORMANCE_AT_ACCEPTANCE_DATE2":PERFORMANCE_AT_ACCEPTANCE_DATE2,
                                                        "Performance_AT_Status_Accept_Rejected_Offered_Pending_Dismantle":str(d["Performance_AT_Status( Accepted/Rejected/Offered/Pending/Dismantle)"]),
                                                        "MS1_Vs_Performance_AT_Acceptance_Ageing":MS1_Vs_Performance_AT_Acceptance_Ageing ,
                                                        "Reason_for_Performance_AT_Rejection_Not_offered_beyond_7_days":str(d["Reason for Performance AT Rejection/ Not offered beyond 7 days"]),
                                                        "MAPA":MAPA,

                                                        "Reason_for_delay_more_than_15_days":str(d["Reason for delay more than 15 days"]),
                                                        "MS1_VS_MS2_Responsibility":str(d["MS1 VS MS2 Responsibility"]),
                                                        "Addition_MS2_Remarks":str(d["Addition MS2 Remarks"]),
                                                        "CURRENT_STATUS_OF_SITE":str(d["CURRENT_STATUS_OF_SITE"]),
                                                        "Circle_Reamarks":str(d["Circle Reamarks"]),
                                                        "PRI_CATEGORY_ACCESS_INFRA":str(d["PRI_CATEGORY_(ACCESS/INFRA)"]),
                                                        "PRI_CATEGORY_ACCESS_INFRA_Last_Discussion_Date":PRI_CATEGORY_ACCESS_INFRA_Last_Discussion_Date,
                                                        "ATP_Name":str(d["ATP Name"]),
                                                        "ATP_Status":str(d["ATP Status"]),
                                                        "ATP_Count":str(d["ATP Count"]),
                                                        "Internal_RFAI_Vs_Ms1_In_Days":str(d["Internal RFAI Vs Ms1-In Days"]),
                                                        "Internal_Ms1_Vs_Ms2_In_days":str(d["Internal Ms1 Vs Ms2-In days"]),
                                                        "RFAI_Vs_MS1":str(d["RFAI Vs MS1"]),
                                                        "Total_Allocation":str(d["Total  Allocation"]),
                                                        "High_Ageing_Remark_1":str(d["High Ageing Remark_1"]),
                                                        "Project":str(d["Project"]),
                                                        "RFAI_Week":str(d["RFAI Week"]),
                                                        "MS1_week":str(d["MS1 -week"]),
                                                        "ATP_Count":str(d["ATP Count"]),
                                                        "MS2_Week":str(d["MS2-Week"]),
                                                        "E_Site_Id":str(d["E// Site Id"]),
                                                        "Band":str(d["Band"]),
                                                        "E_Project":str(d["E// Project"]),
                                                        "Media_Type":str(d["Media Type"]),
                                                        "UBR_MW_ATP_Final_Status":str(d["UBR/MW ATP Final Status"]),
                                                        "UBR_MW_ATP_Phy_AT_Status":str(d["UBR/MW ATP Phy AT Status"]),
                                                        "UBR_MW_ATP_Soft_AT_Status":str(d["UBR/MW ATP Soft AT Status"]),
                                                        "Additional_DPR_Remarks":str(d["Additional DPR Remarks"]),
                                                        "Media_Done_By":str(d["Media Done By"]),
                                                        "Sub_Project":str(d["Sub Project"]),
                                                       
                                                        }   # we provide a date in string formate to a date field of models
                                                        )
                        
                    except Exception as e:
                            print("error",e)
                            error=str(e)
                            traceback.print_exc()
                            obj=WPR_DPR2_Table_upload_status.objects.filter(id=pk)
                            if len(obj)==0:
                                 
                                          WPR_DPR2_Table_upload_status.objects.create(id=pk,Site_id=d["SITE_ID"],update_status="Not Uploaded",Remark=error)
                            else:
                                    continue 
                
            objs=WPR_DPR2_Table_upload_status.objects.all()
            serializers=ser_Soft_At_upload_status(objs,many=True)          


            return Response({"status": True,"message":"Report uploaded Successfully .","status_obj":serializers.data})
    else:
         return Response({"status": False,"message":"No report file Sent"})


def project_ageing(perticularWeekObjects):
    circles=circle_list(perticularWeekObjects)
    print(circles)
    circlewise_data={}
    for circle in circles:
          circle_obj=perticularWeekObjects.filter(CIRCLE = circle)
          projects=project_list(circle_obj)
          print(projects)
          projectwise_data={}
          for project in projects:
              project_obj=circle_obj.filter(Project = project)
              RFAI=project_obj.exclude(RFAI = None).count()
              Ms1=project_obj.exclude(MS1 = None).count()
              Ms2=project_obj.exclude(MAPA = None).count()

              RFAI_Ms1_Gap = RFAI - Ms1
              Ms1_Ms2_Gap=Ms1-Ms2
              # Ms1_per=round((Ms1/RFAI)*100,2)
              # Ms2_per=round((Ms2/Ms1)*100,2)

              if RFAI >0:
                Ms1_per=round((Ms1/RFAI)*100,)
              else:
                Ms1_per =0
              if Ms1 >0:
                Ms2_per=round((Ms2/Ms1)*100,)
              else:
                Ms2_per=0
              
              ########################################### MS1 ageing #####################################
              Ms1_ageing_0_15=project_obj.filter(MS1=None, Internal_RFAI_Vs_Ms1_In_Days = "0-15").count()
              Ms1_ageing_16_30=project_obj.filter(MS1=None, Internal_RFAI_Vs_Ms1_In_Days = "16-30").count()
              Ms1_ageing_31_60=project_obj.filter(MS1=None, Internal_RFAI_Vs_Ms1_In_Days = "31-60").count()
              Ms1_ageing_61_90=project_obj.filter(MS1=None,Internal_RFAI_Vs_Ms1_In_Days = "61-90").count()
              Ms1_ageing_GT90=project_obj.filter(MS1=None,Internal_RFAI_Vs_Ms1_In_Days = "GT90").count()   
              
              ########################################## MS2 ageing ########################################
              Ms2_ageing_0_15=project_obj.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "0-15").count()
              Ms2_ageing_16_30=project_obj.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "16-30").count()
              Ms2_ageing_31_60=project_obj.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "31-60").count()
              Ms2_ageing_61_90=project_obj.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "61-90").count()
              Ms2_ageing_GT90=project_obj.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "GT90").count() 

              projectwise_data[project]={"RFAI":RFAI,
                                        "Ms1":Ms1,
                                        "RFAI_Ms1_Gap":RFAI_Ms1_Gap,
                                        "Ms1_per":Ms1_per,
                                        "Ms2":Ms2,
                                        "Ms1_Ms2_Gap":Ms1_Ms2_Gap,
                                        "Ms2_per":Ms2_per,

                                        "Ms1_ageing_0_15":Ms1_ageing_0_15,
                                        "Ms1_ageing_16_30":Ms1_ageing_16_30,
                                        "Ms1_ageing_31_60":Ms1_ageing_31_60,
                                        "Ms1_ageing_61_90":Ms1_ageing_61_90,
                                        "Ms1_ageing_GT90":Ms1_ageing_GT90,

                                        "Ms2_ageing_0_15":Ms2_ageing_0_15,
                                        "Ms2_ageing_16_30":Ms2_ageing_16_30,
                                        "Ms2_ageing_31_60":Ms2_ageing_31_60,
                                        "Ms2_ageing_61_90":Ms2_ageing_61_90,
                                        "Ms2_ageing_GT90":Ms2_ageing_GT90
                                        }
          circlewise_data[circle]=projectwise_data

    total_RFAI=perticularWeekObjects.exclude(RFAI = None).count()
    total_Ms1=perticularWeekObjects.exclude(MS1 = None).count()
    total_Ms2=perticularWeekObjects.exclude(MAPA = None).count()

    total_RFAI_Ms1_Gap = RFAI - Ms1
    total_Ms1_Ms2_Gap=Ms1-Ms2
    # Ms1_per=round((Ms1/RFAI)*100,2)
    # Ms2_per=round((Ms2/Ms1)*100,2)

    if RFAI >0:
      total_Ms1_per=round((Ms1/RFAI)*100,)
    else:
      total_Ms1_per =0
    if Ms1 >0:
      total_Ms2_per=round((Ms2/Ms1)*100,)
    else:
      total_Ms2_per=0

    total_Ms1_ageing_0_15=perticularWeekObjects.filter(MS1=None, Internal_RFAI_Vs_Ms1_In_Days = "0-15").count()
    total_Ms1_ageing_16_30=perticularWeekObjects.filter(MS1=None, Internal_RFAI_Vs_Ms1_In_Days = "16-30").count()
    total_Ms1_ageing_31_60=perticularWeekObjects.filter(MS1=None, Internal_RFAI_Vs_Ms1_In_Days = "31-60").count()
    total_Ms1_ageing_61_90=perticularWeekObjects.filter(MS1=None,Internal_RFAI_Vs_Ms1_In_Days = "61-90").count()
    total_Ms1_ageing_GT90=perticularWeekObjects.filter(MS1=None,Internal_RFAI_Vs_Ms1_In_Days = "GT90").count()   
    
    total_Ms2_ageing_0_15=perticularWeekObjects.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "0-15").count()
    total_Ms2_ageing_16_30=perticularWeekObjects.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "16-30").count()
    total_Ms2_ageing_31_60=perticularWeekObjects.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "31-60").count()
    total_Ms2_ageing_61_90=perticularWeekObjects.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "61-90").count()
    total_Ms2_ageing_GT90=perticularWeekObjects.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "GT90").count()
    total_projectwise_data={}
    total_projectwise_data["Total"]={   "RFAI":total_RFAI,
                                        "Ms1":total_Ms1,
                                        "RFAI_Ms1_Gap":total_RFAI_Ms1_Gap,
                                        "Ms1_per":total_Ms1_per,
                                        "Ms2":total_Ms2,
                                        "Ms1_Ms2_Gap":total_Ms1_Ms2_Gap,
                                        "Ms2_per":total_Ms2_per,

                                        "Ms1_ageing_0_15":total_Ms1_ageing_0_15,
                                        "Ms1_ageing_16_30":total_Ms1_ageing_16_30,
                                        "Ms1_ageing_31_60":total_Ms1_ageing_31_60,
                                        "Ms1_ageing_61_90":total_Ms1_ageing_61_90,
                                        "Ms1_ageing_GT90":total_Ms1_ageing_GT90,

                                        "Ms2_ageing_0_15":total_Ms2_ageing_0_15,
                                        "Ms2_ageing_16_30":total_Ms2_ageing_16_30,
                                        "Ms2_ageing_31_60":total_Ms2_ageing_31_60,
                                        "Ms2_ageing_61_90":total_Ms2_ageing_61_90,
                                        "Ms2_ageing_GT90":total_Ms2_ageing_GT90
                                        }
    circlewise_data["Total"]=total_projectwise_data

    return circlewise_data

@ api_view(["POST","GET"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def overall_Dashboard_off(request):
      
      upload_week=request.POST.get("Upload_Week")
      perticularWeekObjects = WPR_DPR2_Table.objects.filter(WEEK = upload_week)
    
    
      ############################################# Code for filtering #########################################
      project_filter=request.POST.get("project")
      print("project filter-------------",project_filter)
      if project_filter != "":
          project_filter=project_filter.split(",")
          print("project filter-------------",project_filter)
          perticularWeekObjects=perticularWeekObjects.filter(Project__in=project_filter)

     
      circle_filter=request.POST.get("circle")
      print("circle filter-------------",circle_filter)
      if circle_filter != "":
           circle_filter=circle_filter.split(",")
           print("circle filter-------------",circle_filter)
           perticularWeekObjects=perticularWeekObjects.filter(CIRCLE__in=circle_filter)
      if len(perticularWeekObjects) != 0:
          ###################################### code for project wise dashboard(Dashboard 2) #####################################
        
          Projects=project_list(perticularWeekObjects)
          print(Projects)
        
          overall_projectwise_data={}
          for project in Projects:
              
              project_obj=perticularWeekObjects.filter(Project = project)
              
              RFAI=project_obj.exclude(RFAI = None).count()
              Ms1=project_obj.exclude(MS1 = None).count()
              Ms2=project_obj.exclude(MAPA = None).count()

              Ms2_Gap=Ms1-Ms2
              if RFAI >0:
                Ms1_per=round((Ms1/RFAI)*100,)
              else:
                  Ms1_per =0
              if Ms1 >0:
                Ms2_per=round((Ms2/Ms1)*100,)
              else:
                  Ms2_per=0
              
              overall_projectwise_data[project]={"RFAI":RFAI,"Ms1":Ms1,"Ms2":Ms2,"Ms2_Gap":Ms2_Gap,"Ms1_Per":Ms1_per,"Ms2_per":Ms2_per}


          #################################### code for total of the project wise data(Dashboard 2) #######################
          total_RFAI=perticularWeekObjects.exclude(RFAI = None).count()
          total_Ms1=perticularWeekObjects.exclude(MS1 = None).count()
          total_Ms2=perticularWeekObjects.exclude(MAPA = None).count()
          
          total_Ms2_Gap=Ms1-Ms2
          total_Ms1_per=round((total_Ms1/total_RFAI)*100,)
          total_Ms2_per=round((total_Ms2/total_Ms1)*100,)

          overall_projectwise_data["Total"]={"RFAI":total_RFAI,"Ms1":total_Ms1,"Ms2":total_Ms2,"Ms2_Gap":total_Ms2_Gap,"Ms1_Per":total_Ms1_per,"Ms2_per":total_Ms2_per}
          

          ###################################################### OverAll data (dashboard 1) ######################################################
          overall_data = {"total_RFAI":total_RFAI,"total_Ms1":total_Ms1,"total_Ms2":total_Ms2,"total_Ms1_per":total_Ms1_per,"total_Ms2_per":total_Ms2_per} 

          ####################################################### code for circlewise data (Dashboard 3) #########################################
          circles=circle_list(perticularWeekObjects)
          print(circles)
        
          overall_circlewise_data={}
          for circle in circles:
              
              circle_obj=perticularWeekObjects.filter(CIRCLE = circle)
              
              RFAI=circle_obj.exclude(RFAI = None).count()
              Ms1=circle_obj.exclude(MS1 = None).count()
              Ms2=circle_obj.exclude(MAPA = None).count()
              
              RFAI_Ms1_Gap = RFAI - Ms1
              Ms1_Ms2_Gap=Ms1-Ms2
              
              # Ms1_per=round((Ms1/RFAI)*100,)
              # Ms2_per=round((Ms2/Ms1)*100,)
              if RFAI >0:
                Ms1_per=round((Ms1/RFAI)*100,)
              else:
                Ms1_per =0
              if Ms1 >0:
                Ms2_per=round((Ms2/Ms1)*100,)
              else:
                Ms2_per=0
              
              overall_circlewise_data[circle]={"RFAI":RFAI,"Ms1":Ms1,"Ms2":Ms2,"RFAI_Ms1_Gap":RFAI_Ms1_Gap,"Ms1_Ms2_Gap":Ms1_Ms2_Gap,"Ms1_Per":Ms1_per,"Ms2_per":Ms2_per}


          #################################### code for total of the project wise data () #######################
          total_RFAI=perticularWeekObjects.exclude(RFAI = None).count()
          total_Ms1=perticularWeekObjects.exclude(MS1 = None).count()
          total_Ms2=perticularWeekObjects.exclude(MAPA = None).count()
          
          total_RFAI_Ms1_Gap = RFAI - Ms1
          total_Ms1_Ms2_Gap=Ms1-Ms2
          total_Ms1_per=round((total_Ms1/total_RFAI)*100,)
          total_Ms2_per=round((total_Ms2/total_Ms1)*100,)

          overall_circlewise_data["Total"]={"RFAI":total_RFAI,"Ms1":total_Ms1,"Ms2":total_Ms2,"RFAI_Ms1_Gap":total_RFAI_Ms1_Gap,"Ms1_Ms2_Gap":total_Ms1_Ms2_Gap,"Ms1_Per":total_Ms1_per,"Ms2_per":total_Ms2_per}
          print("------------------------overall_circlewise_data-------------------------------")
          
          print(overall_circlewise_data)

          all_obj=WPR_DPR2_Table.objects.all()
          show_project=project_list(all_obj)
          show_circle=circle_list(all_obj)
          project_ageing_data =project_ageing(perticularWeekObjects)
          return Response({"status":True,"overall_data":overall_data,"overall_project_data":overall_projectwise_data,"overall_circlewise_data":overall_circlewise_data, "circles":show_circle,"project":show_project,"project_ageing":project_ageing_data})
          
      else:
           return Response({"status":False,"message":"No data found"})





@api_view(["GET","POST"])
def site_list_request_handler_projectWise(request):
      upload_week=request.POST.get("Upload_Week")
      perticularWeekObjects = WPR_DPR2_Table.objects.filter(WEEK = upload_week)

      ############################################# Code for filtering #########################################
      project_filter=request.POST.get("project")
      print("project filter-------------",project_filter)
      if project_filter != "":
          project_filter=project_filter.split(",")
          print("project filter-------------",project_filter)
          perticularWeekObjects=perticularWeekObjects.filter(Project__in=project_filter)

     
      circle_filter=request.POST.get("circle")
      print("circle filter-------------",circle_filter)
      if circle_filter != "":
           circle_filter=circle_filter.split(",")
           print("circle filter-------------",circle_filter)
           perticularWeekObjects=perticularWeekObjects.filter(CIRCLE__in=circle_filter)

      s_project=request.POST.get("s_project")
      pro_object=perticularWeekObjects.filter(Project=s_project)
      
      column_filter=request.POST.get("column_filter")
      if column_filter == "RFAI":
        Objects=pro_object.exclude(RFAI= None)
      if column_filter == "MS1":
        Objects=pro_object.exclude(MS1 = None)
      if column_filter == "MS2":
        Objects=pro_object.exclude(MAPA = None)
      
      # Objects=pro_object.exclude(eval(column_filter + ' = ' + "as"))

      site_list = Objects.values_list('SITE_ID', flat=True)
      print("---------------------------",site_list)
      return Response({"status":True,"site_list":site_list})

 ##############################################    below code is not in use right now #################################
@ api_view(["GET","POST"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def projectAgeing(request):
    
    upload_week=request.POST.get("Upload_Week")
    print("upload_week -------------------",upload_week)

    perticularWeekObjects = WPR_DPR2_Table.objects.filter(WEEK = upload_week)
    ############################################# Code for filtering #########################################

    project_filter=request.POST.get("project")
    print("project filter-------------",project_filter)
    
    
    if project_filter != "":
        project_filter=project_filter.split(",")
        print("project filter-------------",project_filter)
        perticularWeekObjects=perticularWeekObjects.filter(Project__in=project_filter)
    
    circle_filter=request.POST.get("circle")
    print("circle filter-------------",circle_filter)
    
    
    
    if circle_filter != "":
          circle_filter=circle_filter.split(",")
          print("circle filter-------------",circle_filter)
          perticularWeekObjects=perticularWeekObjects.filter(CIRCLE__in=circle_filter)
    
    #########################################                   ###################################################
    circles=circle_list(perticularWeekObjects)
    print(circles)
    circlewise_data={}
    for circle in circles:
          circle_obj=perticularWeekObjects.filter(CIRCLE = circle)
          projects=project_list(circle_obj)
          print(projects)
          projectwise_data={}
          for project in projects:
              project_obj=circle_obj.filter(Project = project)
              RFAI=project_obj.exclude(RFAI = None).count()
              Ms1=project_obj.exclude(MS1 = None).count()
              Ms2=project_obj.exclude(MAPA = None).count()

              RFAI_Ms1_Gap = RFAI - Ms1
              Ms1_Ms2_Gap=Ms1-Ms2
              # Ms1_per=round((Ms1/RFAI)*100,2)
              # Ms2_per=round((Ms2/Ms1)*100,2)

              if RFAI >0:
                Ms1_per=round((Ms1/RFAI)*100,)
              else:
                Ms1_per =0
              if Ms1 >0:
                Ms2_per=round((Ms2/Ms1)*100,)
              else:
                Ms2_per=0
              
              ########################################### MS1 ageing #####################################
              Ms1_ageing_0_15=project_obj.filter(MS1=None, Internal_RFAI_Vs_Ms1_In_Days = "0-15").count()
              Ms1_ageing_16_30=project_obj.filter(MS1=None, Internal_RFAI_Vs_Ms1_In_Days = "16-30").count()
              Ms1_ageing_31_60=project_obj.filter(MS1=None, Internal_RFAI_Vs_Ms1_In_Days = "31-60").count()
              Ms1_ageing_61_90=project_obj.filter(MS1=None,Internal_RFAI_Vs_Ms1_In_Days = "61-90").count()
              Ms1_ageing_GT90=project_obj.filter(MS1=None,Internal_RFAI_Vs_Ms1_In_Days = "GT90").count()   
              
              ########################################## MS2 ageing ########################################
              Ms2_ageing_0_15=project_obj.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "0-15").count()
              Ms2_ageing_16_30=project_obj.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "16-30").count()
              Ms2_ageing_31_60=project_obj.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "31-60").count()
              Ms2_ageing_61_90=project_obj.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "61-90").count()
              Ms2_ageing_GT90=project_obj.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "GT90").count() 

              projectwise_data[project]={"RFAI":RFAI,
                                        "Ms1":Ms1,
                                        "RFAI_Ms1_Gap":RFAI_Ms1_Gap,
                                        "Ms1_per":Ms1_per,
                                        "Ms2":Ms2,
                                        "Ms1_Ms2_Gap":Ms1_Ms2_Gap,
                                        "Ms2_per":Ms2_per,

                                        "Ms1_ageing_0_15":Ms1_ageing_0_15,
                                        "Ms1_ageing_16_30":Ms1_ageing_16_30,
                                        "Ms1_ageing_31_60":Ms1_ageing_31_60,
                                        "Ms1_ageing_61_90":Ms1_ageing_61_90,
                                        "Ms1_ageing_GT90":Ms1_ageing_GT90,

                                        "Ms2_ageing_0_15":Ms2_ageing_0_15,
                                        "Ms2_ageing_16_30":Ms2_ageing_16_30,
                                        "Ms2_ageing_31_60":Ms2_ageing_31_60,
                                        "Ms2_ageing_61_90":Ms2_ageing_61_90,
                                        "Ms2_ageing_GT90":Ms2_ageing_GT90
                                        }
          circlewise_data[circle]=projectwise_data

    total_RFAI=perticularWeekObjects.exclude(RFAI = None).count()
    total_Ms1=perticularWeekObjects.exclude(MS1 = None).count()
    total_Ms2=perticularWeekObjects.exclude(MAPA = None).count()

    total_RFAI_Ms1_Gap = RFAI - Ms1
    total_Ms1_Ms2_Gap=Ms1-Ms2
    # Ms1_per=round((Ms1/RFAI)*100,2)
    # Ms2_per=round((Ms2/Ms1)*100,2)

    if RFAI >0:
      total_Ms1_per=round((Ms1/RFAI)*100,)
    else:
      total_Ms1_per =0
    if Ms1 >0:
      total_Ms2_per=round((Ms2/Ms1)*100,)
    else:
      total_Ms2_per=0

    total_Ms1_ageing_0_15=perticularWeekObjects.filter(MS1=None, Internal_RFAI_Vs_Ms1_In_Days = "0-15").count()
    total_Ms1_ageing_16_30=perticularWeekObjects.filter(MS1=None, Internal_RFAI_Vs_Ms1_In_Days = "16-30").count()
    total_Ms1_ageing_31_60=perticularWeekObjects.filter(MS1=None, Internal_RFAI_Vs_Ms1_In_Days = "31-60").count()
    total_Ms1_ageing_61_90=perticularWeekObjects.filter(MS1=None,Internal_RFAI_Vs_Ms1_In_Days = "61-90").count()
    total_Ms1_ageing_GT90=perticularWeekObjects.filter(MS1=None,Internal_RFAI_Vs_Ms1_In_Days = "GT90").count()   
    
    total_Ms2_ageing_0_15=perticularWeekObjects.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "0-15").count()
    total_Ms2_ageing_16_30=perticularWeekObjects.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "16-30").count()
    total_Ms2_ageing_31_60=perticularWeekObjects.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "31-60").count()
    total_Ms2_ageing_61_90=perticularWeekObjects.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "61-90").count()
    total_Ms2_ageing_GT90=perticularWeekObjects.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "GT90").count()
    total_projectwise_data={}
    total_projectwise_data["Total"]={   "RFAI":total_RFAI,
                                        "Ms1":total_Ms1,
                                        "RFAI_Ms1_Gap":total_RFAI_Ms1_Gap,
                                        "Ms1_per":total_Ms1_per,
                                        "Ms2":total_Ms2,
                                        "Ms1_Ms2_Gap":total_Ms1_Ms2_Gap,
                                        "Ms2_per":total_Ms2_per,

                                        "Ms1_ageing_0_15":total_Ms1_ageing_0_15,
                                        "Ms1_ageing_16_30":total_Ms1_ageing_16_30,
                                        "Ms1_ageing_31_60":total_Ms1_ageing_31_60,
                                        "Ms1_ageing_61_90":total_Ms1_ageing_61_90,
                                        "Ms1_ageing_GT90":total_Ms1_ageing_GT90,

                                        "Ms2_ageing_0_15":total_Ms2_ageing_0_15,
                                        "Ms2_ageing_16_30":total_Ms2_ageing_16_30,
                                        "Ms2_ageing_31_60":total_Ms2_ageing_31_60,
                                        "Ms2_ageing_61_90":total_Ms2_ageing_61_90,
                                        "Ms2_ageing_GT90":total_Ms2_ageing_GT90
                                        }
    circlewise_data["Total"]=total_projectwise_data
          
    return Response({"status":True,"project_ageing":circlewise_data})      
              
  ###################################### *************************************** ##########################################            


@api_view(["GET","POST"])
def weeklyComparision_off(request):
    week_list_str = request.POST.get("week_list")
    
    if week_list_str != "":
        week_list = week_list_str.split(",")
        print("--------------------------------------------------------requested weeks-----------------------------------------")
        print(week_list)

    else:
            
        # Get the current date
        current_date = datetime.date.today()
        # Get the ISO calendar week number
        current_week_number = current_date.isocalendar()[1]
        week_list=[current_week_number-1,current_week_number-2,current_week_number-3,current_week_number-4,current_week_number-5]
        print("------------------------------------------------------default week-----------------------------------------")
        print(week_list)
    weekwise_data={}    
    for week in week_list:
        print("week_number: ",week)
        perticularWeekObjects= WPR_DPR2_Table.objects.filter(WEEK = week)
        circles=circle_list(perticularWeekObjects)
        print(circles)
        circlewise_data={}
        for circle in circles:
              circle_obj=perticularWeekObjects.filter(CIRCLE = circle)
              # projects=project_list(circle_obj)
              projects=project_list(WPR_DPR2_Table.objects.all())
              print(projects)
              projectwise_data={}
              for project in projects:
                  project_obj=circle_obj.filter(Project = project)
                  
                  
                  ########################################### MS1 ageing #####################################
                  Ms1_ageing_0_15=project_obj.filter(MS1=None, Internal_RFAI_Vs_Ms1_In_Days = "0-15").count()
                  Ms1_ageing_16_30=project_obj.filter(MS1=None, Internal_RFAI_Vs_Ms1_In_Days = "16-30").count()
                  Ms1_ageing_31_60=project_obj.filter(MS1=None, Internal_RFAI_Vs_Ms1_In_Days = "31-60").count()
                  Ms1_ageing_61_90=project_obj.filter(MS1=None,Internal_RFAI_Vs_Ms1_In_Days = "61-90").count()
                  Ms1_ageing_GT90=project_obj.filter(MS1=None,Internal_RFAI_Vs_Ms1_In_Days = "GT90").count()   
                  
                  ########################################## MS2 ageing ########################################
                  Ms2_ageing_0_15=project_obj.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "0-15").count()
                  Ms2_ageing_16_30=project_obj.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "16-30").count()
                  Ms2_ageing_31_60=project_obj.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "31-60").count()
                  Ms2_ageing_61_90=project_obj.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "61-90").count()
                  Ms2_ageing_GT90=project_obj.filter(MAPA=None,Internal_Ms1_Vs_Ms2_In_days = "GT90").count() 

                  projectwise_data[project]={
                                            "Ms1_ageing_0_15":Ms1_ageing_0_15,
                                            "Ms1_ageing_16_30":Ms1_ageing_16_30,
                                            "Ms1_ageing_31_60":Ms1_ageing_31_60,
                                            "Ms1_ageing_61_90":Ms1_ageing_61_90,
                                            "Ms1_ageing_GT90":Ms1_ageing_GT90,

                                            "Ms2_ageing_0_15":Ms2_ageing_0_15,
                                            "Ms2_ageing_16_30":Ms2_ageing_16_30,
                                            "Ms2_ageing_31_60":Ms2_ageing_31_60,
                                            "Ms2_ageing_61_90":Ms2_ageing_61_90,
                                            "Ms2_ageing_GT90":Ms2_ageing_GT90
                                            }
              circlewise_data[circle]=projectwise_data
        weekwise_data[week]=circlewise_data

    return Response({"status":True,"weeklwise_data":weekwise_data,"circle_list":all_circle_list()})    




@api_view(["GET","POST"])
def weeklyComparision(request):
    week_list_str = request.POST.get("week_list")
    
    if week_list_str != "":
        week_list = week_list_str.split(",")
        print("--------------------------------------------------------requested weeks-----------------------------------------")
        print(week_list)
    else:       
        # Get the current date
        current_date = datetime.date.today()
        # Get the ISO calendar week number
        current_week_number = current_date.isocalendar()[1]
        week_list=[current_week_number-1,current_week_number-2,current_week_number-3,current_week_number-4,current_week_number-5]
        print("------------------------------------------------------default week-----------------------------------------")
        print(week_list)
    perticularWeekObjects= WPR_DPR2_Table.objects.filter(WEEK__in = week_list)
    
    serializers=ser_Soft_At_Table(perticularWeekObjects,many=True) 

    # weekly_data={}
    # for week in week_list:
    #     perticularWeekObjects= WPR_DPR2_Tabl                                                        e.objects.filter(WEEK = week)
    
    #     serializers=ser_Soft_At_Table(perticularWeekObjects,many=True) 
    #     weekly_data[week]=serializers.data

    return Response({"status":True,
                     "weeklwise_data":serializers.data,
                    #  "weeklwise_data":weekly_data,
                     "circle_list":all_circle_list()})


# def cursor_to_dict(cursor):
#     columns = [column[0] for column in cursor.description]
#     result_set = cursor.fetchall()

#     # Create a list of dictionaries, where each dictionary represents a row
#     result_dict_list = [dict(zip(columns, row)) for row in result_set]

#     return result_dict_list

@api_view(["GET","POST"])
def weeklyComparision_dashboard(request):
    week_list_str = request.POST.get("week_list")
    Ageing_str = request.POST.get("Ageing")
    Ageing_list = Ageing_str.split(",")
    if len(Ageing_list)==1:
        Ageing=Ageing_list[0]
    else:
        Ageing=tuple(Ageing_list)

    MS1_MS2= request.POST.get("MS1_MS2")
 
    if week_list_str != "":
        week_list = week_list_str.split(",")
        print("--------------------------------------------------------requested weeks-----------------------------------------")
        print(week_list)
    else:       
        # Get the current date
        current_date = datetime.date.today()
        # Get the ISO calendar week number
        current_week_number = current_date.isocalendar()[1]
        week_list=[current_week_number-1,current_week_number-2,current_week_number-3,current_week_number-4,current_week_number-5]
        print("------------------------------------------------------default week-----------------------------------------")
        print(week_list)
    week_list=tuple(week_list)
    with connection.cursor() as cursor:
      # Your raw SQL query
      
      if MS1_MS2 == "MS1":
        if len(Ageing_list)==1: 
          sql_query = '''SELECT "WEEK","CIRCLE","Project","Internal_RFAI_Vs_Ms1_In_Days","MS1" FROM public."WPR_DPR2_wpr_dpr2_table" WHERE "Internal_RFAI_Vs_Ms1_In_Days"='''+"""'""" + str(Ageing) +"""'"""+'''  AND "MS1" IS NULL AND "WEEK" IN ''' + str(week_list) +''';'''
        else:
          sql_query = '''SELECT "WEEK","CIRCLE","Project","Internal_RFAI_Vs_Ms1_In_Days","MS1" FROM public."WPR_DPR2_wpr_dpr2_table" WHERE "Internal_RFAI_Vs_Ms1_In_Days" IN ''' + str(Ageing) + '''  AND "MS1" IS NULL AND "WEEK" IN ''' + str(week_list) +''';'''
      # Ageing="sk"
      if MS1_MS2 == "MS2":
        if len(Ageing_list)==1:
          sql_query = '''SELECT "WEEK","CIRCLE","Project","Internal_Ms1_Vs_Ms2_In_days","MAPA" FROM public."WPR_DPR2_wpr_dpr2_table" WHERE "Internal_Ms1_Vs_Ms2_In_days"='''+"""'""" + str(Ageing) +"""'"""+'''  AND "MAPA" IS NULL AND "WEEK" IN ''' + str(week_list) +''';'''
        else:
          sql_query = '''SELECT "WEEK","CIRCLE","Project","Internal_Ms1_Vs_Ms2_In_days","MAPA" FROM public."WPR_DPR2_wpr_dpr2_table" WHERE "Internal_Ms1_Vs_Ms2_In_days" IN ''' + str(Ageing) + '''  AND "MAPA" IS NULL AND "WEEK" IN ''' + str(week_list) +''';'''
      cursor.execute(sql_query)
      # print(cursor_to_dict(cursor))
      # Fetch the result
      raw_result = cursor.fetchall()
      print("raw_result:",raw_result)
    
    df=pd.DataFrame(raw_result,columns=["WEEK","CIRCLE","Project","Internal_RFAI_Vs_Ms1_In_Days","MS1"])
    print(df)

    pv_df=df.pivot_table(index=["CIRCLE","Project"],columns=["WEEK"],aggfunc='count',values="Internal_RFAI_Vs_Ms1_In_Days")
    pv_df=pv_df.fillna(value=0).astype(int)
    
    cl=pv_df.columns.to_list()
    print(cl)
    pv_df = pv_df.reset_index()
    json_data = pv_df.to_json(orient='records')
    print(json_data)

   


        

    return Response({"data":json_data,"week_cols":cl})
    # return JsonResponse(json_data,safe=False)

@api_view(["GET","POST"])
def overAll_Dashboard(request):
      # project_filter=request.POST.get("project")
      # print("project filter-------------",project_filter)
      # if project_filter != "":
      #     project_filter=project_filter.split(",")
      #     print("project filter-------------",project_filter)
      #     perticularWeekObjects=perticularWeekObjects.filter(Project__in=project_filter)

     
      # circle_filter=request.POST.get("circle")
      # print("circle filter-------------",circle_filter)
      # if circle_filter != "":
      #      circle_filter=circle_filter.split(",")
      #      print("circle filter-------------",circle_filter)
      #      perticularWeekObjects=perticularWeekObjects.filter(CIRCLE__in=circle_filter)

      with connection.cursor() as cursor:
            sql_query=''' SELECT "CIRCLE","Project",
                          count("RFAI") AS "RFAII",
                          COUNT("MS1") AS "MS1 DONE",
                          (count("RFAI")-COUNT("MS1")) as "MS1 Pendency",
                          CAST(trunc(((COUNT("MS1")::DECIMAL / COUNT("RFAI")::DECIMAL)*100)) AS BIGINT) AS "MS1 %",
                          COUNT("MAPA") AS "MS2 DONE",
                          (count("MS1")-COUNT("MAPA")) as "MS2 Pendency",
                          CAST(trunc(((COUNT("MAPA")::DECIMAL / COUNT("MS1")::DECIMAL)*100)) AS BIGINT) AS "MS2 %",

                          SUM(CASE WHEN "Internal_RFAI_Vs_Ms1_In_Days"='0-15' AND "MS1" IS NULL THEN 1
                          ELSE 0
                          END) AS "MS1_0_15",
                          SUM(CASE WHEN "Internal_RFAI_Vs_Ms1_In_Days"='16-30' AND "MS1" IS NULL THEN 1
                          ELSE 0
                          END) AS "MS1_16_30",
                          SUM(CASE WHEN "Internal_RFAI_Vs_Ms1_In_Days"='31-60' AND "MS1" IS NULL THEN 1
                          ELSE 0
                          END) AS "MS1_31_60",
                          SUM(CASE WHEN "Internal_RFAI_Vs_Ms1_In_Days"='61-90' AND "MS1" IS NULL THEN 1
                          ELSE 0
                          END) AS "MS1_61_90",
                          SUM(CASE WHEN "Internal_RFAI_Vs_Ms1_In_Days"='GT90' AND "MS1" IS NULL THEN 1
                          ELSE 0
                          END) AS "MS1_GT90",

                        
                          SUM(CASE WHEN "Internal_Ms1_Vs_Ms2_In_days"='0-15' AND "MAPA" IS NULL THEN 1
                          ELSE 0
                          END) AS "MS2_0_15",
                          SUM(CASE WHEN "Internal_Ms1_Vs_Ms2_In_days"='16-30' AND "MAPA" IS NULL THEN 1
                          ELSE 0
                          END) AS "MS2_16_30",
                          SUM(CASE WHEN "Internal_Ms1_Vs_Ms2_In_days"='31-60' AND "MAPA" IS NULL THEN 1
                          ELSE 0
                          END) AS "MS2_31_60",
                          SUM(CASE WHEN "Internal_Ms1_Vs_Ms2_In_days"='61-90' AND "MAPA" IS NULL THEN 1
                          ELSE 0
                          END) AS "MS2_61_90",
                          SUM(CASE WHEN "Internal_Ms1_Vs_Ms2_In_days"='GT90' AND "MAPA" IS NULL THEN 1
                          ELSE 0
                          END) AS "MS2_GT90"


                          FROM public."WPR_DPR2_wpr_dpr2_table"
                          WHERE "WEEK"=29 
                          GROUP BY "CIRCLE","Project"
                          ORDER BY "CIRCLE" '''
            cursor.execute(sql_query)
            # print(cursor_to_dict(cursor))
            # Fetch the result
            raw_result = cursor.fetchall()
            print("raw_result:",raw_result)
      df_project_ageing=pd.DataFrame(raw_result,columns=["CIRCLE",
                                          "Project",
                                          "RFAI",
                                          "MS1_DONE",
                                          "MS1_Pendency",
                                          "MS1_per",
                                          "MS2_DONE",
                                          "MS2_Pendency",
                                          "MS2_per",

                                          "MS1_0_15",
                                          "MS1_16_30",
                                          "MS1_31_60",
                                          "MS1_61_90",
                                          "MS1_GT90",

                                          "MS2_0_15",
                                          "MS2_16_30",
                                          "MS2_31_60",
                                          "MS2_61_90",
                                          "MS2_GT90",
                                          ])
      
      total_project_ageing = df_project_ageing.sum(numeric_only=True)
      df_project_ageing.loc["total"]=total_project_ageing
      print(df_project_ageing)
      data_project_ageing = df_project_ageing.to_json(orient='records')
      


      with connection.cursor() as cursor:
            sql_query='''SELECT "CIRCLE",
                        count("RFAI") AS "RFAII",
                        COUNT("MS1") AS "MS1 DONE",
                        (count("RFAI")-COUNT("MS1")) as "RAFI vs MS1 GAP",
                        COUNT("MAPA") AS "MS2 DONE",
                        (count("MS1")-COUNT("MAPA")) as "MS2 Pendency",
                        trunc(((COUNT("MS1")::DECIMAL / COUNT("RFAI")::DECIMAL)*100)) AS "MS1 %",
                        trunc(((COUNT("MAPA")::DECIMAL / COUNT("MS1")::DECIMAL)*100)) AS "MS2 %"

                        FROM public."WPR_DPR2_wpr_dpr2_table"
                        WHERE "WEEK"=29 
                        GROUP BY "CIRCLE"
                        ORDER BY "CIRCLE"'''
            
            cursor.execute(sql_query)
            # print(cursor_to_dict(cursor))
            # Fetch the result
            raw_result = cursor.fetchall()
            print("raw_result:",raw_result)
      df_circle_wise=pd.DataFrame(raw_result,columns=[
                                          "CIRCLE",
                                          "RFAI",
                                          "MS1_DONE",
                                          "RAFI_vs_MS1_GAP",
                                          "MS2_DONE",
                                          "MS2_Pendency",
                                          "MS1_per",
                                          "MS2_per",
                                          ])
      total_circle_wise = df_circle_wise.sum(numeric_only=True)
      df_circle_wise.loc["total"]=total_circle_wise
      print(df_circle_wise)
      data_circle_wise = df_circle_wise.to_json(orient='records')

      ######################### project ageing ##############################
      with connection.cursor() as cursor:
            sql_query=''' SELECT "Project",
                          count("RFAI") AS "RFAII",
                          COUNT("MS1") AS "MS1 DONE",
                          
                          COUNT("MAPA") AS "MS2 DONE",
                          (count("MS1")-COUNT("MAPA")) as "MS2 GAP",
                          trunc(((COUNT("MS1")::DECIMAL / COUNT("RFAI")::DECIMAL)*100)) AS "MS1 %",
                          trunc(((COUNT("MAPA")::DECIMAL / COUNT("MS1")::DECIMAL)*100)) AS "MS2 %"

                          FROM public."WPR_DPR2_wpr_dpr2_table"
                          WHERE "WEEK"=29 
                          GROUP BY "Project"
                          ORDER BY "Project" '''
            cursor.execute(sql_query)
            # print(cursor_to_dict(cursor))
            # Fetch the result
            raw_result = cursor.fetchall()
            print("raw_result:",raw_result)
            df_project_wise=pd.DataFrame(raw_result,columns=[
                                          "Project",                                          
                                          "RFAI",
                                          "MS1_DONE",                                          
                                          "MS2_DONE",
                                          "MS2_GAP",
                                          "MS1_per",
                                          "MS2_per",
                                          ])
      print(df_project_wise)
      data_project_wise = df_project_wise.to_json(orient='records')
      with connection.cursor() as cursor:
            sql_query=''' SELECT 
                          count("RFAI") AS "RFAI",
                          COUNT("MS1") AS "MS1 DONE",
                          COUNT("MAPA") AS "MS2 DONE"
                          FROM public."WPR_DPR2_wpr_dpr2_table"
                          WHERE "WEEK"=29 '''
            cursor.execute(sql_query)
            # print(cursor_to_dict(cursor))
            # Fetch the result
            raw_result = cursor.fetchall()
            print("raw_result:",raw_result)
            print("------------------",raw_result,"----------------------")
            rfai=raw_result[0][0]
            ms1=raw_result[0][1]
            ms2=raw_result[0][2]
            # ms1_per= round((rfai/ms1)*100,)
            # ms2_per= round((ms1/ms2)*100,)
            if rfai >0:
                ms1_per=round((ms1/rfai)*100,)
            else:
              ms1_per =0
            if ms1 >0:
              ms2_per=round((ms2/ms1)*100,)
            else:
              ms2_per=0
            all_data={"total_RFAI":rfai,"total_Ms1":ms1,"total_Ms1_per":ms1_per,"total_Ms2":ms2,"total_Ms2_per":ms2_per}
      return Response({"status":True,"project_ageing_data":data_project_ageing,"data_circle_wise":data_circle_wise,"data_project_wise":data_project_wise,"all_data":all_data})
  
        


@api_view(["GET","POST"])
# def weeklyComparision_dashboard_off(request):
def testing(request):
  week_list_str = request.POST.get("week_list")
  week_list = week_list_str.split(",")
  Ageing_str = request.POST.get("Ageing")
  Ageing_list = Ageing_str.split(",")
  # circle = request.POST.get("circle")
  queryset = WPR_DPR2_Table.objects.filter(WEEK__in=week_list,MS1=None,Internal_RFAI_Vs_Ms1_In_Days__in=Ageing_list).values("CIRCLE","Project","WEEK","CIRCLE","Project","Internal_RFAI_Vs_Ms1_In_Days","MAPA")
  df = pd.DataFrame(queryset)
  print(df)
  df=df.to_dict(orient="records")
  print(df)
  return JsonResponse(df, safe=False)


# @api_view(["GET","POST"])
# def weeklyComparision_dashboard_off(request):
#     week_list_str = request.POST.get("week_list")
    
    
#     if week_list_str != "":
#         week_list = week_list_str.split(",")
#         print("--------------------------------------------------------requested weeks-----------------------------------------")
#         print(week_list)
#     else:       
#         # Get the current date
#         current_date = datetime.date.today()
#         # Get the ISO calendar week number
#         current_week_number = current_date.isocalendar()[1]
#         week_list=[current_week_number-1,current_week_number-2,current_week_number-3,current_week_number-4,current_week_number-5]
#         print("------------------------------------------------------default week-----------------------------------------")
#         print(week_list)
#     week_list=tuple(week_list)
   
#     sql_query = '''SELECT "CIRCLE","Project","MS1",COUNT(1) "TOTAL","WEEK" FROM public."WPR_DPR2_wpr_dpr2_table" WHERE  "MS1" IS NULL AND "WEEK" IN ''' + str(week_list) +''' AND "Internal_RFAI_Vs_Ms1_In_Days"=''' +str(Ageing)+''' GROUP BY "Project","CIRCLE","MS1","WEEK";'''
#     result_set = WPR_DPR2_Table.objects.raw(sql_query)
#     for x in result_set:
#       print(x.CIRCLE)
    
#     return Response({"status":True,'data':result_set})

    

# ---FOR PROJECT AGEING---
# SELECT "CIRCLE","Project",
# count("RFAI") AS "RFAII",
# COUNT("MS1") AS "MS1 DONE",
# (count("RFAI")-COUNT("MS1")) as "MS1 Pendency",
# trunc(((COUNT("MS1")::DECIMAL / COUNT("RFAI")::DECIMAL)*100)) AS "MS1 %",
# COUNT("MAPA") AS "MS2 DONE",
# (count("MS1")-COUNT("MAPA")) as "MS2 Pendency",
# trunc(((COUNT("MAPA")::DECIMAL / COUNT("MS1")::DECIMAL)*100)) AS "MS2 %",
# SUM(CASE WHEN "Internal_RFAI_Vs_Ms1_In_Days"='0-15' AND "MS1" IS NULL THEN 1
# ELSE 0
# END) AS "MS1_0-15",
# SUM(CASE WHEN "Internal_RFAI_Vs_Ms1_In_Days"='16-30' AND "MS1" IS NULL THEN 1
# ELSE 0
# END) AS "MS1_16-30",
# SUM(CASE WHEN "Internal_RFAI_Vs_Ms1_In_Days"='31-60' AND "MS1" IS NULL THEN 1
# ELSE 0
# END) AS "MS1_31-60",
# SUM(CASE WHEN "Internal_RFAI_Vs_Ms1_In_Days"='61-90' AND "MS1" IS NULL THEN 1
# ELSE 0
# END) AS "MS1_61-90",
# SUM(CASE WHEN "Internal_RFAI_Vs_Ms1_In_Days"='GT90' AND "MS1" IS NULL THEN 1
# ELSE 0
# END) AS "MS1_GT90",

# -- FOR MS2 AGING
# SUM(CASE WHEN "Internal_Ms1_Vs_Ms2_In_days"='0-15' AND "MAPA" IS NULL THEN 1
# ELSE 0
# END) AS "MS2_0-15",
# SUM(CASE WHEN "Internal_Ms1_Vs_Ms2_In_days"='16-30' AND "MAPA" IS NULL THEN 1
# ELSE 0
# END) AS "MS2_16-30",
# SUM(CASE WHEN "Internal_Ms1_Vs_Ms2_In_days"='31-60' AND "MAPA" IS NULL THEN 1
# ELSE 0
# END) AS "MS2_31-60",
# SUM(CASE WHEN "Internal_Ms1_Vs_Ms2_In_days"='61-90' AND "MAPA" IS NULL THEN 1
# ELSE 0
# END) AS "MS2_61-90",
# SUM(CASE WHEN "Internal_Ms1_Vs_Ms2_In_days"='GT90' AND "MAPA" IS NULL THEN 1
# ELSE 0
# END) AS "MS2_GT90"


# FROM public."WPR_DPR2_wpr_dpr2_table"
# WHERE "WEEK"=29 
# GROUP BY "CIRCLE","Project"
# ORDER BY "CIRCLE"


#----CIRCLE WISE ___
# SELECT "CIRCLE",
# count("RFAI") AS "RFAII",
# COUNT("MS1") AS "MS1 DONE",
# (count("RFAI")-COUNT("MS1")) as "RAFI vs MS1 GAP",
# COUNT("MAPA") AS "MS2 DONE",
# (count("MS1")-COUNT("MAPA")) as "MS2 Pendency",
# trunc(((COUNT("MS1")::DECIMAL / COUNT("RFAI")::DECIMAL)*100)) AS "MS1 %",
# trunc(((COUNT("MAPA")::DECIMAL / COUNT("MS1")::DECIMAL)*100)) AS "MS2 %"

# FROM public."WPR_DPR2_wpr_dpr2_table"
# WHERE "WEEK"=29 
# GROUP BY "CIRCLE"
# ORDER BY "CIRCLE"


# ---for project wise -----
# SELECT "Project",
# count("RFAI") AS "RFAII",
# COUNT("MS1") AS "MS1 DONE",
# -- (count("RFAI")-COUNT("MS1")) as "RAFI vs MS1 GAP",
# COUNT("MAPA") AS "MS2 DONE",
# (count("MS1")-COUNT("MAPA")) as "MS2 GAP",
# trunc(((COUNT("MS1")::DECIMAL / COUNT("RFAI")::DECIMAL)*100)) AS "MS1 %",
# trunc(((COUNT("MAPA")::DECIMAL / COUNT("MS1")::DECIMAL)*100)) AS "MS2 %"

# FROM public."WPR_DPR2_wpr_dpr2_table"
# WHERE "WEEK"=29 
# GROUP BY "Project"
# ORDER BY "Project"


