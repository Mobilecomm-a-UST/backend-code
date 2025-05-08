from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import dpr_upload_form
from .models import DPR_file
import pandas as pd
from .models import DPR_table1,DPR_update_status,performance_at_table
from django.contrib import messages
from .forms import soft_at_acceptance,soft_at_offered,soft_at_pending,soft_at_rejection
from .forms import physical_at_acceptance,physical_at_offered,physical_at_pending,physical_at_rejection
from .forms import performance_at_acceptance,performance_at_offered,performance_at_pending,performance_at_rejection
from django.contrib.auth.decorators import login_required
from mcom_website.settings import MEDIA_URL,BASE_DIR
import numpy as np
import os
import datetime
from rest_framework.decorators import api_view,parser_classes
from rest_framework.response import Response
from django.http import JsonResponse

from .serializer import *

from django.forms.models import model_to_dict

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes,permission_classes
from django.core.files.storage import FileSystemStorage
from mcom_website.settings import MEDIA_ROOT
def circle_list(objs):
    cir=[]
    
    for obj in objs:
        cir.append(obj.CIRCLE)

    cir_set=set(cir)
    cir=list(cir_set)
    return cir

@api_view(["GET"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def get_circle(request):
    cir=[]
    objs=DPR_table1.objects.all()
    for obj in objs:
        cir.append(obj.CIRCLE)

    cir_set=set(cir)
    cir=list(cir_set)
    return Response({"cir":cir})

@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def dpr_key_upload(request):
    
            # message=""
            # status=""
            # DPR_file.objects.all().delete()
                    # obj=DPR_file.objects.create(dpr_file=file)
                    # path=str(obj.dpr_file)
                    # print(path)
                    # df=pd.read_excel("media/"+path)
            
            file = request.FILES["key_file"] if 'key_file' in request.FILES else None
            if file:
                    location=MEDIA_ROOT + r"\dpr\dpr_key_file"
                    fs = FileSystemStorage(location=location)
                    file = fs.save(file.name, file)
                    # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
                    filepath = fs.path(file)
                    print("file_path:-",filepath)
                    df=pd.read_excel(filepath)
                    os.remove(path=filepath)
                    print(filepath,"deleted...............")
                    print(df)
                    del_obj=[]
                    if not(df.empty):
                        for i,d in df.iterrows():
                   
                                pk=str(d["CIRCLE"])+str(d["Unique_SITE_ID"])+str(d["BAND"])+str(d["TOCO_NAME"])+str(d["Project"])+str(d["Activity"])
                                try:
                                    rfai_date= d["RFAI_DATE"] if not(pd.isnull(d["RFAI_DATE"])) else None
                                    oa_date= d["OA_(COMMERCIAL_TRAFFIC_PUT_ON_AIR)_(MS1)_DATE"] if not(pd.isnull(d["OA_(COMMERCIAL_TRAFFIC_PUT_ON_AIR)_(MS1)_DATE"])) else None
                                    mapa_date= d["MAPA_INCLUSION_DATE"] if not(pd.isnull(d["MAPA_INCLUSION_DATE"])) else None
                                    obj=DPR_table1.objects.create(id=pk,
                                                    SITE_ID=str(d["SITE_ID"]),
                                                    CIRCLE=str(d["CIRCLE"]),
                                                    Unique_SITE_ID=str(d["Unique_SITE_ID"]),
                                                    BAND=str(d["BAND"]),
                                                    TOCO_NAME=str(d["TOCO_NAME"]),
                                                    Project=str(d["Project"]),
                                                    Activity=str(d["Activity"]),
                                                    RFAI_DATE=rfai_date,
                                                    OA_COMMERCIAL_TRAFFIC_PUT_ON_AIR_MS1_DATE=oa_date,
                                                    MAPA_INCLUSION_DATE=mapa_date,
                                                    Internal_RFAI_Vs_Ms1_In_Days=str(d["Internal RFAI Vs Ms1-In Days"]),
                                                    Internal_Ms1_Vs_Ms2_In_days=str(d["Internal Ms1 Vs Ms2-In days"]),
                                                    )
                                    bands=str(d["BAND"]).split("_")
                                    print(bands)
                                    for band in bands:
                                        performance_at_table.objects.create(key=obj,band=band)

                                    del_obj.append(obj)
                                    print("obj created",obj)
                                except Exception as e:
                                    print("this is the exception",e)
                                    for o in del_obj:
                                        o.delete()
                                        print("obj deleted",o)
                                    
                                    message='Could not upload,Site id are not unique'
                                    status=False
                                    break
                        else:   
                            
                                message='DPR is Succesfully uploaded'
                                status=True
                               
                    else:
                           
                            message='Coluld not upload,DPR is empty'
                            status=False
            else:
                            
                            message='Did not get any DPR key file'
                            status=False
            context={"messages":message,"status":status}
            return Response(context)                

@api_view(["GET"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def get_dpr_key_temp(request,):
     path="/media/dpr/dpr_templates/DPR_KEY_TEMP.xlsx"
     return Response({"path":path})
 
@api_view(["POST"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def dpr_report_update(request):

    DPR_update_status.objects.all().delete()
    file=request.FILES["myfile"] #required
    soft_at=request.FILES["soft_at"] #required
    physical_at=request.FILES["physical_at"] #required
    G1800=request.FILES.get("G1800",None)
    L900=request.FILES.get("L900",None)
    L1800=request.FILES.get("L1800",None)
    L2300=request.FILES.get("L2300",None)
    L2100=request.FILES.get("L2100",None)
   

    file = request.FILES["myfile"] if 'myfile' in request.FILES else None
    if file:
            location=MEDIA_ROOT + r"\dpr\dpr_report_file"
            fs = FileSystemStorage(location=location)
            file = fs.save(file.name, file)
            # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
            filepath = fs.path(file)
            print("file_path:-",filepath)
            df=pd.read_excel(filepath)
            os.remove(path=filepath)
            print(filepath,"deleted...............")
            print(df)
 
            
            del_obj=[]
            if not(df.empty):
                for i,d in df.iterrows():
                   
                            pk=str(d["CIRCLE"])+str(d["Unique_SITE_ID"])+str(d["BAND"])+str(d["TOCO_NAME"])+str(d["Project"])+str(d["Activity"])
                            try:
                                obj=DPR_table1.objects.get(id=pk)
                                kpi_objs=performance_at_table.objects.filter(key=obj) 
                            except:
                                    status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="site not found in database" )
                                    continue
                           
    ##################################################################### Soft at ##################################################################           
                           
                            if d["Soft_AT_Status"] == "ACCEPTED" or d["Soft_AT_Status"] == "REJECTED" or d["Soft_AT_Status"] == "OFFERED" or d["Soft_AT_Status"] == "PENDING":
                               
                                if d["Soft_AT_Status"] == "ACCEPTED":
                                        if obj.Soft_AT_Status == "ACCEPTED":
                                            status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Status Already accepted in the database" )
                                            
                                            continue
                                        else:
                                            obj.Soft_AT_Status=d["Soft_AT_Status"]
                                            if not pd.isnull(d["SOFT_AT_ACCEPTANCE_DATE"]) and  isinstance(d["SOFT_AT_ACCEPTANCE_DATE"], datetime.datetime):
                                                obj.SOFT_AT_ACCEPTANCE_DATE = d["SOFT_AT_ACCEPTANCE_DATE"]
                                                
                                            else:
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at acceptance date is missing or date formate is not correct" ) 
                                                continue
                                            obj.SOFT_AT_ACCEPTANCE_MAIL=soft_at
                                            obj.SOFT_AT_REJECTION_DATE = None
                                            obj.SOFT_AT_REJECTION_REASON= ""
                                            obj.SOFT_AT_OFFERED_DATE= None
                                            obj.SOFT_AT_OFFERED_REMARKS= ""
                                            obj.SOFT_AT_PENDING_REASON= ""
                                            obj.SOFT_AT_PENDING_REMARK= ""
                                            obj.SOFT_AT_PENDING_TAT_DATE= None
                                            

                                if d["Soft_AT_Status"] == "REJECTED":
                                        print("inside REJECTED update")
                                        
                                        obj.Soft_AT_Status=d["Soft_AT_Status"]
                                        if not pd.isnull(d["SOFT_AT_REJECTION_DATE"]) and  isinstance(d["SOFT_AT_REJECTION_DATE"], datetime.datetime):
                                            obj.SOFT_AT_REJECTION_DATE = d["SOFT_AT_REJECTION_DATE"]
                                            print("updated")
                                        else:
                                            if pd.isnull(d["SOFT_AT_REJECTION_DATE"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Rejection date is missing" )
                                            else:
                                                 status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Rejection date formate is not correct" )
                                          
                                            continue    
                                        if pd.isnull(d["SOFT_AT_REJECTION_REASON"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Rejection Reason is missing" )
                                                continue
                                        else:
                                              obj.SOFT_AT_REJECTION_REASON=d["SOFT_AT_REJECTION_REASON"]
            
                                        obj.SOFT_AT_ACCEPTANCE_DATE=None
                                        obj.SOFT_AT_ACCEPTANCE_MAIL="" 
                                        obj.SOFT_AT_OFFERED_DATE= None
                                        obj.SOFT_AT_OFFERED_REMARKS= ""
                                        obj.SOFT_AT_PENDING_REASON= ""
                                        obj.SOFT_AT_PENDING_REMARK= ""
                                        obj.SOFT_AT_PENDING_TAT_DATE= None   
                                                    

                                if d["Soft_AT_Status"] == "OFFERED":
                                        print("inside OFFERED update")
                                        
                                        obj.Soft_AT_Status=d["Soft_AT_Status"]
                                        
                                        if not pd.isnull(d["SOFT_AT_OFFERED_DATE"]) and  isinstance(d["SOFT_AT_OFFERED_DATE"], datetime.datetime):
                                            obj.SOFT_AT_OFFERED_DATE=d["SOFT_AT_OFFERED_DATE"]
                                            print("updated")
                                        else:
                                            if pd.isnull(d["SOFT_AT_OFFERED_DATE"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Offered date is missing" )
                                            else:
                                                 status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Offered date formate is not correct" ) 
                                            continue    

                                        if pd.isnull(d["SOFT_AT_OFFERED_REMARKS"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Offered remark is missing" )
                                                continue
                                        else:
                                              obj.SOFT_AT_OFFERED_REMARKS=d["SOFT_AT_OFFERED_REMARKS"]  

                                        obj.SOFT_AT_ACCEPTANCE_DATE=None
                                        obj.SOFT_AT_ACCEPTANCE_MAIL=""
                                        obj.SOFT_AT_REJECTION_DATE = None
                                        obj.SOFT_AT_REJECTION_REASON=""
                                        obj.SOFT_AT_PENDING_REASON= ""
                                        obj.SOFT_AT_PENDING_REMARK= ""
                                        obj.SOFT_AT_PENDING_TAT_DATE= None
                                        
                                        
                                if d["Soft_AT_Status"] == "PENDING":
                                        print("inside PENDING update")
                                        obj.Soft_AT_Status=d["Soft_AT_Status"]
                                        if pd.isnull(d["SOFT_AT_PENDING_REASON"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Pending Reason is missing" )
                                                continue
                                        else:
                                              obj.SOFT_AT_PENDING_REASON=d["SOFT_AT_PENDING_REASON"] 

                                        if pd.isnull(d["SOFT_AT_PENDING_REMARK"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Pending Remark is missing" )
                                                continue
                                        else:
                                              obj.SOFT_AT_PENDING_REMARK=d["SOFT_AT_PENDING_REMARK"]
                                        
                                        
                                        if not pd.isnull(d["SOFT_AT_PENDING_TAT_DATE"]) and  isinstance(d["SOFT_AT_PENDING_TAT_DATE"], datetime.datetime):
                                            obj.SOFT_AT_PENDING_TAT_DATE=d["SOFT_AT_PENDING_TAT_DATE"]
                                            print("updated")
                                        else:
                                            if pd.isnull(d["SOFT_AT_PENDING_TAT_DATE"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Pending TAT date is missing" )
                                            else:
                                                 status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Pending TAT formate is not correct" )
                                            continue   
                                        obj.SOFT_AT_ACCEPTANCE_DATE=None
                                        obj.SOFT_AT_ACCEPTANCE_MAIL=""
                                        obj.SOFT_AT_REJECTION_DATE = None
                                        obj.SOFT_AT_REJECTION_REASON=""
                                        obj.SOFT_AT_OFFERED_DATE= None
                                        obj.SOFT_AT_OFFERED_REMARKS= ""
                            
                            else:
                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Getting Soft At Status Other than ACCEPTED/REJECTED/PENDING/OFFERED" )  
                                continue
                            
    ########################################## PHYSICAL AT ############################################################################
                            
                            if d["PHYSICAL_AT_Status"] == "ACCEPTED" or d["PHYSICAL_AT_Status"] == "REJECTED" or d["PHYSICAL_AT_Status"] == "OFFERED" or d["PHYSICAL_AT_Status"] == "PENDING":
                               
                                if d["PHYSICAL_AT_Status"] == "ACCEPTED":
                                        if obj.PHYSICAL_AT_Status == "ACCEPTED":
                                            status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Status Already accepted in the database" )
                                            continue
                                        else:
                                            if not pd.isnull(d["PHYSICAL_AT_ACCEPTANCE_DATE"]) and  isinstance(d["PHYSICAL_AT_ACCEPTANCE_DATE"], datetime.datetime):
                                                obj.PHYSICAL_AT_ACCEPTANCE_DATE = d["PHYSICAL_AT_ACCEPTANCE_DATE"]
                                                obj.PHYSICAL_AT_Status=d["PHYSICAL_AT_Status"]
                                            else:
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at acceptance date is missing or date formate is not correct" )
                                                continue
                                            obj.PHYSICAL_AT_ACCEPTANCE_MAIL=physical_at
                                            obj.PHYSICAL_AT_REJECTION_DATE = None
                                            obj.PHYSICAL_AT_REJECTION_REASON= ""
                                            obj.PHYSICAL_AT_OFFERED_DATE= None
                                            obj.PHYSICAL_AT_OFFERED_REMARKS= ""
                                            obj.PHYSICAL_AT_PENDING_REASON= ""
                                            obj.PHYSICAL_AT_PENDING_REMARK= ""
                                            obj.PHYSICAL_AT_PENDING_TAT_DATE= None
                                        
                                            
                                


                                if d["PHYSICAL_AT_Status"] == "REJECTED":
                                        print("inside REJECTED update")
                                        obj.PHYSICAL_AT_Status=d["PHYSICAL_AT_Status"]
                                        
                                        if not pd.isnull(d["PHYSICAL_AT_REJECTION_DATE"]) and  isinstance(d["PHYSICAL_AT_REJECTION_DATE"], datetime.datetime):
                                            obj.PHYSICAL_AT_REJECTION_DATE = d["PHYSICAL_AT_REJECTION_DATE"]
                                            print("updated")
                                        
                                        else:
                                            if pd.isnull(d["PHYSICAL_AT_REJECTION_DATE"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Rejection date is missing" )
                                            else:
                                                 status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Rejection date formate is not correct" )
                                            continue    
                                       
                                        if pd.isnull(d["PHYSICAL_AT_REJECTION_REASON"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Rejection Reason is missing" )
                                                continue
                                        else:
                                              obj.PHYSICAL_AT_REJECTION_REASON=d["PHYSICAL_AT_REJECTION_REASON"]
                                                     
                                        obj.PHYSICAL_AT_ACCEPTANCE_DATE=None
                                        obj.PHYSICAL_AT_ACCEPTANCE_MAIL=""
                                        obj.PHYSICAL_AT_OFFERED_DATE= None
                                        obj.PHYSICAL_AT_OFFERED_REMARKS= ""
                                        obj.PHYSICAL_AT_PENDING_REASON= ""
                                        obj.PHYSICAL_AT_PENDING_REMARK= ""
                                        obj.PHYSICAL_AT_PENDING_TAT_DATE= None   
                            
                            
                                if d["PHYSICAL_AT_Status"] == "OFFERED":
                                        print("inside OFFERED update")
                                        
                                        obj.PHYSICAL_AT_Status=d["PHYSICAL_AT_Status"]
                                        
                                        if not pd.isnull(d["PHYSICAL_AT_OFFERED_DATE"]) and  isinstance(d["PHYSICAL_AT_OFFERED_DATE"], datetime.datetime):
                                            obj.PHYSICAL_AT_OFFERED_DATE=d["PHYSICAL_AT_OFFERED_DATE"]
                                            print("updated")
                                        else:
                                            if pd.isnull(d["PHYSICAL_AT_OFFERED_DATE"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Offered date is missing" )
                                            else:
                                                 status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Offered date formate is not correct" )
                                            
                                            continue    

                                        if pd.isnull(d["PHYSICAL_AT_OFFERED_REMARKS"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Offered remark is missing" )
                                                continue
                                        else:
                                              obj.PHYSICAL_AT_OFFERED_REMARKS=d["PHYSICAL_AT_OFFERED_REMARKS"]  

                                        obj.PHYSICAL_AT_ACCEPTANCE_DATE=None
                                        obj.PHYSICAL_AT_ACCEPTANCE_MAIL=""
                                        obj.PHYSICAL_AT_REJECTION_DATE = None
                                        obj.PHYSICAL_AT_REJECTION_REASON=""
                                        obj.PHYSICAL_AT_PENDING_REASON= ""
                                        obj.PHYSICAL_AT_PENDING_REMARK= ""
                                        obj.PHYSICAL_AT_PENDING_TAT_DATE= None
                            
                                         
                                if d["PHYSICAL_AT_Status"] == "PENDING":
                                        print("inside PENDING update")
                                        obj.PHYSICAL_AT_Status=d["PHYSICAL_AT_Status"]
                                        if pd.isnull(d["PHYSICAL_AT_PENDING_REASON"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Pending Reason is missing" )
                                                continue
                                        else:
                                              obj.PHYSICAL_AT_PENDING_REASON=d["PHYSICAL_AT_PENDING_REASON"] 

                                        if pd.isnull(d["PHYSICAL_AT_PENDING_REMARK"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Pending Remark is missing" )
                                                continue
                                        else:
                                              obj.PHYSICAL_AT_PENDING_REMARK=d["PHYSICAL_AT_PENDING_REMARK"]
                                        
                                        
                                        if not pd.isnull(d["PHYSICAL_AT_PENDING_TAT_DATE"]) and  isinstance(d["PHYSICAL_AT_PENDING_TAT_DATE"], datetime.datetime):
                                            obj.SOFT_AT_PENDING_TAT_DATE=d["PHYSICAL_AT_PENDING_TAT_DATE"]
                                            print("updated")
                                        else:
                                            if pd.isnull(d["PHYSICAL_AT_PENDING_TAT_DATE"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Pending TAT date is missing" )
                                            else:
                                                 status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Pending TAT formate is not correct" )
                                            continue   
                                        obj.PHYSICAL_AT_ACCEPTANCE_DATE=None
                                        obj.PHYSICAL_AT_ACCEPTANCE_MAIL=""
                                        obj.PHYSICAL_AT_REJECTION_DATE = None
                                        obj.PHYSICAL_AT_REJECTION_REASON=""
                                        obj.PHYSICAL_AT_OFFERED_DATE= None
                                        obj.PHYSICAL_AT_OFFERED_REMARKS= ""
                            
                            else:
                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Getting Physical At Status Other than ACCEPTED/REJECTED/PENDING/OFFERED" )
                                continue
                            
                            
    ############################################### PERFORMANCE AT #####################################################################################################################################################################     
                           
                            bands=str(d["BAND"]).split("_")
                            print(bands)
                            if d["Performance_AT_Status"] == "ACCEPTED" or d["Performance_AT_Status"] == "REJECTED" or d["Performance_AT_Status"] == "OFFERED" or d["Performance_AT_Status"] == "PENDING":
                               
                                if d["Performance_AT_Status"] == "ACCEPTED":
                                        if obj.Performance_AT_Status == "ACCEPTED":
                                            status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark=" Performance at Status Already accepted in the database" )
                                           
                                            continue
                                        else:
                                            obj.Performance_AT_Status=d["Performance_AT_Status"]
                                            if not pd.isnull(d["PERFORMANCE_AT_ACCEPTANCE_DATE"]) and  isinstance(d["PERFORMANCE_AT_ACCEPTANCE_DATE"], datetime.datetime):
                                                obj.PERFORMANCE_AT_ACCEPTANCE_DATE = d["PERFORMANCE_AT_ACCEPTANCE_DATE"]
                                            else:
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at acceptance date is missing or date formate is not correct")
                                                continue

                                            for kpi_obj in kpi_objs:
                                                if kpi_obj.band=="G1800":
                                                  kpi_obj.Performance_AT_Status="ACCEPTED"
                                                  kpi_obj.PERFORMANCE_AT_ACCEPTANCE_MAIL=G1800
                                                  kpi_obj.PERFORMANCE_AT_ACCEPTANCE_DATE=d["PERFORMANCE_AT_ACCEPTANCE_DATE"]
                                                
                                                if kpi_obj.band=="L1800":
                                                  kpi_obj.Performance_AT_Status="ACCEPTED"
                                                  kpi_obj.PERFORMANCE_AT_ACCEPTANCE_DATE=d["PERFORMANCE_AT_ACCEPTANCE_DATE"]
                                                  kpi_obj.PERFORMANCE_AT_ACCEPTANCE_MAIL=L1800

                                                
                                                if kpi_obj.band=="L900":
                                                  kpi_obj.Performance_AT_Status="ACCEPTED"
                                                  kpi_obj.PERFORMANCE_AT_ACCEPTANCE_DATE=d["PERFORMANCE_AT_ACCEPTANCE_DATE"]
                                                  kpi_obj.PERFORMANCE_AT_ACCEPTANCE_MAIL=L900
                                                
                                                if kpi_obj.band=="L2300":
                                                  kpi_obj.Performance_AT_Status="ACCEPTED"
                                                  kpi_obj.PERFORMANCE_AT_ACCEPTANCE_DATE=d["PERFORMANCE_AT_ACCEPTANCE_DATE"]
                                                  kpi_obj.PERFORMANCE_AT_ACCEPTANCE_MAIL=L2300
                                                
                                                if kpi_obj.band=="L2100":
                                                  kpi_obj.Performance_AT_Status="ACCEPTED"
                                                  kpi_obj.PERFORMANCE_AT_ACCEPTANCE_DATE=d["PERFORMANCE_AT_ACCEPTANCE_DATE"]
                                                  kpi_obj.PERFORMANCE_AT_ACCEPTANCE_MAIL=L2100
                                                kpi_obj.save()
                                               

                                            
                                            obj.PERFORMANCE_AT_REJECTION_DATE = None
                                            obj.PERFORMANCE_AT_REJECTION_REASON= "" 
                                            obj.PERFORMANCE_AT_OFFERED_DATE= None
                                            obj.PERFORMANCE_AT_OFFERED_REMARKS= ""
                                            obj.PERFORMANCE_AT_PENDING_REASON= ""
                                            obj.PERFORMANCE_AT_PENDING_REMARK= ""
                                            obj.PERFORMANCE_AT_PENDING_TAT_DATE= None
                                        
                                           
                                        
                                if d["Performance_AT_Status"] == "REJECTED":
                                        obj.Performance_AT_Status=d["Performance_AT_Status"]
                                        if not pd.isnull(d["PERFORMANCE_AT_REJECTION_DATE"])  and  isinstance(d["PERFORMANCE_AT_REJECTION_DATE"], datetime.datetime):
                                            obj.PERFORMANCE_AT_REJECTION_DATE = d["PERFORMANCE_AT_REJECTION_DATE"]

                                        else:
                                            if pd.isnull(d["PERFORMANCE_AT_REJECTION_DATE"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Rejection date is missing" )
                                            else:
                                                 status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Rejection date formate is not correct" )
                                           
                                            continue    
                                        if pd.isnull(d["PERFORMANCE_AT_REJECTION_REASON"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Rejection Reason is missing" )
                                                continue
                                        else:
                                              obj.PERFORMANCE_AT_REJECTION_REASON=d["PERFORMANCE_AT_REJECTION_REASON"]
                                                
                                              lis_kpi_status_bandwise=d["PERFORMANCE_AT_REJECTION_REASON"].split(",")
                                              
                                              
                                              di={}
                                              sts=True
                                              for band_status in lis_kpi_status_bandwise:
                                                    if("_" in band_status):
                                                            lis=band_status.split("_")
                                                            di[lis[0]] = lis[1]
                                                    else:
                                                        status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Band and status should be separated by a '_' in the PERFORMANCE_AT_REJECTION_REASON " )
                                                        sts=False
                                                        break
                                              if sts==False:
                                                continue

                                                    
                                              for  kpi_obj in kpi_objs:
                                                    if kpi_obj.band in di.keys():
                                                        kpi_obj.Performance_AT_Status=di[str(kpi_obj.band)] 
                                                        print(di[str(kpi_obj.band)], kpi_obj.band)
                                                        kpi_obj.save()
                                              print(di)

                                         
                                        obj.PERFORMANCE_AT_ACCEPTANCE_DATE=None
                                        obj.PERFORMANCE_AT_OFFERED_DATE= None
                                        obj.PERFORMANCE_AT_OFFERED_REMARKS= ""
                                        obj.PERFORMANCE_AT_PENDING_REASON= ""
                                        obj.PERFORMANCE_AT_PENDING_REMARK= ""
                                        obj.PERFORMANCE_AT_PENDING_TAT_DATE= None
                                
                                if d["Performance_AT_Status"] == "OFFERED":
                                        print("inside OFFERED update")
                                        
                                        obj.Performance_AT_Status=d["Performance_AT_Status"]
                                        
                                        if not pd.isnull(d["PERFORMANCE_AT_OFFERED_DATE"]) and isinstance(d["PERFORMANCE_AT_OFFERED_DATE"], datetime.datetime):
                                            obj.PERFORMANCE_AT_OFFERED_DATE=d["PERFORMANCE_AT_OFFERED_DATE"]
                                            print("updated")
                                        else:
                                            if pd.isnull(d["PERFORMANCE_AT_OFFERED_DATE"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Offered date is missing" )
                                            else:
                                                 status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Offered date formate is not correct" )
                                            
                                            continue    

                                        if pd.isnull(d["PERFORMANCE_AT_OFFERED_REMARKS"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Offered remark is missing" )
                                                continue
                                        else:
                                              obj.PERFORMANCE_AT_OFFERED_REMARKS=d["PERFORMANCE_AT_OFFERED_REMARKS"]  
                                              lis_kpi_status_bandwise=d["PERFORMANCE_AT_OFFERED_REMARKS"].split(",")
                                              di={}
                                              sts=True
                                              for band_status in lis_kpi_status_bandwise:
                                                    if("_" in band_status):
                                                            lis=band_status.split("_")
                                                            di[lis[0]] = lis[1]
                                                    else:
                                                        status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Band and status should be separated by a '_' in the PERFORMANCE_AT_OFFERED_REMARKS " )
                                                        sts=False
                                                        break
                                              if sts==False:
                                                continue
                                                    
                                              for  kpi_obj in kpi_objs:
                                                    if kpi_obj.band in di.keys():
                                                        kpi_obj.Performance_AT_Status=di[str(kpi_obj.band)] 
                                                        print(di[str(kpi_obj.band)], kpi_obj.band)
                                                        kpi_obj.save()
                                              print(di)
                                        obj.PERFORMANCE_AT_ACCEPTANCE_DATE=None
                                       
                                        obj.PERFORMANCE_AT_REJECTION_DATE = None
                                        obj.PERFORMANCE_AT_REJECTION_REASON=""
                                        
                                        
                                        obj.PERFORMANCE_AT_PENDING_REASON= ""
                                        obj.PERFORMANCE_AT_PENDING_REMARK= ""
                                        obj.PERFORMANCE_AT_PENDING_TAT_DATE= None

                                if d["Performance_AT_Status"] == "PENDING":
                                        print("inside PENDING update")
                                        obj.Performance_AT_Status=d["Performance_AT_Status"]
                                        if pd.isnull(d["PERFORMANCE_AT_PENDING_REASON"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Pending Reason is missing" )
                                                continue
                                        else:
                                              obj.PERFORMANCE_AT_PENDING_REASON=d["PERFORMANCE_AT_PENDING_REASON"] 

                                        if pd.isnull(d["PERFORMANCE_AT_PENDING_REMARK"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Pending Remark is missing" )
                                                continue
                                        else:
                                              obj.PERFORMANCE_AT_PENDING_REMARK=d["PERFORMANCE_AT_PENDING_REMARK"]
                                              lis_kpi_status_bandwise=d["PERFORMANCE_AT_PENDING_REMARK"].split(",")
                                              di={}
                                              sts=True
                                              for band_status in lis_kpi_status_bandwise:
                                                    if("_" in band_status):
                                                            lis=band_status.split("_")
                                                            di[lis[0]] = lis[1]
                                                    else:
                                                        status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Band and status should be separated by a '_' in the PERFORMANCE_AT_PENDING_REMARK " )
                                                        sts=False
                                                        break
                                              if sts==False:
                                                continue
                                                    
                                              for  kpi_obj in kpi_objs:
                                                    if kpi_obj.band in di.keys():
                                                        kpi_obj.Performance_AT_Status=di[str(kpi_obj.band)] 
                                                        print(di[str(kpi_obj.band)], kpi_obj.band)
                                                        kpi_obj.save()
                                              print(di)
                                        
                                        
                                        if not pd.isnull(d["PERFORMANCE_AT_PENDING_TAT_DATE"]) and  isinstance(d["PERFORMANCE_AT_PENDING_TAT_DATE"], datetime.datetime):
                                            obj.PERFORMANCE_AT_PENDING_TAT_DATE=d["PERFORMANCE_AT_PENDING_TAT_DATE"]
                                            print("updated")
                                        else:
                                            if pd.isnull(d["PERFORMANCE_AT_PENDING_TAT_DATE"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Pending TAT date is missing" )
                                            else:
                                                 status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Pending TAT formate is not correct" )
                                           
                                            continue   
                                        obj.PERFORMANCE_AT_ACCEPTANCE_DATE=None
                                        obj.PERFORMANCE_AT_REJECTION_DATE = None
                                        obj.PERFORMANCE_AT_REJECTION_REASON=""
                                        obj.PERFORMANCE_AT_OFFERED_DATE= None
                                        obj.PERFORMANCE_AT_OFFERED_REMARKS= ""

                            else:
                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Getting Performance At Status Other than ACCEPTED/REJECTED/PENDING/OFFERED" ) 
                                continue
    
                            obj.save()
                            print(d["Unique_SITE_ID"], " updated")
                            status_obj=DPR_update_status.objects.create(id=pk, update_status="UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Updated Succesfully")
                           
                else:
                    status_objs=DPR_update_status.objects.all()
                    ser=ser_DPR_update_status(status_objs,many=True)
                    context={"status_obj":ser.data, "status":True}
                    return Response(context)
            else:
                context={"status":False,"message":"DPR Report is empty"}
                return Response(context)

@api_view(["GET"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def get_dpr_temp(request):
    path="/media/dpr/dpr_templates/DPR_TEMP.xlsx"
    return Response({"path":path})

@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def dpr_site_list(request):
    
    if "id search" in request.GET:
        search=request.GET["id search"]
        # obj=DPR_table1.objects.filter(SITE_ID__icontains = search)
        obj=DPR_table1.objects.filter(SITE_ID__iexact = search)
    elif "circle search" in request.GET:
        search=request.GET["circle search"]
        # obj=DPR_table1.objects.filter(SITE_ID__icontains = search)
        obj=DPR_table1.objects.filter(CIRCLE__iexact = search)
    
    elif "activity search" in request.GET:
        search=request.GET["activity search"]
        # obj=DPR_table1.objects.filter(SITE_ID__icontains = search)
        obj=DPR_table1.objects.filter(Activity__iexact = search)
    
    elif "project search" in request.GET:
        search=request.GET["project search"]
        # obj=DPR_table1.objects.filter(SITE_ID__icontains = search)
        obj=DPR_table1.objects.filter(Project__iexact = search)

    else:
        obj=DPR_table1.objects.all()
    
    ser=serializer_DPR_table1(obj,many=True)
    return Response({"messages":"TRUE","data":ser.data})

@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def single_site_view(request,pk):
    object=DPR_table1.objects.get(id=pk)
    kpi_objs=performance_at_table.objects.filter(key=object)
    Band_status_ser=ser_performance_at_table(kpi_objs,many=True)
    bands=object.BAND
    band_list=bands.split("_")
    ser=serializer_DPR_table1_all(object,many=False)
    context={"data":ser.data,"band_list":band_list,"band_status":Band_status_ser.data}
    return Response(context) 

@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def soft_at_update(request,pk,at_status):
    ins=DPR_table1.objects.get(id=pk)
    try:
        # data=FileUploadParser.parse(request)
        data=request.data
        print("data........",data)
        if at_status=="ACCEPTED":

                    print("inside accepted")

                    serializer= ser_soft_at_acceptance(ins, data=data, partial=True)
                    if serializer.is_valid():
                        print("inside validation")
                        serializer.save()
                        print("saved data")
                        print(serializer.data)
                    
                       
                        ins.Soft_AT_Status=at_status
                        ins.SOFT_AT_REJECTION_DATE = None
                        ins.SOFT_AT_REJECTION_REASON= ""
                        # ins.SOFT_AT_REJECTED_TAT_DATE= None
                        ins.SOFT_AT_OFFERED_DATE= None
                        ins.SOFT_AT_OFFERED_REMARKS= ""
                        ins.SOFT_AT_PENDING_REASON= ""
                        ins.SOFT_AT_PENDING_REMARK= ""
                        ins.SOFT_AT_PENDING_TAT_DATE= None
                        ins.save()
                        
                        return Response({
                        "status":True,
                        "message":"Status updated successfully",
                        "data":serializer.data,    
                        })
                    else:
                        return Response({
                        "status":False,
                        "message":"data is in invalid format",
                        "data":serializer.data,
                         })
               
           
                
        if at_status=="REJECTED":
                print("inside Rejected")
                
                serializer= ser_soft_at_rejection(ins,data=data, partial=True)
                if serializer.is_valid():
                    print("inside validation")
                    serializer.save()
                    print("saved data")
                    print(serializer.data)
                    ins.Soft_AT_Status=at_status

                    ins.SOFT_AT_ACCEPTANCE_DATE=None
                    ins.SOFT_AT_ACCEPTANCE_MAIL=""
                    
                    ins.SOFT_AT_OFFERED_DATE= None
                    ins.SOFT_AT_OFFERED_REMARKS= ""
                    ins.SOFT_AT_PENDING_REASON= ""
                    ins.SOFT_AT_PENDING_REMARK= ""
                    ins.SOFT_AT_PENDING_TAT_DATE= None
                    ins.save()
                 
                    
                    return Response({
                    "status":True,
                    "message":"Status updated successfully",
                    "data":serializer.data,    
                    })
                else:
                    return Response({
                    "status":False,
                    "message":"failed,something went wrong",
                    "data":serializer.data,
                        })
        if at_status=="OFFERED":
                
                print("inside offered")
                serializer= ser_soft_at_offered(ins,data=data, partial=True)
                if serializer.is_valid():
                    print("inside validation")
                    serializer.save()
                    print("saved data")
                    print(serializer.data)

                    ins.Soft_AT_Status=at_status
                    ins.SOFT_AT_ACCEPTANCE_DATE=None
                    ins.SOFT_AT_ACCEPTANCE_MAIL=""
                    ins.SOFT_AT_REJECTION_DATE = None
                    ins.SOFT_AT_REJECTION_REASON=""
                    # ins.SOFT_AT_REJECTED_TAT_DATE= None
                    
                    ins.SOFT_AT_PENDING_REASON= ""
                    ins.SOFT_AT_PENDING_REMARK= ""
                    ins.SOFT_AT_PENDING_TAT_DATE= None
                    
                    ins.save()
                  
                    
                   
                    return Response({
                        "status":True,
                        "message":"Status updated successfully",
                        "data":serializer.data,    
                        })
                else:
                        return Response({
                        "status":False,
                        "message":"data is in invalid format",
                        "data":serializer.data,
                         })
        
        if at_status=="PENDING":
                print("inside offered")
            
                serializer= ser_soft_at_pending(ins,data=data, partial=True)
                if serializer.is_valid():
                    print("inside validation")
                    serializer.save()
                    print("saved data")
                    print(serializer.data)
                    ins.Soft_AT_Status=at_status
                    ins.SOFT_AT_ACCEPTANCE_DATE=None
                    ins.SOFT_AT_ACCEPTANCE_MAIL=""
                    ins.SOFT_AT_REJECTION_DATE = None
                    ins.SOFT_AT_REJECTION_REASON=""
                    # ins.SOFT_AT_REJECTED_TAT_DATE= None
                    ins.SOFT_AT_OFFERED_DATE= None
                    ins.SOFT_AT_OFFERED_REMARKS= ""
                    ins.save()

                    return Response({
                        "status":True,
                        "message":"Status updated successfully",
                        "data":serializer.data,    
                        })
                else:
                        return Response({
                        "status":False,
                        "message":"data is in invalid format",
                        "data":serializer.data,
                         })

    except:
           
        return Response({
            "status":False,
            "message":"failed,data inapropriate wrong",
            "data":serializer.data,    
            })

@api_view(['POST'])       
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def physical_at_update(request,pk,at_status):
    ins=DPR_table1.objects.get(id=pk)
    try:
        data=request.data
        print("data........",data)   
        if at_status=="ACCEPTED":

            
                    print("inside accepted")

                    serializer= ser_physical_at_acceptance(ins, data=data, partial=True)
                    if serializer.is_valid():
                        print("inside validation")
                        serializer.save()
                        print("saved data")
                        print(serializer.data)
                
               
                        ins.PHYSICAL_AT_Status = at_status
                        
                        ins.PHYSICAL_AT_REJECTION_DATE = None
                        ins.PHYSICAL_AT_REJECTION_REASON =""
                        # ins.PHYSICAL_AT_REJECTED_TAT_DATE=None
                        ins.PHYSICAL_AT_OFFERED_DATE= None
                        ins.PHYSICAL_AT_OFFERED_REMARKS=""
                        ins.PHYSICAL_AT_PENDING_REASON= ""
                        ins.PHYSICAL_AT_PENDING_REMARK= ""
                        ins.PHYSICAL_AT_PENDING_TAT_DATE=None
                        ins.save()
                        
                        
                        return Response({
                        "status":True,
                        "message":"Status updated successfully",
                        "data":serializer.data,    
                        })
                    else:
                        return Response({
                        "status":False,
                        "message":"data is in invalid format",
                        "data":serializer.data,
                         })
                     
                    
                    
                
        if at_status=="REJECTED":
                    print("inside rejected")
                    serializer= ser_physical_at_rejection(ins, data=data, partial=True)
                    if serializer.is_valid():
                        print("inside validation")
                        serializer.save()
                        print("saved data")
                        print(serializer.data)
            
                
                
                        ins.PHYSICAL_AT_Status=at_status
                        ins.PHYSICAL_AT_ACCEPTANCE_DATE=None
                        ins.PHYSICAL_AT_ACCEPTANCE_MAIL=""
                        ins.PHYSICAL_AT_OFFERED_DATE= None
                        ins.PHYSICAL_AT_OFFERED_REMARKS= ""
                        ins.PHYSICAL_AT_PENDING_REASON= ""
                        ins.PHYSICAL_AT_PENDING_REMARK= ""
                        ins.PHYSICAL_AT_PENDING_TAT_DATE= None
                        ins.save()

                        return Response({
                        "status":True,
                        "message":"Status updated successfully",
                        "data":serializer.data,    
                        })
                    else:
                        return Response({
                        "status":False,
                        "message":"data is in invalid format",
                        "data":serializer.data,
                         })

                        
                        
                    
                  
        if at_status=="OFFERED":
                   
                    print("inside offered")
                    serializer= ser_physical_at_offered(ins, data=data, partial=True)
                    if serializer.is_valid():
                        print("inside validation")
                        serializer.save()
                        print("saved data")
                        print(serializer.data)
                        ins.PHYSICAL_AT_Status=at_status
                        
                        ins.PHYSICAL_AT_ACCEPTANCE_DATE=None
                        ins.PHYSICAL_AT_ACCEPTANCE_MAIL=""
                        
                        ins.PHYSICAL_AT_REJECTION_DATE = None
                        ins.PHYSICAL_AT_REJECTION_REASON = ""
                        # ins.PHYSICAL_AT_REJECTED_TAT_DATE= None
                        
                        ins.PHYSICAL_AT_PENDING_REASON= ""
                        ins.PHYSICAL_AT_PENDING_REMARK= ""
                        ins.PHYSICAL_AT_PENDING_TAT_DATE= None
                        ins.save()
                        return Response({
                            "status":True,
                            "message":"Status updated successfully",
                            "data":serializer.data,    
                            })
                    else:
                        return Response({
                        "status":False,
                        "message":"data is in invalid format",
                        "data":serializer.data,
                         })
        if at_status=="PENDING":
                    print("inside pending")
                    serializer= ser_physical_at_pending(ins, data=data, partial=True)
                    if serializer.is_valid():
                        print("inside validation")
                        serializer.save()
                        print("saved data")
                        print(serializer.data)
            
                        ins.PHYSICAL_AT_Status=at_status
                        
                        ins.PHYSICAL_AT_ACCEPTANCE_DATE=None
                        ins.PHYSICAL_AT_ACCEPTANCE_MAIL=""
                        ins.PHYSICAL_AT_Status = at_status
                        ins.PHYSICAL_AT_REJECTION_DATE = None
                        ins.PHYSICAL_AT_REJECTION_REASON = ""
                        # ins.PHYSICAL_AT_REJECTED_TAT_DATE= None
                        ins.PHYSICAL_AT_OFFERED_DATE= None
                        ins.PHYSICAL_AT_OFFERED_REMARKS= ""
                    
                        ins.save()
                        return Response({
                                "status":True,
                                "message":"Status updated successfully",
                                "data":serializer.data,    
                                })
                    else:
                        return Response({
                        "status":False,
                        "message":"data is in invalid format",
                        "data":serializer.data,
                         })
                    

    except:
           
        return Response({
            "status":False,
            "message":"failed,data inapropriate wrong",
            "data":serializer.data,    
            })

def over_all_performance_at_status(pk):
            obj=DPR_table1.objects.get(id=pk)
            ins=performance_at_table.objects.filter(key=obj)
            reason=[]
            for ob in ins:
                if  (ob.Performance_AT_Status =='' or ob.Performance_AT_Status == None):
                    txt=str(ob.band) +"_" + "PENDING"
                    reason.append(txt)
                else:
                    txt=str(ob.band) + "_" + str(ob.Performance_AT_Status)
                    reason.append(txt)
            txt_reason= ",".join(reason)
            accepted_date_list=[]
            rejected_date_list=[]
            offered_date_list=[]

            accepted=False
            rejected=False
            pending=False
            offered=False
            for ob in ins:
               
                if not(ob.Performance_AT_Status ==''): 
                    if ob.Performance_AT_Status == "ACCEPTED":
                        accepted_date_list.append(ob.PERFORMANCE_AT_ACCEPTANCE_DATE)
                        accepted=True
                    
                    if ob.Performance_AT_Status == "REJECTED":
                        rejected_date_list.append(ob.PERFORMANCE_AT_REJECTION_DATE)
                        rejected=True
                       
                    
                    if ob.Performance_AT_Status == "OFFERED":
                        offered_date_list.append(ob.PERFORMANCE_AT_OFFERED_DATE)  
                        offered=True
                        
                    if ob.Performance_AT_Status == "PENDING":
                        pending=True
                       
                else:
                     last_status="PENDING"
                     pending=True
                     break 
           
            if accepted == True and rejected==False and offered==False:
                    obj.Performance_AT_Status="ACCEPTED"
                    obj.PERFORMANCE_AT_ACCEPTANCE_DATE=max(accepted_date_list)   
                   
                    obj.PERFORMANCE_AT_PENDING_REMARK=None
                    obj.PERFORMANCE_AT_PENDING_TAT_DATE=None  
                    obj.PERFORMANCE_AT_REJECTION_DATE = None
                    obj.PERFORMANCE_AT_REJECTION_REASON=""
                    obj.PERFORMANCE_AT_OFFERED_DATE= None
                    obj.PERFORMANCE_AT_OFFERED_REMARKS= ""                
            else:
                    obj.Performance_AT_Status="PENDING"
                    obj.PERFORMANCE_AT_PENDING_REMARK=txt_reason
                    obj.PERFORMANCE_AT_PENDING_TAT_DATE=datetime.datetime(2001,7,24)
                   
                    obj.PERFORMANCE_AT_ACCEPTANCE_DATE=None
                    obj.PERFORMANCE_AT_REJECTION_DATE = None
                    obj.PERFORMANCE_AT_REJECTION_REASON=""
                    obj.PERFORMANCE_AT_OFFERED_DATE= None
                    obj.PERFORMANCE_AT_OFFERED_REMARKS= ""

            # if pending == True:
            #         obj.Performance_AT_Status="PENDING"
                   
            #         obj.PERFORMANCE_AT_PENDING_REMARK=txt_reason
            #         obj.PERFORMANCE_AT_PENDING_TAT_DATE=datetime.datetime(2001,7,24)
                   
            #         obj.PERFORMANCE_AT_ACCEPTANCE_DATE=None
            #         obj.PERFORMANCE_AT_REJECTION_DATE = None
            #         obj.PERFORMANCE_AT_REJECTION_REASON=""
            #         obj.PERFORMANCE_AT_OFFERED_DATE= None
            #         obj.PERFORMANCE_AT_OFFERED_REMARKS= ""
            # else:

            #     if accepted == True and rejected==True and offered==True:
            #         obj.Performance_AT_Status="OFFERED"
            #         obj.PERFORMANCE_AT_OFFERED_DATE=max(offered_date_list)
            #         obj.PERFORMANCE_AT_OFFERED_REMARKS=txt_reason
                   
            #         obj.PERFORMANCE_AT_ACCEPTANCE_DATE=None
            #         obj.PERFORMANCE_AT_REJECTION_DATE = None
            #         obj.PERFORMANCE_AT_REJECTION_REASON=""
            #         obj.PERFORMANCE_AT_PENDING_REASON= ""
            #         obj.PERFORMANCE_AT_PENDING_REMARK= ""
            #         obj.PERFORMANCE_AT_PENDING_TAT_DATE=None
                
            #     if accepted == True and rejected==True and offered==False:
            #         obj.Performance_AT_Status="REJECTED"
            #         obj.PERFORMANCE_AT_REJECTION_DATE=max(rejected_date_list)
            #         obj.PERFORMANCE_AT_REJECTION_REASON=txt_reason     
            #         obj.PERFORMANCE_AT_ACCEPTANCE_DATE=None
            #         obj.PERFORMANCE_AT_OFFERED_DATE= None
            #         obj.PERFORMANCE_AT_OFFERED_REMARKS= ""
            #         obj.PERFORMANCE_AT_PENDING_REASON= ""
            #         obj.PERFORMANCE_AT_PENDING_REMARK= ""  
            #         obj.PERFORMANCE_AT_PENDING_TAT_DATE=None   
               
            #     if accepted == True and rejected==False and offered==False:
            #         obj.Performance_AT_Status="ACCEPTED"
            #         obj.PERFORMANCE_AT_ACCEPTANCE_DATE=max(accepted_date_list)   
                    
            #         obj.PERFORMANCE_AT_PENDING_REMARK=None
            #         obj.PERFORMANCE_AT_PENDING_TAT_DATE=None  
            #         obj.PERFORMANCE_AT_REJECTION_DATE = None
            #         obj.PERFORMANCE_AT_REJECTION_REASON=""
            #         obj.PERFORMANCE_AT_OFFERED_DATE= None
            #         obj.PERFORMANCE_AT_OFFERED_REMARKS= ""
                   
               
                
            #     if accepted == False and rejected==True and offered==True:
            #         obj.Performance_AT_Status="OFFERED"
            #         obj.PERFORMANCE_AT_OFFERED_DATE=max(offered_date_list)
            #         obj.PERFORMANCE_AT_OFFERED_REMARKS=txt_reason
                    
            #         obj.PERFORMANCE_AT_ACCEPTANCE_DATE=None
            #         obj.PERFORMANCE_AT_REJECTION_DATE = None
            #         obj.PERFORMANCE_AT_REJECTION_REASON=""
            #         obj.PERFORMANCE_AT_PENDING_REASON= ""
            #         obj.PERFORMANCE_AT_PENDING_REMARK= ""
            #         obj.PERFORMANCE_AT_PENDING_TAT_DATE=None

            #     if accepted == False and rejected==False and offered==True:
            #             obj.Performance_AT_Status="OFFERED"
            #             obj.PERFORMANCE_AT_OFFERED_DATE=max(offered_date_list)
            #             obj.PERFORMANCE_AT_OFFERED_REMARKS=txt_reason
                        
            #             obj.PERFORMANCE_AT_ACCEPTANCE_DATE=None
            #             obj.PERFORMANCE_AT_REJECTION_DATE = None
            #             obj.PERFORMANCE_AT_REJECTION_REASON=""
            #             obj.PERFORMANCE_AT_PENDING_REASON= ""
            #             obj.PERFORMANCE_AT_PENDING_REMARK= ""
            #             obj.PERFORMANCE_AT_PENDING_TAT_DATE=None

            #     if accepted == True and rejected==False and offered==True:
            #             obj.Performance_AT_Status="OFFERED"
            #             obj.PERFORMANCE_AT_OFFERED_DATE=max(offered_date_list)
            #             obj.PERFORMANCE_AT_OFFERED_REMARKS=txt_reason
                        
            #             obj.PERFORMANCE_AT_ACCEPTANCE_DATE=None
            #             obj.PERFORMANCE_AT_REJECTION_DATE = None
            #             obj.PERFORMANCE_AT_REJECTION_REASON=""
            #             obj.PERFORMANCE_AT_PENDING_REASON= ""
            #             obj.PERFORMANCE_AT_PENDING_REMARK= ""

            #     if accepted == False and rejected==True and offered==False:

            #             obj.Performance_AT_Status="REJECTED"
            #             obj.PERFORMANCE_AT_REJECTION_DATE=max(rejected_date_list)
            #             obj.PERFORMANCE_AT_REJECTION_REASON=txt_reason
                        
            #             obj.PERFORMANCE_AT_ACCEPTANCE_DATE=None
            #             obj.PERFORMANCE_AT_OFFERED_DATE= None
            #             obj.PERFORMANCE_AT_OFFERED_REMARKS= ""
            #             obj.PERFORMANCE_AT_PENDING_REASON= ""
            #             obj.PERFORMANCE_AT_PENDING_REMARK= ""

            
           
            obj.save()

@api_view(["POST"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def performance_at_update(request,pk,at_status,band):
    obj=DPR_table1.objects.get(id=pk)
    ins=performance_at_table.objects.get(key=obj,band=band)
    try:
   
        data=request.data
        print("data........",data) 
        if at_status=="ACCEPTED":
                    print("inside ACCEPTED")
                    serializer= ser_performance_at_acceptance(ins, data=data, partial=True)
                    if serializer.is_valid():
                        print("inside validation")
                        serializer.save()
                        print("saved data")
                        print(serializer.data)

                        ins.Performance_AT_Status=at_status
                        ins.PERFORMANCE_AT_REJECTION_DATE = None
                        ins.PERFORMANCE_AT_REJECTION_REASON=""
                        ins.PERFORMANCE_AT_OFFERED_DATE= None
                        ins.PERFORMANCE_AT_OFFERED_REMARKS= ""
                        ins.PERFORMANCE_AT_PENDING_REASON= ""
                        ins.PERFORMANCE_AT_PENDING_REMARK= ""
                        ins.save()
                    
                        over_all_performance_at_status(pk)
                        return Response({
                                        "status":True,
                                        "message":"Status updated successfully",
                                        "data":serializer.data, 
                                        "band":band   
                                        })
                    else:
                        return Response({
                        "status":False,
                        "message":"data is in invalid format",
                        "data":serializer.data,
                        "band":band
                         })
                    
            
            
                
        if at_status=="REJECTED":
                    print("inside performance Rejected")
                    serializer= ser_performance_at_rejection(ins, data=data, partial=True)
                    if serializer.is_valid():
                        print("inside validation")
                        serializer.save()
                        print("saved data")
                        print(serializer.data)
           
                        ins.Performance_AT_Status=at_status
                        ins.PERFORMANCE_AT_ACCEPTANCE_DATE=None
                        ins.PERFORMANCE_AT_OFFERED_DATE= None
                        ins.PERFORMANCE_AT_OFFERED_REMARKS= ""
                        ins.PERFORMANCE_AT_PENDING_REASON= ""
                        ins.PERFORMANCE_AT_PENDING_REMARK= ""
                        ins.save()
                    
                        over_all_performance_at_status(pk)
                        return Response({
                                        "status":True,
                                        "message":"Status updated successfully",
                                        "data":serializer.data, 
                                        "band":band   
                                        })
                    else:
                        return Response({
                        "status":False,
                        "message":"data is in invalid format",
                        "data":serializer.data,
                        "band":band
                         })
                  
        if at_status=="OFFERED":
                    print("inside performance Rejected")
                    serializer= ser_performance_at_offered(ins, data=data, partial=True)
                    if serializer.is_valid():
                        print("inside validation")
                        serializer.save()
                        print("saved data")
                        print(serializer.data)
           
           
                        ins.Performance_AT_Status=at_status
                        ins.PERFORMANCE_AT_ACCEPTANCE_DATE=None
                        ins.PERFORMANCE_AT_REJECTION_DATE = None
                        ins.PERFORMANCE_AT_REJECTION_REASON=""
                        ins.PERFORMANCE_AT_PENDING_REASON= ""
                        ins.PERFORMANCE_AT_PENDING_REMARK= ""
                 
                        ins.save()
                   
                        over_all_performance_at_status(pk)
                        return Response({
                                        "status":True,
                                        "message":"Status updated successfully",
                                        "data":serializer.data, 
                                        "band":band   
                                        })
                    else:
                        return Response({
                        "status":False,
                        "message":"data is in invalid format",
                        "data":serializer.data,
                        "band":band
                         })
                  
        if at_status=="PENDING":
                    print("inside performance Rejected")
                    serializer= ser_performance_at_pending(ins, data=data, partial=True)
                    if serializer.is_valid():
                        print("inside validation")
                        serializer.save()
                        print("saved data")
                        print(serializer.data)
            
            
                        ins.Performance_AT_Status=at_status

                        ins.PERFORMANCE_AT_ACCEPTANCE_DATE=None
                        ins.PERFORMANCE_AT_REJECTION_DATE = None
                        ins.PERFORMANCE_AT_REJECTION_REASON=""
                        ins.PERFORMANCE_AT_OFFERED_DATE= None
                        ins.PERFORMANCE_AT_OFFERED_REMARKS= ""
                    
                        ins.save()
                    
                        over_all_performance_at_status(pk)
                        return Response({
                                        "status":True,
                                        "message":"Status updated successfully",
                                        "data":serializer.data, 
                                        "band":band   
                                        })
                    else:
                        return Response({
                        "status":False,
                        "message":"data is in invalid format",
                        "data":serializer.data,
                        "band":band
                         })
                   
    except:
           
        return Response({
            "status":False,
            "message":"failed,data inapropriate wrong",
            "data":serializer.data,  
            "band":band,  
            })

@api_view(["PATCH"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def performance_at_tat_date(request,pk):
    obj=DPR_table1.objects.get(pk=pk)
    obj.PERFORMANCE_AT_PENDING_TAT_DATE=request.POST.get("tat_date")
    obj.save()
 
    return Response({"status":True,"tat_date":request.POST.get("tat_date")})
    

@api_view(["GET"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def dpr_view(request,circle):
           
            if not (circle == "ALL"):
                objs=DPR_table1.objects.filter(CIRCLE=circle)

            else:
                 objs=DPR_table1.objects.all()
            

            if "id search" in request.GET:
                    search=request.GET["id search"]
                    # obj=DPR_table1.objects.filter(SITE_ID__icontains = search)
                    objs=objs.filter(SITE_ID__iexact = search)
            if "MS2 filter" in request.GET:
                    objs= objs.filter( Soft_AT_Status="ACCEPTED").filter(Performance_AT_Status="ACCEPTED").filter(PHYSICAL_AT_Status="ACCEPTED")
                    
                    
                          
           
            path="media/dpr/dpr_excel/excel.xlsx"
            pd.DataFrame(list(objs.values())).to_excel(path,index=False)
            ser=serializer_DPR_table1_all(objs,many=True)
            context={"data":ser.data,"circle":circle,"path":path}
           
            return Response(context)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def all_dashboard(request):
    obj=DPR_table1.objects.all()
    ms2_site=0
    only_soft_at_done=0
    only_physical_at_done=0
    only_performance_at_done=0
    for o in obj:
            if o.Soft_AT_Status=="ACCEPTED" and o.Performance_AT_Status=="ACCEPTED" and o.PHYSICAL_AT_Status=="ACCEPTED":
                ms2_site=ms2_site+1
            if o.Soft_AT_Status=="ACCEPTED" and o.Performance_AT_Status!="ACCEPTED" and o.PHYSICAL_AT_Status!="ACCEPTED":
                only_soft_at_done=only_soft_at_done+1
            if o.Soft_AT_Status!="ACCEPTED" and o.Performance_AT_Status=="ACCEPTED" and o.PHYSICAL_AT_Status!="ACCEPTED":
                only_performance_at_done=only_performance_at_done+1
            if o.Soft_AT_Status!="ACCEPTED" and o.Performance_AT_Status!="ACCEPTED" and o.PHYSICAL_AT_Status=="ACCEPTED":
                only_physical_at_done=only_physical_at_done+1
    total_no_site=len(DPR_table1.objects.all())

    total_soft_at_done_objs=DPR_table1.objects.filter(Soft_AT_Status="ACCEPTED")
    total_soft_at_done=len( total_soft_at_done_objs)

    
    total_physical_at_done_objs=DPR_table1.objects.filter(PHYSICAL_AT_Status="ACCEPTED")
    total_physical_at_done=len( total_physical_at_done_objs)

    
    total_performance_at_done_objs=DPR_table1.objects.filter(Performance_AT_Status="ACCEPTED")
    total_performance_at_done=len( total_performance_at_done_objs)

    total_mapa=len(obj.filter(MAPA_STATUS="OK"))
    if total_no_site > 0 :
        percent_soft_at_done=round((total_soft_at_done/total_no_site)*100,2)
        percent_physical_at_done=round((total_physical_at_done/total_no_site)*100,2)
        percent_performance_at_done=round((total_performance_at_done/total_no_site)*100,2)
    else:
        percent_soft_at_done=0
        percent_physical_at_done=0
        percent_performance_at_done=0
    if ms2_site>0:
        percent_ms2_site=round((ms2_site/total_no_site)*100,2)

    else:
        percent_ms2_site=0
    context={   "total_soft_at_done":total_soft_at_done,
                "total_performance_at_done":total_performance_at_done,
                "total_physical_at_done": total_physical_at_done,
                "percent_soft_at_done":percent_soft_at_done,
                "percent_physical_at_done":percent_physical_at_done,
                "percent_performance_at_done":percent_performance_at_done,
                "total_no_site":total_no_site,
                "Ms2_site":ms2_site,
                "percent_ms2_site": percent_ms2_site,
                "total_mapa":total_mapa,
                "only_soft_at_done":only_soft_at_done,
                "only_physical_at_done":only_physical_at_done,
                "only_performance_at_done":only_performance_at_done,
                
               

                
            }
    
    # return render(request, 'trend/DPR_dashboard.html',context)
    return Response(context)

@api_view(["GET"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def circle_wise_dashboard(request):
    
    
    if "project" in request.GET:
        project=request.GET["project"]
        objects=DPR_table1.objects.filter(Project__iexact=project)
        circles=circle_list(objects)
        
    else:
        objects=DPR_table1.objects.all()
        circles=circle_list(objects)
        
    # data={}
    li=[]
    for circle in circles:
        ms2_site=0
        obj=objects.filter(CIRCLE__iexact = circle)
        for o in obj:
            if o.Soft_AT_Status=="ACCEPTED" and o.Performance_AT_Status=="ACCEPTED" and o.PHYSICAL_AT_Status=="ACCEPTED":
                ms2_site=ms2_site+1
        total_ms1_site=len(obj)
        total_soft_at_done=len(obj.filter(Soft_AT_Status="ACCEPTED"))
        total_physical_at_done=len(obj.filter(PHYSICAL_AT_Status="ACCEPTED"))
        total_performance_at_done=len(obj.filter(Performance_AT_Status="ACCEPTED"))
        total_mapa=len(obj.filter(MAPA_STATUS="OK"))
        
        if  total_ms1_site > 0 :
            percent_soft_at_done=round((total_soft_at_done/total_ms1_site)*100,2)
            percent_physical_at_done=round((total_physical_at_done/total_ms1_site)*100,2)
            percent_performance_at_done=round((total_performance_at_done/total_ms1_site)*100,2)
        else:
            percent_soft_at_done=0
            percent_physical_at_done=0
            percent_performance_at_done=0
        
        if ms2_site>0:
            percent_ms2_site=round((ms2_site/total_ms1_site)*100,2)

        else:
            percent_ms2_site=0
        data={ "circle":circle,
                    "total_ms1_site" :total_ms1_site, 
                    "total_soft_at_done" : total_soft_at_done,
                    "total_physical_at_done":  total_physical_at_done,
                    "total_performance_at_done" : total_performance_at_done,
                    "percent_soft_at_done" :percent_soft_at_done,
                    "percent_physical_at_done" :percent_physical_at_done,
                    'percent_performance_at_done' :percent_performance_at_done,
                    "Total_ms2_site":ms2_site,
                    "percent_ms2_site":percent_ms2_site,
                    "total_mapa":total_mapa,
                    }
        li.append(data)
    context={"data":li}
    # return render(request,"trend/circle_wise_dashboard.html",context)
    return Response(context)

@api_view(["POST"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def mapa_status_upld(request):
            DPR_update_status.objects.all().delete()
    
            DPR_file.objects.all().delete()
            file=request.FILES["MAPA_file"]
            obj=DPR_file.objects.create(dpr_file=file)
            path=str(obj.dpr_file)
            print(path)
            df=pd.read_excel("media/"+path)
            print(df)
            # del_obj=[]
            if not(df.empty):
                
                for i,d in df.iterrows():
                   
                            pk=str(d["CIRCLE"])+str(d["Unique_SITE_ID"])+str(d["BAND"])+str(d["TOCO_NAME"])+str(d["Project"])+str(d["Activity"])
                            try:
                                objs=DPR_table1.objects.get(id=pk)
                                
                            except:
                                    status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="site not found in database" )
                                    
                                    continue
                            if d["Soft_AT_Status"]=="ACCEPTED" and d["Performance_AT_Status"]== "ACCEPTED" and d["PHYSICAL_AT_Status"]=="ACCEPTED" :
                                    objs.MAPA_STATUS=d["MAPA_STATUS"]
                                    print("updating #######################################")
                                    objs.save()
                                    status_obj=DPR_update_status.objects.create(id=pk, update_status="UPDATED",SITE_ID=d["Unique_SITE_ID"] )
                                    messages.success(request,"MAPA_uploaded Succefully")
                            else:
                                  status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="All status are not accepted" )
                                  continue

                else:
                    status_objs=DPR_update_status.objects.all()
                    ser=ser_DPR_update_status(status_objs,many=True)
                    context={"status":True,"status_obj":ser.data}
                    return Response(context)
            else: 
                context={"status":False,"message":"uploaded file is empty"} 
                return Response(context)

@api_view(["POST"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def mapa_single_site_update(request,pk):
        obj=DPR_table1.objects.get(pk=pk)
        
        if 'MAPA' in request.POST:
            if request.POST.get("MAPA")=="OK":
                if obj.Performance_AT_Status=="ACCEPTED" and obj.Soft_AT_Status=="ACCEPTED" and obj.PHYSICAL_AT_Status=="ACCEPTED":
                    obj.MAPA_STATUS=request.POST.get("MAPA")
                    obj.save()
                    # messages.success(request,"MAPA updated Succesfully")
                    message="MAPA updated Succesfully"
                    status=True
                else:
                    messages.error(request,"ALL STATUS are not ACCEPTED")
                    message="ALL STATUS are not ACCEPTED"
                    status=False
            if request.POST.get("MAPA")=="NOT OK":  
                    obj.MAPA_STATUS=request.POST.get("MAPA")
                    obj.save()
                    message="MAPA updated Succesfully"
                    status=True
        else:
            message="MAPA Status required field"
            status=False

        return Response({"message": message,"status":status})
       



@api_view(["GET"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def MasterDashboard(request):
    all_objs=DPR_table1.objects.all()
    cir_list=circle_list(all_objs)
    data={}
    for cir in cir_list:
        print(cir)
        project_list=["NEW_TOWER","Relocation","ULS","Upgrade"]
        project_dict={}
        for project in project_list:
           
            objs=DPR_table1.objects.filter(CIRCLE=cir,Project=project)
            RFAI_Done = objs.exclude(RFAI_DATE__isnull=True).count()
            MS1_Pendency = objs.filter( OA_COMMERCIAL_TRAFFIC_PUT_ON_AIR_MS1_DATE__isnull=True ).count()
            MS1_done= objs.exclude( OA_COMMERCIAL_TRAFFIC_PUT_ON_AIR_MS1_DATE__isnull=True).count()
            MS2_Pendency = objs.filter( MAPA_INCLUSION_DATE__isnull=True ).count()
            MS2_done = objs.exclude(MAPA_INCLUSION_DATE__isnull=True ).count()
            MS1_0_15 = objs.filter(Internal_RFAI_Vs_Ms1_In_Days="0-15").count()
            MS1_16_30 = objs.filter(Internal_RFAI_Vs_Ms1_In_Days="16-30").count()
            MS1_31_60 = objs.filter(Internal_RFAI_Vs_Ms1_In_Days="31-60").count()
            MS1_61_90 = objs.filter(Internal_RFAI_Vs_Ms1_In_Days="61-90").count()
            MS1_GT90 = objs.filter(Internal_RFAI_Vs_Ms1_In_Days="GT90").count()
           
            MS2_0_15 = objs.filter(Internal_Ms1_Vs_Ms2_In_days="0-15").count()
            MS2_16_30 = objs.filter(Internal_Ms1_Vs_Ms2_In_days="16-30").count()
            MS2_31_60 = objs.filter(Internal_Ms1_Vs_Ms2_In_days="31-60").count()
            MS2_61_90 = objs.filter(Internal_Ms1_Vs_Ms2_In_days="61-90").count()
            MS2_GT90 = objs.filter(Internal_Ms1_Vs_Ms2_In_days="GT90").count()
            
            project_dict[project]={"RFAI_Done":RFAI_Done,
                                    "MS1_Done":MS1_done,
                                     "MS1_Pendency":MS1_Pendency,
                                     "MS2_Done":MS2_done,
                                     "MS2_Pendency":MS2_Pendency,
                                    "MS1_0_15":MS1_0_15,
                                    "MS1_16_30": MS1_16_30,
                                    "MS1_31_60":MS1_31_60,
                                    "MS1_61_90":MS1_61_90,
                                    "MS1_GT90":MS1_GT90,
                                    "MS2_0_15":MS2_0_15,
                                    "MS2_16_30":MS2_16_30,
                                    "MS2_31_60":MS2_31_60,
                                    "MS2_61_90":MS2_61_90,
                                    "MS2_GT90":MS2_GT90,

                                  }
        data[cir]=project_dict
            
    print(data)
    return Response(data)



@api_view(["POST"])
def dpr_report_upload(request):

    DPR_update_status.objects.all().delete()
    file=request.FILES["myfile"] #required
    soft_at=request.FILES["soft_at"] #required
    physical_at=request.FILES["physical_at"] #required
    G1800=request.FILES.get("G1800",None)
    L900=request.FILES.get("L900",None)
    L1800=request.FILES.get("L1800",None)
    L2300=request.FILES.get("L2300",None)
    L2100=request.FILES.get("L2100",None)
   

    file = request.FILES["myfile"] if 'myfile' in request.FILES else None
    if file:
            location=MEDIA_ROOT + r"\dpr\dpr_report_file"
            fs = FileSystemStorage(location=location)
            file = fs.save(file.name, file)
            # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
            filepath = fs.path(file)
            print("file_path:-",filepath)
            df=pd.read_excel(filepath)
            os.remove(path=filepath)
            print(filepath,"deleted...............")
            print(df)
 
            
            del_obj=[]
            if not(df.empty):
                for i,d in df.iterrows():
                   
                            pk=str(d["CIRCLE"])+str(d["Unique_SITE_ID"])+str(d["BAND"])+str(d["TOCO_NAME"])+str(d["Project"])+str(d["Activity"])
                            try:
                                rfai_date= d["RFAI_DATE"] if not(pd.isnull(d["RFAI_DATE"])) else None
                                oa_date= d["OA_(COMMERCIAL_TRAFFIC_PUT_ON_AIR)_(MS1)_DATE"] if not(pd.isnull(d["OA_(COMMERCIAL_TRAFFIC_PUT_ON_AIR)_(MS1)_DATE"])) else None
                                # oa_date= d["OA_COMMERCIAL_TRAFFIC_PUT_ON_AIR_MS1_DATE"] if not(pd.isnull(d["OA_COMMERCIAL_TRAFFIC_PUT_ON_AIR_MS1_DATE"])) else None
                                mapa_date= d["MAPA_INCLUSION_DATE"] if not(pd.isnull(d["MAPA_INCLUSION_DATE"])) else None
                                obj=DPR_table1.objects.create(id=pk,
                                                SITE_ID=str(d["SITE_ID"]),
                                                CIRCLE=str(d["CIRCLE"]),
                                                Unique_SITE_ID=str(d["Unique_SITE_ID"]),
                                                BAND=str(d["BAND"]),
                                                TOCO_NAME=str(d["TOCO_NAME"]),
                                                Project=str(d["Project"]),
                                                Activity=str(d["Activity"]),
                                                RFAI_DATE=rfai_date,
                                                OA_COMMERCIAL_TRAFFIC_PUT_ON_AIR_MS1_DATE=oa_date,
                                                MAPA_INCLUSION_DATE=mapa_date,
                                                Internal_RFAI_Vs_Ms1_In_Days=str(d["Internal RFAI Vs Ms1-In Days"]),
                                                Internal_Ms1_Vs_Ms2_In_days=str(d["Internal Ms1 Vs Ms2-In days"]),
                                                )
                                bands=str(d["BAND"]).split("_")
                                print(bands)
                                for band in bands:
                                    performance_at_table.objects.create(key=obj,band=band)
                                
                                kpi_objs=performance_at_table.objects.get(key=obj)
        #                         if d["Soft_AT_Status"] == "ACCEPTED" or d["Soft_AT_Status"] == "REJECTED" or d["Soft_AT_Status"] == "OFFERED" or d["Soft_AT_Status"] == "PENDING":
                               
        #                             if d["Soft_AT_Status"] == "ACCEPTED":
        #                                     if obj.Soft_AT_Status == "ACCEPTED":
        #                                         status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Status Already accepted in the database" )
                                                
        #                                         continue
        #                                     else:
        #                                         obj.Soft_AT_Status=d["Soft_AT_Status"]
        #                                         if not pd.isnull(d["SOFT_AT_ACCEPTANCE_DATE"]) and  isinstance(d["SOFT_AT_ACCEPTANCE_DATE"], datetime.datetime):
        #                                             obj.SOFT_AT_ACCEPTANCE_DATE = d["SOFT_AT_ACCEPTANCE_DATE"]
                                                    
        #                                         else:
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at acceptance date is missing or date formate is not correct" ) 
        #                                             continue
        #                                         obj.SOFT_AT_ACCEPTANCE_MAIL=soft_at
        #                                         obj.SOFT_AT_REJECTION_DATE = None
        #                                         obj.SOFT_AT_REJECTION_REASON= ""
        #                                         obj.SOFT_AT_OFFERED_DATE= None
        #                                         obj.SOFT_AT_OFFERED_REMARKS= ""
        #                                         obj.SOFT_AT_PENDING_REASON= ""
        #                                         obj.SOFT_AT_PENDING_REMARK= ""
        #                                         obj.SOFT_AT_PENDING_TAT_DATE= None
                                                

        #                             if d["Soft_AT_Status"] == "REJECTED":
        #                                     print("inside REJECTED update")
                                            
        #                                     obj.Soft_AT_Status=d["Soft_AT_Status"]
        #                                     if not pd.isnull(d["SOFT_AT_REJECTION_DATE"]) and  isinstance(d["SOFT_AT_REJECTION_DATE"], datetime.datetime):
        #                                         obj.SOFT_AT_REJECTION_DATE = d["SOFT_AT_REJECTION_DATE"]
        #                                         print("updated")
        #                                     else:
        #                                         if pd.isnull(d["SOFT_AT_REJECTION_DATE"]):
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Rejection date is missing" )
        #                                         else:
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Rejection date formate is not correct" )
                                            
        #                                         continue    
        #                                     if pd.isnull(d["SOFT_AT_REJECTION_REASON"]):
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Rejection Reason is missing" )
        #                                             continue
        #                                     else:
        #                                         obj.SOFT_AT_REJECTION_REASON=d["SOFT_AT_REJECTION_REASON"]
                
        #                                     obj.SOFT_AT_ACCEPTANCE_DATE=None
        #                                     obj.SOFT_AT_ACCEPTANCE_MAIL="" 
        #                                     obj.SOFT_AT_OFFERED_DATE= None
        #                                     obj.SOFT_AT_OFFERED_REMARKS= ""
        #                                     obj.SOFT_AT_PENDING_REASON= ""
        #                                     obj.SOFT_AT_PENDING_REMARK= ""
        #                                     obj.SOFT_AT_PENDING_TAT_DATE= None   
                                                        

        #                             if d["Soft_AT_Status"] == "OFFERED":
        #                                     print("inside OFFERED update")
                                            
        #                                     obj.Soft_AT_Status=d["Soft_AT_Status"]
                                            
        #                                     if not pd.isnull(d["SOFT_AT_OFFERED_DATE"]) and  isinstance(d["SOFT_AT_OFFERED_DATE"], datetime.datetime):
        #                                         obj.SOFT_AT_OFFERED_DATE=d["SOFT_AT_OFFERED_DATE"]
        #                                         print("updated")
        #                                     else:
        #                                         if pd.isnull(d["SOFT_AT_OFFERED_DATE"]):
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Offered date is missing" )
        #                                         else:
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Offered date formate is not correct" ) 
        #                                         continue    

        #                                     if pd.isnull(d["SOFT_AT_OFFERED_REMARKS"]):
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Offered remark is missing" )
        #                                             continue
        #                                     else:
        #                                         obj.SOFT_AT_OFFERED_REMARKS=d["SOFT_AT_OFFERED_REMARKS"]  

        #                                     obj.SOFT_AT_ACCEPTANCE_DATE=None
        #                                     obj.SOFT_AT_ACCEPTANCE_MAIL=""
        #                                     obj.SOFT_AT_REJECTION_DATE = None
        #                                     obj.SOFT_AT_REJECTION_REASON=""
        #                                     obj.SOFT_AT_PENDING_REASON= ""
        #                                     obj.SOFT_AT_PENDING_REMARK= ""
        #                                     obj.SOFT_AT_PENDING_TAT_DATE= None
                                            
                                            
        #                             if d["Soft_AT_Status"] == "PENDING":
        #                                     print("inside PENDING update")
        #                                     obj.Soft_AT_Status=d["Soft_AT_Status"]
        #                                     if pd.isnull(d["SOFT_AT_PENDING_REASON"]):
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Pending Reason is missing" )
        #                                             continue
        #                                     else:
        #                                         obj.SOFT_AT_PENDING_REASON=d["SOFT_AT_PENDING_REASON"] 

        #                                     if pd.isnull(d["SOFT_AT_PENDING_REMARK"]):
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Pending Remark is missing" )
        #                                             continue
        #                                     else:
        #                                         obj.SOFT_AT_PENDING_REMARK=d["SOFT_AT_PENDING_REMARK"]
                                            
                                            
        #                                     if not pd.isnull(d["SOFT_AT_PENDING_TAT_DATE"]) and  isinstance(d["SOFT_AT_PENDING_TAT_DATE"], datetime.datetime):
        #                                         obj.SOFT_AT_PENDING_TAT_DATE=d["SOFT_AT_PENDING_TAT_DATE"]
        #                                         print("updated")
        #                                     else:
        #                                         if pd.isnull(d["SOFT_AT_PENDING_TAT_DATE"]):
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Pending TAT date is missing" )
        #                                         else:
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Pending TAT formate is not correct" )
        #                                         continue   
        #                                     obj.SOFT_AT_ACCEPTANCE_DATE=None
        #                                     obj.SOFT_AT_ACCEPTANCE_MAIL=""
        #                                     obj.SOFT_AT_REJECTION_DATE = None
        #                                     obj.SOFT_AT_REJECTION_REASON=""
        #                                     obj.SOFT_AT_OFFERED_DATE= None
        #                                     obj.SOFT_AT_OFFERED_REMARKS= ""
                                
        #                         else:
        #                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Getting Soft At Status Other than ACCEPTED/REJECTED/PENDING/OFFERED" )  
        #                             continue
                                
        # ########################################## PHYSICAL AT ############################################################################
                                
        #                         if d["PHYSICAL_AT_Status"] == "ACCEPTED" or d["PHYSICAL_AT_Status"] == "REJECTED" or d["PHYSICAL_AT_Status"] == "OFFERED" or d["PHYSICAL_AT_Status"] == "PENDING":
                                
        #                             if d["PHYSICAL_AT_Status"] == "ACCEPTED":
        #                                     if obj.PHYSICAL_AT_Status == "ACCEPTED":
        #                                         status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Status Already accepted in the database" )
        #                                         continue
        #                                     else:
        #                                         if not pd.isnull(d["PHYSICAL_AT_ACCEPTANCE_DATE"]) and  isinstance(d["PHYSICAL_AT_ACCEPTANCE_DATE"], datetime.datetime):
        #                                             obj.PHYSICAL_AT_ACCEPTANCE_DATE = d["PHYSICAL_AT_ACCEPTANCE_DATE"]
        #                                             obj.PHYSICAL_AT_Status=d["PHYSICAL_AT_Status"]
        #                                         else:
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at acceptance date is missing or date formate is not correct" )
        #                                             continue
        #                                         obj.PHYSICAL_AT_ACCEPTANCE_MAIL=physical_at
        #                                         obj.PHYSICAL_AT_REJECTION_DATE = None
        #                                         obj.PHYSICAL_AT_REJECTION_REASON= ""
        #                                         obj.PHYSICAL_AT_OFFERED_DATE= None
        #                                         obj.PHYSICAL_AT_OFFERED_REMARKS= ""
        #                                         obj.PHYSICAL_AT_PENDING_REASON= ""
        #                                         obj.PHYSICAL_AT_PENDING_REMARK= ""
        #                                         obj.PHYSICAL_AT_PENDING_TAT_DATE= None
                                            
                                                
                                    


        #                             if d["PHYSICAL_AT_Status"] == "REJECTED":
        #                                     print("inside REJECTED update")
        #                                     obj.PHYSICAL_AT_Status=d["PHYSICAL_AT_Status"]
                                            
        #                                     if not pd.isnull(d["PHYSICAL_AT_REJECTION_DATE"]) and  isinstance(d["PHYSICAL_AT_REJECTION_DATE"], datetime.datetime):
        #                                         obj.PHYSICAL_AT_REJECTION_DATE = d["PHYSICAL_AT_REJECTION_DATE"]
        #                                         print("updated")
                                            
        #                                     else:
        #                                         if pd.isnull(d["PHYSICAL_AT_REJECTION_DATE"]):
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Rejection date is missing" )
        #                                         else:
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Rejection date formate is not correct" )
        #                                         continue    
                                        
        #                                     if pd.isnull(d["PHYSICAL_AT_REJECTION_REASON"]):
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Rejection Reason is missing" )
        #                                             continue
        #                                     else:
        #                                         obj.PHYSICAL_AT_REJECTION_REASON=d["PHYSICAL_AT_REJECTION_REASON"]
                                                        
        #                                     obj.PHYSICAL_AT_ACCEPTANCE_DATE=None
        #                                     obj.PHYSICAL_AT_ACCEPTANCE_MAIL=""
        #                                     obj.PHYSICAL_AT_OFFERED_DATE= None
        #                                     obj.PHYSICAL_AT_OFFERED_REMARKS= ""
        #                                     obj.PHYSICAL_AT_PENDING_REASON= ""
        #                                     obj.PHYSICAL_AT_PENDING_REMARK= ""
        #                                     obj.PHYSICAL_AT_PENDING_TAT_DATE= None   
                                
                                
        #                             if d["PHYSICAL_AT_Status"] == "OFFERED":
        #                                     print("inside OFFERED update")
                                            
        #                                     obj.PHYSICAL_AT_Status=d["PHYSICAL_AT_Status"]
                                            
        #                                     if not pd.isnull(d["PHYSICAL_AT_OFFERED_DATE"]) and  isinstance(d["PHYSICAL_AT_OFFERED_DATE"], datetime.datetime):
        #                                         obj.PHYSICAL_AT_OFFERED_DATE=d["PHYSICAL_AT_OFFERED_DATE"]
        #                                         print("updated")
        #                                     else:
        #                                         if pd.isnull(d["PHYSICAL_AT_OFFERED_DATE"]):
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Offered date is missing" )
        #                                         else:
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Offered date formate is not correct" )
                                                
        #                                         continue    

        #                                     if pd.isnull(d["PHYSICAL_AT_OFFERED_REMARKS"]):
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Offered remark is missing" )
        #                                             continue
        #                                     else:
        #                                         obj.PHYSICAL_AT_OFFERED_REMARKS=d["PHYSICAL_AT_OFFERED_REMARKS"]  

        #                                     obj.PHYSICAL_AT_ACCEPTANCE_DATE=None
        #                                     obj.PHYSICAL_AT_ACCEPTANCE_MAIL=""
        #                                     obj.PHYSICAL_AT_REJECTION_DATE = None
        #                                     obj.PHYSICAL_AT_REJECTION_REASON=""
        #                                     obj.PHYSICAL_AT_PENDING_REASON= ""
        #                                     obj.PHYSICAL_AT_PENDING_REMARK= ""
        #                                     obj.PHYSICAL_AT_PENDING_TAT_DATE= None
                                
                                            
        #                             if d["PHYSICAL_AT_Status"] == "PENDING":
        #                                     print("inside PENDING update")
        #                                     obj.PHYSICAL_AT_Status=d["PHYSICAL_AT_Status"]
        #                                     if pd.isnull(d["PHYSICAL_AT_PENDING_REASON"]):
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Pending Reason is missing" )
        #                                             continue
        #                                     else:
        #                                         obj.PHYSICAL_AT_PENDING_REASON=d["PHYSICAL_AT_PENDING_REASON"] 

        #                                     if pd.isnull(d["PHYSICAL_AT_PENDING_REMARK"]):
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Pending Remark is missing" )
        #                                             continue
        #                                     else:
        #                                         obj.PHYSICAL_AT_PENDING_REMARK=d["PHYSICAL_AT_PENDING_REMARK"]
                                            
                                            
        #                                     if not pd.isnull(d["PHYSICAL_AT_PENDING_TAT_DATE"]) and  isinstance(d["PHYSICAL_AT_PENDING_TAT_DATE"], datetime.datetime):
        #                                         obj.SOFT_AT_PENDING_TAT_DATE=d["PHYSICAL_AT_PENDING_TAT_DATE"]
        #                                         print("updated")
        #                                     else:
        #                                         if pd.isnull(d["PHYSICAL_AT_PENDING_TAT_DATE"]):
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Pending TAT date is missing" )
        #                                         else:
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Pending TAT formate is not correct" )
        #                                         continue   
        #                                     obj.PHYSICAL_AT_ACCEPTANCE_DATE=None
        #                                     obj.PHYSICAL_AT_ACCEPTANCE_MAIL=""
        #                                     obj.PHYSICAL_AT_REJECTION_DATE = None
        #                                     obj.PHYSICAL_AT_REJECTION_REASON=""
        #                                     obj.PHYSICAL_AT_OFFERED_DATE= None
        #                                     obj.PHYSICAL_AT_OFFERED_REMARKS= ""
                                
        #                         else:
        #                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Getting Physical At Status Other than ACCEPTED/REJECTED/PENDING/OFFERED" )
        #                             continue
                                
                                
        # ############################################### PERFORMANCE AT #####################################################################################################################################################################     
                            
        #                         bands=str(d["BAND"]).split("_")
        #                         print(bands)
        #                         if d["Performance_AT_Status"] == "ACCEPTED" or d["Performance_AT_Status"] == "REJECTED" or d["Performance_AT_Status"] == "OFFERED" or d["Performance_AT_Status"] == "PENDING":
                                
        #                             if d["Performance_AT_Status"] == "ACCEPTED":
        #                                     if obj.Performance_AT_Status == "ACCEPTED":
        #                                         status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark=" Performance at Status Already accepted in the database" )
                                            
        #                                         continue
        #                                     else:
        #                                         obj.Performance_AT_Status=d["Performance_AT_Status"]
        #                                         if not pd.isnull(d["PERFORMANCE_AT_ACCEPTANCE_DATE"]) and  isinstance(d["PERFORMANCE_AT_ACCEPTANCE_DATE"], datetime.datetime):
        #                                             obj.PERFORMANCE_AT_ACCEPTANCE_DATE = d["PERFORMANCE_AT_ACCEPTANCE_DATE"]
        #                                         else:
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at acceptance date is missing or date formate is not correct")
        #                                             continue

        #                                         for kpi_obj in kpi_objs:
        #                                             if kpi_obj.band=="G1800":
        #                                                 kpi_obj.Performance_AT_Status="ACCEPTED"
        #                                                 kpi_obj.PERFORMANCE_AT_ACCEPTANCE_MAIL=G1800
        #                                                 kpi_obj.PERFORMANCE_AT_ACCEPTANCE_DATE=d["PERFORMANCE_AT_ACCEPTANCE_DATE"]
                                                        
        #                                             if kpi_obj.band=="L1800":
        #                                                 kpi_obj.Performance_AT_Status="ACCEPTED"
        #                                                 kpi_obj.PERFORMANCE_AT_ACCEPTANCE_DATE=d["PERFORMANCE_AT_ACCEPTANCE_DATE"]
        #                                                 kpi_obj.PERFORMANCE_AT_ACCEPTANCE_MAIL=L1800

                                                    
        #                                             if kpi_obj.band=="L900":
        #                                                 kpi_obj.Performance_AT_Status="ACCEPTED"
        #                                                 kpi_obj.PERFORMANCE_AT_ACCEPTANCE_DATE=d["PERFORMANCE_AT_ACCEPTANCE_DATE"]
        #                                                 kpi_obj.PERFORMANCE_AT_ACCEPTANCE_MAIL=L900
                                                    
        #                                             if kpi_obj.band=="L2300":
        #                                                 kpi_obj.Performance_AT_Status="ACCEPTED"
        #                                                 kpi_obj.PERFORMANCE_AT_ACCEPTANCE_DATE=d["PERFORMANCE_AT_ACCEPTANCE_DATE"]
        #                                                 kpi_obj.PERFORMANCE_AT_ACCEPTANCE_MAIL=L2300
                                                    
        #                                             if kpi_obj.band=="L2100":
        #                                                 kpi_obj.Performance_AT_Status="ACCEPTED"
        #                                                 kpi_obj.PERFORMANCE_AT_ACCEPTANCE_DATE=d["PERFORMANCE_AT_ACCEPTANCE_DATE"]
        #                                                 kpi_obj.PERFORMANCE_AT_ACCEPTANCE_MAIL=L2100
        #                                             kpi_obj.save()
                                                

                                                
        #                                         obj.PERFORMANCE_AT_REJECTION_DATE = None
        #                                         obj.PERFORMANCE_AT_REJECTION_REASON= "" 
        #                                         obj.PERFORMANCE_AT_OFFERED_DATE= None
        #                                         obj.PERFORMANCE_AT_OFFERED_REMARKS= ""
        #                                         obj.PERFORMANCE_AT_PENDING_REASON= ""
        #                                         obj.PERFORMANCE_AT_PENDING_REMARK= ""
        #                                         obj.PERFORMANCE_AT_PENDING_TAT_DATE= None
                                            
                                            
                                            
        #                             if d["Performance_AT_Status"] == "REJECTED":
        #                                     obj.Performance_AT_Status=d["Performance_AT_Status"]
        #                                     if not pd.isnull(d["PERFORMANCE_AT_REJECTION_DATE"])  and  isinstance(d["PERFORMANCE_AT_REJECTION_DATE"], datetime.datetime):
        #                                         obj.PERFORMANCE_AT_REJECTION_DATE = d["PERFORMANCE_AT_REJECTION_DATE"]

        #                                     else:
        #                                         if pd.isnull(d["PERFORMANCE_AT_REJECTION_DATE"]):
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Rejection date is missing" )
        #                                         else:
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Rejection date formate is not correct" )
                                            
        #                                         continue    
        #                                     if pd.isnull(d["PERFORMANCE_AT_REJECTION_REASON"]):
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Rejection Reason is missing" )
        #                                             continue
        #                                     else:
        #                                         obj.PERFORMANCE_AT_REJECTION_REASON=d["PERFORMANCE_AT_REJECTION_REASON"]
                                                    
        #                                         lis_kpi_status_bandwise=d["PERFORMANCE_AT_REJECTION_REASON"].split(",")
                                                
                                                
        #                                         di={}
        #                                         sts=True
        #                                         for band_status in lis_kpi_status_bandwise:
        #                                                 if("_" in band_status):
        #                                                         lis=band_status.split("_")
        #                                                         di[lis[0]] = lis[1]
        #                                                 else:
        #                                                     status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Band and status should be separated by a '_' in the PERFORMANCE_AT_REJECTION_REASON " )
        #                                                     sts=False
        #                                                     break
        #                                         if sts==False:
        #                                             continue

                                                        
        #                                         for  kpi_obj in kpi_objs:
        #                                                 if kpi_obj.band in di.keys():
        #                                                     kpi_obj.Performance_AT_Status=di[str(kpi_obj.band)] 
        #                                                     print(di[str(kpi_obj.band)], kpi_obj.band)
        #                                                     kpi_obj.save()
        #                                         print(di)

                                            
        #                                     obj.PERFORMANCE_AT_ACCEPTANCE_DATE=None
        #                                     obj.PERFORMANCE_AT_OFFERED_DATE= None
        #                                     obj.PERFORMANCE_AT_OFFERED_REMARKS= ""
        #                                     obj.PERFORMANCE_AT_PENDING_REASON= ""
        #                                     obj.PERFORMANCE_AT_PENDING_REMARK= ""
        #                                     obj.PERFORMANCE_AT_PENDING_TAT_DATE= None
                                    
        #                             if d["Performance_AT_Status"] == "OFFERED":
        #                                     print("inside OFFERED update")
                                            
        #                                     obj.Performance_AT_Status=d["Performance_AT_Status"]
                                            
        #                                     if not pd.isnull(d["PERFORMANCE_AT_OFFERED_DATE"]) and isinstance(d["PERFORMANCE_AT_OFFERED_DATE"], datetime.datetime):
        #                                         obj.PERFORMANCE_AT_OFFERED_DATE=d["PERFORMANCE_AT_OFFERED_DATE"]
        #                                         print("updated")
        #                                     else:
        #                                         if pd.isnull(d["PERFORMANCE_AT_OFFERED_DATE"]):
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Offered date is missing" )
        #                                         else:
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Offered date formate is not correct" )
                                                
        #                                         continue    

        #                                     if pd.isnull(d["PERFORMANCE_AT_OFFERED_REMARKS"]):
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Offered remark is missing" )
        #                                             continue
        #                                     else:
        #                                         obj.PERFORMANCE_AT_OFFERED_REMARKS=d["PERFORMANCE_AT_OFFERED_REMARKS"]  
        #                                         lis_kpi_status_bandwise=d["PERFORMANCE_AT_OFFERED_REMARKS"].split(",")
        #                                         di={}
        #                                         sts=True
        #                                         for band_status in lis_kpi_status_bandwise:
        #                                                 if("_" in band_status):
        #                                                         lis=band_status.split("_")
        #                                                         di[lis[0]] = lis[1]
        #                                                 else:
        #                                                     status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Band and status should be separated by a '_' in the PERFORMANCE_AT_OFFERED_REMARKS " )
        #                                                     sts=False
        #                                                     break
        #                                         if sts==False:
        #                                             continue
                                                        
        #                                         for  kpi_obj in kpi_objs:
        #                                                 if kpi_obj.band in di.keys():
        #                                                     kpi_obj.Performance_AT_Status=di[str(kpi_obj.band)] 
        #                                                     print(di[str(kpi_obj.band)], kpi_obj.band)
        #                                                     kpi_obj.save()
        #                                         print(di)
        #                                     obj.PERFORMANCE_AT_ACCEPTANCE_DATE=None
                                        
        #                                     obj.PERFORMANCE_AT_REJECTION_DATE = None
        #                                     obj.PERFORMANCE_AT_REJECTION_REASON=""
                                            
                                            
        #                                     obj.PERFORMANCE_AT_PENDING_REASON= ""
        #                                     obj.PERFORMANCE_AT_PENDING_REMARK= ""
        #                                     obj.PERFORMANCE_AT_PENDING_TAT_DATE= None

        #                             if d["Performance_AT_Status"] == "PENDING":
        #                                     print("inside PENDING update")
        #                                     obj.Performance_AT_Status=d["Performance_AT_Status"]
        #                                     if pd.isnull(d["PERFORMANCE_AT_PENDING_REASON"]):
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Pending Reason is missing" )
        #                                             continue
        #                                     else:
        #                                         obj.PERFORMANCE_AT_PENDING_REASON=d["PERFORMANCE_AT_PENDING_REASON"] 

        #                                     if pd.isnull(d["PERFORMANCE_AT_PENDING_REMARK"]):
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Pending Remark is missing" )
        #                                             continue
        #                                     else:
        #                                         obj.PERFORMANCE_AT_PENDING_REMARK=d["PERFORMANCE_AT_PENDING_REMARK"]
        #                                         lis_kpi_status_bandwise=d["PERFORMANCE_AT_PENDING_REMARK"].split(",")
        #                                         di={}
        #                                         sts=True
        #                                         for band_status in lis_kpi_status_bandwise:
        #                                                 if("_" in band_status):
        #                                                         lis=band_status.split("_")
        #                                                         di[lis[0]] = lis[1]
        #                                                 else:
        #                                                     status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Band and status should be separated by a '_' in the PERFORMANCE_AT_PENDING_REMARK " )
        #                                                     sts=False
        #                                                     break
        #                                         if sts==False:
        #                                             continue
                                                        
        #                                         for  kpi_obj in kpi_objs:
        #                                                 if kpi_obj.band in di.keys():
        #                                                     kpi_obj.Performance_AT_Status=di[str(kpi_obj.band)] 
        #                                                     print(di[str(kpi_obj.band)], kpi_obj.band)
        #                                                     kpi_obj.save()
        #                                         print(di)
                                            
                                            
        #                                     if not pd.isnull(d["PERFORMANCE_AT_PENDING_TAT_DATE"]) and  isinstance(d["PERFORMANCE_AT_PENDING_TAT_DATE"], datetime.datetime):
        #                                         obj.PERFORMANCE_AT_PENDING_TAT_DATE=d["PERFORMANCE_AT_PENDING_TAT_DATE"]
        #                                         print("updated")
        #                                     else:
        #                                         if pd.isnull(d["PERFORMANCE_AT_PENDING_TAT_DATE"]):
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Pending TAT date is missing" )
        #                                         else:
        #                                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Pending TAT formate is not correct" )
                                            
        #                                         continue   
        #                                     obj.PERFORMANCE_AT_ACCEPTANCE_DATE=None
        #                                     obj.PERFORMANCE_AT_REJECTION_DATE = None
        #                                     obj.PERFORMANCE_AT_REJECTION_REASON=""
        #                                     obj.PERFORMANCE_AT_OFFERED_DATE= None
        #                                     obj.PERFORMANCE_AT_OFFERED_REMARKS= ""

        #                         else:
        #                             status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Getting Performance At Status Other than ACCEPTED/REJECTED/PENDING/OFFERED" ) 
        #                             continue
        
                                obj.save()
                                print(d["Unique_SITE_ID"], " updated")
                                status_obj=DPR_update_status.objects.create(id=pk, update_status="UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Updated Succesfully")
                            
                                    
                                del_obj.append(obj)
                                print("obj created",obj)
                            except Exception as e:
                                print("this is the exception",e)
                                for o in del_obj:
                                    o.delete()
                                    print("obj deleted",o)
                                
                                message='Could not upload,Site id are not unique...'
                                status=False
                                break
                           
    ##################################################################### Soft at ##################################################################           
                           
                            
                else:
                    status_objs=DPR_update_status.objects.all()
                    ser=ser_DPR_update_status(status_objs,many=True)
                    context={"status_obj":ser.data, "status":True}
                    return Response(context)
            else:
                context={"status":False,"message":"DPR Report is empty"}
                return Response(context)

    context={"status":False,"message":message}
    return Response(context)