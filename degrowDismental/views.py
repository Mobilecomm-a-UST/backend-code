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
   
# UPLOAD RFS FILES
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
   

# UPLOAD MSMF FILES
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