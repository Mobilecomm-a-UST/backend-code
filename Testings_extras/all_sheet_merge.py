import pandas as pd
df_dict=pd.read_excel(r"C:\Users\dell7480\Desktop\mcom tools\Trend_Project\Tnch_trend\Tnch_NPN_trend_project(0.2)\output\Tnch_trend_output.xlsx",header=[0,2],sheet_name=None) #use  sheet_name=none to make a dictionary of df

print(df_dict["L2100"]) # accessing a perticular df from the df_dict
df = pd.concat(df_dict.values(), axis=0)  # we can merge all dfs in df_dict by this code.
print(df)
df.to_excel("hdhdh.xlsx")
df_req=df[["Unnamed: 0_level_0","CRITERIA","LTE Inter System HO Succ Rate"]]
print(df_req.loc[ : ,("CRITERIA",["SITE"])]  )
# Report_Card.drop(5,axis=0,inplace=True) #to drop a perticular row
# Report_Card.drop("Retake",axis=1,inplace=True) # to drap a perticular column

# df_req.columns = ['_'.join(str(col)) for col in df_req.columns.values]
df_req.columns = df_req.columns.to_flat_index()
print(df_req)
df_req.to_excel("now.xlsx")