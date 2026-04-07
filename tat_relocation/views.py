from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from alok_tracker.models import *  # noqa: F403
import pandas as pd
from django.db import transaction
import os
from django.conf import settings
from datetime import datetime as dtime
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from django.utils import timezone
import json
from datetime import datetime, timedelta, date
import shutil
from django.db.models import Q
from django.forms.models import model_to_dict
import numpy as np
from rest_framework import status
from .models import TrackerModel

@api_view(['GET'])
def download_tracker_data_view(request):
    try:
        fields = TrackerModel._meta.fields

        # DB column names
        headers = [f.column for f in fields]

        # Data
        data = TrackerModel.objects.values_list(
            *[f.name for f in fields]
        )

        df = pd.DataFrame(list(data), columns=headers)

        file_name = 'tracker_data.xlsx'
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        df.to_excel(file_path, index=False)

        download_link = request.build_absolute_uri(
            settings.MEDIA_URL + file_name
        )

        return Response({
            "message": "Excel file generated successfully",
            "file_name": file_name,
            "download_link": download_link,
            "headers": headers,
        }, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


def parse_date(val):
    if pd.isna(val) or val == "":
        return None
    try:
        return pd.to_datetime(val).date()
    except:
        return None


@api_view(["POST"])
def upload_tracker_data_view(request):
    file = request.FILES.get("file")

    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    try:
        df = pd.read_excel(file)
        df = df.replace({pd.NA: None})

        with transaction.atomic():

            for _, row in df.iterrows():

                circle = row.get("Circle")
                new_site_id = row.get("New Site ID")

                if not circle or not new_site_id:
                    continue

                TrackerModel.objects.update_or_create(
                    circle=circle,
                    new_site_id=new_site_id,

                    defaults={
                        "site_tagging": row.get("Site Tagging"),
                        "old_toco_name": row.get("Old TOCO Name"),
                        "old_site_id": row.get("Old Site Id"),
                        "new_toco_name": row.get("New TOCO Name"),
                        "sr_number": row.get("SR Number"),
                        "ran_oem": row.get("RAN OEM"),
                        "media_type": row.get("Media Type"),
                        "mw_oem": row.get("MW OEM"),
                        "relocation_method": row.get("Relocation Method"),
                        "relocation_type": row.get("Relocation Type"),
                        "old_site_band": row.get("OLD Site Band"),
                        "new_site_band": row.get("New Site Band"),
                        "nbd": row.get("NBD"),

                        # ✅ DATE SAFE
                        "workable_rfai_date": parse_date(row.get("Workable RFAI Date")),
                        "rfai_date": parse_date(row.get("RFAI Date")),
                        "allocation_date": parse_date(row.get("Allocation Date")),
                        "rfai_survey_date": parse_date(row.get("RFAI Survey Date")),
                        "mo_punch_date": parse_date(row.get("MO Punch Date")),
                        "material_dispatch_date": parse_date(row.get("Material Dispatch Date")),
                        "material_delivered_date": parse_date(row.get("Material Delivered Date")),
                        "installation_start_date": parse_date(row.get("Installation Start Date")),
                        "installation_end_date": parse_date(row.get("Installation End Date")),
                        "integration_date": parse_date(row.get("Integration Date")),
                        "emf_submission_date": parse_date(row.get("EMF Submission Date")),
                        "scft_done_date": parse_date(row.get("SCFT Done Date")),
                        "site_onair_date": parse_date(row.get("Site ONAIR Date")),
                    }
                )

        return Response({"message": "Upload successful"})

    except Exception as e:
        return Response({"error": str(e)}, status=500)