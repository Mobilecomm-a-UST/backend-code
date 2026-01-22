from django.shortcuts import render
import pandas as pd
from rest_framework.decorators import api_view
from commom_utilities.utils import *
# Create your views here.
@api_view(["GET"])
def RNA_Payload(request):

    payload_file=request.FILES["Payload_file"] if request.FILES["Payload_file"] else None
    payload_file_df=pd.read_csv(payload_file)

    ATP_file=request.FILES["ATP_file"] if request.FILES["ATP_file"] else None
    ATP_file_df=pd.read_csv(ATP_file)

    alarm_nokia_file=request.FILES["alarm_nokia_file"] if request.FILES["alarm_nokia_file"] else None
    alarm_nokia_file_df=pd.read_csv(alarm_nokia_file)

    alarm_erricsion_file=request.FILES["alarm_erricsion_file"] if request.FILES["alarm_erricsion_file"] else None
    alarm_erricsion_file_df=pd.read_csv(alarm_erricsion_file)

    alarm_huawei_file=request.FILES["alarm_huawei_file"] if request.FILES["alarm_huawei_file"] else None
    alarm_huawei_file_df=pd.read_csv(alarm_huawei_file)

    # script_file=r"E:\datascience\rna payload_original.ipynb"
    script_file=r"E:\datascience\testing.ipynb"

    op_df=run_ipynb(script_path=script_file,payload_file_df=payload_file_df,ATP_file=ATP_file,alarm_nokia_file=alarm_nokia_file,alarm_erricsion_file=alarm_erricsion_file,alarm_huawei_file=alarm_huawei_file)

    return Response({"status":True})