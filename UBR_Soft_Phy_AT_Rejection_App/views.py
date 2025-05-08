import win32com.client
from pathlib import Path
import datetime

from datetime import datetime as dt
import pythoncom
import re
import pandas as pd
from django.http import JsonResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from mcom_website.settings import MEDIA_ROOT
from .models import *
from django.core.files.storage import FileSystemStorage
import os
from UBR_Soft_Phy_AT_Rejection_App.serializers import * 
# from Soft_AT_Rejected.utils import subject_filteration
from UBR_Soft_Phy_AT_Rejection_App.utils import *
from django.db.models import Count, Case, When, IntegerField, Sum
# from django.http import JsonResponse
from django.db.models.functions import Cast
from django.db import connection
from UBR_Soft_Phy_AT_Rejection_App.utils import *
import json



@api_view(['GET'])
def save_database(request):
    UBR_Soft_AT_Rejected_save(True,[])   
     
    # Soft_At_Rejection_Database_ERI_save(True,[])
    return Response({"status":True})   



def get_unique_circles():

    obj_soft = list(UBR_Soft_Phy_AT_Rejection_Table.objects.all().values_list('Circle', flat=True).distinct())

    return list(set(obj_soft))





def process_oem_data(oem_model, oem_name, status,circle):
   obj=get_latest_record_per_site(oem_model)
   print("msmsmsmsmsmsmsmms",type(obj))
   circle_count = obj.filter(UBR_Make_OEM=oem_name,Circle=circle, AT_Status__in=status).count()
   return circle_count

@api_view(["GET","POST"])
def Soft_Phy_Rejection_Report(request):
    # Soft_At_Rejection_Database_save(request)
    accepted_and_rejected = request.POST.get("Status")
    print(accepted_and_rejected)
    data = {}

    total_radwin = 0
    total_cambium = 0

    unique_circles = get_unique_circles()

    

    for circle in unique_circles:
            circle_data={}
            if accepted_and_rejected.lower() == "false":
                # data["Status"] = "Rejected"
                # Process Rejected Data
                radwin_data = process_oem_data(
                    oem_model=UBR_Soft_Phy_AT_Rejection_Table,
                    oem_name="RADWIN",
                    status=["REJECTED", "REJECT"],
                    circle= circle
                )   
               
                circle_data["RADWIN"] = radwin_data
                cambium_data = process_oem_data(
                    oem_model=UBR_Soft_Phy_AT_Rejection_Table,
                    oem_name="CAMBIUM",
                    status=["REJECTED", "REJECT"],
                    circle= circle
                )   
               
                circle_data["CAMBIUM"] = cambium_data
            else:
                # data["Status"] = "Accepted"
                # Process Accepted Data
                radwin_data = process_oem_data(
                    oem_model=UBR_Soft_Phy_AT_Rejection_Table,
                    oem_name="RADWIN",
                    status=["ACCEPTED", "ACCEPT"],
                    circle= circle
                )
                circle_data["RADWIN"] = radwin_data

                cambium_data = process_oem_data(
                    oem_model=UBR_Soft_Phy_AT_Rejection_Table,
                    oem_name="CAMBIUM",
                    status=["REJECTED", "REJECT"],
                    circle= circle
                )   
               
                circle_data["CAMBIUM"] = cambium_data 
            
            data[circle] = circle_data  
            

            total_radwin = total_radwin+radwin_data
            total_cambium = total_cambium+cambium_data
            
         
            soft_obj= UBR_Soft_Phy_AT_Rejection_Table.objects.all()

            
            
            min_time_date,max_time_date = get_min_max_date_time(soft_obj)
            
    data["total"] ={"RADWIN":total_radwin, "CAMBIUM": total_cambium}
    
    # get_latest_date()
    
    return Response({
        "message": "Script executed successfully.",
        "status": True,
        "data": data,
        "min_time_date": min_time_date,
        "max_time_date": max_time_date,
    })



@api_view(["GET", "POST"])
def count_of_circle(request):
    oem = request.POST.get("oem")
    circle = request.POST.get("circle")
    status = request.POST.get("status")
    print("front end sts....................", status)
    sts_dict={"true":["ACCEPTED","ACCEPT"], "false":["REJECT","REJECTED"]}
    if(oem == "RADWIN"):
        # obj = Soft_AT_NOKIA_Rejected_Table.objects.filter(Circle=circle, AT_STATUS__in= sts_dict[status])
        obj=get_latest_record_per_site(UBR_Soft_Phy_AT_Rejection_Table)
        obj = obj.filter(UBR_Make_OEM=oem,Circle=circle, AT_Status__in=sts_dict[status])
        serializer_data = ser_UBR_Soft_Phy_AT_Rejection_Table(obj, many=True)

        return Response({
            "Status": True,
            "message": "data sucessfully fetched....",
            "data": serializer_data.data,
        })
    if(oem == "CAMBIUM"):
        # obj = Soft_AT_NOKIA_Rejected_Table.objects.filter(Circle=circle, AT_STATUS__in= sts_dict[status])
        obj=get_latest_record_per_site(UBR_Soft_Phy_AT_Rejection_Table)
        obj = obj.filter(UBR_Make_OEM=oem,Circle=circle, AT_Status__in=sts_dict[status])
        serializer_data = ser_UBR_Soft_Phy_AT_Rejection_Table(obj, many=True)

        return Response({
            "Status": True,
            "message": "data sucessfully fetched....",
            "data": serializer_data.data,
        })
        
    
          

@api_view(["POST"])
def site_wise_view(request):
    site_id = request.POST.get("site_id")
    status = request.POST.get("status")
    print(status,"....................................................................")
    oem = request.POST.get("oem")
    sts_dict={"ACCEPTED": ["ACCEPTED","ACCEPT"], "REJECT":["REJECT","REJECTED"],"REJECTED":["REJECT","REJECTED"]}
    if(oem == "RADWIN"):
        obj = UBR_Soft_Phy_AT_Rejection_Table.objects.filter(UBR_Make_OEM=oem,Site_ID=site_id, AT_Status__in= sts_dict[status])
        # obj = Soft_AT_NOKIA_Rejected_Table.objects.filter(Site_ID=site_id, AT_STATUS =status)
        serializer_data = ser_UBR_Soft_Phy_AT_Rejection_Table(obj, many=True)
        return Response({
            "Status": True,
            "message": "data sucessfully fetched....",
            "data": serializer_data.data,
        }) 
    if(oem == "CAMBIUM"):
        obj = UBR_Soft_Phy_AT_Rejection_Table.objects.filter(UBR_Make_OEM=oem,Site_ID=site_id, AT_Status__in= sts_dict[status])
        # obj = Soft_AT_NOKIA_Rejected_Table.objects.filter(Site_ID=site_id, AT_STATUS =status)
        serializer_data = ser_UBR_Soft_Phy_AT_Rejection_Table(obj, many=True)
        return Response({
            "Status": True,
            "message": "data sucessfully fetched....",
            "data": serializer_data.data,
        }) 
    


@api_view(["POST","GET"])
def master_dashbord_api(request):
    overall_min_date,overall_max_date=("","")
    print("___________MASTER DASHBOARD API ___________")
    str_from_date = request.POST.get("from_date")
    str_to_date = request.POST.get("to_date")
    print("str_from_date:",str_from_date)
    print("str_to_date :",str_to_date)
    if str_from_date != "" and str_to_date != "":
        
       
        from_date=dt.strptime(str_from_date,"%Y-%m-%d %H:%M:%S")
        to_date=dt.strptime(str_to_date,"%Y-%m-%d %H:%M:%S")
        print("from_date :",from_date)
        print("to_date :",to_date)

        radwin_count = UBR_Soft_Phy_AT_Rejection_Table.objects.filter(UBR_Make_OEM="RADWIN",Date_Time__range=(from_date,to_date))
        cambium_count = UBR_Soft_Phy_AT_Rejection_Table.objects.filter(UBR_Make_OEM="CAMBIUM",Date_Time__range=(from_date,to_date))

        

        accepted_radwin_count = radwin_count.filter(AT_Status__in=["ACCEPTED","ACCEPT" ])
        accepted_cambium_count = cambium_count.filter(AT_Status__in=["ACCEPTED","ACCEPT" ])
        
        
        rejected_radwin_count = radwin_count.filter(AT_Status__in = ["REJECTED", "REJECT"])
        rejected_cambium_count = cambium_count.filter(AT_Status__in = ["REJECTED", "REJECT"])

        
    else:
        all_count = UBR_Soft_Phy_AT_Rejection_Table.objects.all()


       

        accepted_radwin_count = all_count.filter(UBR_Make_OEM="RADWIN",AT_Status__in=["ACCEPTED","ACCEPT" ])
        accepted_cambium_count =all_count.filter(UBR_Make_OEM="CAMBIUM",AT_Status__in=["ACCEPTED","ACCEPT" ])

        
        
        rejected_radwin_count = all_count.filter(UBR_Make_OEM="RADWIN",AT_Status__in = ["REJECTED", "REJECT"])
        rejected_cambium_count = all_count.filter(UBR_Make_OEM="CAMBIUM",AT_Status__in = ["REJECTED", "REJECT"])

        

        overall_min_date,overall_max_date=get_min_max_date_time(all_count)
   
    offered_count=all_count.count() 
    accepted_count=accepted_radwin_count.count()+ accepted_cambium_count.count() 
    rejected_count=rejected_radwin_count.count()+rejected_cambium_count.count() 

    percent_accepted_count = round((accepted_count/offered_count)*100, 2)
    percent_rejected_count = round((rejected_count/offered_count)*100, 2)
        
        
    data={"offered_count":offered_count,"accepted_count":accepted_count,"rejected_count":rejected_count,"percent_accepted_count":percent_accepted_count,"percent_rejected_count":percent_rejected_count,"min_time_date": overall_min_date,"max_time_date":overall_max_date,}


    return Response({
        "Status": True,
        "message": "fetched......",
        "data": data,
    })


def process_oem_data_2(from_date, to_date,circle,status,oem_model,oem_name):
    obj=oem_model.objects.filter(UBR_Make_OEM=oem_name,Date_Time__range=(from_date,to_date))
    circle_count = obj.filter(Circle=circle, AT_Status__in=status).count()
    return circle_count



@api_view(["POST", "GET"])
def oem_wise_master_dashbord(request):
    print("___________OEM WISE MASTER DASHBOARD API ___________")
    accepted_and_rejected = request.POST.get("Status")
    str_from_date = request.POST.get("from_date")
    str_to_date = request.POST.get("to_date")
    print("str_to_date....",str_to_date)    
    print("str_from_date....",str_from_date)

    from_date=dt.strptime(str_from_date,"%Y-%m-%d %H:%M:%S")
    to_date=dt.strptime(str_to_date,"%Y-%m-%d %H:%M:%S")
    print("to_date....",to_date)    
    print("from_date....",from_date)
    # to_date=dt(2024,1,30)
    # from_date=dt(2024,1,27)
    
    data = {}
    
    total_radwin=0
    total_cambium = 0

    unique_circles = get_unique_circles()

    

    for circle in unique_circles:
            circle_data={}
            if accepted_and_rejected.lower() == "false":
                # data["Status"] = "Rejected"
                # Process Rejected Data
                radwin_data = process_oem_data_2(
                    oem_model=UBR_Soft_Phy_AT_Rejection_Table,
                    oem_name="RADWIN",
                    status=["REJECTED", "REJECT"],
                    circle= circle,
                    from_date=from_date,
                    to_date=to_date
                )   
               
                circle_data["RADWIN"] = radwin_data
                cambium_data = process_oem_data_2(
                    oem_model=UBR_Soft_Phy_AT_Rejection_Table,
                    oem_name="CAMBIUM",
                    status=["REJECTED", "REJECT"],
                    circle= circle,
                    from_date=from_date,
                    to_date=to_date
                )   
               
                circle_data["CAMBIUM"] = cambium_data

                

            elif(accepted_and_rejected.lower() == "true"):
                # data["Status"] = "Accepted"
                # Process Accepted Data
                radwin_data = process_oem_data_2(
                    from_date=from_date,
                    to_date=to_date,
                    oem_model=UBR_Soft_Phy_AT_Rejection_Table,
                    oem_name="RADWIN",
                    status=["ACCEPTED", "ACCEPT"],
                    circle= circle
                )
                circle_data["RADWIN"] = radwin_data 

                cambium_data = process_oem_data_2(
                    from_date=from_date,
                    to_date=to_date,
                    oem_model=UBR_Soft_Phy_AT_Rejection_Table,
                    oem_name="CAMBIUM",
                    status=["ACCEPTED", "ACCEPT"],
                    circle= circle
                )
                circle_data["CAMBIUM"] = cambium_data 

                
            else:
                radwin_data = process_oem_data_2(
                    from_date=from_date,
                    to_date=to_date,
                    oem_model=UBR_Soft_Phy_AT_Rejection_Table,
                    oem_name="RADWIN",
                    status=["ACCEPTED", "ACCEPT", "REJECTED", "REJECT"],
                    circle= circle
                )
                circle_data["RADWIN"] = radwin_data
                cambium_data = process_oem_data_2(
                    from_date=from_date,
                    to_date=to_date,
                    oem_model=UBR_Soft_Phy_AT_Rejection_Table,
                    oem_name="CAMBIUM",
                    status=["ACCEPTED", "ACCEPT", "REJECTED", "REJECT"],
                    circle= circle
                )
                circle_data["CAMBIUM"] = cambium_data 

                

            

            print("soft__________", circle_data)
            data[circle] = circle_data  
            total_radwin=total_radwin+radwin_data
            total_cambium=total_cambium+cambium_data
            
    soft_obj=UBR_Soft_Phy_AT_Rejection_Table.objects.filter(Date_Time__range=(from_date,to_date))

             
    min_time_date = get_min_max_date_time(soft_obj)[0]
    max_time_date = get_min_max_date_time(soft_obj)[1]
    data["total"] ={"RADWIN": total_radwin, "CAMBIUM":total_cambium}
    
    # get_latest_date()

    return Response({
        "message": "Script executed successfully.",
        "status": True,
        "data": data,
        "min_time_date": min_time_date,
        "max_time_date": max_time_date,
    })



@api_view(["POST","GET"])
def oem_wise_site_details_master_dashbord(request):
    oem = request.POST.get("oem")
    circle = request.POST.get("circle")
    status = request.POST.get("Status")

    str_from_date = request.POST.get("from_date") 
    str_to_date = request.POST.get("to_date") 


    from_date=dt.strptime(str_from_date,"%Y-%m-%d %H:%M:%S")
    to_date=dt.strptime(str_to_date,"%Y-%m-%d %H:%M:%S")

    print("front end sts....................", status)
    sts_dict={"true":["ACCEPTED","ACCEPT"], "false":["REJECT","REJECTED"], "offered":["ACCEPTED","ACCEPT","REJECT","REJECTED"]}
    if(oem == "RADWIN"):
        obj = UBR_Soft_Phy_AT_Rejection_Table.objects.filter(UBR_Make_OEM=oem,Date_Time__range=(from_date, to_date),Circle=circle, AT_Status__in= sts_dict[status])
        
        serializer_data = ser_UBR_Soft_Phy_AT_Rejection_Table(obj, many=True)
        return Response({
            "Status": True,
            "message": "data sucessfully fetched....",
            "data": serializer_data.data,
        })


    if(oem == "CAMBIUM"):
        obj = UBR_Soft_Phy_AT_Rejection_Table.objects.filter(UBR_Make_OEM=oem,Date_Time__range=(from_date, to_date),Circle=circle, AT_Status__in= sts_dict[status])
        
        serializer_data = ser_UBR_Soft_Phy_AT_Rejection_Table(obj, many=True)
        return Response({
            "Status": True,
            "message": "data sucessfully fetched....",
            "data": serializer_data.data,
        })
        


def unique_offered_date():
    obj_soft = UBR_Soft_Phy_AT_Rejection_Table.objects.values('Offered_Date').distinct()


    unique_offered_dates= list(obj_soft)

   
    return unique_offered_dates


@api_view(["GET","POST"])
def date_wise_offering_status(request):

    str_from_date = request.POST.get("from_date")
    str_to_date = request.POST.get("to_date")

    print("str_to_date....",str_to_date)    
    print("str_from_date....",str_from_date)
    if str_from_date != ""  and str_to_date != "":
        from_date=dt.strptime(str_from_date,"%Y-%m-%d %H:%M:%S")
        to_date=dt.strptime(str_to_date,"%Y-%m-%d %H:%M:%S")
    else:
        soft_obj=UBR_Soft_Phy_AT_Rejection_Table.objects.all()

        from_date,to_date= get_min_max_date_time(soft_obj)
        print("inside_circle_summanry ",from_date,to_date)

    print("From date", from_date,"-",to_date)
  
    unique_offered_dates = unique_offered_date()
    
    unique_offered_date_list = [date["Offered_Date"] for date in unique_offered_dates]
    if None in unique_offered_date_list:
        unique_offered_date_list.remove(None)
    print("Unique offeered dates :",unique_offered_date_list)
    unique_offered_date_list.sort()
    if str_from_date != "" and str_to_date != "":
        # from_date=dt.strptime(str_from_date,"%Y-%m-%d").date()
        # to_date=dt.strptime(str_to_date,"%Y-%m-%d").date()
        from_date=from_date.date()
        to_date=to_date.date()
        print(from_date)
        print(to_date)
        unique_offered_date_list = list(filter(lambda x: from_date <= x <= to_date, unique_offered_date_list))
    print("hiiiiiiiiiiiiiiiiiii",unique_offered_dates)
    data={}
    for date in unique_offered_date_list:
        print(date)
        all_obj = UBR_Soft_Phy_AT_Rejection_Table.objects.filter(Date_Time__range = (from_date, to_date)).filter(Offered_Date=date)
        


        accepted_radwin_count = all_obj.filter(UBR_Make_OEM="RADWIN",AT_Status__in=["ACCEPTED","ACCEPT" ])
        accepted_cambium_count = all_obj.filter(UBR_Make_OEM="CAMBIUM",AT_Status__in=["ACCEPTED","ACCEPT" ])


        
        rejected_radwin_count = all_obj.filter(UBR_Make_OEM="RADWIN",AT_Status__in = ["REJECTED", "REJECT"])
        rejected_cambium_count = all_obj.filter(UBR_Make_OEM="CAMBIUM",AT_Status__in = ["REJECTED", "REJECT"])



        offered_count=all_obj.count()
        accepted_count=accepted_radwin_count.count() + accepted_cambium_count.count()
        rejected_count=rejected_radwin_count.count() +rejected_cambium_count.count()
        data[str(date)]={"Offered_count":offered_count,"accepted_count":accepted_count,"rejected_count":rejected_count,}
    

    print("data:   ",data)
    return Response({
        "Status": True,
        "data": data,
        "min_time_date": from_date,
        "max_time_date": to_date

    })

@api_view(["POST", "GET"])
def offered_date_wise_site_view(request):
    status = request.POST.get("Status")
    str_from_date = request.POST.get("offered_date")
    offered_date = dt.strptime(str_from_date, "%Y-%m-%d")

    sts_dict = {"true": ["ACCEPTED", "ACCEPT"], "false": ["REJECT", "REJECTED"], "offered": ["ACCEPTED", "ACCEPT", "REJECT", "REJECTED"]}

    soft_data = UBR_Soft_Phy_AT_Rejection_Table.objects.filter(Offered_Date=offered_date, AT_Status__in=sts_dict[status]).values()


    print("Count____________________",soft_data.count())

    # Combine data into a list
    combined_data = {
        'soft_data': list(soft_data),
    }

    return Response({
        "Status": True,
        "message": "Data successfully fetched....",
        "data": combined_data,
        # "Staus1": sts_dict[status],
        
    })



def process_oem_data_offered_wise(offered_date,circle,status,oem_model,oem_name):
    if(oem_name == "RADWIN"):
        obj = oem_model.objects.filter(Offered_Date=offered_date)
        

        circle_count = obj.filter(Circle=circle, AT_Status__in=status).count()
        return circle_count
    

    if(oem_name == "CAMBIUM"):
        obj = oem_model.objects.filter(Offered_Date=offered_date)
        

        circle_count = obj.filter(Circle=circle, AT_Status__in=status).count()
        return circle_count


         





@api_view(["POST", "GET"])
def offered_date_wise_oemWise_site_count(request):
    print("___________OEM WISE MASTER DASHBOARD API ___________")
    accepted_and_rejected = request.POST.get("Status")
    str_offered_date = request.POST.get("offered_date")
    
    print("str_from_date....",str_offered_date)

    offered_date=dt.strptime(str_offered_date,"%Y-%m-%d")

    # to_date=dt(2024,1,30)
    # from_date=dt(2024,1,27)
    
    data = {}

    total_radwin=0
    total_cambium = 0

    unique_circles = get_unique_circles()

    

    for circle in unique_circles:
            circle_data={}
            if accepted_and_rejected.lower() == "false":
                # data["Status"] = "Rejected"
                # Process Rejected Data
                radwin_data = process_oem_data_offered_wise(
                    oem_model=UBR_Soft_Phy_AT_Rejection_Table,
                    oem_name="RADWIN",
                    status=["REJECTED", "REJECT"],
                    circle= circle,
                    offered_date=offered_date,
                )   
               
                circle_data["RADWIN"] = radwin_data

                cambium_data = process_oem_data_offered_wise(
                    oem_model=UBR_Soft_Phy_AT_Rejection_Table,
                    oem_name="CAMBIUM",
                    status=["REJECTED", "REJECT"],
                    circle= circle,
                    offered_date=offered_date,
                )   
               
                circle_data["CAMBIUM"] = cambium_data

            elif(accepted_and_rejected.lower() == "true"):
                # data["Status"] = "Accepted"
                # Process Accepted Data
                radwin_data = process_oem_data_offered_wise(
                    oem_model=UBR_Soft_Phy_AT_Rejection_Table,
                    oem_name="RADWIN",
                    status=["REJECTED", "REJECT"],
                    circle= circle,
                    offered_date=offered_date,
                )   
               
                circle_data["RADWIN"] = radwin_data

                cambium_data = process_oem_data_offered_wise(
                    oem_model=UBR_Soft_Phy_AT_Rejection_Table,
                    oem_name="CAMBIUM",
                    status=["REJECTED", "REJECT"],
                    circle= circle,
                    offered_date=offered_date,
                )   
               
                circle_data["CAMBIUM"] = cambium_data

            else:
                radwin_data = process_oem_data_offered_wise(
                    oem_model=UBR_Soft_Phy_AT_Rejection_Table,
                    oem_name="RADWIN",
                    status=["REJECTED", "REJECT"],
                    circle= circle,
                    offered_date=offered_date,
                )   
               
                circle_data["RADWIN"] = radwin_data

                cambium_data = process_oem_data_offered_wise(
                    oem_model=UBR_Soft_Phy_AT_Rejection_Table,
                    oem_name="CAMBIUM",
                    status=["REJECTED", "REJECT"],
                    circle= circle,
                    offered_date=offered_date,
                )   
               
                circle_data["CABIUM"] = cambium_data

            

            print("RADWIN: ", circle_data)
            data[circle] = circle_data  

            total_radwin=total_radwin + radwin_data
            total_cambium=total_cambium + cambium_data

            
    all_obj=UBR_Soft_Phy_AT_Rejection_Table.objects.filter(Offered_Date=offered_date)

             
    # min_time_date = get_min_max_date_time(nok_obj, sam_obj, hua_obj)[0]
    # max_time_date = get_min_max_date_time(nok_obj, sam_obj, hua_obj)[1]
    data["total"] ={"RADWIN": total_radwin, "CAMBIUM": total_cambium}
    
    # get_latest_date()

    return Response({
        "message": "Script executed successfully.",
        "status": True,
        "data": data,
        # "min_time_date": min_time_date,
        # "max_time_date": max_time_date,
    })


@api_view(["GET","POST"])
def OverAllCircleWiseSummary(request):

    str_from_date = request.POST.get("from_date")
    str_to_date = request.POST.get("to_date")
    if str_from_date != ""  and str_to_date !='':
        from_date=dt.strptime(str_from_date,"%Y-%m-%d %H:%M:%S")
        to_date=dt.strptime(str_to_date,"%Y-%m-%d %H:%M:%S")
    else:
        soft_obj=UBR_Soft_Phy_AT_Rejection_Table.objects.all()
        from_date,to_date= get_min_max_date_time(soft_obj)
        print("inside_circle_summanry ",from_date,to_date)

    unique_circle = get_unique_circles()
    data={}
    for circle in unique_circle:
        all_obj = UBR_Soft_Phy_AT_Rejection_Table.objects.filter(Circle = circle, Date_Time__range=(from_date, to_date))



        accepted_radwin_count = all_obj.filter(UBR_Make_OEM="RADWIN",AT_Status__in=["ACCEPTED","ACCEPT" ])
        accepted_cambium_count = all_obj.filter(UBR_Make_OEM="CAMBIUM",AT_Status__in=["ACCEPTED","ACCEPT" ])

        
        rejected_radwin_count = all_obj.filter(UBR_Make_OEM="RADWIN",AT_Status__in = ["REJECTED", "REJECT"])
        rejected_cambium_count = all_obj.filter(UBR_Make_OEM="CAMBIUM",AT_Status__in = ["REJECTED", "REJECT"])


        offered_count=all_obj.count()
        accepted_count=accepted_radwin_count.count() + accepted_cambium_count.count()
        rejected_count=rejected_radwin_count.count() + rejected_cambium_count.count()
        percent_accepted_count = round((accepted_count/offered_count)*100, 2)
        percent_rejected_count = round((rejected_count/offered_count)*100, 2)
        data[str(circle)]={"Offered_count":offered_count,"accepted_count":accepted_count,"rejected_count":rejected_count,"accepted_percentage":percent_accepted_count,"rejected_percentage":percent_rejected_count}
        
    return Response({
    "message": "Successfully.",
    "status": True,
    "data": data,
    })



def process_oem_data_3(from_date, to_date,circle,status,oem_model,oem_name, offered_date):

    if(oem_name == "RADWIN"):
        obj = oem_model.objects.filter(Date_Time__range = (from_date, to_date)).filter(Offered_Date=offered_date)
        
        circle_count = obj.filter(Circle=circle, AT_Status__in=status).count()
        return circle_count

    if(oem_name == "CAMBIUM"):
        obj = oem_model.objects.filter(Date_Time__range = (from_date, to_date)).filter(Offered_Date=offered_date)
        
        circle_count = obj.filter(Circle=circle, AT_Status__in=status).count()
        return circle_count


@api_view(["GET","POST"])
def offer_date_wise_oem_wise_circle_wise_summary(request):

    str_from_date = request.POST.get("from_date")
    str_to_date = request.POST.get("to_date")
    str_offered_date = request.POST.get("offered_date")
    offered_date=dt.strptime(str_offered_date,"%Y-%m-%d").date()
    if str_from_date != ""  and str_to_date != "":
        from_date=dt.strptime(str_from_date,"%Y-%m-%d %H:%M:%S")
        to_date=dt.strptime(str_to_date,"%Y-%m-%d %H:%M:%S")
    else:
        all_obj=UBR_Soft_Phy_AT_Rejection_Table.objects.all()

        from_date,to_date= get_min_max_date_time(all_obj)
        print("inside_circle_summanry ",from_date,to_date)

    print("From date", from_date,"-",to_date)
    data={}
    unique_circle = get_unique_circles()
    for circle in unique_circle:
        circle_data={}
        randwin_rejected =  process_oem_data_3(
             from_date= from_date,
             to_date= to_date,
             offered_date = offered_date,
             circle= circle,
             status=["REJECTED", "REJECT"],
             oem_model=UBR_Soft_Phy_AT_Rejection_Table,
             oem_name="RADWIN",
            )   
        randwin_accepted =  process_oem_data_3(
            oem_model=UBR_Soft_Phy_AT_Rejection_Table,
            oem_name="RADWIN",
            status=["ACCEPTED", "ACCEPT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            offered_date = offered_date
            )
        randwin_offered =  process_oem_data_3(
            oem_model=UBR_Soft_Phy_AT_Rejection_Table,
            oem_name="RADWIN",
            status=["ACCEPTED","ACCEPT","REJECTED", "REJECT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            offered_date = offered_date
            
            
            )
        if randwin_offered != 0:
            percent_accepted_count = round((randwin_accepted/randwin_offered)*100, 2)
            percent_rejected_count = round((randwin_rejected/randwin_offered)*100, 2)
        else:
            percent_accepted_count = 0
            percent_rejected_count = 0
            
        circle_data["RADWIN"] = {"offered":randwin_offered,"accepted":randwin_accepted,"rejected":randwin_rejected,"accepted_percentage":percent_accepted_count,"rejected_percentage":percent_rejected_count}


        cambium_rejected =  process_oem_data_3(
             from_date= from_date,
             to_date= to_date,
             offered_date = offered_date,
             circle= circle,
             status=["REJECTED", "REJECT"],
             oem_model=UBR_Soft_Phy_AT_Rejection_Table,
             oem_name="CAMBIUM",
            )   
        cambium_accepted =  process_oem_data_3(
            oem_model=UBR_Soft_Phy_AT_Rejection_Table,
            oem_name="CAMBIUM",
            status=["ACCEPTED", "ACCEPT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            offered_date = offered_date
            )
        cambium_offered =  process_oem_data_3(
            oem_model=UBR_Soft_Phy_AT_Rejection_Table,
            oem_name="CAMBIUM",
            status=["ACCEPTED","ACCEPT","REJECTED", "REJECT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            offered_date = offered_date
            
            
            )
        if cambium_offered != 0:
            percent_accepted_count = round((cambium_accepted/cambium_offered)*100, 2)
            percent_rejected_count = round((cambium_rejected/cambium_offered)*100, 2)
        else:
            percent_accepted_count = 0
            percent_rejected_count = 0
            
        circle_data["CAMBIUM"] = {"offered":cambium_offered,"accepted":cambium_accepted,"rejected":cambium_rejected,"accepted_percentage":percent_accepted_count,"rejected_percentage":percent_rejected_count}

        data[circle] = circle_data

    return Response({
        "Status": True,
        "message": "data feteched successfully",
        "data": data
    })


@api_view(["POST", "GET"])
def oem_wise_hyper_link_over_overall_circlewie_summary(request):
    print("___________OEM WISE MASTER DASHBOARD API ___________")
    accepted_and_rejected = request.POST.get("Status")
    circle = request.POST.get("Circle")
    str_from_date = request.POST.get("from_date")
    str_to_date = request.POST.get("to_date")

    if str_from_date != ""  and str_to_date != "":
        from_date=dt.strptime(str_from_date,"%Y-%m-%d %H:%M:%S")
        to_date=dt.strptime(str_to_date,"%Y-%m-%d %H:%M:%S")
    else:
        all_obj=UBR_Soft_Phy_AT_Rejection_Table.objects.all()

        from_date,to_date= get_min_max_date_time(all_obj)
        print("inside_circle_summanry ",from_date,to_date)

    print("From date", from_date,"-",to_date)
    # to_date=dt(2024,1,30)
    # from_date=dt(2024,1,27)
    
    data = {}
    
    total_radwin=0
    total_cambium = 0

    # unique_circles = get_unique_circles()

    

    # for circle in unique_circles:
    circle_data={}
    if accepted_and_rejected.lower() == "false":
        # data["Status"] = "Rejected"
        # Process Rejected Data
        radwin_data = process_oem_data_2(
            oem_model=UBR_Soft_Phy_AT_Rejection_Table,
            oem_name="RADWIN",
            status=["REJECTED", "REJECT"],
            circle= circle,
            from_date=from_date,
            to_date=to_date
        )   
        
        circle_data["RADWIN"] = radwin_data

        cambium_data = process_oem_data_2(
            oem_model=UBR_Soft_Phy_AT_Rejection_Table,
            oem_name="CAMBIUM",
            status=["REJECTED", "REJECT"],
            circle= circle,
            from_date=from_date,
            to_date=to_date
        )   
        
        circle_data["CAMBIUM"] = cambium_data

    elif(accepted_and_rejected.lower() == "true"):
        # data["Status"] = "Accepted"
        # Process Accepted Data
        radwin_data = process_oem_data_2(
            oem_model=UBR_Soft_Phy_AT_Rejection_Table,
            oem_name="RADWIN",
            status=["ACCEPTED", "ACCEPT"],
            circle= circle,
            from_date=from_date,
            to_date=to_date
        )   
        
        circle_data["RADWIN"] = radwin_data

        cambium_data = process_oem_data_2(
            oem_model=UBR_Soft_Phy_AT_Rejection_Table,
            oem_name="CAMBIUM",
            status=["ACCEPTED", "ACCEPT"],
            circle= circle,
            from_date=from_date,
            to_date=to_date
        )   
        
        circle_data["CAMBIUM"] = cambium_data

    else:
        radwin_data = process_oem_data_2(
            oem_model=UBR_Soft_Phy_AT_Rejection_Table,
            oem_name="RADWIN",
            status=["ACCEPTED", "ACCEPT","REJECTED", "REJECT"],
            circle= circle,
            from_date=from_date,
            to_date=to_date
        )   
        
        circle_data["RADWIN"] = radwin_data    

        cambium_data = process_oem_data_2(
            oem_model=UBR_Soft_Phy_AT_Rejection_Table,
            oem_name="CAMBIUM",
            status=["ACCEPTED", "ACCEPT","REJECTED", "REJECT"],
            circle= circle,
            from_date=from_date,
            to_date=to_date
        )   
        
        circle_data["CAMBIUM"] = cambium_data   

    print("circle data:", circle_data)
    data[circle] = circle_data

    total_radwin = total_radwin+radwin_data
    total_cambium = total_cambium + cambium_data
    

            
    soft_obj=UBR_Soft_Phy_AT_Rejection_Table.objects.filter(Date_Time__range=(from_date,to_date))

             
    min_time_date = get_min_max_date_time(soft_obj)[0]
    max_time_date = get_min_max_date_time(soft_obj)[1]
    data["total"] ={"RADWIN":total_radwin, "CAMBIUM": total_cambium}
    
    # get_latest_date()

    return Response({
        "message": "Script executed successfully.",
        "status": True,
        "data": data,
        "min_time_date": min_time_date,
        "max_time_date": max_time_date,
    })



@api_view(["GET","POST"])
def overall_oem_wise_circle_wise_summary(request):

    str_from_date = request.POST.get("from_date")
    str_to_date = request.POST.get("to_date")
    if str_from_date != ""  and str_to_date !='':
        from_date=dt.strptime(str_from_date,"%Y-%m-%d %H:%M:%S")
        to_date=dt.strptime(str_to_date,"%Y-%m-%d %H:%M:%S")
    else:
        all_obj=UBR_Soft_Phy_AT_Rejection_Table.objects.all()
        from_date,to_date= get_min_max_date_time(all_obj)
        print("inside_circle_summanry ",from_date,to_date)

    print("From date", from_date,"-",to_date)
    data={}
    unique_circle = get_unique_circles()
    for circle in unique_circle:
        circle_data={}
        radwin_rejected =  process_oem_data_2(
             from_date= from_date,
             to_date= to_date,
             circle= circle,
             status=["REJECTED", "REJECT"],
             oem_model=UBR_Soft_Phy_AT_Rejection_Table,
             oem_name="RADWIN",
            )   
        radwin_accepted =  process_oem_data_2(
            oem_model=UBR_Soft_Phy_AT_Rejection_Table,
            oem_name="RADWIN",
            status=["ACCEPTED", "ACCEPT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            )
        radwin_offered =  process_oem_data_2(
            oem_model=UBR_Soft_Phy_AT_Rejection_Table,
            oem_name="RADWIN",
            status=["ACCEPTED","ACCEPT","REJECTED", "REJECT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            
            
            )
        if radwin_offered != 0:
            percent_accepted_count = round((radwin_accepted/radwin_offered)*100, 2)
            percent_rejected_count = round((radwin_rejected/radwin_offered)*100, 2)
        else:
            percent_accepted_count = 0
            percent_rejected_count = 0
            
        circle_data["RADWIN"] = {"offered":radwin_offered,"accepted":radwin_accepted,"rejected":radwin_rejected,"accepted_percentage":percent_accepted_count,"rejected_percentage":percent_rejected_count}

        cambium_rejected = process_oem_data_2(
            oem_model=UBR_Soft_Phy_AT_Rejection_Table,
            oem_name="CAMBIUM",
            status=["REJECTED", "REJECT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            
        )
        canbium_accepted = process_oem_data_2(
            oem_model=UBR_Soft_Phy_AT_Rejection_Table,
            oem_name="CAMBIUM",
            status=["ACCEPTED", "ACCEPT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            
        )
        canbium_offered = process_oem_data_2(
            oem_model=UBR_Soft_Phy_AT_Rejection_Table,
            oem_name="CANBIUM",
            status=["ACCEPTED", "ACCEPT", "REJECTED", "REJECT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            
        )

        if canbium_offered != 0:
            percent_accepted_count = round((canbium_accepted/canbium_offered)*100, 2)
            percent_rejected_count = round((cambium_rejected/canbium_offered)*100, 2)
        else:
            percent_accepted_count = 0
            percent_rejected_count = 0


        
        circle_data["CAMBIUM"] = {"offered":canbium_offered,"accepted":canbium_accepted,"rejected":cambium_rejected,"accepted_percentage":percent_accepted_count,"rejected_percentage":percent_rejected_count}
        
        data[circle]=circle_data

    return Response({
        "Status": True,
        "message": "data feteched successfully",
        "data": data
    })





@api_view(["POST", "GET"])
def range_wise_rejected_site_count(request):
    print("____ INSIDE_RANGE_WISE_REJECTED_COUNT ____")
    str_from_date=request.POST.get("from_date")
    str_to_date=request.POST.get("to_date")
    print("str_to_date....",str_to_date)    
    print("str_from_date....",str_from_date)
    if str_from_date != ""  and str_to_date != "":
        from_date=dt.strptime(str_from_date,"%Y-%m-%d %H:%M:%S")
        to_date=dt.strptime(str_to_date,"%Y-%m-%d %H:%M:%S")
    else:
        all_obj=UBR_Soft_Phy_AT_Rejection_Table.objects.all()

        from_date,to_date= get_min_max_date_time(all_obj)
        print("inside_circle_summanry ",from_date,to_date)
    with connection.cursor() as cursor:

        query = f"""

            WITH all_ranges AS (
                SELECT start_range || '-' || end_range AS "range", start_range
                FROM (
                    SELECT generate_series(1, 28, 3) AS start_range,generate_series(3, 30, 3) AS end_range
                ) q1

                 UNION 

                SELECT '>30' AS "range", 100 AS start_range
            )

            SELECT ar.range,
                   COALESCE(yt.rejected_site_count, 0) AS rejected_site_count
            FROM all_ranges ar
            LEFT JOIN (
                SELECT "range", SUM("repetition_count") AS "rejected_site_count"
                FROM (
                    SELECT "oem", "Site_ID", "repetition_count",
                           CASE
                               WHEN repetition_count BETWEEN 1 AND 3 THEN '1-3'
                               WHEN repetition_count BETWEEN 4 AND 6 THEN '4-6'
                               WHEN repetition_count BETWEEN 7 AND 9 THEN '7-9'
                               WHEN repetition_count BETWEEN 10 AND 12 THEN '10-12'
                               WHEN repetition_count BETWEEN 13 AND 15 THEN '13-15'
                               WHEN repetition_count BETWEEN 16 AND 18 THEN '16-18'
                               WHEN repetition_count BETWEEN 19 AND 21 THEN '19-21'
                               WHEN repetition_count BETWEEN 22 AND 24 THEN '22-24'
                               WHEN repetition_count BETWEEN 25 AND 27 THEN '24-27'
                               WHEN repetition_count BETWEEN 28 AND 30 THEN '28-30'
                               ELSE '>30'  -- Handle greater than 30
                           END AS range
                    FROM (
                        SELECT "UBR_Make_OEM" AS oem, "Site_ID" AS "Site_ID", COUNT(*) AS repetition_count
                        FROM public."UBR_Soft_Phy_AT_Rejection_App_ubr_soft_phy_at_rejection_table"
                        WHERE "AT_Status" IN ('REJECTED', 'REJECT')
                          AND "Date_Time" BETWEEN '{from_date}' AND '{to_date}'
                        GROUP BY "UBR_Make_OEM", "Site_ID"
                        ORDER BY repetition_count DESC
                    ) AS counts_per_site
                ) yt
                GROUP BY "range"
                ORDER BY "range"
            ) yt ON yt.range = ar."range"
            ORDER BY ar.start_range;
        """

        cursor.execute(query)
        results = cursor.fetchall()
        print(results)
    results_as_strings = []

    for row in results:
        # Convert each element in the row to a string
        row_as_string = [str(element) for element in row]
        # Append the row as a string to the list
        results_as_strings.append(row_as_string)
    

    rows_as_dict = [dict(zip([column[0] for column in cursor.description], row)) for row in results_as_strings]


    jsonResult =  json.dumps(rows_as_dict)

    print(jsonResult)
    data={"table_data":jsonResult, "min_time_date": from_date,"max_time_date": to_date,}
    return Response(data)


@api_view(["POST", "GET"])
def range_wise_rejected_remark(request):
    print("____ INSIDE_RANGE_WISE_REJECTED_COUNT _REMARK ____")
    str_from_date=request.POST.get("from_date")
    str_to_date=request.POST.get("to_date")
    print("str_to_date....",str_to_date)    
    print("str_from_date....",str_from_date)
    if str_from_date != ""  and str_to_date != "":
        from_date=dt.strptime(str_from_date,"%Y-%m-%d %H:%M:%S")
        to_date=dt.strptime(str_to_date,"%Y-%m-%d %H:%M:%S")
    else:
        all_obj=UBR_Soft_Phy_AT_Rejection_Table.objects.all()
        from_date,to_date= get_min_max_date_time(all_obj)
        print("inside_circle_summanry ",from_date,to_date)

    range=request.POST.get('range')
    with connection.cursor() as cursor:

        query = f"""
                SELECT *
                FROM
                    (SELECT "Site_ID" || ' ' || "Circle" AS "site_circle", oem, "Circle", "Site_ID", repetition_count, range
                    FROM
                        (SELECT "oem", "Circle", "Site_ID", "repetition_count",
                                CASE
                                    WHEN repetition_count BETWEEN 1 AND 3 THEN '1-3'
                                    WHEN repetition_count BETWEEN 4 AND 6 THEN '4-6'
                                    WHEN repetition_count BETWEEN 7 AND 9 THEN '7-9'
                                    WHEN repetition_count BETWEEN 10 AND 12 THEN '10-12'
                                    WHEN repetition_count BETWEEN 13 AND 15 THEN '13-15'
                                    WHEN repetition_count BETWEEN 16 AND 18 THEN '16-18'
                                    WHEN repetition_count BETWEEN 19 AND 21 THEN '19-21'
                                    WHEN repetition_count BETWEEN 22 AND 24 THEN '22-24'
                                    WHEN repetition_count BETWEEN 25 AND 27 THEN '24-27'
                                    WHEN repetition_count BETWEEN 28 AND 30 THEN '28-30'
                                    ELSE '>30'
                                END AS range
                        FROM
                            (SELECT "UBR_Make_OEM" AS oem, "Circle", "Site_ID" AS "Site_ID", COUNT(*) AS repetition_count
                            FROM public."UBR_Soft_Phy_AT_Rejection_App_ubr_soft_phy_at_rejection_table"
                            WHERE "AT_Status" IN ('REJECTED', 'REJECT')
                              AND "Date_Time" BETWEEN '{from_date}' AND '{to_date}'
                            GROUP BY "UBR_Make_OEM", "Circle", "Site_ID"
                            ORDER BY repetition_count DESC) AS counts_per_site) AS t1
                    ORDER BY range) AS ultimate_table
                LEFT JOIN
                    (SELECT *
                    FROM crosstab($$
                                SELECT "Site_ID" || ' ' || "Circle" AS "site_circle", "Reasons", "Reasons"
                                FROM public."UBR_Soft_Phy_AT_Rejection_App_ubr_soft_phy_at_rejection_table"
                                WHERE "AT_Status" IN ('REJECT', 'REJECTED')
                                  AND "Date_Time" BETWEEN '{from_date}' AND '{to_date}'
                                ORDER BY 1, 2$$)
                                AS final_result(site_circle TEXT, r1 VARCHAR, r2 VARCHAR, r3 VARCHAR, r4 VARCHAR, r5 VARCHAR,
                                                r6 VARCHAR, r7 VARCHAR, r8 VARCHAR, r9 VARCHAR, r10 VARCHAR, r11 VARCHAR,
                                                r12 VARCHAR, r13 VARCHAR, r14 VARCHAR, r15 VARCHAR)) AS t2 on ultimate_table.site_circle =t2.site_circle

                LEFT JOIN 

                (select * from (select  "Site_ID" ||' '|| "Circle" as "site_circle" ,"Site_ID" as "site_id",CURRENT_DATE - "Offered_Date" as "ageing" from (select *, ROW_NUMBER() over (partition by "Site_ID" order by "Offered_Date") as "row_num"  from public."UBR_Soft_Phy_AT_Rejection_App_ubr_soft_phy_at_rejection_table" where "AT_Status" in ('REJECTED','REJECT') AND "Date_Time" between '{from_date}' AND '{to_date}' ) as t1
                where row_num =1 ) as tt  ) as ageing_table
                on ultimate_table.site_circle = ageing_table.site_circle
                where ultimate_table.range = '{range}';

            """

        cursor.execute(query)
        results = cursor.fetchall()
        print(results)
    results_as_strings = []

    for row in results:
        # Convert each element in the row to a string
        row_as_string = [str(element) for element in row]
        # Append the row as a string to the list
        results_as_strings.append(row_as_string)
    

    rows_as_dict = [dict(zip([column[0] for column in cursor.description], row)) for row in results_as_strings]


    jsonResult =  json.dumps(rows_as_dict)

    print(jsonResult)
   
    return Response(jsonResult)
