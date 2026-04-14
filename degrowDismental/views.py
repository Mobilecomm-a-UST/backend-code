import os
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
import pandas as pd
from openpyxl import Workbook
from datetime import datetime
from rest_framework import status
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
import re
from degrowDismental.models import *
from datetime import date
import json
from django.db.models import F, Count, Q
import shutil
from .utils import format_excel
from .tasks import send_survey_done_email



#--main folder in media folder--------------------
main_folder = os.path.join(MEDIA_ROOT, 'degrow_dismantle')
os.makedirs(main_folder, exist_ok=True)



@api_view(["GET"])
def get_Files(request):
    folder_path = os.path.join(main_folder, "locater")
    locater_df_list = []

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)

        if not os.path.isfile(file_path):
            continue

        if file_path.endswith('.csv'):
            try:
                df = pd.read_csv(file_path, usecols=["LOCATION_NAME", "SITEID"])
                locater_df_list.append(df)
            except Exception as e:
                return Response({"error": f"Error in file {file}: {str(e)}"}, status=500)
        elif file_path.endswith(('.xls', '.xlsx')):
            try:
                df = pd.read_excel(file_path, engine='openpyxl', usecols=["LOCATION_NAME", "SITEID"])
                locater_df_list.append(df)
            except Exception as e:
                return Response({"error": f"Error in file {file}: {str(e)}"}, status=500)
        else:
            continue  # skip unsupported formats

    if not locater_df_list:
        return Response({"error": "No valid log files found"}, status=400)

    log_df = pd.concat(locater_df_list, ignore_index=True)
    
    

    # ✅ Proper response
    return Response({
        "message": "Concatenated log_df columns",
        "columns": list(log_df.columns)
    })

# DELETE SINGLE FILE
@api_view(['DELETE'])
def delete_single_file(request):
    try:
        mobinet_data_path = os.path.join(main_folder, request.data.get('foldername'))
        filename = request.data.get('filename')  # expecting JSON body: { "filename": "example.csv" }

        if not filename:
            return Response({'error': 'Filename not provided'}, status=status.HTTP_400_BAD_REQUEST)

        file_path = os.path.join(mobinet_data_path, filename)

        if not os.path.exists(file_path):
            return Response({'error': f'File "{filename}" not found'}, status=status.HTTP_404_NOT_FOUND)

        os.remove(file_path)

        return Response({
            'status': True,
            'message': f'File "{filename}" deleted successfully'
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
# UPLOAD LOCATER FILES
@api_view(['POST', 'GET', 'DELETE'])
def upload_locator_data(request):
    try:
        locator_folder_path = os.path.join(main_folder, 'locater')
        os.makedirs(locator_folder_path, exist_ok=True)
 
        if request.method == 'POST':
            files = request.FILES.getlist('files')
            if not files:
                return Response({'error': 'No files uploaded'}, status=status.HTTP_400_BAD_REQUEST)
 
            for f in files:
                file_path = os.path.join(locator_folder_path, f.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
 
            return Response({'status': True, 'message': 'Files saved successfully'}, status=status.HTTP_200_OK)
 
        elif request.method == 'GET':
            if not os.path.exists(locator_folder_path):
                return Response({'files': []}, status=status.HTTP_200_OK)
            files = os.listdir(locator_folder_path)
            return Response({
                'status': True,
                'message': 'Files found in locator_data folder',
                'files': files,
            }, status=status.HTTP_200_OK)
 
        elif request.method == 'DELETE':
            if not os.path.exists(locator_folder_path):
                return Response({'error': 'Folder does not exist'}, status=status.HTTP_404_NOT_FOUND)
            deleted_files = []
            for filename in os.listdir(locator_folder_path):
                file_path = os.path.join(locator_folder_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    deleted_files.append(filename)
 
            return Response({
                'status': True,
                'message': 'Files deleted successfully',
                'deleted_files': deleted_files
            }, status=status.HTTP_200_OK)
 
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def degrow_dismantle(request):
    # ----------------- Helpers -----------------
    def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and normalize column names"""
        df.columns = (
            df.columns.astype(str)
            .str.strip()
            .str.replace(r"\n+", "", regex=True)
            .str.replace(r"\s+", " ", regex=True)
        )
        return df

    def move_after(cols: list, col_to_move: str, after_col: str) -> list:
        """Reorder columns by moving col_to_move after after_col"""
        if col_to_move in cols and after_col in cols:
            cols.insert(cols.index(after_col) + 1, cols.pop(cols.index(col_to_move)))
        return cols

    def drop_if_exists(df: pd.DataFrame, cols: list) -> pd.DataFrame:
        """Drop columns if they exist"""
        existing = [c for c in cols if c in df.columns]
        return df.drop(columns=existing) if existing else df
    

    #   ----- LOCATER FILE READ -----
    locater_file_path = os.path.join(main_folder, "locater")
    locater_df_list = []

    for file in os.listdir(locater_file_path):
        file_path = os.path.join(locater_file_path, file)

        if not os.path.isfile(file_path):
            continue

        if file_path.endswith('.csv'):
            try:
                df = pd.read_csv(file_path , usecols=["LOCATION_NAME", "SITEID"])
                locater_df_list.append(df)
            except Exception as e:
                return Response({"error": f"Error in file {file}: {str(e)}"}, status=500)
        elif file_path.endswith(('.xls', '.xlsx')):
            try:
                df = pd.read_excel(file_path, engine='openpyxl', usecols=["LOCATION_NAME", "SITEID"])
                locater_df_list.append(df)
            except Exception as e:
                return Response({"error": f"Error in file {file}: {str(e)}"}, status=500)
        else:
            continue  # skip unsupported formats

    if not locater_df_list:
        return Response({"error": "No valid log files found"}, status=400)

    locater_df = pd.concat(locater_df_list, ignore_index=True)

    #  -------------  END OF LOCATER FILE READ  -----------------


    # ----------------- Read Input Files -----------------
    usecols_hw = ["ITEMCODE", "Module Name", "Module type", "Tech"]
    hw_df = pd.read_csv(request.FILES["hw"], usecols=usecols_hw)
    # locater_df = pd.read_csv(request.FILES["locater"], usecols=["LOCATION_NAME", "SITEID"])
    dpr_df = pd.read_excel(request.FILES["dpr"], sheet_name="Compile DPR", engine="openpyxl")
    olm_df = pd.read_excel(request.FILES["olm"], engine="openpyxl")

    # Clean all input dataframes
    for df in [hw_df, locater_df, dpr_df, olm_df]:
        clean_columns(df)

    # Strip & deduplicate critical fields
    hw_df["ITEMCODE"] = hw_df["ITEMCODE"].astype(str).str.strip()
    locater_df["LOCATION_NAME"] = locater_df["LOCATION_NAME"].astype(str).str.strip()
    olm_df["OLM ID"] = olm_df["OLM ID"].astype(str).str.strip()

    hw_df = hw_df.drop_duplicates(subset=["ITEMCODE"])
    locater_df = locater_df.drop_duplicates(subset=["LOCATION_NAME"])

    # Optimize memory: convert some fields to category
    cat_cols = ["Module Name", "Module type", "Tech"]
    for col in cat_cols:
        if col in hw_df.columns:
            hw_df[col] = hw_df[col].astype("category")

    # ----------------- Prepare Export Paths -----------------
    export_dir = os.path.join(MEDIA_ROOT, "exports")
    os.makedirs(export_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    rfs_file = os.path.join(export_dir, f"rfs_version4_{timestamp}.csv")
    dpr_file = os.path.join(export_dir, f"dpr_rfs_version4_{timestamp}.xlsx") 

    # Ensure no old files exist
    for f in [rfs_file, dpr_file]:
        if os.path.exists(f):
            os.remove(f)

    # ----------------- Process RFS in Chunks -----------------
    rfs_file_path = os.path.join(main_folder, "rfs")
    rfs_files = [f for f in os.listdir(rfs_file_path) if os.path.isfile(os.path.join(rfs_file_path, f))]
    # Check file count
    if len(rfs_files) == 0:
        return Response({"error": "No files found in rfs folder"}, status=400)
    elif len(rfs_files) > 1:
        return Response({"error": "More than one file found in rfs folder"}, status=400)
    # Only one file exists
    file_path = os.path.join(rfs_file_path, rfs_files[0])

    chunk_iter = pd.read_csv(file_path, chunksize=50000)
    all_rfs_chunks, total_rows = [], 0

    for i, rfs_chunk in enumerate(chunk_iter):
        clean_columns(rfs_chunk)
        rfs_chunk["FROMLOCATION"] = rfs_chunk["FROMLOCATION"].astype(str).str.strip()
        rfs_chunk["ITEMCODE"] = rfs_chunk["ITEMCODE"].astype(str).str.strip()

        # Merge with OLM, Locator, HW
        merged_rfs = (
            rfs_chunk
            .merge(olm_df[["OLM ID"]], left_on="RFS_CREATED_BY", right_on="OLM ID", how="inner")
            .merge(locater_df, left_on="FROMLOCATION", right_on="LOCATION_NAME", how="left")
            .drop(columns=["LOCATION_NAME"])
            .merge(hw_df, on="ITEMCODE", how="left")
        )

        # Filter valid modules
        merged_rfs = merged_rfs[
            merged_rfs["Module Name"].notna()
            & (merged_rfs["Module Name"].astype(str).str.strip() != "")
            & (merged_rfs["Module type"].isin(["RRU", "BBU", "CC"]))
        ]

        total_rows += len(merged_rfs)

        # Append cleaned chunk
        selected_cols = [
            "SRNCAMREQNUM", "RFS_CREATED_DATE", "Module Name", "RFS_QTY",
            "SERIALNUMBER", "ORACLE_DC_NO", "PICKED_DATE", "PICKED_QTY",
            "SHIPPED_DATE", "RECEIPT_DATE", "RECEIVED_QTY",
            "SRNCAMREQSTATUS", "FROMLOCATION", "SITEID", "Tech"
        ]
        all_rfs_chunks.append(merged_rfs[selected_cols])

        # Write filtered RFS incrementally to CSV
        merged_rfs.to_csv(
            rfs_file, 
            mode="a", 
            header=(i == 0), 
            index=False, 
            encoding="utf-8-sig"
        )

    # ----------------- Final DPR Merge -----------------
    final_rfs_df = pd.concat(all_rfs_chunks, ignore_index=True)

    merged_dpr_rfs_df = (
        dpr_df
        .merge(final_rfs_df, left_on="Site ID", right_on="SITEID", how="left")
        .drop_duplicates(subset=["Module-Serial No"])
    )

    # Rename columns (CATS mapping)
    rename_map = {
        "RFS_CREATED_DATE": "SREQ Date As Per CATS",
        "Module Name": "Dismantle Module As Per CATS",
        "RFS_QTY": "Dismantle Module Qty As Per CATS",
        "SERIALNUMBER": "Serial Number As Per CATS",
        "ORACLE_DC_NO": "DC As Per CATS",
        "PICKED_DATE": "Picked Date As Per CATS",
        "PICKED_QTY": "Picked Qty As Per CATS",
        "SHIPPED_DATE": "Ship Date As Per CATS",
        "RECEIPT_DATE": "Submission Date As Per CATS",
        "RECEIVED_QTY": "Received Qty As Per CATS",
        "SRNCAMREQSTATUS": "SREQ Status as per CATS",
    }
    merged_dpr_rfs_df.rename(columns=rename_map, inplace=True)

    # Reorder important columns
    cols = merged_dpr_rfs_df.columns.tolist()
    reorder_map = [
        ("SREQ Date As Per CATS", "SREQ Date-DD/MM/YY"),
        ("Dismantle Module As Per CATS", "Dismantled-Modules Name"),
        ("Dismantle Module Qty As Per CATS", "Dismantled-Module Qty"),
        ("Serial Number As Per CATS", "Dismantled-Module-Serial No"),
        ("DC As Per CATS", "DC NUMBER"),
        ("Picked Date As Per CATS", "Pick Date"),
        ("Picked Qty As Per CATS", "Pick/Ship Qty QTY"),
        ("Ship Date As Per CATS", "Ship Date"),
        ("Submission Date As Per CATS", "WH Submission Date-DD/MM/YY"),
        ("Received Qty As Per CATS", "WH Submission Qty"),
        ("SREQ Status as per CATS", "All SREQ Status"),
        ("FROMLOCATION", "Locator ID"),
    ]
    for col, after in reorder_map:
        cols = move_after(cols, col, after)
    merged_dpr_rfs_df = merged_dpr_rfs_df[cols]

    # ----------------- Split Matched / Unmatched Tech -----------------
    cond = merged_dpr_rfs_df.apply(
        lambda row: str(row["Tech"]) in str(row["Unique ID"]), axis=1
    )
    #-------------------- this is for blank Dismantled-Module-Serial No -----------------
    cond2 = (
        merged_dpr_rfs_df["Dismantled-Module-Serial No"].isna()
        | (merged_dpr_rfs_df["Dismantled-Module-Serial No"].astype(str).str.strip() == "")
    )

    merged_dpr_rfs_df1 = (
        merged_dpr_rfs_df[cond]
        .merge(
            final_rfs_df[["SERIALNUMBER"]],
            left_on="Dismantled-Module-Serial No",
            right_on="SERIALNUMBER",
            how="left"
        )
        .drop_duplicates(subset=["Module-Serial No"])
    )

    # Drop old col, rename new one, reorder
    merged_dpr_rfs_df1 = drop_if_exists(merged_dpr_rfs_df1, ["Serial Number As Per CATS"])
    merged_dpr_rfs_df1 = merged_dpr_rfs_df1.rename(
        columns={"SERIALNUMBER": "Serial Number As Per CATS 2"}
    )

    cols = merged_dpr_rfs_df1.columns.tolist()
    cols = move_after(cols, "Serial Number As Per CATS 2", "Dismantled-Module-Serial No")
    merged_dpr_rfs_df1 = merged_dpr_rfs_df1[cols]

    merged_dpr_rfs_df2 = merged_dpr_rfs_df[~cond].copy()

    # ----------------- Save Excel with 2 Sheets -----------------
    with pd.ExcelWriter(dpr_file, engine="openpyxl") as writer:
        merged_dpr_rfs_df1.to_excel(writer, sheet_name="Matched Tech", index=False)
        merged_dpr_rfs_df[cond2].to_excel(writer, sheet_name="Matched Tech with blank Sr. No.", index=False)
        merged_dpr_rfs_df2.to_excel(writer, sheet_name="Unmatched Tech", index=False)
    
    dpr_file = dpr_file.replace(MEDIA_ROOT, MEDIA_URL).replace('\\', '/')
    rfs_file = rfs_file.replace(MEDIA_ROOT, MEDIA_URL).replace('\\', '/')
    download_dpr_url = request.build_absolute_uri(dpr_file)
    download_rfs_url = request.build_absolute_uri(rfs_file)

    # ----------------- API Response -----------------
    return Response({
        "status": "success",
        "rfs_rows": total_rows,
        "download_url": {
            "rfs_report": download_rfs_url,
            "dpr_report": download_dpr_url
        },
        "columns": merged_dpr_rfs_df.columns.to_list(),
        "rfs_columns": final_rfs_df.columns.to_list()
    })
    
    
@api_view(['POST', 'GET', 'DELETE'])
def upload_mobinet_data(request):
    try:
        mobinet_folder_path = os.path.join(main_folder, 'mobinet')
        os.makedirs(mobinet_folder_path, exist_ok=True)
 
        if request.method == 'POST':
            files = request.FILES.getlist('files')
            if not files:
                return Response({'error': 'No files uploaded'}, status=status.HTTP_400_BAD_REQUEST)
 
            for f in files:
                file_path = os.path.join(mobinet_folder_path, f.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
 
            return Response({'status': True, 'message': 'Files saved successfully'}, status=status.HTTP_200_OK)
 
        elif request.method == 'GET':
            if not os.path.exists(mobinet_folder_path):
                return Response({'files': []}, status=status.HTTP_200_OK)
            files = os.listdir(mobinet_folder_path)
            return Response({
                'status': True,
                'message': 'Files found in locator_data folder',
                'files': files,
            }, status=status.HTTP_200_OK)
 
        elif request.method == 'DELETE':
            if not os.path.exists(mobinet_folder_path):
                return Response({'error': 'Folder does not exist'}, status=status.HTTP_404_NOT_FOUND)
            deleted_files = []
            for filename in os.listdir(mobinet_folder_path):
                file_path = os.path.join(mobinet_folder_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    deleted_files.append(filename)
 
            return Response({
                'status': True,
                'message': 'Files deleted successfully',
                'deleted_files': deleted_files
            }, status=status.HTTP_200_OK)
 
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   

@api_view(['POST', 'GET', 'DELETE'])
def upload_rfs_data(request):
    try:
        rfs_folder_path = os.path.join(main_folder, 'rfs')
        os.makedirs(rfs_folder_path, exist_ok=True)

        if request.method == 'POST':
            files = request.FILES.getlist('files')
            if not files:
                return Response({'error': 'No files uploaded'}, status=status.HTTP_400_BAD_REQUEST)
 
            for f in files:
                file_path = os.path.join(rfs_folder_path, f.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
 
            return Response({'status': True, 'message': 'Files saved successfully'}, status=status.HTTP_200_OK)
 
        elif request.method == 'GET':
            if not os.path.exists(rfs_folder_path):
                return Response({'files': []}, status=status.HTTP_200_OK)
            files = os.listdir(rfs_folder_path)
            return Response({
                'status': True,
                'message': 'Files found in rfs folder',
                'files': files,
            }, status=status.HTTP_200_OK)
 
        elif request.method == 'DELETE':
            if not os.path.exists(rfs_folder_path):
                return Response({'error': 'Folder does not exist'}, status=status.HTTP_404_NOT_FOUND)
            deleted_files = []
            for filename in os.listdir(rfs_folder_path):
                file_path = os.path.join(rfs_folder_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    deleted_files.append(filename)
 
            return Response({
                'status': True,
                'message': 'Files deleted successfully',
                'deleted_files': deleted_files
            }, status=status.HTTP_200_OK)
 
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST', 'GET', 'DELETE'])
def upload_msmf_data(request):
    try:
        msmf_folder_path = os.path.join(main_folder, 'msmf')
        os.makedirs(msmf_folder_path, exist_ok=True)

        if request.method == 'POST':
            files = request.FILES.getlist('files')
            if not files:
                return Response({'error': 'No files uploaded'}, status=status.HTTP_400_BAD_REQUEST)
 
            for f in files:
                file_path = os.path.join(msmf_folder_path, f.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
 
            return Response({'status': True, 'message': 'Files saved successfully'}, status=status.HTTP_200_OK)
 
        elif request.method == 'GET':
            if not os.path.exists(msmf_folder_path):
                return Response({'files': []}, status=status.HTTP_200_OK)
            files = os.listdir(msmf_folder_path)
            return Response({
                'status': True,
                'message': 'Files found in msmf folder',
                'files': files,
            }, status=status.HTTP_200_OK)
 
        elif request.method == 'DELETE':
            if not os.path.exists(msmf_folder_path):
                return Response({'error': 'Folder does not exist'}, status=status.HTTP_404_NOT_FOUND)
            deleted_files = []
            for filename in os.listdir(msmf_folder_path):
                file_path = os.path.join(msmf_folder_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    deleted_files.append(filename)
 
            return Response({
                'status': True,
                'message': 'Files deleted successfully',
                'deleted_files': deleted_files
            }, status=status.HTTP_200_OK)
 
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST', 'GET', 'DELETE'])
def upload_aw_rfs_data(request):
    try:
        aw_rfs_folder_path = os.path.join(main_folder, 'aw_rfs')
        os.makedirs(aw_rfs_folder_path, exist_ok=True)
 
        if request.method == 'POST':
            files = request.FILES.getlist('files')
            if not files:
                return Response({'error': 'No files uploaded'}, status=status.HTTP_400_BAD_REQUEST)
 
            for f in files:
                file_path = os.path.join(aw_rfs_folder_path, f.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
 
            return Response({'status': True, 'message': 'Files saved successfully'}, status=status.HTTP_200_OK)
 
        elif request.method == 'GET':
            if not os.path.exists(aw_rfs_folder_path):
                return Response({'files': []}, status=status.HTTP_200_OK)
            files = os.listdir(aw_rfs_folder_path)
            return Response({
                'status': True,
                'message': 'Files found in locator_data folder',
                'files': files,
            }, status=status.HTTP_200_OK)
 
        elif request.method == 'DELETE':
            if not os.path.exists(aw_rfs_folder_path):
                return Response({'error': 'Folder does not exist'}, status=status.HTTP_404_NOT_FOUND)
            deleted_files = []
            for filename in os.listdir(aw_rfs_folder_path):
                file_path = os.path.join(aw_rfs_folder_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    deleted_files.append(filename)
 
            return Response({
                'status': True,
                'message': 'Files deleted successfully',
                'deleted_files': deleted_files
            }, status=status.HTTP_200_OK)
 
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   

@api_view(['POST', 'GET', 'DELETE'])
def upload_aw_msmf_data(request):
    try:
        aw_msmf_folder_path = os.path.join(main_folder, 'aw_msmf')
        os.makedirs(aw_msmf_folder_path, exist_ok=True)
 
        if request.method == 'POST':
            files = request.FILES.getlist('files')
            if not files:
                return Response({'error': 'No files uploaded'}, status=status.HTTP_400_BAD_REQUEST)
 
            for f in files:
                file_path = os.path.join(aw_msmf_folder_path, f.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
 
            return Response({'status': True, 'message': 'Files saved successfully'}, status=status.HTTP_200_OK)
 
        elif request.method == 'GET':
            if not os.path.exists(aw_msmf_folder_path):
                return Response({'files': []}, status=status.HTTP_200_OK)
            files = os.listdir(aw_msmf_folder_path)
            return Response({
                'status': True,
                'message': 'Files found in locator_data folder',
                'files': files,
            }, status=status.HTTP_200_OK)
 
        elif request.method == 'DELETE':
            if not os.path.exists(aw_msmf_folder_path):
                return Response({'error': 'Folder does not exist'}, status=status.HTTP_404_NOT_FOUND)
            deleted_files = []
            for filename in os.listdir(aw_msmf_folder_path):
                file_path = os.path.join(aw_msmf_folder_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    deleted_files.append(filename)
 
            return Response({
                'status': True,
                'message': 'Files deleted successfully',
                'deleted_files': deleted_files
            }, status=status.HTTP_200_OK)
 
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   

def format_date(value):
    if isinstance(value, (date, datetime)):
        return value.strftime("%d-%b-%y")
    return value


@api_view(['POST'])
def fetch_site_status(request):
    circle = request.data.get("circle")

    if not circle:
        return Response(
            {"error": "circle is required"},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    if circle == 'CENTRAL':
        queryset = DismantleCircleData.objects.all()
    else:
        queryset = DismantleCircleData.objects.filter(circle=circle)

    if not queryset.exists():
        return Response(
            {"message": "No DB records found for this circle."},
            status=status.HTTP_200_OK
        )

    data = []

    for obj in queryset:
        data.append({
            "id": obj.id,
            "Circle": obj.circle,
            "Site ID": obj.site_id,
            "Partner Code": obj.partner_code,
            "Partner": obj.partner,
            "Is Approved": format_date(obj.is_approved),
            "Is Surveyed": format_date(obj.is_surveyed),
            "Is SRN Done": format_date(obj.is_srn_done),
            "Remarks": obj.remarks,
        })

    return Response({"data": data}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def fetch_circle_summary(request):

    partners = request.data.get("partner") 
    
    partners = [p.strip() for p in partners.split(',')] if partners else ["ALL"]

    queryset = DismantleCircleData.objects.all()

    # Filter by partners if provided
    
    print(partners)
    if "ALL" not in partners:
        queryset = queryset.filter(partner__in=partners)

    queryset = (
        queryset
        .values("circle")
        .annotate(
            total_sites=Count("site_id", distinct=True),
            surveyed_sites=Count(
                "site_id",
                filter=Q(is_surveyed__isnull=False),
                distinct=True
            ),
            srn_done_sites=Count(
                "site_id",
                filter=Q(is_srn_done__isnull=False),
                distinct=True
            )
        )
        .order_by("circle")
    )

    data = []

    total_sites_sum = 0
    surveyed_sum = 0
    srn_sum = 0

    for row in queryset:
        total_sites = row["total_sites"]
        surveyed = row["surveyed_sites"]
        srn_done = row["srn_done_sites"]

        survey_pending = total_sites - surveyed
        srn_pending = surveyed - srn_done

        total_sites_sum += total_sites
        surveyed_sum += surveyed
        srn_sum += srn_done

        data.append({
            "Circle": row["circle"],
            "Total Sites": total_sites,
            "Survey Done": surveyed,
            "Survey Pending": survey_pending,
            "SRN Done": srn_done,
            "SRN Pending": srn_pending,
        })

    # ALL row
    all_row = {
        "Circle": "ALL",
        "Total Sites": total_sites_sum,
        "Survey Done": surveyed_sum,
        "Survey Pending": total_sites_sum - surveyed_sum,
        "SRN Done": srn_sum,
        "SRN Pending": surveyed_sum - srn_sum,
    }

    data.insert(0, all_row)

    return Response({"data": data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def mobinet_data_fetch_from_database(request):
    circle = request.data.get("circle")
    siteId = request.data.get("siteId")

    if not circle or not siteId:
        return Response({"message": "siteId/circle not provided"}, status=400)
    
    try:
        # ---------------- 1️⃣ Check Database First ----------------
        db_queryset = DismantleModelData.objects.filter(
            zone=circle,
            site_id=siteId
        )

        if db_queryset.exists():
            db_data = db_queryset.values(
                "approval_date",
                "model_name",
                "expected_quantity",
                "serial_number",
                "is_found",
                "is_in_mobinet",
                "srn_number",
                "remarks"
            )

            formatted_data = []

            for row in db_data:
                formatted_row = {}
                for key, value in row.items():
                    # Convert: model_name -> Model Name
                    new_key = key.replace("_", " ").title()
                    if new_key == "Srn Number":
                        new_key = "SRN Number"
                    if new_key == "Model Name":
                        new_key = "Model"
                    formatted_row[new_key] = value
                formatted_data.append(formatted_row)

            return Response({
                "status": "success",
                "source": "database",
                "count": len(formatted_data),
                "data": formatted_data
            })

        return Response({
            "status": "No Data found"
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)
        
 
@api_view(['POST'])
def mobinet_data_fetch_from_file(request):

    circle = request.data.get("circle")
    siteId = request.data.get("siteId")

    if not circle or not siteId:
        return Response({"message": "siteId/circle not provided"}, status=400)

    try:

        # ---------------- 1️⃣ Check Database First ----------------
        db_queryset = DismantleModelData.objects.filter(
            zone=circle,
            site_id=siteId
        )

        if db_queryset.exists():

            db_data = db_queryset.values(
                "approval_date",
                "model_name",
                "expected_quantity",
                "serial_number",
                "is_found",
                "is_in_mobinet",
                "srn_number",
                "remarks"
            )

            formatted_data = []

            for row in db_data:
                formatted_row = {}
                for key, value in row.items():

                    new_key = key.replace("_", " ").title()

                    if new_key == "Srn Number":
                        new_key = "SRN Number"

                    if new_key == "Model Name":
                        new_key = "Model"

                    formatted_row[new_key] = value

                formatted_data.append(formatted_row)

            return Response({
                "status": "success",
                "source": "database",
                "count": len(formatted_data),
                "data": formatted_data
            })


        # ---------------- 2️⃣ If Not Found → Fetch From File ----------------

        mobinet_folder = os.path.join(main_folder, 'mobinet')

        expected_filename_prefix = f"{circle}"

        mobinet_files = [
            f for f in os.listdir(mobinet_folder)
            if f.startswith(expected_filename_prefix)
        ]

        if not mobinet_files:
            return Response({"error": "Mobinet file not found"}, status=400)

        mobinet_path = os.path.join(mobinet_folder, mobinet_files[0])

        if mobinet_path.endswith(".csv"):
            mobinet_df = pd.read_csv(
                mobinet_path,
                usecols=["Zone", "Parent Site", "Cabinet", "Serial Number", "Board Model"]
            )

        elif mobinet_path.endswith((".xls", ".xlsx")):
            mobinet_df = pd.read_excel(
                mobinet_path,
                usecols=["Zone", "Parent Site", "Cabinet", "Serial Number", "Board Model"],
                engine="openpyxl"
            )

        else:
            return Response({"error": "Unsupported mobinet file format"}, status=400)
        
        mobinet_df["Model"] = mobinet_df["Board Model"]

        mobinet_df["Parent Site"] = mobinet_df["Parent Site"].astype(str).str.strip()
        mobinet_df["Zone"] = mobinet_df["Zone"].astype(str).str.strip()

        # Filter by circle & site
        filtered_mobinet = mobinet_df[
            (mobinet_df["Zone"] == circle) &
            (mobinet_df["Parent Site"] == f"{siteId}_{circle}")
        ].copy()

        if filtered_mobinet.empty:
            return Response({"message": "No data found in Mobinet for given site"}, status=404)

        filtered_mobinet = filtered_mobinet[
            filtered_mobinet['Serial Number'].notna() &
            (~filtered_mobinet['Serial Number'].astype(str).str.strip().isin(
                ["", "-", "_", "N/A", "NaN", "Nan", "undefined", None]
            ))
        ]

        board_list = [
            "DPLX-1",
            "SFP_R",
            "MN1",
            "FTLF1436W5BTD-SJ",
            "MRSB-OC",
            "RTXM228-702",
            "DuraRET2-AirT20",
            "SPP10ELRIDFRSEC",
            "RTXM228-702-C30",
            "FTLX1370W4BTL-SM",
            "RTXM191-404",
            "COMMRET2S",
            "RTXL185-210",
            "MTRS-1E21-01",
            "SFP24-IS3LC-IAA",
            "LX1801INA-CER",
            "LTF1303-BH+",
            "ECU-005L",
            "ACCURET1"
        ]

        filtered_mobinet = filtered_mobinet[
            ~filtered_mobinet["Board Model"].astype(str).str.strip().isin(board_list)
        ]

        filtered_mobinet = filtered_mobinet[['Model', 'Cabinet', 'Serial Number']]

        filtered_mobinet.rename(columns={"Cabinet": "Expected Quantity"}, inplace=True)

        filtered_mobinet = filtered_mobinet.where(pd.notnull(filtered_mobinet), None)

        filtered_mobinet["Is In Mobinet"] = True
        filtered_mobinet["Remarks"] = ""
        filtered_mobinet["SRN Number"] = ""
        filtered_mobinet["Approval Date"] = ""
        filtered_mobinet["Is Found"] = False
        
        filtered_mobinet = filtered_mobinet.drop_duplicates(subset=["Model", "Serial Number"])

        filtered_mobinet["index"] = range(1, len(filtered_mobinet) + 1)

        return Response({
            "source": "file",
            "data": filtered_mobinet.to_dict(orient="records")
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

        
@api_view(['POST'])
def mobinet_data_submit_by_central(request):
    circle = request.data.get("circle")
    siteId = request.data.get("siteId")
    records = request.data.get("data", [])
    partner = request.data.get("partner")
    partner_code = request.data.get("partner_code")

    if not circle or not siteId or not partner or not partner_code:
        return Response({"message": "siteId/circle not provided"}, status=400)

    if not records:
        return Response({"message": "No data provided"}, status=400)

    try:
        existing_obj = DismantleCircleData.objects.filter(
            circle=circle,
            site_id=siteId
        ).first()

        if existing_obj:
            data = {
                "id": existing_obj.id,
                "Circle": existing_obj.circle,
                "Site ID": existing_obj.site_id,
                "Partner Code": existing_obj.partner_code,
                "Partner": existing_obj.partner,
                "Is Approved": format_date(existing_obj.is_approved),
                "Is Surveyed": format_date(existing_obj.is_surveyed),
                "Is SRN Done": format_date(existing_obj.is_srn_done),
                "Remarks": existing_obj.remarks,
            }

            return Response(
                {
                    "message": "Site already approved. No changes made.",
                    "data": data
                },
                status=status.HTTP_200_OK
            )

        DismantleCircleData.objects.create(
            circle=circle,
            site_id=siteId,
            partner_code=partner_code,
            partner=partner,
            is_approved=date.today(),
            is_surveyed=None,
            is_srn_done=None,
            remarks="Ready for survey",
        )

        # ✅ Safe json load
        if isinstance(records, str):
            records = json.loads(records)

        for record in records:

            model_name = record.get("Model")
            expected_quantity = record.get("Expected Quantity")
            serial_number = record.get("Serial Number")

            DismantleModelData.objects.update_or_create(
                zone=circle,
                site_id=siteId,
                serial_number=serial_number,
                defaults={
                    "model_name": model_name,
                    "expected_quantity": expected_quantity,
                    "is_found": False,
                    "is_in_mobinet": True,
                    "approval_date": date.today(),
                    "srn_number": "",
                    "remarks": "",
                }
            )

        return Response({
            "status": "success",
            "message": "Data saved successfully"
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['DELETE'])
def empty_my_model(request):
    try:
        DismantleModelData.objects.all().delete()
        deleted_count, _ = DismantleCircleData.objects.all().delete()

        return Response(
            {
                "message": "All records deleted successfully",
                "deleted_count": deleted_count
            },
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def mobinet_data_submit_by_circle(request):
    circle = request.data.get("circle")
    siteId = request.data.get("siteId")
    records = request.data.get("data", [])
    remark = request.data.get("remark")

    if not circle or not siteId or not remark:
        return Response({"message": "siteId/circle/remark not provided"}, status=400)

    if not records:
        return Response({"message": "No data provided"}, status=400)

    try:
        existing_obj = DismantleCircleData.objects.filter(
            circle=circle,
            site_id=siteId
        ).first()
        
        def parse_bool(value):
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                return value.strip().lower() in ["true", "1", "yes"]
            if isinstance(value, int):
                return value == 1
            return False

        if existing_obj and existing_obj.is_surveyed:
            if isinstance(records, str):
                records = json.loads(records)
            
            flag = True

            for record in records:

                model_name = record.get("Model")
                expected_quantity = record.get("Expected Quantity")
                serial_number = record.get("Serial Number")
                is_found = parse_bool(record.get("Is Found"))
                is_in_mobinet = parse_bool(record.get("Is In Mobinet"))
                
                if not is_found:
                    continue

                srn_number = record.get("SRN Number")
                remarks = record.get("Remarks")
                
                if not srn_number or srn_number.strip() == "":
                    flag = False

                # ✅ UPSERT HERE
                DismantleModelData.objects.filter(
                    zone=circle, 
                    site_id=siteId, 
                    model_name=model_name, 
                    serial_number=serial_number, 
                    is_in_mobinet=is_in_mobinet
                ).update(
                    srn_number = srn_number,
                    remarks = remarks,
                )
                
            DismantleCircleData.objects.filter(
                circle=circle,
                site_id=siteId
            ).update(
                is_srn_done = date.today() if flag else None,
                remarks="SRN Done" if flag else "SRN Pending"
            )
            
            return Response({"message": "Survey already done. No changes made"})

        DismantleCircleData.objects.filter(
            circle=circle,
            site_id=siteId
        ).update(
            is_surveyed=date.today() if remark == "Survey done" else None,
            remarks=remark
        )
        if remark.strip().lower() == "survey done":
          send_survey_done_email(circle, siteId)
        
        # if not records:
        #     return Response({"message" : "Site not surveyed"})

        # ✅ Safe json load
        if isinstance(records, str):
            records = json.loads(records)

        for record in records:

            model_name = record.get("Model")
            expected_quantity = record.get("Expected Quantity")
            serial_number = record.get("Serial Number")
            is_found = parse_bool(record.get("Is Found"))
            is_in_mobinet = parse_bool(record.get("Is In Mobinet"))

            approval_date = record.get("Approval Date")

            if approval_date:
                try:
                    approval_date = datetime.strptime(approval_date, "%Y-%m-%d").date()
                except:
                    approval_date = date.today()
            else:
                approval_date = date.today()

            srn_number = record.get("SRN Number")
            remarks = record.get("Remarks")

            # ✅ UPSERT HERE
            DismantleModelData.objects.update_or_create(
                zone=circle,
                site_id=siteId,
                model_name=model_name,
                serial_number=serial_number,
                is_in_mobinet=is_in_mobinet,
                defaults={
                    "expected_quantity": expected_quantity,
                    "approval_date": approval_date,
                    "is_found": is_found,
                    "srn_number": srn_number,
                    "remarks": remarks,
                }
            )

       
        return Response({
            "status": "success",
            "message": "Data saved successfully"
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(['POST'])   
def delete_site_in_sitelist(request):
    site_id=request.data.get("site_id")
    if not site_id:
        return Response({"status":True,"message":"Site id is required"})

    try:
        obj = DismantleCircleData.objects.get(site_id=site_id)
        obj.delete()

        return Response(
            {
                "status": True,
                "message": "Deleted successfully"
            },
            status=status.HTTP_200_OK
        )

    except DismantleCircleData.DoesNotExist:
        return Response(
            {
                "status": False,
                "message": "Record not found for this ID"
            },
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
def fetch_model_name(request):
    circle = request.data.get('circle')

    if not circle:
        return Response({"message": "circle not provided"}, status=400)

    try:
        mobinet_folder = os.path.join(main_folder, 'mobinet')

        expected_filename_prefix = f"{circle}"

        mobinet_files = [
            f for f in os.listdir(mobinet_folder)
            if f.startswith(expected_filename_prefix)
        ]

        if not mobinet_files:
            return Response({"error": "Mobinet file not found"}, status=400)

        mobinet_path = os.path.join(mobinet_folder, mobinet_files[0])

        # Read only Model column (optimized)
        if mobinet_path.endswith(".csv"):
            mobinet_df = pd.read_csv(
                mobinet_path,
                usecols=["Model"]
            )
        elif mobinet_path.endswith((".xls", ".xlsx")):
            mobinet_df = pd.read_excel(
                mobinet_path,
                usecols=["Model"],
                engine="openpyxl"
            )
        else:
            return Response({"error": "Unsupported mobinet file format"}, status=400)

        # Clean data
        mobinet_df["Model"] = mobinet_df["Model"].astype(str).str.strip()

        # Remove null/invalid values
        mobinet_df = mobinet_df[
            mobinet_df["Model"].notna() &
            (~mobinet_df["Model"].isin(["", "-", "_", "N/A", "NaN", "Nan", "undefined"]))
        ]

        # Get unique models sorted
        unique_models = sorted(mobinet_df["Model"].unique().tolist())

        return Response({"models": unique_models}, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    

@api_view(['POST'])
def master_file_download(request):
 
    circle_qs = DismantleCircleData.objects.all().values(
        "circle",
        "site_id",
        "partner_code",
        "partner",
        "is_approved",
        "is_surveyed",
        "is_srn_done",
        "remarks"
    )

 
    model_qs = DismantleModelData.objects.all().values(
        "zone",
        "site_id",
        "model_name",
        "serial_number",
        "expected_quantity",
        "is_in_mobinet",
        "is_found",
        "approval_date",
        "srn_number"
    )

    circle_df = pd.DataFrame(list(circle_qs))
    model_df = pd.DataFrame(list(model_qs))

  
    df = pd.merge(
        circle_df,
        model_df,
        left_on=["circle", "site_id"],
        right_on=["zone", "site_id"],
        how="left"
    )

 
    df = df.rename(columns={
        "circle": "Circle",
        "site_id": "Site ID",
        "partner": "Partner",
        "partner_code": "Partner Code",
        "model_name": "NMS Model",
        "serial_number": "Serial Number",
        "expected_quantity": "NMS Quantity",
        "is_in_mobinet": "NMS Remarks",
        "is_found": "Is Material Found in Survey",
        "is_approved": "NMS Fetch Date",
        "is_surveyed": "Survey Date",
        "srn_number": "SRN Number",
        "is_srn_done": "SRN Date",
        "remarks": "Current Status"
    })


    df = df[
        [
            "Circle",
            "Site ID",
            "Partner",
            "Partner Code",
            "NMS Model",
            "Serial Number",
            "NMS Quantity",
            "NMS Remarks",
            "Is Material Found in Survey",
            "NMS Fetch Date",
            "Survey Date",
            "SRN Number",
            "SRN Date",
            "Current Status"
        ]
    ]
    
    df["Is Material Found in Survey"] = df["Is Material Found in Survey"].map({
        True: "Yes",
        False: "No"
    })
    
    df["NMS Remarks"] = df["NMS Remarks"].map({
        True: "No change",
        False: "Additional"
    })

 
    df = df.fillna("")
    
    BASE_URL = os.path.join(settings.MEDIA_ROOT, "degrow_dismantle")
    os.makedirs(BASE_URL, exist_ok=True)

    output_folder = os.path.join(BASE_URL, f"dismantle_master_file")
    shutil.rmtree(output_folder, ignore_errors=True)
    os.makedirs(output_folder, exist_ok=True)

    dashboard_file_path = os.path.join(
        output_folder,
        f"DISMANTLE_MASTER_FILE.xlsx"
    )

    with pd.ExcelWriter(dashboard_file_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='DISMANTLE_MASTER_FILE')
    format_excel(dashboard_file_path)

    dashboard_file_path = dashboard_file_path.replace(
        settings.MEDIA_ROOT, settings.MEDIA_URL
    ).replace("\\", "/")

    download_link = request.build_absolute_uri(dashboard_file_path)
    
  
    data = df.to_dict(orient="records")

    return Response({
        "download_link": download_link,
        "data": data
    }, status=200)

# fatch Site list in mobinate file and Database---
@api_view(["POST"])
def fetch_sites(request):
    circle = request.data.get("circle")
    siteId = request.data.get("siteId")

    try:
        # ---------------- 1️⃣ DB SITES ----------------
        queryset = DismantleModelData.objects.all()

        if circle:
            queryset = queryset.filter(zone__iexact=circle)

        if siteId:
            queryset = queryset.filter(site_id__icontains=siteId)

        db_sites = list(
            queryset.values_list("site_id", flat=True).distinct()
        )

        # ---------------- 2️⃣ FILE SITES ----------------
        file_sites = []

        if circle:
            mobinet_folder = os.path.join(main_folder, 'mobinet')

            mobinet_files = [
                f for f in os.listdir(mobinet_folder)
                if f.startswith(circle)
            ]

            if mobinet_files:
                mobinet_path = os.path.join(mobinet_folder, mobinet_files[0])

                if mobinet_path.endswith(".csv"):
                    df = pd.read_csv(
                        mobinet_path,
                        usecols=["Zone", "Parent Site"]
                    )
                elif mobinet_path.endswith((".xls", ".xlsx")):
                    df = pd.read_excel(
                        mobinet_path,
                        usecols=["Zone", "Parent Site"],
                        engine="openpyxl"
                    )
                else:
                    df = None

                if df is not None:
                    df["Zone"] = df["Zone"].astype(str).str.strip()
                    df["Parent Site"] = df["Parent Site"].astype(str).str.strip()

                    df = df[df["Zone"] == circle]

                    # Extract siteId from "Parent Site" → format: siteId_circle
                    df["site_clean"] = df["Parent Site"].apply(
                        lambda x: x.split("_")[0] if "_" in x else x
                    )

                    if siteId:
                        df = df[df["site_clean"].str.contains(siteId, case=False, na=False)]

                    file_sites = df["site_clean"].dropna().unique().tolist()

        # ---------------- 3️⃣ MERGE + UNIQUE ----------------
        all_sites = list(set(db_sites + file_sites))

        # Optional: sort for consistency
        all_sites = sorted(all_sites)

        # ---------------- 4️⃣ LIMIT ----------------
        return Response({
            "status": True,
            "data": all_sites[:10],
            "message": "Sites fetched (DB + File)"
        }, status=200)

    except Exception as e:
        return Response({
            "status": False,
            "error": str(e)
        }, status=500)
    

# api for  add mail----------------------------------------
@api_view(["POST"])
def add_mail(request):
    mail_type = request.data.get("mail_type")
    mail_input = request.data.get("mailid")  
 
    if not mail_type or not mail_input:
        return Response(
            {"status": False, "message": "mail_type and mailids required"},
            status=400
        )
 
    if mail_type not in ["TO", "CC"]:
        return Response(
            {"status": False, "message": "mail_type must be TO or CC"},
            status=400
        )
 
    if isinstance(mail_input, str):
        mail_ids = mail_input.replace(",", " ").split()
    else:
        mail_ids = mail_input
 
    added = []
    already_exists = []
 
    for mail in mail_ids:
        mail = mail.strip()
 
        if EmailList.objects.filter(email=mail).exists():
            already_exists.append(mail)
            continue
 
        EmailList.objects.create(email=mail, email_type=mail_type)
        added.append(mail)
 
    return Response({
    "status": True,
    "message": f"{len(added)} mail(s) added successfully and {len(already_exists)} already exist",
    "added_emails": added,
    "already_exists": already_exists
})
 

@api_view(["GET"])
def get_to_mails(request):
    email_type = request.data.get("email_type", "TO")

    mails = EmailList.objects.filter(email_type=email_type).values("id", "email_type", "email")

    return Response({
        "status": True,
        "data": list(mails)
    })


@api_view(["GET"])
def get_cc_mails(request):
    email_type = request.data.get("email_type", "CC")
    mails = EmailList.objects.filter(email_type=email_type).values("id", "email_type", "email")
    return Response({
        "status": True,
        "data": list(mails)
    })



@api_view(["POST"])
def delete_mail_id(request):
    mail_id = request.data.get("mailid")  

    if not mail_id:
        return Response(
            {"status": False, "message": "mailid required"},
            status=400
        )

    try:
        obj = EmailList.objects.get(email=mail_id)
        obj.delete()

        return Response({
            "status": True,
            "message": "Email deleted successfully"
        })

    except EmailList.DoesNotExist:
        return Response(
            {"status": False, "message": "Email not found"},
            status=404
        )


        
# api for add model------------------------------------
@api_view(["POST"])
def add_model(request):
    model_input = request.data.get("model")
 
    if not model_input:
        return Response(
            {"status": False, "message": "model required"},
            status=400
        )
 
    if isinstance(model_input, str):
        model_list = model_input.replace(",", " ").split()
    else:
        model_list = model_input
 
    added = []
    already_exists = []
 
    for model_name in model_list:
        model_name = model_name.strip()
 
        if AddModel.objects.filter(model_name__iexact=model_name).exists():
            already_exists.append(model_name)
            continue
 
        AddModel.objects.create(model_name=model_name)
        added.append(model_name)
 
    return Response({
        "status": True,
        "message": f"{len(added)} added & {len(already_exists)} already exist",
        "added_models": added,
        "already_exists": already_exists
    })


@api_view(["GET"])
def get_model(request):

    models = AddModel.objects.all().values("id", "model_name")

    return Response({
        "status": True,
        "data": list(models)
    })



@api_view(["POST"])
def delete_model(request):
    model_name = request.data.get("model")
    if not model_name:
        return Response(
            {"status": False, "message": "model_name required"},
            
        )

    try:
        obj = AddModel.objects.get(model_name=model_name)
        obj.delete()

        return Response({
            "status": True,
            "message": "Model deleted successfully"
        })

    except AddModel.DoesNotExist:
        return Response(
            {"status": False, "message": "Model not found"},
            
        )
