from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from rest_framework.decorators import api_view
from mcom_website.settings import MEDIA_ROOT,MEDIA_URL
from rest_framework.response import Response

from django.core.files.storage import FileSystemStorage
import pandas as pd
import os
from .models import *   
import datetime
# Create your views here.
import json
from .serializers import * 

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes,permission_classes

from commom_utilities.utils import *

def circle_list(objs):
    cir=[]
    
    for obj in objs:
        cir.append(obj.CIRCLE)

    cir_set=set(cir)
    cir=list(cir_set)
    return cir

@ api_view(["GET"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def softAtTemplate(request):
    print("Current_User---------------",request.user)
    download_path= os.path.join(MEDIA_URL,"Soft_AT","templates","Soft_At_Template.xlsx")
    return Response({"status":True, "message":"Downloaded Sucessfully","Download_url":download_path})




@ api_view(["POST"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def SoftAt_Report_Upload(request):
    print("Current_User---------------",request.user)
    Soft_At_upload_status.objects.all().delete()
    Soft_At_report_file = request.FILES["Soft_At_report_file"] if 'Soft_At_report_file' in request.FILES else None
    if Soft_At_report_file:
            location = MEDIA_ROOT + r"\Soft_AT\temporary_files"
            fs = FileSystemStorage(location=location)
            file = fs.save(Soft_At_report_file.name, Soft_At_report_file)
            # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
            filepath = fs.path(file)
            print("file_path:-",filepath)
            df=pd.read_excel(filepath) # should do something if a csv file is coming from the frontend and the csv file should be deleted from the temp files
            os.remove(path=filepath)
            print(filepath,"deleted........")
            print(df)
            upload_date=request.POST.get("upload_date")
            print("upload date is......................",upload_date)
            
            ############################### Code for checking  if the report upoaded have all the necessary columns or not ######################
            df_header_list= df.columns.tolist()
            print("Header Name-------------------",df_header_list)
            required_header_list=["CIRCLE","SITE_ID","UNIQUE ID","ENODEB_ID","BAND","Project","OEM_NAME","Bucket","Alarm Bucket","Status","Ageing",'Date',"Remarks"]
            # required_header_list=["CIRCLE","SITE_ID","UNIQUE ID","Project","OEM_NAME","Alarm Bucket","Status","Ageing",'Date',"Remarks"]
            # for header_name in required_header_list:
            #     if header_name in df_header_list:
            #          pass
            #     else:
            #          message= "Did not get " + header_name + " Column in the uploaded Report"
            #          return Response({"status":False,"message":message})
                
            sts,response=required_col_check(Soft_At_report_file,required_header_list)
            if sts:
                 return Response(response)
        

           
            ######################################################################################################################################

            for i, d in df.iterrows():
                
                    pk=str(d["CIRCLE"])+str(d["SITE_ID"])+str(d["BAND"])+str(d["OEM_NAME"]) +str(upload_date)
                    # pk=str(d["CIRCLE"])+str(d["SITE_ID"])+str(d["OEM_NAME"]) +str(upload_date)
                    if pd.isnull(d['Date']):
                           Date=None
                    else:
                           Date=(d["Date"])
                    try:
                        obj,created=Soft_At_Table.objects.update_or_create(id=pk,Upload_date=upload_date,
                                                     defaults={"CIRCLE":str(d["CIRCLE"]),
                                                        "SITE_ID":str(d["SITE_ID"]),
                                                        # "UNIQUE_ID":str(d["UNIQUE ID"]),
                                                        "ENODEB_ID":str(d["ENODEB_ID"]),
                                                        # "BAND":str(d["BAND"]),
                                                        "Circle_Project":str(d["Project"]),  #changed from circle project to project
                                                        "OEM_NAME":(d["OEM_NAME"]),
                                                        "Pending_Bucket":str(d["Bucket"]),
                                                        "Alarm_Bucket":str(d["Alarm Bucket"]),
                                                        "Status":str(d["Status"]),
                                                        "Ageing":str(d["Ageing"]),
                                                        "Date":Date,
                                                        "Remarks":str(d["Remarks"]),
                                                        "Upload_date":upload_date, }   # we provide a date in string formate to a date field of models
                                                        )
                        
                    except Exception as e:
                            print("error",e)
                            error=str(e)
                            Soft_At_upload_status.objects.create(id=pk,Site_id=d["SITE_ID"],update_status="Not Uploaded",Remark=error)
                            continue 
                
            objs=Soft_At_upload_status.objects.all()
            serializers=ser_Soft_At_upload_status(objs,many=True)          


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
        df['Total'] = df["Accepted"] + df["Rejected"] +df["Dismantle"] + df["Pending"] + df["Need_to_be_offer"] +df["offered"]
        json_data = df.to_json(orient='index') # here json_data  converts the dataframe to a string json
        json_data=json.loads(json_data) # json.loads - Which converts the string form of json data to a dictionary in python.
        print(df)
        return(json_data)
     

def pending_sites_bucketization(objs):
      ################### code for pending sites bucketization ###################
       
       Circle_Team=objs.filter(Status="Pending", Pending_Bucket = "Circle Team").count()
       Circle_Team_NOC_Team=objs.filter(Status="Pending", Pending_Bucket = "Circle/NOC Team").count()
       circle_Team_Media_team=objs.filter(Status="Pending", Pending_Bucket = "Circle/Media team").count()
       NOC_Team=objs.filter(Status="Pending", Pending_Bucket = "NOC Team").count()
       pending_sites_bucketization={}
       pending_sites_bucketization["Pending"]={
                                    "Circle_Team":Circle_Team,
                                    "Circle_Team_NOC_Team":Circle_Team_NOC_Team,
                                    "circle_Team_Media_team":circle_Team_Media_team,
                                    "NOC_Team":NOC_Team,
                                    }
       pending_sites_bucketization=df_raw_column_total(pending_sites_bucketization)
       return pending_sites_bucketization

def Alarm_Bucket(objs):
     ################## Alarm_Bucket Code #########################

       objs=objs.filter(Status__iexact= "Pending")
       Configuration_issue=objs.filter(Alarm_Bucket="Configuration issue").count()
       GTPU_Trxmn_S1_Link_Alarm=objs.filter(Alarm_Bucket="GTPU/Trxmn/S1 Link Alarm").count()
       HW_Alarms=objs.filter(Alarm_Bucket="HW Alarms").count()
       License_Capacity_Software_Issue=objs.filter(Alarm_Bucket="License Capacity/Software Issue").count()
       Service_affecting_alarm=objs.filter(Alarm_Bucket="Service affecting alarm").count()
       Sites_Locked_Down_Ping_Not_OK_Upload_Failed_Login_Failed=objs.filter(Alarm_Bucket="Sites Locked/Down/Ping Not OK/Upload Failed/Login Failed").count()
       Sync_Issue_GPS_TOP=objs.filter(Alarm_Bucket="Sync Issue - GPS/TOP").count()
       TWAMP_Issue=objs.filter(Alarm_Bucket="TWAMP Issue").count()
       VSWR_High_Config_Issue=objs.filter(Alarm_Bucket="VSWR High/Config Issue").count()

       Cell_Nomenclature_Issue=objs.filter(Alarm_Bucket="Cell Nomenclature Issue").count()
       Incomplete_AT_details_OSS_MRBTS_BSC_BCF_LAC_IP=objs.filter(Alarm_Bucket="Incomplete AT details(OSS/MRBTS/BSC/BCF/LAC/IP)").count()
       Zero_Low_Traffic=objs.filter(Alarm_Bucket="Zero /Low Traffic").count()
       CFR_MHT_Working_SDCCH_CH_CONGESTION_TCH_Interference=objs.filter(Alarm_Bucket="CFR/MHT/Working SDCCH/CH CONGESTION/TCH Interference").count()
       History_Alarm=objs.filter(Alarm_Bucket="History Alarm").count()
       Non_Operational_Cell=objs.filter(Alarm_Bucket="Non Operational Cell").count()
       GPL_Deviation_Issue=objs.filter(Alarm_Bucket="GPL Deviation Issue").count()
       UBR_AT_Dependency=objs.filter(Alarm_Bucket="UBR AT Dependency").count()



       total= Configuration_issue + GTPU_Trxmn_S1_Link_Alarm + HW_Alarms + License_Capacity_Software_Issue  + Service_affecting_alarm + Sites_Locked_Down_Ping_Not_OK_Upload_Failed_Login_Failed + Sync_Issue_GPS_TOP + TWAMP_Issue +VSWR_High_Config_Issue + Cell_Nomenclature_Issue + Incomplete_AT_details_OSS_MRBTS_BSC_BCF_LAC_IP + Zero_Low_Traffic +CFR_MHT_Working_SDCCH_CH_CONGESTION_TCH_Interference +History_Alarm +Non_Operational_Cell + GPL_Deviation_Issue + UBR_AT_Dependency
      
       alarm_bucketization={}
  
       alarm_bucketization["Configuration issue"]={"Count_of_Alarm_Bucket":Configuration_issue}
       alarm_bucketization["GTPU/Trxmn/S1 Link Alarm"]={"Count_of_Alarm_Bucket":GTPU_Trxmn_S1_Link_Alarm}
       alarm_bucketization["HW Alarms"]={"Count_of_Alarm_Bucket":HW_Alarms}
       alarm_bucketization["License Capacity/Software Issue"]={"Count_of_Alarm_Bucket":License_Capacity_Software_Issue}
       alarm_bucketization["Service affecting alarm"]={"Count_of_Alarm_Bucket":Service_affecting_alarm}
       alarm_bucketization["Sites Locked/Down/Ping Not OK/Upload Failed/Login Failed"]={"Count_of_Alarm_Bucket":Sites_Locked_Down_Ping_Not_OK_Upload_Failed_Login_Failed}
       alarm_bucketization["Sync Issue - GPS/TOP"]={"Count_of_Alarm_Bucket":Sync_Issue_GPS_TOP}
       alarm_bucketization["TWAMP Issue"]={"Count_of_Alarm_Bucket":TWAMP_Issue}
       alarm_bucketization["VSWR High/Config Issue"]={"Count_of_Alarm_Bucket":VSWR_High_Config_Issue}

       alarm_bucketization["Cell Nomenclature Issue"]={"Count_of_Alarm_Bucket":Cell_Nomenclature_Issue}
       alarm_bucketization["Incomplete AT details(OSS/MRBTS/BSC/BCF/LAC/IP"]={"Count_of_Alarm_Bucket":Incomplete_AT_details_OSS_MRBTS_BSC_BCF_LAC_IP}
       alarm_bucketization["Zero /Low Traffic"]={"Count_of_Alarm_Bucket":Zero_Low_Traffic}
       alarm_bucketization["CFR/MHT/Working SDCCH/CH CONGESTION/TCH Interference"]={"Count_of_Alarm_Bucket":CFR_MHT_Working_SDCCH_CH_CONGESTION_TCH_Interference}
       alarm_bucketization["History Alarm"]={"Count_of_Alarm_Bucket":History_Alarm}
       alarm_bucketization["Non Operational Cell"]={"Count_of_Alarm_Bucket":Non_Operational_Cell}
       alarm_bucketization["GPL Deviation Issue"]={"Count_of_Alarm_Bucket":GPL_Deviation_Issue}
       alarm_bucketization["UBR AT Dependency"]={"Count_of_Alarm_Bucket":UBR_AT_Dependency}
       alarm_bucketization["Grand Total"]={"Count_of_Alarm_Bucket":total}

       return alarm_bucketization 

def pending_ageing(objs):
    #    objs=Soft_At_Table.objects.all()
       circles= circle_list(objs)
      ########################################################## code for pending ageing #######################################################
       ageing_circleWise={}
       for circle in circles:
             
            obj=objs.filter(CIRCLE=circle)
            ageing_0_15=obj.filter(Status="Pending",Ageing = "0-15").count()
            ageing_16_30=obj.filter(Status="Pending",Ageing = "16-30").count()
            ageing_31_60=obj.filter(Status="Pending",Ageing = "31-60").count()
            ageing_61_90=obj.filter(Status="Pending",Ageing = "61-90").count()
            ageing_GT90=obj.filter(Status="Pending",Ageing = "GT90").count()   

            ageing_circleWise[circle]={"ageing_0_15":ageing_0_15,
                                    "ageing_16_30":ageing_16_30,
                                    "ageing_31_60":ageing_31_60,
                                    "ageing_61_90":ageing_61_90,
                                     "ageing_GT90":ageing_GT90,
                                     }
       ageing_circleWise_data = df_raw_column_total(ageing_circleWise)
       return ageing_circleWise_data

@api_view(["GET","POST"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def SoftAt_Circlewise_Dashboard(request):
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
       objs=Soft_At_Table.objects.all()
       circles= circle_list(objs)
       print("Circle_list: ",circles)
       data={}
       for circle in circles:
            if Project != "":
               obj=Soft_At_Table.objects.filter(CIRCLE=circle,Circle_Project__in=Projects)
            else:     
                obj=Soft_At_Table.objects.filter(CIRCLE=circle)
            if str_Date != "":
                print("___________Inside Date___________")
                Date=datetime.datetime.strptime(str_Date,"%Y-%m-%d").date()
                print(Date)
                Accepted=obj.filter(Status__iexact="Accepted", Upload_date=Date).count()
                Dismantle=obj.filter(Status__iexact="Dismantle",Upload_date=Date).count()
                offered=obj.filter(Status__iexact="offered",Upload_date=Date).count()
                Rejected=obj.filter(Status__iexact="Rejected", Upload_date=Date).count()
                Need_to_be_offer=obj.filter(Status__iexact="Need to be offer",Upload_date=Date).count()
                Pending=obj.filter(Status__iexact= "Pending",Upload_date=Date).count()

            elif month != "":
                
                print("___________Inside Month___________")
                print(month)
                
                Accepted=obj.filter(Status__iexact="Accepted",Upload_date__month=month,Upload_date__year=year).count()
                
                month_obj=obj.filter(Upload_date__month=month,Upload_date__year=year)
                
                if(len(month_obj)!=0):
                    obj=month_obj.filter(Upload_date=month_obj.latest("Upload_date").Upload_date)

                    Dismantle=obj.filter(Status__iexact="Dismantle").count()
                    offered=obj.filter(Status__iexact="offered").count()
                    Rejected=obj.filter(Status__iexact="Rejected").count()
                    Need_to_be_offer=obj.filter(Status__iexact="Need to be offer").count()
                    Pending=obj.filter(Status__iexact= "Pending").count()
                else:
                    Dismantle=0
                    offered=0
                    Rejected=0
                    Need_to_be_offer=0
                    Pending=0

            elif week != "":
                
                print("___________Inside week___________")
                week=int(week)
                Accepted=obj.filter(Status__iexact="Accepted",Upload_date__week=week,Upload_date__year=year).count()
                week_obj=obj.filter(Upload_date__week=week,Upload_date__year=year)
                if(len(week_obj)!=0):
                    
                    obj=week_obj.filter(Upload_date=week_obj.latest("Upload_date").Upload_date)
                    Dismantle=obj.filter(Status__iexact="Dismantle").count()
                    offered=obj.filter(Status__iexact="offered").count()
                    Rejected=obj.filter(Status__iexact="Rejected").count()
                    Need_to_be_offer=obj.filter(Status__iexact="Need to be offer").count()
                    Pending=obj.filter(Status__iexact= "Pending").count()
                else:
                    Dismantle=0
                    offered=0
                    Rejected=0
                    Need_to_be_offer=0
                    Pending=0
            elif str_from_date != "" and str_to_date != "":
                
                print("___________Inside from and to ___________")
                from_date=datetime.datetime.strptime(str_from_date,"%Y-%m-%d").date()
                to_date=datetime.datetime.strptime(str_to_date,"%Y-%m-%d").date()
                print("from_date",from_date)
                print("to_date",to_date)

                
                
                Accepted=obj.filter(Status__iexact="Accepted",Upload_date__range=(from_date,to_date)).count()
                Dismantle=obj.filter(Status__iexact="Dismantle",Upload_date=to_date).count()
                offered=obj.filter(Status__iexact="offered",Upload_date=to_date).count()
                Rejected=obj.filter(Status__iexact="Rejected",Upload_date=to_date).count()
                Need_to_be_offer=obj.filter(Status__iexact="Need to be offer",Upload_date=to_date).count()
                Pending=obj.filter(Status__iexact= "Pending",Upload_date=to_date).count()
                  

            else:
                print("_________________Inside All_______________")
                Accepted=obj.filter(Status__iexact="Accepted").count()
                Dismantle=obj.filter(Status__iexact="Dismantle", Upload_date=Soft_At_Table.objects.latest('Upload_date').Upload_date).count()
                offered=obj.filter(Status__iexact="offered",Upload_date=Soft_At_Table.objects.latest('Upload_date').Upload_date).count()
                Rejected=obj.filter(Status__iexact="Rejected",Upload_date=Soft_At_Table.objects.latest('Upload_date').Upload_date).count()
                Need_to_be_offer=obj.filter(Status__iexact="Need to be offer",Upload_date=Soft_At_Table.objects.latest('Upload_date').Upload_date).count()
                Pending=obj.filter(Status__iexact= "Pending",Upload_date=Soft_At_Table.objects.latest('Upload_date').Upload_date).count()
            total=Accepted + Dismantle + offered + Rejected + Need_to_be_offer + Pending
            print(circle,total)
            if total != 0:
                Acceptance_percent=round(Accepted/total,2)
                Rejection_percent=round(Rejected/total,2)
            else:
                Acceptance_percent=0
                Rejection_percent=0
            data[circle]={"Accepted":Accepted,"Dismantle":Dismantle,"offered":offered,"Rejected":Rejected,"Pending":Pending,"Need_to_be_offer":Need_to_be_offer,"Accepted_per":Acceptance_percent,"Rejection_per":Rejection_percent}
       if len(data)!=0:
           data1=df_raw_column_total_circle_wise(data)
       else:
            return Response({"status":False,"message":"Database is empty"})
      

      ######################################### code for filtering of pending_sites/ alarm_bucket / ageing Circle_wise ######################################## 
      
       if Project != "":
               main_obj=Soft_At_Table.objects.filter(Circle_Project__in=Projects)
       else:     
               main_obj=Soft_At_Table.objects.all()
       if str_Date != "":
            Date=datetime.datetime.strptime(str_Date,"%Y-%m-%d").date()
            print(Date)
            Date_objs=main_obj.filter(Upload_date=Date)
            pending_sites_bucketization_data=pending_sites_bucketization(Date_objs)
            alarm_bucketization_data=Alarm_Bucket(Date_objs)
            ageing_circleWise_data=pending_ageing(Date_objs)

       elif month != "":
                print(month) 
                month_objs=obj.filter(Upload_date__month=month,Upload_date__year=year).filter(Upload_date=Soft_At_Table.objects.latest('Upload_date').Upload_date)
                pending_sites_bucketization_data=pending_sites_bucketization(month_objs)
                alarm_bucketization_data=Alarm_Bucket(month_objs)
                ageing_circleWise_data=pending_ageing(month_objs)
      
       elif week != "":
                
                week=int(week)
                week_objs=obj.filter(Upload_date__week=week,Upload_date__year=year).filter(Upload_date=Soft_At_Table.objects.latest('Upload_date').Upload_date)
                pending_sites_bucketization_data=pending_sites_bucketization(week_objs)
                alarm_bucketization_data=Alarm_Bucket(week_objs)
                ageing_circleWise_data=pending_ageing(week_objs)
       elif str_from_date != "" and str_to_date != "":
                
                print("___________Inside from and to ___________")
                from_date=datetime.datetime.strptime(str_from_date,"%Y-%m-%d").date()
                to_date=datetime.datetime.strptime(str_to_date,"%Y-%m-%d").date()
                print("from_date",from_date)
                print("to_date",to_date)

                range_objs = obj.filter( Status__iexact="Accepted", Upload_date = to_date )

                pending_sites_bucketization_data=pending_sites_bucketization(range_objs)
                alarm_bucketization_data=Alarm_Bucket(range_objs)
                ageing_circleWise_data=pending_ageing(range_objs)
        
       else :
            overAll_objs = Soft_At_Table.objects.filter(Upload_date=Soft_At_Table.objects.latest('Upload_date').Upload_date)
            pending_sites_bucketization_data=pending_sites_bucketization(overAll_objs)
            alarm_bucketization_data=Alarm_Bucket(overAll_objs)
            ageing_circleWise_data=pending_ageing(overAll_objs)

       Latest_date = Soft_At_Table.objects.latest('Upload_date').Upload_date
       return Response({"status":True, 
                        "Data":data1,
                        "pending_sites_bucketization":pending_sites_bucketization_data,
                        "alarm_bucketization":alarm_bucketization_data,
                        "ageing_circleWise":ageing_circleWise_data,
                        "Latest_date":Latest_date,
                        })

       
      

@ api_view(["GET"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def View_Soft_At_Report(request):
    print("Current_User---------------",request.user)
    objs=Soft_At_Table.objects.all()
    path="media/Soft_AT/Soft_At_Reports/OverAllSoftAtRreport.xlsx"
    pd.DataFrame(list(objs.values())).to_excel(path,index=False)
    ser=ser_Soft_At_Table(objs,many=True)
    return Response({"status":True,"data":ser.data,"Download_url":path})

@ api_view(["GET","POST"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def weeklyComparision(request):
    print("Current_User---------------",request.user)
    year=request.POST.get("year")
    week=request.POST.get("week")
    print("weekly comparision week----------",week)
    week=int(week)

    objs=Soft_At_Table.objects.all()
    current_week_Accepted=objs.filter(Status__iexact="Accepted",Upload_date__week=week,Upload_date__year=year).count()
    previous_week= week-1

    ##################################### code for pending sites in the current week #######################################
    week_obj=objs.filter(Upload_date__week=week,Upload_date__year=year)
    if(len(week_obj)!=0):
        obj=week_obj.filter(Upload_date=week_obj.latest("Upload_date").Upload_date)
       
        Pendency_of_current_week=obj.filter(Status__iexact= "Pending").count()
    else:
        
        Pendency_of_current_week=0
    
    #################################### code for the pending sites in the previous week ###################################
    week_obj=objs.filter(Upload_date__week=previous_week ,Upload_date__year=year)
    if(len(week_obj)!=0):
        obj=week_obj.filter(Upload_date=week_obj.latest("Upload_date").Upload_date)
       
        Pendency_of_previous_week=obj.filter(Status__iexact = "Pending").count()
       
    else:
        
        Pendency_of_previous_week = 0
        
    print("Pendency of current week----------",Pendency_of_current_week)
    print("Pendency of previous week---------",Pendency_of_previous_week)
    if Pendency_of_previous_week != 0:
        Pendency_change_per= round(((Pendency_of_current_week - Pendency_of_previous_week)/Pendency_of_previous_week)*100,2)
    else:
         Pendency_change_per=0

    pendency_comp_data={
                        "Pendency_change_per":Pendency_change_per,
                        "Pendency_of_previous_week":Pendency_of_previous_week,
                        "Pendency_of_current_week":Pendency_of_current_week,
                        }
    ############################## code for top 3 circles with highest acceptance ##################################################
    objs=Soft_At_Table.objects.all()
    circles= circle_list(objs)
    print("Circle_list: ",circles)
    data={}
    for circle in circles:
            obj=Soft_At_Table.objects.filter(CIRCLE=circle)
            Accepted=obj.filter(Status__iexact="Accepted",Upload_date__week=week,Upload_date__year=year).count()
            data[circle]=Accepted

    # Sort the dictionary items by their values in descending order
    sorted_dict = sorted(data.items(), key=lambda x: x[1], reverse=True)

    # Get the top 3 values
    top_3_circles = sorted_dict[:3]
    print(top_3_circles)
    
    # Print the top 3 values
    for key, value in top_3_circles:
        print(key, value)

    ################################### code for % change in the highest ageing change #####################################
    objs=Soft_At_Table.objects.all()
    previous_week_obj=objs.filter(Upload_date__week=previous_week,Upload_date__year=year)
    if(len(previous_week_obj)!=0):
                    
        obj=previous_week_obj.filter(Upload_date=previous_week_obj.latest("Upload_date").Upload_date)
        ageing_0_15=obj.filter(Status="Pending",Ageing = "0-15").count()
        ageing_16_30=obj.filter(Status="Pending",Ageing = "16-30").count()
        ageing_31_60=obj.filter(Status="Pending",Ageing = "31-60").count()
        ageing_61_90=obj.filter(Status="Pending",Ageing = "61-90").count()
        ageing_GT90=obj.filter(Status="Pending",Ageing = "GT90").count()   
        previous_ageing_dict={"ageing_0_15":ageing_0_15,
                     "ageing_16_30":ageing_16_30,
                     "ageing_31_60":ageing_31_60,
                     "ageing_61_90":ageing_61_90,
                     "ageing_GT90":ageing_GT90,
                                     }
        
        sorted_dict = sorted(previous_ageing_dict.items(), key=lambda x: x[1], reverse=True)

        # Get the top 3 values
        greates_ageing_previous_week = sorted_dict[:1][0][0]
        greates_ageing_previous_week_value = sorted_dict[:1][0][1]
        print("greates_ageing_previous_week-------------------",greates_ageing_previous_week)
    else:
         return Response({"status":False,"message":f"No data of {previous_week} week is present "})
    week_obj=objs.filter(Upload_date__week=week,Upload_date__year=year)
    if(len(week_obj)!=0):
                    
        obj=week_obj.filter(Upload_date=week_obj.latest("Upload_date").Upload_date)
        ageing_0_15=obj.filter(Status="Pending",Ageing = "0-15").count()
        ageing_16_30=obj.filter(Status="Pending",Ageing = "16-30").count()
        ageing_31_60=obj.filter(Status="Pending",Ageing = "31-60").count()
        ageing_61_90=obj.filter(Status="Pending",Ageing = "61-90").count()
        ageing_GT90=obj.filter(Status="Pending",Ageing = "GT90").count()   
        current_ageing_dict={"ageing_0_15":ageing_0_15,
                     "ageing_16_30":ageing_16_30,
                     "ageing_31_60":ageing_31_60,
                     "ageing_61_90":ageing_61_90,
                     "ageing_GT90":ageing_GT90,
                                     }
        corresponding_current_ageing_value=current_ageing_dict[greates_ageing_previous_week]
    else:
         return Response({"status":False,"message":f"No data of {week} week is present "})
    ageing_change_per=round(((corresponding_current_ageing_value - greates_ageing_previous_week_value)/greates_ageing_previous_week_value) * 100,2)
    
    ageing_comp_data={"ageing_change_per":ageing_change_per,
                       "greates_ageing_previous_week":greates_ageing_previous_week,
                       "greates_ageing_previous_week_value":greates_ageing_previous_week_value,
                       "corresponding_current_ageing_value":corresponding_current_ageing_value,
                       }
    ######################################################## code for pendency comparision graph  ####################################################
    
    weekly_pendency_graph={}
    for circle in circles:
        circle_obj=Soft_At_Table.objects.filter(CIRCLE=circle)
        week_obj=circle_obj.filter(Upload_date__week=week,Upload_date__year=year)
        if(len(week_obj)!=0):
           obj=week_obj.filter(Upload_date=week_obj.latest("Upload_date").Upload_date)
           current_week_pendency=obj.filter(Status__iexact = "Pending").count()
        else:
             return Response({"status":False,"message":f"No data of {week} week is present "})
        
        previous_week_obj=circle_obj.filter(Upload_date__week=previous_week,Upload_date__year=year)
        if(len(previous_week_obj)!=0):
           obj=previous_week_obj.filter(Upload_date=previous_week_obj.latest("Upload_date").Upload_date)
           previous_week_pendency=obj.filter(Status__iexact = "Pending").count()
        
    
        else:
             previous_week_pendency = 0
        weekly_pendency_graph[circle]={"current_week_pendency":current_week_pendency,"previous_week_pendency":previous_week_pendency}
    
        
    
    return Response({"status":True,"Accepted":current_week_Accepted,"Pendency_comp_data":pendency_comp_data,"top_3_values":top_3_circles,"ageing_comp_data":ageing_comp_data,"weekly_pendency_graph":weekly_pendency_graph})