from django.shortcuts import render
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from mcom_website.settings import MEDIA_ROOT,MEDIA_URL
# Create your views here.
@api_view(["POST"])
def Degrow_trend(request):
    pre_file = request.FILES["pre_file"] if 'pre_file' in request.FILES else None
    post_file = request.FILES["post_file"] if 'post_file' in request.FILES else None
    additional_inputs = request.FILES["additional_inputs"] if 'additional_inputs' in request.FILES else None


    pre_df =pd.read_excel(pre_file, sheet_name='Sheet1')
    pre_df.fillna(value=0,inplace=True)
    pre_df.rename(columns={"Short name":"Cell ID","MV Freq_Band":"BAND"},inplace=True)
    pre_df.columns

    sam_sector={
    11:"A",
    15:"A",
    21:"A",
    25:"A",
    41:"A",
    45:"A",
    31:"A",
    12:"B",
    16:"B",
    22:"B",
    26:"B",
    42:"B",
    46:"B",
    32:"B",
    13:"C",
    17:"C",
    23:"C",
    27:"C",
    43:"C",
    47:"C",
    33:"C",
    14:"D",
    18:"D",    
    24:"D",
    28:"D",
    34:"D",
    44:"D",
    48:"D",
    19:"E",
    29:"E",
    35:"E",
    49:"E",
    20:"F",
    30:"F",
    36:"F",

    }

    def extract_sector(shortname):
        if "," not in shortname:
            if shortname.split("_")[-1] == "TDD" or shortname.split("_")[-1] =="FDD":
                sector = shortname.split("_")[-3][-1]
            else:
                sector = shortname.split("_")[-2][-1]
        else:
            sector = sam_sector[int(shortname.split(",")[-1][4:])]
        return sector
    def extract_site(MVSiteName):
        if "_" in str(MVSiteName):
            sitename=MVSiteName.split("_")[-1]
        else:
            sitename=MVSiteName
        return sitename
        
    pre_df["T_sector"] =pre_df["Cell ID"].apply(extract_sector)
    pre_df["Site ID"] =pre_df["MV Site Name"].apply(extract_site)
    pd.set_option('display.max_rows', None)


    post_df =pd.read_excel(post_file, sheet_name='Sheet1')
    post_df.fillna(value=0,inplace=True)
    post_df.rename(columns={"Short name":"Cell ID","MV Freq_Band":"BAND"},inplace=True)
    post_df



    def extract_sector(shortname):
        if "," not in shortname:
            if shortname.split("_")[-1] == "TDD" or shortname.split("_")[-1] =="FDD":
                sector = shortname.split("_")[-3][-1]
            else:
                sector = shortname.split("_")[-2][-1]
        else:
            sector = sam_sector[int(shortname.split(",")[-1][4:])]
        return sector
    def extract_site(MVSiteName):
        if "_" in str(MVSiteName):
            sitename=MVSiteName.split("_")[-1]
        else:
            sitename=MVSiteName
        return sitename
        
    post_df["T_sector"] =post_df["Cell ID"].apply(extract_sector)
    post_df["Site ID"] =post_df["MV Site Name"].apply(extract_site)
    pd.set_option('display.max_rows', None)


    additional_input=pd.read_excel(additional_inputs)
    additional_input

    values=[
        'MV_Radio NW Availability', 'MV_4G Data Volume_GB',
        'MV_RRC Setup Success Rate', 'MV_VoLTE ERAB Setup Success Rate',
        'MV_DL User Throughput_Kbps', 'MV_UL User Throughput_Kbps',
        'MV_Average number of used DL PRBs', 'MV_E-UTRAN Average CQI',
        'TA Sample <1KM', 'MV_VoLTE Traffic', 'MV_VoLTE DCR']


    mapping_dict = {
        "MV_Radio NW Availability": "Radio NW Availability",
        "MV_4G Data Volume_GB": "Payload",
        "MV_RRC Setup Success Rate": "RRC Setup Success Rate",
        "MV_VoLTE ERAB Setup Success Rate": "ERAB Setup Success Rate",
        "MV_DL User Throughput_Kbps": "DL User Throughput_Kbps",
        "MV_UL User Throughput_Kbps": "UL User Throughput_Kbps",
        "MV_Average number of used DL PRBs": "Average number of used DL PRBs",
        "MV_E-UTRAN Average CQI": "E-UTRAN Average CQI",
        "TA Sample <1KM": "Average of TA Sample <2KM",
        "MV_VoLTE Traffic": "VoLTE Traffic",
        "MV_VoLTE DCR": "VOLTE DCR"
    }
    ########### for post ############
    unique_dates=list(post_df["Date"].unique())
    unique_dates.sort()
    post_required_5_dates = unique_dates[-5:]
    final_op=pd.DataFrame()
    missing_sites=[]
    post_required_5_dates
    for i,raw in additional_input.iterrows():
        print("site ID: ",raw["Site_ID"])
        # single_pre_df=pre_df[pre_df["Site ID"]==raw["Site_ID"]]
        unique_dates=list(set(pre_df[(pre_df["Date"]<raw["Dismantled date"]) & (pre_df["Site ID"]==raw["Site_ID"])]["Date"]))
        unique_dates.sort()
        pre_required_5_dates = unique_dates[-5:]
        print("pre_dates:",pre_required_5_dates)
        
        single_site_pre_df =pre_df[(pre_df["Site ID"]==raw["Site_ID"]) & (pre_df["T_sector"]==raw["Sector"]) & (pre_df["Date"].isin(pre_required_5_dates))]
        print('single_site pre df :',single_site_pre_df)
        single_site_post_df =post_df[(post_df["Site ID"]==raw["Site_ID"]) & (post_df["T_sector"]==raw["Sector"]) & (post_df["Date"].isin(post_required_5_dates))]
        print('single_site_post_df :',single_site_post_df)
        single_site_op_df=pd.DataFrame()
        
        ################# to tackel missing sites in pre or post ########
        if single_site_pre_df.empty:
            print("missing:",raw['Site_ID'])
            missing_sites.append({"Site":raw["Site_ID"],"Sector":raw['Sector'],"Remark":"Pre Data is missing"})
            continue
        if single_site_post_df.empty:
            print("missing:",raw['Site_ID'])
            missing_sites.append({"Site":raw["Site_ID"],"Sector":raw['Sector'],"Remark":"Post Data is missing"})
            continue
            
        for value in values:
            single_site_pre_piv_df =single_site_pre_df.pivot_table(index=["Cell ID","Site ID","BAND"],columns="Date",values=value)
            column_name =["PRE " + mapping_dict[value] + f"*D{i}" for i in range(1,6)]
    #         print(single_site_pre_piv_df)
            print("pre columns:",single_site_pre_piv_df.columns)
            single_site_pre_piv_df.columns = column_name
            
            ###### pivoting the post df ############
            single_site_post_piv_df = single_site_post_df.pivot_table(index=["Cell ID","Site ID","BAND"],columns="Date",values=value)
            column_name =["POST " +mapping_dict[value] + "*"+str(col.date()) for col in single_site_post_piv_df.columns]
            single_site_post_piv_df.columns=column_name
            single_site_pre_post_piv_df = pd.merge(single_site_pre_piv_df,single_site_post_piv_df, left_index=True, right_index=True, how="outer")
            single_site_op_df=pd.concat([single_site_op_df,single_site_pre_post_piv_df],axis=1)
            
        
        single_site_op_df.insert(0,"Remark", "        ")
        single_site_op_df.insert(1,"De-grow Date",raw["Dismantled date"].date()) 
        final_op=pd.concat([final_op,single_site_op_df],axis=0)
    missing_sites_df=pd.DataFrame(missing_sites)    
        
                                        
        
    print("op empty: ",final_op.empty)


    missing_sites_df

    multi_lev_col=[tuple(col.split("*")) for col in final_op.columns]
    multi_lev_col

    multiindex_col=pd.MultiIndex.from_tuples(multi_lev_col)
    final_op.columns=multiindex_col
    final_op

    final_op2=final_op.reset_index()

    final_op2

    # final_op2.rename(columns={"Short name":"Cell ID","T_Site_Name":"Site ID","MV Freq_Band":"BAND"}, inplace=True)
    final_op2.to_excel(r"output/op3.xlsx")
    final_op2


    ################ for sitewise payload ##################

    ########### for post ############
    unique_dates=list(post_df["Date"].unique())
    unique_dates.sort()
    post_required_5_dates = unique_dates[-5:]

    payload_final_op=pd.DataFrame()
    value="MV_4G Data Volume_GB"
    detail_sheet=[]
    for i,raw in additional_input.iterrows():
        unique_dates=list(set(pre_df[(pre_df["Date"]<raw["Dismantled date"]) & (pre_df["Site ID"]==raw["Site_ID"])]["Date"]))
        unique_dates.sort()
        pre_required_5_dates = unique_dates[-5:]
        print("pre_dates:",pre_required_5_dates)
        

        payload_single_site_pre_df =pre_df[(pre_df["Site ID"]==raw["Site_ID"])  & (pre_df["Date"].isin(pre_required_5_dates))]

        payload_single_site_post_df =post_df[(post_df["Site ID"]==raw["Site_ID"])  & (post_df["Date"].isin(post_required_5_dates))]

        if payload_single_site_pre_df.empty:
                continue
            #########for site wise  payload sheet  #########

        payload_single_site_pre_piv_df =payload_single_site_pre_df.pivot_table(index=["Site ID"],columns="Date",values="MV_4G Data Volume_GB",aggfunc='sum')
        column_name =["PRE " + mapping_dict[value] + f"*D{i}" for i in range(1,6)]
        print(payload_single_site_pre_piv_df)
        payload_single_site_pre_piv_df.columns = column_name

        ###### pivoting the post df ############
        payload_single_site_post_piv_df = payload_single_site_post_df.pivot_table(index=["Site ID"],columns="Date",values="MV_4G Data Volume_GB",aggfunc='sum')
        column_name =["POST " +mapping_dict[value] + "*"+str(col.date()) for col in payload_single_site_post_piv_df.columns]
        payload_single_site_post_piv_df.columns=column_name
        payload_single_site_pre_post_piv_df = pd.merge(payload_single_site_pre_piv_df,payload_single_site_post_piv_df, left_index=True, right_index=True, how="outer")

        payload_single_site_pre_post_piv_df.insert(0,"De-grow Date", raw["Dismantled date"].date())
        
        ####### for payload ###########
        payload_final_op=pd.concat([payload_final_op,payload_single_site_pre_post_piv_df],axis=0)
        
        ################### code for Details Sheet ########################
                                    
        detail_sheet.append({"SCOPE":raw['Site_ID'],"Pre KPI Date":f"({pre_required_5_dates[0].date()}) - ({pre_required_5_dates[-1].date()})","Cell":str(raw['Site_ID'])+str(raw['Sector']),"PROJECT":raw['Project'],"MS1 ( Degrow Date)":raw["Dismantled date"].date()})


    payload_final_op['Pre Average Payload'] = payload_final_op.iloc[:, 1:6].mean(axis=1)
    payload_final_op['Post Average Payload'] = payload_final_op.iloc[:, 6:].mean(axis=1)
    detail_sheet_df =pd.DataFrame(detail_sheet)
    payload_final_op

    detail_sheet_df

    ply_multi_lev_col=[tuple(col.split("*")) for col in payload_final_op.columns]
    ply_multi_lev_col
    ply_multiindex_col=pd.MultiIndex.from_tuples(ply_multi_lev_col)
    payload_final_op.columns=ply_multiindex_col

    payload_final_op2=payload_final_op.reset_index()

    payload_final_op2

    # payload_final_op2.rename(columns={"T_Site_Name":"Site ID"}, inplace=True)
    # payload_final_op2.to_excel(r"output/payload_op.xlsx")
    payload_final_op2
    save_path=os.path.join(MEDIA_ROOT,"Degrow","Degrow_PB_V2","pb_degrow_output.xlsx")
    with pd.ExcelWriter(save_path) as writer:
        # Write each DataFrame to a different sheet
        payload_final_op2.to_excel(writer, sheet_name='Site')
        final_op2.to_excel(writer, sheet_name='Cell')
        detail_sheet_df.to_excel(writer, sheet_name='Details',index=False)
        missing_sites_df.to_excel(writer, sheet_name='missing_site',index=False)

    save_url=os.path.join(MEDIA_URL,"Degrow","Degrow_PB_V2","pb_degrow_output.xlsx")

    return Response({"status":True,"message":"success","url":save_url})
