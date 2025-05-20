from django.shortcuts import render,HttpResponse

# Create your views here.

from django.shortcuts import render
from rest_framework.decorators import api_view
from mcom_website.settings import MEDIA_ROOT
from rest_framework.response import Response
from django.http import JsonResponse
import json
from django.core.files.storage import FileSystemStorage
import pandas as pd
import os
import openpyxl
from .models import *   
import datetime
# Create your views here.
import json
from .serializers import *  


# def circle_list(objs):
#     cir=[]
    
#     for obj in objs:
#         cir.append(obj.CIRCLE)

#     cir_set=set(cir)
#     cir=list(cir_set)
#     return cir

# def ownership(objs):
# #      objs=performanceAT.objects.all()
#      owner=[]
    
#      for obj in objs:
#         owner.append(obj.Ownership)

#      owner_set=set(owner)
#      owner=list(owner_set)
#      return owner
      

# @ api_view(["POST"])
# def performanceAT_Report_Upload(request):
    
#     performance_At_upload_status.objects.all().delete()
#     AT = request.FILES["performance_At_Report_file"] if 'performance_At_Report_file' in request.FILES else None
#     if AT:
#             location = MEDIA_ROOT + r"\ATP\temporary_files"
#             fs = FileSystemStorage(location=location)
#             file = fs.save(AT.name, AT)
#             # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
#             filepath = fs.path(file)
#             print("file_path:-",filepath)
#             df=pd.read_excel(filepath,sheet_name="Data") # should do something if a csv file is coming from the frontend and the csv file should be deleted from the temp files
#             os.remove(path=filepath)
#             print(filepath,"deleted........")
#             print(df)
#             upload_date=request.POST.get("upload_date")
#             print("upload date is......................",upload_date)

#             df_header_list= df.columns.tolist()
#             print("Header Name-------------------",df_header_list)
#             required_header_list=["CIRCLE","SITE_ID","UNIQUE ID","ENODEB_ID","BAND","Circle Project","OEM_NAME (Nokia/ZTE/Ericsson/Huawei)","MS1","Performance_AT_Status( Accepted/Rejected/Offered/Pending/Dismantle)","Internal Ms1 Vs Ms2-In days","Total  Allocation","Project","Acceptance Status ( Accepted / Offered/Pending","Accepted / Offered Date","Pending Reason","Action Plan","Ownership","Ageing"]
#             for header_name in required_header_list:
#                 if header_name in df_header_list:
#                      pass
#                 else:
#                      message= "Did not get " + header_name + " Column in the uploaded Report"
#                      return Response({"status":False,"message":message})

#             for i, d in df.iterrows():
#                 # try:
#                     # if pd.isnull(d["CIRCLE"]) or pd.isnull(d["UNQUI ID"]) or pd.isnull(d["SITE_ID"]) or pd.isnull(d["Circle Project"]) or pd.isnull(d["RFAI_DATE"]) or pd.isnull(["OA_(COMMERCIAL_TRAFFIC_PUT_ON_AIR)_(MS1)_DATE"]) or pd.isnull(d["Status"] or pd.isnull("Date")):

#                     pk=str(d["CIRCLE"])+str(d["SITE_ID"])+str(d["BAND"])+str(d["UNIQUE ID"])+str(upload_date)
#                     if pd.isnull(d['Accepted / Offered Date']):
#                            Accepted_Offered_Date=None    
#                     else:
#                            Accepted_Offered_Date=(d["Accepted / Offered Date"])

#                     if pd.isnull(d['MS1']) :
#                           MS1=None
#                     else:
#                           MS1=(d['MS1'])            
#                     try:
#                         obj=performanceAT.objects.update_or_create(id=pk,upload_date=upload_date,
#                                                         defaults={"CIRCLE":str(d["CIRCLE"]),dd
#                                                         "SITE_ID":str(d["SITE_ID"]),dd
#                                                         "UNIQUE_ID":str(d["UNIQUE ID"]),dd
#                                                         "ENODEB_ID":str(d["ENODEB_ID"]),
#                                                         "BAND":str(d["BAND"]),
#                                                         "Circle_Project":str(d["Circle Project"]),  
#                                                         "OEM_NAME_Nokia_ZTE_Ericsson_Huawei":str(d["OEM_NAME (Nokia/ZTE/Ericsson/Huawei)"]),
#                                                         "MS1":MS1,
#                                                         "Performance_AT_Status_Accepted_Rejected":str(d["Performance_AT_Status( Accepted/Rejected/Offered/Pending/Dismantle)"]),
#                                                         "Internal_Ms1_Vs_Ms2_n_days":str(d["Internal Ms1 Vs Ms2-In days"]),
#                                                         "Total_Allocation":str(d["Total  Allocation"]),
#                                                         "Project":str(d["Project"]),
#                                                         "Acceptance_Status_Accepted_Offered_Pending":str(d["Acceptance Status ( Accepted / Offered/Pending"]),
#                                                         "Accepted_Offered_Date":Accepted_Offered_Date,
#                                                         "Pending_Reason":str(d["Pending Reason"]),
#                                                         "Action_Plan":str(d["Action Plan"]),
#                                                         "Ownership":str(d["Ownership"]),
#                                                         "Ageing":str(d["Ageing"]),
#                                                         "upload_date":upload_date,}



                                                        
#                                                         )
                        
#                     except Exception as e:
#                             print(e)
#                             error=str(e)
#                             performance_At_upload_status.objects.create(id=pk,Site_id=d["SITE_ID"],update_status="Not Uploaded",Remark=error)
#                             continue 

#             objs=performance_At_upload_status.objects.all()
#             serializers=ser_performance_At_upload_status(objs,many=True)
                 


#             return Response({"status": True,"message":"Report uploaded Successfully .","status_obj":serializers.data})
#     else:
#          return Response({"status": False,"message":"No report file Sent"})
    

# def df_raw_column_total(data):
#         # print("_________________circle_wise_data_____________________________________")
#         print(data)
#         df=pd.DataFrame(data)
#         df=df.T
#         # add a sum row at the bottom of the dataframe
#         df.loc['Total'] = df.sum()
#         # add a sum column at the right end of the dataframe
#         df['Total'] = df.sum(axis=1)
#         json_data = df.to_json(orient='index') # here json_data  converts the dataframe to a string json
#         json_data=json.loads(json_data) # json.loads - Which converts the string form of json data to a dictionary in python.
#         print(df)
#         return(json_data)
# def df_raw_column_total_circle_wise(data):
#         print("_________________circle_wise_data_____________________________________")
#         print(data)
#         df=pd.DataFrame(data)
#         df=df.T
#         print("---------------------------dataframe------------------------",df)
#         # add a sum row at the bottom of the dataframe
#         df.loc['Total'] = df.sum()
#         # add a sum column at the right end of the dataframe
#         df['Total'] = df["Accepted"]+ df["Pending"] +df["Offered"]+df["Dismantled"]+df["Non workable"] +df["Under Dismantle"]
#         json_data = df.to_json(orient='index') # here json_data  converts the dataframe to a string json
#         json_data=json.loads(json_data) # json.loads - Which converts the string form of json data to a dictionary in python.
#         print(df)
#         return(json_data)

# @api_view(["GET","POST"])
# # @authentication_classes([TokenAuthentication])
# # @permission_classes([IsAuthenticated])
# def PerformanceAT_Circlewise_Dashboard(request):
#        print("Current_User---------------",request.user)
#        str_Date=request.POST.get("Date")
#        month=request.POST.get("month")
#        week=request.POST.get("week")
#        year=request.POST.get("year")
#        str_from_date=request.POST.get("from_date")
#        str_to_date=request.POST.get("to_date")
#        Project=request.POST.get("project")
#        Projects=Project.split(",")
       
#        print("Project-----",Project)
#        print("Projects------",Projects)
#        print("month:-----",month)
#        print("date:-----",str_Date)
#        print("week:---",week)
#        print("year:---",year)
#        print("str_from_date:---",str_from_date)
#        print("str_to_date---",str_to_date)
      

#        year=int(year)
#        objs=performanceAT.objects.all()
#        circles= circle_list(objs)
#        print("Circle_list: ",circles)
#        data={}
#        for circle in circles:
#             if Project != "":
#                obj=performanceAT.objects.filter(CIRCLE=circle,Circle_Project__in=Projects)
#             else:     
#                 obj=performanceAT.objects.filter(CIRCLE=circle)
#             if str_Date != "":
#                 print("___________Inside Date___________")
#                 Date=datetime.datetime.strptime(str_Date,"%Y-%m-%d").date()
#                 print(Date)
#                 Accepted=obj.filter(Acceptance_Status_Accepted_Offered_Pending__iexact="Accepted", upload_date=Date).count()
#                 Offered=obj.filter(Acceptance_Status_Accepted_Offered_Pending__iexact="offered",upload_date=Date).count()
#                 Pending=obj.filter(Acceptance_Status_Accepted_Offered_Pending__iexact= "Pending",upload_date=Date).count()
#                 Dismantled=obj.filter(Acceptance_Status_Accepted_Offered_Pending__iexact="Dismantled",upload_date=Date).count()
#                 Non_workable=obj.filter(Acceptance_Status_Accepted_Offered_Pending__iexact="Non workable",upload_date=Date).count()
#                 Under_Dismantle=obj.filter(Acceptance_Status_Accepted_Offered_Pending__iexact="Under Dismantle",upload_date=Date).count()

#             elif month != "":
                
#                 print("___________Inside Month___________")
#                 print(month)
                
#                 Accepted=obj.filter(Status__iexact="Accepted",Upload_date__month=month,Upload_date__year=year).count()
                
#                 month_obj=obj.filter(Upload_date__month=month,Upload_date__year=year)
                
#                 if(len(month_obj)!=0):
#                     obj=month_obj.filter(Upload_date=month_obj.latest("Upload_date").Upload_date)

#                     Dismantled=obj.filter(Status__iexact="Dismantled").count()
#                     Offered=obj.filter(Status__iexact="Offered").count()
#                     Non_workable=obj.filter(Status__iexact="Non_workable").count()
#                     Under_Dismantle=obj.filter(Status__iexact="Under_Dismantle").count()
#                     Pending=obj.filter(Status__iexact= "Pending").count()
#                 else:
#                     Dismantled=0
#                     Offered=0
#                     Non_workable=0
#                     Under_Dismantle=0
#                     Pending=0

#             elif week != "":
                
#                 print("___________Inside week___________")
#                 week=int(week)
#                 Accepted=obj.filter(Status__iexact="Accepted",Upload_date__week=week,Upload_date__year=year).count()
#                 week_obj=obj.filter(Upload_date__week=week,Upload_date__year=year)
#                 if(len(week_obj)!=0):
                    
#                     obj=week_obj.filter(Upload_date=week_obj.latest("Upload_date").Upload_date)
#                     Dismantled=obj.filter(Status__iexact="Dismantled").count()
#                     Offered=obj.filter(Status__iexact="Offered").count()
#                     Non_workable=obj.filter(Status__iexact="Non_workable").count()
#                     Under_Dismantle=obj.filter(Status__iexact="Under_Dismantle").count()
#                     Pending=obj.filter(Status__iexact= "Pending").count()
#                 else:
#                     Dismantled=0
#                     Offered=0
#                     Non_workable=0
#                     Under_Dismantle=0
#                     Pending=0
#             elif str_from_date != "" and str_to_date != "":
                
#                 print("___________Inside from and to ___________")
#                 from_date=datetime.datetime.strptime(str_from_date,"%Y-%m-%d").date()
#                 to_date=datetime.datetime.strptime(str_to_date,"%Y-%m-%d").date()
#                 print("from_date",from_date)
#                 print("to_date",to_date)

                
                
#                 Accepted=obj.filter(Status__iexact="Accepted",Upload_date__range=(from_date,to_date)).count()
#                 Dismantled=obj.filter(Status__iexact="Dismantled",Upload_date=to_date).count()
#                 Offered=obj.filter(Status__iexact="Offered",Upload_date=to_date).count()
#                 Non_workable=obj.filter(Status__iexact="Non_workable",Upload_date=to_date).count()
#                 Under_Dismantle=obj.filter(Status__iexact="Under_Dismantle",Upload_date=to_date).count()
#                 Pending=obj.filter(Status__iexact= "Pending",Upload_date=to_date).count()


#             else:
#                 print("_________________Inside All_______________")
#                 Accepted=obj.filter(Acceptance_Status_Accepted_Offered_Pending__iexact="Accepted").count()
#                 Offered=obj.filter(Acceptance_Status_Accepted_Offered_Pending__iexact="offered",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#                 Pending=obj.filter(Acceptance_Status_Accepted_Offered_Pending__iexact= "Pending",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#                 Dismantled=obj.filter(Acceptance_Status_Accepted_Offered_Pending__iexact="Dismantled",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#                 Non_workable=obj.filter(Acceptance_Status_Accepted_Offered_Pending__iexact="Non workable",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#                 Under_Dismantle=obj.filter(Acceptance_Status_Accepted_Offered_Pending__iexact="Under Dismantle",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
                                      



#             total=Accepted +  Offered +  Pending + Dismantled + Non_workable + Under_Dismantle
#             print(circle,total)

#             data[circle]={"Accepted":Accepted,"Dismantled":Dismantled,"Offered":Offered,"Non_workable":Non_workable,"Pending":Pending,"Under_Dismantle":Under_Dismantle}
#        print("__________________________data________________",data)
#        if len(data)!=0:
#             data1=df_raw_column_total(data)
#        else:
#             return Response({"status":False,"message":"Database is empty"})


         
      

# ####################################### PENDING REASON ###############################################################
#        pending_sites_ownership={}
#        circles=circle_list(objs)
#        print('________________circles________________',circles)
#        for circle in circles: 
#             objs=performanceAT.objects.filter(CIRCLE=circle)
#             SCFT_Team=objs.filter(Acceptance_Status_Accepted_Offered_Pending="Pending",Ownership = "SCFT Team").count()
#             Circle_Team=objs.filter(Acceptance_Status_Accepted_Offered_Pending="Pending",Ownership = "Circle Team").count()
#             RNO=objs.filter(Acceptance_Status_Accepted_Offered_Pending="Pending",Ownership = "RNO").count()
#             Airtel=objs.filter(Acceptance_Status_Accepted_Offered_Pending="Pending",Ownership = "Airtel").count()
#             Ericsson=objs.filter(Acceptance_Status_Accepted_Offered_Pending="Pending",Ownership = "Ericsson").count()
#             Bharti_TOCO=objs.filter( Acceptance_Status_Accepted_Offered_Pending="Pending",Ownership = "Bharti TOCO").count()
#             Dismantled=objs.filter( Acceptance_Status_Accepted_Offered_Pending="Pending",Ownership = "Dismantled").count()
#             Not_belongs_to_Mcom=objs.filter(Acceptance_Status_Accepted_Offered_Pending="Pending",Ownership = "Not belongs to Mcom").count()  

#             pending_sites_ownership[circle]={"SCFT_Team":SCFT_Team,
#                                      "Circle_Team":Circle_Team,
#                                     "RNO":RNO,
#                                     "Airtel":Airtel,
#                                     "Ericsson":Ericsson,
#                                     "Bharti_TOCO":Bharti_TOCO,
#                                     "Dismantled":Dismantled,
#                                     "Not_belongs_to_Mcom":Not_belongs_to_Mcom
#                                      }
#        # ageing_circleWise_data = df_raw_column_total(ageing_circleWise)
#        pending_sites_ownership=df_raw_column_total(pending_sites_ownership)

       
# ################################################# pending reason (Alarm Bucket) #########################################################
#        objs=performanceAT.objects.all()

#        objs=objs.filter(Acceptance_Status_Accepted_Offered_Pending__iexact= "Pending")
#        Imbalanced=objs.filter(Pending_Reason="Imbalanced",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        Site_Relocated=objs.filter(Pending_Reason="Site Relocated",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        Payload_Dip=objs.filter(Pending_Reason="Payload Dip",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        HOSR_Issue=objs.filter(Pending_Reason="HOSR Issue",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        RF_Unit_VSWR_Threshold_Crossed_HOSR_Issue=objs.filter(Pending_Reason="RF Unit VSWR Threshold Crossed/HOSR-Issue",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        Swapped_with_Ericsson=objs.filter(Pending_Reason="Swapped with Ericsson",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        GNSS_Antenna_Fault_Rejected_HOSR_Issue=objs.filter(Pending_Reason="GNSS Antenna Fault/Rejected/HOSR Issue",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        PS_RAB_Volte_Erab_Volte_Drop_NE_Disconnected_Swapped_with_Ericsson=objs.filter(Pending_Reason="PS RAB-Volte Erab-Volte Drop/NE Disconnected/Swapped with Ericsson",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        HOSR_Issue_Site_Down=objs.filter(Pending_Reason="HOSR Issue/Site Down",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()

#        CSFB_HOSR_Issue=objs.filter(Pending_Reason="CSFB-HOSR Issue",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        Site_Locked_dismantling_required=objs.filter(Pending_Reason="Site Locked/dismantling required",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        One_sec_Down=objs.filter(Pending_Reason="One sec Down",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        VSWR_major_alarm=objs.filter(Pending_Reason="VSWR major alarm",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        Site_Down=objs.filter(Pending_Reason="Site Down",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        S1_SCTP_path_failure=objs.filter(Pending_Reason="S1 SCTP path failure",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        Two_sec_Down=objs.filter(Pending_Reason="Two sec Down",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        Payload_150_GB_Optimization_Req=objs.filter(Pending_Reason="Payload < 150 GB, Optimization Req",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()

#        Transport_layer_connection_failure_in_S1_interface=objs.filter(Pending_Reason="Transport layer connection failure in S1 interface",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        Need_to_Offer=objs.filter(Pending_Reason="Need to Offer",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        Twamp_Issue=objs.filter(Pending_Reason="Twamp Issue",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        Poor_RNA=objs.filter(Pending_Reason="Poor RNA",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        Days_KPI_Pending=objs.filter(Pending_Reason="5 Days KPI Pending",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        Sec_Down=objs.filter(Pending_Reason="Sec Down",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        Failure_in_replaceable_baseband_unit=objs.filter(Pending_Reason="Failure in replaceable baseband unit",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        RNA_Issue=objs.filter(Pending_Reason="RNA Issue",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        Optimization_Req=objs.filter(Pending_Reason="Optimization Req",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        Nbr_Sites_Less_Payload=objs.filter(Pending_Reason="Nbr Sites Less Payload",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        Media_Issue=objs.filter(Pending_Reason="Media Issue",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        Nbr_Site_offload_Req=objs.filter(Pending_Reason="Nbr Site offload Req",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        Nbr_Site_less_PL=objs.filter(Pending_Reason="Nbr Site less PL",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()

#        Pending_2G=objs.filter(Pending_Reason=",,,2G Pending,",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        RNA_Issue=objs.filter(Pending_Reason=",RNA Issue,,,",upload_date=performanceAT.objects.latest('upload_date').upload_date).count() 
# #        TWAMP_Issue=objs.filter(Pending_Reason="TWAMP Issue,,,,",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        TWAMP_Issue_2G_Pending=objs.filter(Pending_Reason="TWAMP Issue,,,2G Pending,",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
# #        Sec_Down=objs.filter(Pending_Reason=",,,,Sec Down",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        less_PL=objs.filter(Pending_Reason=",,,,less PL",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        Rectification_required_Packet_Loss_issue=objs.filter(Pending_Reason="Rectification required Packet Loss issue",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        Partially_KPI_accepted_only_2G_HOSR_issue=objs.filter(Pending_Reason="Partially KPI accepted only 2G HOSR issue",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        SCFT_Done_but_RET_Alarm_showing=objs.filter(Pending_Reason="SCFT Done but RET Alarm showing",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
#        Site_locked_due_to_customer_complaints=objs.filter(Pending_Reason="Site locked due to customer complaints",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()



#        total= Imbalanced + Site_Relocated + Payload_Dip + HOSR_Issue  + RF_Unit_VSWR_Threshold_Crossed_HOSR_Issue + Swapped_with_Ericsson + GNSS_Antenna_Fault_Rejected_HOSR_Issue + PS_RAB_Volte_Erab_Volte_Drop_NE_Disconnected_Swapped_with_Ericsson +HOSR_Issue_Site_Down + CSFB_HOSR_Issue + Site_Locked_dismantling_required + One_sec_Down +VSWR_major_alarm +Site_Down +S1_SCTP_path_failure + Two_sec_Down + Payload_150_GB_Optimization_Req + Transport_layer_connection_failure_in_S1_interface + Need_to_Offer + Twamp_Issue + Days_KPI_Pending + Sec_Down + Failure_in_replaceable_baseband_unit + RNA_Issue + Optimization_Req + Nbr_Sites_Less_Payload + Media_Issue + Nbr_Site_offload_Req + Nbr_Site_less_PL + Pending_2G + RNA_Issue  + TWAMP_Issue_2G_Pending  + less_PL + Rectification_required_Packet_Loss_issue + Partially_KPI_accepted_only_2G_HOSR_issue + SCFT_Done_but_RET_Alarm_showing + Site_locked_due_to_customer_complaints + Poor_RNA
#        print("____________total____________",total)
#        alarm_Reasonization={}
  
#        alarm_Reasonization["Imbalanced"]={"Count_of_Pending_Reason":Imbalanced}
#        alarm_Reasonization["Site Relocated"]={"Count_of_Pending_Reason":Site_Relocated}
#        alarm_Reasonization["Payload_Dip"]={"Count_of_Pending_Reason":Payload_Dip}
#        alarm_Reasonization["HOSR_Issue"]={"Count_of_Pending_Reason":HOSR_Issue}
#        alarm_Reasonization["RF Unit VSWR Threshold Crossed/HOSR-Issue"]={"Count_of_Pending_Reason":RF_Unit_VSWR_Threshold_Crossed_HOSR_Issue}
#        alarm_Reasonization["Swapped with Ericsson"]={"Count_of_Pending_Reason":Swapped_with_Ericsson}
#        alarm_Reasonization["GNSS Antenna Fault/Rejected/HOSR Issue"]={"Count_of_Pending_Reason":GNSS_Antenna_Fault_Rejected_HOSR_Issue}
#        alarm_Reasonization["PS RAB-Volte Erab-Volte Drop/NE Disconnected/Swapped with Ericsson"]={"Count_of_Pending_Reason":PS_RAB_Volte_Erab_Volte_Drop_NE_Disconnected_Swapped_with_Ericsson}
#        alarm_Reasonization["HOSR Issue/Site Down"]={"Count_of_Pending_Reason":HOSR_Issue_Site_Down}




#        alarm_Reasonization["CCSFB-HOSR Issue"]={"Count_of_Pending_Reason":CSFB_HOSR_Issue}
#        alarm_Reasonization["Site Locked/dismantling required"]={"Count_of_Pending_Reason":Site_Locked_dismantling_required}
#        alarm_Reasonization["One_sec_Down"]={"Count_of_Pending_Reason":One_sec_Down}
#        alarm_Reasonization["VSWR major alarm"]={"Count_of_Pending_Reason":VSWR_major_alarm}
#        alarm_Reasonization["Site Down"]={"Count_of_Pending_Reason":Site_Down}
#        alarm_Reasonization["S1 SCTP path failure"]={"Count_of_Pending_Reason":S1_SCTP_path_failure}
#        alarm_Reasonization["Two sec Down"]={"Count_of_Pending_Reason":Two_sec_Down}
#        alarm_Reasonization["Payload < 150 GB, Optimization Req"]={"Count_of_Pending_Reason":Payload_150_GB_Optimization_Req}


#        alarm_Reasonization["Transport layer connection failure in S1 interface"]={"Count_of_Pending_Reason":Transport_layer_connection_failure_in_S1_interface}
#        alarm_Reasonization["Need to Offer"]={"Count_of_Pending_Reason":Need_to_Offer}
#        alarm_Reasonization["Twamp_Issue"]={"Count_of_Pending_Reason":Twamp_Issue}
#        alarm_Reasonization["Poor RNA"]={"Count_of_Pending_Reason":Poor_RNA}
#        alarm_Reasonization["Days KPI Pending"]={"Count_of_Pending_Reason":Days_KPI_Pending}
#        alarm_Reasonization["Sec Down"]={"Count_of_Pending_Reason":Sec_Down}
#        alarm_Reasonization["Failure in replaceable baseband unit"]={"Count_of_Pending_Reason":Failure_in_replaceable_baseband_unit}
#        alarm_Reasonization["RNA Issue"]={"Count_of_Pending_Reason":RNA_Issue}
#        alarm_Reasonization["Optimization_Req"]={"Count_of_Pending_Reason":Optimization_Req}
#        alarm_Reasonization["Nbr Sites Less Payload"]={"Count_of_Pending_Reason":Nbr_Sites_Less_Payload}
#        alarm_Reasonization["Media Issue"]={"Count_of_Pending_Reason":Media_Issue}
#        alarm_Reasonization["Nbr Site offload Req"]={"Count_of_Pending_Reason":Nbr_Site_offload_Req}
#        alarm_Reasonization["Nbr Site less PL"]={"Count_of_Pending_Reason":Nbr_Site_less_PL}

#        alarm_Reasonization["Pending 2G"]={"Count_of_Pending_Reason":Pending_2G}
#        alarm_Reasonization[",RNA Issue,,,"]={"Count_of_Pending_Reason":RNA_Issue}
#        alarm_Reasonization["TWAMP Issue,,,2G Pending,"]={"Count_of_Pending_Reason":TWAMP_Issue_2G_Pending}
#        alarm_Reasonization[",,,,less PL"]={"Count_of_Pending_Reason":less_PL}
#        alarm_Reasonization["Rectification required Packet Loss issue"]={"Count_of_Pending_Reason":Rectification_required_Packet_Loss_issue}
#        alarm_Reasonization["Partially KPI accepted only 2G HOSR issue"]={"Count_of_Pending_Reason":Partially_KPI_accepted_only_2G_HOSR_issue}

#        alarm_Reasonization["SCFT_Done_but_RET_Alarm_showing"]={"Count_of_Pending_Reason":SCFT_Done_but_RET_Alarm_showing}
#        alarm_Reasonization["Site locked due to customer complaints"]={"Count_of_Pending_Reason":Site_locked_due_to_customer_complaints}

#        alarm_Reasonization["Grand_Total"]={"Count_of_Pending_Reason":total}
# #        alarm_Reasonization=df_raw_column_total(alarm_Reasonization)
#        print("------------------------------------------------------ Alarm Reasonization ---------------------------------------",alarm_Reasonization)
       
# ######################################## AGEING(CIRCLE WISE) ########################################################################
#        ageing_circleWise={}
#        for circle in circles:
             
#             obj=performanceAT.objects.filter(CIRCLE=circle).filter(upload_date=performanceAT.objects.latest('upload_date').upload_date)
#             ageing_0_15=obj.filter(Acceptance_Status_Accepted_Offered_Pending="Pending",Ageing = "0-15").count()
#             ageing_16_30=obj.filter(Acceptance_Status_Accepted_Offered_Pending="Pending",Ageing = "16-30").count()
#             ageing_31_60=obj.filter(Acceptance_Status_Accepted_Offered_Pending="Pending",Ageing = "31-60").count()
#             ageing_61_90=obj.filter(Acceptance_Status_Accepted_Offered_Pending="Pending",Ageing = "61-90").count()
#             ageing_GT90=obj.filter(Acceptance_Status_Accepted_Offered_Pending="Pending",Ageing = "GT90").count()   

#             ageing_circleWise[circle]={"ageing_0_15":ageing_0_15,
#                                     "ageing_16_30":ageing_16_30,
#                                     "ageing_31_60":ageing_31_60,
#                                     "ageing_61_90":ageing_61_90,
#                                      "ageing_GT90":ageing_GT90,
#                                      }
#        ageing_circleWise_data = df_raw_column_total(ageing_circleWise)

      
#        Latest_date = performanceAT.objects.latest('upload_date').upload_date
       
#        objs=performanceAT.objects.all()
#        owner=ownership(objs)
#        return Response({"status":True,"message":"successfully","Data":data1,"ownership":pending_sites_ownership,"alarm_Reasonization":alarm_Reasonization,"ageing_circleWise_data":ageing_circleWise_data,"latest_date":Latest_date,"Ownerships":owner})

     

# #############################################################################################
# @api_view(["GET","POST"])
# def ownership_wise_pending_ageing(request):
#      ownership=request.POST.get("ownership")

     
#      ownership=ownership.split(",")
#      print("------------------------------ownership",ownership)
#      objs=performanceAT.objects.all()
#      circles= circle_list(objs)
     
#      pending_ageingwise_dict={}
#      for circle in circles:
#             obj=performanceAT.objects.filter(CIRCLE=circle).filter(upload_date=performanceAT.objects.latest('upload_date').upload_date)
#             ageing_0_15=obj.filter(Acceptance_Status_Accepted_Offered_Pending="Pending",Ageing = "0-15",Ownership__in = ownership).count()
#             ageing_16_30=obj.filter(Acceptance_Status_Accepted_Offered_Pending="Pending",Ageing = "16-30",Ownership__in = ownership).count()
#             ageing_31_60=obj.filter(Acceptance_Status_Accepted_Offered_Pending="Pending",Ageing = "31-60",Ownership__in = ownership).count()
#             ageing_61_90=obj.filter(Acceptance_Status_Accepted_Offered_Pending="Pending",Ageing = "61-90",Ownership__in = ownership).count()
#             ageing_GT90=obj.filter(Acceptance_Status_Accepted_Offered_Pending="Pending",Ageing = "GT90",Ownership__in = ownership).count()


#             pending_ageingwise_dict[circle]={"ageing_0_15":ageing_0_15,
#                                         "ageing_16_30":ageing_16_30,
#                                         "ageing_31_60":ageing_31_60,
#                                         "ageing_61_90":ageing_61_90,
#                                         "ageing_GT90":ageing_GT90}  

#      pending_ageingWise= df_raw_column_total(pending_ageingwise_dict)

#      print(pending_ageingWise)

#      # return Response({"status":True,"ageing_pendingWise_SCFT_Team":ageing_pendingWise_SCFT_Team})

#      return Response({"status":True,"message":"successfully","pending_ageingWise":pending_ageingWise,
#                       })
# @api_view(["GET","POST"])
# def site_list_request_handler(request):
#      ownership_str= request.POST.get("ownership")
#      ownership=ownership_str.split(",")
#      print(ownership)
#      circle= request.POST.get("circle")
#      print(circle)
#      ageing= request.POST.get("ageing")
#      print(ageing)
#      objs=performanceAT.objects.filter(upload_date=performanceAT.objects.latest('upload_date').upload_date,Acceptance_Status_Accepted_Offered_Pending="Pending")
#      if ownership_str =='':
          
#           objs_F=objs.filter(CIRCLE=circle,Ageing=ageing)
#      else:
#           objs_F=performanceAT.objects.filter(CIRCLE=circle,Ageing=ageing,Ownership__in=ownership)
#      site_list = objs_F.values_list('SITE_ID', flat=True)
#      print("---------------------------",site_list)
#      return Response({"status":True,"site_list":site_list})

     
def circle_list(objs):
    cir=[]
    
    for obj in objs:
        cir.append(obj.CIRCLE)

    cir_set=set(cir)
    cir=list(cir_set)
    return cir

def ownership(objs):
#      objs=performanceAT.objects.all()
     owner=[]
    
     for obj in objs:
        owner.append(obj.Ownership)

     owner_set=set(owner)
     owner=list(owner_set)
     return owner
      

@ api_view(["POST"])
def performanceAT_Report_Upload(request):
    
    performance_At_upload_status.objects.all().delete()
    AT = request.FILES["performance_At_Report_file"] if 'performance_At_Report_file' in request.FILES else None
    if AT:
            location = MEDIA_ROOT + r"\ATP\temporary_files"
            fs = FileSystemStorage(location=location)
            file = fs.save(AT.name, AT)
            # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
            filepath = fs.path(file)
            print("file_path:-",filepath)
            df=pd.read_excel(filepath,sheet_name="Data") # should do something if a csv file is coming from the frontend and the csv file should be deleted from the temp files
            os.remove(path=filepath)
            print(filepath,"deleted........")
            print(df)
            upload_date=request.POST.get("upload_date")
            print("upload date is......................",upload_date)

            df_header_list= df.columns.tolist()
            print("Header Name-------------------",df_header_list)
            required_header_list=["CIRCLE","SITE_ID","UNIQUE ID","Project ","OEM_NAME (Nokia/ZTE/Ericsson/Huawei)","MS1","Internal Ms1 Vs Ms2-In days","Ownership","Ageing","Only KPI AT pending","Workable date ( If pending due to other reason)","Reason of new workable date","No of Pending layers","Status","Acceptance Date","Impacted KPI's","Analysis","Action plan/Remarks","RCA for high Ageing","TAT","Ownership","Ownership(Mcom-Internal)","Tool Bucket"]
            for header_name in required_header_list:
                if header_name in df_header_list:
                     pass
                else:
                     message= "Did not get " + header_name + " Column in the uploaded Report"
                     return Response({"status":False,"message":message})

            for i, d in df.iterrows():
                # try:
                    # if pd.isnull(d["CIRCLE"]) or pd.isnull(d["UNQUI ID"]) or pd.isnull(d["SITE_ID"]) or pd.isnull(d["Circle Project"]) or pd.isnull(d["RFAI_DATE"]) or pd.isnull(["OA_(COMMERCIAL_TRAFFIC_PUT_ON_AIR)_(MS1)_DATE"]) or pd.isnull(d["Status"] or pd.isnull("Date")):

                    pk=str(d["CIRCLE"])+str(d["SITE_ID"])+str(d["UNIQUE ID"])+str(upload_date)
                    if pd.isnull(d['Workable date ( If pending due to other reason)']):
                           Workable_date_If_pending_due_to_other_reason=None    
                    else:
                           Workable_date_If_pending_due_to_other_reason=(d["Workable date ( If pending due to other reason)"])

                    if pd.isnull(d['MS1']) :
                          MS1=None
                    else:
                          MS1=(d['MS1']) 
                    if pd.isnull(d['TAT']) :
                          TAT=None
                    else:
                          TAT=(d['TAT'])          
                    if pd.isnull(d['Acceptance Date']) :
                         Acceptance_Date=None
                    else:
                          Acceptance_Date=(d['Acceptance Date'])               
                    try:
                        obj=performanceAT.objects.update_or_create(id=pk,upload_date=upload_date,
                                                        defaults={"CIRCLE":str(d["CIRCLE"]),
                                                        "SITE_ID":str(d["SITE_ID"]),
                                                        "UNIQUE_ID":str(d["UNIQUE ID"]),
                                                        "OEM_NAME_Nokia_ZTE_Ericsson_Huawei":str(d["OEM_NAME (Nokia/ZTE/Ericsson/Huawei)"]),
                                                        "Project":str(d["Project "]),
                                                        "MS1":MS1,
                                                        "Ageing":str(d["Ageing"]),
                                                        "Internal_Ms1_Vs_Ms2_n_days":str(d["Internal Ms1 Vs Ms2-In days"]),
                                                        "Only_KPI_AT_pending":str(d["Only KPI AT pending"]),
                                                        "Workable_date_If_pending_due_to_other_reason":Workable_date_If_pending_due_to_other_reason,  
                                                        "Reason_of_new_workable_date":str(d["Reason of new workable date"]),
                                                        
                                                        "No_of_Pending_layers":str(d["No of Pending layers"]),
                                                        
                                                        "Status":str(d["Status"]),
                                                        "Acceptance_Date":Acceptance_Date,
                                                        "Impacted_KPIs":str(d["Impacted KPI's"]),
                                                        
                                                        "Analysis":str(d["Analysis"]),
                                                        "Action_plan_Remarks":str(d["Action plan/Remarks"]),
                                                        "RCA_for_high_Ageing":str(d["RCA for high Ageing"]),
                                                         
                                                        "TAT":TAT,
                                                        "Ownership":str(d["Ownership"]),
                                                        "Ownership_Mcom_Internal":str(d["Ownership(Mcom-Internal)"]),
                                                        "Tool_Bucket":str(d["Tool Bucket"]),
                                                        "upload_date":upload_date,}



                                                        
                                                        )
                        
                    except Exception as e:
                            print(e)
                            error=str(e)
                            performance_At_upload_status.objects.create(id=pk,Site_id=d["SITE_ID"],update_status="Not Uploaded",Remark=error)
                            continue 

            objs=performance_At_upload_status.objects.all()
            serializers=ser_performance_At_upload_status(objs,many=True)
                 


            return Response({"status": True,"message":"Report uploaded Successfully .","status_obj":serializers.data})
    else:
         return Response({"status": False,"message":"No report file Sent"})
    

def df_raw_column_total(data):
        # print("_________________circle_wise_data_____________________________________")
        print(data)
        df=pd.DataFrame(data)
        df=df.T
        # add a sum row at the bottom of the dataframe
        df.loc['Total'] = df.sum()
        # add a sum column at the right end of the dataframe
        df['Total'] = df.sum(axis=1)
        json_data = df.to_json(orient='index') # here json_data  converts the dataframe to a string json
        json_data=json.loads(json_data) # json.loads - Which converts the string form of json data to a dictionary in python.
        print(df)
        return(json_data)
def df_raw_column_total_circle_wise(data):
        print("_________________circle_wise_data_____________________________________")
        print(data)
        df=pd.DataFrame(data)
        df=df.T
        print("---------------------------dataframe------------------------",df)
        # add a sum row at the bottom of the dataframe
        df.loc['Total'] = df.sum()
        # add a sum column at the right end of the dataframe
        df['Total'] = df["Accepted"]+ df["Pending"] +df["Offered"]+df["Dismantle"]
        json_data = df.to_json(orient='index') # here json_data  converts the dataframe to a string json
        json_data=json.loads(json_data) # json.loads - Which converts the string form of json data to a dictionary in python.
        print(df)
        return(json_data)

@api_view(["GET","POST"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def PerformanceAT_Circlewise_Dashboard(request):
       print("Current_User---------------",request.user)
       str_Date=request.POST.get("Date")
       month=request.POST.get("month")
       week=request.POST.get("week")
       year=request.POST.get("year")
       str_from_date=request.POST.get("from_date")
       str_to_date=request.POST.get("to_date")
       Project=request.POST.get("project")
       Projects=Project.split(",")
       
       print("Project-----",Project)
       print("Projects------",Projects)
       print("month:-----",month)
       print("date:-----",str_Date)
       print("week:---",week)
       print("year:---",year)
       print("str_from_date:---",str_from_date)
       print("str_to_date---",str_to_date)
       
       
       year=int(year)
       objs=performanceAT.objects.all()
       circles= circle_list(objs)
       print("Circle_list: ",circles)
       data={}
       for circle in circles:
            if Project != "":
               obj=performanceAT.objects.filter(CIRCLE=circle,Project__in=Projects)
            else:     
                obj=performanceAT.objects.filter(CIRCLE=circle)
            if str_Date != "":
                print("___________Inside Date___________")
                Date=datetime.datetime.strptime(str_Date,"%Y-%m-%d").date()
                print(Date)
                Accepted=obj.filter(Status__iexact="Accepted", upload_date=Date).count()
                Offered=obj.filter(Status__iexact="offered",upload_date=Date).count()
                Pending=obj.filter(Status__iexact= "Pending",upload_date=Date).count()
                Dismantle=obj.filter(Status__iexact="Dismantle",upload_date=Date).count()
                
            elif month != "":
                
                print("___________Inside Month___________")
                print(month)
                
                Accepted=obj.filter(Status__iexact="Accepted",Upload_date__month=month,Upload_date__year=year).count()
                
                month_obj=obj.filter(Upload_date__month=month,Upload_date__year=year)
                
                if(len(month_obj)!=0):
                    obj=month_obj.filter(Upload_date=month_obj.latest("Upload_date").Upload_date)

                    Dismantle=obj.filter(Status__iexact="Dismantle").count()
                    Offered=obj.filter(Status__iexact="Offered").count()
                    Pending=obj.filter(Status__iexact= "Pending").count()
                else:
                    Dismantle=0
                    Offered=0
                    Pending=0

            elif week != "":
                
                print("___________Inside week___________")
                week=int(week)
                Accepted=obj.filter(Status__iexact="Accepted",Upload_date__week=week,Upload_date__year=year).count()
                week_obj=obj.filter(Upload_date__week=week,Upload_date__year=year)
                if(len(week_obj)!=0):
                    
                    obj=week_obj.filter(Upload_date=week_obj.latest("Upload_date").Upload_date)
                    Dismantle=obj.filter(Status__iexact="Dismantle").count()
                    Offered=obj.filter(Status__iexact="Offered").count()
                    Pending=obj.filter(Status__iexact= "Pending").count()
                else:
                    Dismantle=0
                    Offered=0
                    Pending=0
            elif str_from_date != "" and str_to_date != "":
                
                print("___________Inside from and to ___________")
                from_date=datetime.datetime.strptime(str_from_date,"%Y-%m-%d").date()
                to_date=datetime.datetime.strptime(str_to_date,"%Y-%m-%d").date()
                print("from_date",from_date)
                print("to_date",to_date)

                
                
                Accepted=obj.filter(Status__iexact="Accepted",Upload_date__range=(from_date,to_date)).count()
                Dismantle=obj.filter(Status__iexact="Dismantle",Upload_date=to_date).count()
                Offered=obj.filter(Status__iexact="Offered",Upload_date=to_date).count()
                Pending=obj.filter(Status__iexact= "Pending",Upload_date=to_date).count()


            else:
                print("_________________Inside All_______________")
                Accepted=obj.filter(Status__iexact="Accepted").count()
                Offered=obj.filter(Status__iexact="Offered",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
                Pending=obj.filter(Status__iexact= "Pending",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
                Dismantle=obj.filter(Status__iexact="Dismantle",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
               
                                      



            total=Accepted +  Offered +  Pending + Dismantle
            print(circle,total)

            data[circle]={"Accepted":Accepted,"Dismantled":Dismantle,"Offered":Offered,"Pending":Pending}
       print("__________________________data________________",data)
       if len(data)!=0:
            data1=df_raw_column_total(data)
       else:
            return Response({"status":False,"message":"Database is empty"})


         
      

####################################### PENDING REASON ###############################################################
       pending_sites_ownership={}
       circles=circle_list(objs)
       print('________________circles________________',circles)
       for circle in circles: 
            if Project != "":
               obj=performanceAT.objects.filter(CIRCLE=circle,Project__in=Projects)
            else:     
                obj=performanceAT.objects.filter(CIRCLE=circle)
            if str_Date != "":
                obj=obj.filter(upload_date=Date)
            elif month != "":
                obj=obj.filter(Upload_date__month=month,Upload_date__year=year)

            elif week != "":
                
                print("___________Inside week___________")
                week=int(week)
                obj=obj.filter(Upload_date__week=week,Upload_date__year=year)   

            elif str_from_date != "" and str_to_date != "":
                
                print("___________Inside from and to ___________")
                from_date=datetime.datetime.strptime(str_from_date,"%Y-%m-%d").date()
                to_date=datetime.datetime.strptime(str_to_date,"%Y-%m-%d").date()  
                obj=obj.filter(Upload_date__range=(from_date,to_date))
            else:
                obj=performanceAT.objects.filter(CIRCLE=circle)
            objs=obj
            Airtel_Toco=objs.filter(Status__iexact="Pending",Ownership = "Airtel_Toco").count()
            Mcom_RNO=objs.filter(Status__iexact="Pending",Ownership = "Mcom_RNO").count()
            Mcom_SCFT_team=objs.filter(Status__iexact="Pending",Ownership = "Mcom_SCFT_team").count()
            Mcom_Circle_Team=objs.filter(Status__iexact="Pending",Ownership = "Mcom_Circle_Team").count()
            Mcom_Operations=objs.filter(Status__iexact="Pending",Ownership = "Mcom_Operations").count()
            SCFT_team =objs.filter(Status__iexact="Pending",Ownership = "SCFT_team").count()
            Integration_Team=objs.filter(Status__iexact="Pending",Ownership = "Integration_Team").count() 
            Mcom_Tx_Issue=objs.filter(Status__iexact="Pending",Ownership = "Mcom_Tx_Issue").count()  
            Mcom_RNO=objs.filter(Status__iexact="Pending",Ownership = "Mcom_RNO").count()  


            pending_sites_ownership[circle]={"Airtel_Toco":Airtel_Toco,
                                    "Mcom_RNO":Mcom_RNO,
                                    "Mcom_SCFT_team":Mcom_SCFT_team,
                                    "Mcom_Circle_Team":Mcom_Circle_Team,
                                    "Mcom_Operations":Mcom_Operations,
                                    "SCFT_team":SCFT_team,
                                    "Integration_Team":Integration_Team,
                                    "Mcom_Tx_Issue":Mcom_Tx_Issue,
                                    # "Mcom_RNO":Mcom_RNO

                                     }
       # ageing_circleWise_data = df_raw_column_total(ageing_circleWise)
       pending_sites_ownership=df_raw_column_total(pending_sites_ownership)

       
################################################# pending reason (tool Bucket) #########################################################
       if Project != "":
            obj=performanceAT.objects.filter(Project__in=Projects)
       else:     
            obj=performanceAT.objects.all()
       if str_Date != "":
            obj=obj.filter(upload_date=Date)
       elif month != "":
          obj=obj.filter(Upload_date__month=month,Upload_date__year=year)

       elif week != "":
        
         print("___________Inside week___________")
         week=int(week)
         obj=obj.filter(Upload_date__week=week,Upload_date__year=year)   

       elif str_from_date != "" and str_to_date != "":
        
         print("___________Inside from and to ___________")
         from_date=datetime.datetime.strptime(str_from_date,"%Y-%m-%d").date()
         to_date=datetime.datetime.strptime(str_to_date,"%Y-%m-%d").date()  
         obj=obj.filter(Upload_date__range=(from_date,to_date))
       else:
         obj=performanceAT.objects.all()
       objs=obj

       objs=performanceAT.objects.all()

       objs=objs.filter(Status__iexact= "Pending")
       Accepted=objs.filter(Tool_Bucket="Accepted",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
       Toco_Issues=objs.filter(Tool_Bucket="Toco_Issues",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
       Offered_to_MSP=objs.filter(Tool_Bucket="Offered_to_MSP",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
       SCFT_Pending=objs.filter(Tool_Bucket="SCFT_Pending",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
       Phy_Optimization=objs.filter(Tool_Bucket="Phy_Optimization",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
       HW_Issues=objs.filter(Tool_Bucket="HW_Issues",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
       Site_Down_Sec_Down=objs.filter(Tool_Bucket="Site_Down/Sec_Down",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
       Under_observation=objs.filter(Tool_Bucket="Under_observation",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
       RNA=objs.filter(Tool_Bucket="RNA",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()

       Exclusion_Required=objs.filter(Tool_Bucket="Exclusion_Required",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
       Soft_Parameter_Opti=objs.filter(Tool_Bucket="Soft_Parameter_Opti",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
       Multiple_KPI_Issues=objs.filter(Tool_Bucket="Multiple_KPI_Issues",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
       Ready_for_Offer=objs.filter(Tool_Bucket="Ready_for_Offer",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
       Media_Issues=objs.filter(Tool_Bucket="Media_Issues",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
       Dismantle=objs.filter(Tool_Bucket="Dismantle",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
       Reporting_Issue=objs.filter(Tool_Bucket="Reporting_Issue",upload_date=performanceAT.objects.latest('upload_date').upload_date).count()
      


       total= Accepted + Offered_to_MSP +  Ready_for_Offer + Exclusion_Required  + Multiple_KPI_Issues + Soft_Parameter_Opti + Under_observation + HW_Issues +Media_Issues + Phy_Optimization + Reporting_Issue + RNA +SCFT_Pending +Site_Down_Sec_Down +Toco_Issues + Dismantle
       print("____________total____________",total)
       alarm_Reasonization={}
  
       alarm_Reasonization["Accepted"]={"Count_of_Pending_Reason":Accepted}
       alarm_Reasonization["Offered_to_MSP"]={"Count_of_Pending_Reason":Offered_to_MSP}
       alarm_Reasonization["Ready_for_Offer"]={"Count_of_Pending_Reason":Ready_for_Offer}
       alarm_Reasonization["Exclusion_Required"]={"Count_of_Pending_Reason":Exclusion_Required}
       alarm_Reasonization["Multiple_KPI_Issues"]={"Count_of_Pending_Reason":Multiple_KPI_Issues}
       alarm_Reasonization["Soft_Parameter_Opti"]={"Count_of_Pending_Reason":Soft_Parameter_Opti}
       alarm_Reasonization["Under_observation"]={"Count_of_Pending_Reason":Under_observation}
       alarm_Reasonization["HW_Issues"]={"Count_of_Pending_Reason":HW_Issues}
       alarm_Reasonization["Media_Issues"]={"Count_of_Pending_Reason":Media_Issues}

       alarm_Reasonization["Phy_Optimization"]={"Count_of_Pending_Reason":Phy_Optimization}
       alarm_Reasonization["Reporting_Issue"]={"Count_of_Pending_Reason":Reporting_Issue}
       alarm_Reasonization["RNA"]={"Count_of_Pending_Reason":RNA}
       alarm_Reasonization["SCFT_Pending"]={"Count_of_Pending_Reason":SCFT_Pending}
       alarm_Reasonization["Site_Down_Sec_Down"]={"Count_of_Pending_Reason":Site_Down_Sec_Down}
       alarm_Reasonization["Toco_Issues"]={"Count_of_Pending_Reason":Toco_Issues}
       alarm_Reasonization["Dismantle"]={"Count_of_Pending_Reason":Dismantle}
       

       alarm_Reasonization["Grand_Total"]={"Count_of_Pending_Reason":total}
#        alarm_Reasonization=df_raw_column_total(alarm_Reasonization)
       print("------------------------------------------------------ Alarm Reasonization ---------------------------------------",alarm_Reasonization)
       
######################################## AGEING(CIRCLE WISE) ########################################################################
       ageing_circleWise={}
       for circle in circles:
            if Project != "":
               obj=performanceAT.objects.filter(CIRCLE=circle,Project__in=Projects)
            else:     
                obj=performanceAT.objects.filter(CIRCLE=circle)
            if str_Date != "":
                obj=obj.filter(upload_date=Date)
            elif month != "":
                obj=obj.filter(Upload_date__month=month,Upload_date__year=year)

            elif week != "":
                
                print("___________Inside week___________")
                week=int(week)
                obj=obj.filter(Upload_date__week=week,Upload_date__year=year)   

            elif str_from_date != "" and str_to_date != "":
                
                print("___________Inside from and to ___________")
                from_date=datetime.datetime.strptime(str_from_date,"%Y-%m-%d").date()
                to_date=datetime.datetime.strptime(str_to_date,"%Y-%m-%d").date()  
                obj=obj.filter(Upload_date__range=(from_date,to_date))
            else:
                obj=performanceAT.objects.filter(CIRCLE=circle)
            objs=obj 
            obj=performanceAT.objects.filter(CIRCLE=circle).filter(upload_date=performanceAT.objects.latest('upload_date').upload_date)
            ageing_0_15=obj.filter(Status__iexact="Pending",Internal_Ms1_Vs_Ms2_n_days = "0-15").count()
            ageing_16_30=obj.filter(Status__iexact="Pending",Internal_Ms1_Vs_Ms2_n_days = "16-30").count()
            ageing_31_60=obj.filter(Status__iexact="Pending",Internal_Ms1_Vs_Ms2_n_days = "31-60").count()
            ageing_61_90=obj.filter(Status__iexact="Pending",Internal_Ms1_Vs_Ms2_n_days = "61-90").count()
            ageing_91_120=obj.filter(Status__iexact="Pending",Internal_Ms1_Vs_Ms2_n_days = "91-120").count()
            ageing_GT120=obj.filter(Status__iexact="Pending",Internal_Ms1_Vs_Ms2_n_days = "GT120").count()   

            ageing_circleWise[circle]={"ageing_0_15":ageing_0_15,
                                    "ageing_16_30":ageing_16_30,
                                    "ageing_31_60":ageing_31_60,
                                    "ageing_61_90":ageing_61_90,
                                    "ageing_91_120":ageing_91_120,
                                     "ageing_GT120":ageing_GT120,
                                     }
       ageing_circleWise_data = df_raw_column_total(ageing_circleWise)

      
       Latest_date = performanceAT.objects.latest('upload_date').upload_date
       
       objs=performanceAT.objects.all()
       owner=ownership(objs)
       return Response({"status":True,"message":"successfully","Data":data1,"ownership":pending_sites_ownership,"alarm_Reasonization":alarm_Reasonization,"ageing_circleWise_data":ageing_circleWise_data,"latest_date":Latest_date,"Ownerships":owner})

     

#############################################################################################
@api_view(["GET","POST"])
def ownership_wise_pending_ageing(request):
     ownership=request.POST.get("ownership")

     
     ownership=ownership.split(",")
     print("------------------------------ownership",ownership)
     objs=performanceAT.objects.all()
     circles= circle_list(objs)
     
     pending_ageingwise_dict={}
     for circle in circles:
            obj=performanceAT.objects.filter(CIRCLE=circle).filter(upload_date=performanceAT.objects.latest('upload_date').upload_date)
            ageing_0_15=obj.filter(Acceptance_Status_Accepted_Offered_Pending="Pending",Ageing = "0-15",Ownership__in = ownership).count()
            ageing_16_30=obj.filter(Acceptance_Status_Accepted_Offered_Pending="Pending",Ageing = "16-30",Ownership__in = ownership).count()
            ageing_31_60=obj.filter(Acceptance_Status_Accepted_Offered_Pending="Pending",Ageing = "31-60",Ownership__in = ownership).count()
            ageing_61_90=obj.filter(Acceptance_Status_Accepted_Offered_Pending="Pending",Ageing = "61-90",Ownership__in = ownership).count()
            ageing_91_120=obj.filter(Acceptance_Status_Accepted_Offered_Pending="Pending",Ageing = "91-120",Ownership__in = ownership).count()

            ageing_GT120=obj.filter(Acceptance_Status_Accepted_Offered_Pending="Pending",Ageing = "GT120",Ownership__in = ownership).count()


            pending_ageingwise_dict[circle]={"ageing_0_15":ageing_0_15,
                                        "ageing_16_30":ageing_16_30,
                                        "ageing_31_60":ageing_31_60,
                                        "ageing_61_90":ageing_61_90,
                                        "ageing_91_90":ageing_91_120,
                                        "ageing_GT120":ageing_GT120}  

     pending_ageingWise= df_raw_column_total(pending_ageingwise_dict)

     print(pending_ageingWise)

     # return Response({"status":True,"ageing_pendingWise_SCFT_Team":ageing_pendingWise_SCFT_Team})

     return Response({"status":True,"message":"successfully","pending_ageingWise":pending_ageingWise,
                      })
@api_view(["GET","POST"])
def site_list_request_handler(request):
     ownership_str= request.POST.get("ownership")
    #  ownership=ownership_str.split(",")
     print(ownership)
     circle= request.POST.get("circle")
     print(circle)
     ageing= request.POST.get("ageing")
     print(ageing)
     objs=performanceAT.objects.filter(upload_date=performanceAT.objects.latest('upload_date').upload_date,Status="Pending")
     if ownership_str =='':
          
          objs_F=objs.filter(CIRCLE=circle,Ageing=ageing)
     else:
          objs_F=performanceAT.objects.filter(CIRCLE=circle,Ageing=ageing,Ownership__in=ownership_str)
     site_list = objs_F.values_list('SITE_ID', flat=True)
     print("---------------------------",site_list)
     return Response({"status":True,"site_list":site_list})

@api_view(["GET"])
def filter_by_tool_bucket(request):
    try:
        tool_bucket = request.GET.get('tool_bucket')

        queryset = performanceAT.objects.all()

        if tool_bucket:
            queryset = queryset.filter(Tool_Bucket=tool_bucket)

        data = {}
        for item in queryset:
            circle = item.CIRCLE
            internal_ms1_vs_ms2 = item.Internal_Ms1_Vs_Ms2_n_days
            tool_bucket = item.Tool_Bucket

            if tool_bucket not in data:
                data[tool_bucket] = {}

            if circle not in data[tool_bucket]:
                data[tool_bucket][circle] = {}

            if internal_ms1_vs_ms2 not in data[tool_bucket][circle]:
                data[tool_bucket][circle][internal_ms1_vs_ms2] = 0

            data[tool_bucket][circle][internal_ms1_vs_ms2] += 1

        # Transform the data for the horizontal bar chart
        chart_data = []
        for tool_bucket, circle_data in data.items():
            counts_by_ageing = []
            for circle, counts in circle_data.items():
                counts_by_ageing.append({
                    "CIRCLE": circle,
                    "counts": counts,
                })

            chart_data.append({
                "Tool_Bucket": tool_bucket,
                "counts_by_ageing": counts_by_ageing,
            })

        return Response({"status": True, "data": chart_data})

    except Exception as e:
        return Response({"status": False, "message": str(e)})

          

# Nishant... Verma...



