import os
from django.conf import settings
from rest_framework.decorators import api_view , parser_classes
from rest_framework.response import Response
import pandas as pd
import warnings
from pathlib import Path
import stat
import shutil
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
import datetime
from openpyxl.styles import Alignment, PatternFill, Font, Border, Side
from openpyxl.utils import get_column_letter
import pandas as pd
from datetime import datetime
# from .models import MobinetDump
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from pyxlsb import open_workbook


def write_df_in_chunks(df, writer, sheet_name, chunk_size=100000):
    """
    Write a large DataFrame to Excel in chunks to avoid memory/time issues.
    """
    row_start = 0
    for start in range(0, len(df), chunk_size):
        end = start + chunk_size
        chunk = df.iloc[start:end]

        # Only write header for the first chunk
        header = (start == 0)

        chunk.to_excel(
            writer,
            sheet_name=sheet_name,
            index=False,
            header=header,
            startrow=row_start
        )

        row_start += len(chunk) + (1 if header else 0)


def safe_write(df, writer, sheet_name, threshold=50000, chunk_size=100000):
    """
    Automatically decide whether to write normally or in chunks.
    """
    if len(df) > threshold:
        write_df_in_chunks(df, writer, sheet_name, chunk_size=chunk_size)
    else:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
 
 
 
 
# Excel  formate  function.........  
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
# def final_excel(df, writer, sheet_name='Sheet1', fast_mode=False):
#     df.to_excel(writer, index=False, sheet_name=sheet_name)
#     ws = writer.sheets[sheet_name]
 
#     if fast_mode:
#         # Only style the header for large files
#         header_fill = PatternFill(start_color='FFFF00', fill_type='solid')
#         bold = Font(bold=True)
#         align = Alignment(horizontal='center', vertical='center')
#         border = Border(*[Side(style='thin')] * 4)
 
#         for col_idx, col in enumerate(df.columns, start=1):
#             cell = ws.cell(row=1, column=col_idx)
#             cell.fill = header_fill
#             cell.font = bold
#             cell.alignment = align
#             cell.border = border
#         return  # Skip data cell styling
#     else:
#         # Full formatting (original logic)
#         header_fill = PatternFill(start_color='FFFF00', fill_type='solid')
#         bold = Font(bold=True)
#         align = Alignment(horizontal='center', vertical='center')
#         border = Border(*[Side(style='thin')] * 4)
 
#         for col_idx, col in enumerate(df.columns, start=1):
#             cell = ws.cell(row=1, column=col_idx)
#             cell.fill = header_fill
#             cell.font = bold
#             cell.alignment = align
#             cell.border = border
#             ws.row_dimensions[1].height = 25
 
#         for col_idx, col in enumerate(df.columns, 1):
#             max_len = len(col)
#             for row in range(2, ws.max_row + 1):
#                 cell = ws.cell(row=row, column=col_idx)
#                 cell.alignment = align
#                 cell.border = border
#                 if cell.value:
#                     max_len = max(max_len, len(str(cell.value)))
#             ws.column_dimensions[get_column_letter(col_idx)].width = max_len + 2
 
       
# Delete the existing file function_______________
def delete_existing_files(folder_path):
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
               
# Read the both  excel and csv file function___________
def read_file(file):
    filename = file.name.lower()
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file, engine='openpyxl')
        else:
            raise ValueError("supported only csv and excel file")
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        raise ValueError(f"Error reading file '{file.name}': {str(e)}")          
   
   
#--main folder in media folder--------------------
main_folder = os.path.join(MEDIA_ROOT, 'Mobinet_CATs_TOOL')
os.makedirs(main_folder, exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
 
# API Delete singal file from current folder ---------
@api_view(['DELETE'])
def delete_single_mobinet_file(request):
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
 
# API to upload and manage Mobinet dumps--------
@api_view(['POST', 'GET' , 'DELETE'])
def upload_mobinet_dumps(request):
    try:
        mobinet_data_path = os.path.join(main_folder, 'mobinet_dump_data')
        os.makedirs(mobinet_data_path, exist_ok=True)
 
        if request.method == 'POST':
            files = request.FILES.getlist('files')
            # files = request.FILES.getlist('mobinet_dumps')
            if not files:
                return Response({'error': 'No files uploaded'}, status=status.HTTP_400_BAD_REQUEST)
 
            for f in files:
                file_path = os.path.join(mobinet_data_path, f.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
 
            return Response({'status': True, 'message': 'Files uploaded and saved successfully'}, status=status.HTTP_200_OK)
 
        elif request.method == 'GET':
            if not os.path.exists(mobinet_data_path):
                return Response({'files': []}, status=status.HTTP_200_OK)
 
            files = os.listdir(mobinet_data_path)
            return Response({
                'status': True,
                'message': f'{len(files)} Files found in mobinet_dump_data folder',
                'files': files,
                }, status=status.HTTP_200_OK)
           
        elif request.method == 'DELETE':
            if not os.path.exists(mobinet_data_path):
                return Response({'error': 'Folder does not exist'}, status=status.HTTP_404_NOT_FOUND)
 
            deleted_files = []
            for filename in os.listdir(mobinet_data_path):
                file_path = os.path.join(mobinet_data_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    deleted_files.append(filename)
 
            return Response({
                'status': True,
                'message': f'{len(deleted_files)} Files deleted successfully',
                'deleted_files': deleted_files
            }, status=status.HTTP_200_OK)
           
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
    #Api to upload and manage RFS(CATS) ends here-----------
@api_view(['POST', 'GET', 'DELETE'])
def upload_rfs_data(request):
    try:
        rfs_data_path = os.path.join(main_folder, 'rfs_data')
        os.makedirs(rfs_data_path, exist_ok=True)
 
        if request.method == 'POST':
            files = request.FILES.getlist('files')
            if not files:
                return Response({'error': 'No files uploaded'}, status=status.HTTP_400_BAD_REQUEST)
 
            for f in files:
                file_path = os.path.join(rfs_data_path, f.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
 
            return Response({'status': True, 'message': 'Files saved successfully'}, status=status.HTTP_200_OK)
       
        elif request.method == 'GET':
            if not os.path.exists(rfs_data_path):
                return Response({'files': []}, status=status.HTTP_200_OK)
            files = os.listdir(rfs_data_path)
            return Response({
                'status': True,
                'message': 'Files found in rfs_data folder',
                'files': files,
            }, status=status.HTTP_200_OK)
           
        elif request.method == 'DELETE':
            if not os.path.exists(rfs_data_path):
                return Response({'error': 'Folder does not exist'}, status=status.HTTP_404_NOT_FOUND)
            deleted_files = []
            for filename in os.listdir(rfs_data_path):
                file_path = os.path.join(rfs_data_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    deleted_files.append(filename)
 
            return Response({
                'status': True,
                'message': 'Files deleted successfully',
                'deleted_files': deleted_files  }, status=status.HTTP_200_OK)
       
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
# api to upload and manage MSMF ends here-----------  
@api_view(['POST', 'GET', 'DELETE'])  
def upload_msmf_data(request):
    try:
        msmf_folder_path = os.path.join(main_folder, 'msmf_data')
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
                'message': 'Files found in msmf_data folder',
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
   
    #api for locator file  data ends here-----------
@api_view(['POST', 'GET', 'DELETE'])
def upload_locator_data(request):
    try:
        locator_folder_path = os.path.join(main_folder, 'locator_data')
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
   
#api to upload and manage stock report data ends here-----------
@api_view(['POST', 'GET', 'DELETE'])
def upload_stock_report_data(request):
    stock_report_folder_path = os.path.join(main_folder, 'stock_report_data')
    os.makedirs(stock_report_folder_path, exist_ok=True)
    try:
        if request.method == 'POST':
            files = request.FILES.getlist('files')
            if not files:
                return Response({'error': 'No files uploaded'}, status=status.HTTP_400_BAD_REQUEST)
 
            for f in files:
                file_path = os.path.join(stock_report_folder_path, f.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
 
            return Response({'status': True, 'message': 'Files saved successfully'}, status=status.HTTP_200_OK)
        elif request.method == 'GET':
            if not os.path.exists(stock_report_folder_path):
                return Response({'files': []}, status=status.HTTP_200_OK)
            files = os.listdir(stock_report_folder_path)
            return Response({
                'status': True,
                'message': 'Files found in stock_report_data folder',
                'files': files,
            }, status=status.HTTP_200_OK)    
           
        elif request.method == 'DELETE':
            if not os.path.exists(stock_report_folder_path):
                return Response({'error': 'Folder does not exist'}, status=status.HTTP_404_NOT_FOUND)
            deleted_files = []
            for filename in os.listdir(stock_report_folder_path):
                file_path = os.path.join(stock_report_folder_path, filename)
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
         
 
 
 
       
# Frist Api for mobinet_dump site_match and hw_files-------------
@api_view(['POST'])
def mobinet_dump(request):
    print("Start Process_________")
    try:
        # Read files from mobinet_dump_data folder-------------
        mobinet_log_folder = os.path.join(main_folder, 'mobinet_dump_data')
 
        if not os.path.exists(mobinet_log_folder):
            return Response({"error": "mobinet_dump_data folder not found"}, status=400)
 
        log_df_list = []
        for file in os.listdir(mobinet_log_folder):
            file_path = os.path.join(mobinet_log_folder, file)
 
            if not os.path.isfile(file_path):
                continue  # skip subfolders
 
            try:
                if file_path.endswith('.csv'):
                   df = pd.read_csv(file_path)
                elif file_path.endswith(('.xls', '.xlsx')):
                    df = pd.read_excel(file_path, engine='openpyxl')
                else:
                    return Response({"error": f"Unsupported file format: {file}"}, status=400)
                log_df_list.append(df)
            except Exception as e:
                return Response({"error": f"Error in file {file}: {str(e)}"}, status=500)
 
        if not log_df_list:
            return Response({"error": "No valid log files found"}, status=400)
 
        log_df = pd.concat(log_df_list, ignore_index=True)
        print("Concatenated log_df columns:", log_df.columns)
       
       
       
 
        # Read site list file (CSV or Excel)
        site_list_file = request.FILES.get("site_list")
        if not site_list_file:
            return Response({"error": "site_list file not provided"}, status=400)
 
        try:
            site_df = read_file(site_list_file)
            site_df.columns = site_df.columns.str.strip()
            print(site_df)
        except ValueError as e:
            return Response({"error": str(e)}, status=500)
 
        # Read multiple hw_files
        # hw_files = request.FILES.getlist("hw_file")
        # if not hw_files:
        #     return Response({"error": "hw_files not provided"}, status=400)
 
        # hw_df_list = []
        # for hw_file in hw_files:
        #     try:
        #         df = read_file(hw_file)
        #         df.columns = df.columns.str.strip()
        #         hw_df_list.append(df)
        #     except Exception as e:
        #         return Response({"error": f"Error reading one of the hw_files: {str(e)}"}, status=500)
 
        # hw_df = pd.concat(hw_df_list, ignore_index=True)
 
        # Strip and match values
        log_df['Parent Site'] = log_df['Parent Site'].astype(str).str.strip()
        site_df['Unique ID'] = site_df['Unique ID'].astype(str).str.strip()
 
        # Merge logs with site list
        matched_df = pd.merge(
            log_df,
            site_df[['Unique ID', 'Dismantled date']],
            how='inner',
            left_on='Parent Site',
            right_on='Unique ID'
        )
        print("Matched DF:")
        print(matched_df)
 
        # Unmatched sites
        unmatched_df = site_df.loc[
            ~site_df['Unique ID'].isin(log_df['Parent Site']), ['Unique ID']
        ].copy()
        unmatched_df.rename(columns={'Unique ID': 'Unmatched Unique ID'}, inplace=True)
        print("Unmatched Unique IDs:")
        print(unmatched_df)
 
        # Merge with HW file
        #   matched_df = pd.merge(
        #     matched_df,
        #     hw_df[['Module Name', 'ITEMCODE']],
        #     how='outer',
        #     left_on='Board Model',
        #     right_on='Module Name'
        # )
        #   matched_df.drop(columns='Module Name', inplace=True)
 
        # Remove blank and '-' data in serial number
        matched_df = matched_df[
              matched_df['Serial Number'].notna() &
            (  matched_df['Serial Number'].astype(str).str.strip() != '') &
            (  matched_df['Serial Number'].astype(str).str.strip() != '-')
        ]
 
        matched_df['Site+Module'] =   matched_df['Parent Site'].astype(str).str.strip() + "_" +   matched_df['Board Model'].astype(str).str.strip()
        matched_df['Site+Serial'] =   matched_df['Parent Site'].astype(str).str.strip() + "_" +   matched_df['Serial Number'].astype(str).str.strip()
        matched_df.drop_duplicates(subset='Serial Number', inplace=True)
 
        # Count serial numbers per Site+Module
        data_count =   matched_df.copy()
        summary_df = (
            data_count.groupby("Site+Module", as_index=False)
            .agg({"Serial Number": "count"})
            .rename(columns={"Serial Number": "Serial Number_count"})
        )
        print("Summary DF:")
        print(summary_df)
 
        # Export Excel
        output_dir = os.path.join(main_folder, 'Final_Mobinet_Summary_output')
        os.makedirs(output_dir, exist_ok=True)
        delete_existing_files(output_dir)
 
        filename = f"mobinet_summary_data_{timestamp}.xlsx"
        output_path = os.path.join(output_dir, filename)
 
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            safe_write(summary_df, writer, sheet_name='Mobinet_Summary')
            safe_write(data_count, writer, sheet_name='Mobinet_Backup_Data')
            safe_write(unmatched_df, writer, sheet_name='Unmatched_Site_IDs')
 
        # Generate download URL
        relative_path = os.path.relpath(output_path, MEDIA_ROOT)
        download_url = request.build_absolute_uri(os.path.join(MEDIA_URL, relative_path).replace("\\", "/"))
        print("End Process_________")
 
        return Response({
            "status": True,
            "message": "File saved successfully",
            "download_url": download_url
        })
 
    except Exception as e:
        return Response({"error": f"find an error: {str(e)}"}, status=500)
 
   
   
   
# Second Api for CATs(rfs) and Locator files and hw files-------------
# Second Api for CATs(rfs) and Locator files and hw files-------------
@api_view(['POST'])
def rfs_dump(request):
    print("Start Process_________")
    try:
        # RFS File
        rfs_folder = os.path.join(main_folder, 'rfs_data')
        if not os.path.exists(rfs_folder):
            return Response({"error": "rfs_data folder not found"}, status=400)
       
        for file in os.listdir(rfs_folder):
            rfs_file_path = os.path.join(rfs_folder, file)
            if not os.path.isfile(rfs_file_path):
                continue
            try:
                if rfs_file_path.endswith('.csv'):
                    rfs_df = pd.read_csv(rfs_file_path)
                elif rfs_file_path.endswith(('.xls', '.xlsx')):
                    rfs_df = pd.read_excel(rfs_file_path, engine='openpyxl')    
                elif rfs_file_path.endswith('.xlsb'):
                    with open_workbook(rfs_file_path) as wb:
                        with wb.get_sheet(wb.sheets[0]) as sheet:
                            data = []
                            for row in sheet.rows():
                                data.append([item.v for item in row])
                            rfs_df = pd.DataFrame(data[1:], columns=data[0])  
                else:
                    return Response({"error": f"Unsupported file format: {file}"}, status=400)  
                rfs_df.columns = rfs_df.columns.str.strip()
                print("RFS Data columns:", rfs_df.columns)
            except Exception as e:
                return Response({"error": f"error reading rfs file: {str(e)}"}, status=500)
           
       
        #OLM ID File------------------------------------------------------------``
        olm_id_file = request.FILES.get("olm_id_file")
        if not olm_id_file:
            return Response({"error": "olm_id_file not provided"}, status=400)
        try:
            if olm_id_file.name.endswith('.csv'):
                olm_id_df = pd.read_csv(olm_id_file, usecols=['OLM ID', 'Partner'])
            elif olm_id_file.name.endswith(('.xls', '.xlsx')):
                olm_id_df = pd.read_excel(olm_id_file, engine='openpyxl', usecols=['OLM ID', 'Partner'])
            else:
                return Response({"error": "Invalid file format for olm_id_file"}, status=400)
            olm_id_df.columns = olm_id_df.columns.str.strip()
            print(olm_id_df.columns)
        except Exception as e:
            return Response({"error": f"error reading olm_id_file: {str(e)}"}, status=500)
 
        #  Multiple HW Files--------------------------------------------------
        hw_files = request.FILES.getlist("hw_file")
        if not hw_files:
            return Response({"error": "hw_file(s) not provided"}, status=400)
 
        hw_df_list = []
        for hw_file in hw_files:
            try:
                if hw_file.name.endswith('.csv'):
                    df = pd.read_csv(hw_file, usecols=['ITEMCODE', 'Module Name'])
                elif hw_file.name.endswith(('.xls', '.xlsx')):
                 df = pd.read_excel(hw_file, engine='openpyxl', usecols=['ITEMCODE', 'Module Name'])
                else:
                    return Response({"error": "Unsupported file format for hw_file"}, status=400)
                df.columns = df.columns.str.strip()
                hw_df_list.append(df)
            except Exception as e:
                return Response({"error": f"error reading a hw_file: {str(e)}"}, status=500)
        hw_df = pd.concat(hw_df_list, ignore_index=True).drop_duplicates()
        print(hw_df.columns)
 
        #  Site List File-----------------------------------------------------------
        site_list_file = request.FILES.get("site_list_file")
        if not site_list_file:
            return Response({"error": "site_list_file not provided"}, status=400)
        try:
            if site_list_file.name.endswith('.csv'):
                site_list_df = pd.read_csv(site_list_file)
            elif site_list_file.name.endswith(('.xls', '.xlsx')):
              site_list_df = pd.read_excel(site_list_file, engine='openpyxl', usecols=['Unique ID', 'Dismantled date'])
            site_list_df.columns = site_list_df.columns.str.strip()
            print(site_list_df.columns)
        except Exception as e:
            return Response({"error": f"error reading site_list_file: {str(e)}"}, status=500)
 
        # Multiple Locator Files -------------------------------------------------
        locator_folder = os.path.join(main_folder, 'locator_data')
        if not os.path.exists(locator_folder):
            return Response({"error": "locator_data folder not found"}, status=400)
       
        locator_df_list = []
        for file in os.listdir(locator_folder):
            locator_file_path = os.path.join(locator_folder, file)
            if not os.path.isfile(locator_file_path):
                continue
            try:
                if locator_file_path.endswith('.csv'):
                    df = pd.read_csv(locator_file_path, usecols=['LOCATION_NAME', 'SITEID'])    
                elif locator_file_path.endswith(('.xls', '.xlsx')):
                    df = pd.read_excel(locator_file_path, engine='openpyxl', usecols=['LOCATION_NAME', 'SITEID'])
                elif locator_file_path.endswith('.xlsb'):
                    with open_workbook(locator_file_path) as wb:
                        with wb.get_sheet(wb.sheets[0]) as sheet:
                            data = []
                            for row in sheet.rows():
                                data.append([item.v for item in row])
                            df = pd.DataFrame(data[1:], columns=data[0])
                else:
                    return Response({"error": f"Unsupported file format: {file}"}, status=400)
                df.columns = df.columns.str.strip()
                locator_df_list.append(df)
            except Exception as e:
                return Response({"error": f"error reading locator file: {str(e)}"}, status=500)
        locator_df = pd.concat(locator_df_list, ignore_index=True).drop_duplicates()
        print(locator_df.columns)
           
     
    #    # Unmatched Sites...
    #     unmatched_sites = request.POST.getlist('unmatched_sites')
    #     if not unmatched_sites:
    #         return Response({"error": "unmatched_sites not provided"}, status=400)
    #     if len(unmatched_sites) == 1 and "\n" in unmatched_sites[0]:
    #      unmatched_sites = unmatched_sites[0].strip().split("\n")
    #     print("Aarry of unmatched_sites:",unmatched_sites)
    #     unmatched_sites_df = pd.DataFrame(unmatched_sites, columns=["Unmatched Sites"])
    #     print(unmatched_sites_df.head())
       
        # Mobinet Dump File--------------------------------------------
        mobinet_dump_file = request.FILES.get("mobinet_dump_file")
        if not mobinet_dump_file:
            return Response({"error": "mobinet_dump_file not provided"}, status=400)
        try:
            mobinet_output_df = pd.read_excel(mobinet_dump_file, engine='openpyxl', sheet_name='Mobinet_Summary')
            mobinet_output_df.columns = mobinet_output_df.columns.str.strip()
            mobinet_dump_df = pd.read_excel(mobinet_dump_file, engine='openpyxl',sheet_name='Mobinet_Backup_Data')
            mobinet_dump_df.columns = mobinet_dump_df.columns.str.strip()
            print(mobinet_dump_df.columns)
        except Exception as e:
            return Response({"error": f"error reading mobinet_dump_file: {str(e)}"}, status=500)
       
       
        #MS-MF file-----------------------------------------------
        msmf_folder = os.path.join(main_folder, 'msmf_data')
        if not os.path.exists(msmf_folder):
            return Response({"error": "msmf_data folder not found"}, status=400)
       
        for file in os.listdir(msmf_folder):
            msmf_file_path = os.path.join(msmf_folder, file)
            if not os.path.isfile(msmf_file_path):
                continue
            try:
                if msmf_file_path.endswith('.csv'):
                    msmf_df = pd.read_csv(msmf_file_path)
                elif msmf_file_path.endswith(('.xls', '.xlsx')):
                    msmf_df = pd.read_excel(msmf_file_path, engine='openpyxl')
                elif msmf_file_path.endswith('.xlsb'):
                    with open_workbook(msmf_file_path) as wb:
                        with wb.get_sheet(wb.sheets[0]) as sheet:
                            data = []
                            for row in sheet.rows():
                                data.append([item.v for item in row])
                            msmf_df = pd.DataFrame(data[1:], columns=data[0])
                else:
                    return Response({"error": f"Unsupported file format: {file}"}, status=400)
                   
                msmf_df.columns = msmf_df.columns.str.strip()
                print("MS-MF Data columns:", msmf_df.columns)
            except Exception as e:
                return Response({"error": f"error reading ms-mf file: {str(e)}"}, status=500)
           
       
       
           
       
        # stock-report_file -----------------------------------------------
        stock_report_folder=os.path.join(main_folder, 'stock_report_data')
        stock_report_df = None
        if not os.path.exists(stock_report_folder):
            return Response({"error": "stock_report_data folder not found"}, status=400)
       
        for file in os.listdir(stock_report_folder):
            stock_report_file_path = os.path.join(stock_report_folder, file)
            if not os.path.isfile(stock_report_file_path):
                continue
            try:
                if stock_report_file_path.endswith('.csv'):
                    stock_report_df = pd.read_csv(stock_report_file_path)
                elif stock_report_file_path.endswith(('.xls', '.xlsx')):
                    stock_report_df = pd.read_excel(stock_report_file_path, engine='openpyxl')
                elif stock_report_file_path.endswith('.xlsb'):
                    with open_workbook(stock_report_file_path) as wb:
                        with wb.get_sheet(wb.sheets[0]) as sheet:  # First sheet
                            data = []
                            for row in sheet.rows():
                                data.append([item.v for item in row])
                            stock_report_df = pd.DataFrame(data[1:], columns=data[0])
                stock_report_df.columns = stock_report_df.columns.str.strip()
                print("Stock Report Data columns:", stock_report_df.columns)
            except Exception as e:
                return Response({"error": f"error reading stock report file: {str(e)}"}, status=500)
       
 
   
       
########for RFS file#######################################
        # Circle Mapping ....
        circle_map_code = {
            151: 'AP', 132: 'BR',152: 'CN',111: 'DL',113: 'HR', 114: 'JK',
            153: 'KK', 174: 'MU', 172: 'MP',  134: 'OR', 115: 'PB', 176: 'RJ',
            116: 'UE', 117: 'UW', 135: 'WB', 136: 'KO', 155: 'TN',133: 'NE',131: 'AS'
        }
 
 
        #  Add Patner information---
        rfs_df["Patner"] = "Other TSP"
        rfs_df.loc[rfs_df["RFS_CREATED_BY"].isin(olm_id_df["OLM ID"]), "Patner"] = "Mobliecomm"
 
        # Merge with locator----
        merged_df = pd.merge(
            rfs_df,
            locator_df[['LOCATION_NAME', 'SITEID']],
            how='inner',
            left_on='FROMLOCATION',
            right_on='LOCATION_NAME',
            sort=False
        )
        print('marge with locator',merged_df.head())
       
        # Circle Mapping ----
        merged_df['Circle_Map'] = merged_df['FROMLOCATION'].astype(str).str[:3].astype(int)
        merged_df['Circle'] = merged_df['Circle_Map'].map(circle_map_code)
        merged_df['Unique Site ID'] = merged_df['SITEID'].astype(str) + "_" + merged_df['Circle'].astype(str)
        merged_df.drop(columns=['LOCATION_NAME', 'Circle_Map'], inplace=True)
       
     
 
        # Merge with HW File -----
        merged_hw = pd.merge(
            merged_df,
            hw_df,
            how='outer',
            on='ITEMCODE',
            sort=False
        )
        print('merge with Hardware',merged_hw.head())
 
        #  Merge with site list
        merged_site_df = pd.merge(
            merged_hw,
            site_list_df,
            how='inner',
            left_on='Unique Site ID',
            right_on='Unique ID',
            sort=False
        )
        merged_site_df.drop(columns=['Unique ID'], inplace=True)
        print('merge with site list file',merged_site_df.head())
       
        #  #data for unmatched site.
        # unmatched_data= merged_site_df[merged_site_df['Unique Site ID'].isin(unmatched_sites_df["Unmatched Sites"])]
        # unmatched_data["Remark"]="Unmatched Site"
        # print(unmatched_data.head())
       
 
 
        merged_site_df["Dismantled date"] = pd.to_datetime(merged_site_df["Dismantled date"], errors='coerce')
        merged_site_df["RFS_CREATED_DATE"] = pd.to_datetime(merged_site_df["RFS_CREATED_DATE"], errors='coerce')
 
        merged_site_df["Aging"] = (merged_site_df["Dismantled date"] - merged_site_df["RFS_CREATED_DATE"]).dt.days
        merged_site_df = merged_site_df[merged_site_df["Aging"].between(-45, 45, inclusive="both")]
 
       
        merged_site_df["Site+Module"] = merged_site_df["Unique Site ID"].astype(str) + "_" + merged_site_df["Module Name"].astype(str)
        merged_site_df.drop_duplicates(inplace=True)
       
       
 
       
       
        #work on serial number----------------------------------------------------------
        rfs_matched_sn =merged_site_df.copy()
        rfs_matched_sn["Site+Serial"]= rfs_matched_sn["Unique Site ID"].astype(str) + "_" + rfs_matched_sn["SERIALNUMBER"].astype(str)
       
        #remove S from serial number
        rfs_matched_sn_2= rfs_matched_sn.copy()
        rfs_matched_sn_2["SERIALNUMBER"]=rfs_matched_sn_2["SERIALNUMBER"].str.replace(r'^[Ss]', '', regex=True)
        rfs_matched_sn_2["Site+Serial"]= rfs_matched_sn_2["Unique Site ID"].astype(str) + "_" + rfs_matched_sn_2["SERIALNUMBER"].astype(str)
       
        #merge with serial number from mobinet dump file
        rfs_matched_sn=pd.merge(
            rfs_matched_sn,
            mobinet_dump_df[['Site+Serial']],
            how='inner',
            on='Site+Serial',
        )
        rfs_matched_sn["Remark"] = "Matched by Serial Number"
       
        #merge without S serial number from mobinet dump file
        rfs_matched_sn_2=pd.merge(
            rfs_matched_sn_2,
            mobinet_dump_df[['Site+Serial']],
            how='inner',
            on='Site+Serial',
        )
        rfs_matched_sn_2["Remark"] = "Matched by Serial Number"
       
        rfs_matched_sn_merege=pd.concat([rfs_matched_sn, rfs_matched_sn_2], ignore_index=True)
        rfs_matched_sn_merege.drop_duplicates(inplace=True)
       
         
 # Merge with stock report file if provided-----------------------------------
        if stock_report_df is not None and not stock_report_df.empty:
            rfs_finally =merged_site_df.copy()
            rfs_with_stock_report = pd.merge(
            rfs_finally,
            stock_report_df[['LOT_MRR_NUMBER', 'CURRENTLOCATION', 'CURRENTSTATUS', 'LOCATION_TYPE', 'SUBINVENTORY', 'ORACLE_STOCK_LOCATOR']],
            left_on='ORACLE_LOT_NO',
            right_on='LOT_MRR_NUMBER',
            how='left',
            )  
            rfs_with_stock_report.drop(columns=['LOT_MRR_NUMBER'], inplace=True)
            rfs_with_stock_report.drop_duplicates(inplace=True)
            print("rfs_with_stock_report", rfs_with_stock_report)
            
        else:
            rfs_with_stock_report= merged_site_df.copy()     
    
       
       
# summary_df for RFS file------
        summary_df = (
            merged_site_df.groupby("Site+Module", as_index=False)
            .agg({
                "RECEIVED_QTY": "count",
                "RFS_QTY": "count",
                "SRNCAMREQSTATUS":lambda x: ", ".join(set(x)),
               
               
            })
            .rename(columns={
                "RECEIVED_QTY": "RECEIVED_QTY_COUNT(RFS_FILE)",
                "RFS_QTY": "RFS_QTY_COUNT(RFS_FILE)"
            })
        )
       
        print(summary_df)
    #######################################################################################
   
   
    #######for MS-MF file####################
        msmf_df["Patner"] = "Other TSP"
        msmf_df.loc[msmf_df["MS_CREATED_BY"].isin(olm_id_df["OLM ID"]), "Patner"] = "Mobliecomm"
 
        # Merge with locator----
        merged_df_ms_mf = pd.merge(
            msmf_df,
            locator_df[['LOCATION_NAME', 'SITEID']],
            how='inner',
            left_on='MS_FROMLOCATION',
            right_on='LOCATION_NAME',
            sort=False
        )
        print('marge with locator',merged_df_ms_mf.head())
       
        # Circle Mapping ----
        merged_df_ms_mf['Circle_Map'] = merged_df_ms_mf['MS_FROMLOCATION'].astype(str).str[:3].astype(int)
        merged_df_ms_mf['Circle'] = merged_df_ms_mf['Circle_Map'].map(circle_map_code)
        merged_df_ms_mf['Unique Site ID'] = merged_df_ms_mf['SITEID'].astype(str) + "_" + merged_df_ms_mf['Circle'].astype(str)
        merged_df_ms_mf.drop(columns=['LOCATION_NAME', 'Circle_Map'], inplace=True)
       
     
 
        # Merge with HW File -----
        merged_hw_ms_mf = pd.merge(
            merged_df_ms_mf,
            hw_df,
            how='outer',
            left_on='PARTCODE',
            right_on='ITEMCODE',
            sort=False
        )
        merged_hw_ms_mf.drop(columns=['ITEMCODE'], inplace=True)
 
        print('merge with Hardware',merged_hw_ms_mf.head())
 
        #  Merge with site list
        merged_site_df_ms_mf = pd.merge(
            merged_hw_ms_mf,
            site_list_df,
            how='inner',
            left_on='Unique Site ID',
            right_on='Unique ID',
            sort=False
        )
        merged_site_df_ms_mf.drop(columns=['Unique ID'], inplace=True)
        print('merge with site list file',merged_site_df_ms_mf.head())
       
        # #data for unmatched site.
        # unmatched_data_ms_mf= merged_site_df_ms_mf[merged_site_df_ms_mf['Unique Site ID'].isin(unmatched_sites_df["Unmatched Sites"])]
        # unmatched_data_ms_mf["Remark"]="Unmatched Site"
        # print(unmatched_data_ms_mf.head())
       
     
       
        merged_site_df_ms_mf["Dismantled date"] = pd.to_datetime(merged_site_df_ms_mf["Dismantled date"], errors='coerce')
        merged_site_df_ms_mf["MOVE_START_DATE"] = pd.to_datetime(merged_site_df_ms_mf["MOVE_START_DATE"], errors='coerce')
       
        merged_site_df_ms_mf["Aging"] = (merged_site_df_ms_mf["Dismantled date"] - merged_site_df_ms_mf["MOVE_START_DATE"]).dt.days
        merged_site_df_ms_mf = merged_site_df_ms_mf[merged_site_df_ms_mf["Aging"].between(-45, 45, inclusive="both")]
 
       
        merged_site_df_ms_mf["Site+Module"] = merged_site_df_ms_mf["Unique Site ID"].astype(str) + "_" + merged_site_df_ms_mf["Module Name"].astype(str)
        merged_site_df_ms_mf.drop_duplicates(inplace=True)
       
        #work with serial number----------------------------------------
        ms_mf_matched_sn =merged_site_df_ms_mf.copy()
        ms_mf_matched_sn["Site+Serial"]= ms_mf_matched_sn["Unique Site ID"].astype(str) + "_" + ms_mf_matched_sn["SERIAL_NUMBER"].astype(str)
         #remove S from serial number
        ms_mf_matched_sn_2= ms_mf_matched_sn.copy()
        ms_mf_matched_sn_2["SERIAL_NUMBER"]=ms_mf_matched_sn_2["SERIAL_NUMBER"].str.replace(r'^[Ss]', '', regex=True)
        ms_mf_matched_sn_2["Site+Serial"]= ms_mf_matched_sn_2["Unique Site ID"].astype(str) + "_" + ms_mf_matched_sn_2["SERIAL_NUMBER"].astype(str)
       
         
        #merge with serial number from mobinet dump file
        ms_mf_matched_sn=pd.merge(
            ms_mf_matched_sn,
            mobinet_dump_df[['Site+Serial']],
            how='inner',
            on='Site+Serial',
        )
       
        #merge without S serial number from mobinet dump file
        ms_mf_matched_sn_2=pd.merge(
            ms_mf_matched_sn_2,
            mobinet_dump_df[['Site+Serial']],
            how='inner',
            on='Site+Serial',
        )
       
        ms_mf_matched_sn_2["Remark"]="Matched by Serial Number"
        ms_mf_matched_sn["Remark"]="Matched by Serial Number"
       
        ms_mf_matched_merged=pd.concat([ms_mf_matched_sn, ms_mf_matched_sn_2], ignore_index=True)
        ms_mf_matched_merged.drop_duplicates(inplace=True)
       
       
   
       
       # summary of MS-MF file------
        ms_mf_data_cout =merged_site_df_ms_mf.copy()
       
        ms_mf_summary_df = (
            merged_site_df_ms_mf.groupby("Site+Module", as_index=False)
            .agg({
                "RECEIVED_QTY": "count",
                "QTY": "count"
            })
            .rename(columns={
                "RECEIVED_QTY": "RECEIVED_QTY_COUNT(MS-MF FILE)",
                "QTY": "RFS_QTY_COUNT(MS-MF FILE)"
            })
        )
       
        print("ms_mf_summary_df",ms_mf_summary_df)
     
    #merge summary_df and ms_mf_summary_df
        final_summary_df=pd.merge(
            summary_df,
            ms_mf_summary_df,
            how='outer',
            on='Site+Module',)
        print(final_summary_df)
       
        ## final Api work here-------------------------
        #site wise summary and circle wise summary data site wise  data count
        merged_find_summary = pd.merge(
            left=mobinet_output_df,
            right=final_summary_df[['Site+Module', 'RECEIVED_QTY_COUNT(RFS_FILE)' ,'RFS_QTY_COUNT(RFS_FILE)','RECEIVED_QTY_COUNT(MS-MF FILE)','RFS_QTY_COUNT(MS-MF FILE)','SRNCAMREQSTATUS']].copy(),  # include ITEMCODE here
            how='outer',
            on='Site+Module',
           
        )
        merged_find_summary['Unique ID'] = merged_find_summary['Site+Module'].str.split('_', expand=True)[0] + "_" + merged_find_summary['Site+Module'].str.split('_', expand=True)[1]
     #site wise summay----------------------------------------------
        site_wise_summary = (
        merged_find_summary
        .groupby('Unique ID', as_index=False)
        .agg({
            'Serial Number_count': 'sum',
            
            'RECEIVED_QTY_COUNT(RFS_FILE)': 'sum',
            'RECEIVED_QTY_COUNT(MS-MF FILE)': 'sum',
            'RFS_QTY_COUNT(RFS_FILE)': 'sum',
            'RFS_QTY_COUNT(MS-MF FILE)': 'sum',
          'SRNCAMREQSTATUS': 'first'
 
        })
        .assign(
            Total_In_CATS =lambda x:  x['RFS_QTY_COUNT(RFS_FILE)'] + x['RFS_QTY_COUNT(MS-MF FILE)'],
            Total_Receipt_CATS=lambda x: x['RECEIVED_QTY_COUNT(RFS_FILE)'] + x['RECEIVED_QTY_COUNT(MS-MF FILE)'],
            Dismantle_vs_SREQ=lambda x: x['Total_In_CATS'] - x['Serial Number_count'],
            SREQ_vs_WH_Receipt=lambda x:x['Total_Receipt_CATS'] - x['Total_In_CATS'],
           
            )
       
        .rename(columns={
            'Unique ID': 'Site ID',
            'Serial Number_count': 'Mobinet_Count(Serial Number)',
        })
    )
        print(site_wise_summary)
       
        #Circle wise summary----------------------------------------------
        merged_find_summary['Circle'] = merged_find_summary['Unique ID'].str.split('_', expand=True)[1]
       
        circle_wise_summary = (
            merged_find_summary
                .groupby('Circle', as_index=False)
                .agg({
                    'Serial Number_count': 'sum',
                    'RECEIVED_QTY_COUNT(RFS_FILE)': 'sum',
                    'RECEIVED_QTY_COUNT(MS-MF FILE)': 'sum',
                    'RFS_QTY_COUNT(RFS_FILE)': 'sum',
                    'RFS_QTY_COUNT(MS-MF FILE)': 'sum',
                    'SRNCAMREQSTATUS': 'first'
 
                })
               
            .assign(
                    Total_In_CATS =lambda x:  x['RFS_QTY_COUNT(RFS_FILE)'] + x['RFS_QTY_COUNT(MS-MF FILE)'],
                    Total_Receipt_CATS=lambda x: x['RECEIVED_QTY_COUNT(RFS_FILE)'] + x['RECEIVED_QTY_COUNT(MS-MF FILE)'],
                    Dismantle_vs_SREQ=lambda x: x['Total_In_CATS'] - x['Serial Number_count'],
                    SREQ_vs_WH_Receipt=lambda x:x['Total_Receipt_CATS'] - x['Total_In_CATS'],
                   
                    )
                .rename(columns={
                    'Serial Number_count': 'Mobinet_Count(Serial Number)',
               
                })
            )
        print(circle_wise_summary)
       
        #count of matched sites in mobinet and rfs file ms-mf------------------------
       
        site_count_mobinet = mobinet_dump_df['Parent Site'].value_counts()
        site_count_rfs =merged_site_df['Unique Site ID'].value_counts()
        site_count_msmf = ms_mf_data_cout['Unique Site ID'].value_counts()
 
        new_df = site_list_df[['Unique ID']].copy()
        new_df.rename(columns={'Unique ID': 'Site ID'}, inplace=True)
        new_df['SiteID in Mobinet'] = site_list_df['Unique ID'].map(site_count_mobinet).fillna(0).astype(int)
        new_df['SiteID in RFS'] = site_list_df['Unique ID'].map(site_count_rfs).fillna(0).astype(int)
        new_df['SiteID in MS-MF'] = site_list_df['Unique ID'].map(site_count_msmf).fillna(0).astype(int)
 
        print("new_df", new_df)
        print("End all files Process. Saving the data in excel file")
 
       
        output_dir = os.path.join(main_folder,'Finall_CATs_MSMF_Summary_Output')
        os.makedirs(output_dir, exist_ok=True)
        delete_existing_files(output_dir)
        filename = f"CATs_Summary_data{timestamp}.xlsx"
        output_path = os.path.join(output_dir, filename)
        with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
            safe_write(site_wise_summary, writer, "Site Wise Summary")
            safe_write(circle_wise_summary, writer, "Circle Wise Summary")
            safe_write(final_summary_df, writer, "CATs_MS-MF_Summary")
            safe_write(summary_df, writer, "CATs_Summary")
            safe_write(ms_mf_summary_df, writer, "MS-MF_Summary")
            safe_write(rfs_with_stock_report, writer, "CATs_Backup Data")
            safe_write(rfs_matched_sn_merege, writer, "CATs_Matched_by_SN")
            safe_write(ms_mf_data_cout, writer, "MS-MF_Backup Data")
            safe_write(ms_mf_matched_merged, writer, "MS-MF_Matched_by_SN")
            safe_write(new_df, writer, "SiteID Count Summary")

         
        relative_path = os.path.relpath(output_path, MEDIA_ROOT)
        download_url = request.build_absolute_uri(os.path.join(MEDIA_URL, relative_path).replace("\\", "/"))
        print("End Process_________")
       
        return Response({
            "status": True,
            "message": "File saved successfully",
            "download_url": download_url
        })
    except Exception as e:
        return Response({"error": f"find an error: {str(e)}"}, status=500)
    

#api for  Rfs mapping tool----------------------------------------
@api_view(["POST"])
def rfs_site_mapping(request):
    print("Start Process rfsmapping tool_________")
    try:
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

        # ----------------- RFS File -----------------
        rfs_folder = os.path.join(main_folder, "rfs_data")
        if not os.path.exists(rfs_folder):
            return Response({"error": "rfs_data folder not found"}, status=400)

        rfs_df = None
        for file in os.listdir(rfs_folder):
            rfs_file_path = os.path.join(rfs_folder, file)
            if not os.path.isfile(rfs_file_path):
                continue
            if rfs_file_path.endswith(".csv"):
                rfs_df = pd.read_csv(rfs_file_path, chunksize=50000)  # <-- chunked
            elif rfs_file_path.endswith((".xls", ".xlsx")):
                rfs_df = pd.read_excel(rfs_file_path, engine="openpyxl")
            else:
                return Response({"error": f"Unsupported file format: {file}"}, status=400)
        if rfs_df is None:
            return Response({"error": "No RFS file found"}, status=400)

        # ----------------- Locator Files -----------------
        locator_folder = os.path.join(main_folder, "locator_data")
        if not os.path.exists(locator_folder):
            return Response({"error": "locator_data folder not found"}, status=400)

        locator_df_list = []
        for file in os.listdir(locator_folder):
            locator_file_path = os.path.join(locator_folder, file)
            if not os.path.isfile(locator_file_path):
                continue
            if locator_file_path.endswith(".csv"):
                df = pd.read_csv(locator_file_path, usecols=["LOCATION_NAME", "SITEID"])
            elif locator_file_path.endswith((".xls", ".xlsx")):
                df = pd.read_excel(locator_file_path, engine="openpyxl", usecols=["LOCATION_NAME", "SITEID"])
            else:
                return Response({"error": f"Unsupported file format: {file}"}, status=400)
            clean_columns(df)
            locator_df_list.append(df)
        locater_df = pd.concat(locator_df_list, ignore_index=True).drop_duplicates()

        # ----------------- OLM ID File -----------------
        olm_id_file = request.FILES.get("olm")
        if not olm_id_file:
            return Response({"error": "olm_id not provided"}, status=400)

        if olm_id_file.name.endswith(".csv"):
            olm_df = pd.read_csv(olm_id_file)
        elif olm_id_file.name.endswith((".xls", ".xlsx")):
            olm_df = pd.read_excel(olm_id_file, engine="openpyxl")
        else:
            return Response({"error": "Invalid file format for olm_id_file"}, status=400)
        clean_columns(olm_df)

        # ----------------- HW Files -----------------
        hw_files = request.FILES.getlist("hw")
        if not hw_files:
            return Response({"error": "hw_file(s) not provided"}, status=400)

        hw_df_list = []
        for hw_file in hw_files:
            if hw_file.name.endswith(".csv"):
                df = pd.read_csv(hw_file, usecols=["ITEMCODE", "Module Name", "Module type", "Tech"])
            elif hw_file.name.endswith((".xls", ".xlsx")):
                df = pd.read_excel(hw_file, engine="openpyxl", usecols=["ITEMCODE", "Module Name", "Module type", "Tech"])
            else:
                return Response({"error": "Unsupported file format for hw_file"}, status=400)
            clean_columns(df)
            hw_df_list.append(df)
        hw_df = pd.concat(hw_df_list, ignore_index=True).drop_duplicates()

        # ----------------- Process RFS in Chunks -----------------
        export_dir = os.path.join(main_folder, "RFS_Mapping_Data")
        os.makedirs(export_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(export_dir, f"RFS_Mapping_Output{timestamp}.csv")

        total_rows = 0
        if isinstance(rfs_df, pd.io.parsers.TextFileReader):  # chunked CSV
            for i, rfs_chunk in enumerate(rfs_df):
                clean_columns(rfs_chunk)
                rfs_chunk["FROMLOCATION"] = rfs_chunk["FROMLOCATION"].astype(str).str.strip()
                rfs_chunk["ITEMCODE"] = rfs_chunk["ITEMCODE"].astype(str).str.strip()

                merged_rfs = (
                    rfs_chunk
                    .merge(olm_df[["OLM ID", "Partner"]], left_on="RFS_CREATED_BY", right_on="OLM ID", how="left")
                    .drop(columns=["OLM ID"])
                    .merge(locater_df, left_on="FROMLOCATION", right_on="LOCATION_NAME", how="left")
                    .drop(columns=["LOCATION_NAME"])
                    .merge(hw_df, on="ITEMCODE", how="left")
                )

                merged_rfs["Partner"] = merged_rfs["Partner"].replace("", None).fillna("Other TSP")

                # Column reordering
                cols = merged_rfs.columns.tolist()
                cols = move_after(cols, "SITEID", "FROMLOCATION")
                for col in ["Module Name", "Module type", "Tech"]:
                    cols = move_after(cols, col, "ITEM_DESCRIPTION")
                cols = move_after(cols, "Partner", "RFS_CREATED_BY")
                merged_rfs = merged_rfs[cols]

                total_rows += len(merged_rfs)
                merged_rfs.to_csv(output_path, mode="a", header=(i == 0), index=False, encoding="utf-8-sig")
        else:
            # Excel file (no chunks)
            clean_columns(rfs_df)
            merged_rfs = (
                rfs_df
                .merge(olm_df[["OLM ID", "Partner"]], left_on="RFS_CREATED_BY", right_on="OLM ID", how="left")
                .drop(columns=["OLM ID"])
                .merge(locater_df, left_on="FROMLOCATION", right_on="LOCATION_NAME", how="left")
                .drop(columns=["LOCATION_NAME"])
                .merge(hw_df, on="ITEMCODE", how="left")
            )
            merged_rfs["Partner"] = merged_rfs["Partner"].replace("", None).fillna("Other TSP")
            merged_rfs.to_csv(output_path, index=False, encoding="utf-8-sig")
            total_rows = len(merged_rfs)

        # ----------------- API Response -----------------
        relative_path = os.path.relpath(output_path, MEDIA_ROOT)
        download_url = request.build_absolute_uri(os.path.join(MEDIA_URL, relative_path).replace("\\", "/"))

        print("End Process_________")
        return Response({
            "status": True,
            "rows_processed": total_rows,
            "message": "File saved successfully",
            "download_url": download_url
        })

    except Exception as e:
        return Response({"error": f"find an error: {str(e)}"}, status=500)
    


# API for MS-MF Mapping Tool ----------------------------------------
@api_view(["POST"])
def ms_mf_site_mapping(request):
    print("Start Process for msmfmapping tool_________")
    try:
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

        # ----------------- MS-MF File -----------------
        msmf_folder = os.path.join(main_folder, "msmf_data")
        if not os.path.exists(msmf_folder):
            return Response({"error": "msmf_data folder not found"}, status=400)

        msmf_df = None
        for file in os.listdir(msmf_folder):
            msmf_file_path = os.path.join(msmf_folder, file)
            if not os.path.isfile(msmf_file_path):
                continue
            if msmf_file_path.endswith(".csv"):
                msmf_df = pd.read_csv(msmf_file_path, chunksize=50000)  # chunked
            elif msmf_file_path.endswith((".xls", ".xlsx")):
                msmf_df = pd.read_excel(msmf_file_path, engine="openpyxl")
            else:
                return Response({"error": f"Unsupported file format: {file}"}, status=400)
        if msmf_df is None:
            return Response({"error": "No MS-MF file found"}, status=400)

        # ----------------- Locator Files -----------------
        locator_folder = os.path.join(main_folder, "locator_data")
        if not os.path.exists(locator_folder):
            return Response({"error": "locator_data folder not found"}, status=400)

        locator_df_list = []
        for file in os.listdir(locator_folder):
            locator_file_path = os.path.join(locator_folder, file)
            if not os.path.isfile(locator_file_path):
                continue
            if locator_file_path.endswith(".csv"):
                df = pd.read_csv(locator_file_path, usecols=["LOCATION_NAME", "SITEID"])
            elif locator_file_path.endswith((".xls", ".xlsx")):
                df = pd.read_excel(locator_file_path, engine="openpyxl", usecols=["LOCATION_NAME", "SITEID"])
            else:
                return Response({"error": f"Unsupported file format: {file}"}, status=400)
            clean_columns(df)
            locator_df_list.append(df)
        locator_df = pd.concat(locator_df_list, ignore_index=True).drop_duplicates()

        # ----------------- OLM ID File -----------------
        olm_id_file = request.FILES.get("olm")
        if not olm_id_file:
            return Response({"error": "olm_id not provided"}, status=400)

        if olm_id_file.name.endswith(".csv"):
            olm_df = pd.read_csv(olm_id_file)
        elif olm_id_file.name.endswith((".xls", ".xlsx")):
            olm_df = pd.read_excel(olm_id_file, engine="openpyxl")
        else:
            return Response({"error": "Invalid file format for olm_id_file"}, status=400)
        clean_columns(olm_df)

        # ----------------- HW Files -----------------
        hw_files = request.FILES.getlist("hw")
        if not hw_files:
            return Response({"error": "hw_file(s) not provided"}, status=400)

        hw_df_list = []
        for hw_file in hw_files:
            if hw_file.name.endswith(".csv"):
                df = pd.read_csv(hw_file, usecols=["ITEMCODE", "Module Name", "Module type", "Tech"])
            elif hw_file.name.endswith((".xls", ".xlsx")):
                df = pd.read_excel(hw_file, engine="openpyxl", usecols=["ITEMCODE", "Module Name", "Module type", "Tech"])
            else:
                return Response({"error": "Unsupported file format for hw_file"}, status=400)
            clean_columns(df)
            hw_df_list.append(df)
        hw_df = pd.concat(hw_df_list, ignore_index=True).drop_duplicates()

        # ----------------- Process MSMF in Chunks -----------------
        export_dir = os.path.join(main_folder, "MSMF_Mapping_Data")
        os.makedirs(export_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(export_dir, f"MSMF_Mapping_Output{timestamp}.csv")

        total_rows = 0
        if isinstance(msmf_df, pd.io.parsers.TextFileReader):  # chunked CSV
            for i, msmf_chunk in enumerate(msmf_df):
                clean_columns(msmf_chunk)
                msmf_chunk["MS_FROMLOCATION"] = msmf_chunk["MS_FROMLOCATION"].astype(str).str.strip()
                msmf_chunk["PARTCODE"] = msmf_chunk["PARTCODE"].astype(str).str.strip()

                merged_msmf = (
                    msmf_chunk
                    .merge(olm_df[["OLM ID", "Partner"]], left_on="MS_CREATED_BY", right_on="OLM ID", how="left")
                    .drop(columns=["OLM ID"])
                    .merge(locator_df, left_on="MS_FROMLOCATION", right_on="LOCATION_NAME", how="left")
                    .drop(columns=["LOCATION_NAME"])
                    .merge(hw_df, left_on="PARTCODE", right_on="ITEMCODE", how="left")
                )

                merged_msmf["Partner"] = merged_msmf["Partner"].replace("", None).fillna("Other TSP")

                # Column reordering
                cols = merged_msmf.columns.tolist()
                cols = move_after(cols, "SITEID", "MS_FROMLOCATION")
                for col in ["Module Name", "Module type", "Tech"]:
                    cols = move_after(cols, col, "PART_DESCRIPTION")
                cols = move_after(cols, "Partner", "MS_CREATED_BY")
                merged_msmf = merged_msmf[cols]

                total_rows += len(merged_msmf)
                merged_msmf.to_csv(output_path, mode="a", header=(i == 0), index=False, encoding="utf-8-sig")
        else:
            # Excel file (no chunks)
            clean_columns(msmf_df)
            merged_msmf = (
                msmf_df
                .merge(olm_df[["OLM ID", "Partner"]], left_on="MS_CREATED_BY", right_on="OLM ID", how="left")
                .drop(columns=["OLM ID"])
                .merge(locator_df, left_on="MS_FROMLOCATION", right_on="LOCATION_NAME", how="left")
                .drop(columns=["LOCATION_NAME"])
                .merge(hw_df, left_on="PARTCODE", right_on="ITEMCODE", how="left")
            )
            merged_msmf["Partner"] = merged_msmf["Partner"].replace("", None).fillna("Other TSP")
            merged_msmf.to_csv(output_path, index=False, encoding="utf-8-sig")
            total_rows = len(merged_msmf)

        # ----------------- API Response -----------------
        relative_path = os.path.relpath(output_path, MEDIA_ROOT)
        download_url = request.build_absolute_uri(os.path.join(MEDIA_URL, relative_path).replace("\\", "/"))

        print("End Process_________")
        return Response({
            "status": True,
            "rows_processed": total_rows,
            "message": "File saved successfully",
            "download_url": download_url
        })

    except Exception as e:
        return Response({"error": f"find an error: {str(e)}"}, status=500)

    print("Start Process for msmfmapping  tool_________")
    try:
         #MS-MF file-----------------------------------------------
        msmf_folder = os.path.join(main_folder, 'msmf_data')
        if not os.path.exists(msmf_folder):
            return Response({"error": "msmf_data folder not found"}, status=400)
       
        for file in os.listdir(msmf_folder):
            msmf_file_path = os.path.join(msmf_folder, file)
            if not os.path.isfile(msmf_file_path):
                continue
            try:
                if msmf_file_path.endswith('.csv'):
                    msmf_df = pd.read_csv(msmf_file_path)
                elif msmf_file_path.endswith(('.xls', '.xlsx')):
                    msmf_df = pd.read_excel(msmf_file_path, engine='openpyxl')
                else:
                    return Response({"error": f"Unsupported file format: {file}"}, status=400)  
                msmf_df.columns = msmf_df.columns.str.strip()
                print("MS-MF Data -------------:", msmf_df.head())
            except Exception as e:
             return Response({"error": f"error reading olm_id_file: {str(e)}"}, status=500)
 
        # Locator Files -------------------------------------------------
        locator_folder = os.path.join(main_folder, 'locator_data')
        if not os.path.exists(locator_folder):
            return Response({"error": "locator_data folder not found"}, status=400)
       
        locator_df_list = []
        for file in os.listdir(locator_folder):
            locator_file_path = os.path.join(locator_folder, file)
            if not os.path.isfile(locator_file_path):
                continue
            try:
                if locator_file_path.endswith('.csv'):
                    df = pd.read_csv(locator_file_path, usecols=['LOCATION_NAME', 'SITEID'])    
                elif locator_file_path.endswith(('.xls', '.xlsx')):
                    df = pd.read_excel(locator_file_path, engine='openpyxl', usecols=['LOCATION_NAME', 'SITEID'])
                else:
                    return Response({"error": f"Unsupported file format: {file}"}, status=400)
                df.columns = df.columns.str.strip()
                locator_df_list.append(df)
            except Exception as e:
                return Response({"error": f"error reading locator file: {str(e)}"}, status=500)
        locator_df = pd.concat(locator_df_list, ignore_index=True).drop_duplicates()
        print("locator_df:",locator_df.head())
       
           
        #OLM ID File------------------------------------------------------------``
        olm_id_file = request.FILES.get("olm_id")
        if not olm_id_file:
            return Response({"error": "olm_id not provided"}, status=400)
        try:
            if olm_id_file.name.endswith('.csv'):
                olm_id_df = pd.read_csv(olm_id_file)
            elif olm_id_file.name.endswith(('.xls', '.xlsx')):
                olm_id_df = pd.read_excel(olm_id_file, engine='openpyxl')
            else:
                return Response({"error": "Invalid file format for olm_id_file"}, status=400)
            olm_id_df.columns = olm_id_df.columns.str.strip()
            print(olm_id_df.columns)
        except Exception as e:
            return Response({"error": f"error reading olm_id_file: {str(e)}"}, status=500)
 
        #  Multiple HW Files--------------------------------------------------
        hw_files = request.FILES.getlist("hw_file")
        if not hw_files:
            return Response({"error": "hw_file(s) not provided"}, status=400)
 
        hw_df_list = []
        for hw_file in hw_files:
            try:
                if hw_file.name.endswith('.csv'):
                    df = pd.read_csv(hw_file, usecols=["ITEMCODE", "Module Name", "Module type", "Tech"])
                elif hw_file.name.endswith(('.xls', '.xlsx')):
                 df = pd.read_excel(hw_file, engine='openpyxl', usecols=["ITEMCODE", "Module Name", "Module type", "Tech"])
                else:
                    return Response({"error": "Unsupported file format for hw_file"}, status=400)
                df.columns = df.columns.str.strip()
                hw_df_list.append(df)
            except Exception as e:
                return Response({"error": f"error reading a hw_file: {str(e)}"}, status=500)
        hw_df = pd.concat(hw_df_list, ignore_index=True).drop_duplicates()
        print(hw_df.columns)
       
       
        merged_data = (
                msmf_df
                .merge(olm_id_df[["OLM ID", "Partner"]], left_on="MS_CREATED_BY", right_on="OLM ID", how="left")
                .drop(columns=["OLM ID"])
                .merge(locator_df, left_on="MS_FROMLOCATION", right_on="LOCATION_NAME", how="left")
                .drop(columns=["LOCATION_NAME"])
                .merge(hw_df, left_on="PARTCODE", right_on="ITEMCODE", how="left")
            )
 
        if "Partner" in merged_data.columns:
            merged_data["Partner"] = merged_data["Partner"].replace("", None).fillna("Other TSP")
               
        # ----------------- Save Output -----------------
            export_dir = os.path.join(main_folder, "MSMF_Mapping_Data")
            os.makedirs(export_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(export_dir, f"MSMF_Mapping_Output{timestamp}.xlsx")
 
            with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
                merged_data.to_excel(writer, sheet_name="Msmf_Mapping", index=False)
                final_excel(merged_data, sheet_name="Msmf_Mapping", fast_mode=True)
 
   
            relative_path = os.path.relpath(output_path, MEDIA_ROOT)
            download_url = request.build_absolute_uri(
                os.path.join(MEDIA_URL, relative_path).replace("\\", "/")
            ).replace("\\", "/")
 
            print("End Process_________")
 
            return Response({
                "status": True,
                "message": "File saved successfully",
                "download_url": download_url
            })      
    except Exception as e:
     return Response({"error": f"find an error: {str(e)}"}, status=500)            