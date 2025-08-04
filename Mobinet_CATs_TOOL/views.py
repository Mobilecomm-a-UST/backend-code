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




# Excel  formate  function.........  
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
def final_excel(df, writer, sheet_name='Sheet1', fast_mode=False):
    df.to_excel(writer, index=False, sheet_name=sheet_name)
    ws = writer.sheets[sheet_name]

    if fast_mode:
        # Only style the header for large files
        header_fill = PatternFill(start_color='FFFF00', fill_type='solid')
        bold = Font(bold=True)
        align = Alignment(horizontal='center', vertical='center')
        border = Border(*[Side(style='thin')] * 4)

        for col_idx, col in enumerate(df.columns, start=1):
            cell = ws.cell(row=1, column=col_idx)
            cell.fill = header_fill
            cell.font = bold
            cell.alignment = align
            cell.border = border
        return  # Skip data cell styling
    else:
        # Full formatting (original logic)
        header_fill = PatternFill(start_color='FFFF00', fill_type='solid')
        bold = Font(bold=True)
        align = Alignment(horizontal='center', vertical='center')
        border = Border(*[Side(style='thin')] * 4)

        for col_idx, col in enumerate(df.columns, start=1):
            cell = ws.cell(row=1, column=col_idx)
            cell.fill = header_fill
            cell.font = bold
            cell.alignment = align
            cell.border = border
            ws.row_dimensions[1].height = 25

        for col_idx, col in enumerate(df.columns, 1):
            max_len = len(col)
            for row in range(2, ws.max_row + 1):
                cell = ws.cell(row=row, column=col_idx)
                cell.alignment = align
                cell.border = border
                if cell.value:
                    max_len = max(max_len, len(str(cell.value)))
            ws.column_dimensions[get_column_letter(col_idx)].width = max_len + 2

        
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

# # Mapping for renaming to original DB column names
# field_mapping = {
#         field.name: field.db_column if field.db_column else field.name
#         for field in MobinetDump._meta.fields
#     }




# @api_view(['POST'])
# @parser_classes([MultiPartParser])
# def upload_mobinet_dumps(request):
#     try:
#         # Delete old data--------------
        
#         MobinetDump.objects.all().delete()
#         print("Old MobinetDump data deleted successfully.")
       
#         # Read and process uploaded files
#         files = request.FILES.getlist('mobinet_dumps')
#         if not files:
#             return Response({'error': 'No files uploaded'}, status=status.HTTP_400_BAD_REQUEST)
 
#         for file in files:
#             df =read_file(file)# Read the file csv or excel
#             df.fillna('', inplace=True)
#             for _, row in df.iterrows():
#                 try:
#                     # Convert date strings to datetime objects---
#                     insert_date = pd.to_datetime(row.get('Insert Date', None), errors='coerce')
#                     update_date = pd.to_datetime(row.get('Update Date', None), errors='coerce')
                   
#                     # Create a MobinetDump instance and save it to the database
#                     MobinetDump.objects.create(
#                         node_type=row.get('Node type'),
#                         object_id=row.get('Object ID'),
#                         object_name=row.get('Object Name'),
#                         model=row.get('Model'),
#                         parent_site=row.get('Parent Site'),
#                         zone=row.get('Zone'),
#                         cabinet=row.get('Cabinet'),
#                         cabinet_type=row.get('Cabinet Type'),
#                         cabinet_part_number=row.get('Cabinet Part Number'),
#                         cabinet_sn=row.get('Cabinet SN'),
#                         shelf=row.get('Shelf'),
#                         shelf_type=row.get('Shelf Type'),
#                         ru_index=row.get('RU Index'),
#                         shelf_manufacturer=row.get('Shelf Manufacturer'),
#                         shelf_part_number=row.get('Shelf Part Number'),
#                         shelf_sn=row.get('Shelf SN'),
#                         slot=row.get('Slot'),
#                         index_on_slot=row.get('Index On Slot'),
#                         board_type=row.get('Board Type'),
#                         category=row.get('Category'),
#                         board_model=row.get('Board Model'),
#                         board_manufacturer=row.get('Board Manufacturer'),
#                         board_manufacturing_date=row.get('Board Manufacturing Date'),
#                         board_part_number=row.get('Board Part Number'),
#                         board_serial_number=row.get('Board Serial Number'),
#                         type_category=row.get('Type Category'),
#                         technology=row.get('Technology'),
#                         serial_number=row.get('Serial Number'),
#                         insert_date=insert_date,
#                         update_date=update_date,
#                         hardware_version=row.get('Hardware Version')
#                     )
#                 except Exception as e:
#                     print(f"Error processing row: {e}")
#                     continue
#             print("New MobinetDump data uploaded successfully.")
 
#         return Response({"message": "Mobinet Dump uploaded successfully"}, status=200)
 
#     except Exception as e:
#         return Response({'error': str(e)}, status=500)



        
        
# Frist Api for mobinet_dump site_match and hw_files-------------
@api_view(['POST'])
def mobinet_dump(request):
    try:
        # Read log files (CSV or Excel)
        log_files = request.FILES.getlist('log_files')
        if not log_files:
            return Response({"error": "log files not provided"}, status=400)
 
        log_df_list = []
        for file in log_files:
            try:
                df = read_file(file)
                log_df_list.append(df)
            except ValueError as e:
                return Response({"error": str(e)}, status=500)
        log_df = pd.concat(log_df_list, ignore_index=True)
 
        # Read site list file (CSV or Excel)
        site_list_file = request.FILES.get("site_list")
        if not site_list_file:
            return Response({"error": "site_list file not provided"}, status=400)
 
        try:
            site_df = read_file(site_list_file)
            # Optional: If sheet name needed specifically for Excel:
            if site_list_file.name.endswith(('.xls', '.xlsx')):
                site_df = pd.read_excel(site_list_file, engine='openpyxl')
                site_df.columns = site_df.columns.str.strip()
               
        except ValueError as e:
            return Response({"error": str(e)}, status=500)
       
        # Get multiple hw_files---
        hw_files = request.FILES.getlist("hw_file")
        if not hw_files:
            return Response({"error": "hw_files not provided"}, status=400)
 
        hw_df_list = []
        for hw_file in hw_files:
            try:
                df = read_file(hw_file)
                df.columns = df.columns.str.strip()
                hw_df_list.append(df)
            except Exception as e:
                return Response({"error": f"error reading one of the hw_files: {str(e)}"}, status=500)
        hw_df = pd.concat(hw_df_list, ignore_index=True)
 

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
        print(matched_df)
        # Unmatched sites.......
        unmatched_df = site_df.loc[
            ~site_df['Unique ID'].isin(log_df['Parent Site']), ['Unique ID']
        ].copy()
 
        unmatched_df.rename(columns={'Unique ID': 'Unmatched Unique ID'}, inplace=True)
       
        print("Unmatched Unique IDs:____________________")
        print(unmatched_df)
 
        # Merge with HW file
        matchedhw_df = pd.merge(
            matched_df,
            hw_df[['Module Name', 'ITEMCODE']],
            how='outer',
            left_on='Board Model',
            right_on='Module Name'
        )
        print(matchedhw_df)
        matchedhw_df.drop(columns='Module Name', inplace=True)
       
        #remove blank and - data in serial number
        matchedhw_df = matchedhw_df[matchedhw_df['Serial Number'].notna() & (matchedhw_df['Serial Number'].astype(str).str.strip() != '') &
                                        (matchedhw_df['Serial Number'].astype(str).str.strip() != '-')]
     
        matchedhw_df['Site+Module'] = matchedhw_df['Parent Site'].astype(str).str.strip() + "_" + matchedhw_df['Board Model'].astype(str).str.strip()
       
        matchedhw_df['Site+Serial'] = matchedhw_df['Parent Site'].astype(str).str.strip() + "_" + matchedhw_df['Serial Number'].astype(str).str.strip()
       
        matchedhw_df.drop_duplicates(subset='Serial Number', inplace=True)
       
        data_count=matchedhw_df.copy()
       
        summary_df = (
            data_count.groupby("Site+Module", as_index=False)
            .agg({
                "Serial Number": "count"
            })
            .rename(columns={
                "Serial Number": "Serial Number_count"
            })
        )
 
        print(summary_df)
       
 
        # sn_count = matchedhw_df.groupby('Site+Module')['Serial Number'].nunique()
        # matchedhw_df['Serial Number Count'] = matchedhw_df['Site+Module'].map(sn_count)
        # matchedhw_df.drop_duplicates(subset='Site+Module', inplace=True)
       
 
        output_dir = os.path.join(main_folder, 'Mobinet_Summary_output')
        os.makedirs(output_dir, exist_ok=True)
        delete_existing_files(output_dir)
        filename = f"mobinet_summary_data_{timestamp}.xlsx"
        output_path = os.path.join(output_dir, filename)
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
         final_excel(summary_df, writer, sheet_name='Mobinet_Summary')  
         final_excel(data_count, writer, sheet_name='Mobinet_Backup_Data')
         final_excel(unmatched_df, writer, sheet_name='Unmatched_Site_IDs')
 
           
        # Generate download URL----------
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
@api_view(['POST'])
def rfs_dump(request):
    print("Start Process_________")
    try:
        # RFS File
        rfs_file = request.FILES.get("rfs_file")
        if not rfs_file:
            return Response({"error": "rfs_file not provided"}, status=400)
        try:
            rfs_df = pd.read_excel(rfs_file, engine='openpyxl')
            rfs_df.columns = rfs_df.columns.str.strip()
            print(rfs_df.columns)
        except Exception as e:
            return Response({"error": f"error reading rfs_file: {str(e)}"}, status=500)

        #OLM ID File------------------------------------------------------------
        olm_id_file = request.FILES.get("olm_id_file")
        if not olm_id_file:
            return Response({"error": "olm_id_file not provided"}, status=400)
        try:
            olm_id_df = pd.read_excel(olm_id_file, engine='openpyxl', usecols=['MO', 'Partner'])
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
                df = pd.read_excel(hw_file, engine='openpyxl', usecols=['ITEMCODE', 'Module Name'])
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
            site_list_df = pd.read_excel(site_list_file, engine='openpyxl', usecols=['Unique ID', 'Dismantled date'])
            site_list_df.columns = site_list_df.columns.str.strip()
            print(site_list_df.columns)
        except Exception as e:
            return Response({"error": f"error reading site_list_file: {str(e)}"}, status=500)

        # Multiple Locator Files -------------------------------------------------
        locator_files = request.FILES.getlist("locator_file")
        if not locator_files:
            return Response({"error": "locator_file(s) not provided"}, status=400)

        locator_df_list = []
        for locator_file in locator_files:
            try:
                df = pd.read_excel(locator_file, engine='openpyxl')
                df.columns = df.columns.str.strip()
                locator_df_list.append(df)
            except Exception as e:
                return Response({"error": f"error reading a locator_file: {str(e)}"}, status=500)
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
        ms_mf_file = request.FILES.get("msmf_file")
        if not ms_mf_file:
            return Response({"error": "msmf_file not provided"}, status=400)
        try:
            ms_mf_df = pd.read_excel(ms_mf_file, engine='openpyxl')
            ms_mf_df.columns = ms_mf_df.columns.str.strip()
            print(ms_mf_df.columns)
        except Exception as e:
            return Response({"error": f"error reading msmf_file: {str(e)}"}, status=500)
        
        # stock-report_file -----------------------------------------------
        stock_report_file = request.FILES.get("stock_report_file")
        if not stock_report_file:
            return Response({"error": "stock_report_file not provided"}, status=400)
        try:
            stock_report_df =read_file(stock_report_file)
            stock_report_df.columns = stock_report_df.columns.str.strip()
            print(stock_report_df.columns)
        except Exception as e:
            return Response({"error": f"error reading stock_report_file: {str(e)}"}, status=500)


    
        
########for RFS file#######################################
        # Circle Mapping ....
        circle_map_code = {
            151: 'AP', 132: 'BR',152: 'CN',111: 'DL',113: 'HR', 114: 'JK',
            153: 'KK', 174: 'MU', 172: 'MP',  134: 'OR', 115: 'PB', 176: 'RJ', 
            116: 'UE', 117: 'UW', 135: 'WB', 136: 'KO', 155: 'TN',133: 'NE',131: 'AS'
        }


        #  Add Patner information---
        rfs_df["Patner"] = "Other TSP"
        rfs_df.loc[rfs_df["RFS_CREATED_BY"].isin(olm_id_df["MO"]), "Patner"] = "Mobliecomm"

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
        ms_mf_df["Patner"] = "Other TSP"
        ms_mf_df.loc[ms_mf_df["MS_CREATED_BY"].isin(olm_id_df["MO"]), "Patner"] = "Mobliecomm"
 
        # Merge with locator----
        merged_df_ms_mf = pd.merge(
            ms_mf_df,
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
        site_count_rfs = rfs_with_stock_report['Unique Site ID'].value_counts()
        site_count_msmf = ms_mf_data_cout['Unique Site ID'].value_counts()

        new_df = site_list_df[['Unique ID']].copy()
        new_df.rename(columns={'Unique ID': 'Site ID'}, inplace=True)
        new_df['SiteID in Mobinet'] = site_list_df['Unique ID'].map(site_count_mobinet).fillna(0).astype(int)
        new_df['SiteID in RFS'] = site_list_df['Unique ID'].map(site_count_rfs).fillna(0).astype(int)
        new_df['SiteID in MS-MF'] = site_list_df['Unique ID'].map(site_count_msmf).fillna(0).astype(int)

        print("new_df", new_df)
        print("End all files Process. Saving the data in excel file")

        
        output_dir = os.path.join(main_folder,'CATs_MS-MF_Summary_Output')
        os.makedirs(output_dir, exist_ok=True)
        delete_existing_files(output_dir)
        filename = f"CATs_Summary_data{timestamp}.xlsx"
        output_path = os.path.join(output_dir, filename)
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            final_excel(site_wise_summary, writer, sheet_name='Site Wise Summary')
            final_excel(circle_wise_summary, writer,  sheet_name='Circle Wise Summary')
            final_excel(final_summary_df,writer, sheet_name='CATs_MS-MF_Summary' )
            final_excel(summary_df,writer, sheet_name='CATs_Summary' )
            final_excel(ms_mf_summary_df,writer, sheet_name='MS-MF_Summary' )
            final_excel(rfs_with_stock_report,writer, sheet_name='CATs_Backup Data' )
            final_excel(rfs_matched_sn_merege ,writer, sheet_name='CATs_Matched_by_SN' )
            # final_excel(unmatched_data,writer, sheet_name='CATs_Unmatched_Sites' )
            final_excel(ms_mf_data_cout, writer, sheet_name='MS-MF_Backup Data' )
            final_excel(ms_mf_matched_merged, writer, sheet_name='MS-MF_Matched_by_SN')
            final_excel(new_df, writer, sheet_name='SiteID Count Summary')
            # final_excel(unmatched_data_ms_mf,writer, sheet_name='MS-MF_Unmatched_Sites' )
           
           
          
      
         
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
    
    
    
    
    
    
    
    
    
    
#Finall Api for CATs(rfs) and Mobinetoutput files-------------    

# @api_view(['POST'])
# def mobinet_rfslocator_dump(request):
#     try:
#         mobinet_output_file= request.FILES.get("mobinet_output_file")
#         if not mobinet_output_file:
#             return Response({"error": "mobinet_output_file not provided"}, status=400)
#         try:
#             mobinet_output_file_df = pd.read_excel(mobinet_output_file, engine='openpyxl')
#             mobinet_output_file_df.columns = mobinet_output_file_df.columns.str.strip()
#             mobinet_sheet_data=pd.read_excel(mobinet_output_file, engine='openpyxl', sheet_name='Mobinet_Backup_Data')
#             mobinet_sheet_data.columns = mobinet_sheet_data.columns.str.strip()
#         except Exception as e:
#             return Response({"error": f"error reading rfs_file: {str(e)}"}, status=500)
        
        
#         rfs_output_file= request.FILES.get("rfs_output_file")
#         if not rfs_output_file:
#             return Response({"error": "rfs_locator_output_file not provided"}, status=400)
#         try:
#             rfs_output_file_df = pd.read_excel(rfs_output_file, engine='openpyxl')
#             rfs_output_file_df.columns = rfs_output_file_df.columns.str.strip()
#             rfs_sheet_data=pd.read_excel(rfs_output_file, engine='openpyxl', sheet_name='CATs_Backup Data')
#             rfs_sheet_data.columns = rfs_sheet_data.columns.str.strip()
#             ms_mf_sheet_data=pd.read_excel(rfs_output_file, engine='openpyxl', sheet_name='MS-MF_Backup Data')
#             ms_mf_sheet_data.columns = ms_mf_sheet_data.columns.str.strip() 
            
#         except Exception as e:
#             return Response({"error": f"error reading locator_file: {str(e)}"}, status=500)
        
#         # Read site list file (CSV or Excel)
#         site_list_file = request.FILES.get("site_list_file")
#         if not site_list_file:
#             return Response({"error": "site_list_file not provided"}, status=400)
#         try:
#             site_df = pd.read_excel(site_list_file, engine='openpyxl')
#             site_df.columns = site_df.columns.str.strip()
#         except Exception as e:
#             return Response({"error": f"error reading site_list_file: {str(e)}"}, status=500)
        
# #find the count of matcted site in mobinate and rfs file ms-mf------------------------
#         site_count_mobinet = mobinet_sheet_data['Parent Site'].value_counts()
#         site_count_rfs = rfs_sheet_data['Unique Site ID'].value_counts()
#         site_count_msmf = ms_mf_sheet_data['Unique Site ID'].value_counts()

#         new_df = site_df[['Unique ID']].copy()
#         new_df.rename(columns={'Unique ID': 'Site ID'}, inplace=True)
#         new_df['SiteID in Mobinet'] = site_df['Unique ID'].map(site_count_mobinet).fillna(0).astype(int)
#         new_df['SiteID in RFS'] = site_df['Unique ID'].map(site_count_rfs).fillna(0).astype(int)
#         new_df['SiteID in MS-MF'] = site_df['Unique ID'].map(site_count_msmf).fillna(0).astype(int)







        
#         merged_df = pd.merge(
#             left=mobinet_output_file_df,
#             right=rfs_output_file_df[['Site+Module', 'RECEIVED_QTY_COUNT(RFS_FILE)' ,'RFS_QTY_COUNT(RFS_FILE)','RECEIVED_QTY_COUNT(MS-MF FILE)','RFS_QTY_COUNT(MS-MF FILE)','SRNCAMREQSTATUS']].copy(),  # include ITEMCODE here
#             how='outer',
#             on='Site+Module',
           
#         )

#         merged_df['Unique ID'] = merged_df['Site+Module'].str.split('_', expand=True)[0] + "_" +merged_df['Site+Module'].str.split('_', expand=True)[1]
#      #site wise summay----------------------------------------------
#         site_wise_summary = (
#         merged_df
#         .groupby('Unique ID', as_index=False)
#         .agg({
#             'Serial Number_count': 'sum',
#             'RECEIVED_QTY_COUNT(RFS_FILE)': 'sum',
#             'RECEIVED_QTY_COUNT(MS-MF FILE)': 'sum',
#             'RFS_QTY_COUNT(RFS_FILE)': 'sum',
#             'RFS_QTY_COUNT(MS-MF FILE)': 'sum',
#           'SRNCAMREQSTATUS': 'first'

#         })
#         .assign(
#             Total_In_CATS =lambda x:  x['RFS_QTY_COUNT(RFS_FILE)'] + x['RFS_QTY_COUNT(MS-MF FILE)'],
#             Total_Receipt_CATS=lambda x: x['RECEIVED_QTY_COUNT(RFS_FILE)'] + x['RECEIVED_QTY_COUNT(MS-MF FILE)'],
#             Dismantle_vs_SREQ=lambda x: x['Total_In_CATS'] - x['Serial Number_count'],
#             SREQ_vs_WH_Receipt=lambda x:x['Total_Receipt_CATS'] - x['Total_In_CATS'],
            
#             )
        
#         .rename(columns={
#             'Unique ID': 'Site ID',
#             'Serial Number_count': 'Mobinet_Count(Serial Number)',
#         })
#     )
#         print(site_wise_summary)
        
#         #Circle wise summary----------------------------------------------
#         merged_df['Circle'] = merged_df['Unique ID'].str.split('_', expand=True)[1]
        
#         circle_wise_summary = (
#                         merged_df
#                         .groupby('Circle', as_index=False)
#                         .agg({
#                             'Serial Number_count': 'sum',
#                             'RECEIVED_QTY_COUNT(RFS_FILE)': 'sum',
#                             'RECEIVED_QTY_COUNT(MS-MF FILE)': 'sum',
#                             'RFS_QTY_COUNT(RFS_FILE)': 'sum',
#                             'RFS_QTY_COUNT(MS-MF FILE)': 'sum',
#                             'SRNCAMREQSTATUS': 'first'

#                         })
                          
#                       .assign(
#                             Total_In_CATS =lambda x:  x['RFS_QTY_COUNT(RFS_FILE)'] + x['RFS_QTY_COUNT(MS-MF FILE)'],
#                             Total_Receipt_CATS=lambda x: x['RECEIVED_QTY_COUNT(RFS_FILE)'] + x['RECEIVED_QTY_COUNT(MS-MF FILE)'],
#                             Dismantle_vs_SREQ=lambda x: x['Total_In_CATS'] - x['Serial Number_count'],
#                             SREQ_vs_WH_Receipt=lambda x:x['Total_Receipt_CATS'] - x['Total_In_CATS'],
                            
#                             )
#                         .rename(columns={
#                             'Serial Number_count': 'Mobinet_Count(Serial Number)',
                          
#                         })
#                     )


#         output_dir = os.path.join(main_folder,'Final_Output')
#         os.makedirs(output_dir, exist_ok=True)
#         delete_existing_files(output_dir)
#         timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         filename = f"mobinet_CATs_final_data{timestamp}.xlsx"
#         output_path = os.path.join(output_dir,filename)
       
#         with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
#             final_excel(site_wise_summary, writer, sheet_name='Site Wise Summary')
#             final_excel(circle_wise_summary, writer,  sheet_name='Circle Wise Summary')
#             final_excel(new_df, writer, sheet_name='SiteID Count Summary')
        
           

#         relative_path = os.path.relpath(output_path, MEDIA_ROOT)
#         download_url = request.build_absolute_uri(os.path.join(MEDIA_URL, relative_path).replace("\\", "/"))
#         print("End Process_________")
#         return Response({
#             "status": True,
#             "message": "File saved successfully",
#             "download_url": download_url
#         })
    
#     except Exception as e:
#         return Response({"error": f"find an error: {str(e)}"}, status=500)















# #########################################
    
# #mobinet_dump for only site data match------find NMS_Dump data
# @api_view(['POST'])
# def mobinet_Site_match(request):
#     print("Start Process_________")
#     try:
#         log_files = request.FILES.getlist('log_files')
#         if not log_files:
#             return Response({"error": "log files not provided"}, status=400)

#         log_df_list = []
#         for file in log_files:
#             try:
#                 df = read_file(file)
#                 log_df_list.append(df)
#             except ValueError as e:
#                 return Response({"error": str(e)}, status=500)
#         log_df = pd.concat(log_df_list, ignore_index=True)
        

#         site_list_file = request.FILES.get("site_list")
#         if not site_list_file:
#             return Response({"error": "site_list file not provided"}, status=400)

#         try:
#             site_df = read_file(site_list_file)
#             if site_list_file.name.endswith(('.xls', '.xlsx')):
#                 site_df = pd.read_excel(site_list_file, engine='openpyxl')
#                 site_df.columns = site_df.columns.str.strip()
                
#         except ValueError as e:
#             return Response({"error": str(e)}, status=500)
        

#         # Validation of required columns
#         if 'Parent Site' not in log_df.columns:
#             return Response({"error": "'Parent Site' column not found in log_file"}, status=400)
    
#         # Strip and match values
#         log_df['Parent Site'] = log_df['Parent Site'].astype(str).str.strip()
#         site_df['Unique ID'] = site_df['Unique ID'].astype(str).str.strip()

#         # Merge logs with site list
#         matched_df = pd.merge(
#             log_df,
#             site_df[['Unique ID']],
#             how='inner',
#             left_on='Parent Site',
#             right_on='Unique ID'
#         )
#         matched_df.drop(columns='Unique ID', inplace=True)
#         print(matched_df)
#         # Unmatched sites.......
#         unmatched_df = site_df.loc[
#             ~site_df['Unique ID'].isin(log_df['Parent Site']), ['Unique ID']
#         ].copy()

#         unmatched_df.rename(columns={'Unique ID': 'Unmatched Unique ID'}, inplace=True)
#         print("Unmatched Unique IDs:____________________")
#         print(unmatched_df)

      
        
#         #remove blank and - data in serial number 
#         matched_df = matched_df[matched_df['Serial Number'].notna() & (matched_df['Serial Number'].astype(str).str.strip() != '') &
#                                         (matched_df['Serial Number'].astype(str).str.strip() != '-')]
        
#         matched_df.drop_duplicates(subset='Serial Number', inplace=True)
     

#         # sn_count = matchedhw_df.groupby('Site+Module')['Serial Number'].nunique()
#         # matchedhw_df['Serial Number Count'] = matchedhw_df['Site+Module'].map(sn_count)
#         # matchedhw_df.drop_duplicates(subset='Site+Module', inplace=True)
        

#         output_dir = os.path.join(main_folder, 'Mobinet_Summary_output')
#         os.makedirs(output_dir, exist_ok=True)
#         delete_existing_files(output_dir)
#         timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         filename = f"NMS_dump_data_{timestamp}.xlsx"
#         output_path = os.path.join(output_dir, filename)
#         with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
#          final_excel(matched_df, writer, sheet_name='Mobinet_Backup_Data')
#          final_excel(unmatched_df, writer, sheet_name='Unmatched_SiteIDs')

            
#         # Generate download URL----------
#         relative_path = os.path.relpath(output_path, MEDIA_ROOT)
#         download_url = request.build_absolute_uri(os.path.join(MEDIA_URL, relative_path).replace("\\", "/"))
#         print("End Process_________")

#         return Response({
#             "status": True,
#             "message": "File saved successfully",
#             "download_url": download_url
#         })
#     except Exception as e:
#         return Response({"error": f"find an error: {str(e)}"}, status=500)
    




# # Mapping for renaming to original DB column names
# field_mapping = {
#         field.name: field.db_column if field.db_column else field.name
#         for field in MobinetDump._meta.fields
#     }




# @api_view(['POST'])
# @parser_classes([MultiPartParser])
# def upload_mobinet_dumps(request):
#     try:
#         # Delete old data--------------
        
#         MobinetDump.objects.all().delete()
#         print("Old MobinetDump data deleted successfully.")
       
#         # Read and process uploaded files
#         files = request.FILES.getlist('mobinet_dumps')
#         if not files:
#             return Response({'error': 'No files uploaded'}, status=status.HTTP_400_BAD_REQUEST)
 
#         for file in files:
#             df =read_file(file)# Read the file csv or excel
#             df.fillna('', inplace=True)
#             for _, row in df.iterrows():
#                 try:
#                     # Convert date strings to datetime objects---
#                     insert_date = pd.to_datetime(row.get('Insert Date', None), errors='coerce')
#                     update_date = pd.to_datetime(row.get('Update Date', None), errors='coerce')
                   
#                     # Create a MobinetDump instance and save it to the database
#                     MobinetDump.objects.create(
#                         node_type=row.get('Node type'),
#                         object_id=row.get('Object ID'),
#                         object_name=row.get('Object Name'),
#                         model=row.get('Model'),
#                         parent_site=row.get('Parent Site'),
#                         zone=row.get('Zone'),
#                         cabinet=row.get('Cabinet'),
#                         cabinet_type=row.get('Cabinet Type'),
#                         cabinet_part_number=row.get('Cabinet Part Number'),
#                         cabinet_sn=row.get('Cabinet SN'),
#                         shelf=row.get('Shelf'),
#                         shelf_type=row.get('Shelf Type'),
#                         ru_index=row.get('RU Index'),
#                         shelf_manufacturer=row.get('Shelf Manufacturer'),
#                         shelf_part_number=row.get('Shelf Part Number'),
#                         shelf_sn=row.get('Shelf SN'),
#                         slot=row.get('Slot'),
#                         index_on_slot=row.get('Index On Slot'),
#                         board_type=row.get('Board Type'),
#                         category=row.get('Category'),
#                         board_model=row.get('Board Model'),
#                         board_manufacturer=row.get('Board Manufacturer'),
#                         board_manufacturing_date=row.get('Board Manufacturing Date'),
#                         board_part_number=row.get('Board Part Number'),
#                         board_serial_number=row.get('Board Serial Number'),
#                         type_category=row.get('Type Category'),
#                         technology=row.get('Technology'),
#                         serial_number=row.get('Serial Number'),
#                         insert_date=insert_date,
#                         update_date=update_date,
#                         hardware_version=row.get('Hardware Version')
#                     )
#                 except Exception as e:
#                     print(f"Error processing row: {e}")
#                     continue
#             print("New MobinetDump data uploaded successfully.")
 
#         return Response({"message": "Mobinet Dump uploaded successfully"}, status=200)
 
#     except Exception as e:
#         return Response({'error': str(e)}, status=500)



        
        
# # Frist Api for mobinet_dump site_match and hw_files-------------work wit database

# @api_view(['POST'])
# def mobinet_dump(request):
#     print("Start Process_________")
#     try:
#         # Read Mobinet dump file from database
#         mobinet_dump =request.FILES.get("log_files")
#         if not mobinet_dump:
#             return Response({"error": "No MobinetDump file found "}, status=400)
             
#         try:
#             mobinate_files_df = read_file(mobinet_dump)
#             mobinate_files_df.columns =  mobinate_files_df.columns.str.strip()
#             print("Mobinet files DataFrame columns:", mobinate_files_df.columns)
#         except Exception as e:
#             return Response({"error":  f"Error reading MobinetDump file: {str(e)}"}, status=500)
        
        
#         # #read mobinet_dump file from database
#         # mobinet_dumps = MobinetDump.objects.all()
#         # if not mobinet_dumps.exists():
#         #     return Response({"error": "No data found in the database"}, status=400)
        
#         # dump_list = list(mobinet_dumps.values())  # returns dict with field names (e.g., 'node_type')
#         # mobinate_files_df  = pd.DataFrame(dump_list)
        
#         # if mobinate_files_df.empty:
#         #     return Response({"error": "Data is empty"}, status=400)
#         # # Rename columns-----------
#         # mobinate_files_df.rename(columns=field_mapping, inplace=True)
#         # mobinate_files_df.columns = mobinate_files_df.columns.str.strip()
#         # print("Mobinet files DataFrame columns:", mobinate_files_df.columns)
        


    
   
    
#         # Read site list file (CSV or Excel)
#         site_list_file = request.FILES.get("site_list")
#         if not site_list_file:
#             return Response({"error": "site_list file not provided"}, status=400)
 
#         try:
#             site_df = read_file(site_list_file)
#             # Optional: If sheet name needed specifically for Excel:
#             if site_list_file.name.endswith(('.xls', '.xlsx')):
#                 site_df = pd.read_excel(site_list_file, engine='openpyxl')
#                 site_df.columns = site_df.columns.str.strip()
#             print("Site list file DataFrame columns:", site_df.columns)
            
#         except Exception as e:
#             return Response({"error": f"Error reading site_list file: {str(e)}"}, status=500)
       
#         # Get multiple hw_files---
#         hw_files = request.FILES.getlist("hw_file")
#         if not hw_files:
#             return Response({"error": "hw_files not provided"}, status=400)
 
#         hw_df_list = []
#         for hw_file in hw_files:
#             try:
#                 df = pd.read_excel(hw_file, engine='openpyxl')
#                 df.columns = df.columns.str.strip()
#                 hw_df_list.append(df)
                
#             except Exception as e:
#                 return Response({"error": f"error reading the hw_files: {str(e)}"}, status=500)
#         hw_df = pd.concat(hw_df_list, ignore_index=True)
 

 
#         # Strip and match values-----
#         mobinate_files_df['Parent Site'] = mobinate_files_df['Parent Site'].astype(str).str.strip()
#         site_df['Unique ID'] = site_df['Unique ID'].astype(str).str.strip()
 
#         # Merge logs with site list
#         matched_df = pd.merge(
#             mobinate_files_df,
#             site_df[['Unique ID', 'Dismantled date']],
#             how='inner',
#             left_on='Parent Site',
#             right_on='Unique ID'
#         )
#         matched_df.drop(columns='Unique ID', inplace=True)

#         print(matched_df)

    
 
#         # Merge with HW file
#         matchedhw_df = pd.merge(
#             matched_df,
#             hw_df[['Module Name', 'ITEMCODE']],
#             how='outer',
#             left_on='Board Model',
#             right_on='Module Name'
#         )
#         matchedhw_df.drop(columns='Module Name', inplace=True)
#         print(matchedhw_df)
       
#         #remove blank and - data in serial number
#         matchedhw_df = matchedhw_df[matchedhw_df['Serial Number'].notna() & (matchedhw_df['Serial Number'].astype(str).str.strip() != '') &
#                                         (matchedhw_df['Serial Number'].astype(str).str.strip() != '-')]
     
#         matchedhw_df['Site+Module'] = matchedhw_df['Parent Site'].astype(str).str.strip() + "_" + matchedhw_df['Board Model'].astype(str).str.strip()
        
#         matchedhw_df['Site+Serial'] = matchedhw_df['Parent Site'].astype(str).str.strip() + "_" + matchedhw_df['Serial Number'].astype(str).str.strip()
       
#         matchedhw_df.drop_duplicates(subset='Serial Number', inplace=True)
        
#        #make a summary-----
#         data_count=matchedhw_df.copy()
       
#         summary_df = (
#             data_count.groupby("Site+Module", as_index=False)
#             .agg({
#                 "Serial Number": "count"
#             })
#             .rename(columns={
#                 "Serial Number": "Serial Number_count"
#             })
#         )
 
#         print(summary_df)
       
#  # # Unmatched Unique IDs
#         unmatched_df = site_df.loc[
#             ~site_df['Unique ID'].isin(mobinate_files_df['Parent Site']), ['Unique ID']
#         ].copy()
#         unmatched_df.rename(columns={'Unique ID': 'Unmatched Site ID'}, inplace=True)
#         print("Unmatched Unique IDs:____________________")
#         print(unmatched_df)
 
 
#         # sn_count = matchedhw_df.groupby('Site+Module')['Serial Number'].nunique()
#         # matchedhw_df['Serial Number Count'] = matchedhw_df['Site+Module'].map(sn_count)
#         # matchedhw_df.drop_duplicates(subset='Site+Module', inplace=True)
       
 
#         output_dir = os.path.join(main_folder, 'Mobinet_Summary_output')
#         os.makedirs(output_dir, exist_ok=True)
#         delete_existing_files(output_dir)
#         filename = f"mobinet_summary_data_{timestamp}.xlsx"
#         output_path = os.path.join(output_dir, filename)
#         with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
#          final_excel(summary_df, writer, sheet_name='Mobinet_Summary')  
#          final_excel(data_count, writer, sheet_name='Mobinet_Backup_Data')
#          final_excel(unmatched_df, writer, sheet_name='Unmatched_Site_IDs')
       
      
        
#         # Generate download URL----------
#         relative_path = os.path.relpath(output_path, MEDIA_ROOT)
#         download_url = request.build_absolute_uri(os.path.join(MEDIA_URL, relative_path).replace("\\", "/"))
#         print("End Process_________")
 
#         return Response({
#             "status": True,
#             "message": "File saved successfully",
#             "download_url": download_url
#         })
#     except Exception as e:
#         return Response({"error": f"find an error: {str(e)}"}, status=500)
   
   