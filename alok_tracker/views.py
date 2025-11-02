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

CENTRAL_COLUMNS = [
    'Integration Date',    
    'EMF Submission Date',  
    'Alarm Status',    
    'Alarm Rectification Done Date',    
    'SCFT Done Date',  
    'SCFT Offered Date',    
    'RAN PAT Offer Date',
    'RAN SAT Offer Date' ,
    'MW Phy AT Offer Date',
    'MW Soft AT Offer Date',    
    'MW MS1 Date (MIDS)',  
    'Site ONAIR Date',  
    'I-Deploy ONAIR Date',  
    '5G ONAIR Date',    
    'RAN PAT Accepted Date',    
    'RAN SAT Accepted Date',    
    'MW Phy AT Accepted Date',
    'MW Soft AT Accepted Date',
    'SCFT Accepted Date',
    'KPI AT offer Date',
    'KPI AT Accepted Date',
    '4G MS2 Date',
    '5G MS2 date'
]

CIRCLE_COLUMNS = [
    'Circle',
    'Site Tagging',
    'Old TOCO Name',
    'Old Site Id',
    'New Site ID',
    'New TOCO Name',
    'SR Number',
    'RAN OEM',
    'Media Type',
    'MW OEM',
    'Relocation Method',
    'Relocation Type',
    'OLD Site Band',
    'New Site Band',
    'RFAI Date' ,
    'Allocation Date',
    'RFAI Survey Date',
    'RFAI Survey Done Date',
    'MO Punch Date',
    'Material Dispatch Date',
    'Material Delivered Date',
    'Installation Start Date',
    'Installation End Date',
    'RAN LKF Status',
    'MW Plan ID',
    'RSL Value Status',
    'ENM Status',
    'MW LKF'
]

ALL_CIRCLES = [
    'Integration Date',    
    'EMF Submission Date',  
    'Alarm Status',    
    'Alarm Rectification Done Date',    
    'SCFT Done Date',  
    'SCFT Offered Date',    
    'RAN PAT Offer Date',
    'RAN SAT Offer Date' ,
    'MW Phy AT Offer Date',
    'MW Soft AT Offer Date',    
    'MW MS1 Date (MIDS)',  
    'Site ONAIR Date',  
    'I-Deploy ONAIR Date',  
    '5G ONAIR Date',    
    'RAN PAT Accepted Date',    
    'RAN SAT Accepted Date',    
    'MW Phy AT Accepted Date',
    'MW Soft AT Accepted Date',
    'SCFT Accepted Date',
    'KPI AT offer Date',
    'KPI AT Accepted Date',
    '4G MS2 Date',
    '5G MS2 date',
    'Circle',
    'Site Tagging',
    'Old TOCO Name',
    'Old Site Id',
    'New Site ID',
    'New TOCO Name',
    'SR Number',
    'RAN OEM',
    'Media Type',
    'MW OEM',
    'Relocation Method',
    'Relocation Type',
    'OLD Site Band',
    'New Site Band',
    'RFAI Date' ,
    'Allocation Date',
    'RFAI Survey Date',
    'RFAI Survey Done Date',
    'MO Punch Date',
    'Material Dispatch Date',
    'Material Delivered Date',
    'Installation Start Date',
    'Installation End Date',
    'RAN LKF Status',
    'MW Plan ID',
    'RSL Value Status',
    'ENM Status',
    'MW LKF'
]

############################################################### Access Rights ##############################################################

ACCESS_RIGHTS = {
    "girraj.singh@mcpsinc.in":"CENTRAL",
    "vinay.duklan@mcpsinc.in":"AP",
    "mohit.batra@mcpsinc.com":"CENTRAL",
    "Devansh.Jain@ust.com":"HRY",
}

############################################################  UPLOAD DATA ######################################################################################

@api_view(["POST"])
def upload_tracker_data_view(request):
    userId = request.data.get('userId')
    circle = ACCESS_RIGHTS[userId]
    file = request.FILES.get("tracker_file")

    if not userId or not circle:
        return Response({'error': 'userId and circle are required.'}, status=400)

    if not file:
        return Response({"status": False, "message": "No file provided."}, status=400)

    try:
        # ✅ Read Excel/CSV file
        df = pd.read_csv(file, header=[3]) if file.name.endswith('.csv') else pd.read_excel(file, header=[3])
        df.columns = [col.strip() for col in df.columns]

        # ✅ Replace NaT/NaN/empty with None (Main Fix)
        df = df.where(pd.notnull(df), None)

        # Optional: if some dates still have tzinfo/NaT, clean them
        INVALID_DATE_STRINGS = {"need to check", "pending", "na", "tbd", "n/a", "nan", "-"}

        def safe_datetime(value):
            """Safely convert to datetime or return None."""
            import pandas as pd
            if pd.isna(value) or value is pd.NaT:
                return None
            if isinstance(value, (pd.Timestamp, dtime)):
                return value
            if isinstance(value, str):
                v = value.strip().lower()
                if v in INVALID_DATE_STRINGS or not v:
                    return None
                try:
                    val = pd.to_datetime(value, errors="coerce")
                    if pd.isna(val):
                        return None
                    return val.to_pydatetime()
                except Exception:
                    return None
            return None
 
        for col in df.columns:
            if "date" in col:
                df[col] = df[col].apply(safe_datetime)
 
        # ✅ Validate required columns
        required_columns = ALL_CIRCLES if circle == "CENTRAL" else CIRCLE_COLUMNS
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return Response(
                {"status": False, "error": f"Missing columns: {', '.join(missing_columns)}"},
                status=400,
            )
 
        # ✅ Keep only relevant columns
        df = df[[col for col in df.columns if col in required_columns]]
 
        # ✅ Prepare DB operations
        objects_to_create = []
        objects_to_update = []
 
        # Cache existing records to avoid duplicate queries
        existing_records = {
            (rec.circle, rec.new_site_id): rec
            for rec in AlokTrackerModel.objects.all().only("circle", "new_site_id")
        }
 
        # ✅ Convert dataframe to dict (faster than iterrows)
        records = df.to_dict(orient='records')
 
        with transaction.atomic():
            for row in records:
                circle_val = row.get("Circle")
                new_site_id_val = row.get("New Site ID")
 
                if not circle_val or not new_site_id_val:
                    continue  # skip invalid rows
 
                # Common fields for both create/update
                common_fields = {
                    "circle": circle_val,
                    "site_tagging": row.get("Site Tagging"),
                    "old_toco_name": row.get("Old TOCO Name"),
                    "old_site_id": row.get("Old Site Id"),
                    "new_site_id": new_site_id_val,
                    "new_toco_name": row.get("New TOCO Name"),
                    "sr_number": row.get("SR Number"),
                    "ran_oem": row.get("RAN OEM"),
                    "media_type": row.get("Media Type"),
                    "mw_oem": row.get("MW OEM"),
                    "relocation_method": row.get("Relocation Method"),
                    "relocation_type": row.get("Relocation Type"),
                    "old_site_band": row.get("OLD Site Band"),
                    "new_site_band": row.get("New Site Band"),
                    "rfai_date": safe_datetime(row.get("RFAI Date")),
                    "allocation_date": safe_datetime(row.get("Allocation Date")),
                    "rfai_survey_date": safe_datetime(row.get("RFAI Survey Date")),
                    "rfai_survey_done_date": safe_datetime(row.get("RFAI Survey Done Date")),
                    "mo_punch_date": safe_datetime(row.get("MO Punch Date")),
                    "material_dispatch_date": safe_datetime(row.get("Material Dispatch Date")),
                    "material_delivered_date": safe_datetime(row.get("Material Delivered Date")),
                    "installation_start_date": safe_datetime(row.get("Installation Start Date")),
                    "installation_end_date": safe_datetime(row.get("Installation End Date")),
                    "ran_lkf_status": row.get("RAN LKF Status"),
                    "mw_plan_id": row.get("MW Plan ID"),
                    "rsl_value_status": row.get("RSL Value Status"),
                    "enm_status": row.get("ENM Status"),
                    "mw_lkf": row.get("MW LKF"),
                    "last_updated_by": userId,
                }
 
                # CENTRAL has extra fields
                if circle == "CENTRAL":
                    extra_fields = {
                        "integration_date": safe_datetime(row.get("Integration Date")),
                        "emf_submission_date": safe_datetime(row.get("EMF Submission Date")),
                        "alarm_status": row.get("Alarm Status"),
                        "alarm_rectification_done_date": safe_datetime(row.get("Alarm Rectification Done Date")),
                        "scft_done_date": safe_datetime(row.get("SCFT Done Date")),
                        "scft_offered_date": safe_datetime(row.get("SCFT Offered Date")),
                        "ran_pat_offer_date": safe_datetime(row.get("RAN PAT Offer Date")),
                        "ran_sat_offer_date": safe_datetime(row.get("RAN SAT Offer Date")),
                        "mw_phy_at_offer_date": safe_datetime(row.get("MW Phy AT Offer Date")),
                        "mw_soft_at_offer_date": safe_datetime(row.get("MW Soft AT Offer Date")),
                        "mw_ms1_date_mids": safe_datetime(row.get("MW MS1 Date (MIDS)")),
                        "site_onair_date": safe_datetime(row.get("Site ONAIR Date")),
                        "i_deploy_onair_date": safe_datetime(row.get("I-Deploy ONAIR Date")),
                        "five_g_onair_date": safe_datetime(row.get("5G ONAIR Date")),
                        "ran_pat_accepted_date": safe_datetime(row.get("RAN PAT Accepted Date")),
                        "ran_sat_accepted_date": safe_datetime(row.get("RAN SAT Accepted Date")),
                        "mw_phy_at_accepted_date": safe_datetime(row.get("MW Phy AT Accepted Date")),
                        "mw_soft_at_accepted_date": safe_datetime(row.get("MW Soft AT Accepted Date")),
                        "scft_accepted_date": safe_datetime(row.get("SCFT Accepted Date")),
                        "kpi_at_offer_date": safe_datetime(row.get("KPI AT offer Date")),
                        "kpi_at_accepted_date": safe_datetime(row.get("KPI AT Accepted Date")),
                        "four_g_ms2_date": safe_datetime(row.get("4G MS2 Date")),
                        "five_g_ms2_date": safe_datetime(row.get("5G MS2 date")),
                    }
                    common_fields.update(extra_fields)
 
                # Create or update decision
                key = (circle_val, new_site_id_val)
                if key in existing_records:
                    obj = existing_records[key]
                    
                    if obj.site_onair_date:
                        continue
                    
                    for field, value in common_fields.items():
                        setattr(obj, field, value)
                    objects_to_update.append(obj)
                else:
                    objects_to_create.append(AlokTrackerModel(**common_fields))
 
            # ✅ Bulk create & update
            if objects_to_create:
                AlokTrackerModel.objects.bulk_create(objects_to_create, batch_size=500)
 
            if objects_to_update:
                # Manually update the timestamp for each object
                now = timezone.now()
                for obj in objects_to_update:
                    print(obj.circle, " ", obj.new_site_id)
                    obj.last_updated_date = now
 
                # Then bulk update including last_updated_date
                AlokTrackerModel.objects.bulk_update(
                    objects_to_update,
                    fields=list(common_fields.keys()) + ['last_updated_date'],
                    batch_size=500,
                )
 
        return Response({"status": True, "message": "Data inserted successfully."})
 
    except Exception as e:
        return Response({"status": False, "error": str(e)}, status=500)

############################################################ DOWNLOAD DATA ###################################################################

@api_view(['POST'])
def download_tracker_data_view(request):
    userId = request.data.get('userId')
    circle = ACCESS_RIGHTS[userId]
 
    if not userId or not circle:
        return Response({'error': 'userId and circle are required.'}, status=400)
    try:
        obj = []
        if circle == 'CENTRAL':
            obj = AlokTrackerModel.objects.all() # noqa: F405
        else:
            obj = AlokTrackerModel.objects.filter(circle=circle)  # noqa: F405
        print('0')
        df = pd.DataFrame(obj.values())
        for col in df.columns:
            if col != 'last_updated_date':
                converted = pd.to_datetime(df[col], errors='coerce')
 
                if converted.notna().sum() > 0:
                    df[col] = converted.dt.strftime('%d-%b-%y')
            else:
                converted = pd.to_datetime(df[col], errors='coerce')
                if converted.notna().sum() > 0:
                    df[col] = converted.dt.strftime('%d-%b-%y %H:%M:%S')
 
 
        print("1")
        current_date = dtime.now().strftime("%Y-%m-%d")
        current_time = dtime.now().strftime("%H-%M-%S")
 
        BASE_URL = os.path.join(settings.MEDIA_ROOT, "alok_sir_tracking")
        os.makedirs(BASE_URL, exist_ok=True)
        output_folder = os.path.join(BASE_URL, f"generated_files_{current_date}")
        os.makedirs(output_folder, exist_ok=True)
       
        tracker_file_path = os.path.join(output_folder, f"TRACKER_FILE_{current_date}_{current_time}.xlsx")
        print('2')
        df.insert(0, "Unique ID", range(1, len(df) + 1))
        print(df)
       
        df.drop(columns=['id', df.columns.tolist()[-1], df.columns.tolist()[-2]], inplace=True)
 
        template_path = os.path.join(BASE_URL, "template", "templateAlok.xlsx")
        wb = load_workbook(template_path)
        ws = wb.active  
        print("3")
        start_row = 5
        for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=False), start=start_row):
            for c_idx, value in enumerate(row, start=1):
                ws.cell(row=r_idx, column=c_idx, value=value)
 
        wb.save(tracker_file_path)
        print("4")
        relative_path = tracker_file_path.replace(settings.MEDIA_ROOT, '').lstrip(os.sep)
        download_url = request.build_absolute_uri(
            os.path.join(settings.MEDIA_URL, relative_path).replace('\\', '/')
        )
        return Response({'message': f'Welcome {userId}! Credentials verified.', "download_link": download_url}, status=200)
   
   
    except Exception as e:
        return Response({"error": f"{str(e)}"},status=500)
    
############################################################# DASHBOARD ##########################################################################

@api_view(['GET', 'POST'])
def daily_dashboard_file(request):
    circle = request.data.get('circle')
    site_tagging = request.data.get('site_tagging')
    relocation_method = request.data.get('relocation_method')
    new_toco_name = request.data.get('new_toco_name')
    start_date = request.data.get('from_date')
    end_date = request.data.get('to_date')
   
    all_unique_circles = list(
        AlokTrackerModel.objects.exclude(circle__isnull=True)
        .distinct("circle")
        .values_list("circle", flat=True)
    )

    all_unique_site_tagging = list(
        AlokTrackerModel.objects.exclude(site_tagging__isnull=True)
        .distinct("site_tagging")
        .values_list("site_tagging", flat=True)
    )

    all_unique_relocation_method = list(
        AlokTrackerModel.objects.exclude(relocation_method__isnull=True)
        .distinct("relocation_method")
        .values_list("relocation_method", flat=True)
    )

    all_unique_new_toco_name = list(
        AlokTrackerModel.objects.exclude(new_toco_name__isnull=True)
        .distinct("new_toco_name")
        .values_list("new_toco_name", flat=True)
    )

    # ✅ Add "ALL" at the top of each list
    unique_data = {
        "unique_circle": ["ALL"] + sorted(all_unique_circles),
        "unique_site_tagging": ["ALL"] + sorted(all_unique_site_tagging),
        "unique_relocation_method": ["ALL"] + sorted(all_unique_relocation_method),
        "unique_new_toco_name": ["ALL"] + sorted(all_unique_new_toco_name),
    }

    # Default to 'ALL' if not provided
    circle = circle or 'ALL'
    site_tagging = site_tagging or 'ALL'
    relocation_method = relocation_method or 'ALL'
    new_toco_name = new_toco_name or 'ALL'
    
    start_date = dtime.strptime(start_date, "%Y-%m-%d").date() if start_date else None
    end_date = dtime.strptime(end_date, "%Y-%m-%d").date() if end_date else None
 
    try:
        ############################################################## 🔹 Dynamic filters #########################################################
        filters = {}
        if circle != 'ALL':
            filters['circle'] = circle
        if site_tagging != 'ALL':
            filters['site_tagging'] = site_tagging
        if relocation_method != 'ALL':
            filters['relocation_method'] = relocation_method
        if new_toco_name != 'ALL':
            filters['new_toco_name'] = new_toco_name
 
        ############################################################## 🔹 Fetch data ###############################################################
        obj = AlokTrackerModel.objects.filter(**filters)  # noqa: F405
        df = pd.DataFrame(obj.values())
 
        if df.empty:
            return Response({'error': 'No data found for given filters'}, status=404)
 
        ############################################################### 🔹 Convert all date columns to datetime ####################################
        for col in df.columns:
            if "Date" in col:
                df[col] = pd.to_datetime(df[col], format="%d-%b-%y", errors="coerce")
 
        ################################################################### 🔹 Determine start_date and end_date for 26 → 25 cycle #####################
        today = dtime.today().date()
 
        if not start_date or not end_date:
            if today.day >= 26:
                start_date = today.replace(day=25)
                if today.month == 12:
                    end_date = today.replace(year=today.year + 1, month=1, day=25)
                else:
                    end_date = today.replace(month=today.month + 1, day=25)
            else:
                if today.month == 1:
                    start_date = today.replace(year=today.year - 1, month=12, day=25)
                else:
                    start_date = today.replace(month=today.month - 1, day=25)
                end_date = today.replace(day=25)
 
        ############################################################## 🔹 Generate date range and formatted column headers ###########################
        
        date_range = pd.date_range(start=start_date, end=min(end_date, today)).date
 
        formatted_dates = [d.strftime("%d-%b-%y") for d in date_range]
        result_columns = ["Milestone Track/Site Count", "CF"] + formatted_dates
        result = pd.DataFrame(columns=result_columns)
 
        ###################################################### 🔹 Milestone list #############################################################
        milestones = [
            "RFAI Date",
            "Allocation Date",
            "RFAI Survey Date",
            "RFAI Survey Done Date",
            "MO Punch Date",
            "Material Dispatch Date",
            "Material Delivered Date",
            "Installation Start Date",
            "Installation End Date",
            "Integration Date",
            "EMF Submission Date",
            "Alarm Rectification Done Date",
            "SCFT Done Date",
            "SCFT Offered Date",
            "RAN PAT Offer Date",
            "RAN SAT Offer Date",
            "MW Phy AT Offer Date",
            "MW Soft AT Offer Date",
            "MW MS1 Date (MIDS)",
            "Site ONAIR Date",
            "I-Deploy ONAIR Date",
        ]
 
        # #####################################################🔹 Loop through milestones and count per date ######################################
 
        for milestone in milestones:
            print(milestone)
            milestone_df_format = (
                milestone.lower()
                .replace(" ", "_")
                .replace("-", "_")
                .replace("(", "")
                .replace(")", "")
            )
 
            if milestone_df_format not in df.columns:
                continue  # skip if milestone column not in df
 
            # 🧹 Clean conversion to datetime (ignore time)
            df[milestone_df_format] = pd.to_datetime(df[milestone_df_format], errors="coerce").dt.date
 
            # Valid dates only
            valid_dates = df[milestone_df_format].dropna()
 
            # Skip empty milestones gracefully
            if valid_dates.empty:
                row = {"Milestone Track/Site Count": milestone, "CF": "-", **{d.strftime("%d-%b-%y"): "-" for d in date_range}}
                result.loc[len(result)] = row
                continue
 
            cf_count = (valid_dates < start_date).sum()
 
            cumulative = cf_count
            row = {"Milestone Track/Site Count": milestone, "CF": cf_count}
            for date in date_range:
                if(date >= today):
                    row[date.strftime("%d-%b-%y")] = 0
                    continue
                count = (valid_dates == date).sum()
                cumulative += count
                row[date.strftime("%d-%b-%y")] = cumulative
 
            result.loc[len(result)] = row
 
        ######################################################## 🔹 Convert and format ##############################################
        result = result.astype(str).reset_index(drop=True)
 
        result.columns = [
            col.strftime("%d-%b-%y") if isinstance(col, (dtime,)) or hasattr(col, "strftime") else col
            for col in result.columns
        ]
 
        print(result.columns)
 
        ############################################# 🔹 Arrange columns #####################################
        result = result[["Milestone Track/Site Count", "CF"] + formatted_dates]
        
        last_col = formatted_dates[-1]
        result[last_col] = pd.to_numeric(result[last_col], errors='coerce')

        # ✅ Compute difference with next row (current - next)
        result['Gap'] = result[last_col].diff(-1)

        # ✅ Optional: convert to int and replace NaN with blank
        result['Gap'] = result['Gap'].fillna('-').astype(str)
        
        result['Milestone Track/Site Count'] = result['Milestone Track/Site Count'].apply(lambda col: col.replace(" Date", "") if " Date" in col else col)
        
        ############################################################################################################################
        new_result = result.copy()
        
        for i, date in enumerate(formatted_dates, start=1):
            new_result.rename(columns={date : f'date_{i}'}, inplace=True)
        
        result_json = new_result.to_dict(orient="records")
        json_data = json.dumps(result_json)


        current_date = dtime.now().strftime("%Y-%m-%d")
        current_time = dtime.now().strftime("%H-%M-%S")
 
        BASE_URL = os.path.join(settings.MEDIA_ROOT, "alok_sir_tracking")
        os.makedirs(BASE_URL, exist_ok=True)
        output_folder = os.path.join(BASE_URL, f"generated_files_{current_date}")
        os.makedirs(output_folder, exist_ok=True)
       
        dashboard_file_path = os.path.join(output_folder, f"DAILY_DASHBOARD_FILE_{circle}_{site_tagging}_{relocation_method}_{new_toco_name}_{current_date}_{current_time}.xlsx")
        
        with pd.ExcelWriter(dashboard_file_path, engine='xlsxwriter') as writer:
            result.to_excel(writer, index=False, sheet_name='Daily Waterfall MS1')
        
        dashboard_file_path = dashboard_file_path.replace(settings.MEDIA_ROOT, settings.MEDIA_URL).replace("\\", "/")
        download_link = request.build_absolute_uri(dashboard_file_path)
    
        return Response({'message': 'Dashboard created successfully !!!', "download_link": download_link, "data": json_data, "dates": formatted_dates, "unique_data": unique_data}, status=200)
    except Exception as e:
        return Response({"error": f"{str(e)}"},status=500)


@api_view(['GET','POST'])
def weekly_monthly_dashboard_view(request):
    circle = request.data.get('circle')
    site_tagging = request.data.get('site_tagging')
    relocation_method = request.data.get('relocation_method')
    new_toco_name = request.data.get('new_toco_name')
    month_filtered = request.data.get('month')
    year_filtered = request.data.get('year')
 
    # Default to 'ALL' if not provided
    circle = circle or 'ALL'
    site_tagging = site_tagging or 'ALL'
    relocation_method = relocation_method or 'ALL'
    new_toco_name = new_toco_name or 'ALL'
    
    if month_filtered and year_filtered:
        month_filtered = int(month_filtered)
        year_filtered = int(year_filtered)

        month_end = date(year_filtered, month_filtered, 25)

        if month_filtered == 1:
            month_start = date(year_filtered - 1, 12, 26)
        else:
            month_start = date(year_filtered, month_filtered - 1, 26)
    else:
        month_start = None
        month_end = None
   
    all_unique_circles = list(
        AlokTrackerModel.objects.exclude(circle__isnull=True)
        .distinct("circle")
        .values_list("circle", flat=True)
    )

    all_unique_site_tagging = list(
        AlokTrackerModel.objects.exclude(site_tagging__isnull=True)
        .distinct("site_tagging")
        .values_list("site_tagging", flat=True)
    )

    all_unique_relocation_method = list(
        AlokTrackerModel.objects.exclude(relocation_method__isnull=True)
        .distinct("relocation_method")
        .values_list("relocation_method", flat=True)
    )

    all_unique_new_toco_name = list(
        AlokTrackerModel.objects.exclude(new_toco_name__isnull=True)
        .distinct("new_toco_name")
        .values_list("new_toco_name", flat=True)
    )

    # ✅ Add "ALL" at the top of each list
    unique_data = {
        "unique_circle": ["ALL"] + sorted(all_unique_circles),
        "unique_site_tagging": ["ALL"] + sorted(all_unique_site_tagging),
        "unique_relocation_method": ["ALL"] + sorted(all_unique_relocation_method),
        "unique_new_toco_name": ["ALL"] + sorted(all_unique_new_toco_name),
    }

    try:
        # 🔹 Dynamic filters
        filters = {}
        if circle != 'ALL':
            filters['circle'] = circle
        if site_tagging != 'ALL':
            filters['site_tagging'] = site_tagging
        if relocation_method != 'ALL':
            filters['relocation_method'] = relocation_method
        if new_toco_name != 'ALL':
            filters['new_toco_name'] = new_toco_name
 
        # 🔹 Fetch data
        obj = AlokTrackerModel.objects.filter(**filters)  # noqa: F405
        df = pd.DataFrame(obj.values())
 
        if df.empty:
            return Response({'error': 'No data found for given filters'}, status=404)
       
        for col in df.columns:
            if "Date" in col:
                df[col] = pd.to_datetime(df[col], format="%d-%b-%y", errors="coerce")
               
        today = dtime.today().date()
 
        if today.month >= 4:
            fy_start = dtime(today.year, 2, 26).date()   # 26-Apr current year start
            fy_end = dtime(today.year + 1, 3, 25).date() # 25-Mar next year end
        else:
            fy_start = dtime(today.year - 1, 2, 26).date()
            fy_end = dtime(today.year, 3, 25).date()
 
        # 🧩 2. Determine current cycle (26th prev → 25th curr)
        if today.day >= 26:
            if today.month == 12:
                current_cycle_start = dtime(today.year, 12, 26).date()
                current_cycle_end = dtime(today.year + 1, 1, 25).date()
            else:
                current_cycle_start = dtime(today.year, today.month, 26).date()
                current_cycle_end = dtime(today.year, today.month + 1, 25).date()
        else:
            if today.month == 1:
                current_cycle_start = dtime(today.year - 1, 12, 26).date()
            else:
                current_cycle_start = dtime(today.year, today.month - 1, 26).date()
            current_cycle_end = dtime(today.year, today.month, 25).date()
 
        # 🗓️ 3. Create monthly periods (Apr → month before current)
        months = []
        start = fy_start
        while start <= current_cycle_start:
            if start.month == 12:
                end = dtime(start.year + 1, 1, 25).date()
            else:
                end = dtime(start.year, start.month + 1, 25).date()
            months.append((start, end))
            start = end + timedelta(days=1)
 
        # 🗓️ 4. Create weekly periods for current month
        weeks = []
        
        if month_start and month_end:
            current_cycle_start = month_start
            current_cycle_end = month_end
        
        week_start = current_cycle_start
 
        # First week: from 26th → Sunday
        first_sunday = week_start + timedelta(days=(6 - week_start.weekday()))
        weeks.append((week_start, min(first_sunday, current_cycle_end)))
 
        # Next weeks: Monday–Sunday
        next_start = weeks[-1][1] + timedelta(days=1)
        while next_start <= current_cycle_end:
            week_end = next_start + timedelta(days=6)
            if week_end > current_cycle_end:
                week_end = current_cycle_end
            weeks.append((next_start, week_end))
            next_start = week_end + timedelta(days=1)
 
        print(weeks)
 
        # 📊 5. Prepare result DataFrame
        result = pd.DataFrame()
       
       
        # result.set_index("Milestone Track/Site Count", inplace=True)
 
        milestones = [
            "Allocation Date",
            "RFAI Date",
            "RFAI Survey Done Date",
            "MO Punch Date",
            "Material Delivered Date",
            "Installation End Date",
            "Integration Date",
            "EMF Done Date",
            "Alarm Rectification Done Date",
            "SCFT Done Date",
            "RAN PAT Offer Date",
            "RAN SAT Offer Date",
            "MW PHY AT Offer Date",
            "MW Soft AT Offer Date",
            "Site ONAIR Date"
        ]
 
        data = []
        print(df.columns)
        for milestone in milestones:
            
            milestone_df_format = milestone.lower().replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "")
            print(milestone_df_format)
            if milestone_df_format not in df.columns:
                continue
            
            milestone_data = pd.to_datetime(df[milestone_df_format], errors='coerce').dt.date
            row = {"Milestone Track/Site Count": milestone}
            if milestone_data.dropna().empty:
                row["CF"] = "-"
                # Set all month and week columns to "-"
                for _, end in months:
                    month_name = end.strftime("%b-%y")
                    row[month_name] = "-"
                for i, _ in enumerate(weeks, 1):
                    week_name = f"{current_cycle_end.strftime('%b-%y')} W{i}"
                    row[week_name] = "-"
                data.append(row)
                continue
 
 
            # CF → sites before financial year start
            row["CF"] = (milestone_data < fy_start).sum()
 
            cumulative_month = row["CF"]
            print("data:- \n",milestone_data)
            for start, end in months:
                month_name = end.strftime("%b-%y")
                count = ((milestone_data >= start) & (milestone_data <= end)).sum()
                cumulative_month += count
                row[month_name] = cumulative_month
 
            cumulative_week = 0
            for i, (start, end) in enumerate(weeks, 1):
                week_name = f"{current_cycle_end.strftime('%b-%y')} W{i}"
                if(start >= today):
                    row[week_name] = 0
                count = ((milestone_data >= start) & (milestone_data <= end)).sum()
                cumulative_week += count
                row[week_name] = cumulative_week
 
            data.append(row)
 
        # 🧮 6. Build final DataFrame
        result = pd.DataFrame(data)
 
        # 🧹 7. Fill NaNs with 0 and convert numeric columns to int
        for col in result.columns:
            if col != "Milestone Track/Site Count":
                result[col] = result[col].astype(str)
 
        # ✅ Final tidy DataFrame
        result = result.reset_index(drop=True)
        print(2)
        result['Milestone Track/Site Count'] = result['Milestone Track/Site Count'].apply(lambda col: col.replace(" Date", "") if " Date" in col else col)
 
        new_data = result.copy()
        months_columns = [col for col in new_data.columns.to_list()[2:] if " W" not in col]
        months_data = new_data[new_data.columns.to_list()[:2] + months_columns].copy()
        
        weeks_columns = [col for col in new_data.columns.to_list()[2:] if " W" in col]
        
        week_data = new_data[new_data.columns.to_list()[:1] + weeks_columns].copy()
        
        months_data.rename(columns={
            col : f"Month-{i}" for i, col in enumerate(months_columns, start=1)
        }, inplace=True)
        
        week_data.rename(columns={
            col : f"Month_Week-{i}" for i, col in enumerate(weeks_columns, start=1)
        }, inplace=True)
        
        unique_data.update(**{"month_columns": months_columns, "week_columns" : weeks_columns})
        

        month_dict_data = months_data.to_dict(orient="records")
        month_json_data = json.dumps(month_dict_data)
        week_dict_data = week_data.to_dict(orient="records")
        week_json_data = json.dumps(week_dict_data)
        
        current_date = dtime.now().strftime("%Y-%m-%d")
        current_time = dtime.now().strftime("%H-%M-%S")
 
        BASE_URL = os.path.join(settings.MEDIA_ROOT, "alok_sir_tracking")
        os.makedirs(BASE_URL, exist_ok=True)
        output_folder = os.path.join(BASE_URL, f"generated_files_{current_date}")
        os.makedirs(output_folder, exist_ok=True)
       
        dashboard_file_path = os.path.join(output_folder, f"WEEKLY_MONTHY_DASHBOARD_FILE_{circle}_{site_tagging}_{relocation_method}_{new_toco_name}_{current_date}_{current_time}.xlsx")
       
        with pd.ExcelWriter(dashboard_file_path, engine='xlsxwriter') as writer:
            result.to_excel(writer, index=False, sheet_name='Monthly MS1')
       
        dashboard_file_path = dashboard_file_path.replace(settings.MEDIA_ROOT, settings.MEDIA_URL).replace("\\", "/")
        download_link = request.build_absolute_uri(dashboard_file_path)
   
        return Response({'message': 'Weekly and Monthly Dashboard created successfully !!!', "download_link": download_link, "unique_data": unique_data, "months_data": month_json_data, "week_data": week_json_data}, status=200)
    except Exception as e:
        return Response({"error": f"{str(e)}"},status=500)
    

@api_view(['GET', 'POST'])
def gap_view(request):
    circle = request.data.get('circle')
    site_tagging = request.data.get('site_tagging')
    relocation_method = request.data.get('relocation_method')
    new_toco_name = request.data.get('new_toco_name')
    last_date = request.data.get('last_date')
    milestone1 = request.data.get('milestone1')
    milestone2 = request.data.get('milestone2')
    
    circle = circle or 'ALL'
    site_tagging = site_tagging or 'ALL'
    relocation_method = relocation_method or 'ALL'
    new_toco_name = new_toco_name or 'ALL'
    last_date = dtime.strptime(last_date, "%Y-%m-%d").date() if last_date else None
    
    try:
        
        today = dtime.today().date()
 
        if not last_date:
            if today.day >= 26:
                if today.month == 12:
                    last_date = today.replace(year=today.year + 1, month=1, day=25)
                else:
                    last_date = today.replace(month=today.month + 1, day=25)
            else:
                last_date = today.replace(day=25)
                
            last_date = min(today - timedelta(days=1), last_date)
                
        filters = {}
        if circle != 'ALL':
            filters['circle'] = circle
        if site_tagging != 'ALL':
            filters['site_tagging'] = site_tagging
        if relocation_method != 'ALL':
            filters['relocation_method'] = relocation_method
        if new_toco_name != 'ALL':
            filters['new_toco_name'] = new_toco_name
        filters[f"{milestone1}__lte"] = last_date
 
        # 🔹 Fetch data
        obj1 = AlokTrackerModel.objects.filter(**filters)  # noqa: F405
        df1 = pd.DataFrame(obj1.values())
        
        filters[f"{milestone2}__lte"] = last_date
        
        obj2 = AlokTrackerModel.objects.filter(**filters)  # noqa: F405
        df2 = pd.DataFrame(obj2.values())
        
        df1['key'] = df1['circle'].astype(str) + "_" + df1['site'].astype(str)
        df2['key'] = df2['circle'].astype(str) + "_" + df2['site'].astype(str)

        df = df1[~df1['key'].isin(df2['key'])].drop(columns=['key'])
        
        for col in df.columns:
            if col != 'last_updated_date':
                converted = pd.to_datetime(df[col], errors='coerce')
 
                if converted.notna().sum() > 0:
                    df[col] = converted.dt.strftime('%d-%b-%y')
            else:
                converted = pd.to_datetime(df[col], errors='coerce')
                if converted.notna().sum() > 0:
                    df[col] = converted.dt.strftime('%d-%b-%y %H:%M:%S')
 
 
        print("1")
        current_date = dtime.now().strftime("%Y-%m-%d")
        current_time = dtime.now().strftime("%H-%M-%S")
 
        BASE_URL = os.path.join(settings.MEDIA_ROOT, "alok_sir_tracking")
        os.makedirs(BASE_URL, exist_ok=True)
        output_folder = os.path.join(BASE_URL, f"generated_files_{current_date}")
        os.makedirs(output_folder, exist_ok=True)
       
        tracker_file_path = os.path.join(output_folder, f"TRACKER_GAP_FILE_{milestone1}_{milestone2}_{circle}_{site_tagging}_{relocation_method}_{new_toco_name}_{current_date}_{current_time}.xlsx")
        print('2')
        df.insert(0, "Unique ID", range(1, len(df) + 1))
        print(df)
       
        df.drop(columns=['id', df.columns.tolist()[-1], df.columns.tolist()[-2]], inplace=True)
 
        template_path = os.path.join(BASE_URL, "template", "templateAlok.xlsx")
        wb = load_workbook(template_path)
        ws = wb.active  
        print("3")
        start_row = 5
        for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=False), start=start_row):
            for c_idx, value in enumerate(row, start=1):
                ws.cell(row=r_idx, column=c_idx, value=value)
 
        wb.save(tracker_file_path)
        print("4")
        relative_path = tracker_file_path.replace(settings.MEDIA_ROOT, '').lstrip(os.sep)
        download_url = request.build_absolute_uri(
            os.path.join(settings.MEDIA_URL, relative_path).replace('\\', '/')
        )
        
        return Response({'message': 'request processed successfully !!!', "download_link": download_url}, status=200)
    except Exception as e:
        return Response({"error": f"{str(e)}"},status=500)