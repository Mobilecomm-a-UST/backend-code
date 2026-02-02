from django.shortcuts import render
from django.db.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
import os
from django.conf import settings
from rest_framework import status
import numpy as np
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
from rest_framework.status import HTTP_200_OK
from .models import NokiaAlarm

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import os

@api_view(['POST'])
def alarmfileUpload(request):
    alarm_files = request.FILES.getlist('alarm_file')
    mapping_file = request.FILES.get('mapping_file')

    if not alarm_files or not mapping_file:
        return Response(
            {'error': 'Both alarm_file and mapping_file are required!'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # --- Read Alarm Files ---
    alarm_dfs = []
    for file in alarm_files:
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file)
            else:
                continue

            df.columns = df.columns.str.strip()
            alarm_dfs.append(df)
            
        except Exception as e:
            return Response(
                {'error': f'Error reading alarm file {file.name}: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    if not alarm_dfs:
        return Response(
            {'error': 'No valid alarm files provided'},
            status=status.HTTP_400_BAD_REQUEST
        )

    df_alarm = pd.concat(alarm_dfs, ignore_index=True)

    # --- Read Mapping File ---
    try:
        if mapping_file.name.endswith('.csv'):
            df_map = pd.read_csv(mapping_file)
        else:
            df_map = pd.read_excel(mapping_file)
        df_map.columns = df_map.columns.str.strip()
    except Exception as e:
        return Response(
            {'error': f'Error reading mapping file: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # --- Ensure MRBTS exists ---
    if "mrbts" not in df_alarm.columns:
        if "Distinguished Name" in df_alarm.columns:
            df_alarm["mrbts"] = (
                df_alarm["Distinguished Name"]
                .astype(str)
                .str.extract(r"MRBTS-(\d+)")
            )
        else:
            df_alarm["mrbts"] = 0

    # --- Keep Required Columns ---
    needed_cols = [
        "mrbts",
        "Supplementary Information",
        "Origin Alarm Time",
        "Origin Alarm Update Time",
        
    ]
    df_alarm = df_alarm[[c for c in needed_cols if c in df_alarm.columns]]

    # --- Type Conversion ---
    df_map["MRBTS"] = pd.to_numeric(df_map["MRBTS"], errors="coerce").fillna(0).astype(int)
    df_alarm["mrbts"] = pd.to_numeric(df_alarm["mrbts"], errors="coerce").fillna(0).astype(int)

    # --- Merge ---
    df_merged = pd.merge(
        df_map,
        df_alarm,
        left_on="MRBTS",
        right_on="mrbts",
        how="left"
    )

    # --- Save Output ---
    output_path = os.path.join(MEDIA_ROOT, "Nokia_Alarm_Mapped.xlsx")
    df_merged.to_excel(output_path, index=False)

    return Response(
        {
            "message": "Alarm files processed successfully",
            "output_file": "Nokia_Alarm_Mapped.xlsx"
        },
        status=status.HTTP_200_OK
    )
