from django.shortcuts import render
from django.db.models import *
from rest_framework.decorators import api_view
from mcom_website.settings import MEDIA_ROOT
from rest_framework.response import Response
import pandas as pd
from django.db import transaction
import os
from RCA_TOOL.models import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import operator
from RCA_TOOL.serializers import *
from rest_framework import status
from datetime import datetime, timedelta, time
import numpy as np
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
import requests


def inbetween(x, a, b):
    print("x=", x, "a=", a, "b=", b)
    return not (a <= x <= b)


OPERATORS_dict = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "%": operator.mod,
    "==": operator.eq,
    "!=": operator.ne,
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
    "=<=<": inbetween,
}


@api_view(["GET", "POST"])
def rca_table_list(request):
    if request.method == "GET":
        rca_tables = RCA_TABLE.objects.all()
        serializer = RCATableSerializer(rca_tables, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = RCATableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def rca_table_detail(request, pk):
    try:
        rca_table = RCA_TABLE.objects.get(pk=pk)
    except RCA_TABLE.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = RCATableSerializer(rca_table)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = RCATableSerializer(rca_table, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        rca_table.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def kpi_table_list(request):
    if request.method == "GET":
        kpi_tables = KPI_TABLE.objects.all()
        serializer = KPITableSerializer(kpi_tables, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = KPITableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def kpi_table_detail(request, pk):
    try:
        kpi_table = KPI_TABLE.objects.get(pk=pk)
    except KPI_TABLE.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = KPITableSerializer(kpi_table)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = KPITableSerializer(kpi_table, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        kpi_table.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def unique_kpi(request):
    fields = Daily_4G_KPI._meta.get_fields()
    fields_tentative = Tantitive_Counters_24_Hours._meta.get_fields()

    # Extract field names
    KPI_names = [field.name for field in fields][8:]
    tentative_counters = [field.name for field in fields_tentative]
    print(tentative_counters)

    operators_var = ["==", "+", ">", "<", ">=", "<=", "!="]

    data_source = ["MYCOM", "Alarm dump"]

    return Response(
        {
            "Status": True,
            "KPI_name": KPI_names,
            "operators": operators_var,
            "data_source": data_source,
            "tentative_counters": tentative_counters,
        }
    )


import pytz


@api_view(["POST"])
def AlarmFileUpload(request):
    file = request.FILES.get("alarm_notifications")
    upload_date = request.POST.get("Upload_date")
    if not file:
        return Response({"status": False, "message": "No file provided."}, status=400)
    if not upload_date:
        return Response({"status": False, "message": "No file provided."}, status=400)

    try:
        df = pd.read_csv(file)
    except Exception as e:
        return Response({"status": False, "error": str(e)}, status=500)

    required_columns = [
        "Notification ID",
        "Alarm Number",
        "Alarm Type",
        "Severity",
        "Alarm Time",
        "Probable Cause",
        "Probable Cause Code",
        "Alarm Text",
        "Distinguished Name",
        "Object Class",
        "Acknowledgement State",
        "Acknowledgement Time/UnAcknowledgement Time",
        "Acknowledgement User",
        "Cancel State",
        "Cancel Time",
        "Cancel User",
        "Name",
        "Maintenance Region Name",
        "Site Name",
        "Site Priority",
        "Site Address",
        "Extra Information",
        "Diagnostic Info",
        "User Additional Information",
        "Supplementary Information",
        "Additional Information 1",
        "Additional Information 2",
        "Additional Information 3",
        "Correlation Indicator",
        "Notes Indicator",
        "Trouble Ticket Indicator",
        "Alarm Sound",
        "Instance Counter",
        "Consecutive Number",
        "Alarm Insertion Time",
        "Alarm Update Time",
        "Controlling Object Name",
        "Origin Alarm Time",
        "Origin Alarm Update Time",
        "Origin Acknowledgement/UnAcknowledgement Time",
        "Origin Cancel Time",
        "Related DN's",
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return Response(
            {
                "status": False,
                "error": f"Missing columns: {', '.join(missing_columns)}",
            },
            status=400,
        )

    try:
        objects_to_create = []
        for _, row in df.iterrows():
            # print("alarm t.........................",pd.to_datetime(row["Alarm Time"], errors="coerce").tz_localize('utc'))
            # print("alarm t.........................",pd.to_datetime(row["Alarm Time"], errors="coerce"))
            if pd.notnull(row["Notification ID"]):
                obj = AlarmNotification(
                    NotificationId=row["Notification ID"],
                    AlarmNumber=row["Alarm Number"],
                    AlarmType=row["Alarm Type"],
                    Severity=row["Severity"],
                    Upload_date=upload_date,
                    AlarmTime=pd.to_datetime(
                        row["Alarm Time"], errors="coerce"
                    ).tz_localize("utc"),
                    AlarmText=row["Alarm Text"],
                    DistinguishedName=row["Distinguished Name"],
                    ObjectClass=row["Object Class"],
                    AcknowledgementState=row["Acknowledgement State"],
                    AcknowledgementTimeOrUnacknowledgementTime=row[
                        "Acknowledgement Time/UnAcknowledgement Time"
                    ],
                    AcknowledgementUser=row["Acknowledgement User"],
                    CancelState=row["Cancel State"],
                    CancelTime=row["Cancel Time"],
                    CancelUser=row["Cancel User"],
                    Name=row["Name"],
                    MaintenanceRegionName=row["Maintenance Region Name"],
                    SiteName=row["Site Name"],
                    SitePriority=row["Site Priority"],
                    SiteAddress=row["Site Address"],
                    ExtraInformation=row["Extra Information"],
                    DiagnosticInfo=row["Diagnostic Info"],
                    UserAdditionalInformation=row["User Additional Information"],
                    SupplementaryInformation=row["Supplementary Information"],
                    AdditionalInformation1=row["Additional Information 1"],
                    AdditionalInformation2=row["Additional Information 2"],
                    AdditionalInformation3=row["Additional Information 3"],
                    CorrelationIndicator=row["Correlation Indicator"],
                    NotesIndicator=row["Notes Indicator"],
                    TroubleTicketIndicator=row["Trouble Ticket Indicator"],
                    AlarmSound=row["Alarm Sound"],
                    InstanceCounter=row["Instance Counter"],
                    ConsecutiveNumber=row["Consecutive Number"],
                    AlarmInsertionTime=row["Alarm Insertion Time"],
                    AlarmUpdateTime=row["Alarm Update Time"],
                    ControllingObjectName=row["Controlling Object Name"],
                    OriginAlarmTime=row["Origin Alarm Time"],
                    OriginAlarmUpdateTime=row["Origin Alarm Update Time"],
                    OriginAcknowledgementOrUnacknowledgementTime=row[
                        "Origin Acknowledgement/UnAcknowledgement Time"
                    ],
                    OriginCancelTime=row["Origin Cancel Time"],
                    RelatedDns=row["Related DN's"],
                )
                objects_to_create.append(obj)

        with transaction.atomic():
            AlarmNotification.objects.bulk_create(objects_to_create)

        return Response({"status": True, "message": "Data inserted successfully."})

    except Exception as e:
        return Response({"status": False, "error": str(e)}, status=500)


@api_view(["POST"])
def Daily_RAW_KPI_4G(request):
    kpi_4g = request.FILES.get("4G_raw")
    if not kpi_4g:
        return Response({"status": False, "message": "No file provided."}, status=400)

    try:
        df = pd.read_csv(kpi_4g)
    except Exception as e:
        return Response({"status": False, "error": str(e)}, status=500)

    try:
        df["Short name"] = df["Short name"].fillna(method="ffill")
        df.rename(columns={"Unnamed: 1": "Date"}, inplace=True)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["MV eCell Data BH"] = pd.to_datetime(
            df["MV eCell Data BH"], errors="coerce", format="%H:%M"
        ).dt.time

        required_columns = [
            "Short name",
            "Date",
            "ECGI",
            "OEM_GGSN",
            "MV_Radio NW Availability",
            "MV_4G Data Volume_GB",
            "MV_VoLTE Traffic",
            "MV_DL User Throughput_Kbps [CDBH]",
            "MV_E-UTRAN Average CQI [CDBH]",
            "UL RSSI",
            "UL RSSI [RSSI-SINR]",
            "UL RSSI PUCCH [CDBH]",
            "MV_Average number of used DL PRBs [CDBH]",
            "MV_RRC Setup Success Rate [CDBH]",
            "MV_ERAB Setup Success Rate [CDBH]",
            "MV_PS Drop Call Rate % [CDBH]",
            "MV_UL User Throughput_Kbps [CDBH]",
            "MV_Max Connected User",
            "MV_PUSCH SINR [CBBH]",
            "MV_Average UE Distance KM [CDBH]",
            "MV_PS handover success rate [LTE Inter System] [CDBH]",
            "MV_PS handover success rate [LTE Intra System] [CDBH]",
            "MV_VoLTE DCR [CDBH]",
            "MV_Packet Loss DL [CDBH]",
            "MV_Packet Loss UL [CDBH]",
            "PS InterF HOSR [CDBH]",
            "PS IntraF HOSR [CDBH]",
            "MV eCell Data BH",
            "RS Power [dB]",
            "dlRsBoost",
            # "MV_UL_RSSI_dBm_PRB",
            "MV_CSFB Redirection Success Rate [CDBH]",
            "VoLTE Inter-Frequency Handover Success Ratio [CBBH]",
            "VoLTE Intra-LTE Handover Success Ratio [CBBH]",
            "MV_RRC Setup Success Rate_DENOM",
            "MV_DL User Throughput_Kbps [CUBH]",
            "Average UE Distance_KM [CDBH]",
            "MV_VoLTE Packet Loss UL [CBBH]",
            "MV_VoLTE Packet Loss DL [CBBH]",
        ]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return Response(
                {
                    "status": False,
                    "error": f"Missing columns: {', '.join(missing_columns)}",
                },
                status=400,
            )
    except Exception as e:
        return Response(
            {"status": False, "error": f"Data preparation error: {str(e)}"}, status=500
        )

    present_dates = df["Date"].unique()
    present_dates = pd.to_datetime(present_dates).strftime("%Y-%m-%d").tolist()
    exists = Daily_4G_KPI.objects.filter(Date__in=present_dates).values_list(
        "Date", flat=True
    )
    kpiStrToZero = [
        "MV_UL User Throughput_Kbps [CDBH]",
        "MV_DL User Throughput_Kbps [CDBH]",
        "MV_DL User Throughput_Kbps [CUBH]",
    ]
    for x in kpiStrToZero:
        # df[x] = df[x].replace(to_replace='.*', value=0, regex=True)
        df[x] = pd.to_numeric(df[x], errors="coerce").fillna(0)

    if not exists:
        objects_to_create = []
        try:
            for _, row in df.iterrows():

                print(row["MV eCell Data BH"], type(row["MV eCell Data BH"]))
                # print("MV_DL User Throughput_Kbps [CDBH]: ",row['MV_DL User Throughput_Kbps [CDBH]'],type(row['MV_DL User Throughput_Kbps [CDBH]']))
                if isinstance(row["MV eCell Data BH"], time):
                    print("here..")
                    mv_date_bh = timezone.localize(row["MV eCell Data BH"])
                else:
                    mv_date_bh = None

                if pd.notnull(row["Date"]):
                    obj = Daily_4G_KPI(
                        Short_name=row["Short name"],
                        Date=row["Date"],
                        ECGI_4G=row["ECGI"],
                        MV_Site_Name=row.get("MV Site Name", ""),
                        OEM_GGSN=row["OEM_GGSN"],
                        MV_Freq_Band=row.get("MV Freq_Band", ""),
                        MV_Freq_Bandwidth=row.get("MV Freq_Bandwidth", ""),
                        MV_Radio_NW_Availability=row["MV_Radio NW Availability"],
                        MV_4G_Data_Volume_GB=row["MV_4G Data Volume_GB"],
                        MV_VoLTE_raffic=row["MV_VoLTE Traffic"],
                        name_SiteA=row.get("name_SiteA", 0),
                        name_SiteB=row.get("name_SiteB", 0),
                        MV_DL_User_Throughput_Kbps=row[
                            "MV_DL User Throughput_Kbps [CDBH]"
                        ],
                        MV_E_UTRAN_Average_CQI=row["MV_E-UTRAN Average CQI [CDBH]"],
                        UL_RSSI=row["UL RSSI"],
                        # MV_UL_RSSI_dBm_PRB=row["UL RSSI PUCCH [CDBH]"],
                        MV_Average_number_of_used_DL_PRBs=row[
                            "MV_Average number of used DL PRBs [CDBH]"
                        ],
                        MV_RRC_Setup_Success_Rate=row[
                            "MV_RRC Setup Success Rate [CDBH]"
                        ],
                        MV_ERAB_Setup_Success_Rate=row[
                            "MV_ERAB Setup Success Rate [CDBH]"
                        ],
                        MV_PS_Drop_Call_Rate=row["MV_PS Drop Call Rate % [CDBH]"],
                        MV_UL_User_Throughput_Kbps=row[
                            "MV_UL User Throughput_Kbps [CDBH]"
                        ],
                        MV_Max_Connecteda_User=row["MV_Max Connected User"],
                        MV_PUCCH_SINR=row["MV_PUSCH SINR [CBBH]"],
                        MV_Average_UE_Distance_KM=row[
                            "MV_Average UE Distance KM [CDBH]"
                        ],
                        MV_PS_handover_success_rate_LTE_INTER_SYSTEM=row[
                            "MV_PS handover success rate [LTE Inter System] [CDBH]"
                        ],
                        MV_PS_handover_success_rate_LTE_INTRA_SYSTEM=row[
                            "MV_PS handover success rate [LTE Intra System] [CDBH]"
                        ],
                        MV_VoLTE_DCR=row["MV_VoLTE DCR [CDBH]"],
                        MV_Packet_Loss_DL=row["MV_Packet Loss DL [CDBH]"],
                        MV_Packet_Loss_UL=row["MV_Packet Loss UL [CDBH]"],
                        PS_InterF_HOSR=row["PS InterF HOSR [CDBH]"],
                        PS_IntraF_HOSR=row["PS IntraF HOSR [CDBH]"],
                        MV_eCell_Data_BH=mv_date_bh,
                        dlRsBoost=row["dlRsBoost"],
                        RS_Power_dB=row["RS Power [dB]"],
                        UL_RSSI_Nokia_RSSI_SINR=row["UL RSSI [RSSI-SINR]"],
                        MV_CSFB_Redirection_Success_Rate=row[
                            "MV_CSFB Redirection Success Rate [CDBH]"
                        ],
                        VoLTE_Inter_Frequency_Handover_Success_Ratio=row[
                            "VoLTE Inter-Frequency Handover Success Ratio [CBBH]"
                        ],
                        VoLTE_Intra_LTE_Handover_Success_Ratio=row[
                            "VoLTE Intra-LTE Handover Success Ratio [CBBH]"
                        ],
                        MV_RRC_Setup_Success_Rate_DENOM=row[
                            "MV_RRC Setup Success Rate_DENOM"
                        ],
                        MV_DL_User_Throughput_Kbps_CUBH=row["MV_DL User Throughput_Kbps [CUBH]"],
                        Sams_Average_UE_Distance_KM=row[
                            "Average UE Distance_KM [CDBH]"
                        ],
                        MV_VoLTE_Packet_Loss_UL_CBBH=row[
                            "MV_VoLTE Packet Loss UL [CBBH]"
                        ],
                        MV_VoLTE_Packet_Loss_DL_CBBH=row[
                            "MV_VoLTE Packet Loss DL [CBBH]"
                        ],
                        # UL_RSSI_Nokia_RSSI_SINR = row["UL RSSI [RSSI-SINR]"],
                    )
                    objects_to_create.append(obj)
            with transaction.atomic():
                print("finally get here...")
                Daily_4G_KPI.objects.bulk_create(objects_to_create)
            return Response(
                {
                    "status": True,
                    "message": "Data inserted successfully.",
                }
            )
        except Exception as e:
            return Response({"status": False, "error": f"{str(e)}"}, status=500)

    return Response(
        {
            "status": False,
            "message": "Data for these dates already exists in the database.",
            "existing_dates": exists,
        }
    )


timezone = pytz.timezone("UTC")


@api_view(["POST"])
def tantitive_counters_save_data(request):
    file = request.FILES.get("tantative_counters_file")
    if not file:
        return Response({"status": False, "message": "No file provided."}, status=400)

    try:
        df = pd.read_csv(file)
        df["Short name"] = df["Short name"].fillna(method="ffill")
        df["Nokia_S1_Failures_MME_Issue"] = df["Nokia_S1_Failures_MME_Issue"].apply(
            lambda x: np.nan if isinstance(x, str) else x
        )
        df["S1_Failures_MME_Issue"] = df["S1_Failures_MME_Issue"].apply(
            lambda x: np.nan if isinstance(x, str) else x
        )

        df.rename(columns={"Unnamed: 1": "DateTime"}, inplace=True)
        # df.to_csv("daku_mangel_singh.csv")
        # exit(0)
    except Exception as e:
        return Response({"status": False, "error": str(e)}, status=500)

    required_columns = [
        "Short name",
        "DateTime",
        "S1 Failure CDBH",
        "Nokia_S1_Failures_MME_Issue",
        "S1_Failures_MME_Issue",
        "MME Generated Issues on Cells",
        "LS1AP.S1AP_PARTIAL_RESET_INIT_MME",
        "LS1AP.S1AP_KILL_REQ",
        "LS1AP.S1AP_KILL_RESP",
        "LRRC.REJ_RRC_CONN_RE_ESTAB",
        "LRRC.RRC_PAGING_REQUESTS",
        "LRRC.RRC_CON_RE_ESTAB_ATT_HO_FAIL",
        "LRRC.RRC_CON_RE_ESTAB_ATT_OTHER",
        "RRC_CONN_REL_TA_LIMIT",
        "LEPSB.EPC_EPS_BEARER_REL_REQ_NORM",
        "LEPSB.EPC_EPS_BEARER_REL_REQ_DETACH",
        "LEPSB.EPC_EPS_BEARER_REL_REQ_RNL",
        "LEPSB.EPC_EPS_BEARER_REL_REQ_OTH",
        "LEPSB.ERAB_NBR_DL_FAIL_OVL",
        "LEPSB.ERAB_NBR_UL_FAIL_OVL",
        "LEPSB.ERAB_REL_DOUBLE_S1",
        "LEPSB.ERAB_REL_ALL_ABNORMAL_H_PWR_UE",
        "LXPL.SCG_ADD_COMPLETION_FAIL_T",
        "LXPL.SGNB_ADD_COMPL_FAIL_T",
        "LXPL.SCG_MOD_ADD_MENB_COMPL_FAIL_T",
        "NX2CC.NX2CC_RAB_REL_ATT_MENB",
        "NX2CC.NX2CC_RAB_REL_NORM_MENB",
        "NX2CC.NX2CC_RAB_REL_ATT_SGNB",
        "NX2CC.NX2CC_RAB_REL_ABNORM_SGNB",
        "NX2CC.NX2CC_RAB_REL_PREEM_SGNB",
        "RSRP Samples<-116 dBm",
        "TNL Failure Count",
        "TNL Failure %",
        "LRRC.DISC_RRC_PAGING",
        "MV_Radio NW Availability",
        "UL RSSI",
        "Bler UL",
        "Bler DL",
        "LEPSB.ERAB_REL_ENB_TNL_TRU",
        "LEPSB.ERAB_INI_SETUP_FAIL_TNL_TRU",
        "LEPSB.ERAB_INI_SETUP_FAIL_RNL_UEL",
        "LEPSB.ERAB_INI_SETUP_FAIL_RNL_RRNA",
        "LEPSB.ERAB_INI_SETUP_FAIL_RNL_RIP",
        "LUEST.SIGN_EST_F_RRCCOMPL_MISSING",
        "LUEST.SIGN_CONN_ESTAB_FAIL_PUCCH",
        "LUEST.SIGN_CONN_ESTAB_FAIL_MAXRRC",
    ]

    # LEPSB.EPC_EPS_BEAR_REL_REQ_N_QCI1	LEPSB.EPC_EPS_BEAR_REL_REQ_O_QCI1LEPSB.EPC_EPS_BEAR_REL_REQ_D_QCI1	LEPSB.EPC_EPS_BEAR_REL_REQ_R_QCI1		LEPSB.EPC_EPS_BEAR_REL_REQ_R_QCI2	LEPSB.EPC_EPS_BEAR_REL_REQ_O_QCI2	LEPSB.ERAB_REL_DOUBLE_S1_QCI1

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return Response(
            {
                "status": False,
                "error": f"Missing columns: {', '.join(missing_columns)}",
            },
            status=400,
        )

    objects_to_create = []
    for _, row in df.iterrows():
        try:
            date_time = datetime.strptime(row["DateTime"], "%d/%m/%y, %H:%M")
            date_time = timezone.localize(date_time)
            obj = Tantitive_Counters_24_Hours(
                Short_name=row["Short name"],
                DateTime=date_time,
                S1_Failure_CDBH=row["S1 Failure CDBH"],
                Nokia_S1_Failures_MME_Issue=row["Nokia_S1_Failures_MME_Issue"],
                S1_Failures_MME_Issue=row["S1_Failures_MME_Issue"],
                MME_Generated_Issues_on_Cells=row["MME Generated Issues on Cells"],
                LS1AP_S1AP_PARTIAL_RESET_INIT_MME=row[
                    "LS1AP.S1AP_PARTIAL_RESET_INIT_MME"
                ],
                LS1AP_S1AP_KILL_REQ=row["LS1AP.S1AP_KILL_REQ"],
                LS1AP_S1AP_KILL_RESP=row["LS1AP.S1AP_KILL_RESP"],
                LRRC_REJ_RRC_CONN_RE_ESTAB=row["LRRC.REJ_RRC_CONN_RE_ESTAB"],
                LRRC_RRC_PAGING_REQUESTS=row["LRRC.RRC_PAGING_REQUESTS"],
                LRRC_RRC_CON_RE_ESTAB_ATT_HO_FAIL=row[
                    "LRRC.RRC_CON_RE_ESTAB_ATT_HO_FAIL"
                ],
                LRRC_RRC_CON_RE_ESTAB_ATT_OTHER=row["LRRC.RRC_CON_RE_ESTAB_ATT_OTHER"],
                RRC_CONN_REL_TA_LIMIT=row["RRC_CONN_REL_TA_LIMIT"],
                LEPSB_EPC_EPS_BEARER_REL_REQ_NORM=row[
                    "LEPSB.EPC_EPS_BEARER_REL_REQ_NORM"
                ],
                LEPSB_EPC_EPS_BEARER_REL_REQ_DETACH=row[
                    "LEPSB.EPC_EPS_BEARER_REL_REQ_DETACH"
                ],
                LEPSB_EPC_EPS_BEARER_REL_REQ_RNL=row[
                    "LEPSB.EPC_EPS_BEARER_REL_REQ_RNL"
                ],
                LEPSB_EPC_EPS_BEARER_REL_REQ_OTH=row[
                    "LEPSB.EPC_EPS_BEARER_REL_REQ_OTH"
                ],
                LEPSB_ERAB_NBR_DL_FAIL_OVL=row["LEPSB.ERAB_NBR_DL_FAIL_OVL"],
                LEPSB_ERAB_NBR_UL_FAIL_OVL=row["LEPSB.ERAB_NBR_UL_FAIL_OVL"],
                LEPSB_ERAB_REL_DOUBLE_S1=row["LEPSB.ERAB_REL_DOUBLE_S1"],
                LEPSB_ERAB_REL_ALL_ABNORMAL_H_PWR_UE=row[
                    "LEPSB.ERAB_REL_ALL_ABNORMAL_H_PWR_UE"
                ],
                LXPL_SCG_ADD_COMPLETION_FAIL_T=row["LXPL.SCG_ADD_COMPLETION_FAIL_T"],
                LXPL_SGNB_ADD_COMPL_FAIL_T=row["LXPL.SGNB_ADD_COMPL_FAIL_T"],
                LXPL_SCG_MOD_ADD_MENB_COMPL_FAIL_T=row[
                    "LXPL.SCG_MOD_ADD_MENB_COMPL_FAIL_T"
                ],
                NX2CC_NX2CC_RAB_REL_ATT_MENB=row["NX2CC.NX2CC_RAB_REL_ATT_MENB"],
                NX2CC_NX2CC_RAB_REL_NORM_MENB=row["NX2CC.NX2CC_RAB_REL_NORM_MENB"],
                NX2CC_NX2CC_RAB_REL_ATT_SGNB=row["NX2CC.NX2CC_RAB_REL_ATT_SGNB"],
                NX2CC_NX2CC_RAB_REL_ABNORM_SGNB=row["NX2CC.NX2CC_RAB_REL_ABNORM_SGNB"],
                NX2CC_NX2CC_RAB_REL_PREEM_SGNB=row["NX2CC.NX2CC_RAB_REL_PREEM_SGNB"],
                RSRP_Samples_lt_116_dBm=row["RSRP Samples<-116 dBm"],
                TNL_Failure_Count=row["TNL Failure Count"],
                TNL_Failure_Percent=row["TNL Failure %"],
                LRRC_DISC_RRC_PAGING=row["LRRC.DISC_RRC_PAGING"],
                MV_Radio_NW_Availability=row["MV_Radio NW Availability"],
                UL_RSSI=row["UL RSSI"],
                UL_BLER=row["Bler UL"],
                DL_BLER=row["Bler DL"],
                LUEST_SIGN_CONN_ESTAB_FAIL_MAXRRC=row[
                    "LUEST.SIGN_CONN_ESTAB_FAIL_MAXRRC"
                ],
                LUEST_SIGN_CONN_ESTAB_FAIL_PUCCH=row[
                    "LUEST.SIGN_CONN_ESTAB_FAIL_PUCCH"
                ],
                LUEST_SIGN_EST_F_RRCCOMPL_MISSING=row[
                    "LUEST.SIGN_EST_F_RRCCOMPL_MISSING"
                ],
                LEPSB_ERAB_INI_SETUP_FAIL_RNL_RIP=row[
                    "LEPSB.ERAB_INI_SETUP_FAIL_RNL_RIP"
                ],
                LEPSB_ERAB_INI_SETUP_FAIL_RNL_RNA=row[
                    "LEPSB.ERAB_INI_SETUP_FAIL_RNL_RRNA"
                ],
                LEPSB_ERAB_INI_SETUP_FAIL_RNL_UEL=row[
                    "LEPSB.ERAB_INI_SETUP_FAIL_RNL_UEL"
                ],
                LEPSB_ERAB_INI_SETUP_FAIL_TNL_TRU=row[
                    "LEPSB.ERAB_INI_SETUP_FAIL_TNL_TRU"
                ],
                LEPSB_ERAB_REL_ENB_TNL_TRU=row["LEPSB.ERAB_REL_ENB_TNL_TRU"],
            )
            objects_to_create.append(obj)
        except Exception as e:
            return Response({"status": False, "error": str(e)}, status=400)

    try:
        with transaction.atomic():
            Tantitive_Counters_24_Hours.objects.bulk_create(objects_to_create)
    except Exception as e:
        return Response({"status": False, "error": str(e)}, status=500)

    return Response({"status": True, "message": "Data inserted successfully."})


def calculate_datetime_range(datetime):
    # Parse the input datetime string to a datetime object
    # input_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    input_datetime = datetime
    # Calculate the start time (2 hours before)
    start_datetime = input_datetime - timedelta(hours=2)

    # Calculate the end time (2 hours after)
    end_datetime = input_datetime + timedelta(hours=2)

    # Format start and end times back to "YYYY-MM-DD HH:MM"
    start_datetime_str = start_datetime.strftime("%Y-%m-%d %H:%M")
    end_datetime_str = end_datetime.strftime("%Y-%m-%d %H:%M")
    # print(start_datetime_str, end_datetime_str)
    return start_datetime, end_datetime


def save_df_to_model(df, date):
    # Ensure the DataFrame has the correct columns
    expected_columns = [
        "Cell_name",
        "OEM_GGSN",
        "KPI",
        "cell_value",
        "threshold_value",
        "check",
        "RCA",
        "Proposed Solution",
        "history_alarms",
        "circle",
    ]
    if not all(col in df.columns for col in expected_columns):
        raise ValueError("DataFrame does not have the required columns")

    df_list = df.to_dict("records")
    unique_values = [(record["Cell_name"], date) for record in df_list]

    # Fetch existing objects from the database
    existing_objs = RCA_output_table.objects.filter(
        Cell_name__in=[x[0] for x in unique_values], date=date
    )

    # Create a dictionary to map existing objects for quick lookup
    existing_records = {(obj.Cell_name, obj.date): obj for obj in existing_objs}

    # Lists to hold objects to update and create
    objs_to_update = []
    objs_to_create = []

    # Iterate through the DataFrame records
    for record in df_list:
        key = (record["Cell_name"], date)
        if key in existing_records:
            # Update existing object
            obj = existing_records[key]
            obj.cell_value = record["cell_value"]
            obj.OEM_GGSN = record["OEM_GGSN"]
            obj.threshold_value = record["threshold_value"]
            obj.check_condition = record["check"]
            obj.RCA = record["RCA"]
            obj.Proposed_Solution = record["Proposed Solution"]
            obj.history_alarms = record["history_alarms"]
            obj.circle = record["circle"]
            obj.KPI = record["KPI"]
            objs_to_update.append(obj)
        else:
            # Create a new object
            new_obj = RCA_output_table(
                Cell_name=record["Cell_name"],
                date=date,
                cell_value=record["cell_value"],
                OEM_GGSN=record["OEM_GGSN"],
                threshold_value=record["threshold_value"],
                check_condition=record["check"],
                RCA=record["RCA"],
                Proposed_Solution=record["Proposed Solution"],
                history_alarms=record["history_alarms"],
                circle=record["circle"],
                KPI=record["KPI"],
            )
            objs_to_create.append(new_obj)

    # Perform bulk update and bulk create
    if objs_to_update:
        RCA_output_table.objects.bulk_update(
            objs_to_update,
            [
                "cell_value",
                "threshold_value",
                "check_condition",
                "RCA",
                "Proposed_Solution",
                "history_alarms",
                "circle",
                "KPI",
            ],
        )

    if objs_to_create:
        RCA_output_table.objects.bulk_create(objs_to_create)

    print("Records processed successfully.")


def accessibility_rca(KPI_4G_record_df, KPI_row, alarm_data_df, tentative_counter_df):
    def perticular_condotion_check(
        KPI, cell_record, alarm_data_df, tentative_counter_df
    ):
        RCA_TABLE_OBJS = RCA_TABLE.objects.filter(KPI=KPI).values()
        RCA_TABLE_df = pd.DataFrame(RCA_TABLE_OBJS)

        rca = []
        solution = []
        history_alarms = []

        mv_cell_data_BH = cell_record.get("MV_eCell_Data_BH")
        short_name = cell_record["Short_name"]
        # print(short_name)
        if mv_cell_data_BH is None:
            return (
                ["MV eCell Data BH is None in daily 4G KPI table"],
                solution,
                history_alarms,
            )

        tantative_cell_record = tentative_counter_df[
            (tentative_counter_df["Short_name"] == short_name)
            & (tentative_counter_df["DateTime"].dt.time == mv_cell_data_BH)
        ]
        # if cell_record["Short_name"] == 'MU_E_F1_OM_2972B_B':
        #          tentative_counter_df.to_csv("tentative_file_MU_E_F1_OM_2972B_B.csv")
        #  exit(0)
        if tantative_cell_record.empty:
            return (
                [f" Cell not found in tentative counter table"],
                solution,
                history_alarms,
            )
        # tantative_cell_record.to_csv("tentative_file.csv")
        tantative_cell_record_series = tantative_cell_record.iloc[0]

        # exit(0)
        for i, row in RCA_TABLE_df.iterrows():
            # print("jiji")
            if row["Data_source"] == "MYCOM":
                # print("_________my_com___________")
                # print("_________my_com___________",tantative_cell_record_series[row['Tentative_counters']],type(tantative_cell_record_series[row['Tentative_counters']]))
                # print("tentative counter:",row['Tentative_counters'],"actual_value:",tantative_cell_record_series[row['Tentative_counters']],"tentative counter:",row["Condition_check"])
                if OPERATORS_dict[row.Operator](
                    tantative_cell_record_series[row["Tentative_counters"]],
                    row["Condition_check"],
                ):
                    # print("______condition_check__")
                    rca.append(row["RCA"])
                    solution.append(row["Proposed_solution"])
            elif row["Data_source"] == "Alarm dump":
                mrbts_id = cell_record["MRBTS_ID"]
                # print(cell_record['Short_name'],mrbts_id)
                combine_datetime = datetime.combine(
                    cell_record["Date"], cell_record["MV_eCell_Data_BH"]
                )

                # print(combine_datetime)

                start_datetime, end_datetime = calculate_datetime_range(
                    combine_datetime
                )
                alarm_data_df_active = alarm_data_df[
                    (alarm_data_df["MRBTS_ID"] == mrbts_id)
                    & (alarm_data_df["AlarmTime"].dt.tz_localize(None) <= end_datetime)
                    & alarm_data_df["CancelState"]
                    == "False"
                ]
                # alarm_data_df.to_csv("alarm_aaram_data.csv"   T``
                # \G             # exit(0)
                if alarm_data_df_active.empty:
                    print("empty alarm file")
                else:
                    print("not empty alarm file")

                # exit(0)
                supplementry_information = alarm_data_df_active[
                    "SupplementaryInformation"
                ].to_list()

                if row["Tentative_counters"] in supplementry_information:
                    print("fount the alarm")
                    rca.append(row["RCA"])
                    solution.append(row["Proposed_solution"])

                ############### for history alarms ##################
                alarm_data_df_history = alarm_data_df[
                    (alarm_data_df["MRBTS_ID"] == mrbts_id)
                    & (alarm_data_df["CancelState"] == "True")
                    & (alarm_data_df["AlarmTime"].dt.date == cell_record["Date"])
                ]
                # alarm_data_df.to_csv("alarm_aaram_data.csv"   T``
                # \G             # exit(0)
                if alarm_data_df_history.empty:
                    print("empty alarm file")
                else:
                    print("not empty alarm file")

                # exit(0)
                supplementry_information = alarm_data_df_history[
                    "SupplementaryInformation"
                ].to_list()

                if row["Tentative_counters"] in supplementry_information:
                    print("fount the alarm")
                    history_alarms.append(row["Tentative_counters"])

        return rca, solution, history_alarms

    rca_report = []
    for i, cell_record in KPI_4G_record_df.iterrows():
        #  print(cell_record['Short_name'])

        #  print(KPI_row['KPI'])
        kpi = KPI_row["KPI"]
        if OPERATORS_dict[KPI_row.operator](cell_record[kpi], KPI_row.threshold_value):
            #  print(KPI_row.operator)
            #  print("cell_value; ",cell_record[kpi]," threshold_value: ",KPI_row.threshold_value)
            #  print("true")
            rca_report.append(
                {
                    "Cell_name": cell_record["Short_name"],
                    "OEM_GGSN": cell_record["OEM_GGSN"],
                    "KPI": kpi,
                    "cell_value": cell_record[kpi],
                    "threshold_value": KPI_row.threshold_value,
                    "check": "OK",
                    "RCA": "",
                    "Proposed Solution": "",
                    "history_alarms": "",
                }
            )
        else:
            rca, solution, history_alarms = perticular_condotion_check(
                kpi, cell_record, alarm_data_df, tentative_counter_df
            )

            rca_str = ",".join(rca)
            solution_str = ",".join(solution)
            history_str = ",".join(history_alarms)

            #  print(rca_str,solution_str)
            rca_report.append(
                {
                    "Cell_name": cell_record["Short_name"],
                    "OEM_GGSN": cell_record["OEM_GGSN"],
                    "KPI": kpi,
                    "cell_value": cell_record[kpi],
                    "threshold_value": KPI_row.threshold_value,
                    "check": "NOT OK",
                    "RCA": rca_str,
                    "Proposed Solution": solution_str,
                    "history_alarms": history_str,
                }
            )
        #  print(KPI_row.operator)
        #  print("cell_value; ",cell_record[kpi]," threshold_value: ",KPI_row.threshold_value)
        #  print('false')
    return rca_report


def payload_rca(latest_date, alarm_data_df):
    RCA_payload_table_df = pd.DataFrame(RCA_payload_table.objects.all().values())

    def check_condition(cell_record, alarm_data_df):

        rca = []
        solution = []
        history_alarms = []
        for i, row in RCA_payload_table_df.iterrows():
            if row["Data_source"] == "MYCOM":
                if row["Data_source"] == "MYCOM":
                    # print('operator..',row.Operator)
                    if not (row.Operator == "=<=<"):
                        if OPERATORS_dict[row.Operator](
                            cell_record[row["Tentative_counters"]],
                            row["Condition_check"],
                        ):
                            # print("______condition_check__")

                            rca.append(row["RCA"])
                            solution.append(row["Proposed_solution"])
                    else:
                        if OPERATORS_dict[row.Operator](
                            cell_record[row["Tentative_counters"]], -30, 30
                        ):
                            # print("______condition_check__")

                            rca.append(row["RCA"])
                            solution.append(row["Proposed_solution"])

            elif row["Data_source"] == "Alarm dump":
                mrbts_id = cell_record["MRBTS_ID"]
                # print(cell_record['Short_name'],mrbts_id)
                alarm_data_df_active = alarm_data_df[
                    (alarm_data_df["MRBTS_ID"] == mrbts_id)
                    & alarm_data_df["CancelState"]
                    == "False"
                ]
                # alarm_data_df.to_csv("alarm_aaram_data.csv"   T``
                # \G             # exit(0)
                if alarm_data_df_active.empty:
                    print("empty alarm file")
                else:
                    print("not empty alarm file")

                # exit(0)
                supplementry_information = alarm_data_df_active[
                    "SupplementaryInformation"
                ].to_list()

                if row["Tentative_counters"] in supplementry_information:
                    print("fount the alarm")
                    rca.append(row["RCA"])
                    solution.append(row["Proposed_solution"])

                ############### for history alarms ##################
                alarm_data_df_history = alarm_data_df[
                    (alarm_data_df["MRBTS_ID"] == mrbts_id)
                    & (alarm_data_df["CancelState"] == "True")
                    & (alarm_data_df["AlarmTime"].dt.date == cell_record["Date_N"])
                ]
                # alarm_data_df.to_csv("alarm_aaram_data.csv"   T``
                # \G             # exit(0)
                if alarm_data_df_history.empty:
                    print("empty alarm file")
                else:
                    print("not empty alarm file")

                # exit(0)
                supplementry_information = alarm_data_df_history[
                    "SupplementaryInformation"
                ].to_list()

                if row["Tentative_counters"] in supplementry_information:
                    print("fount the alarm")
                    history_alarms.append(row["Tentative_counters"])

        return rca, solution, history_alarms

    rca_report = []
    response = requests.get(
        "http://103.242.225.195:8000/Zero_Count_Rna_Payload_Tool/Date_Wise_Dashboard/"
    )
    data = response.json()
    date_n = latest_date
    date_n_1 = date_n - timedelta(1)
    pyl_dip_cell = data.get("payload_dip_cells")
    db_n = Daily_4G_KPI.objects.filter(Date=date_n).values().order_by("Short_name")
    db_n_1 = Daily_4G_KPI.objects.filter(Date=date_n_1).values().order_by("Short_name")

    df_N = pd.DataFrame(db_n)
    df_N_1 = pd.DataFrame(db_n_1)

    # df_N=pd.DataFrame(db_n)[:500]
    # df_N_1=pd.DataFrame(db_n_1)[:500]
    # df_N=df_N[df_N["Short_name"]=='AP_E_F3_OM_HY6852B_B']
    # df_N_1=df_N_1[df_N_1["Short_name"]=='AP_E_F3_OM_HY6852B_B']
    if df_N.empty or df_N_1.empty:
        return []
    else:
        df_N["Short_name"] = df_N["Short_name"].ffill()
        df_N_1["Short_name"] = df_N_1["Short_name"].ffill()
        merged_df = pd.merge(
            df_N, df_N_1, on="Short_name", how="left", suffixes=["_N", "_N_1"]
        )
        # for cell in merged_df.columns:
        #     print(cell)
        merged_df["dev ue distance"] = round(
            (
                (
                    (
                        merged_df["MV_Average_UE_Distance_KM_N"]
                        - merged_df["MV_Average_UE_Distance_KM_N_1"]
                    )
                )
                / merged_df["MV_Average_UE_Distance_KM_N_1"]
            )
            * 100,
            2,
        )
        merged_df["dev RS Power [dB]"] = (
            merged_df["RS_Power_dB_N"] - merged_df["RS_Power_dB_N_1"]
        )
        merged_df["dev dlRsBoost"] = (
            merged_df["dlRsBoost_N"] - merged_df["dlRsBoost_N_1"]
        )

        merged_df["dev UL RSSI"] = np.where(
            (merged_df["UL_RSSI_N"] - merged_df["UL_RSSI_N_1"]) < 0,
            0,
            np.where(
                merged_df["UL_RSSI_N"] > -102,
                merged_df["UL_RSSI_N"] - merged_df["UL_RSSI_N_1"],
                0,
            ),
        )
        op_df = merged_df[
            [
                "Short_name",
                "Date_N",
                "ECGI_4G_N",
                "MV_Radio_NW_Availability_N",
                "dev UL RSSI",
                "dev dlRsBoost",
                "dev RS Power [dB]",
                "dev ue distance",
            ]
        ].fillna(value=0)

        # print(op_df)
        op_df["MRBTS_ID"] = op_df["ECGI_4G_N"].str.split("-").str[-2]
        kpi = "MV_4G_Data_Volume_GB_N"
        for i, cell_record in op_df.iterrows():
            if cell_record["Short_name"] not in pyl_dip_cell:
                rca_report.append(
                    {
                        "Cell_name": cell_record["Short_name"],
                        "KPI": kpi,
                        "cell_value": 0,
                        "threshold_value": 0,
                        "check": "OK",
                        "RCA": "",
                        "Proposed Solution": "",
                        "history_alarms": "",
                    }
                )
            else:
                rca, solution, history_alarms = check_condition(
                    cell_record, alarm_data_df
                )

                rca_str = ",".join(rca)
                solution_str = ",".join(solution)
                history_str = ",".join(history_alarms)

                #  print(rca_str,solution_str)
                rca_report.append(
                    {
                        "Cell_name": cell_record["Short_name"],
                        "KPI": kpi,
                        "cell_value": 0,
                        "threshold_value": 0,
                        "check": "NOT OK",
                        "RCA": rca_str,
                        "Proposed Solution": solution_str,
                        "history_alarms": history_str,
                    }
                )
            #  print(KPI_row.operator)
            #  print("cell_value; ",cell_record[kpi]," threshold_value: ",KPI_row.threshold_value)
            #  print('false')
    return rca_report


def throupt_rca(KPI_4G_record_df, collable_date, tentative_counter_df, KPI_row):

    def process_tentative_counter_df(api_url, data, tentative_counter_df):
        response = requests.post(api_url, json=data)

        # Check if the request was successful
        if response.status_code == 200:
            # Convert the JSON data to a DataFrame
            # print(response.text)
            tentative_counter_df = pd.DataFrame(response.json().get("data"))
        else:
            print(f"Error: {response.status_code}", response.text)
        tentative_counter_df["DateTime"] = pd.to_datetime(
            tentative_counter_df["DateTime"]
        )

        tentative_counter_df

        tentative_counter_df["Date"] = tentative_counter_df["DateTime"].dt.date
        tentative_counter_df["Time"] = tentative_counter_df["DateTime"].dt.time
        return tentative_counter_df

    def process_MV_E_UTRAN_Average_CQI(api_url, data):
        response = requests.post(api_url, json=data)

        # Check if the request was successful
        if response.status_code == 200:
            # Convert the JSON data to a DataFrame
            # print(response)
            cqi_day_data_df = pd.DataFrame(response.json())
        else:
            print(f"Error: {response.status_code}")

        cqi_day_data_df.drop(
            ["date_1_val", "date_2_val", "date_3_val"], inplace=True, axis=1
        )
        cqi_day_data_df = cqi_day_data_df.drop_duplicates(
            subset="Short_name", keep="first"
        )
        columns_to_rename = [
            "week_1_val",
            "week_2_val",
            "date_4_val",
            "date_5_val",
            "date_6_val",
            "date_7_val",
            "date_8_val",
        ]

        # Renaming with a suffix
        cqi_day_data_df = cqi_day_data_df.rename(
            columns={col: f"{col}_CQI" for col in columns_to_rename}
        )
        return cqi_day_data_df

    def process_MV_Radio_NW_Availability(api_url, data):
        response = requests.post(api_url, json=data)

        # Check if the request was successful
        if response.status_code == 200:
            # Convert the JSON data to a DataFrame
            print(response)
            rna_5day_data_df = pd.DataFrame(response.json())
        else:
            print(f"Error: {response.status_code}")

        rna_5day_data_df = rna_5day_data_df.drop_duplicates(
            subset="Short_name", keep="first"
        )

        rna_5day_data_df.drop(
            ["date_1_val", "date_2_val", "date_3_val"], inplace=True, axis=1
        )

        columns_to_rename = [
            "week_1_val",
            "week_2_val",
            "date_4_val",
            "date_5_val",
            "date_6_val",
            "date_7_val",
            "date_8_val",
        ]

        # Renaming with a suffix
        rna_5day_data_df = rna_5day_data_df.rename(
            columns={col: f"{col}_rna" for col in columns_to_rename}
        )
        return rna_5day_data_df

    def process_ul_rssi(api_url, data):
        response = requests.post(api_url, json=data)

        # Check if the request was successful
        if response.status_code == 200:
            # Convert the JSON data to a DataFrame
            # print(response)
            ul_rssi_day_data_df = pd.DataFrame(response.json())
        else:
            print(f"Error: {response.status_code}")
        ul_rssi_day_data_df = ul_rssi_day_data_df.drop_duplicates(
            subset="Short_name", keep="first"
        )
        ul_rssi_day_data_df.drop(
            ["date_1_val", "date_2_val", "date_3_val"], inplace=True, axis=1
        )

        columns_to_rename = [
            "week_1_val",
            "week_2_val",
            "date_4_val",
            "date_5_val",
            "date_6_val",
            "date_7_val",
            "date_8_val",
        ]

        # Renaming with a suffix
        ul_rssi_day_data_df = ul_rssi_day_data_df.rename(
            columns={col: f"{col}_rssi" for col in columns_to_rename}
        )
        return ul_rssi_day_data_df

    def process_MV_Average_number_of_used_DL_PRBs(api_url, data):

        response = requests.post(api_url, json=data)

        # Check if the request was successful
        if response.status_code == 200:
            # Convert the JSON data to a DataFrame
            # print(response)
            prb_day_data_df = pd.DataFrame(response.json())
        else:
            print(f"Error: {response.status_code}")
        prb_day_data_df
        prb_day_data_df = prb_day_data_df.drop_duplicates(
            subset="Short_name", keep="first"
        )
        prb_day_data_df.drop(
            ["date_1_val", "date_2_val", "date_3_val"], inplace=True, axis=1
        )
        prb_day_data_df["max_prb_among _5_day"] = prb_day_data_df[
            ["date_4_val", "date_5_val", "date_6_val", "date_7_val", "date_8_val"]
        ].max(axis=1)
        columns_to_rename = [
            "week_1_val",
            "week_2_val",
            "date_4_val",
            "date_5_val",
            "date_6_val",
            "date_7_val",
            "date_8_val",
        ]

        # Renaming with a suffix
        prb_day_data_df = prb_day_data_df.rename(
            columns={col: f"{col}_prb" for col in columns_to_rename}
        )

        return prb_day_data_df

    def process_throupt_data(api_url, data):
        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            # Convert the JSON data to a DataFrame
            print(response.text)
            thpt_5day_data_df = pd.DataFrame(response.json())
        else:
            print(f"Error: {response.status_code}")

        thpt_5day_data_df.drop(
            ["week_1_val", "week_2_val", "date_1_val", "date_2_val", "date_3_val"],
            inplace=True,
            axis=1,
        )
        thpt_5day_data_df[
            ["date_4_val", "date_5_val", "date_6_val", "date_7_val", "date_8_val"]
        ] /= 1000
        thpt_5day_data_df["more_than_3_values"] = (
            thpt_5day_data_df[
                ["date_4_val", "date_5_val", "date_6_val", "date_7_val", "date_8_val"]
            ]
            >= 3
        ).sum(axis=1) >= 3
        thpt_5day_data_df["worst_thpt"] = thpt_5day_data_df[
            ["date_4_val", "date_5_val", "date_6_val", "date_7_val", "date_8_val"]
        ].idxmin(axis=1)

        thpt_5day_data_df = thpt_5day_data_df.drop_duplicates(
            subset="Short_name", keep="first"
        )
        thpt_5day_data_df["sector"] = (
            thpt_5day_data_df["Short_name"].str.split("_").str[-2].str[-1]
        )

        columns_to_rename = [
            "week_1_val",
            "week_2_val",
            "date_4_val",
            "date_5_val",
            "date_6_val",
            "date_7_val",
            "date_8_val",
        ]

        # Renaming with a suffix
        thpt_5day_data_df = thpt_5day_data_df.rename(
            columns={col: f"{col}_thpt" for col in columns_to_rename}
        )

        return thpt_5day_data_df

    condition_nokia = KPI_4G_record_df["Short_name"].str.startswith("@Nokia")
    removed_nokia_df = KPI_4G_record_df[~condition_nokia]
    condition_NE_ik = removed_nokia_df["Short_name"].str.startswith("NE-ik")
    removed_nokia_NE_ik_df = removed_nokia_df[~condition_NE_ik]
    removed_nokia_NE_ik_nospace_df = removed_nokia_NE_ik_df[
        removed_nokia_df["Short_name"].str.contains("_")
        | removed_nokia_df["Short_name"].str.startswith(",")
    ]
    condition_sams = removed_nokia_NE_ik_nospace_df["Short_name"].str.startswith("Sams")
    removed_nokia_NE_ik_nospace_sams_df = removed_nokia_NE_ik_nospace_df[
        ~condition_sams
    ]
    removed_nokia_NE_ik_nospace_sams_df[
        "site_id"
    ] = removed_nokia_NE_ik_nospace_sams_df["Short_name"].apply(
        lambda x: (
            x.split("_")[-3][:-1]
            if "_FDD" in x or "_TDD" in x
            else x.split("_")[-2][:-1]
        )
    )
    removed_nokia_NE_ik_nospace_sams_df["sector"] = (
        removed_nokia_NE_ik_nospace_sams_df["Short_name"].str.split("_").str[-2].str[-1]
    )
    removed_nokia_NE_ik_nospace_sams_df = (
        removed_nokia_NE_ik_nospace_sams_df.sort_values(
            by=["site_id", "sector", "MV_Freq_Band"]
        )
    )
    columns_order = ["site_id", "sector", "MV_Freq_Band"] + [
        col
        for col in removed_nokia_NE_ik_nospace_sams_df.columns
        if col not in ["site_id", "sector", "MV_Freq_Band"]
    ]
    removed_nokia_NE_ik_nospace_sams_df = removed_nokia_NE_ik_nospace_sams_df[
        columns_order
    ]
    removed_nokia_NE_ik_nospace_sams_df["MV_DL_User_Throughput_mbps"] = (
        removed_nokia_NE_ik_nospace_sams_df["MV_DL_User_Throughput_Kbps"] / 1000
    )
    removed_nokia_NE_ik_nospace_sams_df["MV_Freq_Band"] = (
        removed_nokia_NE_ik_nospace_sams_df["MV_Freq_Band"].astype(float)
    )

    #### processing the throupt_data_df

    api_url = f"http://103.242.225.195:8000/Zero_Count_Rna_Payload_Tool/get_daily_4g_kpi_report_by_date_and_kpi/"
    data = {"date": collable_date, "kpi_name": "MV_DL_User_Throughput_Kbps"}

    thpt_5day_data_df = process_throupt_data(api_url, data)
    cell_t_f_dict = (
        thpt_5day_data_df[["Short_name", "more_than_3_values"]]
        .set_index("Short_name")["more_than_3_values"]
        .to_dict()
    )

    # To find the ok and not ok value based on the 5 day data of the thpt
    # Create an empty DataFrame to store the results

    results_df = pd.DataFrame(
        columns=[
            "site_id",
            "sector",
            "cell_name",
            "MV_Freq_Band",
            "MV_Freq_Bandwidth",
            "MV_eCell_Data_BH",
            "MV_Radio_NW_Availability",
            # 'MV_4G_Data_Volume_GB',
            # 'Dl_Throughput_mbps',
            # 'MV_E_UTRAN_Average_CQI',
            "remark",
        ]
    )
    removed_nokia_NE_ik_nospace_sams_df = removed_nokia_NE_ik_nospace_sams_df[:2000]
    # Iterate over each site_id
    for site_id in removed_nokia_NE_ik_nospace_sams_df["site_id"].unique():
        site_data = removed_nokia_NE_ik_nospace_sams_df[
            removed_nokia_NE_ik_nospace_sams_df["site_id"] == site_id
        ]

        # Iterate over each sector within the site
        for sector in site_data["sector"].unique():
            sector_data = site_data[site_data["sector"] == sector]

            # Iterate over each MV_Freq_Band within the sector
            for freq_band in sector_data["MV_Freq_Band"].unique():
                freq_band_data = sector_data[sector_data["MV_Freq_Band"] == freq_band]
                # Check the MV_DL_User_Throughput_Kbps values
                for index, row in freq_band_data.iterrows():
                    if cell_t_f_dict.get(row["Short_name"]) or (
                        row["MV_Freq_Band"] == 900 or row["MV_Freq_Band"] == 850
                    ):
                        remark = "ok"
                    else:
                        remark = "not ok"

                    # Append the result to the results DataFrame
                    results_df = pd.concat(
                        [
                            results_df,
                            pd.DataFrame(
                                [
                                    {
                                        "site_id": site_id,
                                        "sector": sector,
                                        "cell_name": row["Short_name"],
                                        "MV_Freq_Band": row["MV_Freq_Band"],
                                        "MV_Freq_Bandwidth": row["MV_Freq_Bandwidth"],
                                        "MV_eCell_Data_BH": row["MV_eCell_Data_BH"],
                                        "MV_Radio_NW_Availability": row[
                                            "MV_Radio_NW_Availability"
                                        ],
                                        # 'MV_4G_Data_Volume_GB': row['MV_4G_Data_Volume_GB'],
                                        # 'Dl_Throughput_mbps': row['MV_DL_User_Throughput_mbps'],
                                        # 'MV_E_UTRAN_Average_CQI':row['MV_E_UTRAN_Average_CQI'],
                                        "remark": remark,
                                    }
                                ]
                            ),
                        ],
                        ignore_index=True,
                    )

    thpt_5data_for_merge = thpt_5day_data_df[
        [
            "Short_name",
            "date_4_val_thpt",
            "date_5_val_thpt",
            "date_6_val_thpt",
            "date_7_val_thpt",
            "date_8_val_thpt",
            "worst_thpt",
        ]
    ]
    results_df = pd.merge(
        results_df,
        thpt_5data_for_merge,
        left_on="cell_name",
        right_on="Short_name",
        how="left",
    )
    results_df = results_df[
        [
            "site_id",
            "sector",
            "cell_name",
            "MV_Freq_Band",
            "MV_eCell_Data_BH",
            "MV_Freq_Bandwidth",
            "MV_Radio_NW_Availability",
            "date_4_val_thpt",
            "date_5_val_thpt",
            "date_6_val_thpt",
            "date_7_val_thpt",
            "date_8_val_thpt",
            "worst_thpt",
            "remark",
        ]
    ]

    results_df["MV_Freq_Bandwidth"] = (
        results_df["MV_Freq_Bandwidth"].str.rstrip("MHz").str.strip()
    )
    results_df["MV_Freq_Band"] = results_df["MV_Freq_Band"].astype(int)

    #### processing the MV_Average_number_of_used_DL_PRBs kpi analysis

    data = {"date": collable_date, "kpi_name": "MV_Average_number_of_used_DL_PRBs"}
    prb_day_data_df = process_MV_Average_number_of_used_DL_PRBs(api_url, data)
    results_df = pd.merge(
        results_df,
        prb_day_data_df[
            [
                "Short_name",
                "max_prb_among _5_day",
                "week_1_val_prb",
                "week_2_val_prb",
                "date_4_val_prb",
                "date_5_val_prb",
                "date_6_val_prb",
                "date_7_val_prb",
                "date_8_val_prb",
            ]
        ],
        left_on="cell_name",
        right_on="Short_name",
        how="left",
    )

    #### processing the UL_RSSI kpi analysis

    data = {"date": collable_date, "kpi_name": "UL_RSSI"}
    ul_rssi_day_data_df = process_ul_rssi(api_url, data)
    results_df = pd.merge(
        results_df,
        ul_rssi_day_data_df[
            [
                "Short_name",
                "week_1_val_rssi",
                "week_2_val_rssi",
                "date_4_val_rssi",
                "date_5_val_rssi",
                "date_6_val_rssi",
                "date_7_val_rssi",
                "date_8_val_rssi",
            ]
        ],
        left_on="cell_name",
        right_on="Short_name",
        how="left",
    )

    #### processing the MV_Radio_NW_Availability kpi analysis

    data = {"date": collable_date, "kpi_name": "MV_Radio_NW_Availability"}
    rna_5day_data_df = process_MV_Radio_NW_Availability(api_url, data)
    results_df = pd.merge(
        results_df,
        rna_5day_data_df[
            [
                "Short_name",
                "week_1_val_rna",
                "week_2_val_rna",
                "date_4_val_rna",
                "date_5_val_rna",
                "date_6_val_rna",
                "date_7_val_rna",
                "date_8_val_rna",
            ]
        ],
        left_on="cell_name",
        right_on="Short_name",
        how="left",
    )

    results_df["rna_on_worst_thpt_date"] = results_df.apply(
        lambda row: row[row["worst_thpt"] + "_rna"], axis=1
    )

    #### processing the MV_E_UTRAN_Average_CQI kpi analysis
    data = {"date": collable_date, "kpi_name": "MV_E_UTRAN_Average_CQI"}
    cqi_day_data_df = process_MV_E_UTRAN_Average_CQI(api_url, data)

    results_df.drop("Short_name", inplace=True, axis=1)
    results_df = pd.merge(
        results_df,
        cqi_day_data_df,
        left_on="cell_name",
        right_on="Short_name",
        how="left",
    )

    results_df["worst_thpt"] = results_df[
        [
            "date_4_val_thpt",
            "date_5_val_thpt",
            "date_6_val_thpt",
            "date_7_val_thpt",
            "date_8_val_thpt",
        ]
    ].idxmin(axis=1)

    date_obj = datetime.strptime(collable_date, "%Y-%m-%d").date()

    # Generate the list of dates (descending order from greatest to oldest)
    date_list = [date_obj - timedelta(days=i) for i in range(4, -1, -1)]

    # Convert the date objects to string format for column names
    date_columns = [d.strftime("%Y-%m-%d") for d in date_list]

    # Rename the DataFrame columns

    column_mapping = {
        "date_4_val_thpt": date_columns[0],
        "date_5_val_thpt": date_columns[1],
        "date_6_val_thpt": date_columns[2],
        "date_7_val_thpt": date_columns[3],
        "date_8_val_thpt": date_columns[4],
    }

    results_df["worst_thpt_original_date"] = results_df["worst_thpt"].apply(
        lambda x: column_mapping[x]
    )
    results_df["worst_thpt_original_date"] = pd.to_datetime(
        results_df["worst_thpt_original_date"]
    )
    results_df["worst_thpt_original_date"] = results_df[
        "worst_thpt_original_date"
    ].dt.date

    date_obj = datetime.strptime(collable_date, "%Y-%m-%d").date()

    # Generate the list of dates (descending order from greatest to oldest)
    date_list = [date_obj - timedelta(days=i) for i in range(4, -1, -1)]
    # Convert the date objects to string format for column names
    date_columns = [d.strftime("%Y-%m-%d") for d in date_list]
    print(date_columns)

    api_url = f"http://103.242.225.195:8000/RCA_TOOL/filter_tantitive_data_postgres/"
    data = {
        "dates": date_columns,
        "columns": [
            "LEPSB_ERAB_INI_SETUP_FAIL_RNL_RIP",
            "TNL_Failure_Percent",
            "RSRP_Samples_lt_116_dBm",
        ],
    }

    tentative_counter_df = process_tentative_counter_df(
        api_url, data, tentative_counter_df
    )
    results_df.drop("Short_name", inplace=True, axis=1)
    results_df = results_df.merge(
        tentative_counter_df,
        left_on=["cell_name", "worst_thpt_original_date", "MV_eCell_Data_BH"],
        right_on=["Short_name", "Date", "Time"],
        how="left",
    )

    # checking for >5 mb on other sector and
    results_df["RCA"] = ""
    results_df["Solution"] = ""
    for index, row in results_df.iterrows():
        if row["remark"] == "not ok":
            site = row["site_id"]
            sector = row["sector"]
            worst_thpt = row["worst_thpt"]
            throughput_check = results_df[
                (results_df["site_id"] == site)
                & (results_df["sector"] == sector)
                & (results_df["cell_name"] != row["cell_name"])
                & (results_df[worst_thpt] > 5)
                & (~results_df["MV_Freq_Band"].isin([900, 850]))
            ]
            if not throughput_check.empty:
                results_df.loc[index, ["RCA", "Solution"]] = [
                    ">5 mbps on other layer within the same sector",
                    "Load Balancing required",
                ]
            worst_thpt_cqi = worst_thpt.rstrip("_thpt") + "_CQI"
            # print(worst_thpt_cqi)
            if row[worst_thpt_cqi] < 7.5:
                results_df.loc[index, "RCA"] = (
                    str(results_df.loc[index, "RCA"]) + ",CQI Poor"
                )
                results_df.loc[index, "Solution"] = (
                    str(results_df.loc[index, "Solution"])
                    + ",Optimization for Cqi improvement"
                )

            #     equiped_payload_check_df= results_df[(results_df['site_id'] == site) &  (results_df['sector'] == sector)]
            #     if (equiped_payload_check_df['equipped_payload'] < equiped_payload_check_df['MV_4G_Data_Volume_GB'] ).all():
            #          results_df.loc[index, 'RCA']= str(results_df.loc[index, 'RCA']) + ', All cell are taking payload greater than equiped payload'
            #          results_df.loc[index, 'Solution'] = str(results_df.loc[index, 'Solution']) + ', Capacity addition required'

            # logic for prb....
            prb_day_data_series = prb_day_data_df[
                prb_day_data_df["Short_name"] == row["cell_name"]
            ].iloc[0]

            rna_check_on_not_ok_cell_on_wrst_thpr_df = results_df[
                (results_df["site_id"] == site)
                & (results_df["sector"] == sector)
                & (results_df["cell_name"] != row["cell_name"])
                & (~results_df["MV_Freq_Band"].isin([900, 850]))
            ][[worst_thpt.rstrip("_thpt") + "_rna"]]
            rna_check_on_not_ok_cell_on_wrst_thpr_df = (
                rna_check_on_not_ok_cell_on_wrst_thpr_df[
                    rna_check_on_not_ok_cell_on_wrst_thpr_df[
                        worst_thpt.rstrip("_thpt") + "_rna"
                    ]
                    < 80
                ]
            )

            if prb_day_data_series["max_prb_among _5_day"] > 75:
                results_df.loc[index, "RCA"] = (
                    str(results_df.loc[index, "RCA"]) + ", High PRB Utilization"
                )
                results_df.loc[index, "Solution"] = (
                    str(results_df.loc[index, "Solution"]) + ", need to set solution."
                )

            if prb_day_data_series["week_1_val_prb"] > 2:

                percentage_change = (
                    prb_day_data_series["max_prb_among _5_day"]
                    - prb_day_data_series["week_1_val_prb"]
                )
                if prb_day_data_series["Short_name"] == "MU_E_F3_OM_1990A_A":
                    print(
                        "max_val: ",
                        prb_day_data_series["max_prb_among _5_day"],
                        "pre week val: ",
                        prb_day_data_series["week_1_val_prb"],
                    )
                    print(percentage_change)
                if (
                    prb_day_data_series["max_prb_among _5_day"] > 75
                    and percentage_change > 5
                ):
                    if not rna_check_on_not_ok_cell_on_wrst_thpr_df.empty:
                        results_df.loc[index, "RCA"] = (
                            str(results_df.loc[index, "RCA"])
                            + ", payload Prb increased on cell due to RNA issue"
                        )
                        results_df.loc[index, "Solution"] = (
                            str(results_df.loc[index, "Solution"])
                            + ", RNA correction with in sector."
                        )

                    else:
                        results_df.loc[index, "RCA"] = (
                            str(results_df.loc[index, "RCA"])
                            + ", payload Prb increased"
                        )
                        results_df.loc[index, "Solution"] = (
                            str(results_df.loc[index, "Solution"])
                            + ", need to set solution."
                        )

            # logic for rssi.....

            worst_thpt_rssi = thpt_5day_data_df[
                thpt_5day_data_df["Short_name"] == row["cell_name"]
            ]["worst_thpt"].unique()
            worst_thpt_rssi = worst_thpt_rssi[0] + "_rssi"
            # print("rssi:",worst_thpt)
            ul_rssi = ul_rssi_day_data_df[
                ul_rssi_day_data_df["Short_name"] == row["cell_name"]
            ].iloc[0][worst_thpt_rssi]
            # print(ul_rssi)
            if ul_rssi >= -100:
                results_df.loc[index, "RCA"] = (
                    str(results_df.loc[index, "RCA"]) + ", High Rssi"
                )
                results_df.loc[index, "Solution"] = (
                    str(results_df.loc[index, "Solution"])
                    + ", HW troubleshooting or Interfernce improvement."
                )
            # logic for LEPSB.ERAB_INI_SETUP_FAIL_RNL_RIP.....
            if row["LEPSB_ERAB_INI_SETUP_FAIL_RNL_RIP"] > 50:
                results_df.loc[index, "RCA"] = (
                    str(results_df.loc[index, "RCA"]) + ", RNL fail high"
                )
                results_df.loc[index, "Solution"] = (
                    str(results_df.loc[index, "Solution"])
                    + ", Coverage/ cell overlapping  improvement."
                )
            if row["TNL_Failure_Percent"] > 5:
                results_df.loc[index, "RCA"] = (
                    str(results_df.loc[index, "RCA"]) + ", TNL fails high"
                )
                results_df.loc[index, "Solution"] = (
                    str(results_df.loc[index, "Solution"]) + ", need to set solution."
                )
            if row["RSRP_Samples_lt_116_dBm"] > 15:
                results_df.loc[index, "RCA"] = (
                    str(results_df.loc[index, "RCA"])
                    + ", Sample coming from poor coverage"
                )
                results_df.loc[index, "Solution"] = (
                    str(results_df.loc[index, "Solution"]) + ", need to set solution."
                )

            # logic for >5 mb not available on other layers with in the same sector and PRB >70 for all the layers within the sector.....
            no_gt_5mb_thpt_on_other_layers_check = results_df[
                (results_df["site_id"] == site)
                & (results_df["sector"] == sector)
                & (results_df["cell_name"] != row["cell_name"])
                & (results_df[worst_thpt] > 5)
                & (~results_df["MV_Freq_Band"].isin([900, 850]))
            ]
            prb_gt_70_on_other_layers_on_wrst_thpt_check = results_df[
                (results_df["site_id"] == site)
                & (results_df["sector"] == sector)
                & (~results_df["MV_Freq_Band"].isin([900, 850]))
            ]

            if (
                no_gt_5mb_thpt_on_other_layers_check.empty
                and (
                    prb_gt_70_on_other_layers_on_wrst_thpt_check[
                        worst_thpt.rstrip("_thpt") + "_prb"
                    ]
                    > 70
                ).all()
            ):
                results_df.loc[index, "RCA"] = (
                    str(results_df.loc[index, "RCA"]) + ", High utilization"
                )
                results_df.loc[index, "Solution"] = (
                    str(results_df.loc[index, "Solution"])
                    + ", Capacity addition required."
                )

    new_columns = [
        "site_id",
        "sector",
        "cell_name",
        "oem",
        "MV_Freq_Band",
        "MV_Freq_Bandwidth",
        "date_4_val_thpt",
        "date_5_val_thpt",
        "date_6_val_thpt",
        "date_7_val_thpt",
        "date_8_val_thpt",
        "week_1_val_rssi",
        "week_2_val_rssi",
        "date_4_val_rssi",
        "date_5_val_rssi",
        "date_6_val_rssi",
        "date_7_val_rssi",
        "date_8_val_rssi",
        "week_1_val_CQI",
        "week_2_val_CQI",
        "date_4_val_CQI",
        "date_5_val_CQI",
        "date_6_val_CQI",
        "date_7_val_CQI",
        "date_8_val_CQI",
        "week_1_val_rna",
        "week_2_val_rna",
        "date_4_val_rna",
        "date_5_val_rna",
        "date_6_val_rna",
        "date_7_val_rna",
        "date_8_val_rna",
        "week_1_val_prb",
        "week_2_val_prb",
        "date_4_val_prb",
        "date_5_val_prb",
        "date_6_val_prb",
        "date_7_val_prb",
        "date_8_val_prb",
        "rna_on_worst_thpt_date",
        "max_prb_among _5_day",
        "LEPSB_ERAB_INI_SETUP_FAIL_RNL_RIP",
        "TNL_Failure_Percent",
        "RSRP_Samples_lt_116_dBm",
        "remark",
        "RCA",
        "Solution",
    ]
    results_df = results_df[new_columns]

    results_df.rename(
        columns={"cell_name": "Short_name", "oem": "OEM_GGSN"}, inplace=True
    )

    rca_report = []
    for i, cell_record in results_df.iterrows():
        kpi = KPI_row["KPI"]
        cell_value = cell_record[""]
        if cell_record["remark"] == "ok":
            #  print(KPI_row.operator)
            #  print("cell_value; ",cell_record[kpi]," threshold_value: ",KPI_row.threshold_value)
            #  print("true")
            rca_report.append(
                {
                    "Cell_name": cell_record["Short_name"],
                    "OEM_GGSN": cell_record["OEM_GGSN"],
                    "KPI": kpi,
                    "cell_value": "",
                    "threshold_value": KPI_row.threshold_value,
                    "check": "OK",
                    "RCA": "",
                    "Proposed Solution": "",
                    "history_alarms": "",
                }
            )
        else:
            rca_report.append(
                {
                    "Cell_name": cell_record["Short_name"],
                    "OEM_GGSN": cell_record["OEM_GGSN"],
                    "KPI": kpi,
                    "cell_value": "",
                    "threshold_value": KPI_row.threshold_value,
                    "check": "NOT OK",
                    "RCA": cell_record["RCA"],
                    "Proposed Solution": cell_record["Solution"],
                    "history_alarms": "",
                }
            )

    return rca_report


def mark_rows_vectorized(df):
    specified_columns = [
        "Short_name",
        "Date",
        "OEM_GGSN",
        "ECGI_4G",
        "MV_Site_Name",
        "MV_Freq_Band",
        "MV_Freq_Bandwidth",
    ]

    complete_empty_mask = (
        df[specified_columns].isnull()
        | (df[specified_columns] == 0)
        | (df[specified_columns] == "")
    )
    complete_empty_mask = complete_empty_mask.all(axis=1)
    non_specified_columns = df.columns.difference(specified_columns)
    partial_empty_mask = (
        df[non_specified_columns].isnull()
        | (df[non_specified_columns] == 0)
        | (df[non_specified_columns] == "")
    )
    partial_empty_mask = partial_empty_mask.all(axis=1)

    df["mark_value"] = "non_empty"

    df.loc[complete_empty_mask, "mark_value"] = "complete_empty"
    df.loc[partial_empty_mask & ~complete_empty_mask, "mark_value"] = "partial"

    return df["mark_value"]


def process_remove_duplicates(data):
    data = data.drop(columns=["id"], axis=1)

    print(data.columns[7:])

    columns_to_convert = data.columns[7:]
    data[columns_to_convert] = data[columns_to_convert].apply(
        pd.to_numeric, errors="coerce"
    )

    data["mark_value"] = mark_rows_vectorized(data)

    # to remove the duplicate cells where we have partial values in the both the duplicate row of a cell
    data = data[
        (data["mark_value"] != "partial") & (data["mark_value"] != "complete_empty")
    ]

    data["null_zero_count"] = data.isnull().sum(axis=1) + (data == 0).sum(axis=1)

    # Sort the DataFrame by 'cell_name' and 'null_zero_count'
    df_sorted = data.sort_values(by=["Short_name", "null_zero_count"])

    # Keep the row with the minimum 'null_zero_count' for each 'cell_name'
    result_df = df_sorted.drop_duplicates(subset=["Short_name"], keep="first")

    # Drop the temporary column if not needed
    result_df = result_df.drop(columns=["null_zero_count"])
    return result_df


@api_view(["GET"])
def main_process(request):
    print("main process started....")
    latest_record_Date_df = Daily_4G_KPI.objects.latest("Date").Date

    filtered_records_df = (
        Daily_4G_KPI.objects.filter(Date=latest_record_Date_df)
        .values()
        .order_by("Short_name")
    )

    KPI_4G_record_df = pd.DataFrame(filtered_records_df)
    # KPI_4G_record_df.to_csv("before_KPI_4G_record_df.csv")
    KPI_4G_record_df = process_remove_duplicates(KPI_4G_record_df)
    # print(KPI_4G_record_df)
    # KPI_4G_record_df.to_csv("after_removing_duplicates_KPI_4G_record_df.csv")

    # KPI_4G_record_df=KPI_4G_record_df[KPI_4G_record_df['Short_name']=='AP_E_F3_OM_HY6852B_B']
    # KPI_4G_record_df=KPI_4G_record_df[:500]
    # KPI_4G_record_df.to_excel("teeeeeeeest.xlsx")
    KPI_4G_record_df["MRBTS_ID"] = KPI_4G_record_df["ECGI_4G"].str.split("-").str[-2]

    KPI_TABLE_df = pd.DataFrame(KPI_TABLE.objects.all().values())

    tentative_counter = Tantitive_Counters_24_Hours.objects.filter(
        DateTime__date=latest_record_Date_df
    ).values()
    tentative_counter_df = pd.DataFrame(tentative_counter)

    tentative_counter_df.fillna(value=0, inplace=True)
    # tentative_counter_df.to_csv("tentative_counter123.csv")

    # previous_date = latest_record_Date_df - timedelta(days=1)
    # next_date = latest_record_Date_df + timedelta(days=1)

    # alarm_data = AlarmNotification.objects.filter(AlarmTime__range = (previous_date,next_date)).values()
    alarm_data = AlarmNotification.objects.filter(
        Upload_date=latest_record_Date_df
    ).values()
    alarm_data_df = pd.DataFrame(alarm_data)

    alarm_data_df["MRBTS_ID"] = alarm_data_df["DistinguishedName"].str[16:22]
    alarm_data_df["MRBTS_ID"] = alarm_data_df["MRBTS_ID"].astype(str)
    # alarm_data_df.to_csv("alarm_data.csv")
    # alarm_data_df.to_csv("alarm_data.csv")
    # exit(0)
    rca_report = []
    for _, KPI_row in KPI_TABLE_df.iterrows():
        # Iterate over the filtered recordsl

        if KPI_row["KPI"] in [
            "MV_RRC_Setup_Success_Rate",
            "MV_ERAB_Setup_Success_Rate",
        ]:
            print("Working for kpi:- 'Accessibility' Analysis...")
            #  print('Working for accessibility parameters...')
            access_rca = accessibility_rca(
                KPI_4G_record_df, KPI_row, alarm_data_df, tentative_counter_df
            )
            rca_report = rca_report + access_rca

        elif KPI_row["KPI"] == "MV_4G_Data_Volume_GB":
            print("Working for kpi:- 'MV_4G_Data_Volume_GB' Analysis...")
            #  print('Working for payload parameter...')
            pyld_rca = payload_rca(latest_record_Date_df, alarm_data_df)
            rca_report = rca_report + pyld_rca

        elif KPI_row["KPI"] == "MV_DL_User_Throughput_Kbps":
            print("Working for kpi:- 'MV_DL_User_Throughput_Kbps' Analysis...")
            dl_throupt = throupt_rca(
                KPI_4G_record_df, latest_record_Date_df, tentative_counter_df, KPI_row
            )
            rca_report = rca_report + dl_throupt

    rca_report_df = pd.DataFrame(rca_report)
    df = rca_report_df
    # cell 1
    condition_nokia = df["Cell_name"].str.startswith("@Nokia")
    removed_nokia_df = df[~condition_nokia]
    condition_NE_ik = removed_nokia_df["Cell_name"].str.startswith("NE-ik")
    removed_nokia_NE_ik_df = removed_nokia_df[~condition_NE_ik]
    removed_nokia_NE_ik_nospace_df = removed_nokia_NE_ik_df[
        removed_nokia_df["Cell_name"].str.contains("_")
        | removed_nokia_df["Cell_name"].str.startswith(",")
    ]

    # Cell 2
    def extract_circle(cell):
        if cell.startswith("Sams-"):
            circle = cell.split(",")[1].split("_")[0]
        else:
            circle = cell.split("_")[0]
        return circle

    removed_nokia_NE_ik_nospace_df["circle"] = removed_nokia_NE_ik_nospace_df[
        "Cell_name"
    ].apply(extract_circle)

    # Cell 3

    removed_nokia_NE_ik_nospace_df = removed_nokia_NE_ik_nospace_df[
        [
            "circle",
            "OEM_GGSN",
            "Cell_name",
            "KPI",
            "cell_value",
            "threshold_value",
            "check",
            "RCA",
            "Proposed Solution",
            "history_alarms",
        ]
    ]

    print("saving to db statred.", datetime.now())
    save_df_to_model(removed_nokia_NE_ik_nospace_df, latest_record_Date_df)
    print("saving to db finished.", datetime.now())
    removed_nokia_NE_ik_nospace_df.to_csv(
        os.path.join(
            MEDIA_ROOT, "RCA_TOOL", "output", f"rca_report_{latest_record_Date_df}.csv"
        ),
        index=False,
    )
    download_path = os.path.join(
        MEDIA_URL, "RCA_TOOL", "output", f"rca_report_{latest_record_Date_df}.csv"
    )

    return Response({"message": "success", "download_link": download_path})


@api_view(["GET"])
def latest_record_data(request):
    latest_4G_KPI_date = Daily_4G_KPI.objects.latest("Date").Date
    latest_tentative_counter_date = Tantitive_Counters_24_Hours.objects.latest(
        "DateTime"
    ).DateTime.date()
    latest_alarm_date = AlarmNotification.objects.latest("Upload_date").Upload_date

    return Response(
        {
            "latest_4G_KPI_date": latest_4G_KPI_date,
            "latest_tentative_counter": latest_tentative_counter_date,
            "latest_alarm_date": latest_alarm_date,
        }
    )


from .serializers import CellDataSerializer

################################## Dashboard API's #######################################


@api_view(["GET", "POST"])
def get_RCA_Table_Output(request):
    print(request.user)
    date_str = request.POST.get("date")
    if date_str:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        print("Date: ", date)
    else:
        date = RCA_output_table.objects.latest("date").date
        print("latest date :", date)
    cell_data = RCA_output_table.objects.filter(date=date)
    serializer = CellDataSerializer(cell_data, many=True)
    return Response({"Data": serializer.data, "date": date})


@api_view(["GET", "POST"])
def rca_payload_list(request):
    if request.method == "GET":
        rca_payload_table = RCA_payload_table.objects.all()
        serializer = RCA_PayloadTableSerializer(rca_payload_table, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = RCA_PayloadTableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def rca_payload_detail(request, pk):
    try:
        rca_payload_table = RCA_payload_table.objects.get(pk=pk)
    except RCA_payload_table.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = RCA_PayloadTableSerializer(rca_payload_table)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = RCA_PayloadTableSerializer(rca_payload_table, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        rca_payload_table.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def get_rca_output_dated(request):
    # Extract parameters from the request
    date_str = request.data.get("date")
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    print(date)
    cell_names = request.data.get("cell_name").split(",")
    print(type(cell_names))  # Expecting a list of cell names
    # print('Cell Name', cell_names)
    if date and cell_names:
        # Filter the RCA_output_table based on date and list of cell_names
        rca_output = RCA_output_table.objects.filter(
            date=date, Cell_name__in=cell_names, KPI="MV_4G_Data_Volume_GB_N"
        )

        if rca_output.exists():
            serializer = CellDataSerializer(rca_output, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "No data found for the provided parameters."},
                status=status.HTTP_404_NOT_FOUND,
            )
    else:
        return Response(
            {"message": "Both 'date' and 'cell_name' parameters are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )


from django.db import connection
import json


@api_view(["POST"])
def rca_dashboard(request):
    print("User: ", request.user.username)
    # date=request.POST.get("date")
    # date=datetime.strptime(date,"%Y-%m-%d").date()
    kpi_name = request.POST.get("kpi_name")
    date = RCA_output_table.objects.latest("date").date
    print(date, kpi_name)

    with connection.cursor() as cursor:

        query = f"""SELECT * FROM public."RCA_TOOL_rca_output_table"
                   where "date" = '{date}' and "KPI" = '{kpi_name}'
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

    rows_as_dict = [
        dict(zip([column[0] for column in cursor.description], row))
        for row in results_as_strings
    ]

    jsonResult = json.dumps(rows_as_dict)
    jsonResult = json.loads(jsonResult)
    # print(jsonResult)
    data = {"table_data": jsonResult}
    return Response(data)


from django.http import JsonResponse
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(["POST"])
def filter_tantitive_data_postgres(request):
    try:
        # Parse the input JSON
        dates = request.data.get("dates", [])
        columns = request.data.get("columns", [])

        if not dates or not columns:
            return JsonResponse(
                {"error": "Both 'dates' and 'columns' are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate columns
        valid_fields = {
            field.name for field in Tantitive_Counters_24_Hours._meta.fields
        }
        invalid_columns = [col for col in columns if col not in valid_fields]

        if invalid_columns:
            return JsonResponse(
                {"error": f"Invalid columns: {', '.join(invalid_columns)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Prepare columns and dates for the query
        selected_columns = ", ".join(
            ['"DateTime"', '"Short_name"'] + [f'"{col}"' for col in columns]
        )
        formatted_dates = ", ".join([f"'{date}'" for date in dates])

        # PostgreSQL query
        query = f"""
            SELECT {selected_columns}
            FROM public."RCA_TOOL_tantitive_counters_24_hours"
            WHERE "DateTime"::DATE IN ({formatted_dates});
        """

        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        # Prepare the response
        column_names = ["DateTime", "Short_name"] + columns
        response_data = [dict(zip(column_names, row)) for row in rows]

        return JsonResponse({"data": response_data}, status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse(
            {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
