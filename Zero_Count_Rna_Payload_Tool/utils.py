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
from Zero_Count_Rna_Payload_Tool.models import *
from django.db.models import Min, Max
from django.db.models import Max, F, Subquery, OuterRef
from django.db.models.functions import Coalesce
from django.db import IntegrityError, connection
import pytz
import json
from django.db import connection
from rest_framework.response import Response


def save_database_KPI_4G(df):
    pass


def clean_infinity(value):
    if value == "∞":
        return float("inf")
    elif value == "-∞":
        return float("-inf")
    elif value == "âˆž":
        return float("0")
    return value


def database_Save_Raw_2G(df_2G):
    for i, d in df_2G.iterrows():
        date = None
        if not pd.isnull(d["Unnamed: 1"]):
            date = d["Unnamed: 1"].date()
        obj_2g = Daily_2G_KPI.objects.create(
            Short_name=str(d["Short name"]),
            Date=date,
            Cell_Name=str(d["2G Cell Name"]),
            MV_2G_Site_Name=str(d["MV 2G_Site Name"]),
            Site_Name=str(d["2G Site Name"]),
            CGI_2G=str(d["2G CGI"]),
            OEM_GGSN=str(d["OEM_GGSN"]),
            MV_Total_Voice_Traffic_BBH=str(d["MV_Total Voice Traffic [BBH]"]),
            Network_availability_RNA=str(d["Network availability [RNA]"]),
            MV_of_2G_Cell_with_Network_Availability=str(
                d["MV_% of 2G Cell with Network Availability <98%"]
            ),
        )
