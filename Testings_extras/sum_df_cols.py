import pandas as pd


path=r"C:\Users\dell7480\Desktop\Mobile_com_web_app\mcom_website\report without header.xlsx"
all_df=pd.read_excel(path)
print(all_df)
sum_list=[]
site_list=["JDPLM2"]
for site in site_list:
    df=all_df[all_df.Post_cell_site_id==site]
    print(df)

    print("#################################################################################################")
    df_sum=df.sum(axis=0,numeric_only=True)
    # df_sum.T.to_excel("kkddkk.xlsx")
    df_list=df_sum.tolist()
    print(df_list)

    sum_list.append(df_list)

dr=pd.DataFrame(sum_list)
print(dr)