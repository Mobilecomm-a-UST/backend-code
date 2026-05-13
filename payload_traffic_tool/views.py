from django.shortcuts import render

# Create your views here.

import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .calculation import calculate_traffic
import os 
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
from .models import PayloadTraffic4G, UploadHistory,PayloadTraffic5G

main_folder=os.path.join(MEDIA_ROOT, "Payload_traffic")
output_path = os.path.join(main_folder, "Traffic_querry_output")
os.makedirs(output_path, exist_ok=True)




@api_view(['POST'])
def upload_4g_payload(request):
    username = request.user.username
    file = request.FILES.get('file')

    if not file:
        return Response({
            "status": False,
            "message": "No file uploaded"
        })

    file_name = file.name.lower()

    # ── Step 1: Read file ──────────────────────────
    if file_name.endswith('.csv'):
        df = pd.read_csv(file)
    elif file_name.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(file, engine='openpyxl')
    elif file_name.endswith('.xlsb'):
        df = pd.read_excel(file, engine='pyxlsb')
    else:
        return Response({
            "status": False,
            "message": "Unsupported file format"
        })

    # ── Step 2: Clean columns ──────────────────────
    df.columns = df.columns.astype(str).str.strip()
    df = df.dropna(how='all')

    fixed_cols = ['Short name', 'Site ID']
    date_cols = [
        col for col in df.columns
        if col not in fixed_cols
        and col != '4G Data Volume [GB]'
    ]

    # ── Step 3: Build data list ────────────────────
    data_to_save = []
    first_valid_date = None

    for row in df.itertuples(index=False):
        row_dict = dict(zip(df.columns, row))

        site_id    = str(row_dict.get('Site ID')).strip()
        short_name = str(row_dict.get('Short name')).strip()

        if (site_id.lower() in ["", "nan", "site id"] or
                short_name.lower() in
                ["", "nan", "short name"]):
            continue

        for date_col in date_cols:
            value = row_dict.get(date_col)
            if pd.isna(value):
                continue

            try:
                traffic_date = pd.to_datetime(
                    date_col).date()

                if first_valid_date is None:
                    first_valid_date = traffic_date

                data_to_save.append(
                    PayloadTraffic4G(
                        site_id       = site_id,
                        short_name    = short_name,
                        traffic_value = float(value),
                        traffic_date  = traffic_date
                    )
                )
            except Exception:
                continue

    if not data_to_save:
        return Response({
            "status": False,
            "message": "No valid data found"
        })

    # ── Step 4: Deduplicate within file ───────────
    unique_map = {}
    for obj in data_to_save:
        key = (obj.site_id,
               obj.traffic_date,
               obj.short_name)
        unique_map[key] = obj
    data_to_save = list(unique_map.values())

    # ── Step 5: Get ALL dates from current file ───
    # FIX: filter by BOTH site_id AND traffic_date
    all_site_ids    = list({
        obj.site_id for obj in data_to_save})
    all_dates       = list({
        obj.traffic_date for obj in data_to_save})

    # ── Step 6: Fetch existing records from DB ────
    # FIX: filter by site_id AND traffic_date both
    existing_records = PayloadTraffic4G.objects.filter(
        site_id__in      = all_site_ids,
        traffic_date__in = all_dates       # ← KEY FIX
    )

    existing_map = {
        (obj.site_id,
         obj.traffic_date,
         obj.short_name): obj
        for obj in existing_records
    }

    # ── Step 7: Separate into create and update ───
    to_create = []
    to_update = []

    for obj in data_to_save:
        key = (obj.site_id,
               obj.traffic_date,
               obj.short_name)

        if key in existing_map:
            # Record exists — update value
            existing_obj = existing_map[key]
            existing_obj.traffic_value = obj.traffic_value
            to_update.append(existing_obj)
        else:
            # New record — create it
            to_create.append(obj)

    # ── Step 8: Bulk create with ignore_conflicts ─
    # FIX: ignore_conflicts=True prevents crashes
    # on race conditions or missed duplicates
    if to_create:
        PayloadTraffic4G.objects.bulk_create(
            to_create,
            batch_size      = 10000,
            ignore_conflicts = True    # ← KEY FIX
        )

    # ── Step 9: Bulk update ───────────────────────
    if to_update:
        PayloadTraffic4G.objects.bulk_update(
            to_update,
            ['traffic_value'],
            batch_size = 10000
        )

    # ── Step 10: Log upload ───────────────────────
    UploadHistory.objects.create(
        user          = username,
        filename      = file.name,
        traffic_date  = first_valid_date,
        table_name    = "payload_traffic_4G",
        row_inserted  = len(to_create)
    )

    return Response({
        "status"         : True,
        "message"        : "4G Payload uploaded successfully",
        "inserted"       : len(to_create),
        "updated"        : len(to_update),
        "total_processed": len(data_to_save)
    })


@api_view(['POST'])
def upload_5g_payload(request):
    username = request.user.username
    file = request.FILES.get('file')

    if not file:
        return Response({
            "status": False,
            "message": "No file uploaded"
        })

    file_name = file.name.lower()

    # ── Step 1: Read file ──────────────────────────
    if file_name.endswith('.csv'):
        df = pd.read_csv(file)
    elif file_name.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(file, engine='openpyxl')
    elif file_name.endswith('.xlsb'):
        df = pd.read_excel(file, engine='pyxlsb')
    else:
        return Response({
            "status": False,
            "message": "Unsupported file format"
        })

    # ── Step 2: Clean columns ──────────────────────
    df.columns = df.columns.astype(str).str.strip()
    df = df.dropna(how='all')

    fixed_cols = ['Short name', 'Site ID']
    date_cols = [
        col for col in df.columns
        if col not in fixed_cols
        and col != '5G Data Volume [GB]'
    ]

    # ── Step 3: Build data list ────────────────────
    data_to_save = []
    first_valid_date = None

    for row in df.itertuples(index=False):
        row_dict = dict(zip(df.columns, row))

        site_id    = str(row_dict.get('Site ID')).strip()
        short_name = str(row_dict.get('Short name')).strip()

        if (site_id.lower() in ["", "nan", "site id"] or
                short_name.lower() in
                ["", "nan", "short name"]):
            continue

        for date_col in date_cols:
            value = row_dict.get(date_col)
            if pd.isna(value):
                continue

            try:
                traffic_date = pd.to_datetime(
                    date_col).date()

                if first_valid_date is None:
                    first_valid_date = traffic_date

                data_to_save.append(
                    PayloadTraffic5G(
                        site_id       = site_id,
                        short_name    = short_name,
                        traffic_value = float(value),
                        traffic_date  = traffic_date
                    )
                )
            except Exception:
                continue

    if not data_to_save:
        return Response({
            "status": False,
            "message": "No valid data found"
        })

    # ── Step 4: Deduplicate within file ───────────
    unique_map = {}
    for obj in data_to_save:
        key = (obj.site_id,
               obj.traffic_date,
               obj.short_name)
        unique_map[key] = obj
    data_to_save = list(unique_map.values())

    # ── Step 5: Get ALL dates from current file ───
    all_site_ids = list({
        obj.site_id for obj in data_to_save})
    all_dates    = list({
        obj.traffic_date for obj in data_to_save})

    # ── Step 6: Fetch existing from DB ───────────
    # FIX: filter by BOTH site_id AND traffic_date
    existing_records = PayloadTraffic5G.objects.filter(
        site_id__in      = all_site_ids,
        traffic_date__in = all_dates       # ← KEY FIX
    )

    existing_map = {
        (obj.site_id,
         obj.traffic_date,
         obj.short_name): obj
        for obj in existing_records
    }

    # ── Step 7: Separate create and update ────────
    to_create = []
    to_update = []

    for obj in data_to_save:
        key = (obj.site_id,
               obj.traffic_date,
               obj.short_name)

        if key in existing_map:
            existing_obj = existing_map[key]
            existing_obj.traffic_value = obj.traffic_value
            to_update.append(existing_obj)
        else:
            to_create.append(obj)

    # ── Step 8: Bulk create with ignore_conflicts ─
    if to_create:
        PayloadTraffic5G.objects.bulk_create(
            to_create,
            batch_size       = 10000,
            ignore_conflicts = True    # ← KEY FIX
        )

    # ── Step 9: Bulk update ───────────────────────
    if to_update:
        PayloadTraffic5G.objects.bulk_update(
            to_update,
            ['traffic_value'],
            batch_size = 10000
        )

    # ── Step 10: Log upload ───────────────────────
    UploadHistory.objects.create(
        user         = username,
        filename     = file.name,
        traffic_date = first_valid_date,
        table_name   = "payload_traffic_5G",
        row_inserted = len(to_create)
    )

    return Response({
        "status"         : True,
        "message"        : "5G Payload uploaded successfully",
        "inserted"       : len(to_create),
        "updated"        : len(to_update),
        "total_processed": len(data_to_save)
    })

#get data in db for traffic 
@api_view(['POST'])
def get_traffic(request):
    user_name=request.user
    print(user_name)

    site_ids_str = request.data.get('site_id', '').strip()
    on_air_date_str = request.data.get('on_air_date', '').strip()
    if not site_ids_str:
        return Response(
            {'status': False, 'message': 'site_id parameter is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not on_air_date_str:
        return Response(
            {'status': False, 'message': 'on_air_date parameter is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    result, filepath = calculate_traffic(site_ids_str, on_air_date_str)
    filename = os.path.basename(filepath)
    file_relative_path = f"Payload_traffic/Report/{filename}"

    download_url = request.build_absolute_uri(
        f"{MEDIA_URL.rstrip('/')}/{file_relative_path}"
    )

    return Response({
        'status': True,
        'message': 'Traffic calculation successfully!',
        'download_url': download_url,
       
    })


@api_view(['POST'])
def get_history(request):
    queryset = UploadHistory.objects.all().order_by('-upload_timestamp').values(
        "id", "user", "filename", "traffic_date", "table_name", "row_inserted", "upload_timestamp"
    )
    return Response({
        "status": True,
        "message": "Upload history fetched successfully",
        "data": list(queryset)
    })


@api_view(['POST'])
def delete_data_4g(request):
    deleted_count, _ = PayloadTraffic4G.objects.all().delete()

    return Response({
        "status": True,
        "message": f"All 4G data deleted successfully ({deleted_count} records)"
    })



@api_view(['POST'])
def delete_data_5g(request):
    deleted_count, _ = PayloadTraffic5G.objects.all().delete()

    return Response({
        "status": True,
        "message": f"All 5G data deleted successfully ({deleted_count} records)"
    })  

@api_view(['POST'])
def delete_history(request):
    deleted_count, _ = UploadHistory.objects.all().delete()

    return Response({
        "status": True,
        "message": f"All History deleted successfully ({deleted_count} records)"
    })
