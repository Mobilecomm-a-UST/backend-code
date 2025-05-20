from django.shortcuts import render
from mcom_website.settings import MEDIA_ROOT,MEDIA_URL
import os
from django.shortcuts import render
import datetime
from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse
import sys
import pandas as pd
from django.contrib import messages
# import json
from django.contrib.auth.decorators import login_required
# from mcom_websites.settings import MEDIA_URL,BASE_DIR,ALLOWED_HOSTS
import numpy as np
import os
import datetime
from rest_framework.decorators import api_view,parser_classes
from rest_framework.response import Response
from django.http import JsonResponse
# from .serializer import *
from django.forms.models import model_to_dict

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes,permission_classes
from django.core.files.storage import FileSystemStorage
# from .settings import MEDIA_ROOT
from .models import *

import openpyxl
# from openpyxl.styles import PatternFill
# Create your views here.
from openpyxl import Workbook,load_workbook
from statistics import mean

from django.db.models import Sum
# from Merged_APP.form import UploadFilesForm



import pandas as pd
# import matplotlib  as mpl
import numpy as np

from datetime import date, timedelta

# from zipfile import ZipFile
import os

from django.core.files.storage import FileSystemStorage

import pandas as pd
from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
import glob



        


import pandas as pd
from django.http import JsonResponse


def merge_dataframe(dict_list):
    dfs = []
    i=0
    for name,file in dict_list.items():
        print("doning...",i)
        i=i+1
        df = pd.read_csv(file)
        dfs.append(df)
    merge_df = pd.concat(dfs, ignore_index=True)

    return merge_df




@api_view(["POST"])
def merge_App(request):
    files = request.FILES
    
    print(files)
    
    dict = files

    list = ["ATP_file", "RNA_PAYL_file","4G_raw_kpi","4G_site_list"]

    for x in list:
        if x in dict.keys():
            dict.popitem()

    print(dict)
    # file_extension = os.path.splitext(files.values['file_1'].name)[1]
    # print(file_extension)
    merged_df=merge_dataframe(dict)
    
    custom_header = ['COLUMN1', 'COLUMN2']
    
    file_name= "merged_file" + str(datetime.datetime.now().date())+ "_tim-" +str(datetime.datetime.now().time()).replace(':',"-").replace('.',"_") + ".csv"
    file_name=file_name.replace(' ',"_")

    savepath=os.path.join(MEDIA_ROOT,'mergeAPP',file_name) 
    merged_df.to_csv(savepath, index=False)
    
    downlad_url1=os.path.join(MEDIA_URL,'mergeAPP',file_name) 
    print(merged_df)
    
    return Response({"status": True,"Download_url1": downlad_url1,"message":"file merged sucessfully"})
    
    
    