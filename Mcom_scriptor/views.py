from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import xml.etree.ElementTree as ET
import pandas as pd
import os
from mcom_website.settings import MEDIA_ROOT,MEDIA_URL
from .dynamic import process 
import Mcom_scriptor.modify_xml_element
import datetime
# Create your views here.

@api_view(["POST"])
def XML_scriptor(request):
    print("current_user:",request.user)
    input_xl = request.FILES["input_xl"] if 'input_xl' in request.FILES else None
    input_df2=pd.read_excel(input_xl, sheet_name="Sheet2",dtype=str)
    # input_df2=input_df2.dropna().astype(str)
    input_df2.fillna('', inplace=True)
    input2_dict=input_df2.to_dict(orient='list')
    input2_dict = {key: [value for value in values if value != ''] for key, values in input2_dict.items()}
    
    # print(input2_dict)
    for key,value in input2_dict.items():
        print(key,":",value)
        # print(value)
    # exit(0)
    input_df1=pd.read_excel(input_xl, sheet_name="CellWise",dtype=str)
    input_df1.dropna(subset=['Cell ID'], inplace=True)
    print(input_df1)
    input1_dict=input_df1.to_dict(orient='record')
    # print(input1_dict)
    for x in input1_dict:
        print(x)
    


    # Filter columns containing 'irfim' followed by a space and a digit
    irfim_df = input_df1.filter(regex=r'\b(IRFIM \d+)\b')
    # Rename columns by taking the second word of each column name
    irfim_df.columns = irfim_df.columns.str.strip().str.split().str[1]
    # Convert the DataFrame to a dictionary with orient 'records'
    irfim_df.set_index(input_df1['Cell ID'], inplace=True)
    print(irfim_df)
    irfim_dict = irfim_df.to_dict(orient='index')
    print("IRFIM:",irfim_dict)   
    # exit(0)



    # Filter columns containing 'LNHOIF' followed by a space and a digit
    lnhoif_df = input_df1.filter(regex=r'\b(LNHOIF \d+)\b')
    # Rename columns by taking the second word of each column name
    lnhoif_df.columns = lnhoif_df.columns.str.strip().str.split().str[1]
    # Convert the DataFrame to a dictionary with orient 'records'
    lnhoif_df.set_index(input_df1['Cell ID'], inplace=True)
    print(lnhoif_df)
    lnhoif_dict = lnhoif_df.to_dict(orient='index')
    print("LNHOIF:",lnhoif_dict) 
    # exit(0)


    # Creating irfim_lnhoif_list
    irfim_lnhoif_list=lnhoif_df.columns.to_list()
    print("irfim_lnhoif_list......... :",irfim_lnhoif_list)
    #creating  cell_list
    cell_list= input_df1["Cell ID"].tolist()
    print("cell_list.....................",cell_list)

    
    #creating cell mimo dict
    cell_mimo_df=input_df1[["Cell ID","MIMO","LTE CellName"]]
    # cell_mimo = cell_mimo_df.set_index('Cell ID')['MIMO'].to_dict()
    cell_mimo_df['cell_sector']=cell_mimo_df['LTE CellName'].str[-1]
    print(cell_mimo_df)
    # Group by 'cell_name' and aggregate 'cell_id' values into a tuple
    grouped_df = cell_mimo_df.groupby('cell_sector')['Cell ID','MIMO'].agg(tuple).reset_index()

    # Rename the column to 'cell_ids'
    grouped_df.rename(columns={'Cell ID': 'cell_ids'}, inplace=True)
    print(grouped_df)
    cell_mimo={}
    for index,raw in grouped_df.iterrows():
        print(raw)
        cell_mimo[raw['cell_ids']]=raw['MIMO'][0]


    print(cell_mimo)
    # cell_mimo={(11,21):"4T4R",(12,22):"2T2R",(13,23):"2T2R"}
    print("Cell MIMO:............... ",cell_mimo)

    POST_request= request.POST
    print(POST_request)
    root=process(cell_list,irfim_lnhoif_list,cell_mimo,POST_request,input2_dict)

    file_name=Mcom_scriptor.modify_xml_element.process(input1_dict,input2_dict,cell_list,root,irfim_dict,lnhoif_dict)

    download_url=os.path.join(MEDIA_URL,"Mcom_scriptor","output",file_name)
    
    return Response({"status":True,"Xml_script_url":download_url}) 


    

    # _______________________________********************************________________________
                
