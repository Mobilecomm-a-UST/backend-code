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
from .serializers import * 
from .models import *
from django.db.models import Min, Max
from django.db.models import Max, F,Subquery, OuterRef
from django.db.models.functions import Coalesce
from django.db import connection
import pytz
import json
from django.db import connection
from mailapp.tasks import send_email

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




target_senders = ["shekhar.bhatnagar@ericsson.com",
                    "prashant.goswami@ericsson.com",
                    "priya.gupta@ericsson.com",
                    "puneet.bhayana@ericsson.com",
                    "jitendra.q.kumar@ericsson.com",
                    "ravinder.x@ericsson.com",
                    "bharti.gnoc.site.at.hua@ericsson.com",
                    "priyanka.c.jain@ericsson.com",
                    "chandra.prabha@ericsson.com",
                    "neyaz.ahmad.ansari@ericsson.com",
                    "deepa.rani@ericsson.com",
                    "gaurav.a.sethi@ericsson.com",
                    "abhinay.barnwal@ericsson.com",
                    "nirbhay.kumar.pal@ericsson.com",
                    "neelima.a.singh@ericsson.com", 
                    # "abhishek.gupta1@mcpsinc.com",
                    "alpana.k@mcpsinc.com",
                    "nishant.verma@mcpsinc.in",
                    # "nocsupport@mcpsinc.com",
                    "vinay.duklan@mcpsinc.in",
                    "anu.a.singh@ericsson.com",
                    "ankit.ankit@ericsson.com",
                    "anoop.singh@ericsson.com",
                    "nakul.chaudhary@ericsson.com",
                    "vivek.kk.kumar@ericsson.com",
                    "bharti.gnoc.site.at.zt@ericsson.com",
                    "md.arsalan.khan@ericsson.com",

                    ]

oem_dict={}

def subject_filteration(all_messages):

      

    list_of_subjects_rx = [
                        re.compile(r'^.*OPS_ERI_(\w+)_Redep\s*Site_NT\(TDD_(\w+)_(\w+)\)(?:[_\s]*(\d+))?[_\s]*Sites \| Redep$'), 
                        re.compile(r'^.*MPCG_ Soft AT MOBILE COMM_(.*).$'),
                        re.compile(r'^.*MUM_HPSC_NT __Soft AT Mobilecom.*$'),
                        re.compile(r'^.*OPS_ERI_UPW_Sector_Addition_Site\(TDD_LG1800_L900_L850\)_\d+_Site \| Sector_Addition$'),                      
                        re.compile(r'^.*OPS_NOK(?:IA)?_(.*)$'),
                        re.compile(r'^.*OPS_SAMSUNG_(.*)$'),
                        re.compile(r'^.*OPS_MOBILECOMM_(\w+)_SOFT_(\d{2})\(.*\)@(\d{2}[A-Za-z]+)$'),
                        re.compile(r'^.*MobileComm_ULS_Relocation_NT_Soft_AT_Offer$'),
                        re.compile(r'^.*OPS_HUA_(\w+)_New_Others_Site Count_(\d+)$'),
                        re.compile(r'^.*HR_Soft AT_(.*)$'),
                        re.compile(r'^.*OPS_ZTE_(.*)$'),
                        re.compile(r'^.*OPS_ERI_(.*)$'),
                    ]
    
    list1=["Ericsson", "Nokia", "Nokia", "Ericsson", "Nokia", "Samsung", "Nokia","Nokia", "Huawei","ZTE","ZTE","Ericsson"]
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

def get_min_max_date_time(nok_obj, sam_obj, hua_obj, eri_obj, zte_obj):
    # Initialize with None values
    huawei_min_date = huawei_max_date = nokia_min_date = nokia_max_date = samsung_min_date = samsung_max_date = eri_min_date = eri_max_date = zte_min_date = zte_max_date = None
    min_date_list=[]
    max_date_list=[]
    # Check if data exists for Huawei
    if hua_obj.exists():
        huawei_min_date = hua_obj.aggregate(min_date=Min('Date_Time'))['min_date']
        huawei_max_date = hua_obj.aggregate(max_date=Max('Date_Time'))['max_date']
        min_date_list.append(huawei_min_date)
        max_date_list.append(huawei_max_date)
    

    # Check if data exists for Nokia
    if nok_obj.exists():
        nokia_min_date = nok_obj.aggregate(min_date=Min('Date_Time'))['min_date']
        nokia_max_date = nok_obj.aggregate(max_date=Max('Date_Time'))['max_date']
        min_date_list.append(nokia_min_date)
        max_date_list.append(nokia_max_date)

    # Check if data exists for Samsung
    if sam_obj.exists():
        samsung_min_date = sam_obj.aggregate(min_date=Min('Date_Time'))['min_date']
        samsung_max_date = sam_obj.aggregate(max_date=Max('Date_Time'))['max_date']

        min_date_list.append(samsung_min_date)
        max_date_list.append(samsung_max_date)
    if eri_obj.exists():
        eri_min_date = eri_obj.aggregate(min_date=Min('Date_Time'))['min_date']
        eri_max_date = eri_obj.aggregate(max_date=Max('Date_Time'))['max_date']

        
        min_date_list.append(eri_min_date)
        max_date_list.append(eri_max_date)
        
    if zte_obj.exists():
        zte_min_date = sam_obj.aggregate(min_date=Min('Date_Time'))['min_date']
        zte_max_date = sam_obj.aggregate(max_date=Max('Date_Time'))['max_date']

        
        min_date_list.append(zte_min_date)
        max_date_list.append(zte_max_date)

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

def process_and_save_NOK_to_database(df, received_date_time, message):
    try:

        for i, d in df.iterrows():
            Integration_date = None
            On_Air_DATE = None
            Offered_Date = None
            if  not pd.isnull(d['INTEGRATION_DATE']):
                Integration_date = d["INTEGRATION_DATE"].date()
            if  not pd.isnull(d['ON AIR DATE']):
                On_Air_DATE = d["ON AIR DATE"].date()   
            if not pd.isnull(d['OFFERED_DATE']):
                Offered_Date = d["OFFERED_DATE"].date()
            if 'CELL_ID' in df.columns:
                cell_id=d["CELL_ID"] 
            else :
                cell_id= None
            if '2G_CELL_ID' in df.columns:
                cell_id_2G =d["2G_CELL_ID"]
            else:
                cell_id_2G=None 

            if 'LNCEL_ID' in df.columns:
                lncel_id=d["LNCEL_ID"]
            else:
                lncel_id=None     
            if 'LNCEL_ID_PCI' in df.columns:
                lncel_id_pci=d["LNCEL_ID_PCI"]     
            else:
                lncel_id_pci=None  

            if 'AT REMARK' in df.columns:
                AT_REMARK=d["AT REMARK"] 

            elif 'AT REMARKS' in df.columns:
                AT_REMARK=d["AT REMARKS"]   
            else:
                AT_REMARK=None      
            
            central_spoc_mails=""
            central_spoc_objs= Centeral_Responsible_Spoc_Mail.objects.filter(OEM__iexact = str(d["OEM"]), Circle__iexact=str(d["CIRCLE"]))
            spoc_mail_list=[]
            if(len(central_spoc_objs) > 0):
                for obj in central_spoc_objs:
                    central_spoc_mails= central_spoc_mails + ", " + obj.Central_Soft_At_Spoc_Mail
          
            else:
                central_spoc_mails="Nishant"
            obj= Soft_AT_NOKIA_Rejected_Table.objects.create(
                        Reference_Id=str(d["REFERENCE_ID"]),
                        AoP=str(d["AOP"]),
                        Circle=str(d["CIRCLE"]),
                        OEM=str(d["OEM"]),
                        TSP=str(d["TSP"]),
                        Offered_Date=Offered_Date,
                        AT_Type=str(d["AT_TYPE"]),
                        Site_ID=str(d["SITE_ID"]),
                        MRBTS_ID=str(d["MRBTS_ID"]),
                        Cell_ID=cell_id,
                        Cell_ID_2G=cell_id_2G,
                        DPR_Cell_Name=str(d["DPR_CELL_NAME"]),
                        LNCEL_ID=lncel_id,
                        LNCEL_ID_PCI=lncel_id_pci,
                        MRBTS_Name=str(d["MRBTS_NAME"]),
                        OSS_FDD_OSS_2G_OSS=str(d["OSS[ FDD OSS 2G OSS]"]),
                        Toco=str(d["TOCO"]),
                        Tech_info=str(d["TECH_INFO"]),
                        Tech=str(d["TECH"]),
                        Band=str(d["BAND"]),
                        Activity_Type=str(d["ACTIVITY TYPE"]),
                        Integration_date=Integration_date,
                        On_Air_DATE=On_Air_DATE,
                        Mplane=str(d["MPLANE"]),
                        Sync_Status=str(d["SYNC STATUS"]),
                        Profile=str(d["PROFILE"]),
                        BSC=str(d["BSC"]),
                        BCF=str(d["BCF"]),
                        Offer_Reoffer=str(d["OFFER/REOFFER"]),
                        LAC=str(d["LAC"]),
                        TAC=str(d["TAC"]),
                        Latitude_N=str(d["LATITUDE (N)"]),
                        Longitude_E=str(d["LONGITUDE (E)"]),
                        FDD_MRBTS_ID=str(d["FDD_MRBTS_ID"]),
                        FDD_Mplane_IP=str(d["FDD_MPLANE_IP"]),
                        RET_Count=str(d["RET COUNT"]),
                        Nominal_Type=str(d["NOMINAL_TYPE"]),
                        Project_Remarks=str(d["PROJECT REMARKS"]),
                        Rejection_Remarks=str(d["REJECTION_REMARKS"]),
                        Media=str(d["MEDIA"]),
                        Ckt_Id=str(d["CKT ID"]),
                        SMP_ID=str(d["SMP_ID"]),
                        Processed_By=str(d["PROCESSED_BY"]),
                        AT_REMARK=AT_REMARK,
                        AT_STATUS =str(d["AT STATUS"]),
                        Date_Time = received_date_time,
                        CENTRAL_SPOC = central_spoc_mails,
                    )
            print("-------------------obj_______________",obj)

        status_objs = Soft_AT_Rejection_Mail_Saved_Status.objects.create(
            Saved_Status = True,
            Date_Time = message.ReceivedTime,
            Sender_Mail = message.SenderEmailAddress,
            OEM = str(d["OEM"]),
        )
        print("Status_obj--:", status_objs)

            

    except Exception as e:
            print("error", e)
            OEM=str(d["OEM"])
            subject = "Soft At rejection App Status"
            from_mail = message.SenderEmailAddress
            body = f""" Mail from {from_mail} on {received_date_time} could't be saved in the DataBase because of "{str(e)}" error in {OEM} oem
                
                Regards.
                Software development Team Mcom
                """
            to_mail = "nishant.verma@mcpsinc.in" + ";" + "abhishek.gupta1@mcpsinc.com"
            send_email(to_mail,"",subject, body)
            status_objs = Soft_AT_Rejection_Mail_Saved_Status.objects.create(
                Error_Status = str(e),
                Date_Time = message.ReceivedTime,
                Sender_Mail = message.SenderEmailAddress,
                OEM = str(d["OEM"]),
            )

            print("Status_objs:",status_objs)

def process_and_save_HUAWEI_to_database(df, received_date_time, message):
    try:
        for i, d in df.iterrows():
            
            On_Air_DATE = None
            Offer_Reoffer_date = None
            if  not pd.isnull(d['ON AIR DATE']):
                On_Air_DATE = d["ON AIR DATE"].date()

            if not pd.isnull(d['OFFER/REOFFER DATE']):
                Offer_Reoffer_date = d["OFFER/REOFFER DATE"].date()

            obj= Soft_AT_HUAWEI_Rejected_Table.objects.create(
                    Circle=str(d["CIRCLE"]),
                    REGION=str(d["REGION"]),
                    OEM=str(d["OEM"]),
                    TSP=str(d["TSP"]),
                    Site_ID_2G=str(d["SITE ID 2G"]),
                    Site_ID_4G=str(d["SITE ID 4G"]),
                    Cell_ID_Parent=str(d["CELL ID (PARENT)"]),
                    Cell_ID_New=str(d["CELL ID (NEW)"]),
                    Technology=str(d["TECHNOLOGY"]),
                    Other_Tech_Info=str(d["OTHER TECH INFO"]),
                    On_Air_Date=On_Air_DATE,
                    Activity=str(d["ACTIVITY"]),
                    Unique_ID=str(d["UNIQUE ID"]),
                    Type_of_Cell=str(d["TYPE OF CELL"]),
                    Frequency_Band=str(d["FREQUENCY BAND"]),
                    MME_0=str(d["MME 0"]),
                    MME_1=str(d["MME 1"]),
                    MME_2=str(d["MME 2"]),
                    MME_3=str(d["MME 3"]),
                    MME_4=str(d["MME 4"]),
                    SGW_IP=str(d["SGW IP"]),
                    UPEU_Count=str(d["UPEU COUNT"]),
                    VSWR_Alarm_Threshold=str(d["VSWR ALARM THRESHOLD"]),
                    Sync_Status_GPS_status_IP=str(d["SYNC STATUS (GPS STATUS/IP)"]),
                    EMF_Status_Yes_No=str(d["EMF STATUS (YES/NO)"]),
                    BSC_RNC_detail=str(d["BSC/RNC DETAIL"]),
                    OSS=str(d["OSS"]),
                    OSS_IP=str(d["OSS IP"]),
                    Site_OSS_Name=str(d["SITE OSS NAME"]),
                    PHYSICAL_ID=str(d["PHYSICAL ID"]),
                    TRX_configuration_Detail_900=str(d["TRX CONFIGURATION DETAIL (900)"]),
                    TRX_configuration_Detail_900_Required=str(d["TRX CONFIGURATION DETAIL (900) REQUIRED"]),
                    TRX_configuration_Detail_1800=str(d["TRX CONFIGURATION DETAIL (1800)"]),
                    TRX_configuration_Detail_1800_Required=str(d["TRX CONFIGURATION DETAIL (1800)REQUIRED"]),
                    Sector_Count=str(d["SECTOR COUNT"]),
                    TX_RX_configuration_Detail=str(d["TX/RX CONFIGURATION DETAIL"]),
                    Type_Physical_AT_Soft_AT=str(d["TYPE(PHYSICAL AT/SOFT AT)"]),
                    Offer_Reoffer=str(d["OFFER/REOFFER"]),
                    Offer_Reoffer_date=Offer_Reoffer_date,
                    LAC=str(d["LAC"]),
                    TAC=str(d["TAC"]),
                    LAST_REJECTION_REMARKS=str(d["LAST REJECTION REMARKS"]),
                    RET_Status=str(d["RET STATUS"]),
                    AT_STATUS=str(d["AT STATUS"]),
                    AT_Remarks=str(d["AT REMARKS"]),
                    Date_Time = received_date_time,
                )
            print("-------------------obj_______________",obj)

        status_objs = Soft_AT_Rejection_Mail_Saved_Status.objects.create(
            Saved_Status = True,
            Date_Time = message.ReceivedTime,
            Sender_Mail = message.SenderEmailAddress,
            OEM = str(d["OEM"]),
        )
        print("Status_obj--:", status_objs)
    except Exception as e:
        print("error", e)
        OEM=str(d["OEM"])
        subject = "Soft At rejection App Status"
        from_mail = message.SenderEmailAddress
        body = f""" Mail from {from_mail} on {received_date_time} could't be saved in the DataBase because of "{str(e)}" error in {OEM} oem
            
            Regards.
            Software development Team Mcom
            """
        to_mail = "nishant.verma@mcpsinc.in" + ";" + "abhishek.gupta1@mcpsinc.com"
        send_email(to_mail,"",subject, body)
        status_objs = Soft_AT_Rejection_Mail_Saved_Status.objects.create(
            Error_Status = str(e),
            Date_Time = message.ReceivedTime,
            Sender_Mail = message.SenderEmailAddress,
            OEM = str(d["OEM"]),
        )
        print("Status_obj--:", status_objs)


def process_and_save_SAMSUNG_to_database(df, received_date_time, message):
    try:
        for i, d in df.iterrows():
            # if d["AT STATUS "]== "REJECT":
            #     continue
            On_Air_DATE = None
            Integration_Date=None
            Offer_Reoffer_date = None
            if  not pd.isnull(d['ON-AIR DATE']):
                On_Air_DATE = d["ON-AIR DATE"].date()

            if not pd.isnull(d['INTEGRATION DATE']):
                Integration_Date = d["INTEGRATION DATE"].date()

            if not pd.isnull(d['OFFER/REOFFER DATE']):
                Offer_Reoffer_date = d["OFFER/REOFFER DATE"].date()

            regx_gpl = re.compile(r'^(.*) GPL TYPE$') 
            for i,column in enumerate(df.columns):
                if(regx_gpl.match(column)):

                    gpl_type = d[column]
                    print("inside test.....")
            obj= Soft_AT_SAMSUNG_Rejected_Table.objects.create(
                        Circle=str(d["CIRCLE"]),
                        OEM=str(d["OEM"]),
                        TSP=str(d["TSP"]),
                        SR_UNIQUE_Project_ID=str(d["SR / UNIQUE PROJECT ID"]),
                        AT_Type=str(d["AT TYPE"]),
                        Physical_Cascade_ID=str(d["PHYSICAL/CASCADE ID"]),
                        Site_ID_2G=str(d["SITE ID (2G)"]),
                        Site_ID_4G_MRBTS_ID=str(d["SITE ID (4G/)/MRBTS ID"]),
                        Technology=str(d["TECHNOLOGY"]),
                        Other_Tech_Info_Band=str(d["OTHER TECH INFO(BAND)"]),
                        On_Air_Date=On_Air_DATE,
                        Activity_Type_Swap_New_Site=str(d["ACTIVITY TYPE(SWAP/NEW SITE)"]),
                        Parent_Cell_Id_Name_In_Case_Of_Twin_Beam=str(d["PARENT CELL ID/NAME (IN CASE OF TWIN BEAM)"]),
                        Newly_Added_In_Case_Of_SA_Twin_Beam_MIMO_Cell_Id_Name=str(d["NEWLY ADDED (IN CASE OF SA,TWIN BEAM & MIMO) CELL ID/NAME"]),
                        Node_4G_IP_Mplane_IP=str(d["4G NODE IP/MPLANE IP"]),
                        OSS_Name=str(d["OSS NAME"]),
                        OSS_IP=str(d["OSS IP"]),
                        ENodeB_ID=str(d["ENODEB ID"]),
                        BSC_In_Case_Of_NT_2G=str(d["BSC (IN CASE OF NT/2G)"]),
                        BSC_OSS_In_Case_Of_NT=str(d["BSC OSS(IN CASE OF NT)"]),
                        R_Site_Name_Ericsson_2G_BCF_ID_Nokia_2G=str(d["R_SITE NAME (ERICSSON 2G)/BCF ID (NOKIA 2G)"]),
                        OLD_Cell_Count_No_Of_Cells=str(d["OLD CELL COUNT/NO. OF CELLS"]),
                        New_Cell_Count_No_Of_Cells=str(d["NEW CELL COUNT/NO. OF CELLS"]),
                        TRX_Configuration_in_case_of_2G=str(d["TRX CONFIGURATION IN CASE OF 2G"]),
                        Site_4G_Configuration=str(d["4G SITE CONFIGURATION"]),
                        No_Of_RRU=str(d["NO OF RRU"]),
                        Other_Hardware_Related_Additional_Information=str(d["OTHER HARDWARE RELATED ADDITIONAL INFORMATION"]),
                        TAC=str(d["TAC"]),
                        MME_IP=str(d["MME IP"]),
                        SGW_IP=str(d["SGW IP"]),
                        VSWR_current_value=str(d["VSWR CURRENT VALUE"]),
                        BBU_Type_Model=str(d["BBU TYPE &MODEL"]),
                        OD_ID_Configuration=str(d["OD & ID CONFIGURATION"]),
                        RET_Configuration=str(d["RET CONFIGURATION"]),
                        hrs24_Alarm_History=str(d["24 HRS ALARM HISTORY"]),
                        NE_Version=str(d["NE VERSION"]),
                        Integration_Date=Integration_Date,
                        SW_Version=str(d["SW VERSION"]),
                        Sync_status_GPS_clock_NTP=str(d["SYNC STATUS GPS/CLOCK/NTP"]),
                        GPL_compliance=str(d["GPL COMPLIANCE"]),
                        LMS_compliance=str(d["LMS COMPLIANCE"]),
                        Power_compliance=str(d["POWER COMPLIANCE"]),
                        IFLB_Compliance=str(d["IFLB COMPLIANCE"]),
                        CA_compliance=str(d["CA COMPLIANCE"]),
                        QoS_Compliance=str(d["QOS COMPLIANCE"]),
                        Ducting_compliance=str(d["DUCTING COMPLIANCE"]),
                        Energy_saving_fetaures_compliance=str(d["ENERGY SAVING FETAURES COMPLIANCE"]),
                        Features_implemented_compliance=str(d["FEATURES IMPLEMENTED COMPLIANCE"]),
                        Nomenclature_Compliance=str(d["NOMENCLATURE COMPLIANCE"]),
                        PCI_RSI_PRACH_definition_compliance=str(d["PCI, RSI, PRACH DEFINITION COMPLIANCE"]),
                        Critical_Major_Alarms=str(d["CRITICAL & MAJOR ALARMS (OBSERVED AFTER ACTIVITY AND NOT THERE PRE ACTIVITY)"]),
                        # Observed_after_activity_and_not_there_pre_activity=str(d["(Observed after activity and not there pre activity)"])
                        Splitting_Details=str(d["SPLITTING DETAILS"]),
                        RET_Details_Cell_Name=str(d["RET DETAILS/(CELL NAME)"]),
                        Toco_Type_Shared_Anchor=str(d["TOCO TYPE(SHARED/ANCHOR)"]),
                        Project_Remarks=str(d["PROJECT_REMARKS"]),
                        Rejection_Remarks_in_Case_of_Re_offer=str(d["REJECTION REMARKS(IN CASE OF RE-OFFER)"]),
                        All_approved_features_compliance_implemented=str(d["ALL APPROVED FEATURES & COMPLIANCE IMPLEMENTED"]),
                        Offer_Reoffer=str(d["OFFER/REOFFER"]),
                        Offer_Reoffer_Date=Offer_Reoffer_date,
                        GPL_Type=gpl_type,
                        Scope=str(d["SCOPE"]),
                        External_Alarm_Status_YES_NO=str(d["EXTERNAL ALARM STATUS(YES/NO)"]),
                        LTE_Technology_for_GPL_Validation=str(d["LTE TECHNOLOGY FOR GPL VALIDATION"]),
                        Carrier_Type=str(d["CARRIER TYPE"]),
                        Radio_Unit_Info_Connected_digital_unit_port_id=str(d["RADIO-UNIT-INFO/CONNECTED-DIGITAL-UNIT-PORT-ID"]),
                        Type_of_Media=str(d["TYPE OF MEDIA"]),
                        MW_Link_Id_Ckt_Id=str(d["MW LINK ID/CKT ID"]),
                        AT_STATUS=str(d["AT STATUS"]),
                        AT_Remarks=str(d["AT REMARKS"]),
                        Date_Time = received_date_time,
                    )
            print("-------------------obj_______________",obj)
        status_objs = Soft_AT_Rejection_Mail_Saved_Status.objects.create(
            Saved_Status = True,
            Date_Time = message.ReceivedTime,
            Sender_Mail = message.SenderEmailAddress,
            OEM = str(d["OEM"]),
        )
        print("Status_obj--:", status_objs)                 
    except Exception as e:
        print("error", e)
        OEM=str(d["OEM"])
        subject = "Soft At rejection App Status"
        from_mail = message.SenderEmailAddress
        body = f""" Mail from {from_mail} on {received_date_time} could't be saved in the DataBase because of "{str(e)}" error in {OEM} oem
            
            Regards.
            Software development Team Mcom
            """
        to_mail = "nishant.verma@mcpsinc.in" + ";" + "abhishek.gupta1@mcpsinc.com"
        send_email(to_mail,"",subject, body)
        status_objs = Soft_AT_Rejection_Mail_Saved_Status.objects.create(
            Error_Status = str(e),
            Date_Time = message.ReceivedTime,
            Sender_Mail = message.SenderEmailAddress,
            OEM = str(d["OEM"]),
        )
        print("Status_obj--:", status_objs)
def process_and_save_ZTE_to_database(df, received_date_time, message):
    try:
       
        for i, d in df.iterrows():

            Integration_date = None
            Offer_Reoffer_dates = None
            if  not pd.isnull(d['INTEGRATION DATE']):
                Integration_date = d["INTEGRATION DATE"].date()
            if  not pd.isnull(d['OFFER/REOFFER DATE']):
                Offer_Reoffer_dates= d["OFFER/REOFFER DATE"].date()   

            for column in df.columns:
                lower_col = column.lower()
                if lower_col.find("at remark"):
                    remark = str(df[column])

            obj= Soft_AT_ZTE_Rejected_Table.objects.create(
                    Circle=str(d["CIRCLE"]),                  
                    OEM=str(d["OEM"]),
                    TSP=str(d["TSP"]),
                    Site_ID=str(d["SITE ID"]),
                    No_of_Cell=str(d["NO OF CELL"]),
                    Cell_ID_Parent=str(d["CELL ID (PARENT)"]),
                    Cell_ID_New=str(d["CELL ID (NEW)"]),
                    Technology=str(d["TECHNOLOGY"]),
                    Other_Tech_Info_Band=str(d["OTHER TECH INFO(BAND)"]),
                    Integration_Date=Integration_date,
                    Activity_Type=str(d["ACTIVITY TYPE"]),
                    OSS=str(d["OSS"]),
                    BSC=str(d["BSC"]),
                    Offer_Reoffer=str(d["OFFER/REOFFER"]),
                    Offer_Reoffer_date=Offer_Reoffer_dates,
                    AT_Type_Physical_AT_Soft_AT=str(d["AT TYPE(PHYSICAL AT/SOFT AT)"]),
                    Cascaded_Remarks=str(d["CASCADED REMARKS"]),
                    LAC=str(d["LAC"]),
                    TAC=str(d["TAC"]),
                    SiteID_MEID=str(d["4GSITEID/MEID"]),
                    RET_Configuration_Remarks_Cell_Name=str(d["RET CONFIGURATION REMARKS/(CELL NAME)"]),
                    Toco_Type_Shared_Anchor=str(d["TOCO TYPE(SHARED/ANCHOR)"]),
                    LAST_REJECTION_REMARKS=str(d["LAST REJECTION REMARKS"]),
                    DPR_Cell_Name=str(d["DPR_CELL_NAME"]),
                    Media=str(d["MEDIA"]),
                    Duplex=str(d["DUPLEX"]),
                    Detected_Speed_Duplex=str(d["DETECTED SPEED & DUPLEX"]),
                    M_plane=str(d["M-PLANE"]),
                    Sync_Status=str(d["SYNC STATUS"]),
                    User_Plane_IP=str(d["USER PLANE IP"]),
                    TAC_ID=str(d["TAC ID"]),
                    CIRCUITID=str(d["CIRCUIT ID"]),
                    AT_Remarks=remark,
                    AT_STATUS =str(d["AT STATUS"]),
                    Date_Time = received_date_time,
                )
            print("-------------------obj_______________",obj)
        status_objs = Soft_AT_Rejection_Mail_Saved_Status.objects.create(
            Saved_Status = True,
            Date_Time = message.ReceivedTime,
            Sender_Mail = message.SenderEmailAddress,
            OEM = str(d["OEM"]),
        )
        print("Status_obj--:", status_objs)
    except Exception as e:
        print("error", e)
        OEM=str(d["OEM"])
        subject = "Soft At rejection App Status"
        from_mail = message.SenderEmailAddress
        body = f""" Mail from {from_mail} on {received_date_time} could't be saved in the DataBase because of "{str(e)}" error in {OEM} oem
            
            Regards.
            Software development Team Mcom
            """
        to_mail = "nishant.verma@mcpsinc.in" + ";" + "abhishek.gupta1@mcpsinc.com"
        send_email(to_mail,"",subject, body)
        status_objs = Soft_AT_Rejection_Mail_Saved_Status.objects.create(
            Error_Status = str(e),
            Date_Time = message.ReceivedTime,
            Sender_Mail = message.SenderEmailAddress,
            OEM = str(d["OEM"]),
        )
        print("Status_obj--:", status_objs)

                        
def process_and_save_ERI_to_database(message,sender_email,received_date_time, output_folder):
    try:
        output_dir = Path.cwd() / "output"
        output_dir.mkdir(parents=True, exist_ok=True)

        if any(target_sender.lower() == sender_email.lower() for target_sender in target_senders):
            subject = message.Subject

        body = message.Body

        # save_body_and_attachments(message, output_dir, subject)

        # Extract tabular data from the body
        start_marker = "AOP"
        end_marker = "AT Remarks"
        start_index = body.find(start_marker)
        end_index = body.find(end_marker, start_index + len(start_marker))
        if start_index != -1 and end_index != -1:
            # Extract headers
            headers_text = body[start_index + len(start_marker):end_index].strip()
            headers = re.split(r'\r\n\r\n|\r\n', headers_text)
            headers = ['AOP'] + headers + ["AT Remarks","Status","Remarks"]
            # print("header",headers)
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

                    header_lis=['Status','Remarks']
                    data_lines = [line for line in data_lines if not any(substring in line for substring in header_lis)]            
                    # print("data_text___________",data_lines)
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
                     # print("_____________data_____________",dat
             # Transpose the data to distribute across all columns
            transposed_data = list(map(list, zip(*data)))
            body_mail = [item if item is not None else None for sublist in transposed_data for item in sublist]
             # print("__________body__________mail___________",body_mai
             # Reshape the data into a 2D array
            reshaped_data = np.array(body_mail).reshape(-1, len(headers))
             # reshaped_data = reshaped_data.replace("", "NA")
            print("reshaped________________data",reshaped_data)
             # Create DataFrame
            table_df = pd.DataFrame(reshaped_data, columns=headers)
            # Create a folder for each message
            target_folder = output_dir / sanitize_filename(subject)
            target_folder.mkdir(parents=True, exist_ok=True)
            # Save the DataFrame to an Excel file
            excel_file_path = target_folder / f"{subject}_data.xlsx"
            print(excel_file_path, "__________hi_______________")
            table_df.to_excel(excel_file_path, index=False, header=True, sheet_name='Sheet1')
            df = pd.read_excel(excel_file_path)
            df.dropna(subset=['AOP'], inplace=True)
            df.to_excel(excel_file_path)
                # print("df",df)
            df.columns = df.columns.str.upper().str.strip()
            df = df.applymap(lambda x: x.upper().strip() if isinstance(x, str) else x)
            print("df_____",df)
            if "OEM" in df.columns:
                 print("dfdfdf",df["OEM"])
                 oem=str(df["OEM"][0])
            elif "HARDWARE MADE (OEM)" in df.columns:
                 oem=str(df["HARDWARE MADE (OEM)"][0])

            for i, d in df.iterrows():
                # if d["AT STATUS "]== "REJECT":
                #     continue
                AT_Offering_Date = None
                On_Air_Date = None
                # Offered_Date = None
                if  not pd.isnull(d['ON-AIR DATE']):
                    On_Air_Date = pd.to_datetime(d['ON-AIR DATE'], format='%d-%b-%y').date()
                    print("on_air_date",On_Air_Date)
                else:
                    On_Air_Date=None


                if  not pd.isnull(d['AT OFFERING DATE']):
                    AT_Offering_Date = pd.to_datetime(d["AT OFFERING DATE"],format='%d-%b-%y').date()
                    print("at_offering",type(AT_Offering_Date))

                if 'OEM' in df.columns:
                    OEM=d["OEM"] 

                elif 'HARDWARE MADE (OEM)' in df.columns:
                    OEM=d["HARDWARE MADE (OEM)"]   
                else:
                    OEM=None 
                status_column = None
                if "STATUS" in df.columns:
                    status_column = "STATUS"
                elif "AT STATUS" in df.columns:
                    status_column = "AT STATUS"
                print(status_column)
                remark_column = None
                if "REMARKS" in df.columns:
                    remark_column = "REMARKS"
                elif "AT REMARKS" in df.columns:
                    remark_column = "AT REMARKS"  
                print(remark_column)  
                obj= Soft_AT_ERI_Rejected_Table.objects.create(
                        AOP=str(d["AOP"]),
                        Circle=str(d["CIRCLE"]),
                        OEM=oem,

                        Offered_AT_Type=str(d["OFFERED AT TYPE"]),
                        Physical_Site_Id=str(d["PHYSICAL SITE ID"]),
                        Site_ID=str(d["2G SITE ID"]),
                        Technology=str(d["TECHNOLOGY"]),
                        Layers_Other_Tech_Info=str(d["LAYERS(OTHER TECH INFO)"]),
                        Activity_Name=str(d["ACTIVITY NAME"]),
                        RET_Configuration_Cell_Name=str(d["RET CONFIGURATION(CELL NAME)"]),
                        RET_Configured_on_Layer=str(d["RET CONFIGURED ON(LAYER)"]),
                        Parent_Cell_Name_In_Case_Of_Twin_Beam=str(d["PARENT CELL NAME (IN CASE OF TWIN BEAM)"]),
                        Cell_Name_New=str(d["CELL NAME (NEW)"]),
                        MO_Name=str(d["MO NAME"]),
                        Node_IP=str(d["4G NODE IP"]),
                        OSS_Name_IP=str(d["OSS NAME/IP"]),
                        BSC_In_Case_Of_NT_2G=str(d["BSC (IN CASE OF NT/2G)"]),
                        OSS_ENM_For_BSC_In_Case_Of_NT_2G=str(d["OSS/ENM (FOR BSC IN CASE OF NT/2G)"]),
                        TAC_Name=str(d["TAC NAME"]).upper(),
                        Cells_Configuration=str(d["CELLS CONFIGURATION"]),
                        Scenario_In_Case_Of_Swap=str(d["SCENARIO (IN CASE OF SWAP)"]),
                        Hardware_RRU=str(d["HARDWARE/RRU"]),
                        Hardware_BBU=str(d["HARDWARE/BBU"]),
                        Antenna=str(d["ANTENNA"]),
                        CPRI=str(d["CPRI"]),
                        On_Air_Date=On_Air_Date,
                        SW_Version=str(d["SW VERSION"]),
                        Sync_status_GPS_clock_NTP=str(d["SYNC STATUS GPS/CLOCK/NTP"]),
                        AT_Offering_Date=AT_Offering_Date,
                        MIMO_Power_configuration=str(d["MIMO POWER CONFIGURATION"]),
                        Media_Type=str(d["MEDIA TYPE"]),
                        Link_id=str(d["LINK ID"]),
                        Project_remarks=str(d["PROJECT REMARKS"]),
                        AT_STATUS=str(d[status_column]) if status_column else None,
                        AT_Remarks=str(d[remark_column]) if remark_column else None,
                        Date_Time = received_date_time,
                        )
                print("-------------------obj_______________",obj)
            status_objs = Soft_AT_Rejection_Mail_Saved_Status.objects.create(
                Saved_Status = True,
                Date_Time = message.ReceivedTime,
                Sender_Mail = message.SenderEmailAddress,
                OEM = str(d["OEM"]),
            )
            print("Status_obj--:", status_objs)
    except Exception as e:
        print("error", e)
        OEM=oem
        subject = "Soft At rejection App Status"
        from_mail = sender_email
        body = f""" Mail from {from_mail} on {received_date_time} could't be saved in the DataBase because of "{str(e)}" error in {OEM} oem
            
            Regards.
            Software development Team Mcom
            """
        to_mail = "nishant.verma@mcpsinc.in" + ";" + "abhishek.gupta1@mcpsinc.com"
        send_email(to_mail,"",subject, body)
        status_objs = Soft_AT_Rejection_Mail_Saved_Status.objects.create(
            Error_Status = str(e),
            Date_Time = message.ReceivedTime,
            Sender_Mail = message.SenderEmailAddress,
            OEM = oem,
        )
        print("Status_obj--:", status_objs)      

                        
def get_latest_record_per_site(oem_table):
    # Assuming Soft_AT_NOKIA_Rejected_Table and Soft_AT_HUAWEI_Rejected_Table are Django models

    site_id_field = "Site_ID" if oem_table == Soft_AT_NOKIA_Rejected_Table else "Site_ID_2G"

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

def Soft_At_Rejection_Database_save(multiple,all_items):
        
        # Initialize COM
        pythoncom.CoInitialize()
        # Create output folder
        output_dir = Path.cwd() / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        
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
                all_messages = inbox.Items.Restrict(filter_condition)[1]
                all_messages = [all_messages]

                # sorted_messages = inbox.Items.Sort("[ReceivedTime]", True)

                # # Get the latest (first) message
                # latest_message = sorted_messages.GetFirst()
                # all_messages=[latest_message]
                # print(all_messages.Count)
                # print("all_messages..........",all_messages.Count)
        else:
             all_messages =all_items


        tup_meessage_oem = subject_filteration(all_messages)
        filtered_messages = tup_meessage_oem[0]
        oem_list= tup_meessage_oem[1]
    

        print("line execution")
        for i,message in enumerate(filtered_messages):
            OEM=oem_list[i]
            print("message :",message.Subject," OEM from filter subject method:",OEM)
            # try:
            
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
            # except Exception as e:

            #     continue
            try:
                # # Try to get the message headers
                # transport_headers = message.PropertyAccessor.GetProperty("http://schemas.microsoft.com/mapi/proptag/0x007D001E")

                # # Extract the sender's email address from headers
                # match = re.search(r"From:.*?<([^>]+)>", transport_headers)
                # sender_email = match.group(1) if match else "Unknown Sender"
                sender_email=message.SenderEmailAddress
            except Exception as e:
                continue  # Skip to the next email if extraction fails

            # Check if the target sender's email address is present in the list of sender's email addresses
            if any(target_sender.lower() == sender_email.lower() for target_sender in target_senders):
                subject = sanitize_filename(message.Subject)
                # print("_________subject____________", subject)

                # Handle attachments outside the 'else' statement
                try:
                    attachments = message.Attachments
                    attachment_count = attachments.Count
                except Exception as e:
                    # print(f"Error accessing attachments for email with subject '{subject}': {e}")
                    attachment_count = 0

                if attachment_count > 0:
                    # Create a separate folder for each message
                    target_folder = output_dir / subject
                    target_folder.mkdir(parents=True, exist_ok=True)
                   
                    for i in range(1, attachment_count + 1):
                        # try:
                            attachment = attachments.Item(i)

                            # Create the target folder if it does not exist
                            target_folder.mkdir(parents=True, exist_ok=True)
                            attachment_filename = sanitize_filename(attachment.FileName)
                            attachment.SaveAsFile(str(target_folder / attachment_filename))
                            # attachment.SaveAsFile(target_folder / sanitize_filename(str(attachment)))
                            print("attachment_file_NIS_________________________",attachment_filename)
                            
                            file_name,extension = os.path.splitext(attachment_filename)
                            print("extension.................",extension)
                            if extension.strip().lower() == ".xlsx":
                                print("inside excel attachment________", attachment_filename)
                                df = pd.read_excel(target_folder / (str(attachment_filename)))

                                # print("df",df)
                                df.columns = df.columns.str.upper().str.strip()
                                df = df.applymap(lambda x: x.strip().upper() if isinstance(x, str) else x)
                                # print("__________________Dfhu_________",df)
                                
                                # received_date_time = datetime.datetime(2023,2,27,12,12,12)
                                if "OEM" in df.columns:
                                    print("dfdfdf",df["OEM"])
                                    oem=str(df["OEM"][0]).upper()
                                elif "OEM" in df.columns or "Hardware Made (OEM)".upper() in df.columns:
                                    oem=str(df["OEM"][0]).upper()
                                else:
                                    pass
                                
                                print("Oem from attached excel....",type(oem))
                                
                                if(oem == "NOKIA"):
                                    print("nok_______enter")
                                    process_and_save_NOK_to_database(df, received_date_time, message)

                                if(oem == "HUAWEI"):
                                    print("inside huawei")  
                                    process_and_save_HUAWEI_to_database(df, received_date_time, message)

                                if(oem == "SAMSUNG"):  
                                    print("inside samsung") 
                                    process_and_save_SAMSUNG_to_database(df, received_date_time, message)

                                if(oem == "ZTE"):  
                                    print("inside ZTE") 
                                    process_and_save_ZTE_to_database(df, received_date_time, message)
                            
                            if OEM == "Ericsson":
                                print("Erission and Mobilecomm process")
                                
                                process_and_save_ERI_to_database(message,sender_email, received_date_time, target_folder)
                                
                            # get_min_max_date_time()
                        
                            # Accept_Reject_save_to_database(df)
                        # except Exception as e:
                        #         print(f"Error saving/reading attachment {i} for email with subject '{subject}': {e}")
                
                







