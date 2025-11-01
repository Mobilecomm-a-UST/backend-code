from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
import os
import numpy as np
import re
from mcom_website.settings import MEDIA_URL,MEDIA_ROOT
from django.conf import settings
from datetime import datetime as dtime

    
circle_map = {
    "AP": "AP",
    "BH": "BIH",
    "CH": "CHN",
    "DL": "DEL",
    "HR": "HRY",
    "JK": "JK",
    "KK": "KK",
    "KO": "KOL",
    "MP": "MP",
    "MU": "MUM",
    "OR": "ORI",
    "OD": "ORI",
    "PB": "PUN",
    "RJ": "RAJ",
    "TN": "ROTN",
    "UE": "UPE",
    "UW": "UPW",
    "WB": "WB",
    "MH": "MH",
    "GJ": "GUJ",
    "KL": "KL",
    "AS": "ASM",
    "CN": "CHN",
    "NE": "NE",
    "MUM":"MUM",
    "BI":"BIH",
    "PJ": "PUN",
}
 
def cut_if_alpha(s):
    """Cut last char if it is alphabet (any case)."""
    return s[:-1] if re.match(r"[A-Za-z]", s[-1]) else s
 
def cut_if_upper(s):
    """Cut last char if it is uppercase alphabet."""
    return s[:-1] if re.match(r"[A-Z]", s[-1]) else s
 
def strip_x(s):
    """Remove leading x/X characters."""
    return re.sub(r"^[xX]+", "", s)
 
def parse_neik(sn, prefix="NE-ik-"):
    if "DEL" in sn:
        return strip_x(sn.split("-")[-1].split("_")[-2][:-1])
    
    if "Sams" in sn:
        return sn.split(",")[-2].split("_")[-1]
    
    if re.match(r'^[xX]', sn):
        return strip_x(sn)
    
    return sn.split("-")[-1].split("_")[-2][:-1]

prefix_parsers = {
    "AP_": lambda sn: sn.split("_")[-2][:-1],
    "AS_": lambda sn: sn.split("_")[-2][:-1],
    "GJ_": lambda sn: sn.split("_")[-2][:-1],
    "BH_": lambda sn: sn.split("_")[-2][:-1] if len(sn.split("_")[-2][:-1])>0 else sn.split("_")[-3],
    "NE_": lambda sn: sn.split("_")[-2][:-1],
    "Sams-": lambda sn: sn.split(",")[1].split("_")[-1],
    "WB_": lambda sn: cut_if_alpha(sn.split("_")[-2]),
    "MU_": lambda sn: cut_if_alpha(sn.split("_")[-2]),
    "UE_": lambda sn: cut_if_alpha(sn.split("_")[-2]),
    "MP_": lambda sn: cut_if_alpha(sn.split("_")[-2]),
    "OD_": lambda sn: cut_if_alpha(sn.split("_")[-2]),
    "UW_": lambda sn: cut_if_alpha(sn.split("_")[-2]),
    "TN_": lambda sn: cut_if_alpha(sn.split("_")[-2]),
    "JH_": lambda sn: cut_if_upper(sn.split("_")[-2]),
    "KK_": lambda sn: cut_if_upper(sn.split("_")[-2]),
    "KO_": lambda sn: cut_if_upper(sn.split("_")[-2]),
    "HR_": lambda sn: cut_if_upper(sn.split("_")[-2]),
    "JK_": lambda sn: cut_if_upper(sn.split("_")[-2]),
    "CH_": lambda sn: cut_if_upper(sn.split("_")[-2]),
    "RJ_": lambda sn: cut_if_upper(sn.split("_")[-2]),
    "DL_": lambda sn: strip_x(cut_if_upper(sn.split("_")[-2])),
    "PB_": lambda sn: (
        cut_if_upper(sn.split("_")[-3])
        if sn.split("_")[-1] in ["FDD", "TDD"]
        else cut_if_upper(sn.split("_")[-2])
    ),
    "NE-ik-": lambda sn: parse_neik(sn, "NE-ik-"),
    "EWB_": lambda sn: sn.split("_")[-2],
}

def extract_site_name(sn):
    for prefix, parser in prefix_parsers.items():
        if sn.startswith(prefix):
            try:
                return parser(sn)
            except Exception:
                return None
    return None
 
def get_circle(short_name):
    if "NE-ik" in short_name:
        if "Sams-" not in short_name:
            return short_name.split("-")[-1].split("_")[0]
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


def get_5G_cell_site_id(name):
    return re.sub(r"^[x]+","",name.split("_")[-2] if "_" in name else "") if not name.startswith("DL") else re.sub(r"^[a-zA-Z]+|[a-zA-Z]+$","",name.split("_")[-2] if "_" in name else "")


@api_view(['POST'])
def referenceView(request):
    raw_data_5G = request.FILES.get('main_file_5G')
    raw_data_4G = request.FILES.get('main_file_4G')
    reference_file = request.FILES.get('reference_file')
    
    if not raw_data_4G or not raw_data_5G or not reference_file:
        return Response('All files are required !', status=400)
    
    print('1. FILES FETCHED !')
    
    try:
        
        main_5G_df = pd.read_csv(raw_data_5G) if raw_data_5G.name.endswith('.csv') else pd.read_excel(raw_data_5G)
        main_4G_df = pd.read_csv(raw_data_4G) if raw_data_4G.name.endswith('.csv') else pd.read_excel(raw_data_4G)
        
        main_4G_df["Short name"] = main_4G_df["Short name"].fillna(method="ffill")
        main_5G_df["Short name"] = main_5G_df["Short name"].fillna(method="ffill")
        
        main_4G_df.drop_duplicates(subset='Short name', inplace=True)
        main_5G_df.drop_duplicates(subset='Short name', inplace=True)
        
        reference_4G_df = pd.read_excel(reference_file, sheet_name="4G1")
        reference_5G_df = pd.read_excel(reference_file, sheet_name="5G1")
        
        print('2. FILES READ !')
        
        df_5G1 = main_5G_df[['Short name','Cell Name']]
        df_4G1 = main_4G_df[['Short name','MV Cell Name']]
        
        reference_5G_df = reference_5G_df[['Short name', 'SITE', 'CIRCLE2', 'SITE_CIRCLE']].drop_duplicates(subset='Short name')
        reference_4G_df = reference_4G_df[['Short name', 'SITEID', 'CIRCLE2', 'SITE_CIRCLE']].drop_duplicates(subset='Short name')
        
        df_5G1 = pd.merge(df_5G1, reference_5G_df, on='Short name', how='left')
        df_4G1 = pd.merge(df_4G1, reference_4G_df, on='Short name', how='left')
        
        df_5G1 = df_5G1[
            df_5G1['SITE'].isna() | (df_5G1['SITE'].astype(str).str.strip() == '') |
            df_5G1['CIRCLE2'].isna() | (df_5G1['CIRCLE2'].astype(str).str.strip() == '')
        ]
        
        df_4G1 = df_4G1[
            df_4G1['SITEID'].isna() | (df_4G1['SITEID'].astype(str).str.strip() == '') |
            df_4G1['CIRCLE2'].isna() | (df_4G1['CIRCLE2'].astype(str).str.strip() == '')
        ]
        
        print('3.  OLD SITE VS CIRCLE MERGED AND NEW SITES SEGREGATED !')
        
        # 4G
        
        df_4G1['Circle'] = df_4G1['Short name'].apply(lambda x: get_circle(x))
        
        df_4G1["Circle"].replace({"BIH":"BH","EWB":"WB"},inplace=True)
        
        df_4G1["CIRCLE2"] = df_4G1['Circle'].apply(lambda x: circle_map.get(x, None))
        
        df_4G1['SITEID'] = df_4G1['Short name'].apply(lambda x: extract_site_name(x))
        
        df_4G1['CIRCLE2'] = df_4G1.apply(
            lambda x: "JRK" if (x['CIRCLE2'] == "BIH" and str(x['SITEID']).startswith('J')) else x['CIRCLE2'],axis=1
        )
        
        df_4G1['SITEID'] = df_4G1.apply(
            lambda x: re.sub(r"^[a-zA-Z]+|[a-zA-Z]+$", "", x['SITEID']) if x['CIRCLE2']=="DEL" else x['SITEID'], axis=1
        )
        
        new_df = df_4G1[
            (~df_4G1['Short name'].str.contains("_ES_")) &
            (~df_4G1['Short name'].str.contains("_IS_")) &
            (~df_4G1['Short name'].str.contains("_OS_"))
        ].copy()
        
        all_data = new_df.copy()
        
        hs_data = new_df[
            (new_df['Short name'].str.contains("_HS_")) &
            (new_df['Circle'].isin(['AS', 'MU', 'NE']))
        ].copy()
        
        all_data_clean = all_data[~all_data['Short name'].str.contains("_HS_")]
        
        mrbts_df = all_data_clean[all_data_clean['Short name'].str.contains("-PLMN-PLMN/MRBTS-")]
        mrbts_cell_name_dict = {
            x['MV Cell Name']: x['Short name']
            for _, x in mrbts_df.iterrows()
            if pd.notna(x['MV Cell Name'])
        }
        
        mrbts_cell_name_dict = {value:key for key, value in mrbts_cell_name_dict.items()}
        mrbts_df['MV Cell Name'] = mrbts_df['Short name'].apply(
            lambda x: mrbts_cell_name_dict.get(x, '')
        )
        print("1")
        mrbts_df['SITEID'] = (
            mrbts_df['MV Cell Name']
            .fillna("")                            
            .apply(lambda x: x.split("_")[-2][:-1] if "_" in x else "")
        )
        
        print("2")
        
        all_data_clean_new = all_data_clean[~all_data_clean['Short name'].str.contains("-PLMN-PLMN/MRBTS-")]
        print("3")
        final_df = pd.concat([mrbts_df,all_data_clean_new, hs_data], ignore_index=True)
        
        final_df['SITEID'] = final_df['SITEID'].apply(
            lambda x: x.strip() if x is not None and isinstance(x, str) else x
        )
        
        print("4")
        # final_df['SITEID'] = final_df['SITEID'].map( lambda x: x.strip() if x != None else "")  # noqa: E711
        final_df['CIRCLE2'] = final_df['CIRCLE2'].apply( lambda x: x.strip() if x is not None and isinstance(x, str) else x)
        
        
        print("5")

        final_df['SITE_CIRCLE'] = final_df['SITEID']+'_'+final_df['CIRCLE2']
        
        print('4. 4G SITE VS CIRCLE DONE !')
        
        #5G
        
        df_5G1["CIRCLE2"] = df_5G1['Short name'].map(lambda x: circle_map.get(x.split("_")[0]) if "_" in x else circle_map.get(x.split("-")[1][0:2]))        
        print('1')
        df_5G1['SITE'] = df_5G1.apply(lambda x: get_5G_cell_site_id(str(x['Cell Name'])) if str(x['Short name']).startswith("Nokia") or str(x['Short name']).startswith("Sams") else get_5G_cell_site_id(x['Short name']), axis=1)
        print('1')
        df_5G1['CIRCLE2'] = df_5G1.apply(
            lambda x: "JRK" if x['CIRCLE2'] == "BIH" and str(x['SITE']).startswith("J") else x['CIRCLE2'],
            axis=1
        )
        print('1')
        df_5G1['SITE'] = df_5G1['SITE'].apply( lambda x: x.strip() if x is not None and isinstance(x, str) else x)
        df_5G1['CIRCLE2'] = df_5G1['CIRCLE2'].apply( lambda x: x.strip() if x is not None and isinstance(x, str) else x)
        print('1')
        df_5G1['SITE_CIRCLE'] = df_5G1['SITE'] + '_' + df_5G1['CIRCLE2']
        
        print('5. 5G SITE VS CIRCLE DONE !')
        
        # GENERATING FILES

        BASE_URL = os.path.join(settings.MEDIA_ROOT, "relocation_tracking")
        os.makedirs(BASE_URL, exist_ok=True)
        output_folder = os.path.join(BASE_URL, f"reference_generated_file")
        os.makedirs(output_folder, exist_ok=True)
        
        file_path_reference = os.path.join(output_folder, f"REFERENCE_FILE.xlsx")

        with pd.ExcelWriter(file_path_reference, engine='xlsxwriter') as writer:
            final_df.to_excel(writer, index=False, sheet_name='4G1')
            df_5G1.to_excel(writer, index=False, sheet_name="5G1")
            
        print('6. REFERENCE FILE CREATED !')
        
        relative_url = file_path_reference.replace(settings.MEDIA_ROOT, settings.MEDIA_URL)
        relative_url = relative_url.replace("\\", "/")
        download_link = request.build_absolute_uri(relative_url)
        
#################################################################### RESPONSE ##########################################################################

        return Response(
            {
            "status": True,
            "message": "File saved successfully !!!",
            "download_url": download_link,
            },
            status=200,
        ) 
        
    except Exception as e:
        return Response({"error": f"{str(e)}"},status=500)

@api_view(['POST'])
def relocationView(request):
    raw_data_5G = request.FILES.get('main_file_5G')
    raw_data_4G = request.FILES.get('main_file_4G')
    raw_hourly_data_4G = request.FILES.get('hourly_file_4G')
    reference_file = request.FILES.get('reference_file')
    relocation_file = request.FILES.get('relocation_file')
    
    
    if not raw_data_4G or not raw_data_5G or not reference_file or not relocation_file or not raw_hourly_data_4G:
        return Response('All files are required !', status=400)
    
    print('1. FILES FETCHED !')
    
    try:
        main_5G_df = pd.read_csv(raw_data_5G) if raw_data_5G.name.endswith('.csv') else pd.read_excel(raw_data_5G)
        main_4G_df = pd.read_csv(raw_data_4G, na_values=["∞", "âˆž", "inf", "-inf"]) if raw_data_4G.name.endswith('.csv') else pd.read_excel(raw_data_4G, na_values=["∞", "âˆž", "inf", "-inf"])
        
        print(main_4G_df.dtypes)
        
        hourly_4G_df = pd.read_csv(raw_hourly_data_4G) if raw_hourly_data_4G.name.endswith('.csv') else pd.read_excel(raw_hourly_data_4G)
        
        reference_5G_df = pd.read_excel(reference_file, sheet_name='5G1')
        reference_4G_df = pd.read_excel(reference_file, sheet_name='4G1')
        relocation_df_total = pd.read_excel(relocation_file, sheet_name='Main', header=[0,1])
        
        relocation_df_total = relocation_df_total.loc[:, ~((relocation_df_total.columns.get_level_values(0) == '') & (relocation_df_total.columns.get_level_values(1) == ''))]
        
        main_4G_df["Short name"] = main_4G_df["Short name"].fillna(method="ffill")
        main_5G_df["Short name"] = main_5G_df["Short name"].fillna(method="ffill")
        
        main_4G_df = main_4G_df[
            (~main_4G_df['Short name'].str.contains("_ES_")) &
            (~main_4G_df['Short name'].str.contains("_IS_")) &
            (~main_4G_df['Short name'].str.contains("_OS_"))
        ]
        
        HS_main_4G_df = main_4G_df[
            (main_4G_df['Short name'].str.contains("_HS_")) &
            (main_4G_df['Circle'].isin(['AS', 'MU', 'NE','']))
        ]
        
        main_4G_df = main_4G_df[~main_4G_df['Short name'].str.contains("_HS_")]
        
        main_4G_df = pd.concat([main_4G_df, HS_main_4G_df])
        
        # main_4G_df.replace("âˆž", '', inplace=True)
        # exit(0)
        print('2. FILES READ AND UNWANTED SITES OMITTED !')
        
#########################################################################################################################################################
################################################################### 5G FILE ##############################################################################
##########################################################################################################################################################
        
######################################################### 5G SITEID, CIRCLE2, SITE_CIRCLE #############################################################

        reference_5G_df = reference_5G_df[['Short name', 'SITE', 'CIRCLE2', 'SITE_CIRCLE']].drop_duplicates(subset='Short name')
        main_5G_df = pd.merge(main_5G_df, reference_5G_df, on='Short name', how='left')
        
        main_5G_df.rename(columns={"Unnamed: 3": "Date"}, inplace=True)
        
        main_5G_df['Date'] = pd.to_datetime(main_5G_df['Date'], errors='coerce')
        
        main_5G_df['5G Data Volume [GB]'] = main_5G_df['5G Data Volume [GB]'].fillna(-0.000001)
        
        print('3. 5G SITE AND CIRCLE MAPPED !')
        
################################################################## 5G PAYLOAD TREND ##################################################################

        payload_trend_5G_df = pd.pivot_table(
            main_5G_df,
            values='5G Data Volume [GB]',
            index='SITE_CIRCLE',
            columns='Date',
            aggfunc='sum'
        )
        
        payload_trend_5G_df.columns = payload_trend_5G_df.columns.strftime('%d-%b-%y')
        payload_trend_5G_df = payload_trend_5G_df.reset_index()
        numeric_cols = payload_trend_5G_df.columns.drop('SITE_CIRCLE')
        payload_trend_5G_df[numeric_cols] = payload_trend_5G_df[numeric_cols].mask(
            payload_trend_5G_df[numeric_cols] < 0, '-'
        )
        
        print('4. 5G PAYLOAD TREND CREATED !')
        
################################################################### 5G RNA TREND ######################################################################

        RNA_trend_5G_df = pd.pivot_table(
            main_5G_df.loc[main_5G_df['Radio Network Availability %'].notna(),:],
            values='Radio Network Availability %',
            index='SITE_CIRCLE',
            columns='Date',
            aggfunc='mean'
        )
        
        all_site_circles = main_5G_df['SITE_CIRCLE'].unique()
        RNA_trend_5G_df = RNA_trend_5G_df.reindex(all_site_circles)
        
        RNA_trend_5G_df.columns = RNA_trend_5G_df.columns.strftime('%d-%b-%y')
        RNA_trend_5G_df = RNA_trend_5G_df.reset_index()
        
        print('5. 5G RNA TREND CREATED !')
        
#########################################################################################################################################################
################################################################### 4G FILE ##############################################################################
##########################################################################################################################################################
        
######################################################### 4G SITEID, CIRCLE2, SITE_CIRCLE ##############################################################

        reference_4G_df = reference_4G_df[['Short name', 'SITEID', 'CIRCLE2', 'SITE_CIRCLE']].drop_duplicates(subset='Short name')
        main_4G_df = pd.merge(main_4G_df, reference_4G_df, on='Short name', how='left')
        
        # main_4G_df['<3MBPS THPT FLAG'] = main_4G_df['MV_DL User Throughput_Kbps [CDBH]'].apply( lambda x: 1 if pd.notnull(x) and float(x) < 3000 else 0 )
        
        main_4G_df.rename(columns={"Unnamed: 2": "Date"}, inplace=True)
        
        main_4G_df['Date'] = pd.to_datetime(main_4G_df['Date'], errors='coerce')
        
        main_4G_df['MV_4G Data Volume_GB'] = main_4G_df['MV_4G Data Volume_GB'].fillna(-0.000001)
        main_4G_df['TNL Fail [ERAB setup + Release]'] = main_4G_df['TNL Fail [ERAB setup + Release]'].fillna(0)
        main_4G_df['MV_VoLTE Traffic'] = main_4G_df['MV_VoLTE Traffic'].fillna(-0.000001)
        
        print('6. 4G SITE AND CIRCLE MAPPED !')
        
################################################################ PAYLOAD 4G TREND ######################################################################

        payload_trend_4G_df = pd.pivot_table(
            main_4G_df,
            values='MV_4G Data Volume_GB',
            index='SITE_CIRCLE',
            columns='Date',
            aggfunc='sum'
        )
        
        payload_trend_4G_df.columns = payload_trend_4G_df.columns.strftime('%d-%b-%y')
        payload_trend_4G_df = payload_trend_4G_df.reset_index()
        numeric_cols = payload_trend_4G_df.columns.drop('SITE_CIRCLE')
        payload_trend_4G_df[numeric_cols] = payload_trend_4G_df[numeric_cols].mask(
            payload_trend_4G_df[numeric_cols] < 0, '-'
        )
        
        print('7. 4G PAYLOAD TREND CREATED !')
        
################################################################ RNA 4G TREND #############################################################################

        RNA_trend_4G_df = pd.pivot_table(
            main_4G_df.loc[main_4G_df['MV_Radio NW Availability'].notna(),:],
            values='MV_Radio NW Availability',
            index='SITE_CIRCLE',
            columns='Date',
            aggfunc='mean'
        )
        
        all_site_circles = main_4G_df['SITE_CIRCLE'].unique()
        RNA_trend_4G_df = RNA_trend_4G_df.reindex(all_site_circles)
        
        RNA_trend_4G_df.columns = RNA_trend_4G_df.columns.strftime('%d-%b-%y')
        RNA_trend_4G_df = RNA_trend_4G_df.reset_index()
        
        print('8. 4G RNA TREND CREATED !')
        
################################################################ TNL 4G TREND ##########################################################################

        TNL_trend_4G_df = pd.pivot_table(
            main_4G_df,
            values='TNL Fail [ERAB setup + Release]',
            index='SITE_CIRCLE',
            columns='Date',
            aggfunc='sum'
        )
        
        TNL_trend_4G_df.columns = TNL_trend_4G_df.columns.strftime('%d-%b-%y')
        TNL_trend_4G_df = TNL_trend_4G_df.reset_index()
        
        print('9. 4G TNL TREND CREATED !')
        
############################################################ VOLTE TRAFFIC 4G TREND ####################################################################

        VOLTE_traffic_trend_4G_df = pd.pivot_table(
            main_4G_df,
            values='MV_VoLTE Traffic',
            index='SITE_CIRCLE',
            columns='Date',
            aggfunc='sum'
        )
        
        VOLTE_traffic_trend_4G_df.columns = VOLTE_traffic_trend_4G_df.columns.strftime('%d-%b-%y')
        VOLTE_traffic_trend_4G_df = VOLTE_traffic_trend_4G_df.reset_index()
        numeric_cols = VOLTE_traffic_trend_4G_df.columns.drop('SITE_CIRCLE')
        VOLTE_traffic_trend_4G_df[numeric_cols] = VOLTE_traffic_trend_4G_df[numeric_cols].mask(
            VOLTE_traffic_trend_4G_df[numeric_cols] < 0, '-'
        )
        
        print('10. 4G VOLTE TRAFFIC TREND CREATED !')
        
############################################################## THPT FLAG 4G TREND ######################################################################

        # THPT_flag_trend_4G_df = pd.pivot_table(
        #     main_4G_df,
        #     values='<3MBPS THPT FLAG',
        #     index='SITE_CIRCLE',
        #     columns='Date',
        #     aggfunc='sum'
        # )
        
        # THPT_flag_trend_4G_df.columns = THPT_flag_trend_4G_df.columns.strftime('%d-%b-%y')
        # THPT_flag_trend_4G_df = THPT_flag_trend_4G_df.reset_index()
        
        # print('11. 4G THPT FLAG TREND CREATED !')
        
#########################################################################################################################################################
############################################################### HOURLY FILE ##############################################################################
##########################################################################################################################################################

################################################### 4G HOURLY SITEID, CIRCLE2, SITE_CIRCLE ##############################################################

        hourly_4G_df.rename(columns={"Unnamed: 2": "DateTime"}, inplace=True)
        hourly_4G_df['Short name'] = hourly_4G_df['Short name'].fillna(method="ffill")
        
        hourly_4G_df = hourly_4G_df[
            (~hourly_4G_df['Short name'].str.contains("_ES_")) &
            (~hourly_4G_df['Short name'].str.contains("_IS_")) &
            (~hourly_4G_df['Short name'].str.contains("_OS_"))
        ]
        
        HS_hourly_4G_df = hourly_4G_df[
            (hourly_4G_df['Short name'].str.contains("_HS_")) &
            (hourly_4G_df['Circle'].isin(['AS', 'MU', 'NE','']))
        ]
        
        hourly_4G_df = hourly_4G_df[~hourly_4G_df['Short name'].str.contains("_HS_")]
        
        hourly_4G_df = pd.concat([hourly_4G_df, HS_hourly_4G_df])
        
        hourly_4G_df = pd.merge(hourly_4G_df, reference_4G_df, on='Short name', how='left')
        
        hourly_4G_df['DateTime'] = pd.to_datetime(hourly_4G_df['DateTime'], dayfirst=True, errors='coerce')

        hourly_4G_df['MV_4G Data Volume_GB'] = hourly_4G_df['MV_4G Data Volume_GB'].fillna(-0.000001)
        
        print('12. 4G HOURLY DATA CLEANED AND, SITE AND CIRCLE DONE !')
        
########################################################## 4G HOURLY PAYLOAD TREND ###############################################################################
        
        payload_hourly_trend_4G_df = pd.pivot_table(
            hourly_4G_df,
            values='MV_4G Data Volume_GB',
            index='SITE_CIRCLE',
            columns='DateTime',
            aggfunc='sum'
        )
        payload_hourly_trend_4G_df.columns = payload_hourly_trend_4G_df.columns.strftime('%d-%b-%y , %H-%M')
        payload_hourly_trend_4G_df = payload_hourly_trend_4G_df.reset_index()
        numeric_cols = payload_hourly_trend_4G_df.columns.drop('SITE_CIRCLE')
        payload_hourly_trend_4G_df[numeric_cols] = payload_hourly_trend_4G_df[numeric_cols].mask(
            payload_hourly_trend_4G_df[numeric_cols] < 0, '-'
        )
        
        print('13. HOURLY PAYLOAD TREND CREATED !')
        
########################################################## 4G HOURLY RNA TREND ###############################################################################
        
        RNA_hourly_trend_4G_df = pd.pivot_table(
            hourly_4G_df,
            values='MV_Radio NW Availability',
            index='SITE_CIRCLE',
            columns='DateTime',
            aggfunc='mean'
        )
        
        RNA_hourly_trend_4G_df.columns = RNA_hourly_trend_4G_df.columns.strftime('%d-%b-%y , %H-%M')
        all_site_circles = hourly_4G_df['SITE_CIRCLE'].unique()
        RNA_hourly_trend_4G_df = RNA_hourly_trend_4G_df.reindex(all_site_circles)
        RNA_hourly_trend_4G_df = RNA_hourly_trend_4G_df.reset_index()
        
        print('14. HOURLY RNA TREND CREATED !')
        
###########################################################################################################################################################################
################################################################### RELOCATION FILE #####################################################################################
################################################################################################################################################################################        
    
        today = pd.Timestamp.today().normalize()
        
################################## REPLACING UNNAMED INDEXES WITH EMPTY STRINGS AND TIMESTAMP WITH DATE STRING ##################################################

        relocation_df_total.columns = pd.MultiIndex.from_tuples(
            tuple(
                (
                    lvl.strftime("%d-%b-%y") if hasattr(lvl, "strftime")
                    else ("" if isinstance(lvl, str) and lvl.startswith("Unnamed") else lvl)
                )
                for lvl in col
            )
            for col in relocation_df_total.columns
        )
        
        print('15. MULTIINDEX DF CREATED AND COLUMNS RENAMED !')
        
############################################# SEPERATING OLD SITES AND NEW SITES AND FILLING NEW SITE DATA ##############################################################################

        relocation_df_new_sites = relocation_df_total.loc[relocation_df_total[('AGEING','')].squeeze().isna()]
        relocation_df_old_sites = relocation_df_total.loc[relocation_df_total[('AGEING','')].squeeze().notna()]
        
        # FILLING NEW SITE DATA
        
        if not relocation_df_new_sites.empty:
        
            # FILLING AOP
            relocation_df_new_sites[('AOP','')] = relocation_df_new_sites[('AOP','')].fillna('New AOP')

            # FILLING PRE PAYLOAD DATA 4G AND 5G NEW SITES` `
            days = ['D-1', 'D-2', 'D-3', 'D-4', 'D-5']
            relocation_df_new_sites[('On Air DATE','')] = pd.to_datetime(
                relocation_df_new_sites[('On Air DATE','')].squeeze(), errors='coerce'
            )

            onAirDates = relocation_df_new_sites[('On Air DATE','')].dropna().squeeze().unique()
            
            for onAirDate in onAirDates:
                first_date_data_available = pd.to_datetime(payload_trend_5G_df.columns[1])
                two_weeks_ago = onAirDate - pd.Timedelta(days=14)
                one_week_ago = onAirDate - pd.Timedelta(days=7)
                start_date_two_weeks_ago = two_weeks_ago - pd.Timedelta(days=two_weeks_ago.weekday())
                start_date_one_week_ago = one_week_ago - pd.Timedelta(days=one_week_ago.weekday())

                if(first_date_data_available > start_date_two_weeks_ago):
                    week_dates_str = [(start_date_one_week_ago + pd.Timedelta(days=i)).strftime('%d-%b-%y') for i in range(5)]  
                else:
                    week_dates_str = [(start_date_two_weeks_ago + pd.Timedelta(days=i)).strftime('%d-%b-%y') for i in range(5)]
                
                print(week_dates_str)

                for i, day in enumerate(days):
                    date_str = week_dates_str[i]
                    
                    if date_str in payload_trend_5G_df.columns:
                        trend_series_5G = payload_trend_5G_df.set_index('SITE_CIRCLE')[date_str]
                    else:
                        trend_series_5G = {}

                    # 5G
                    # trend_series_5G = payload_trend_5G_df.set_index('SITE_CIRCLE')[date_str]
                    relocation_df_new_sites.loc[
                        relocation_df_new_sites[('On Air DATE','')].squeeze() == onAirDate, (day, '5G')
                    ] = relocation_df_new_sites.loc[
                        relocation_df_new_sites[('On Air DATE','')].squeeze() == onAirDate, ('Unique_SiteID_Old','')
                    ].map(lambda site_id: trend_series_5G.get(site_id, '-'))


                    if date_str in payload_trend_4G_df.columns:
                        trend_series_4G = payload_trend_4G_df.set_index('SITE_CIRCLE')[date_str]
                    else:
                        trend_series_4G = {}
                    # 4G
                    # trend_series_4G = payload_trend_4G_df.set_index('SITE_CIRCLE')[date_str]
                    relocation_df_new_sites.loc[
                        relocation_df_new_sites[('On Air DATE','')].squeeze() == onAirDate, (day, '4G')
                    ] = relocation_df_new_sites.loc[
                        relocation_df_new_sites[('On Air DATE','')].squeeze() == onAirDate, ('Unique_SiteID_Old','')
                    ].map(lambda site_id: trend_series_4G.get(site_id, '-'))

            # FILLING PRE AVG PL OF NEW SITES
                # 5G
            relocation_df_new_sites[('Pre Avg PL', '5G')] = (
                relocation_df_new_sites.loc[:, pd.IndexSlice[days, '5G']]
                .replace(['-'], pd.NA)
                .mean(axis=1, skipna=True)
            )
            
                # 4G
            relocation_df_new_sites[('Pre Avg PL', '4G')] = (
                relocation_df_new_sites.loc[:, pd.IndexSlice[days, '4G']]
                .replace(['-'], pd.NA)
                .mean(axis=1, skipna=True)
            )
            
                # 4G + 5G
            relocation_df_new_sites[('Pre Avg PL', '4G+5G')] = relocation_df_new_sites[
                [('Pre Avg PL', '4G'), ('Pre Avg PL', '5G')]
            ].sum(axis=1, skipna=True)
        
            relocation_df_new_sites[('Pre Avg PL', '4G')] = relocation_df_new_sites[('Pre Avg PL', '4G')].fillna('-')
            relocation_df_new_sites[('Pre Avg PL', '5G')] = relocation_df_new_sites[('Pre Avg PL', '5G')].fillna('-')
            relocation_df_new_sites[('Pre Avg PL', '4G+5G')] = relocation_df_new_sites[('Pre Avg PL', '4G+5G')].fillna(0)
            
        # MERGING OLD AND NEW SITES

        relocation_df_final = pd.concat([relocation_df_old_sites, relocation_df_new_sites])
        
        print('16. NEW SITE DATA FILLED !')
        
        # CREATING TEMPLATE DF
        template_df = pd.DataFrame(columns=relocation_df_final.columns)

            # 5G POST PAYLOAD NEW DATES
        index = template_df.columns.get_loc(('Pre Avg PL', '4G'))
        if isinstance(index, slice):
            index = index.start

        last_date_post_payload_data_5G_logged = template_df.columns[index-1][0]
        
        last_date_post_payload_data_5G_logged = pd.to_datetime(last_date_post_payload_data_5G_logged, format="%d-%b-%y")
        
        dates_post_payload_data_5G_available = pd.to_datetime(payload_trend_5G_df.columns[1:], format="%d-%b-%y")
        
        dates_post_payload_data_5G_to_be_logged = dates_post_payload_data_5G_available[
            dates_post_payload_data_5G_available > last_date_post_payload_data_5G_logged
        ]
        
        dates_post_payload_data_5G_to_be_logged = dates_post_payload_data_5G_to_be_logged.strftime("%d-%b-%y").tolist()
        
        for date in dates_post_payload_data_5G_to_be_logged:
            template_df[(date, '5G')] = np.nan  
            
            cols = template_df.columns.to_list()
            cols.insert(index, cols.pop(cols.index((date, '5G'))))
            template_df = template_df[cols]

            index += 1
        
            # 4G POST PAYLOAD NEW DATES
        index = template_df.columns.get_loc(('19-May-25', '5G'))
        if isinstance(index, slice):
            index = index.start

        last_date_post_payload_data_4G_logged = template_df.columns[index-1][0]
        
        last_date_post_payload_data_4G_logged = pd.to_datetime(last_date_post_payload_data_4G_logged, format="%d-%b-%y")
        
        dates_post_payload_data_4G_available = pd.to_datetime(payload_trend_4G_df.columns[1:], format="%d-%b-%y")
        
        dates_post_payload_data_4G_to_be_logged = dates_post_payload_data_4G_available[
            dates_post_payload_data_4G_available > last_date_post_payload_data_4G_logged
        ]
        
        dates_post_payload_data_4G_to_be_logged = dates_post_payload_data_4G_to_be_logged.strftime("%d-%b-%y").tolist()
        
        for date in dates_post_payload_data_4G_to_be_logged:
            template_df[(date, '4G')] = np.nan
            
            cols = template_df.columns.to_list()
            cols.insert(index, cols.pop(cols.index((date, '4G'))))
            template_df = template_df[cols]

            index += 1

        print('17. TEMPLATE DF CREATED !')

        # FILLING POST PAYLOAD DATA ALL SITES NEW DATES
            # 5G
        for date in dates_post_payload_data_5G_to_be_logged:
            trend_series = payload_trend_5G_df.set_index('SITE_CIRCLE')[date]
            relocation_df_final = relocation_df_final.drop((date,'5G'), axis=1, errors='ignore')
            relocation_df_final[(date, '5G')] = relocation_df_final[('Unique_SiteID_New','')].map(
                lambda site_id: trend_series.get(site_id, '-')
            )
            
            # 4G
        for date in dates_post_payload_data_4G_to_be_logged:
            trend_series = payload_trend_4G_df.set_index('SITE_CIRCLE')[date]
            relocation_df_final = relocation_df_final.drop((date,'4G'), axis=1, errors='ignore')
            relocation_df_final[(date, '4G')] = relocation_df_final[('Unique_SiteID_New','')].map(
                lambda site_id: trend_series.get(site_id, '-')
            )
            
        print('18. POST DATA NEW DATES FILLED !')
        
        # FILLING POST PAYLOAD DATA OF SITES JUST STARTED GETTING TRAFFIC
        
            # 5G
        date_post_payload_data_5G_just_logged = dates_post_payload_data_5G_to_be_logged[-1]
        date_post_payload_data_5G_already_logged = last_date_post_payload_data_5G_logged.strftime("%d-%b-%y")
        
        sites_just_started_df = relocation_df_final.loc[(relocation_df_final[(date_post_payload_data_5G_already_logged,'5G')].squeeze()=='-') & (relocation_df_final[(date_post_payload_data_5G_just_logged,'5G')].squeeze()!='-'),:]

        relocation_df_final = relocation_df_final.drop(sites_just_started_df.index)
        
        dates_post_payload_data_5G_available = list(payload_trend_5G_df.columns[1:])
        
        for date in dates_post_payload_data_5G_available:
            trend_series = payload_trend_5G_df.set_index('SITE_CIRCLE')[date]
            sites_just_started_df = sites_just_started_df.drop((date,'5G'), axis=1, errors='ignore')
            sites_just_started_df[(date, '5G')] = sites_just_started_df[('Unique_SiteID_New','')].map(
                lambda site_id: trend_series.get(site_id, '-')
            )
        
            # MERGING THIS DF TO FINAL ONE
        relocation_df_final = pd.concat([relocation_df_final, sites_just_started_df])
        
        print('19. 5G POST DATA OLD DATES REFRESHED !')
        
            # 4G
        date_post_payload_data_4G_just_logged = dates_post_payload_data_4G_to_be_logged[-1]
        date_post_payload_data_4G_already_logged = last_date_post_payload_data_4G_logged.strftime("%d-%b-%y")
        
        sites_just_started_df = relocation_df_final.loc[(relocation_df_final[(date_post_payload_data_4G_already_logged,'4G')]=='-') & (relocation_df_final[(date_post_payload_data_4G_just_logged,'4G')]!='-'),:]
        
        relocation_df_final = relocation_df_final.drop(sites_just_started_df.index)
        
        dates_post_payload_data_4G_available = list(payload_trend_4G_df.columns[1:])
        
        for date in dates_post_payload_data_4G_available:
            trend_series = payload_trend_4G_df.set_index('SITE_CIRCLE')[date]
            sites_just_started_df = sites_just_started_df.drop((date,'5G'), axis=1, errors='ignore')
            sites_just_started_df[(date, '5G')] = sites_just_started_df[('Unique_SiteID_New','')].map(
                lambda site_id: trend_series.get(site_id, '-')
            )
        
            # MERGING THIS DF TO FINAL ONE
        relocation_df_final = pd.concat([relocation_df_final, sites_just_started_df])
        
        print('20. 4G POST DATA OLD DATES REFRESHED !')
        
        # FILLING RNA
            # 5G POST
        date_RNA_5G = list(RNA_trend_5G_df.columns)[-1]
        trend_series = RNA_trend_5G_df.set_index('SITE_CIRCLE')[date_RNA_5G]
        relocation_df_final = relocation_df_final.drop(('New Site Current RNA 5G','X'), axis=1, errors='ignore')
        relocation_df_final[('New Site Current RNA 5G', 'X')] = relocation_df_final[('Unique_SiteID_New','')].map(
            lambda site_id: trend_series.get(site_id, '-')
        )
        
        print('21. 5G POST SITEID RNA FILLED !')
        
            # 5G PRE
        relocation_df_final = relocation_df_final.drop(('Old Site Current RNA 5G','X'), axis=1, errors='ignore')
        relocation_df_final[('Old Site Current RNA 5G', 'X')] = relocation_df_final[('Unique_SiteID_Old','')].map(
            lambda site_id: trend_series.get(site_id, '-')
        )
        
        print('22. 5G PRE SITEID RNA FILLED !')
        
            # 4G POST
        date_RNA_4G = list(RNA_trend_4G_df.columns)[-1]
        trend_series = RNA_trend_4G_df.set_index('SITE_CIRCLE')[date_RNA_4G]
        relocation_df_final = relocation_df_final.drop(('New Site Current RNA 4G','X'), axis=1, errors='ignore')
        relocation_df_final[('New Site Current RNA 4G', 'X')] = relocation_df_final[('Unique_SiteID_New','')].map(
            lambda site_id: trend_series.get(site_id, '-')
        )
        
        print('23. 4G POST SITEID RNA FILLED !')
        
            # 4G PRE
        relocation_df_final = relocation_df_final.drop(('Old Site Current RNA','X'), axis=1, errors='ignore')
        relocation_df_final[('Old Site Current RNA', 'X')] = relocation_df_final[('Unique_SiteID_Old','')].map(
            lambda site_id: trend_series.get(site_id, '-')
        )
        
        print('24. 4G PRE SITEID RNA FILLED !')
        
        # FILLING TNL 4G
        
        date_TNL_4G = list(TNL_trend_4G_df.columns)[-1]
        trend_series = TNL_trend_4G_df.set_index('SITE_CIRCLE')[date_TNL_4G]
        relocation_df_final = relocation_df_final.drop(('TNL-TRU Fails','X'), axis=1, errors='ignore')
        relocation_df_final[('TNL-TRU Fails', 'X')] = relocation_df_final[('Unique_SiteID_New','')].map(
            lambda site_id: trend_series.get(site_id, '-')
        )
        
        print('25. 4G TNL FILLED !')
        
        # FILLING PRE PAYLOAD
            # 5G
        date_pre_payload_5G = list(payload_trend_5G_df.columns)[-1]
        trend_series = payload_trend_5G_df.set_index('SITE_CIRCLE')[date_pre_payload_5G]
        relocation_df_final = relocation_df_final.drop(('Old Site Current Payload 5G','X'), axis=1, errors='ignore')
        relocation_df_final[('Old Site Current Payload 5G', 'X')] = relocation_df_final[('Unique_SiteID_Old','')].map(
            lambda site_id: trend_series.get(site_id, '-')
        )
        
        print('26. 5G PRE SITEID CURRENT PAYLOAD FILLED !')
        
            # 4G
        date_pre_payload_4G = list(payload_trend_4G_df.columns)[-1]
        trend_series = payload_trend_4G_df.set_index('SITE_CIRCLE')[date_pre_payload_4G]
        relocation_df_final = relocation_df_final.drop(('Old Site Current Payload 4G','X'), axis=1, errors='ignore')
        relocation_df_final[('Old Site Current Payload 4G', 'X')] = relocation_df_final[('Unique_SiteID_Old','')].map(
            lambda site_id: trend_series.get(site_id, '-')
        )
        
        print('27. 4G PRE SITEID CURRENT PAYLOAD FILLED !')
        
        # REARRANGING COLUMNS
        relocation_df_final = pd.concat([template_df, relocation_df_final])
        
        print('28. CONCAT WITH TEMPLATE DF DONE !')
        
        # FILLING POST - PRE PAYLOAD D-1
        index1 = relocation_df_final.columns.get_loc(('Pre Avg PL', '4G'))
        index2 = relocation_df_final.columns.get_loc(('19-May-25', '5G'))
        if isinstance(index1, slice):
            index1 = index1.start
        if isinstance(index2, slice):
            index2 = index2.start
        
        col1 = pd.to_numeric(relocation_df_final.iloc[:, index1-1], errors='coerce')
        col2 = pd.to_numeric(relocation_df_final.iloc[:, index2-1], errors='coerce')
        pre  = pd.to_numeric(relocation_df_final[('Pre Avg PL', '4G+5G')], errors='coerce')

        delta = col1.fillna(0) + col2.fillna(0) - pre.fillna(0)

        pct = pd.Series(np.where(pre == 0, np.nan, delta*100 / pre), index=relocation_df_final.index)

        relocation_df_final[('Pre-Post delta% D-1','')] = pct.fillna('-')
        
        relocation_df_final[('Post -Pre delta D-1','')] = delta.where(~delta.isna(), '-')
        
        print("29. POST - PRE D-1 FILLED !")
        
        # FILLING PAYLOAD DIP DATE AND AGEING1
        relocation_df_final[('Traffic payload dip date','')] = relocation_df_final[('Traffic payload dip date','')].fillna('')

        relocation_df_final[('AGEING1','')] = relocation_df_final[('AGEING1','')].fillna(0)

        def update_row(row):
            if row[('Pre-Post delta% D-1','')]!='-' and row[('Pre-Post delta% D-1','')] <= -10:
                if row[('Traffic payload dip date','')] == "":
                    row[('Traffic payload dip date','')] = today.strftime("%d-%b-%y")
                    row[('AGEING1','')] = 1
                else:
                    dip_date = pd.to_datetime(row[('Traffic payload dip date','')], format="%d-%b-%y", errors="coerce")
                    row[('AGEING1','')] = (today - dip_date).days
            else:
                row[('Traffic payload dip date','')] = ""
                row[('AGEING1','')] = 0
            return row

        relocation_df_final = relocation_df_final.apply(update_row, axis=1)
        
        print('30. TRAFFIC DIP DATE AND AGEING FILLED !')
        
        # CALCULATING AGEING
        relocation_df_final[('On Air DATE', '')] = pd.to_datetime(
            relocation_df_final[('On Air DATE', '')].squeeze(), errors="coerce"
        )
        relocation_df_final[("AGEING", "")] = (
            today - relocation_df_final[("On Air DATE", "")].squeeze()
        ).dt.days
        
        # FILLING AGEING CATEGORY
        relocation_df_final[("AGEING CATEGORY", "")] = relocation_df_final[("AGEING", "")].apply(
            lambda x: "0 To 12 Days" if x <= 12 else "13 To 21 Days" if x <= 21 else "GT 21 Days"
        )
        
        print('31. AGEING ANG AGEING CATEGORY FILLED !')
        
        # FILLING POST AVG PL
        index_5G = relocation_df_final.columns.get_loc(('Pre Avg PL', '4G'))
        index_4G = relocation_df_final.columns.get_loc(('19-May-25', '5G'))
        
        if isinstance(index_4G, slice):
            index_4G = index_4G.start
        if isinstance(index_5G, slice):
            index_5G = index_5G.start
            
        candidate_idx_5G = list(range(index_5G-7, index_5G))
        candidate_idx_4G = list(range(index_4G-7, index_4G))

        dates = pd.to_datetime(
            relocation_df_final.columns.get_level_values(0)[candidate_idx_5G],
            errors='coerce'
        )

        weekday_idx_5G = [
            candidate_idx_5G[i] for i, d in enumerate(dates)
            if pd.notna(d) and d.weekday() < 5
        ]
        
        weekday_idx_4G = [
            candidate_idx_4G[i] for i, d in enumerate(dates)
            if pd.notna(d) and d.weekday() < 5
        ]
        
        relocation_df_final[('Post Avg PL', '5G')] = (
            relocation_df_final.iloc[:, weekday_idx_5G]
            .replace(['-'], pd.NA)                          
            .mean(axis=1, skipna=True)                      
        )
        
        relocation_df_final[('Post Avg PL', '4G')] = (
            relocation_df_final.iloc[:, weekday_idx_4G]  
            .replace(['-'], pd.NA)                       
            .mean(axis=1, skipna=True)                     
        )
        
        relocation_df_final[('Post Avg PL', '4G+5G')] = relocation_df_final[
            [('Post Avg PL', '4G'), ('Post Avg PL', '5G')]
        ].sum(axis=1, skipna=True)
        
        relocation_df_final[('Post Avg PL', '4G')] = relocation_df_final[('Post Avg PL', '4G')].fillna('-')
        relocation_df_final[('Post Avg PL', '5G')] = relocation_df_final[('Post Avg PL', '5G')].fillna('-')
        relocation_df_final[('Post Avg PL', '4G+5G')] = relocation_df_final[('Post Avg PL', '4G+5G')].fillna(0)
        
        print('32. POST AVG PL FILLED !')
        
        # FILLING POST - PRE PAYLOAD
        pre  = pd.to_numeric(relocation_df_final[('Pre Avg PL', '4G+5G')], errors='coerce')
        post = pd.to_numeric(relocation_df_final[('Post Avg PL', '4G+5G')], errors='coerce')
        
        delta = post.fillna(0) - pre.fillna(0)
        
        pct = pd.Series(np.where(pre == 0, np.nan, delta*100 / pre), index=relocation_df_final.index)

        relocation_df_final[('Pre-Post delta%','')] = pct.fillna('-')
        
        relocation_df_final[('Post -Pre delta','')] = delta.where(~delta.isna(), '-')
        
        print('33. POST - PRE FILLED !')
        
############################################################# FILLING HOURLY DATA ############################################################################
        
        last_4_datetime_hourly_RNA = list(RNA_hourly_trend_4G_df.columns[-4:])
        last_4_datetime_hourly_payload = list(payload_hourly_trend_4G_df.columns[-4:])
        cols = ['A','B','C','D']
        
        for i in range(4):
            datetime = last_4_datetime_hourly_RNA[i]
            trend_series = RNA_hourly_trend_4G_df.set_index('SITE_CIRCLE')[datetime]
            relocation_df_final = relocation_df_final.drop(('New RNA',cols[i]), axis=1, errors='ignore')
            relocation_df_final[('New RNA', cols[i])] = relocation_df_final[('Unique_SiteID_New','')].map(
                lambda site_id: trend_series.get(site_id, '-')
            )
        
        for i in range(4):
            datetime = last_4_datetime_hourly_payload[i]
            trend_series = payload_hourly_trend_4G_df.set_index('SITE_CIRCLE')[datetime]
            relocation_df_final = relocation_df_final.drop(('New Payload',cols[i]), axis=1, errors='ignore')
            relocation_df_final[('New Payload', cols[i])] = relocation_df_final[('Unique_SiteID_New','')].map(
                lambda site_id: trend_series.get(site_id, '-')
            )
            
        for i in range(4):
            datetime = last_4_datetime_hourly_RNA[i]
            trend_series = RNA_hourly_trend_4G_df.set_index('SITE_CIRCLE')[datetime]
            relocation_df_final = relocation_df_final.drop(('Old RNA',cols[i]), axis=1, errors='ignore')
            relocation_df_final[('Old RNA', cols[i])] = relocation_df_final[('Unique_SiteID_Old','')].map(
                lambda site_id: trend_series.get(site_id, '-')
            )
        
        for i in range(4):
            datetime = last_4_datetime_hourly_payload[i]
            trend_series = payload_hourly_trend_4G_df.set_index('SITE_CIRCLE')[datetime]
            relocation_df_final = relocation_df_final.drop(('Old Payload',cols[i]), axis=1, errors='ignore')
            relocation_df_final[('Old Payload', cols[i])] = relocation_df_final[('Unique_SiteID_Old','')].map(
                lambda site_id: trend_series.get(site_id, '-')
            )
            
        print('34. HOURLY DATA FILLED !')
        
############################################################ FORMAT CHANGE FOR DISPLAY #################################################################

        main_5G_df['Date'] = main_5G_df['Date'].dt.strftime('%d-%b-%y')
        main_4G_df['Date'] = main_4G_df['Date'].dt.strftime('%d-%b-%y')
        
        hourly_4G_df['DateTime'] = hourly_4G_df['DateTime'].dt.strftime('%d-%b-%y , %H-%M')
        
        relocation_df_final[('MS2 Date','')] = pd.to_datetime(relocation_df_final[('MS2 Date','')], errors='coerce')
        relocation_df_final[('On Air DATE','')] = pd.to_datetime(relocation_df_final[('On Air DATE','')], errors='coerce')
        
        relocation_df_final = relocation_df_final.sort_values(by=('On Air DATE', ''), ascending=True)
        
        relocation_df_final[('Airtel MS1 Date','')] = pd.to_datetime(relocation_df_final[('Airtel MS1 Date','')], errors='coerce')
        relocation_df_final[('Traffic Validation Date','')] = pd.to_datetime(relocation_df_final[('Traffic Validation Date','')], errors='coerce')
        relocation_df_final[('MS2 Date','')] = relocation_df_final[('MS2 Date','')].dt.strftime('%d-%b-%y')
        relocation_df_final[('On Air DATE','')] = relocation_df_final[('On Air DATE','')].dt.strftime('%d-%b-%y')
        relocation_df_final[('Airtel MS1 Date','')] = relocation_df_final[('Airtel MS1 Date','')].dt.strftime('%d-%b-%y')
        relocation_df_final[('Traffic Validation Date','')] = relocation_df_final[('Traffic Validation Date','')].dt.strftime('%d-%b-%y')
        relocation_df_final = relocation_df_final.replace([np.inf, -np.inf], '').fillna('')
        
        print('35. FORMATTING DONE !')
        
########################################################## CREATING 4G AND 5G EXCEL FILES ###########################################################################

        current_date = dtime.now().strftime("%Y-%m-%d")
        current_time = dtime.now().strftime("%H-%M-%S")

        BASE_URL = os.path.join(settings.MEDIA_ROOT, "relocation_tracking")
        os.makedirs(BASE_URL, exist_ok=True)
        output_folder = os.path.join(BASE_URL, f"relocation_generated_files_{current_date}")
        os.makedirs(output_folder, exist_ok=True)
        
        file_path_5G = os.path.join(output_folder, f"5G_FILE_{current_date}_{current_time}.xlsx")
        file_path_4G = os.path.join(output_folder, f"4G_FILE_{current_date}_{current_time}.xlsx")
        file_path_relocation = os.path.join(output_folder, f"RELOCATION_TRACKER_FILE_{current_date}_{current_time}.xlsx")
        file_path_hourly = os.path.join(output_folder, f"4G_HOURLY_FILE_{current_date}_{current_time}.xlsx")

        with pd.ExcelWriter(file_path_5G, engine='xlsxwriter') as writer:
            main_5G_df.to_excel(writer, index=False, sheet_name='5G RELOCATION PRE POST PAYLOAD ')
            payload_trend_5G_df.to_excel(writer, index=False, sheet_name='PLD')
            RNA_trend_5G_df.to_excel(writer, index=False, sheet_name='RNA')
            
        print('36. 5G FILE CREATED !')

        with pd.ExcelWriter(file_path_4G, engine='xlsxwriter') as writer:
            main_4G_df.to_excel(writer, index=False, sheet_name='4G RELOCATION PRE POST PAYLOAD ')
            payload_trend_4G_df.to_excel(writer, index=False, sheet_name='PLD')
            RNA_trend_4G_df.to_excel(writer, index=False, sheet_name='RNA')
            TNL_trend_4G_df.to_excel(writer, index=False, sheet_name='TNL')
            VOLTE_traffic_trend_4G_df.to_excel(writer, index=False, sheet_name='VOLTE')
            # THPT_flag_trend_4G_df.to_excel(writer, index=False, sheet_name='<3 MBPS')
    
        print('37. 4G FILE CREATED !')
    
        with pd.ExcelWriter(file_path_relocation, engine='xlsxwriter') as writer:
            relocation_df_final.to_excel(writer, sheet_name='Main', index=True)

            workbook  = writer.book
            worksheet = writer.sheets['Main']
            
            # full_format = workbook.add_format({
            #     'border': 1,
            #     'align': 'center',
            #     'valign': 'center',
            #     'bg_color': '#D3D3D3'
            # })
            
            yellow_format = workbook.add_format({'bg_color': '#FFD700', 'border': 2, 'align': 'center'})
            pink_format = workbook.add_format({'bg_color': '#FFB6C1', 'border': 2, 'align': 'center'})
            lightblue_format = workbook.add_format({'bg_color': '#ADD8E6', 'border': 2, 'align': 'center'}) 
            lightgreen_format = workbook.add_format({'bg_color': '#90EE90', 'border': 2, 'align': 'center'}) 
            # Light Grey format
            lightgrey_format = workbook.add_format({
                'bg_color': '#D3D3D3',   # Light Grey
                'border': 2,
                'align': 'center'
            })

            # Light Purple format
            lightpurple_format = workbook.add_format({
                'bg_color': '#D8BFD8',   # Thistle (Light Purple)
                'border': 2,
                'align': 'center'
            })

            # Cream format
            cream_format = workbook.add_format({
                'bg_color': '#FFFDD0',   # Cream
                'border': 2,
                'align': 'center'
            })

            # Dark Blue with White Font format
            darkblue_whitefont_format = workbook.add_format({
                'bg_color': '#00008B',   # Dark Blue
                'font_color': '#FFFFFF', # White text
                'border': 2,
                'align': 'center'
            })
            
            max_row, max_col = relocation_df_final.shape
            # num_levels = relocation_df_final.columns.nlevels
            
            # for row in range(num_levels, max_row + num_levels):
            #     for col in range(max_col):
            #         worksheet.write(row, col, relocation_df_final.iloc[row - num_levels, col], full_format)
            
            worksheet.write(0, 1, relocation_df_final.columns[0][0], lightblue_format)
            worksheet.write(1, 1, relocation_df_final.columns[0][1], lightblue_format)
            worksheet.write(0, 2, relocation_df_final.columns[1][0], yellow_format)
            worksheet.write(1, 2, relocation_df_final.columns[1][1], yellow_format)
            worksheet.write(0, 3, relocation_df_final.columns[2][0], yellow_format)
            worksheet.write(1, 3, relocation_df_final.columns[2][1], yellow_format)
            worksheet.write(0, 4, relocation_df_final.columns[3][0], yellow_format)
            worksheet.write(1, 4, relocation_df_final.columns[3][1], yellow_format)
            worksheet.write(0, 5, relocation_df_final.columns[4][0], yellow_format)
            worksheet.write(1, 5, relocation_df_final.columns[4][1], yellow_format)
            worksheet.write(0, 6, relocation_df_final.columns[5][0], lightblue_format)
            worksheet.write(1, 6, relocation_df_final.columns[5][1], lightblue_format)
            worksheet.write(0, 7, relocation_df_final.columns[6][0], lightblue_format)
            worksheet.write(1, 7, relocation_df_final.columns[6][1], lightblue_format)
            worksheet.write(0, 8, relocation_df_final.columns[7][0], lightblue_format)
            worksheet.write(1, 8, relocation_df_final.columns[7][1], lightblue_format)
            worksheet.write(0, 9, relocation_df_final.columns[8][0], lightblue_format)
            worksheet.write(1, 9, relocation_df_final.columns[8][1], lightblue_format)
            worksheet.write(0, 10, relocation_df_final.columns[9][0], lightblue_format)
            worksheet.write(1, 10, relocation_df_final.columns[9][1], lightblue_format)
            worksheet.write(0, 11, relocation_df_final.columns[10][0], lightblue_format)
            worksheet.write(1, 11, relocation_df_final.columns[10][1], lightblue_format)
            worksheet.write(0, 12, relocation_df_final.columns[11][0], lightgreen_format)
            worksheet.write(1, 12, relocation_df_final.columns[11][1], lightgreen_format)
            worksheet.write(0, 13, relocation_df_final.columns[12][0], lightgreen_format)
            worksheet.write(1, 13, relocation_df_final.columns[12][1], lightgreen_format)
            worksheet.write(0, 14, relocation_df_final.columns[13][0], lightgreen_format)
            worksheet.write(1, 14, relocation_df_final.columns[13][1], lightgreen_format)
            worksheet.write(0, 15, relocation_df_final.columns[14][0], lightgreen_format)
            worksheet.write(1, 15, relocation_df_final.columns[14][1], lightgreen_format)
            worksheet.write(0, 16, relocation_df_final.columns[15][0], lightgreen_format)
            worksheet.write(1, 16, relocation_df_final.columns[15][1], lightgreen_format)
            worksheet.write(0, 17, relocation_df_final.columns[16][0], pink_format)
            worksheet.write(1, 17, relocation_df_final.columns[16][1], pink_format)
            worksheet.write(0, 18, relocation_df_final.columns[17][0], pink_format)
            worksheet.write(1, 18, relocation_df_final.columns[17][1], pink_format)
            worksheet.write(0, 19, relocation_df_final.columns[18][0], pink_format)
            worksheet.write(1, 19, relocation_df_final.columns[18][1], pink_format)
            worksheet.write(0, 20, relocation_df_final.columns[19][0], pink_format)
            worksheet.write(1, 20, relocation_df_final.columns[19][1], pink_format)
            worksheet.write(0, 21, relocation_df_final.columns[20][0], pink_format)
            worksheet.write(1, 21, relocation_df_final.columns[20][1], pink_format)
            
            index1 = relocation_df_final.columns.get_loc(('19-May-25', '4G'))
            index2 = relocation_df_final.columns.get_loc(('19-May-25', '5G'))

            for idx in range(index1,index2):
                worksheet.write(0, idx+1, relocation_df_final.columns[idx][0], lightblue_format)
                worksheet.write(1, idx+1, relocation_df_final.columns[idx][1], lightblue_format)
            
            index1 = relocation_df_final.columns.get_loc(('19-May-25', '5G'))
            index2 = relocation_df_final.columns.get_loc(('Pre Avg PL', '4G'))

            for idx in range(index1,index2):
                worksheet.write(0, idx+1, relocation_df_final.columns[idx][0], pink_format)
                worksheet.write(1, idx+1, relocation_df_final.columns[idx][1], pink_format)
            
            for idx in range(index2,index2+3):
                worksheet.write(0, idx+1, relocation_df_final.columns[idx][0], lightgreen_format)
                worksheet.write(1, idx+1, relocation_df_final.columns[idx][1], lightgreen_format)
            
            for idx in range(index2+3,index2+6):
                worksheet.write(0, idx+1, relocation_df_final.columns[idx][0], lightblue_format)
                worksheet.write(1, idx+1, relocation_df_final.columns[idx][1], lightblue_format)
            
            for idx in range(index2+6,index2+13):
                worksheet.write(0, idx+1, relocation_df_final.columns[idx][0], yellow_format)
                worksheet.write(1, idx+1, relocation_df_final.columns[idx][1], yellow_format)
                
            for idx in range(index2+13,index2+19):
                worksheet.write(0, idx+1, relocation_df_final.columns[idx][0], pink_format)
                worksheet.write(1, idx+1, relocation_df_final.columns[idx][1], pink_format)
                
            for idx in range(index2+19,max_col):
                worksheet.write(0, idx+1, relocation_df_final.columns[idx][0], lightblue_format)
                worksheet.write(1, idx+1, relocation_df_final.columns[idx][1], lightblue_format)
                
            idx = relocation_df_final.columns.get_loc(("AOP1",""))+1
            worksheet.write(0, idx, relocation_df_final.columns[idx-1][0], lightgrey_format)
            worksheet.write(1, idx, relocation_df_final.columns[idx-1][1], lightgrey_format)
            
            idx = relocation_df_final.columns.get_loc(("Cluster Pre Payload",""))+1
            worksheet.write(0, idx, relocation_df_final.columns[idx-1][0], lightpurple_format)
            worksheet.write(1, idx, relocation_df_final.columns[idx-1][1], lightpurple_format)
            worksheet.write(0, idx+1, relocation_df_final.columns[idx][0], lightpurple_format)
            worksheet.write(1, idx+1, relocation_df_final.columns[idx][1], lightpurple_format)
            worksheet.write(0, idx+2, relocation_df_final.columns[idx+1][0], lightpurple_format)
            worksheet.write(1, idx+2, relocation_df_final.columns[idx+1][1], lightpurple_format)
            
            idx = relocation_df_final.columns.get_loc(("MS-1 Month",""))+1
            worksheet.write(0, idx, relocation_df_final.columns[idx-1][0], cream_format)
            worksheet.write(1, idx, relocation_df_final.columns[idx-1][1], cream_format)
            
            idx = relocation_df_final.columns.get_loc(("TAT",""))+1
            for idx in range(idx, idx+4):
                worksheet.write(0, idx, relocation_df_final.columns[idx-1][0], darkblue_whitefont_format)
                worksheet.write(1, idx, relocation_df_final.columns[idx-1][1], darkblue_whitefont_format)
            

            payload_trend_4G_df.to_excel(writer, index=False, sheet_name='4G PLD')
            RNA_trend_4G_df.to_excel(writer, index=False, sheet_name='4G RNA')
            TNL_trend_4G_df.to_excel(writer, index=False, sheet_name='4G TNL')
            VOLTE_traffic_trend_4G_df.to_excel(writer, index=False, sheet_name='4G VOLTE TRAFFIC')
            # THPT_flag_trend_4G_df.to_excel(writer, index=False, sheet_name='4G THPT FLAG')
            payload_trend_5G_df.to_excel(writer, index=False, sheet_name='5G PLD')
            RNA_trend_5G_df.to_excel(writer, index=False, sheet_name='5G RNA')
            
        print('38. RELOCATION FILE CREATED !')
        
        with pd.ExcelWriter(file_path_hourly, engine='xlsxwriter') as writer:
            hourly_4G_df.to_excel(writer, index=False, sheet_name='4G RELOCATION HRLY PRE POST PAY')
            payload_hourly_trend_4G_df.to_excel(writer, index=False, sheet_name='PLD')
            RNA_hourly_trend_4G_df.to_excel(writer, index=False, sheet_name='RNA')
            
        print('39. HOURLY FILE CREATED !')
        
        file_path_5G = file_path_5G.replace(settings.MEDIA_ROOT, settings.MEDIA_URL).replace("\\", "/")
        download_link1 = request.build_absolute_uri(file_path_5G)
        file_path_4G = file_path_4G.replace(settings.MEDIA_ROOT, settings.MEDIA_URL).replace("\\", "/")
        download_link2 = request.build_absolute_uri(file_path_4G)
        file_path_relocation = file_path_relocation.replace(settings.MEDIA_ROOT, settings.MEDIA_URL).replace("\\", "/")
        download_link3 = request.build_absolute_uri(file_path_relocation)
        file_path_hourly = file_path_hourly.replace(settings.MEDIA_ROOT, settings.MEDIA_URL).replace("\\", "/")
        download_link4 = request.build_absolute_uri(file_path_hourly)
        
        download_object = {
            f"5G_FILE" : download_link1,
            f"4G_FILE" : download_link2,
            f"RELOCATION_TRACKER_FILE" : download_link3,
            f"4G_HOURLY_FILE" : download_link4,
        }
        
#################################################################### RESPONSE ##########################################################################

        return Response(
            {
            "status": True,
            "message": "Files saved successfully !!!",
            "download_url_object": download_object,
            },
            status=200,
        )  
    except Exception as e:
        return Response({"error": f"{str(e)}"},status=500)






