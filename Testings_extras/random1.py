import datetime

from datetime import timedelta,date

import pandas as pd
# date1=datetime.datetime.today()
# dt1 = date1 - timedelta(1)
# dt2 = date1 -  timedelta(2)
# dt3 = date1 - timedelta(3)
# dt4 = date1 -  timedelta(4)
# dt5 = date1 - timedelta(5)
# dt6 = date1- timedelta(6)


# print(dt1,dt2,dt3,dt4,dt5,dt6,)


# filepath=r"C:\Users\dell7480\Desktop\pre_post_tool\7day kpi\JDPLM2_POST 7 DAY KPI.xlsx"
# filepath=r"C:\Users\dell7480\Desktop\Mobile_com_web_app\mcom_website\media\Original_trend\record.xlsx"
# df_raw_kpi=pd.read_excel(filepath)



#                                 #__________ Preprocessing of the Raw KPI _____________#

# df_raw_kpi["Short name"].fillna( inplace=True, method="ffill")
# df_raw_kpi["Short name"] =df_raw_kpi["Short name"].apply(lambda x: x.strip()) # to remove all tralling spaces..... and leading spaces..


# df_raw_kpi.rename( columns={'Unnamed: 1':'date'}, inplace=True)

# df_raw_kpi["MV_DL User Throughput_Kbps [CDBH]"] = (df_raw_kpi["MV_DL User Throughput_Kbps [CDBH]"]/1024)
# df_raw_kpi.rename(columns={"MV_DL User Throughput_Kbps [CDBH]" :"MV_DL User Throughput_Mbps [CDBH]" } ,inplace = True )

# df_raw_kpi["MV_UL User Throughput_Kbps [CDBH]"] = (df_raw_kpi["MV_UL User Throughput_Kbps [CDBH]"]/1024)
# df_raw_kpi.rename(columns={"MV_UL User Throughput_Kbps [CDBH]" :"MV_UL User Throughput_Mbps [CDBH]" } ,inplace = True )

# print(df_raw_kpi)
# print(df_raw_kpi.columns)



# lis=list(df_raw_kpi["Short name"])
# sit_id_lis=[]
# cell_id_lis=[]
# for item in lis:
#         if("_" in item):
#             cell_id=item.split("_")[-2]
#             ln=len(item.split("_")[-1])
#             #print(ln)
#             sit_id=item.split("_")[-2][:-ln]
#         else:
#             cell_id=item
#             sit_id=item
#             cell_id_lis.append(cell_id)
#             sit_id_lis.append(sit_id)

# print(sit_id)
# print(cell_id_lis)

# df_raw_kpi.insert(1, "SITE_ID", sit_id_lis)
# df_raw_kpi.insert(2, "CELL_ID", cell_id_lis)



# df_raw_kpi.rename(columns={"Short name" :"Shortname" } ,inplace = True )
# df_raw_kpi.fillna(value=0,inplace=True)

# date1=datetime.datetime.today()
# dt1 = date1 - timedelta(1)
# dt2 = date1 - timedelta(2)
# dt3 = date1 - timedelta(3)
# dt4 = date1 - timedelta(4)
# dt5 = date1 - timedelta(5)
# dt6 = date1-  timedelta(6)
# dt7 = date1-  timedelta(7)
# ls=[dt1,dt2,dt3,dt4,dt5,dt6,dt7]
# df_DateFiltered = df_raw_kpi[(df_raw_kpi.date.isin(ls))]
# df_pivoted = df_DateFiltered.pivot_table(index=["SITE_ID","Shortname","CELL_ID"], columns="date")

# df_pivoted.to_excel("tst.x

# path=r"C:\Users\dell7480\Desktop\Mobile_com_web_app\mcom_website\media\Original_trend\record.xlsx"
# idx=pd.IndexSlice
# df=pd.read_excel(path,header=[0,1],engine="openpyxl")
# # dr=df.loc[idx[1:10],idx[("Pre_Volte_Traffic","Day1"):("Post_Volte_Traffic","Day7")]]
# # print(dr)

# print(df)
# T_df=df.T

# print(T_df)
# print(T_df.index.is_lexsorted())

# sorted = T_df.sort_index()
# print(sorted)
# print(sorted.index.is_lexsorted())

# df=sorted.T

# print(df)
# df.to_excel("tjsjj.xlsx")

# dr=df.loc[idx[1:10],idx[("Pre_Volte_Traffic","Day1"):("Post_Volte_Traffic","Day7")]]
# print(dr)


dat=date.today()
print(dat)