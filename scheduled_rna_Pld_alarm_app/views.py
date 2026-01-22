from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
import re
from mcom_website.settings import MEDIA_ROOT,MEDIA_URL
import os

data={'UNIQUE ID':'UNIQUE_ID',
        'BAND':'BAND',
        'Circle Project':'Circle_Project',
        'Allocation-Date':'Allocation_Date',
        'OEM_NAME (Nokia/ZTE/Ericsson/Huawei)':'OEM_NAME_Nokia_ZTE_Ericsson_Huawei',
        'TOCO_NAME':'TOCO_NAME',
        'EMF_SUBMISSION_DATE':'EMF_SUBMISSION_DATE',
        'SCFT_COMPLETION_DATE':'SCFT_COMPLETION_DATE',
        'MS1':'MS1',
        'Rfai vs MS1 ': 'Rfai_vs_MS1',
        'Reason for Delay over period of more than 14 Days ':'Reason_for_Delay_over_period_of_more_than_14_Days',
        'RFAI VS MS1- Responsibility':'FAI_VS_MS1_Responsibility',
        'PERFORMANCE_AT_ACCEPTANCE_DATE2':'PERFORMANCE_AT_ACCEPTANCE_DATE2',
        'Performance_AT_Status( Accepted/Rejected/Offered/Pending/Dismantle)':'performanceATStatusAcceptedRejectedOfferedPendingDismantle',
        'MS1 Vs Performance AT Acceptance- Ageing':'MS1_Vs_Performance_AT_Acceptance_Agein',
        'Reason for delay more than 15 days': 'Reason_for_delay_more_than_15_day',
        'MS1 VS MS2 Responsibility':'MS1_VS_MS2_Responsibilit',
        'Addition MS2 Remarks':'Addition_MS2_Remark',
        'Internal RFAI Vs Ms1-In Days':'Internal_RFAI_Vs_Ms1_In_Day',
        "('date', '')":'date',
        "('4G Data Volume [GB]', ' 00:00')":'Data_Volume_GB_01_00',
        "('4G Data Volume [GB]', ' 01:00')":'Data_Volume_GB_01_00',
        "('4G Data Volume [GB]', ' 02:00')":'Data_Volume_GB_02_00',
        "('4G Data Volume [GB]', ' 03:00')":'Data_Volume_GB_03_00',
        "('4G Data Volume [GB]', ' 04:00')":'Data_Volume_GB_04_00',
        "('4G Data Volume [GB]', ' 05:00')":'Data_Volume_GB_05_00',
        "('4G Data Volume [GB]', ' 06:00')":'Data_Volume_GB_06_00',
        "('4G Data Volume [GB]', ' 07:00')":'Data_Volume_GB_07_00',
        "('4G Data Volume [GB]', ' 08:00')":'Data_Volume_GB_08_00',
        "('4G Data Volume [GB]', ' 09:00')":'Data_Volume_GB_09_00',
        "('4G Data Volume [GB]', ' 10:00')":'Data_Volume_GB_10_00',
        "('4G Data Volume [GB]', ' 11:00')":'Data_Volume_GB_11_00',
        "('4G Data Volume [GB]', ' 12:00')":'Data_Volume_GB_12_00',
        "('4G Data Volume [GB]', ' 13:00')":'Data_Volume_GB_13_00',
        "('4G Data Volume [GB]', ' 14:00')":'Data_Volume_GB_14_00',
        "('4G Data Volume [GB]', ' 15:00')":'Data_Volume_GB_15_00',
        "('4G Data Volume [GB]', ' 16:00')":'Data_Volume_GB_16_00',
        "('4G Data Volume [GB]', ' 17:00')":'Data_Volume_GB_17_00',
        "('4G Data Volume [GB]', ' 18:00')":'Data_Volume_GB_18_00',
        "('4G Data Volume [GB]', ' 19:00')":'Data_Volume_GB_19_00',
        "('4G Data Volume [GB]', ' 20:00')":'Data_Volume_GB_20_00',
        "('4G Data Volume [GB]', ' 21:00')":'Data_Volume_GB_21_00',
        "('4G Data Volume [GB]', ' 22:00')":'Data_Volume_GB_22_00',
        "('4G Data Volume [GB]', ' 23:00')":'Data_Volume_GB_23_00',
        "('Radio NW Availability', ' 00:00')":'RNA_00_00',
        "('Radio NW Availability', ' 01:00')":'RNA_01_00',
        "('Radio NW Availability', ' 02:00')":'RNA_02_00',
        "('Radio NW Availability', ' 03:00')":'RNA_03_00',
        "('Radio NW Availability', ' 04:00')":'RNA_04_00',
        "('Radio NW Availability', ' 05:00')":'RNA_05_00',
        "('Radio NW Availability', ' 06:00')":'RNA_06_00',
        "('Radio NW Availability', ' 07:00')":'RNA_07_00',
        "('Radio NW Availability', ' 08:00')":'RNA_08_00',
        "('Radio NW Availability', ' 09:00')":'RNA_09_00',
        "('Radio NW Availability', ' 10:00')":'RNA_10_00',
        "('Radio NW Availability', ' 11:00')":'RNA_11_00',
        "('Radio NW Availability', ' 12:00')":'RNA_12_00',
        "('Radio NW Availability', ' 13:00')":'RNA_13_00',
        "('Radio NW Availability', ' 14:00')":'RNA_14_00',
        "('Radio NW Availability', ' 15:00')":'RNA_15_00',
        "('Radio NW Availability', ' 16:00')":'RNA_16_00',
        "('Radio NW Availability', ' 17:00')":'RNA_17_00',
        "('Radio NW Availability', ' 18:00')":'RNA_18_00',
        "('Radio NW Availability', ' 19:00')":'RNA_19_00',
        "('Radio NW Availability', ' 20:00')":'RNA_20_00',
        "('Radio NW Availability', ' 21:00')":'RNA_21_00',
        "('Radio NW Availability', ' 22:00')":'RNA_22_00',
        "('Radio NW Availability', ' 23:00')":'RNA_23_00',
        'Alarm Type':'Alarm_Type',
        'Severity':'Severity',
        'Alarm Time':'Alarm_Time',
        'Distinguished Name': 'Distinguished_Name',
        'Name':'Name',
        'Supplementary Information':'Supplementary_Information',
        'Origin Alarm Time':'Origin_Alarm_Time' }



@api_view(["POST"])
def generat_rna_ply_alrm_trend(request):
    ATP_file = request.FILES["ATP_file"] if 'ATP_file' in request.FILES else None
    RNA_PAYL_file = request.FILES["RNA_PAYL_file"] if 'RNA_PAYL_file' in request.FILES else None
    Alarm_file = request.FILES["Alarm_file"] if 'Alarm_file' in request.FILES else None


    ########################### checking required columns for the RNA Payload file #####################
#     columns_list_RNA_PAYL_file= pd.read_excel(RNA_PAYL_file,nrows=1).columns.tolist()
    columns_list_RNA_PAYL_file= pd.read_csv(RNA_PAYL_file,nrows=1).columns.tolist()
    print("Header Name-------------------",columns_list_RNA_PAYL_file)
    required_columns_RNA_PAYL_file=['Short name', 'Unnamed: 1', '4G Data Volume [GB]', '4G_ECGI',
       'Radio NW Availability']
                                            
                        
    for header_name in required_columns_RNA_PAYL_file:
        if header_name in columns_list_RNA_PAYL_file:
                pass
        else:
                message= "Did not get '" + header_name + "' Column in the uploaded RNA PAYLOAD Report"
                return Response({"status":False,"message":message}) 
    ############## checking columns  for atp file ######################################
#     columns_list_ATP_file= pd.read_excel(ATP_file,nrows=1).columns.tolist()
    columns_list_ATP_file= pd.read_csv(ATP_file,nrows=1).columns.tolist()
    print("Header Name-------------------",columns_list_ATP_file)
    required_columns_ATP_file=['CIRCLE','SITE_ID','UNIQUE ID',
                        'ENODEB_ID','BAND','Circle Project',
                        'Allocation-Date',
                        "OEM_NAME (Nokia/ZTE/Ericsson/Huawei)","TOCO_NAME","EMF_SUBMISSION_DATE",
                        "SCFT_COMPLETION_DATE","MS1","Rfai vs MS1 ","Reason for Delay over period of more than 14 Days ",
                        "RFAI VS MS1- Responsibility",
                        "PERFORMANCE_AT_ACCEPTANCE_DATE2","Performance_AT_Status( Accepted/Rejected/Offered/Pending/Dismantle)",
                        "MS1 Vs Performance AT Acceptance- Ageing","Reason for delay more than 15 days","MS1 VS MS2 Responsibility",
                        "Addition MS2 Remarks","Internal RFAI Vs Ms1-In Days",'Alarm aging',
                                             
                        ]
    for header_name in required_columns_ATP_file:
        if header_name in columns_list_ATP_file:
                pass
        else:
                message= "Did not get '" + header_name + "' Column in the uploaded ATP Report"
                return Response({"status":False,"message":message}) 
    ################################### ********************** #########################################################
    
    ##############################  checking columns for alarm file ##################################
#     columns_list_Alarm_file= pd.read_excel(Alarm_file,nrows=1).columns.tolist()
    columns_list_Alarm_file= pd.read_csv(Alarm_file,nrows=1).columns.tolist()
    print("Header Name-------------------",columns_list_Alarm_file)
    required_columns_Alarm_file=["Distinguished Name","Alarm Type","Severity",
                                "Alarm Time","Name","Supplementary Information"
                                ,"Origin Alarm Time"
                        ]
    for header_name in required_columns_Alarm_file:
        if header_name in columns_list_Alarm_file:
                pass
        else:
                message= "Did not get '" + header_name + "' Column in the uploaded Alarm Report"
                return Response({"status":False,"message":message}) 

    ############################### reading and processing the RNA PAYLOAD file ##################################
    # path_hourly_kpi=r"E:\scheduler_project\bih_2aug_rna_pld_atp_alrm\BIH_HOURLY_KPI.XLSX"
    df_rna_payload=pd.read_csv(RNA_PAYL_file,header=None,names=columns_list_RNA_PAYL_file)
    print(df_rna_payload.columns)
    # df_site=pd.read_excel("E:/scheduler_project/BIHSITE.xlsx")


    df_rna_payload["Short name"].fillna( inplace=True, method="ffill")
    print(df_rna_payload)

    df_cellname=df_rna_payload["Short name"][(df_rna_payload["4G_ECGI"] == '---') | (df_rna_payload["4G_ECGI"] == '')]
    missing_ecgi_cellname=list(set(df_cellname))
    print(missing_ecgi_cellname)

    df_rna_payload=df_rna_payload[(df_rna_payload["4G_ECGI"] != '---') &  (df_rna_payload["4G_ECGI"] != '') ]
    print(df_rna_payload)


    # path_merged_alrm=r"E:\scheduler_project\bih_2aug_rna_pld_atp_alrm\BIHAR_alarm.xlsx"
    # df_merge_alarm=pd.read_excel(Alarm_file)

    df_date_time_split=df_rna_payload["Unnamed: 1"].str.split(',', expand=True)
    print(df_date_time_split) 

    # df1=df1.drop("Unnamed: 1",axis=1)
    df_rna_payload_DateTime_split = pd.concat([df_rna_payload, df_date_time_split], axis=1)
    df_rna_payload_DateTime_split .rename(columns={ 0:"date",1:"time"},inplace=True)
    print(df_rna_payload_DateTime_split )

    df_rna_payload_DateTime_split["Short name"].fillna( inplace=True, method="ffill")
    df_rna_payload_DateTime_split["4G_ECGI"]=df_rna_payload_DateTime_split["4G_ECGI"].astype(str)
    
    df_rna_payload_DateTime_split["ENODEB_ID"]= [ x.split("-")[2] if "-" in x else x for x in df_rna_payload_DateTime_split["4G_ECGI"]]   


    # df_rna_payload_DateTime_split.info()
    # df_rna_payload_DateTime_split=df_rna_payload_DateTime_split[df_rna_payload_DateTime_split.ENODEB_ID.isin(list(df_site["ENODEB_ID"]))]
    print(df_rna_payload_DateTime_split)

    df_piv=round(df_rna_payload_DateTime_split.pivot_table(index=["ENODEB_ID","date"],columns=["time"],values=["Radio NW Availability","4G Data Volume [GB]"]),2)
    # print(df_piv.index)
    print(df_piv)

    # df_piv.to_excel("E:/scheduler_project/ori_rna_payload.xlsx")


    ###################################### reading the atp file #################################################

    # import pandas as pd
    # df1=pd.read_excel('biharrna/rnaout.xlsx',header=0)
    
    path_of_atp_file=r'E:\scheduler_project\bih_2aug_rna_pld_atp_alrm\DPR_W-30_20230730.XLSX'
    
    df_ATP=pd.read_csv(ATP_file,header=None,names=columns_list_ATP_file,usecols=['CIRCLE','SITE_ID','UNIQUE ID',
                                                            'ENODEB_ID','BAND','Circle Project',
                                                            'Allocation-Date',
                                                            "OEM_NAME (Nokia/ZTE/Ericsson/Huawei)","TOCO_NAME","EMF_SUBMISSION_DATE",
                                                            "SCFT_COMPLETION_DATE","MS1","Rfai vs MS1 ","Reason for Delay over period of more than 14 Days ",
                                                            "RFAI VS MS1- Responsibility",
                                                            "PERFORMANCE_AT_ACCEPTANCE_DATE2","Performance_AT_Status( Accepted/Rejected/Offered/Pending/Dismantle)",
                                                            "MS1 Vs Performance AT Acceptance- Ageing","Reason for delay more than 15 days","MS1 VS MS2 Responsibility",
                                                            "Addition MS2 Remarks","Internal RFAI Vs Ms1-In Days","Alarm aging"
                                                                            ])
    # df2
    # d.set_index('ROW Labels',inplace=True)
    df_ATP["ENODEB_ID"]=df_ATP["ENODEB_ID"].astype(str)
    # print(df2)
    df_ATP.set_index('ENODEB_ID',inplace=True)
    print(df_ATP.index)
    df_piv.reset_index(inplace=True)
    df_piv.set_index("ENODEB_ID",inplace=True)
    # print('_____',df2.set_index)
    df_piv_ATP_merged= pd.merge(df_ATP,df_piv, on="ENODEB_ID", how='right')
    df_piv_ATP_merged

    # df_rna_payload_DateTime_split.to_excel("E:/scheduler_project/rna_piv.xlsx")

    ############################################################## reading the Alarm file ########################################### 
    path_merged_alrm=r"E:\scheduler_project\bih_2aug_rna_pld_atp_alrm\BIHAR_alarm.xlsx"
    df_merge_alarm=pd.read_csv(Alarm_file,header=None,names=columns_list_Alarm_file,usecols=["Distinguished Name","Alarm Type","Severity",
                                                                                "Alarm Time","Name","Supplementary Information"
                                                                            ,"Origin Alarm Time"])

    df_merge_alarm["ENODEB_ID"]=df_merge_alarm["Distinguished Name"].str[16:22]
    df_merge_alarm["ENODEB_ID"]=df_merge_alarm["ENODEB_ID"].astype(str)
    df_merge_alarm.set_index("ENODEB_ID",inplace=True)
    df_merge_alarm
  
   #################################################     merging the alarm df and rna payl pivoted df       ########################################################

    df_output=pd.merge(df_piv_ATP_merged,df_merge_alarm,on="ENODEB_ID",how="left")
    print(df_output)

    print(df_output.columns)
   

    save_path= os.path.join(MEDIA_ROOT,'scheduler_project',"alarm_output_new_reindex.csv")
    df_output.to_csv(save_path)
    download_url=os.path.join(MEDIA_URL,'scheduler_project',"alarm_output_new_reindex.csv")
    print("completed..................")

    return Response({"status":True,"message":"Report Generated Succesfully","Download_url":download_url})

            
           

