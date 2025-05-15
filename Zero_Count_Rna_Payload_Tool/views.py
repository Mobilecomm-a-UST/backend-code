import uuid
from Zero_Count_Rna_Payload_Tool.utils import clean_infinity
from rest_framework.decorators import api_view
from mcom_website.settings import *
from django.conf import settings
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from django.db import transaction
import pandas as pd
import os
from rest_framework import status
from .models import *
import datetime
import json
from .serializers import *
from Zero_Count_Rna_Payload_Tool.utils import *
from django.db.models.functions import ExtractWeek, ExtractYear
import json
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from django.db.models.functions import TruncDate
from rest_framework.pagination import PageNumberPagination
import requests
from mailapp.tasks import send_email
from Zero_Count_Rna_Payload_Tool.send_mail_spoc import send_email_spoc_circle
# from Zero_Count_Rna_Payload_App.pagination import *
from django.db.models import Q
from django.db.models import Avg, F, Value, CharField, DateField
from django.db.models.functions import ExtractDay, Cast, Coalesce, Substr
from django.db.models import Case, When, Value, Func
from datetime import date, timedelta, timezone, datetime
import re
from pandas.tseries.offsets import DateOffset
from commom_utilities.utils import short_name_handler, site_list_handler
from RCA_TOOL.models import *
from rest_framework.exceptions import ValidationError
import logging
from Zero_Count_Rna_Payload_Tool.Zero_count_database_conn import get_data_from_table
from rest_framework import viewsets
class level1View(viewsets.ModelViewSet):
    queryset = level1.objects.all()
    serializer_class = level1Serializer



class level2View(viewsets.ModelViewSet):
    queryset = level2.objects.all()
    serializer_class = level2Serializer



class level3View(viewsets.ModelViewSet):
    queryset = level3.objects.all()
    serializer_class = level3Serializer


class level4View(viewsets.ModelViewSet):
    queryset = level4.objects.all()
    serializer_class = level4Serializer


class ThresholdView(viewsets.ModelViewSet):
     queryset = Threshold.objects.all()
     serializer_class = ThresholdSerializer


logger = logging.getLogger(__name__)
@api_view(["POST"])
def save_database_RAW_4G(request):
    Raw_Kpi_4G = request.FILES["4G"] if "4G" in request.FILES else None
    # #print("raw_kpi_4g",Raw_Kpi_4G)
    if Raw_Kpi_4G:
        location = MEDIA_ROOT + r"\Raw_4G\temporary_files"
        fs = FileSystemStorage(location=location)
        file = fs.save(Raw_Kpi_4G.name, Raw_Kpi_4G)
        # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
        filepath = fs.path(file)
        # print("file_path:-", filepath)
        df = pd.read_excel(
            filepath
        )  # should do something if a csv file is coming from the frontend and the csv file should be deleted from the temp files

        df["Short name"] = df["Short name"].fillna(method="ffill")

        df.rename(columns={"Unnamed: 1": "Date"}, inplace=True)

        df["Cell_Name"] = [
            cell.split("_")[-2] if ("_") in str(cell) else cell
            for cell in df["Short name"]
        ]
        df["Site_ID"] = [
            site.split("_")[-2][:-1] if ("_") in str(site) else site
            for site in df["Short name"]
        ]
        df["Technology"] = [
            tech.split("_")[2] if ("_") in str(tech) else tech
            for tech in df["Short name"]
        ]
        os.remove(path=filepath)
        # print(filepath, "deleted........")
        # print("dfraw", df)

        save_database_KPI_4G(df)
        print("DFFFF", df)
        return Response({"Status": True})


@api_view(["POST"])
def Daily_RAW_KPI_4G(request):
    kpi_4g = request.FILES.get("4G_raw")
    if not kpi_4g:
        return Response({"status": False, "message": "No file provided."}, status=400)

    location = os.path.join(MEDIA_ROOT, "Kpi_Raw_4G", "temporary_files")
    os.makedirs(location, exist_ok=True)

    fs = FileSystemStorage(location=location)
    try:
        file = fs.save(kpi_4g.name, kpi_4g)
        file_path = os.path.join(location, file)
        df = pd.read_csv(file_path)
    except Exception as e:
        return Response({"status": False, "error": str(e)}, status=500)
    try:
        df["Short name"] = df["Short name"].fillna(method="ffill")
        df.rename(columns={"Unnamed: 1": "Date"}, inplace=True)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

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
            # "MV_UL RSSI [dBm/PRB] [CBBH]",
            "UL RSSI",
            # "UL RSSI [CDBH]",
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
            "dlRsBoost",
            "RS Power [dB]",
            "MV_CSFB Redirection Success Rate [CDBH]",
            "VoLTE Inter-Frequency Handover Success Ratio [CBBH]",
            "VoLTE Intra-LTE Handover Success Ratio [CBBH]",
            "MV_RRC Setup Success Rate_DENOM",
        ]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return Response(
                {
                    "status": False,
                    "error": f"Missing columns: {', '.join(missing_columns)}",
                }
            )
    except Exception as e:
        return Response({"status": False, "error": f"Data preparation error: {str(e)}"})

    present_dates = df["Date"].unique()
    present_dates = pd.to_datetime(present_dates).strftime("%Y-%m-%d").tolist()
    exists = Daily_4G_KPI.objects.filter(Date__in=present_dates).exists()

    if exists:
        return Response(
            {"status": False, "message": "Data for the given dates already exists."}
        )

    kpi = [columns for columns in df.columns if columns != "MV eCell Data BH"]
    kpi = kpi[4:]

    df[kpi] = df[kpi].apply(lambda x: x.apply(clean_infinity))

    objects_to_create = []
    try:
        for _, row in df.iterrows():
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
                    MV_DL_User_Throughput_Kbps=row["MV_DL User Throughput_Kbps [CDBH]"],
                    MV_E_UTRAN_Average_CQI=row["MV_E-UTRAN Average CQI [CDBH]"],
                    UL_RSSI=row["UL RSSI"],
                    # MV_UL_RSSI_dBm_PRB=row["MV_UL RSSI [dBm/PRB] [CBBH]"],
                    MV_UL_RSSI_dBm_PRB=row["UL RSSI PUCCH [CDBH]"],
                    # MV_UL_RSSI_dBm_PRB=row["UL RSSI [CDBH]"],
                    MV_Average_number_of_used_DL_PRBs=row[
                        "MV_Average number of used DL PRBs [CDBH]"
                    ],
                    MV_RRC_Setup_Success_Rate=row["MV_RRC Setup Success Rate [CDBH]"],
                    MV_ERAB_Setup_Success_Rate=row["MV_ERAB Setup Success Rate [CDBH]"],
                    MV_PS_Drop_Call_Rate=row["MV_PS Drop Call Rate % [CDBH]"],
                    MV_UL_User_Throughput_Kbps=row["MV_UL User Throughput_Kbps [CDBH]"],
                    MV_Max_Connecteda_User=row["MV_Max Connected User"],
                    MV_PUCCH_SINR=row["MV_PUSCH SINR [CBBH]"],
                    MV_Average_UE_Distance_KM=row["MV_Average UE Distance KM [CDBH]"],
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
                    dlRsBoost=row["dlRsBoost"],
                    RS_Power_dB=row["RS Power [dB]"],
                    UL_RSSI_Nokia_RSSI_SINR=row["UL RSSI_Nokia[RSSI-SINR]"],
                    MV_CSFB_Redirection_Success_Rate = row["MV_CSFB Redirection Success Rate [CDBH]"],
                    VoLTE_Inter_Frequency_Handover_Success_Ratio = row["VoLTE Inter-Frequency Handover Success Ratio [CBBH]"],
                    VoLTE_Intra_LTE_Handover_Success_Ratio = row["VoLTE Intra-LTE Handover Success Ratio [CBBH]"],
                    MV_RRC_Setup_Success_Rate_DENOM = row["MV_RRC Setup Success Rate_DENOM"]
                )
                objects_to_create.append(obj)
    except Exception as e:
        return Response({"status": False, "error": f"Object creation error: {str(e)}"})

    try:
        with transaction.atomic():
            Daily_4G_KPI.objects.bulk_create(objects_to_create)
        os.remove(file_path)
        return Response({"status": True, "message": "Data successfully saved."})
    except Exception as e:
        return Response(
            {
                "status": False,
                "error": f"{str(e)} {row['Short name']}{row}",
            }
        )


@api_view(["POST"])
def template_links(request):
    Location_4G = MEDIA_ROOT + r"\zero_count_rna_payload\template\4G_template"
    Location_2G = MEDIA_ROOT + r"\zero_count_rna_payload\template\2G_template"

    data = {"raw_4g": Location_4G, "raw_2g": Location_2G}
    return Response({"status": True, "data": data})


@api_view(["POST"])
def ms1_site_deletion(request):
    response, cell_list = short_name_handler(request)

    cell_list = [cell.strip() for cell in cell_list]

    cell_series = pd.Series(cell_list)

    cell_list = list(
        cell_series.apply(lambda x: x.replace("*", ",") if ("Sams" in x) else x)
    )

    print(cell_list)

    try:
        with transaction.atomic():
            rows_to_move = Daily_4G_KPI.objects.filter(Short_name__in=cell_list)
            print(rows_to_move)

            archived_rows = []
            for row in rows_to_move:
                row_data = {
                    "Short_name": row.Short_name,
                    "Date": row.Date,
                    "ECGI_4G": row.ECGI_4G,
                    "MV_Site_Name": row.MV_Site_Name,
                    "OEM_GGSN": row.OEM_GGSN,
                    "MV_Freq_Band": row.MV_Freq_Band,
                    "MV_Freq_Bandwidth": row.MV_Freq_Bandwidth,
                }

                archived_rows.append(MS1_SITE_DONE(**row_data))

            MS1_SITE_DONE.objects.bulk_create(archived_rows)

            Daily_4G_KPI.objects.filter(Short_name__in=cell_list).delete()

        return Response(
            {
                "status": True,
                "message": "Data successfully archived and deleted from the original table.",
            }
        )
    except Exception as e:
        return Response({"status": False, "message": f"An error occurred: {str(e)}"})


@api_view(["POST"])
def Daily_RAW_KPI_2G(request):
    kpi_2g = request.FILES["2G_raw"] if "2G_raw" in request.FILES else None
    if kpi_2g:
        location = MEDIA_ROOT + r"\Kpi_Raw_2G\temporary_files"
        fs = FileSystemStorage(location=location)
        file = fs.save(kpi_2g.name, kpi_2g)
        # print("file", file)
        filepath = os.path.join(location, file)
        # filepath=fs.save(file)
        df_2G = pd.read_excel(filepath)
        df_2G["Short name"] = df_2G["Short name"].fillna(method="ffill")
        # print(df_2G)
        database_Save_Raw_2G(df_2G)
        return Response({"Status": True})


def drop_rows(df):
    return df[df["Circle"] != df["Short_name"]]


def replace_blank_with_zero(df, columns_slice):
    df.loc[:, columns_slice] = df.loc[:, columns_slice].replace("", 0)
    return df


@api_view(["GET"])
def kpi_trend_2g_api(request):
    obj = Daily_2G_KPI.objects.all()

    current_date = datetime.datetime.now().date()

    # Get the ISO week number for the current date
    current_week = current_date.isocalendar()[1]

    annual_weeks = (
        obj.annotate(week=ExtractWeek("Date"), year=ExtractYear("Date"))
        .values("week", "year")
        .distinct()
    )

    week_numbers = [week_info["week"] for week_info in annual_weeks]

    dfs = []
    for week in week_numbers:

        # Filter the queryset for the current week
        filtered_obj = obj.filter(Date__week=week)
        obj_values = filtered_obj.values(
            "Short_name",
            "Date",
            "OEM_GGSN",
            "MV_Total_Voice_Traffic_BBH",
            "Network_availability_RNA",
            "MV_of_2G_Cell_with_Network_Availability",
        )
        df = pd.DataFrame(list(obj_values))

        dfs.append(df)
    result_df = pd.concat(dfs, ignore_index=True)
    print(result_df)
    dates_list = list(result_df["Date"].unique())

    date_format = [date.strftime("%Y-%m-%d") for date in dates_list]
    date_format_2 = [date.strftime("%Y_%m_%d") for date in dates_list]
    print(date_format_2)

    print(date_format)

    week1_data = pd.DataFrame(dfs[0])

    week2_data = pd.DataFrame(dfs[1])

    kpi = [
        "MV_Total_Voice_Traffic_BBH",
        "Network_availability_RNA",
        "MV_of_2G_Cell_with_Network_Availability",
    ]

    for col in kpi:
        result_df[col] = result_df[col].astype(float)

    pivot_table = result_df.pivot_table(
        values=kpi,
        index=["Short_name", "OEM_GGSN"],
        columns="Date",
        aggfunc="mean",
        dropna=True,
    )

    # Convert columns to float
    for col in kpi:
        week1_data[col] = week1_data[col].astype(float)
        week2_data[col] = week2_data[col].astype(float)

    # Pivot tables for each week
    weeks1 = week1_data.pivot_table(
        values=kpi,
        columns="Date",
        index=["Short_name", "OEM_GGSN"],
        aggfunc="mean",
        dropna=False,
    )
    print("weeks1:", weeks1)
    weeks2 = week2_data.pivot_table(
        values=kpi,
        columns="Date",
        index=["Short_name", "OEM_GGSN"],
        aggfunc="mean",
        dropna=False,
    )
    # Modify the pivot_table DataFrame based on conditions
    week11 = {}

    week22 = {}

    for i, col in enumerate(kpi):
        if col in weeks1.columns:
            week11[f"{col}"] = weeks1[col].mean(axis=1)

        if col in weeks2.columns:
            week22[f"{col}"] = weeks2[col].mean(axis=1)

    n1 = pd.DataFrame(week11)

    n1.columns = pd.MultiIndex.from_tuples(
        [
            ("MV_Total_Voice_Traffic_BBH", "week-1"),
            ("Network_availability_RNA", "week-1"),
            ("MV_of_2G_Cell_with_Network_Availability", "week-1"),
        ]
    )
    n2 = pd.DataFrame(week22)
    n2.columns = pd.MultiIndex.from_tuples(
        [
            ("MV_Total_Voice_Traffic_BBH", "week-2"),
            ("Network_availability_RNA", "week-2"),
            ("MV_of_2G_Cell_with_Network_Availability", "week-2"),
        ]
    )
    dfs = []
    for cell in kpi:
        if cell in n1.columns and cell in n2.columns:
            merged_df = pd.merge(
                n2[[cell]], n1[[cell]], left_index=True, right_index=True
            )
            dfs.append(merged_df)
    merge_df = pd.concat(dfs, axis=1)
    print(merge_df)
    pivot_table = pd.DataFrame(pivot_table)

    dfs1 = []
    for cell in kpi:
        if cell in merge_df.columns and cell in pivot_table.columns:
            result_df = pd.merge(
                merge_df[[cell]], pivot_table[[cell]], left_index=True, right_index=True
            )
            dfs1.append(result_df)
    result_df = pd.concat(dfs1, axis=1)
    print(result_df)
    result_df.to_excel("result12.xlsx")
    result_df2 = pd.read_excel("result12.xlsx")

    for i, value in enumerate(result_df2.columns):
        if value == "Unnamed: 0":
            result_df2 = result_df2.rename(columns={"Unnamed: 0": "Short_name"})
        elif value == "Unnamed: 1":
            result_df2 = result_df2.rename(columns={"Unnamed: 1": "OEM_GGSN"})
        # elif value == "Unnamed: 2":
        #     result_df2 = result_df2.rename(columns={"Unnamed: 2": "MV_Freq_Band"})
        elif value in [f"Unnamed: {i}" for i in range(2, 9)]:
            result_df2 = result_df2.rename(
                columns={value: "MV_Total_Voice_Traffic_BBH"}
            )
        elif value in [f"Unnamed: {i}" for i in range(10, 17)]:
            result_df2 = result_df2.rename(columns={value: "Network_availability_RNA"})
        elif value in [f"Unnamed: {i}" for i in range(17, 24)]:
            result_df2 = result_df2.rename(
                columns={value: "MV_of_2G_Cell_with_Network_Availability"}
            )

    result_df2.columns = result_df2.columns + " " + result_df2.iloc[0].astype(str)

    result_df2 = result_df2.drop([0, 1])

    result_df2 = pd.DataFrame(result_df2)

    result_df2.to_excel("result_df2.xlsx")
    for i, value in enumerate(result_df2.columns):
        val_str = " "
        if val_str in value:
            result_df2.columns = result_df2.columns.str.replace(val_str, "_")
        if "00:00:00" in value:
            result_df2.columns = result_df2.columns.str.replace("00:00:00", "")
        if "-" in value:
            result_df2.columns = result_df2.columns.str.replace("-", "_")
    result_df2.columns = result_df2.columns.str.strip("_")

    x = 0
    for i, value in enumerate(result_df2.columns):
        if x < len(date_format_2) and (date_format_2[x] in value):
            result_df2.columns = result_df2.columns.str.replace(
                date_format_2[x], f"date_{x+1}"
            )
            x += 1

    json_data = result_df2.to_json(orient="records")

    new_json = json.loads(json_data)

    return Response(
        {
            "Status": True,
            "message": "successfully submitted.....",
            "dates_data": date_format,
            "data": new_json,
        }
    )


def cleaned_data(df):
    condition_nokia = df["Short_name"].str.startswith("@Nokia")
    print(condition_nokia)
    removed_nokia_df = df[~condition_nokia]

    condition_NE_ik = removed_nokia_df["Short_name"].str.startswith("NE-ik")
    removed_nokia_NE_ik_df = removed_nokia_df[~condition_NE_ik]

    removed_nokia_NE_ik_nospace_df = removed_nokia_NE_ik_df[
        removed_nokia_df["Short_name"].str.contains("_")
        | removed_nokia_df["Short_name"].str.startswith(",")
    ]
    removed_nokia_NE_ik_nospace_df.shape

    return df
  

def get_circle(short_name):
    if "NE-ik" in short_name:
        if not "Sams-" in short_name:
            return short_name.split("-")[4]
        else:
            return short_name.split(",")[1][0:2]
    elif "Sams" in short_name:
        return short_name.split(",")[1][0:2]
    elif "@Nokia" in short_name:
        parts = re.split(r"(\d+)", short_name.split("-")[1])
        return parts[0] if len(parts) > 0 else None
    elif short_name.startswith("LD") or short_name.startswith("LU"):
        return "DL"
    else:
        return short_name.split("_")[0]


def get_last_five_days_of_week(df):
    print(df)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Week_Number"] = df["Date"].dt.isocalendar().week
    df["Day_of_Week"] = df["Date"].dt.dayofweek

    filtered_df = df[df["Day_of_Week"] < 7]

    filtered_df = filtered_df.drop(["Week_Number", "Day_of_Week"], axis=1)

    return filtered_df


def get_last_five_days_of_week_current_week(df):
    df["Date"] = pd.to_datetime(df["Date"])
    df["Week_Number"] = df["Date"].dt.isocalendar().week
    df["Day_of_Week"] = df["Date"].dt.dayofweek

    # Calculate the maximum day number in the week (Monday=0, Sunday=6)
    max_day_number = df["Day_of_Week"].max()

    # Calculate the starting day number for the last five days (Wednesday=2)
    start_day_number = max(
        0, max_day_number - 4
    )  # Ensure start_day_number is at least 0

    # If the start_day_number is less than 2 (Wednesday), consider days from the previous week
    if start_day_number < 2:
        prev_week_max_day_number = start_day_number - 1
        prev_week_data = df[
            (df["Week_Number"] == df["Week_Number"].max() - 1)
            & (df["Day_of_Week"] >= 2)
        ]
        filtered_df = pd.concat(
            [prev_week_data, df[df["Day_of_Week"] >= start_day_number]]
        )
    else:
        # Filter the DataFrame for the last five days of the week
        filtered_df = df[(df["Day_of_Week"] >= start_day_number)]

    # Drop temporary columns
    filtered_df = filtered_df.drop(["Week_Number", "Day_of_Week"], axis=1)

    return filtered_df


def latest_date_to_past_7_days(objs):
    # latest_date = objs.aggregate(latest_date=Max("Date"))
    latest_date = objs['Date'].max()
    latest_date = latest_date
    # latest_date = latest_date["latest_date"]
    print(latest_date)
    d1 = latest_date
    d2 = latest_date - timedelta(1)
    d3 = latest_date - timedelta(2)
    d4 = latest_date - timedelta(3)
    d5 = latest_date - timedelta(4)
    d6 = latest_date - timedelta(5)
    d7 = latest_date - timedelta(6)
    d8 = latest_date - timedelta(7)

    date_list = [d1, d2, d3, d4, d5, d6, d7, d8]

    return date_list


def latest_date_to_past_4_days(objs):
    latest_date = objs.aggregate(latest_date=Max("Date"))
    latest_date = latest_date["latest_date"]
    d1 = latest_date
    d2 = latest_date - timedelta(1)
    d3 = latest_date - timedelta(2)
    d4 = latest_date - timedelta(3)
    d5 = latest_date - timedelta(4)

    date_list = [d1, d2, d3, d4, d5]

    return date_list


def rename_columns_master(cols):
    new_columns = []
    date_counters = {}

    for col in cols:
        if "week-" in col:
            col = col.replace("-", "_")
            new_columns.append(col)
        elif any(char.isdigit() for char in col):
            val = col.split("_")[-1]
            col_base = col.split(f"_{val}")[0]
            if col_base not in date_counters:
                date_counters[col_base] = 1
            new_col = f"{col_base}_date_{date_counters[col_base]}"
            date_counters[col_base] += 1
            if date_counters[col_base] > 5:
                date_counters[col_base] = 1
            new_columns.append(new_col)
        else:
            new_columns.append(col)

    return new_columns


@api_view(["GET"])
def Master_Dashboard_api(request):
    objs = Daily_4G_KPI.objects.all().values()

    current_date = datetime.now().date()

    current_week = current_date.isocalendar()[1]

    date_list = latest_date_to_past_4_days(objs)

    filtered_obj = objs.filter(Date__in=date_list)

    current_df = pd.DataFrame(filtered_obj)

    current_df = cleaned_data(current_df)

    current_df = current_df.replace("nan", 0)

    filtered_df = process_remove_duplicates(current_df)

    current_df = filtered_df

    kpi = [
        "MV_4G_Data_Volume_GB",
        "MV_Radio_NW_Availability",
        "MV_VoLTE_raffic",
        "MV_DL_User_Throughput_Kbps",
        "MV_E_UTRAN_Average_CQI",
        "UL_RSSI",
        "MV_Average_number_of_used_DL_PRBs",
        "MV_RRC_Setup_Success_Rate",
        "MV_ERAB_Setup_Success_Rate",
        "MV_PS_Drop_Call_Rate",
        "MV_Max_Connecteda_User",
        "MV_PUCCH_SINR",
        "MV_Average_UE_Distance_KM",
        "MV_PS_handover_success_rate_LTE_INTER_SYSTEM",
        "MV_PS_handover_success_rate_LTE_INTRA_SYSTEM",
        "UL_RSSI_Nokia_RSSI_SINR",
        "MV_VoLTE_DCR",
        "MV_Packet_Loss_DL",
        "MV_Packet_Loss_UL",
        "PS_InterF_HOSR",
        "PS_IntraF_HOSR",
    ]

    current_dates = current_df["Date"].unique()

    date_list = pd.to_datetime(current_dates)
    date_format = sorted([date.strftime("%Y-%m-%d") for date in date_list])
    print(date_format)
    date_format_2 = sorted([date.strftime("%Y_%m_%d") for date in date_list])
    current_df.fillna(value=0, inplace=True)
    for col in kpi:
        current_df[col] = current_df[col].astype(float)

    current_pivot_df = current_df.pivot_table(
        values=kpi,
        index=["Short_name", "OEM_GGSN", "MV_Freq_Band"],
        columns="Date",
        aggfunc="mean",
        dropna=True,
    )
    current_pivot_df.fillna(value=0, inplace=True)
    current_pivot_df.columns = [
        "_".join([str(c) for c in col]).strip()
        for col in current_pivot_df.columns.values
    ]

    current_pivot_df.reset_index(inplace=True)

    result_df = current_pivot_df

    result_df["Circle"] = (
        result_df["Short_name"].apply(lambda x: str(x)).apply(get_circle)
    )
    result_df["Circle"] = result_df["Circle"].apply(
        lambda x: x.strip() if isinstance(x, str) else x
    )
    cols = result_df.columns.tolist()
    cols = [cols[-1]] + cols[:-1]
    result_df = result_df[cols]

    result_df.columns = rename_columns_master(result_df.columns)

    result_df = drop_rows(result_df)

    result = []

    kpi = [
        "MV_4G_Data_Volume_GB",
        "MV_Radio_NW_Availability",
        "MV_VoLTE_raffic",
    ]
    for circle, group in result_df.groupby("Circle"):
        circle_data = {"Circle": circle}
        for i, date in enumerate(sorted(date_format_2), start=1):
            for col in kpi:
                col_name = f"{col}_date_{i}"
                if col_name in group.columns:
                    count = (group[col_name] == 0).sum()
                else:
                    count = 0
                circle_data[f"{col}_date_{i}"] = count
        result.append(circle_data)
    result_data = pd.DataFrame(result)

    result_data.to_excel("master_dashboard.xlsx")

    return Response({"Status": True, "dates": date_format, "result": result})


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
    # data = data.drop(columns=["id"], axis=1)

    print(data.columns[7:])

    columns_to_convert = data.columns[7:]
    data[columns_to_convert] = data[columns_to_convert].apply(
        pd.to_numeric, errors="coerce"
    )

    data["mark_value"] = mark_rows_vectorized(data)

    # data.to_csv("data.csv", index=False)

    data = data[data["mark_value"] != "partial"]

    return data


def rename_columns(cols):
    new_columns = []
    date_counters = {}

    for col in cols:
        if "week-" in col:
            col = col.replace("-", "_")
            new_columns.append(col)
        elif any(char.isdigit() for char in col):
            val = col.split("_")[-1]
            col_base = col.split(f"_{val}")[0]
            if col_base not in date_counters:
                date_counters[col_base] = 1
            new_col = f"{col_base}_date_{date_counters[col_base]}"
            date_counters[col_base] += 1
            if date_counters[col_base] > 8:
                date_counters[col_base] = 1
            new_columns.append(new_col)
        else:
            new_columns.append(col)

    return new_columns


# def get_site_id(short_name):
#     check_short_names = ["Sams", "BH", "WB", "MU","UE","MP","OD","UW","TN","JH","JK","KK","KO","DL","HR","CH","MP","PB","RJ"]

#     if "_" in short_name and not any(sub in short_name for sub in check_short_names):
#         return short_name.split("_")[4][:6]
#     elif "Sams-" in short_name:
#         return short_name.split(",")[1].split("_")[-1]
#     elif "BH_" in short_name:
#         return short_name.split("_")[-2][:8]
#     elif "WB_" in short_name and "@Nokia" not in short_name:
#         site_id = short_name.split("_")[-2]
#         return site_id[:-1] if site_id[-1] in "ABCDEF" else site_id
#     elif "MU_" in short_name:
#         site_id = short_name.split("_")[-2]
#         return site_id[:-1] if site_id[-1] in "ABCDEF" else site_id
#     elif "UE_" in short_name:
#         site_id = short_name.split("_")[-2]
#         return site_id[:-1] if site_id[-1] in "ABCDEF" else site_id
#     elif "MP_" in short_name:
#         site_id = short_name.split("_")[-2]
#         return site_id[:-1] if site_id[-1] in "ABCDEF" else site_id
#     elif "OD_" in short_name:
#         site_id = short_name.split("_")[-2]
#         return site_id[:-1] if site_id[-1] in "ABCDEF" else site_id
#     elif "UW_" in short_name:
#         site_id = short_name.split("_")[-2]
#         return site_id[:-1] if site_id[-1] in "ABCDEF" else site_id
#     elif "TN_" in short_name:
#         site_id = short_name.split("_")[-2]
#         return site_id[:-1] if site_id[-1] in "ABCDEF" else site_id
#     elif "JH_" in short_name:
#         site_id = short_name.split("_")[-2]
#         return site_id[:-1] if site_id[-1] in "ABCDEF" else site_id
#     elif "KK_" in short_name:
#         site_id = short_name.split("_")[-2]
#         return site_id[:-1] if site_id[-1] in "ABCDEF" else site_id
#     elif "KO_" in short_name:
#         site_id = short_name.split("_")[-2]
#         return site_id[:-1] if site_id[-1] in "ABCDEF" else site_id
#     elif "MP_" in short_name:
#         site_id = short_name.split("_")[-2]
#         return site_id[:-1] if site_id[-1] in "ABCDEF" else site_id
#     elif "HR_" in short_name:
#         site_id = short_name.split("_")[-2]
#         return site_id[:-1] if site_id[-1] in "ABCDEF" else site_id
#     elif "DL_" in short_name:
#         site_id = short_name.split("_")[-2]
#         return site_id[:-1] if site_id[-1] in "ABCDEF" else site_id
#     elif "JK_" in short_name:
#         site_id = short_name.split("_")[-2]
#         return site_id[:-1] if site_id[-1] in "ABCDEF" else site_id
#     elif "CH_" in short_name:
#         site_id = short_name.split("_")[-2]
#         return site_id[:-1] if site_id[-1] in "ABCDEF" else site_id
#     elif "PB_" in short_name:
#         site_id = short_name.split("_")[-2]
#         return site_id[:-1] if site_id[-1] in "ABCDEF" else site_id
#     elif "RJ_" in short_name:
#         site_id = short_name.split("_")[-2]
#         return site_id[:-1] if site_id[-1] in "ABCDEF" else site_id
#     else:
#         return ""


def get_site_id(short_name):
    # Define a dictionary with prefixes and their corresponding parsing logic
    prefix_parsers = {
        "Sams-": lambda sn: sn.split(",")[1].split("_")[-1],
        "BH_": lambda sn: sn.split("_")[-2][:8],
        "WB_": lambda sn: (
            sn.split("_")[-2][:-1]
            if re.match(r"[A-Z]", sn.split("_")[-2][-1])
            else sn.split("_")[-2]
        ),
        "MU_": lambda sn: (
            sn.split("_")[-2][:-1]
            if re.match(r"[A-Z]", sn.split("_")[-2][-1])
            else sn.split("_")[-2]
        ),
        "UE_": lambda sn: (
            sn.split("_")[-2][:-1]
            if re.match(r"[A-Z]", sn.split("_")[-2][-1])
            else sn.split("_")[-2]
        ),
        "MP_": lambda sn: (
            sn.split("_")[-2][:-1]
            if re.match(r"[A-Z]", sn.split("_")[-2][-1])
            else sn.split("_")[-2]
        ),
        "OD_": lambda sn: (
            sn.split("_")[-2][:-1]
            if re.match(r"[A-Z]", sn.split("_")[-2][-1])
            else sn.split("_")[-2]
        ),
        "UW_": lambda sn: (
            sn.split("_")[-2][:-1]
            if re.match(r"[A-Z]", sn.split("_")[-2][-1])
            else sn.split("_")[-2]
        ),
        "TN_": lambda sn: (
            sn.split("_")[-2][:-1]
            if re.match(r"[A-Z]", sn.split("_")[-2][-1])
            else sn.split("_")[-2]
        ),
        "JH_": lambda sn: (
            sn.split("_")[-2][:-1]
            if re.match(r"[A-Z]", sn.split("_")[-2][-1])
            else sn.split("_")[-2]
        ),
        "KK_": lambda sn: (
            sn.split("_")[-2][:-1]
            if re.match(r"[A-Z]", sn.split("_")[-2][-1])
            else sn.split("_")[-2]
        ),
        "KO_": lambda sn: (
            sn.split("_")[-2][:-1]
            if re.match(r"[A-Z]", sn.split("_")[-2][-1])
            else sn.split("_")[-2]
        ),
        "HR_": lambda sn: (
            sn.split("_")[-2][:-1]
            if re.match(r"[A-Z]", sn.split("_")[-2][-1])
            else sn.split("_")[-2]
        ),
        "DL_": lambda sn: (
            sn.split("_")[-2][:-1]
            if re.match(r"[A-Z]", sn.split("_")[-2][-1])
            else sn.split("_")[-2]
        ),
        "JK_": lambda sn: (
            sn.split("_")[-2][:-1]
            if re.match(r"[A-Z]", sn.split("_")[-2][-1])
            else sn.split("_")[-2]
        ),
        "CH_": lambda sn: (
            sn.split("_")[-2][:-1]
            if re.match(r"[A-Z]", sn.split("_")[-2][-1])
            else sn.split("_")[-2]
        ),
        "PB_": lambda sn: (
            re.match(
                r"[A-Z]",
                (
                    sn.split("_")[-3]
                    if sn.split("_")[-1] in ["FDD", "TDD"]
                    else sn.split("_")[-2][:-1]
                )[-1],
            )
            and (
                sn.split("_")[-3][:-1]
                if sn.split("_")[-1] in ["FDD", "TDD"]
                else sn.split("_")[-2][:-1]
            )
            or (
                sn.split("_")[-3]
                if sn.split("_")[-1] in ["FDD", "TDD"]
                else sn.split("_")[-2][:-1]
            )
        ),
        "RJ_": lambda sn: (
            sn.split("_")[-2][:-1]
            if re.match(r"[A-Z]", sn.split("_")[-2][-1])
            else sn.split("_")[-2]
        ),
    }

    for prefix, parser in prefix_parsers.items():
        if short_name.startswith(prefix):
            return parser(short_name)

    if "_" in short_name and not any(sn in short_name for sn in prefix_parsers):
        return short_name.split("_")[4][:6]

    return ""


def get_LTE_download_link(df):
    df.reset_index(inplace=True)

    cols_to_swap = ["Short_name", "OEM_GGSN", "ECGI_4G"]
    cols_to_swap = [(col, "") for col in cols_to_swap]

    # Create a new MultiIndex for the columns to swap
    new_columns = [
        (level2, level1) if (level1, level2) in cols_to_swap else (level1, level2)
        for level1, level2 in df.columns
    ]

    # Set the new columns to the DataFrame
    df.columns = pd.MultiIndex.from_tuples(new_columns, names=df.columns.names)

    df[("", "Circle")] = df[("", "Short_name")].astype(str).apply(get_circle)

    df[("", "Site_ID")] = df[("", "Short_name")].astype(str).apply(get_site_id)

    circle_column = df.pop(("", "Circle"))

    site_id_Column = df.pop(("", "Site_ID"))

    df.insert(0, ("", "Circle"), circle_column)

    df.insert(2, ("", "Site_ID"), site_id_Column)

    filename = f"{uuid.uuid4()}.csv"

    # Ensure the media/excels/ directory exists
    excel_directory = os.path.join(settings.MEDIA_ROOT, "csvs")
    os.makedirs(excel_directory, exist_ok=True)

    # Create the full path for the file
    file_path = os.path.join(excel_directory, filename)

    # Save the DataFrame as an Excel file directly
    df.to_csv(file_path, index=False)

    # Generate the download link
    download_link = os.path.join(settings.MEDIA_URL, "csvs", filename)

    return download_link


class CustomPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 1000

# def save_daily_4g_kpi_report(data):
#     """
#     Save function to insert or update Daily_4G_KPI_REPORT data.

#     Args:
#         data (list of dict): A list of dictionaries, each containing the data to save.

#     Example:
#         data = [
#             {
#                 "Short_name": "Site1",
#                 "OEM_GGSN": "VendorX",
#                 "ECGI_4G": "12345",
#                 "week_1_val": 10.5,
#                 "week_2_val": 12.3,
#                 "date_1_val": 8.9,
#                 "date_2_val": 9.0,
#                 "date_3_val": 10.1,
#                 "date_4_val": 11.2,
#                 "date_5_val": 12.0,
#                 "date_6_val": 13.5,
#                 "date_7_val": 14.2,
#                 "date_8_val": 15.1,
#                 "kpi_name": "Sample KPI",
#                 "Date": "2024-01-01",
#             },
#             ...
#         ]
#     """
    
    
#     with transaction.atomic():
#         for _,record in data.iterrows():
#             try:
#                 obj, created = Daily_4G_KPI_REPORT.objects.update_or_create(
#                     Short_name=record.get("Short_name"),
#                     Date=datetime.strftime(record.get("Date"), "%Y-%m-%d"),
#                     oem =  record.get("OEM_GGSN"),
#                     ECGI_4G =  record.get("ECGI_4G"),
#                     kpi_name = record.get("kpi_name", "No KPI Found"),
#                     defaults={
#                         "week_1_val": record.get("week_1_val", 0),
#                         "week_2_val": record.get("week_2_val", 0),
#                         "date_1_val": record.get("date_1_val", 0),
#                         "date_2_val": record.get("date_2_val", 0),
#                         "date_3_val": record.get("date_3_val", 0),
#                         "date_4_val": record.get("date_4_val", 0),
#                         "date_5_val": record.get("date_5_val", 0),
#                         "date_6_val": record.get("date_6_val", 0),
#                         "date_7_val": record.get("date_7_val", 0),
#                         "date_8_val": record.get("date_8_val", 0),
#                     },
#                 )
#                 if created:
#                     print(f"Created new record: {obj.Short_name} for date {obj.Date}")
#                 else:
#                     print(f"Updated record: {obj.Short_name} for date {obj.Date}")
#             except Exception as e:
#                 print(f"Error saving record {record}: {e}")

def save_daily_4g_kpi_report(data):
    print("saving to database started...")
    data_dict = data.to_dict(orient="records")
    create_obj_list=[]
    for record in data_dict:
       obj= Daily_4G_KPI_REPORT(
           Short_name=record.get("Short_name"),
           Site_ID = record.get("Site_ID"),
           Date=datetime.strftime(record.get("Date"), "%Y-%m-%d"),
           oem =  record.get("OEM_GGSN"),
           ECGI_4G =  record.get("ECGI_4G"),
           kpi_name = record.get("kpi_name", "No KPI Found"),
           week_1_val = record.get("week_1_val", 0),
           week_2_val = record.get("week_2_val", 0),
           date_1_val = record.get("date_1_val", 0),
           date_2_val = record.get("date_2_val", 0),
           date_3_val = record.get("date_3_val", 0),
           date_4_val = record.get("date_4_val", 0),
           date_5_val = record.get("date_5_val", 0),
           date_6_val = record.get("date_6_val", 0),
           date_7_val = record.get("date_7_val", 0),
           date_8_val = record.get("date_8_val", 0),
       )
       create_obj_list.append(obj)
    Daily_4G_KPI_REPORT.objects.bulk_create(create_obj_list)
    print("saving to database completed...")
  

@api_view(["GET"])
def kpi_trend_4g_api(request):
    # objs = Daily_4G_KPI.objects.all().values()
    from_required_date = datetime.now().date() - timedelta(days=17)
    to_required_date = datetime.now().date() - timedelta(days=1)
    query = f"""
        SELECT * FROM public."RCA_TOOL_daily_4g_kpi" where "Date" between '{from_required_date}' and '{to_required_date}'
    """
    
    objs = get_data_from_table(query)
    
    
    objs.drop(
        columns=["id"], inplace=True
    )
    
    print(objs)
    objs['Date'] = pd.to_datetime(objs['Date'], errors='coerce')
    current_date = datetime.now().date()

    current_week = current_date.isocalendar()[1]

    objs['Week'] = objs['Date'].dt.isocalendar().week
    objs['year'] = objs['Date'].dt.year
    
    annual_weeks = objs[['Week', 'year']].drop_duplicates()
    print(annual_weeks)
    # annual_weeks = (
    #     objs.(week=ExtractWeek("Date"), year=ExtractYear("Date"))
    #     .values("week", "year")
    #     .distinct()
    # )
    week_numbers = annual_weeks['Week'].tolist()

    print(week_numbers)
    

    date_list = latest_date_to_past_7_days(objs)
    print(date_list)
    # exit(0)
    filtered_obj = objs[objs['Date'].isin(date_list)]

    current_df = filtered_obj
    current_df = cleaned_data(current_df)

    current_df = current_df.replace("nan", 0)

    current_df.drop(
        columns=["dlRsBoost", "RS_Power_dB", "name_SiteA", "name_SiteB"], inplace=True
    )

    filtered_df = process_remove_duplicates(current_df)

    current_df = filtered_df

    kpi =[
            'MV_Radio_NW_Availability'
            'MV_4G_Data_Volume_GB', 
            'MV_RRC_Setup_Success_Rate', 
            'MV_RRC_Setup_Success_Rate_DENOM', 
            'MV_ERAB_Setup_Success_Rate', 
            'MV_PS_Drop_Call_Rate', 
            'MV_DL_User_Throughput_Kbps', 
            'MV_UL_User_Throughput_Kbps', 
            'MV_Average_number_of_used_DL_PRBs', 
            'MV_Max_Connecteda_User', 
            'MV_E_UTRAN_Average_CQI', 
            'MV_PUCCH_SINR', 
            'MV_Average_UE_Distance_KM', 
            'MV_PS_handover_success_rate_LTE_INTER_SYSTEM', 
            'MV_PS_handover_success_rate_LTE_INTRA_SYSTEM', 
            'PS_InterF_HOSR', 
            'PS_IntraF_HOSR', 
            'UL_RSSI', 
            'MV_VoLTE_raffic', 
            'MV_VoLTE_DCR', 
            'VoLTE_Inter_Frequency_Handover_Success_Ratio', 
            'VoLTE_Intra_LTE_Handover_Success_Ratio', 
            'MV_VoLTE_Packet_Loss_UL', 
            'MV_VoLTE_Packet_Loss_DL',   
            'MV_Packet_Loss_DL', 
            'MV_Packet_Loss_UL', 
            'MV_CSFB_Redirection_Success_Rate', 
        ]

    current_dates = current_df["Date"].unique()

    date_list = pd.to_datetime(current_dates)
    date_format = sorted([date.strftime("%Y-%m-%d") for date in date_list])
    print(date_format)
    date_format_2 = sorted([date.strftime("%Y_%m_%d") for date in date_list])
    current_df.fillna(value=0, inplace=True)
    for col in kpi:
        current_df[col] = current_df[col].astype(float)

    current_pivot_df = current_df.pivot_table(
        values=kpi,
        index=["Short_name", "OEM_GGSN", "ECGI_4G"],
        columns="Date",
        aggfunc="mean",
        dropna=True,
    )
    week1_data = pd.DataFrame()
    week2_data = pd.DataFrame()
    # for week in week_numbers:
    #     if current_week - week == 1:
    #         # week1_data = pd.DataFrame(objs.filter(Date__week=week))
    #         week1_data = objs[objs['Week'] == week]
    #     if current_week - week == 2:
    #         # week2_data = pd.DataFrame(objs.filter(Date__week=week))
    #         week2_data = objs[objs['Week'] == week]
    
    week1_data = objs[objs['Week'] == week_numbers[-2]]
    week2_data = objs[objs['Week'] == week_numbers[-3]]
            
    print("Week-1 data:- ",week1_data)
    week1_data = get_last_five_days_of_week(week1_data)
    week2_data = get_last_five_days_of_week(week2_data)

    for col in kpi:
        week1_data[col] = week1_data[col].astype(float)
        week2_data[col] = week2_data[col].astype(float)

    weeks1 = week1_data.pivot_table(
        values=kpi,
        columns="Date",
        index=["Short_name"],
        aggfunc="mean",
        dropna=False,
    )

    weeks2 = week2_data.pivot_table(
        values=kpi,
        columns="Date",
        index=["Short_name"],
        aggfunc="mean",
        dropna=False,
    )

    week11 = {}

    week22 = {}

    for i, col in enumerate(kpi):
        if col in weeks1.columns:
            week11[f"{col}"] = round(weeks1[col].mean(axis=1), 2)

        if col in weeks2.columns:
            week22[f"{col}"] = round(weeks2[col].mean(axis=1), 2)

    n1 = pd.DataFrame(week11)

    n1.columns = pd.MultiIndex.from_tuples(
        [
            ('MV_Radio_NW_Availability', 'week-1'),
            ('MV_4G_Data_Volume_GB', 'week-1'),
            ('MV_RRC_Setup_Success_Rate', 'week-1'),
            ('MV_RRC_Setup_Success_Rate_DENOM', 'week-1'),
            ('MV_ERAB_Setup_Success_Rate', 'week-1'),
            ('MV_PS_Drop_Call_Rate', 'week-1'),
            ('MV_DL_User_Throughput_Kbps', 'week-1'),
            # ('MV_DL_User_Throughput_Kbps', 'week-1'),  # Duplicate - CUBH not present, repeated for order
            ('MV_UL_User_Throughput_Kbps', 'week-1'),
            ('MV_Average_number_of_used_DL_PRBs', 'week-1'),
            ('MV_Max_Connecteda_User', 'week-1'),
            ('MV_E_UTRAN_Average_CQI', 'week-1'),
            ('MV_PUCCH_SINR', 'week-1'),
            ('MV_Average_UE_Distance_KM', 'week-1'),
            # ('MV_Average_UE_Distance_KM', 'week-1'),  # Duplicate label for Average UE Distance_KM
            ('MV_PS_handover_success_rate_LTE_INTER_SYSTEM', 'week-1'),
            ('MV_PS_handover_success_rate_LTE_INTRA_SYSTEM', 'week-1'),
            ('PS_InterF_HOSR', 'week-1'),
            ('PS_IntraF_HOSR', 'week-1'),
            ('UL_RSSI', 'week-1'),
            # ('MV_UL_RSSI_dBm_PRB', 'week-1'),
            ('MV_VoLTE_raffic', 'week-1'),
            ('MV_VoLTE_DCR', 'week-1'),
            ('VoLTE_Inter_Frequency_Handover_Success_Ratio', 'week-1'),
            ('VoLTE_Intra_LTE_Handover_Success_Ratio', 'week-1'),
            ('MV_VoLTE_Packet_Loss_UL', 'week-1'),
            ('MV_VoLTE_Packet_Loss_DL', 'week-1'),  
            ('MV_Packet_Loss_DL', 'week-1'),
            ('MV_Packet_Loss_UL', 'week-1'),
            ('MV_CSFB_Redirection_Success_Rate', 'week-1'),
        ]
    )

    n2 = pd.DataFrame(week22)
    n2.columns = pd.MultiIndex.from_tuples(
        [
            ('MV_Radio_NW_Availability', 'week-2'),
            ('MV_4G_Data_Volume_GB', 'week-2'),
            ('MV_RRC_Setup_Success_Rate', 'week-2'),
            ('MV_RRC_Setup_Success_Rate_DENOM', 'week-2'),
            ('MV_ERAB_Setup_Success_Rate', 'week-2'),
            ('MV_PS_Drop_Call_Rate', 'week-2'),
            ('MV_DL_User_Throughput_Kbps', 'week-2'),
            # ('MV_DL_User_Throughput_Kbps', 'week-2'),  # Duplicate - CUBH not present, repeated for order
            ('MV_UL_User_Throughput_Kbps', 'week-2'),
            ('MV_Average_number_of_used_DL_PRBs', 'week-2'),
            ('MV_Max_Connecteda_User', 'week-2'),
            ('MV_E_UTRAN_Average_CQI', 'week-2'),
            ('MV_PUCCH_SINR', 'week-2'),
            ('MV_Average_UE_Distance_KM', 'week-2'),
            # ('MV_Average_UE_Distance_KM', 'week-2'),  # Duplicate label for Average UE Distance_KM
            ('MV_PS_handover_success_rate_LTE_INTER_SYSTEM', 'week-2'),
            ('MV_PS_handover_success_rate_LTE_INTRA_SYSTEM', 'week-2'),
            ('PS_InterF_HOSR', 'week-2'),
            ('PS_IntraF_HOSR', 'week-2'),
            ('UL_RSSI', 'week-2'),
            # ('MV_UL_RSSI_dBm_PRB', 'week-2'),
            ('MV_VoLTE_raffic', 'week-2'),
            ('MV_VoLTE_DCR', 'week-2'),
            ('VoLTE_Inter_Frequency_Handover_Success_Ratio', 'week-2'),
            ('VoLTE_Intra_LTE_Handover_Success_Ratio', 'week-2'),
            ('MV_VoLTE_Packet_Loss_UL', 'week-2'),  # Not present in original, may need correction
            ('MV_VoLTE_Packet_Loss_DL', 'week-2'),  # Not present in original, may need correction
            ('MV_Packet_Loss_DL', 'week-2'),
            ('MV_Packet_Loss_UL', 'week-2'),
            ('MV_CSFB_Redirection_Success_Rate', 'week-2'),

        ]
    )

    dfs = []
    for cell in kpi:
        if cell in n1.columns and cell in n2.columns:
            merged_df = pd.merge(
                n2[[cell]], n1[[cell]], left_index=True, right_index=True, how="outer"
            )
            dfs.append(merged_df)

    merge_df = pd.concat(dfs, axis=1)

    dfs1 = []
    for cell in kpi:
        if cell in merge_df.columns and cell in current_pivot_df.columns:
            result_df = pd.merge(
                merge_df[[cell]],
                current_pivot_df[[cell]],
                left_index=True,
                right_index=True,
                how="outer",
            )
            dfs1.append(result_df)
    result_df = pd.concat(dfs1, axis=1)

    result_df.fillna(value=0, inplace=True)
    print( "index as you want.......",result_df.index)
    
    ######################################## adding new database values ######################################################
    print(date_list[-1].date())
    trend_obj=Daily_4G_KPI_REPORT.objects.filter(Date = date_list[-1].date()) 
    if not trend_obj.exists():
        print("creating new records......")
        trend_4g_df = pd.DataFrame()
        for k in kpi:
            df_1 = result_df[k]
            print(df_1.columns)
            print(df_1.index)
            
            df_1['kpi_name'] = k
            trend_4g_df = pd.concat([trend_4g_df, df_1], axis=0)
        
        print(trend_4g_df)

        trend_4g_df.columns = [
            'week_1_val',
            'week_2_val',
            'date_1_val', 
            "date_2_val",
            "date_3_val",
            "date_4_val",
            "date_5_val",
            "date_6_val",
            "date_7_val",
            "date_8_val",
            'kpi_name',
        ]    
        # trend_4g_df.to_csv("trend_4g_df.csv")
        # exit(0)
        print(trend_4g_df)
        trend_4g_df.reset_index(inplace=True)
        
        trend_4g_df["Date"] = trend_4g_df['Short_name'].apply(lambda x: date_list[-1])
        # trend_4g_df["Site_ID"] = trend_4g_df['Short_name'].apply(lambda x: get_site_id)
        trend_4g_df["Site_ID"] = trend_4g_df["Short_name"].astype(str).apply(get_site_id)
        print("here is the merged df \n:- ", list(trend_4g_df.columns)) #print(trend_4g_df.columns)
        
        save_daily_4g_kpi_report(trend_4g_df)
    
    else:
        print("data already exist")
    #################################################################### end the new Code....... #################################################

    download_df = result_df.copy()
    download_link = get_LTE_download_link(download_df)

    print(download_link)
    
    result_df.columns = [
        "_".join([str(c) for c in col]).strip() for col in result_df.columns.values
    ]

    result_df.columns = rename_columns(result_df.columns)

    result_df.reset_index(inplace=True)

    result_df["Circle"] = result_df["Short_name"].astype(str).apply(get_circle)
    result_df["Site_ID"] = result_df["Short_name"].astype(str).apply(get_site_id)

    # for circle
    cols = result_df.columns.tolist()
    cols = [cols[-1]] + cols[:-1]
    result_df = result_df[cols]
    # result_df2 = drop_rows(result_df2)

    #for site id
    new_cols = result_df.columns.tolist()
    new_cols = [new_cols[-1]] + new_cols[:-1]
    result_df = result_df[new_cols]

    result_df = result_df.dropna(subset=["Short_name"])


    # paginator = CustomPagination()
    # paginated_result = paginator.paginate_queryset(result_df.to_dict('records'), request)

    json_data = result_df.to_json(orient="records")

    new_json = json.loads(json_data)

    return Response(
        {
            "count": 1000,
            # "next": "http://example.com/api/kpi_trend_4g_api?page=2",
            # "previous": null,
            "Status": True,
            "message": "successfully submitted.....",
            "Download_Link": download_link,
            "dates": date_format,
            "data": new_json,
        }
    )


@api_view(["GET", "POST"])
def  circle_based_rna_count(request):
    objs = Daily_4G_KPI.objects.all()

    latest_date = objs.aggregate(latest_date=Max("Date"))
    latest_date = latest_date["latest_date"]

    date_list = []

    for value in range(8):
        date = latest_date - timedelta(value)

        date = date.strftime("%Y-%m-%d")

        date_list.append(date)
    date_list = sorted(date_list)

    new_objs = objs.filter(Date__in=date_list)
    df = pd.DataFrame(new_objs.values())
    df = cleaned_data(df)
    df = df.drop(columns="id", axis=1)

    df.fillna(value=0, inplace=True)

    kpi = [
        "MV_4G_Data_Volume_GB",
        "MV_Radio_NW_Availability",
        "MV_VoLTE_raffic",
        "MV_DL_User_Throughput_Kbps",
        "MV_E_UTRAN_Average_CQI",
        "UL_RSSI",
        "MV_Average_number_of_used_DL_PRBs",
        "MV_RRC_Setup_Success_Rate",
        "MV_ERAB_Setup_Success_Rate",
        "MV_PS_Drop_Call_Rate",
        "MV_Max_Connecteda_User",
        "MV_PUCCH_SINR",
        "MV_Average_UE_Distance_KM",
        "MV_PS_handover_success_rate_LTE_INTER_SYSTEM",
        "MV_PS_handover_success_rate_LTE_INTRA_SYSTEM",
        "UL_RSSI_Nokia_RSSI_SINR",
        "MV_VoLTE_DCR",
        "MV_Packet_Loss_DL",
        "MV_Packet_Loss_UL",
    ]

    for col in kpi:
        df[col] = df[col].astype(float)

    pivot_df = pd.pivot_table(
        df,
        values=["MV_4G_Data_Volume_GB", "MV_Radio_NW_Availability"],
        index="Short_name",
        columns="Date",
    )

    pivot_df.columns = [f"{col[0]}_{col[1]}" for col in pivot_df.columns]
    pivot_df.reset_index(inplace=True)

    pivot_df["Circle"] = (
        pivot_df["Short_name"].apply(lambda x: str(x).strip()).apply(get_circle)
    )
    cols = pivot_df.columns.tolist()
    cols = [cols[-1]] + cols[:-1]
    pivot_df = pivot_df[cols]

    result = []
    i = 1
    for date in date_list:
        columns_to_keep = [
            "Circle",
            "Short_name",
            f"MV_4G_Data_Volume_GB_{date}",
            f"MV_Radio_NW_Availability_{date}",
        ]
        new_df = pivot_df[columns_to_keep].copy()

        new_df = new_df[
            (new_df[f"MV_4G_Data_Volume_GB_{date}"] == 0)
            & (new_df[f"MV_Radio_NW_Availability_{date}"] >= 90)
        ]

        new_df.rename(
            columns={
                f"MV_4G_Data_Volume_GB_{date}": "MV_4G_Data_Volume_GB",
                f"MV_Radio_NW_Availability_{date}": "MV_Radio_NW_Availability",
            },
            inplace=True,
        )

        new_df["Circle"] = new_df["Circle"].astype(str)
        new_df["Short_name"] = new_df["Short_name"].astype(str)

        circle_counts = new_df.groupby("Circle")["Short_name"].nunique().reset_index()

        circle_counts = circle_counts.rename(columns={"Short_name": "Cell_Count"})

        circle_counts[f"date_{i}"] = date

        i = i + 1

        result_dict = circle_counts.to_dict(orient="records")

        result.extend(result_dict)

    return Response(
        {
            "Status": True,
            "message": "sucessfully fetched",
            "dates": date_list,
            "data": result,
        }
    )


@api_view(["POST"])
def hyperlink_circle_based_rna_count(request):
    circle = request.POST.get("circle")
    payload_date = request.POST.get("date")

    objs = Daily_4G_KPI.objects.all()

    latest_date = objs.aggregate(latest_date=Max("Date"))
    latest_date = latest_date["latest_date"]

    date_list = []

    for value in range(8):
        date = latest_date - timedelta(value)

        date = date.strftime("%Y-%m-%d")

        date_list.append(date)
    date_list = sorted(date_list)

    new_objs = objs.filter(Date__in=date_list)
    df = pd.DataFrame(new_objs.values())

    df = cleaned_data(df)

    df = df.drop(columns="id", axis=1)

    df.fillna(value=0, inplace=True)

    kpi = [
        "MV_4G_Data_Volume_GB",
        "MV_Radio_NW_Availability",
        "MV_VoLTE_raffic",
        "MV_DL_User_Throughput_Kbps",
        "MV_E_UTRAN_Average_CQI",
        "UL_RSSI",
        "MV_Average_number_of_used_DL_PRBs",
        "MV_RRC_Setup_Success_Rate",
        "MV_ERAB_Setup_Success_Rate",
        "MV_PS_Drop_Call_Rate",
        "MV_Max_Connecteda_User",
        "MV_PUCCH_SINR",
        "MV_Average_UE_Distance_KM",
        "MV_PS_handover_success_rate_LTE_INTER_SYSTEM",
        "MV_PS_handover_success_rate_LTE_INTRA_SYSTEM",
        "UL_RSSI_Nokia_RSSI_SINR",
        "MV_VoLTE_DCR",
        "MV_Packet_Loss_DL",
        "MV_Packet_Loss_UL",
    ]

    for col in kpi:
        df[col] = df[col].astype(float)

    pivot_df = pd.pivot_table(
        df,
        values=["MV_4G_Data_Volume_GB", "MV_Radio_NW_Availability"],
        index="Short_name",
        columns="Date",
    )

    pivot_df.columns = [f"{col[0]}_{col[1]}" for col in pivot_df.columns]
    pivot_df.reset_index(inplace=True)

    pivot_df["Circle"] = (
        pivot_df["Short_name"].apply(lambda x: str(x).strip()).apply(get_circle)
    )
    cols = pivot_df.columns.tolist()
    cols = [cols[-1]] + cols[:-1]
    pivot_df = pivot_df[cols]

    result = []
    for date in date_list:
        columns_to_keep = [
            "Circle",
            "Short_name",
            f"MV_4G_Data_Volume_GB_{date}",
            f"MV_Radio_NW_Availability_{date}",
        ]
        new_df = pivot_df[columns_to_keep].copy()
        new_df = new_df[
            (new_df[f"MV_4G_Data_Volume_GB_{date}"] == 0)
            & (new_df[f"MV_Radio_NW_Availability_{date}"] >= 90)
        ]

        new_df["Circle"] = new_df["Circle"].astype(str)
        new_df["Short_name"] = new_df["Short_name"].astype(str)

        filtered_df = new_df[new_df["Circle"].apply(lambda x: x.strip()) == circle]

        filtered_df = filtered_df.rename(
            columns={
                f"MV_4G_Data_Volume_GB_{date}": "MV_4G_Data_Volume_GB",
                f"MV_Radio_NW_Availability_{date}": "MV_Radio_NW_Availability",
            }
        )

        if not filtered_df.empty and date == payload_date:
            hyper_link_dict = filtered_df.to_dict(orient="records")
            result.extend(hyper_link_dict)

    print(result)

    return Response({"Status": True, "date": payload_date, "data": result})


@api_view(["POST", "GET"])
def Date_Wise_Dashboard(request):
    objs = Daily_4G_KPI.objects.all()
    latest_date = objs.aggregate(latest_date=Max("Date"))["latest_date"]

    current_date = latest_date.strftime("%Y-%m-%d")
    previous_date = (latest_date - timedelta(days=1)).strftime("%Y-%m-%d")

    objs_new = objs.filter(Date__in=[current_date, previous_date])
    df = pd.DataFrame(list(objs_new.values()))

    df = cleaned_data(df)

    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")

    kpi = [
        "MV_4G_Data_Volume_GB",
        "MV_Radio_NW_Availability",
    ]

    for col in kpi:
        df[col] = df[col].astype(float)

    df_pivot = pd.pivot_table(
        df,
        index="Short_name",
        columns="Date",
        values=kpi,
        aggfunc="mean",
        fill_value=0,
    )

    df_pivot.drop(columns=[("MV_Radio_NW_Availability", previous_date)], inplace=True)

    df_pivot["delta"] = (
        df_pivot[("MV_4G_Data_Volume_GB", previous_date)]
        - df_pivot[("MV_4G_Data_Volume_GB", current_date)]
    )

    df_pivot = df_pivot[
        df_pivot.index.isin(df[df["Date"] == current_date]["Short_name"])
    ]
    conditions = [
        (df_pivot["delta"] >= 100),
        (df_pivot["delta"] >= 50) & (df_pivot["delta"] < 100),
        (df_pivot["delta"] >= 30) & (df_pivot["delta"] < 50),
        (df_pivot["delta"] >= 10) & (df_pivot["delta"] < 30),
        (df_pivot["delta"] < 10),
    ]
    choices = ["P0", "P1", "P2", "P3", "P4"]
    df_pivot["del_value"] = np.select(conditions, choices, default="P4")

    new_dataframe = df_pivot.reset_index()
    new_dataframe["Circle"] = new_dataframe["Short_name"].apply(get_circle)

    cols = new_dataframe.columns.tolist()
    cols = [cols[-1]] + cols[:-1]
    new_dataframe = new_dataframe[cols]
    print(new_dataframe)
    payload_dip_cells = list(
        new_dataframe[new_dataframe["del_value"].isin(["P0", "P1", "P2"])][
            "Short_name"
        ].unique()
    )
    pivot_delta_df = new_dataframe.pivot_table(
        index="Circle", columns="del_value", values="delta", aggfunc="count"
    )

    if ("", "P4") in pivot_delta_df.columns:
        pivot_delta_df.drop(columns=[("", "P4")], inplace=True)

    pivot_delta_df["Total"] = pivot_delta_df.sum(axis=1)
    new_total = pivot_delta_df.sum().rename("new_total")
    pivot_delta_df = pivot_delta_df.append(new_total)

    pivot_delta_df.columns = [
        "_".join(filter(None, col)).strip() for col in pivot_delta_df.columns
    ]
    new_data = pivot_delta_df.reset_index()

    new_columns = ["Circle"] + [col for col in new_data.columns if col != "Circle"]
    new_data.columns = new_columns
    print(new_data)
    json_data = new_data.to_json(orient="records")
    new_json = json.loads(json_data)

    return Response(
        {
            "Status": True,
            "message": "Successfully fetched the data.",
            "current_date": current_date,
            "previous_date": previous_date,
            "data": new_json,
            "payload_dip_cells": payload_dip_cells,
        }
    )


@api_view(["POST"])
def hyperlink_Date_wise_dashboard(request):
    circle = request.POST.get("circle")
    delta = request.POST.get("delta")

    print(circle)
    print(delta)

    objs = Daily_4G_KPI.objects.all()
    objs = objs.values()
    latest_date = objs.aggregate(latest_date=Max("Date"))
    latest_date = latest_date["latest_date"]

    current_date = latest_date.strftime("%Y-%m-%d")
    previous_date = latest_date - timedelta(1)
    previous_date = previous_date.strftime("%Y-%m-%d")

    objs_new = objs.filter(Date__in=[current_date, previous_date])

    df = pd.DataFrame(objs_new)

    df = cleaned_data(df)

    df["Date"] = pd.to_datetime(df["Date"])

    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    # print(df["Date"].unique())

    df.fillna(value=0, inplace=True)

    kpi = [
        "MV_4G_Data_Volume_GB",
        "MV_Radio_NW_Availability",
    ]

    for col in kpi:
        df[col] = df[col].astype(dtype=float)

    df_pivot = pd.pivot_table(
        df,
        index="Short_name",
        columns="Date",
        values=kpi,
        aggfunc="mean",
    )

    df_pivot.drop(columns=[(kpi[1], previous_date)], inplace=True)

    df_pivot[("delta", "")] = (
        df_pivot[(kpi[0], previous_date)] - df_pivot[(kpi[0], current_date)]
    )

    df_pivot[("del_value", "")] = ""

    for index, row in df_pivot.iterrows():
        if row[("delta", "")] >= 100:
            df_pivot.loc[index, ("del_value", "")] = "P0"
        elif row[("delta", "")] >= 50 and row[("delta", "")] < 100:
            df_pivot.loc[index, ("del_value", "")] = "P1"
        elif row[("delta", "")] >= 30 and row[("delta", "")] < 50:
            df_pivot.loc[index, ("del_value", "")] = "P2"
        elif row[("delta", "")] >= 10 and row[("delta", "")] < 30:
            df_pivot.loc[index, ("del_value", "")] = "P3"
        else:
            df_pivot.loc[index, ("del_value", "")] = "P4"

    new_dataframe = df_pivot.reset_index()

    new_dataframe["Circle"] = (
        new_dataframe["Short_name"].apply(lambda x: str(x)).apply(get_circle)
    )

    cols = new_dataframe.columns.tolist()
    cols = [cols[-1]] + cols[:-1]
    new_dataframe = new_dataframe[cols]

    new_columns = [f"{col[0]}_{col[1]}".strip("_") for col in new_dataframe.columns]

    new_dataframe.columns = new_columns

    new_dataframe = new_dataframe.rename(
        columns={
            f"{kpi[0]}_{current_date}": f"{kpi[0]}_current_date",
            f"{kpi[0]}_{previous_date}": f"{kpi[0]}_previous_date",
            f"{kpi[1]}_{current_date}": f"{kpi[1]}_current_date",
        }
    )

    new_dataframe = new_dataframe[
        new_dataframe["del_value"].isin(["P0", "P1", "P2", "P3"])
    ]

    new_dataframe = new_dataframe[
        (new_dataframe["Circle"] == circle) & (new_dataframe["del_value"] == delta)
    ]

    print(new_dataframe)

    json_data = new_dataframe.to_json(orient="records")

    new_json = json.loads(json_data)

    return Response(
        {
            "Status": True,
            "message": "hyper link data",
            "current_date": current_date,
            "previous_date": previous_date,
            "data": new_json,
        }
    )


def assign_depth_2(row):
    if row["Delta"] >= 100:
        return "P0"
    elif 50 <= row["Delta"] < 100:
        return "P1"
    elif 30 <= row["Delta"] < 50:
        return "P2"
    elif 10 <= row["Delta"] < 30:
        return "P3"
    else:
        return None


@api_view(["GET"])
def Week_Wise_Dashboard(request):
    objs = Daily_4G_KPI.objects.all()

    latest_date = objs.aggregate(latest_date=Max("Date"))["latest_date"]

    previous_same_date = latest_date - timedelta(days=7)

    print(previous_same_date)

    objs = objs.filter(Date__in=[latest_date, previous_same_date])

    objs = objs.values()

    df = cleaned_data(pd.DataFrame(objs))
    df["Short_name"] = df["Short_name"].str.strip()

    kpi = ["MV_4G_Data_Volume_GB"]
    for col in kpi:
        df[col] = df[col].astype(float)

    pivot_df = df.pivot_table(
        values=["MV_4G_Data_Volume_GB"], columns="Date", index="Short_name"
    )

    pivot_df.fillna(value=0, inplace=True)
    pivot_df["Delta"] = (
        pivot_df["MV_4G_Data_Volume_GB", previous_same_date]
        - pivot_df["MV_4G_Data_Volume_GB", latest_date]
    )
    pivot_df.columns = [f"{col[0]}_{col[1]}" for col in pivot_df.columns]

    pivot_df.columns = [col.rstrip("_") for col in pivot_df.columns]
    pivot_df.reset_index(inplace=True)

    pivot_df["depth"] = pivot_df.apply(assign_depth_2, axis=1)

    pivot_df["Circle"] = (
        pivot_df["Short_name"].apply(lambda x: str(x)).apply(get_circle)
    )

    cols = pivot_df.columns.tolist()
    cols = [cols[-1]] + cols[:-1]
    pivot_df = pivot_df[cols]
    piv = pivot_df.pivot_table(
        values="Delta", columns="depth", index=["Circle"], aggfunc="count"
    )

    piv["total"] = piv.sum(axis=1)

    new_total = piv.sum().rename("Base_Total")

    piv = piv.append(new_total)

    new_data = piv.reset_index()

    json_data = new_data.to_json(orient="records")

    new_json = json.loads(json_data)

    return Response(
        {
            "Status": True,
            "message": "Data Successfully fetehed",
            "latest_date": latest_date,
            "previous_date": previous_same_date,
            "data": new_json,
        }
    )


@api_view(["POST"])
def Hyperlink_Week_Wise_Dashboard(request):
    circle = request.POST.get("circle") if request.POST.get("circle") else None
    depth = request.POST.get("delta") if request.POST.get("delta") else None

    objs = Daily_4G_KPI.objects.all()
    latest_date = objs.aggregate(latest_date=Max("Date"))["latest_date"]

    previous_same_date = latest_date - timedelta(days=7)

    print(previous_same_date)

    objs = objs.filter(Date__in=[latest_date, previous_same_date])

    objs = objs.values()

    df = cleaned_data(pd.DataFrame(objs))
    df["Short_name"] = df["Short_name"].str.strip()

    kpi = ["MV_4G_Data_Volume_GB"]
    # for col in kpi:
    #     df[col] = df[col].astype(float)

    pivot_df = df.pivot_table(
        values=["MV_4G_Data_Volume_GB"], columns="Date", index="Short_name"
    )

    pivot_df.fillna(value=0, inplace=True)
    pivot_df["Delta"] = (
        pivot_df["MV_4G_Data_Volume_GB", previous_same_date]
        - pivot_df["MV_4G_Data_Volume_GB", latest_date]
    )

    pivot_df.columns = [f"{col[0]}_{col[1]}" for col in pivot_df.columns]

    pivot_df.columns = [col.rstrip("_") for col in pivot_df.columns]
    pivot_df.reset_index(inplace=True)

    pivot_df["depth"] = pivot_df.apply(assign_depth_2, axis=1)

    pivot_df["Circle"] = (
        pivot_df["Short_name"].apply(lambda x: str(x)).apply(get_circle)
    )

    cols = pivot_df.columns.tolist()
    cols = [cols[-1]] + cols[:-1]
    pivot_df = pivot_df[cols]

    # pivot_df.to_excel("pivot_data.xlsx")
    # print(pivot_df)

    new_dataframe = pivot_df[
        (pivot_df["Circle"] == circle) & (pivot_df["depth"] == depth)
    ]
    print(new_dataframe)

    new_dataframe = new_dataframe.rename(
        columns={
            f"MV_4G_Data_Volume_GB_{latest_date}": "MV_4G_Data_Volume_GB_current_date",
            f"MV_4G_Data_Volume_GB_{previous_same_date}": "MV_4G_Data_Volume_GB_previous_date",
        }
    )

    link = new_dataframe.to_json(orient="records")
    new_json = json.loads(link)

    return Response(
        {
            "Status": True,
            "current_date": latest_date,
            "previous_date": previous_same_date,
            "data": new_json,
        }
    )


@api_view(["GET"])
def hyperlink_day_to_day_all(request):

    objs = Daily_4G_KPI.objects.all()
    objs = objs.values()
    latest_date = objs.aggregate(latest_date=Max("Date"))
    latest_date = latest_date["latest_date"]

    current_date = latest_date.strftime("%Y-%m-%d")
    previous_date = latest_date - timedelta(1)
    previous_date = previous_date.strftime("%Y-%m-%d")

    objs_new = objs.filter(Date__in=[current_date, previous_date])

    df = cleaned_data(pd.DataFrame(objs_new))

    df["Date"] = pd.to_datetime(df["Date"])

    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    # print(df["Date"].unique())

    df.fillna(value=0, inplace=True)

    kpi = [
        "MV_4G_Data_Volume_GB",
        "MV_Radio_NW_Availability",
    ]

    for col in kpi:
        df[col] = df[col].astype(dtype=float)

    df_pivot = pd.pivot_table(
        df,
        index="Short_name",
        columns="Date",
        values=kpi,
        aggfunc="mean",
    )

    df_pivot.drop(columns=[(kpi[1], previous_date)], inplace=True)

    df_pivot[("delta", "")] = (
        df_pivot[(kpi[0], previous_date)] - df_pivot[(kpi[0], current_date)]
    )

    df_pivot[("del_value", "")] = ""

    for index, row in df_pivot.iterrows():
        if row[("delta", "")] >= 100:
            df_pivot.loc[index, ("del_value", "")] = "P0"
        elif row[("delta", "")] >= 50 and row[("delta", "")] < 100:
            df_pivot.loc[index, ("del_value", "")] = "P1"
        elif row[("delta", "")] >= 30 and row[("delta", "")] < 50:
            df_pivot.loc[index, ("del_value", "")] = "P2"
        elif row[("delta", "")] >= 10 and row[("delta", "")] < 30:
            df_pivot.loc[index, ("del_value", "")] = "P3"
        else:
            df_pivot.loc[index, ("del_value", "")] = "P4"

    new_dataframe = df_pivot.reset_index()

    new_dataframe["Circle"] = (
        new_dataframe["Short_name"].apply(lambda x: str(x)).apply(get_circle)
    )

    cols = new_dataframe.columns.tolist()
    cols = [cols[-1]] + cols[:-1]
    new_dataframe = new_dataframe[cols]

    new_columns = [f"{col[0]}_{col[1]}".strip("_") for col in new_dataframe.columns]

    new_dataframe.columns = new_columns

    new_dataframe = new_dataframe.rename(
        columns={
            f"{kpi[0]}_{current_date}": f"{kpi[0]}_current_date",
            f"{kpi[0]}_{previous_date}": f"{kpi[0]}_previous_date",
            f"{kpi[1]}_{current_date}": f"{kpi[1]}_current_date",
        }
    )

    new_dataframe = new_dataframe[
        new_dataframe["del_value"].isin(["P0", "P1", "P2", "P3"])
    ]

    print(new_dataframe)
    link = new_dataframe.to_json(orient="records")
    new_json = json.loads(link)

    return Response(
        {
            "Status": True,
            "current_date": current_date,
            "previous_date": previous_date,
            "data": new_json,
        }
    )


@api_view(["GET"])
def hyperlink_week_to_week_all(request):

    objs = Daily_4G_KPI.objects.all()
    latest_date = objs.aggregate(latest_date=Max("Date"))["latest_date"]

    previous_same_date = latest_date - timedelta(days=7)

    print(previous_same_date)

    objs = objs.filter(Date__in=[latest_date, previous_same_date])

    objs = objs.values()

    df = cleaned_data(pd.DataFrame(objs))
    df["Short_name"] = df["Short_name"].str.strip()

    kpi = ["MV_4G_Data_Volume_GB"]
    for col in kpi:
        df[col] = df[col].astype(float)

    pivot_df = df.pivot_table(
        values=["MV_4G_Data_Volume_GB"], columns="Date", index="Short_name"
    )

    pivot_df.fillna(value=0, inplace=True)
    pivot_df["Delta"] = (
        pivot_df["MV_4G_Data_Volume_GB", previous_same_date]
        - pivot_df["MV_4G_Data_Volume_GB", latest_date]
    )

    pivot_df.columns = [f"{col[0]}_{col[1]}" for col in pivot_df.columns]

    pivot_df.columns = [col.rstrip("_") for col in pivot_df.columns]
    pivot_df.reset_index(inplace=True)

    pivot_df["depth"] = pivot_df.apply(assign_depth_2, axis=1)

    pivot_df["Circle"] = (
        pivot_df["Short_name"].apply(lambda x: str(x)).apply(get_circle)
    )

    cols = pivot_df.columns.tolist()
    cols = [cols[-1]] + cols[:-1]
    pivot_df = pivot_df[cols]

    pivot_df = pivot_df.rename(
        columns={
            f"MV_4G_Data_Volume_GB_{latest_date}": "MV_4G_Data_Volume_GB_current_date",
            f"MV_4G_Data_Volume_GB_{previous_same_date}": "MV_4G_Data_Volume_GB_previous_date",
        }
    )

    print(pivot_df.columns)

    pivot_df = pivot_df[pivot_df["depth"].isin(["P0", "P1", "P2", "P3"])]
    print(pivot_df.shape)

    link = pivot_df.to_json(orient="records")
    new_json = json.loads(link)

    return Response(
        {
            "Status": True,
            "current_date": latest_date,
            "privous_date": previous_same_date,
            "data": new_json,
        }
    )


@api_view(["GET"])
def get_data_from_url(request):
    url1 = (
        "http://103.242.225.195:8000/Zero_Count_Rna_Payload_Tool/Date_Wise_Dashboard/"
    )
    url = "http://103.242.225.195:8000/RCA_TOOL/get-rca-output-dated/"

    # First API request (GET)
    res = requests.get(url1)
    res_data = res.json()
    date = res_data["current_date"]
    # print(date)
    if res.status_code != 200:
        return Response(
            {"error": f"Failed to fetch data from {url1}"}, status=res.status_code
        )
    # val = list(res_data["payload_dip_cells"])
    val = ",".join(res_data["payload_dip_cells"])
    # print(val)

    data = {
        "date": date,
        "cell_name": val,
    }

    # Second API request (POST)
    response = requests.post(url, data=data)
    # print(response.json())
    if response.status_code == 200:
        response_data = response.json()
        df = pd.DataFrame(response_data["data"])

        response_data = df.to_json(orient="records")
        response_data = json.loads(response_data)
        # print(df)

        return Response({"resposne_data": response_data}, status=status.HTTP_200_OK)
    else:
        return Response(
            {
                "error": f"Failed with status code {response.status_code}: {response.text}"
            },
            status=response.status_code,
        )


@api_view(['GET'])
def ticket_counter_api(request):
    try:
        # Fetching the database table name and latest date
        db_name = Daily_4G_KPI._meta.db_table
        latest_date = Daily_4G_KPI.objects.aggregate(latest_date=Max("Date"))['latest_date']

        if not latest_date:
            raise ValueError("No data available in the database for processing.")

        latest_date_str = latest_date.strftime('%Y-%m-%d')
        previous_date_str = (latest_date - timedelta(1)).strftime('%Y-%m-%d')

        # Constructing the SQL query
        query_n = f"""
            SELECT * FROM "{db_name}"
            WHERE "Date" IN ('{latest_date_str}', '{previous_date_str}')
        """

        # Processing the data
        try:
            latest_date_df = process_remove_duplicates(get_data_from_table(query_n))
        except Exception as e:
            logger.error(f"Error processing data from the table: {e}")
            return Response({"status": False, "message": "Error processing data from the table."}, status=500)

        # Ensuring necessary columns exist
        if "mark_value" in latest_date_df.columns:
            latest_date_df.drop(columns=["mark_value"], inplace=True)

        latest_date_df.fillna(value=0, inplace=True)
        latest_date_df["Date"] = pd.to_datetime(latest_date_df["Date"]).dt.strftime("%Y-%m-%d")

        kpi = ["MV_Radio_NW_Availability", "MV_4G_Data_Volume_GB"]

        # Creating the pivot table
        try:
            pivot_table = latest_date_df.pivot_table(
                index=['Short_name', 'OEM_GGSN'],
                columns="Date",
                values=kpi,
                aggfunc="mean"
            )
        except KeyError as e:
            logger.error(f"Error creating pivot table: {e}")
            return Response({"status": False, "message": "Required columns are missing for pivot table."}, status=500)

        pivot_table.reset_index(inplace=True)

        # Calculating deltas and priorities
        try:
            pivot_table["delta"] = pivot_table[(kpi[1], previous_date_str)] - pivot_table[(kpi[1], latest_date_str)]
            column_to_drop = (kpi[0], previous_date_str)
            if column_to_drop in pivot_table.columns:
                pivot_table.drop(columns=[column_to_drop], inplace=True)
        except KeyError as e:
            logger.error(f"Error calculating deltas or dropping columns: {e}")
            return Response({"status": False, "message": "Error calculating deltas or dropping columns."}, status=500)

        priority_map = {100: "P0", 50: "P1", 30: "P2", 10: "P3", 0: "P4"}

        pivot_table['del_value'] = pivot_table['delta'].apply(
            lambda x: next((v for k, v in priority_map.items() if x >= k), "P4")
        )

        pivot_table['Circle'] = pivot_table['Short_name'].apply(
            lambda x: get_circle(x) if x else "Unknown"
        )

        # Reordering columns
        new_cols = pivot_table.columns.to_list()
        new_cols = [new_cols[-1]] + new_cols[:-1]
        pivot_table = pivot_table[new_cols]

        # Filtering data
        pivot_table = pivot_table[pivot_table["del_value"].isin(["P0", "P1", "P2"])]

        # Splitting and merging data
        print("pivot_table \n",pivot_table)
        ericsson_df = pivot_table[pivot_table["OEM_GGSN"] == "Ericsson"]
        remaining_df = pivot_table[
            (pivot_table["OEM_GGSN"] != "Ericsson") &
            (pivot_table['Short_name'].str.contains("_ZQ_", na=False))
        ]
        result_df = pd.concat([ericsson_df, remaining_df], axis=0)

        result_df.rename(
            columns={
                f"MV_4G_Data_Volume_GB {latest_date_str}": "MV_4G_Data_Volume_GB_current_date",
                f"MV_4G_Data_Volume_GB {previous_date_str}": "MV_4G_Data_Volume_GB_previous_date",
                f"MV_Radio_NW_Availability {latest_date_str}": "MV_Radio_NW_Availability_current_date",
            }, inplace=True
        )

        print(result_df)
        # Formatting the result
        result_df.columns = [f"{col[0]} {col[1]}" for col in result_df.columns]
        result_df.reset_index(drop=True, inplace=True)
        result_df.columns = result_df.columns.str.strip()

        print(result_df)

        # Converting to JSON
        json_data = result_df.to_json(orient="records")
        new_json = json.loads(json_data)

        return Response({
            "status": True,
            "message": "Data successfully fetched",
            "latest_date": latest_date_str,
            "previous_date": previous_date_str,
            "all_data": new_json,
        })

    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
        return Response({"status": False, "message": str(ve)}, status=400)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return Response({"status": False, "message": "An unexpected error occurred."}, status=500)

    






# @api_view(["GET"])
# def ticket_counter_api(request):
#     try:
#         # Fetch data from the database
        
#         latest_date = Daily_4G_KPI.objects.aggregate(latest_date=Max("Date"))["latest_date"]
#         objs = Daily_4G_KPI.objects.filter(Q(Date__in = [latest_date, latest_date - timedelta(1)]))
#         if not latest_date:
#             raise ValueError("No data available in the database.")

#         current_date = latest_date.strftime("%Y-%m-%d")
#         previous_date = (latest_date - timedelta(days=1)).strftime("%Y-%m-%d")

#         df = pd.DataFrame(list(objs.values()))
#         df = process_remove_duplicates(df)

#         if df.empty:
#             raise ValueError("No data found for the selected dates.")
#         df = cleaned_data(df)
#         df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")

#         # Ensure numeric conversion
#         kpi = ["MV_4G_Data_Volume_GB", "MV_Radio_NW_Availability"]
#         df[kpi] = df[kpi].astype(float)

#         # Pivot Table Creation
#         df_pivot = pd.pivot_table(
#             df,
#             index=["Short_name", "OEM_GGSN"],
#             columns="Date",
#             values=kpi,
#             aggfunc="mean",
#             fill_value=0,
#         )

#         # Add delta and priority levels
#         df_pivot["delta"] = (
#             df_pivot[("MV_4G_Data_Volume_GB", previous_date)]
#             - df_pivot[("MV_4G_Data_Volume_GB", current_date)]
#         )
#         df_pivot.drop(columns=[(kpi[1],previous_date)], inplace=True)
#         priority_map = {
#             100: "P0",
#             50: "P1",
#             30: "P2",
#             10: "P3",
#             0: "P4",
#         }
#         df_pivot["del_value"] = df_pivot["delta"].apply(
#             lambda x: next((v for k, v in priority_map.items() if x >= k), "P4")
#         )
        

#         new_dataframe = df_pivot.reset_index()
#         new_dataframe["Circle"] = new_dataframe["Short_name"].apply(get_circle)

#         cols = new_dataframe.columns.tolist()
#         cols = [cols[-1]] + cols[:-1]
#         new_dataframe = new_dataframe[cols]

#         data_df_new = new_dataframe.copy()

#         data_df_new.columns = [f"{col[0]} {col[1]}" for col in data_df_new.columns]
#         data_df_new.reset_index(drop=True, inplace=True)
#         data_df_new.columns = data_df_new.columns.str.strip()
#         data_df_new = data_df_new[data_df_new["del_value"].isin(["P0", "P1", "P2"])]

#         data_df_new = data_df_new.rename(
#             columns={
#                 f"MV_4G_Data_Volume_GB {current_date}": "MV_4G_Data_Volume_GB_current_date",
#                 f"MV_4G_Data_Volume_GB {previous_date}": "MV_4G_Data_Volume_GB_previous_date",
#                 f"MV_Radio_NW_Availability {current_date}": "MV_Radio_NW_Availability_current_date",
#             }
#         )

#         print(data_df_new)

#         ericsson_df = data_df_new[data_df_new["OEM_GGSN"].isin(["Ericsson"])]

#         # print(ericsson_df)

#         remaining_df = data_df_new[data_df_new["OEM_GGSN"] != "Ericsson"]
#         remaining_df = remaining_df[remaining_df["Short_name"].str.contains("_ZQ_")]
#         # print(remaining_df)

#         result_df = pd.concat([ericsson_df, remaining_df], axis=0)

#         # print("result_df",result_df)

        
#         all_data_df = result_df.to_json(orient="records")
#         all_data = json.loads(all_data_df)

#         pivot_delta_df = new_dataframe.pivot_table(
#             index="Circle", columns="del_value", values="delta", aggfunc="count"
#         )


#         if ("", "P4") in pivot_delta_df.columns:
#             pivot_delta_df.drop(columns=[("", "P4")], inplace=True)

#         if ("", "P3") in pivot_delta_df.columns:
#             pivot_delta_df.drop(columns=[("", "P3")], inplace=True)

#         pivot_delta_df["total"] = pivot_delta_df.sum(axis=1)
#         new_total = pivot_delta_df.sum().rename("new_total")
#         pivot_delta_df = pivot_delta_df._append(new_total)

#         pivot_delta_df.columns = [
#             "_".join(filter(None, col)).strip() for col in pivot_delta_df.columns
#         ]
#         new_data = pivot_delta_df.reset_index()

#         new_columns = ["Circle"] + [col for col in new_data.columns if col != "Circle"]
#         new_data.columns = new_columns
#         # new_data.drop(columns=['P3'], inplace=True)
#         json_data = new_data.to_json(orient="records")
#         new_json = json.loads(json_data)

#         return Response(
#             {
#                 "status": True,
#                 "message": "Data successfully fetched",
#                 "latest_date": latest_date,
#                 "previous_date": previous_date,
#                 "data": new_json,
#                 "all_data": all_data,
#             }
#         )
#     except Exception as e:
#         return Response({"status": False, "message": str(e)})


@api_view(["POST"])
def hyperlink_Date_wise_dashboard_payload_dip(request):
    circle = request.POST.get("circle")
    del_value = request.POST.get("del_value")

    print(circle)
    print(del_value)

    objs = Daily_4G_KPI.objects.all()
    objs = objs.values()
    latest_date = objs.aggregate(latest_date=Max("Date"))["latest_date"]

    current_date = latest_date.strftime("%Y-%m-%d")
    previous_date = (latest_date - timedelta(days=1)).strftime("%Y-%m-%d")

    objs_new = objs.filter(Date__in=[current_date, previous_date])
    df = pd.DataFrame(list(objs_new.values()))

    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")

    kpi = [
        "MV_4G_Data_Volume_GB",
        "MV_Radio_NW_Availability",
    ]

    for col in kpi:
        df[col] = df[col].astype(float)

    df_pivot = pd.pivot_table(
        df,
        index="Short_name",
        columns="Date",
        values=kpi,
        aggfunc="mean",
        fill_value=0,
    )

    df_pivot.drop(columns=[("MV_Radio_NW_Availability", previous_date)], inplace=True)

    df_pivot[("delta", "")] = (
        df_pivot[("MV_4G_Data_Volume_GB", previous_date)]
        - df_pivot[("MV_4G_Data_Volume_GB", current_date)]
    )
    conditions = [
        (df_pivot[("delta", "")] >= 100),
        (df_pivot[("delta", "")] >= 50) & (df_pivot[("delta", "")] < 100),
        (df_pivot[("delta", "")] >= 30) & (df_pivot[("delta", "")] < 50),
        (df_pivot[("delta", "")] >= 10) & (df_pivot[("delta", "")] < 30),
        (df_pivot[("delta", "")] < 10),
    ]
    choices = ["P0", "P1", "P2", "P3", "P4"]
    df_pivot[("del_value", "")] = np.select(conditions, choices, default="P4")

    df_pivot.reset_index(inplace=True)
    df_pivot["Circle"] = df_pivot["Short_name"].apply(get_circle)

    new_columns = [df_pivot.columns.to_list()[-1]] + [
        col for col in df_pivot.columns if col != ("Circle", "")
    ]

    df_pivot = df_pivot[new_columns]

    df_pivot.columns = [f"{col[0]}_{col[1]}".strip("_") for col in df_pivot.columns]

    df_pivot = df_pivot.rename(
        columns={
            f"{kpi[0]}_{current_date}": f"{kpi[0]}_current_date",
            f"{kpi[0]}_{previous_date}": f"{kpi[0]}_previous_date",
            f"{kpi[1]}_{current_date}": f"{kpi[1]}_current_date",
        }
    )

    df_pivot = df_pivot[
        (df_pivot["Circle"] == circle) & (df_pivot["del_value"] == del_value)
    ]
    json_data = df_pivot.to_json(orient="records")
    new_json = json.loads(json_data)

    return Response(
        {
            "status": True,
            "message": "Hyperlink data",
            "current_date": current_date,
            "previous_date": previous_date,
            "data": new_json,
        }
    )


circle_spoc_dict = {
    "AP": {
        "Name": "Ummalaneni Sai Teja", 
        "Email": "saiteja.u@mcpsinc.com",
        "l2_management_email": "krishna.kantverma@ust.com",
        "l3_management_email": "nilesh.jain@ust.com",
        "l4_management_email": "saurabh.rathore@ust.com",
    },
    "BH": {
        "Name": "Sonu Kumar Singh", 
        "Email": "sonu.kumar1@mcpsinc.com",
        "l2_management_email": "krishna.kantverma@ust.com",
        "l3_management_email": "nilesh.jain@ust.com",
        "l4_management_email": "saurabh.rathore@ust.com",
    },
    "CH": {
        "Name": "Baratheeswaran Arugakeerthi / Shubham Gupta", 
        "Email": "Baratheeswaran.Arugakeerthi@ust.com",
        "l2_management_email": "krishna.kantverma@ust.com",
        "l3_management_email": "nilesh.jain@ust.com",
        "l4_management_email": "saurabh.rathore@ust.com",
    },
    "DL": {
        "Name": "Nishant Kumar Sharma", 
        "Email": "nishant.kumar@mcpsinc.com",
        "l2_management_email": "krishna.kantverma@ust.com",
        "l3_management_email": "nilesh.jain@ust.com",
        "l4_management_email": "saurabh.rathore@ust.com",
    },
    "WB": {
        "Name": "Masud Rana", 
        "Email": "masud.rana@mcpsinc.com",
        "l2_management_email": "krishna.kantverma@ust.com",
        "l3_management_email": "nilesh.jain@ust.com",
        "l4_management_email": "saurabh.rathore@ust.com",
    },
    "HR": {
        "Name": "Tarun Rakecha", 
        "Email": "tarun.rakecha@mcpsinc.com;Shivam.Pandey@ust.com",
        "l2_management_email": "krishna.kantverma@ust.com",
        "l3_management_email": "nilesh.jain@ust.com",
        "l4_management_email": "saurabh.rathore@ust.com",
    },
    "JH": {
        "Name": "Avnish Kumar Mishra", 
        "Email": "avnish.mishra@mcpsinc.com",
        "l2_management_email": "krishna.kantverma@ust.com",
        "l3_management_email": "nilesh.jain@ust.com",
        "l4_management_email": "saurabh.rathore@ust.com",
    },
    "JK": {
        "Name": "Rohit Bansal", 
        "Email": "Rohit.Bansal@mcpsinc.com",
        "l2_management_email": "krishna.kantverma@ust.com",
        "l3_management_email": "nilesh.jain@ust.com",
        "l4_management_email": "saurabh.rathore@ust.com",
    },
    "KK": {
        "Name": "Karamalla Khader Valli", 
        "Email": "Khader.valli@mcpsinc.com",
        "l2_management_email": "krishna.kantverma@ust.com",
        "l3_management_email": "nilesh.jain@ust.com",
        "l4_management_email": "saurabh.rathore@ust.com",
    },
    "MH": {
        "Name": "",
        "Email": "",
        "l2_management_email": "krishna.kantverma@ust.com",
        "l3_management_email": "nilesh.jain@ust.com",
        "l4_management_email": "saurabh.rathore@ust.com",
    },
    "UW": {
        "Name": "Rajan Agarwal / Shubham Gupta", 
        "Email": "rajan.agarwal@mcpsinc.com;shubham.gupta@mcpsinc.com",
        "l2_management_email": "krishna.kantverma@ust.com",
        "l3_management_email": "nilesh.jain@ust.com",
        "l4_management_email": "saurabh.rathore@ust.com",
    },
    "MP": {
        "Name": "Shashikant Jaiswal", 
        "Email": "shashikant.Jaiswal@mcpsinc.com",
        "l2_management_email": "krishna.kantverma@ust.com",
        "l3_management_email": "nilesh.jain@ust.com",
        "l4_management_email": "saurabh.rathore@ust.com",
    },
    "MU": {
        "Name": "Bharat Bhagwan Kamble/Aman Kumar Kashyap", 
        "Email": "bharat.kamble@mcpsinc.com;aman.kashyap@mcpsinc.com",
        "l2_management_email": "krishna.kantverma@ust.com",
        "l3_management_email": "nilesh.jain@ust.com",
        "l4_management_email": "saurabh.rathore@ust.com",
    },
    "OD": {
        "Name": "Manish Chobisa", 
        "Email": "manish.chobisa@mcpsinc.com",
        "l2_management_email": "krishna.kantverma@ust.com",
        "l3_management_email": "nilesh.jain@ust.com",
        "l4_management_email": "saurabh.rathore@ust.com",
    },
    "PB": {
        "Name": "Devesh Pant / Manoj Kumar", 
        "Email": "devesh.pant@mcpsinc.com;manoj.k2@mcpsinc.com",
        "l2_management_email": "krishna.kantverma@ust.com",
        "l3_management_email": "nilesh.jain@ust.com",
        "l4_management_email": "saurabh.rathore@ust.com",
    },
    "UPE": {
        "Name": "Rakesh Kumar Dubey / Manish Singh", 
        "Email": "rakesh.dubey@mcpsinc.com;Manish.KumarSingh@ust.com",
        "l2_management_email": "krishna.kantverma@ust.com",
        "l3_management_email": "nilesh.jain@ust.com",
        "l4_management_email": "saurabh.rathore@ust.com",
    },
    "RJ": {
        "Name": "Rohit Bansal", 
        "Email": "Rohit.Bansal@mcpsinc.com",
        "l2_management_email": "krishna.kantverma@ust.com",
        "l3_management_email": "nilesh.jain@ust.com",
        "l4_management_email": "saurabh.rathore@ust.com",
    },
    "KO": {
        "Name": "Masud Rana", 
        "Email": "masud.rana@mcpsinc.com",
        "l2_management_email": "krishna.kantverma@ust.com",
        "l3_management_email": "nilesh.jain@ust.com",
        "l4_management_email": "saurabh.rathore@ust.com",
    },
    "TN": {
        "Name": "Baratheeswaran Arugakeerthi / Shubham Gupta / Prakash", 
        "Email": "Baratheeswaran.Arugakeerthi@ust.com;Prakashpandi.T@ust.com",
        "l2_management_email": "krishna.kantverma@ust.com",
        "l3_management_email": "nilesh.jain@ust.com",
        "l4_management_email": "saurabh.rathore@ust.com",
    },
    "UE": {
        "Name": "Rakesh Kumar Dubey / Manish Singh", 
        "Email": "rakesh.dubey@mcpsinc.com;Manish.KumarSingh@ust.com",
        "l2_management_email": "krishna.kantverma@ust.com",
        "l3_management_email": "nilesh.jain@ust.com",
        "l4_management_email": "saurabh.rathore@ust.com",
    },
}




# def get_ticket_status_by_date(request, Date):
#     try:
#         try:
#             date = datetime.strptime(Date, "%Y-%m-%d").date()
#         except ValueError:
#             return Response(
#                 {"error": "Invalid date format. Use YYYY-MM-DD."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         latest_date = date
#         previous_date = latest_date - timedelta(1)
#         objs = Daily_4G_KPI.objects.filter(Date__in=[latest_date, previous_date])

#         if not objs.exists():
#             return Response({"status": False, "message": "No data available"})

#         df = cleaned_data(pd.DataFrame(list(objs.values())))
#         df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")

#         kpi = ["MV_4G_Data_Volume_GB", "MV_Radio_NW_Availability"]
#         df[kpi] = df[kpi].astype(float)

#         df_pivot = pd.pivot_table(
#             df,
#             index="Short_name",
#             columns="Date",
#             values=kpi,
#             aggfunc="mean",
#             fill_value=0,
#         )
#         previous_date = (date - timedelta(days=1)).strftime("%Y-%m-%d")
#         current_date = date.strftime("%Y-%m-%d")
#         df_pivot.drop(
#             columns=[("MV_Radio_NW_Availability", previous_date)], inplace=True
#         )

#         df_pivot["delta"] = (
#             df_pivot[("MV_4G_Data_Volume_GB", previous_date)]
#             - df_pivot[("MV_4G_Data_Volume_GB", current_date)]
#         )

#         conditions = [
#             (df_pivot["delta"] >= 100),
#             (df_pivot["delta"] >= 50) & (df_pivot["delta"] < 100),
#             (df_pivot["delta"] >= 30) & (df_pivot["delta"] < 50),
#             (df_pivot["delta"] >= 10) & (df_pivot["delta"] < 30),
#             (df_pivot["delta"] < 10),
#         ]
#         choices = ["P0", "P1", "P2", "P3", "P4"]
#         df_pivot["del_value"] = np.select(conditions, choices, default="P4")
#         df_pivot.reset_index(inplace=True)
#         df_pivot[("Circle", "")] = df_pivot[("Short_name", "")].apply(get_circle)

#         circle_column = df_pivot.pop(("Circle", ""))
#         df_pivot.insert(0, ("Circle", ""), circle_column)

#         df_pivot.columns = [f"{col[0]} {col[1]}" for col in df_pivot.columns]
#         df_pivot.reset_index(drop=True, inplace=True)
#         df_pivot.columns = df_pivot.columns.str.strip()

#         df_pivot = df_pivot.rename(
#             columns={
#                 f"MV_4G_Data_Volume_GB {current_date}": "MV_4G_Data_Volume_GB_current_date",
#                 f"MV_4G_Data_Volume_GB {previous_date}": "MV_4G_Data_Volume_GB_previous_date",
#                 f"MV_Radio_NW_Availability {current_date}": "MV_Radio_NW_Availability_current_date",
#             }
#         )

#         df_pivot = df_pivot[df_pivot["MV_Radio_NW_Availability_current_date"] >= 50]

#         data_df_new = df_pivot[df_pivot["del_value"].isin(["P0", "P1", "P2"])]
#         all_data_df = data_df_new.to_json(orient="records")
#         all_data = json.loads(all_data_df)

#         new_df_pivot = df_pivot.pivot_table(
#             index="Circle",
#             columns="del_value",
#             values="delta",
#             aggfunc="count",
#             fill_value=0,
#         ).reset_index()

#         for col in ["P0", "P1"]:
#             if col not in new_df_pivot.columns:
#                 new_df_pivot[col] = 0

#         new_df_pivot.drop(columns=["P3", "P4"], inplace=True)
#         new_df_pivot["total"] = new_df_pivot.sum(axis=1)

#         new_total = {
#             "Circle": "new_total",
#             "P0": new_df_pivot["P0"].sum(),
#             "P1": new_df_pivot["P1"].sum(),
#             "P2": new_df_pivot["P2"].sum(),
#             "total": new_df_pivot["total"].sum(),
#         }
#         new_total_df = pd.DataFrame([new_total])
#         new_df_pivot = pd.concat([new_df_pivot, new_total_df], ignore_index=True)

#         json_data = new_df_pivot.to_json(orient="records")
#         new_json = json.loads(json_data)

#         return Response(
#             {
#                 "status": True,
#                 "message": "Data successfully fetched",
#                 "latest_date": current_date,
#                 "previous_date": previous_date,
#                 "data": new_json,
#                 "all_data": all_data,
#             }
#         )
#     except Exception as e:
#         return Response({"status": False, "message": str(e)})
def creating_ticket_for_sleeping_cells():
    objs = Daily_4G_KPI.objects.all()

    latest_date = objs.aggregate(latest_date=Max("Date"))
    print(latest_date)

    latest_date = latest_date["latest_date"]
    objs= objs.filter(Date=latest_date)
    df = pd.DataFrame(list(objs.values()))

    print(df)

    new_df = df[
            (df[f"MV_4G_Data_Volume_GB"] == 0)
            & (df[f"MV_Radio_NW_Availability"] >= 90)
        ]
    new_df["Circle"] = (
        new_df["Short_name"].apply(lambda x: str(x).strip()).apply(get_circle)
    )
    print(new_df)

    for _, row in new_df.iterrows():
        short_name = row["Short_name"] if row["Short_name"] is not None else ""

        pre_exist_data = Ticket_Counter_Table_Data.objects.filter(Short_name=short_name).first()
        if pre_exist_data and pre_exist_data.Status == 'CLOSE':
            with transaction.atomic():
                try:
                    ticket_counter = Ticket_Counter_Table_Data.objects.create(
                        Short_name=short_name,
                        Site_ID=row.get("Site ID", "") if row.get("Site ID") is not None else "",
                        Status=row["Status"] if row["Status"] is not None else "",
                        Remarks=" ",
                        Ownership=row.get("Ownership", "") if row.get("Ownership") is not None else "",
                        priority=row["del_value"] if row["del_value"] is not None else "",
                        Circle_Spoc=circle_spoc_dict.get(row["Circle"], {}).get("Name") if row["Circle"] is not None else "",
                        auto_rca= "",
                        proposed_solution= "",
                        ticket_type="Sleeping Cell",
                        Date=row["Date"]
                    )
                    print(f"Created new ticket for Short_name: {short_name} as the previous ticket was CLOSE")
                except IntegrityError:
                    continue
        else:
            with transaction.atomic():
                try:
                    ticket_counter, created = Ticket_Counter_Table_Data.objects.update_or_create(
                        Short_name=short_name,
                        Site_ID=(
                            row.get("Site ID", "")
                            if row.get("Site ID") is not None
                            else ""
                        ),
                        defaults={
                            "Status": "OPEN",
                            "Remarks": " ",
                            "Ownership": (
                                row.get("Ownership", "")
                                if row.get("Ownership") is not None
                                else ""
                            ),
                            "priority": "P0",
                            "Circle_Spoc": (
                                circle_spoc_dict.get(row["Circle"], {}).get("Name")
                                if row["Circle"] is not None
                                else ""
                            ),
                            "auto_rca": "",
                            "proposed_solution": "",
                            "ticket_type": "Sleeping Cell",
                        },
                    )
                except IntegrityError:
                    continue

                if created:
                    print(f"Created new record for Short_name: {short_name}")
                else:
                    print(f"Updated existing record for Short_name: {short_name}")


def ticket_counter_upload_report():
    factory = APIRequestFactory()

    get_ticket_api = factory.get(reverse("ticket_counter_api"))
    get_response_from_ticlet = ticket_counter_api(get_ticket_api)

    if get_response_from_ticlet.status_code != 200:
        return Response({"error": "Failed to fetch data from the first API"}, status=500)

    try:
        logger.info("Sending request to get_data_from_url")
        get_rca_api = factory.get(reverse("get_data_from_url"))
        response_rca_api = get_data_from_url(get_rca_api)

        if response_rca_api.status_code == 200:
            response_data = response_rca_api.data.get("resposne_data", [])
            rca_df = pd.DataFrame(response_data)
            if rca_df.empty:
                logger.warning("Received an empty response for 'resposne_data'.")
        else:
            logger.error(f"Failed API call. Status code: {response_rca_api.status_code}")
            rca_df = pd.DataFrame()
    except Exception as e:
        logger.exception(f"An unexpected error occurred while calling RCA API: {e}")
        rca_df = pd.DataFrame()

    ticket_df = pd.DataFrame(get_response_from_ticlet.data.get("all_data"))
    ticket_df["Site ID"] = ticket_df["Short_name"].apply(lambda x: get_site_id(x))

    latest_date = get_response_from_ticlet.data.get("latest_date")
    previous_date = get_response_from_ticlet.data.get("previous_date")

    ticket_df["Status"] = ticket_df["Short_name"].apply(lambda x: "OPEN")
    ticket_df["Date"] = ticket_df["Short_name"].apply(lambda x: latest_date)

    date_val = latest_date if latest_date else None
    if date_val is None:
        return Response({"error": "No valid dates found in the file"}, status=400)

    if isinstance(latest_date, np.datetime64):
        latest_date = pd.to_datetime(latest_date).strftime("%Y-%m-%d")
    if isinstance(previous_date, np.datetime64):
        previous_date = pd.to_datetime(previous_date).strftime("%Y-%m-%d")

    if not rca_df.empty:
        rca_df.rename(columns={"Cell_name": "Short_name", "date": "Date"}, inplace=True)
        rca_df_subset = rca_df[["Short_name", "Date", "RCA", "Proposed_Solution"]]

        merged_df = ticket_df.merge(
            rca_df_subset,
            right_on="Short_name",
            left_on="Short_name",
            how="left",
            indicator=False,
        )

        merged_df.rename(
            columns={
                "RCA_x": "RCA",
                "Proposed_Solution_x": "Proposed_Solution",
                "Date_x": "Date",
            },
            inplace=True,
        )
    else:
        merged_df = ticket_df
        merged_df["RCA"] = ""
        merged_df["Proposed_Solution"] = ""

    merged_df = merged_df[
        [
            "Circle",
            "Short_name",
            "Site ID",
            "Date",
            "Status",
            "RCA",
            "Proposed_Solution",
            "del_value",
        ]
    ]

    for _, row in merged_df.iterrows():
        short_name = row["Short_name"] if row["Short_name"] is not None else ""                          
        pre_exist_data = Ticket_Counter_Table_Data.objects.filter(Short_name = short_name).first()
        if pre_exist_data and pre_exist_data.Status == 'CLOSE':
            with transaction.atomic():
                try:
                    ticket_counter = Ticket_Counter_Table_Data.objects.create(
                        Short_name=short_name,
                        Site_ID=row.get("Site ID", "") if row.get("Site ID") is not None else "",
                        Status=row["Status"] if row["Status"] is not None else "",
                        Remarks=" ",
                        Ownership=row.get("Ownership", "") if row.get("Ownership") is not None else "",
                        priority=row["del_value"] if row["del_value"] is not None else "",
                        Circle_Spoc=circle_spoc_dict.get(row["Circle"], {}).get("Name") if row["Circle"] is not None else "",
                        auto_rca=row["RCA"] if row["RCA"] is not None else "",
                        proposed_solution=row["Proposed_Solution"],
                        ticket_type="Payload",
                        Date=row["Date"]
                    )
                    print(f"Created new ticket for Short_name: {short_name} as the previous ticket was CLOSE")
                except IntegrityError:
                    continue
        else:
            with transaction.atomic():
                try:
                    ticket_counter, created = Ticket_Counter_Table_Data.objects.update_or_create(
                        Short_name=short_name,
                        Site_ID=(
                            row.get("Site ID", "")
                            if row.get("Site ID") is not None
                            else ""
                        ),
                        defaults={
                            "Status": row["Status"] if row["Status"] is not None else "",
                            "Remarks": " ",
                            "Ownership": (
                                row.get("Ownership", "")
                                if row.get("Ownership") is not None
                                else ""
                            ),
                            "priority": row["del_value"] if row["del_value"] is not None else "",
                            "Circle_Spoc": (
                                circle_spoc_dict.get(row["Circle"], {}).get("Name")
                                if row["Circle"] is not None
                                else ""
                            ),
                            "auto_rca": row["RCA"] if row["RCA"] is not None else "",
                            "proposed_solution": row["Proposed_Solution"],
                            "ticket_type": "Payload"
                        },
                    )
                except IntegrityError:
                    continue

            if created:
                print(f"Created new record for Short_name: {short_name}")
            else:
                print(f"Updated existing record for Short_name: {short_name}")
                
    creating_ticket_for_sleeping_cells()
    
    objs = Ticket_Counter_Table_Data.objects.filter(Date=latest_date)
    
    serializer = ser_Ticket_Counter(objs, many=True)

    return serializer.data





def convert_unix_to_date(timestamp_ms):
    """ Convert Unix timestamp in milliseconds to a readable date format. """
    timestamp_s = timestamp_ms / 1000
    return datetime.utcfromtimestamp(timestamp_s).strftime('%Y-%m-%d')

def format_dates(obj):
    """ Recursively format date values in a JSON-like object. """
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, int) and (key.lower().endswith('date') or key.lower().endswith('timestamp')):
                obj[key] = convert_unix_to_date(value)
            else:
                # Recursively format nested dictionaries and lists
                format_dates(value)
    elif isinstance(obj, list):
        for index, item in enumerate(obj):
            obj[index] = format_dates(item)
    return obj


def update_aging_count():

    objs = Ticket_Counter_Table_Data.objects.filter(Status = 'OPEN')

    for obj in objs:
        obj.Date = datetime.now().date()
        # obj.aging = datetime.now().date() - obj.Open_Date
        obj.save()


@api_view(["GET"])
def get_ticket_status_data(request):
    """
    Fetch ticket status data and integrate it with RCA API data.
    """
    
    factory = APIRequestFactory()
    logger.info("Entering get_ticket_status_data function")

    # Fetch the latest date from Daily_4G_KPI model
    latest_date = Daily_4G_KPI.objects.all().aggregate(latest_date=Max("Date"))[
        "latest_date"
    ]
    logger.debug(f"Latest date fetched: {latest_date}")

    # Fetch data for the latest date from Ticket_Counter_Table_Data model
    data = Ticket_Counter_Table_Data.objects.filter(Open_Date=latest_date + timedelta(1))
    logger.debug(f"Data exists for latest date: {data.exists()}")

    rca_table_data = RCA_output_table.objects.filter(date = latest_date)


    if not data.exists() and rca_table_data.exists():
        print("baar baar yaha mat aana............")
        logger.info("Processing ticket_counter_upload_report due to missing data.")
        update_aging_count()
        json_data = ticket_counter_upload_report()
        instance = Ticket_Counter_Table_Data.objects.filter(Open_Date=latest_date + timedelta(1))
        new_df = pd.DataFrame(instance.values())

        logger.debug(f"New DataFrame columns: {new_df.columns}")
        send_email_spoc_circle(new_df, circle_spoc_dict)

        # return Response(
        #     {
        #         "Status": True,
        #         "message": "Data fetched and uploaded successfully",
        #         "data": json_data,
        #     }
        # )

    # Fetch ticket counter API data and integrate with RCA data
    try:
        logger.info("Sending request to ticket_counter_api")
        request_for_first_api = factory.get(reverse("ticket_counter_api"))
        response_from_first_api = ticket_counter_api(request_for_first_api)



        if response_from_first_api.status_code == 200:
            logger.info("Successfully received response from ticket_counter_api")
            latest_date = response_from_first_api.data.get("latest_date")
            previous_date = response_from_first_api.data.get("previous_date")
            last_updated_date = Ticket_Counter_Table_Data.objects.latest("Date").Date
            logger.debug(
                f"Latest date: {latest_date}, Previous date: {previous_date}, Last updated date: {last_updated_date}"
            )

            objs = Ticket_Counter_Table_Data.objects.all().order_by("-Open_Date")

            if not objs.exists():
                logger.info(
                    "No records found for the latest date, using last updated date"
                )
                # objs = Ticket_Counter_Table_Data.objects.filter(
                #     Q(Status = "OPEN")
                # ).order_by("-Open_Date")

            new_data_df = pd.DataFrame(objs.values())

            print(new_data_df.columns)
            new_data_df.rename(
                columns={"auto_rca": "RCA", "proposed_solution": "Proposed Solution"},
                inplace=True,
            )
            print(new_data_df)

            new_data_df.fillna("", inplace=True)
            new_data_df_dict = json.loads(new_data_df.to_json(orient="records"))
            return Response(
                {
                    "Status": True,
                    "message": "Successfully retrieved the data",
                    "data": new_data_df_dict,
                }
            )
        else:
            logger.error(
                f"Failed to fetch data from ticket_counter_api. Status code: {response_from_first_api.status_code}"
            )
            return Response(
                {
                    "Status": False,
                    "message": "Failed to fetch data from ticket_counter_api",
                    "error": response_from_first_api.data,
                },
                status=response_from_first_api.status_code,
            )
    except Exception as e:
        logger.exception(
            f"An error occurred while processing ticket_counter_api data: {e}"
        )
        return Response(
            {"Status": False, "message": "An error occurred", "error": str(e)},
            status=500,
        )


# @api_view(["GET"])
# def get_ticket_status_data(request):
#     print("Entering get_ticket_status_data function")
#     latest_date = Daily_4G_KPI.objects.all().aggregate(latest_date=Max("Date"))[
#         "latest_date"
#     ]
#     print(f"latest_date: {latest_date}")
#     data = Ticket_Counter_Table_Data.objects.all().filter(Date=latest_date)
#     print(f"data exists: {data.exists()}")

#     if not data.exists():
#         print("baar baar yaha mat aana......")
#         ticket_counter_upload_report(request)

#     factory = APIRequestFactory()
#     try:
#         print("Sending request to ticket_counter_api")
#         request_for_first_api = factory.get(reverse("ticket_counter_api"))
#         response_from_first_api = ticket_counter_api(request_for_first_api)

#         print("Sending request to get_data_from_url")
#         get_rca_api = factory.get(reverse("get_data_from_url"))
#         response_rca_api = get_data_from_url(get_rca_api)

#         rca_df = (
#             pd.DataFrame(response_rca_api.data.get("resposne_data"))
#             if response_rca_api.status_code == 200
#             else pd.DataFrame()
#         )

#         if response_from_first_api.status_code == 200:
#             print("Successfully received response from ticket_counter_api")
#             latest_date = response_from_first_api.data.get("latest_date")
#             previous_date = response_from_first_api.data.get("previous_date")
#             last_updated_date = Ticket_Counter_Table_Data.objects.latest("Date").Date
#             print(f"latest_date: {latest_date}")
#             print(f"previous_date: {previous_date}")
#             print(f"last_updated_date: {last_updated_date}")

#             objs = Ticket_Counter_Table_Data.objects.filter(
#                 Q(Date=latest_date)
#             ).annotate(Date_only=TruncDate("Date"))

#             if not objs.exists():
#                 print("No records found for latest date, trying previous date")
#                 objs = Ticket_Counter_Table_Data.objects.filter(
#                     Q(Date=last_updated_date)
#                 ).annotate(Date_only=TruncDate("Date"))

#             new_data_df = pd.DataFrame(objs.values())
#             print(f"new_data_df shape: {new_data_df.shape}")
#             print(f"rca_df shape: {rca_df.shape}")

#             if not new_data_df.empty and not rca_df.empty:
#                 print("Merging new_data_df with rca_df")
#                 new_data_df = new_data_df.merge(
#                     rca_df, left_on="Short_name", right_on="Cell_name", how="left"
#                 )
#                 new_data_df.drop(columns=["Cell_name"], inplace=True)
#                 print(f"new_data_df shape after merge: {new_data_df.shape}")

#             new_data_df.fillna("", inplace=True)  # Handle None values globally

#             print(new_data_df["Date"])
#             print(rca_df.columns)

#             new_data_df_dict = new_data_df.to_json(orient="records")
#             new_data_df_dict = json.loads(new_data_df_dict)

#             return Response(
#                 {
#                     "Status": True,
#                     "message": "Successfully retrieved the data",
#                     "data": new_data_df_dict,
#                 }
#             )
#         else:
#             print("Failed to fetch data from the previous API")
#             return Response(
#                 {
#                     "Status": False,
#                     "message": "Failed to fetch data from the previous API",
#                     "error": response_from_first_api.data,
#                 },
#                 status=response_from_first_api.status_code,
#             )

#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return Response(
#             {"Status": False, "message": "An error occurred", "error": str(e)},
#             status=500,
#         )




@api_view(["POST"])
def ticket_status_open_close_all(request):

    ticket_id = request.data.get("ticket_id")
    if not ticket_id:
        return Response(
            {"Status": False, "message": "ticket_id is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    tickets = Ticket_Counter_Table_Data.objects.filter(ticket_id=ticket_id).order_by(
        "ticket_id"
    )
    if tickets.exists():
        serializer = ser_Ticket_Counter(tickets, many=True)
        return Response(
            {
                "Status": True,
                "message": "Successfully fetched the data",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    return Response(
        {"Status": False, "message": "Invalid ticket_id provided"},
        status=status.HTTP_404_NOT_FOUND,
    )


# @api_view(["POST"])
# def ticket_status_open_close(request, ticket_id):
#     required_fields = [
#         "ticket_id",
#         "status",
#         "circle",
#         "short_name",
#         "remarks",
#         "pre_remarks",
#         "ownership",
#         "circle_spoc",
#         "aging",
#         "date",
#         "open_date",
#         "site_id",
#     ]
#     for field in required_fields:
#         if field not in request.data:
#             return Response(
#                 {"Status": False, "message": f"{field} is required"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#     try:
#         ticket = Ticket_Counter_Table_Data.objects.get(ticket_id=ticket_id)
#     except Ticket_Counter_Table_Data.DoesNotExist:
#         return Response(
#             {"Status": False, "message": "Invalid ticket_id provided"},
#             status=status.HTTP_404_NOT_FOUND,
#         )

#     ticket.Status = request.POST.get("status")
#     ticket.Circle = request.POST.get("circle")
#     ticket.Short_name = request.POST.get("short_name")
#     ticket.Remarks = request.POST.get("remarks")
#     ticket.Pre_Remarks = request.POST.get("pre_remarks")
#     ticket.Ownership = request.POST.get("ownership")
#     ticket.Circle_Spoc = request.POST.get("circle_spoc")
#     ticket.Site_ID = request.POST.get("site_id")

#     date_str = request.POST.get("date")
#     open_date_str = request.POST.get("open_date")

#     if date_str:
#         try:
#             ticket.Date = datetime.strptime(date_str, "%Y-%m-%d")
#         except ValueError:
#             return Response(
#                 {
#                     "Status": False,
#                     "message": "Invalid date format, should be YYYY-MM-DD",
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#     if open_date_str:
#         try:
#             ticket.Open_Date = datetime.strptime(open_date_str, "%Y-%m-%d")
#         except ValueError:
#             return Response(
#                 {
#                     "Status": False,
#                     "message": "Invalid open_date format, should be YYYY-MM-DD",
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#     if ticket.Status == "Open":
#         ticket.aging = (datetime.now().date() - ticket.Open_Date).days

#     ticket.save()
#     return Response(
#         {"Status": True, "message": "Successfully updated the data"},
#         status=status.HTTP_200_OK,
#     )


@api_view(["POST"])
def ticket_status_open_close(request, ticket_id):
    print(f"Request Data: {request.data}")
    try:
        # Fetch the instance by ticket_id
        instance = Ticket_Counter_Table_Data.objects.get(ticket_id=ticket_id)
        print(f"Ticket ID: {instance.ticket_id}, Short Name: {instance.Short_name}")

        
        for date_field in ['Date', 'Open_Date']:
            if date_field in request.data:
                request.data[date_field] = datetime.utcfromtimestamp(
                    int(request.data[date_field]) / 1000
                ).strftime('%Y-%m-%d')
        
  
        remarks = request.data.get("Remarks", "")
        pre_remarks = request.data.get("Pre_Remarks", "")
        print(pre_remarks)
        previous_remarks = {"date": f"{datetime.now()}", "Remark": remarks}
        if not instance.Pre_Remarks:
            instance.Pre_Remarks = []
        pre_remarks.append(previous_remarks)

        pre_remarks.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S.%f' if ' ' in x['date'] else '%Y-%m-%d'), reverse=True)

        instance.Pre_Remarks = pre_remarks
        instance.save()


    except Ticket_Counter_Table_Data.DoesNotExist:
        return Response(
            {"error": f"Object with ticket_id '{ticket_id}' not found."},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    try:
        serializer = ser_Ticket_Counter(instance, data=request.data, partial=True)
        print(f"Serializer Initial Data: {serializer.initial_data}")
        if serializer.is_valid():

            serializer.save()

            instance.updated_by = request.user.username
            instance.save()
            print(f"Serializer Data After Save: {serializer.data}")
            response_data = dict(serializer.data)

            if "Pre_Remarks" in response_data.keys():
                for remark in response_data["Pre_Remarks"]:
                    remark["date"] = str(remark['date'])[:19]
            
            
            
            return Response(
                {
                    **response_data,  
                    # "previous_remarks": previous_remarks, 
                },
                status=status.HTTP_200_OK,
            )

        print(f"Serializer Errors: {serializer.errors}")
        return Response(
            {
                "message": "Validation failed",
                "message": serializer.errors,  # Detailed error information
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    except ValidationError as ve:
        return Response(
            {"message": "Validation error occurred", "details": str(ve)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        return Response(
            {"message": "An unexpected error occurred", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )



from datetime import date
@api_view(["POST", "GET"])
def circle_wise_open_close_dashboard(request):
    print(request.POST)
    ticket_type = request.POST.get("ticket_type")
    # ticket_type ="Payload"
    start_date =date(2025,1 , 1)
    objs = Ticket_Counter_Table_Data.objects.filter(Open_Date__gte=start_date)
    if ticket_type == "Sleeping Cell":
        objs = objs.filter(ticket_type="Sleeping Cell")
        MAX_DATE = objs.aggregate(Max("Open_Date"))["Open_Date__max"]
        MIN_DATE = objs.aggregate(Min("Open_Date"))["Open_Date__min"]
        
        print("MAX_DATE: ",MAX_DATE)
        print("MIN_DATE: ",MIN_DATE)
    if ticket_type == "Payload":
        objs = objs.filter(ticket_type="Payload")
        MAX_DATE = objs.aggregate(Max("Open_Date"))["Open_Date__max"]
        MIN_DATE = objs.aggregate(Min("Open_Date"))["Open_Date__min"]
        

        

        print("MAX_DATE: ",MAX_DATE)
        print("MIN_DATE: ",MIN_DATE)

    unique_circle = list(objs.values_list("Circle", flat=True).distinct())

    circle = request.POST.get("circle")

    latest_date = Ticket_Counter_Table_Data.objects.aggregate(latest_date=Max("Date"))[
        "latest_date"
    ]

    from_date = request.POST.get("from_date")
    to_date = request.POST.get("to_date")
    priority = request.POST.get("priority") 



        
    # ageing = request.POST.get("bucket")


    max_ageing_fe =request.POST.get("max_ageing")
    min_ageing_fe =request.POST.get("min_ageing")
    if min_ageing_fe ==''and max_ageing_fe == '':
            max_ageing =objs.aggregate(Max("aging"))["aging__max"]
            min_ageing =objs.aggregate(Min("aging"))["aging__min"]
    else:
            max_ageing = max_ageing_fe
            min_ageing = min_ageing_fe


    objs= objs.filter(aging__gte = min_ageing, aging__lte = max_ageing, ticket_type = ticket_type)
    priority_list = priority.split(",") 
    
    if '' in priority_list:
        priority_list = priority_list.remove('')
    # print("Type: ",type(priority_list))
    # print("priority_list len;;;;;",len(priority_list))
    # ageing_list = ageing.split(",")

    print(from_date, to_date, priority, priority_list)

    # priority_val = request.POST.get("priority")
    
    # aging_bucket = request.POST.get("bucket")
    
    counts = {circle: {"OPEN": 0, "CLOSE": 0} for circle in unique_circle}


    if from_date and to_date:
        from_date = datetime.strptime(str(from_date), "%Y-%m-%d").date()
        to_date = datetime.strptime(str(to_date), "%Y-%m-%d").date()

        objs = objs.filter(Open_Date__range=[from_date, to_date])
        
    else:
        from_date = MIN_DATE
        to_date = MAX_DATE
    
    if priority_list :
        print("priority_list:- ", priority_list)
        objs = objs.filter(priority__in = priority_list)
        
    # if aging_bucket and '-' in aging_bucket:
    #     from_bucket, to_bucket = str(aging_bucket).split('-')
    #     objs = objs.filter(aging__range = [int(from_bucket), int(to_bucket)])
    
    # if aging_bucket and  '>' in aging_bucket:
    #     aging_value = int(''.join(str(aging_bucket).split('>')))
    #     print(aging_value)
    #     objs = objs.filter(aging__gt = aging_value)
    
        
    for obj in objs:
        ageing = (latest_date - obj.Open_Date).days
        obj.aging = ageing
        obj.save(latest_date=latest_date)

        status_obj = obj.Status.upper()
        if status_obj in ["OPEN", "CLOSE"]:
            counts[obj.Circle][status_obj] += 1

    result = []
    if circle:
        result.append({circle: counts[circle]})
        filtered_objs = objs.filter(Circle=circle)
    else:
        for circle in unique_circle:
            result.append({circle: counts[circle]})
        filtered_objs = objs

    serializer = ser_Ticket_Counter(filtered_objs.order_by("ticket_id"), many=True)
    print(result)
    return Response(
        {
            "Status": True,
            "message": "Successfully fetched the data",
            "from_date": from_date,
            "to_date": to_date ,
            "result": result,
            "data": serializer.data,
            "max_ageing": max_ageing,
            "min_ageing": min_ageing
        },
        status=status.HTTP_200_OK,
    )


###


@api_view(['POST'])
def get_unique_category(request):
    category_list = [
        'RNA issue',
        'HW issue',
        'Tx issue',
        'Quality alarm',
        'Soft optimization done/Payload shifted within sector',
        'Optimization done as per customer requirements',
        'Optimization done for KPI improvement',
        'Physical optimization planned',
        'New layer /Sector coming in site',
        'New site / Sector come in neighobur',
        'Soft optimization planned'
    ]

    return Response({
        'category' : category_list
    })


@api_view(['POST'])
def get_daily_4g_kpi_report_by_date_and_kpi(request):
    date = request.data.get('date')
    kpi_name = request.data.get('kpi_name')
    
    if date and kpi_name:
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            report = Daily_4G_KPI_REPORT.objects.filter(Date=date_obj, kpi_name=kpi_name)
            serializer = Daily4GKPIReportSerializer(report, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
    elif not date and not kpi_name:
        return Response({'error': 'Date and KPI name are required'}, status=status.HTTP_400_BAD_REQUEST)
    elif not date:
        return Response({'error': 'Date is required'}, status=status.HTTP_400_BAD_REQUEST)
    elif not kpi_name:
        return Response({'error': 'KPI name is required'}, status=status.HTTP_400_BAD_REQUEST)