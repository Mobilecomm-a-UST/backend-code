import win32com.client
from pathlib import Path
import datetime
from itertools import chain
import json
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
from itertools import chain
import os
from .serializers import * 
# from Soft_AT_Rejected.utils import subject_filteration
from Soft_AT_Rejected.utils import *
from django.db import connection

 

def circle_list(objs):
    cir=[]
    
    for obj in objs:
        cir.append(obj.Circle)

    cir_set=set(cir)
    cir=list(cir_set)
    return cir





    

@api_view(['GET'])
def save_database(request):
    Soft_At_Rejection_Database_save(True,[])   
     
    # Soft_At_Rejection_Database_ERI_save(True,[])
    return Response({"status":True})                        
                                        
        
    
@api_view(["GET","POST"])
def SoftAt_Circlewise_Rejected_Dashboard(request):  
    objs=Soft_AT_NOKIA_Rejected_Table.objects.all()
    str_Date=request.POST.get("Date")  if request.POST.get("Date") else None
    print("str_date,_______",str_Date)
   
    month=request.POST.get("month") if request.POST.get("month") else None
    week=request.POST.get("week") if request.POST.get("week") else None
    year=request.POST.get("year") if request.POST.get("year") else None
    str_from_date=request.POST.get("from_date") if request.POST.get("from_date") else None
    str_to_date=request.POST.get("to_date") if request.POST.get("to_date") else None

    print("month:-----",month)
    print("date:-----",str_Date)
    print("week:---",week)
    print("year:---",year)
    print("str_from_date:---",str_from_date)
    print("str_to_date---",str_to_date)
    # year=int(year)
    objs=Soft_AT_NOKIA_Rejected_Table.objects.all()
   
    circles= circle_list(objs)
    print("Circle_list: ",circles)
    data=[]
    total_all_oems = {}
    oems = objs.values_list('OEM', flat=True).distinct()

    if str_Date :
         Date = datetime.datetime.strptime(str_Date, "%Y-%m-%d").date()
         objs=objs.filter(Offered_Date=Date)
         print(objs,"_____________________date_____________")
    
    if str_from_date is not None and str_to_date is not None:
            
        print("___________Inside from and to ___________")
        from_date=datetime.datetime.strptime(str_from_date,"%Y-%m-%d").date()
        to_date=datetime.datetime.strptime(str_to_date,"%Y-%m-%d").date()
        print("from_date",from_date)
        print("to_date",to_date)
        
        
        objs=objs.filter(Offered_Date__range=(from_date, to_date))
        
    elif month is not None:
            
        print("___________Inside Month___________")
        print("OEM:", oem)
        print("Month:", month)
        print("Year:", year)
        
        
        objs = objs.filter(Offered_Date__month=month, Offered_Date__year=year)


    elif week is not None:
            
        print("___________Inside week___________")
        print(month)
        
        objs = objs.filter(Offered_Date__week=week, Offered_Date__year=year)
   
    for circle in circles:
        # obj = Soft_AT_Rejected_Table.objects.filter(Circle=circle)
        obj = objs.filter(Circle=circle)
        print(obj, "obj")

        print("Processing circle:", circle)

        # Process data for the current circle
        oem_data = {}
        
        total_grand = 0
        # total = 0
        grand = 0
        for oem in oems:
            oem_count = obj.filter(OEM__iexact=oem, AT_STATUS__in=["REJECTED", "REJECT"]).count()
            oem_data[oem] = oem_count
            print("_____________________________",oem_data,"_____________________")

            total_all_oems[oem] = total_all_oems.get(oem, 0) + oem_count

            total_grand += total_all_oems[oem]
        
        total_all_oems["total_grand"] = total_grand

        total = sum(oem_data.values())
        # oem_data["total"]=total

        data.append({
            "circle": circle,
            "total": total,
            "oem_data": oem_data,
            
        })
        #################### Range wise from to to date ##################################

        
   

    return Response({"status": True, "message": "Successfully processed all circles.","data":data,"total_all_oems": total_all_oems})
        # return Response({"status": True,"message": "Successfully processed all circles.","data": {"total_all_oems": {"total_grand": total_grand,"oem_data": total_all_oems},'data':data}})


@api_view(['GET'])
def graph_data(request):
    try:
        # Query the database to get accepted and rejected counts from all three models
        accepted_count_nokia = Soft_AT_NOKIA_Rejected_Table.objects.filter(AT_STATUS='ACCEPTED').count()
        rejected_count_nokia = Soft_AT_NOKIA_Rejected_Table.objects.filter(AT_STATUS__in=["REJECTED", "REJECT"]).count()

        accepted_count_samsung = Soft_AT_SAMSUNG_Rejected_Table.objects.filter(AT_STATUS='ACCEPTED').count()
        rejected_count_samsung = Soft_AT_SAMSUNG_Rejected_Table.objects.filter(AT_STATUS__in=["REJECTED", "REJECT"]).count()

        accepted_count_huawei = Soft_AT_HUAWEI_Rejected_Table.objects.filter(AT_STATUS='ACCEPTED').count()
        rejected_count_huawei = Soft_AT_HUAWEI_Rejected_Table.objects.filter(AT_STATUS__in=["REJECTED", "REJECT"]).count()

        # Calculate total counts
        total_accepted_count = accepted_count_nokia + accepted_count_samsung + accepted_count_huawei
        total_rejected_count = rejected_count_nokia + rejected_count_samsung + rejected_count_huawei

        total = total_accepted_count + total_rejected_count

        accepted_count_percentage = round((total_accepted_count * 100) / total, 2)
        rejected_count_percentage = round((total_rejected_count * 100) / total, 2)

        data = {
            "Accepted_count": total_accepted_count,
            "Rejected_count": total_rejected_count,
            "total": total,
            "accepted_count_percentage": accepted_count_percentage,
            "rejected_count_percentage": rejected_count_percentage
        }

        return Response({'status': True, 'data': data})

    except Exception as e:
        return Response({'status': False, 'message': str(e)})

def get_unique_circles():

    obj_nok = list(Soft_AT_NOKIA_Rejected_Table.objects.all().values_list('Circle', flat=True).distinct())
    obj_hua = list(Soft_AT_HUAWEI_Rejected_Table.objects.all().values_list('Circle', flat=True).distinct())
    obj_sam = list(Soft_AT_SAMSUNG_Rejected_Table.objects.all().values_list('Circle', flat=True).distinct())
    return list(set(obj_nok + obj_hua + obj_sam))




def process_oem_data(oem_model, oem_name, status,circle):
   obj=get_latest_record_per_site(oem_model)
   print("msmsmsmsmsmsmsmms",type(obj))
   circle_count = obj.filter(Circle=circle, AT_STATUS__in=status).count()
   return circle_count

@api_view(["GET","POST"])
def Soft_Rejection_Report(request):
    # Soft_At_Rejection_Database_save(request)
    accepted_and_rejected = request.POST.get("Status")
    print(accepted_and_rejected)
    data = {}
    total_huawei=0
    total_nokia=0
    total_Samsung=0
    unique_circles = get_unique_circles()

    

    for circle in unique_circles:
            circle_data={}
            if accepted_and_rejected.lower() == "false":
                # data["Status"] = "Rejected"
                # Process Rejected Data
                nokia_data = process_oem_data(
                    oem_model=Soft_AT_NOKIA_Rejected_Table,
                    oem_name="Nokia",
                    status=["REJECTED", "REJECT"],
                    circle= circle
                )   
               
                circle_data["Nokia"] = nokia_data

                huawei_data = process_oem_data(
                    oem_model=Soft_AT_HUAWEI_Rejected_Table,
                    oem_name="Huawei",
                    status=["REJECTED", "REJECT"],
                    circle= circle
                )
                circle_data["Huawei"] = huawei_data 
                samsung_data = process_oem_data(
                    oem_model=Soft_AT_SAMSUNG_Rejected_Table,
                    oem_name="Samsung",
                    status=["REJECTED", "REJECT"],
                    circle= circle
                )
                circle_data["Samsung"] = samsung_data 

            else:
                # data["Status"] = "Accepted"
                # Process Accepted Data
                nokia_data = process_oem_data(
                    oem_model=Soft_AT_NOKIA_Rejected_Table,
                    oem_name="Nokia",
                    status=["ACCEPTED", "ACCEPT"],
                    circle= circle
                )
                circle_data["Nokia"] = nokia_data 

                huawei_data = process_oem_data(
                    oem_model=Soft_AT_HUAWEI_Rejected_Table,
                    oem_name="Huawei",
                    status=["ACCEPTED", "ACCEPT"],
                    circle= circle
                )
                circle_data["Huawei"] = huawei_data   

                samsung_data = process_oem_data(
                    oem_model=Soft_AT_SAMSUNG_Rejected_Table,
                    oem_name="Samsung",
                    status=["ACCEPTED", "ACCEPT"],
                    circle= circle
                )
                circle_data["Samsung"] = samsung_data
            
            data[circle] = circle_data  
            total_huawei=total_huawei + huawei_data
            total_nokia=total_nokia+nokia_data 
            total_Samsung=total_Samsung+samsung_data
         
            nok_obj= Soft_AT_NOKIA_Rejected_Table.objects.all()
            sam_obj= Soft_AT_SAMSUNG_Rejected_Table.objects.all()
            hua_obj= Soft_AT_HUAWEI_Rejected_Table.objects.all()
            
            
            min_time_date,max_time_date = get_min_max_date_time(nok_obj, sam_obj, hua_obj)
            
    data["total"] ={"Huawei":total_huawei,"Samsung":total_Samsung,"Nokia":total_nokia}
    
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
    if(oem == "Nokia"):
        # obj = Soft_AT_NOKIA_Rejected_Table.objects.filter(Circle=circle, AT_STATUS__in= sts_dict[status])
        obj=get_latest_record_per_site(Soft_AT_NOKIA_Rejected_Table)
        obj = obj.filter(Circle=circle, AT_STATUS__in=sts_dict[status])
        serializer_data = ser_Soft_At_NOK_upload_table(obj, many=True)

        return Response({
            "Status": True,
            "message": "data sucessfully fetched....",
            "data": serializer_data.data,
        })
        
    elif(oem == "Huawei"):
        
        # obj = Soft_AT_HUAWEI_Rejected_Table.objects.filter(Circle=circle, AT_STATUS__in= sts_dict[status])
        obj=get_latest_record_per_site(Soft_AT_HUAWEI_Rejected_Table)

        print(obj,"_____________HIII_____________",obj.count())
        obj = obj.filter(Circle=circle, AT_STATUS__in=sts_dict[status])

        print(obj,"please check the data___________________")
        serializer_data = ser_Soft_At_HUA_upload_table(obj, many=True)

        return Response({
            "Status": True,
            "message": "data sucessfully fetched....",
            "data": serializer_data.data,
        }) 
    elif(oem == "Samsung"):
        obj=get_latest_record_per_site(Soft_AT_SAMSUNG_Rejected_Table)
        obj = obj.filter(Circle=circle, AT_STATUS__in=sts_dict[status])   
        serializer_data = ser_Soft_At_SAM_upload_table(obj, many=True)

        return Response({
            "Status": True,
            "message": "data sucessfully fetched....",
            "data": serializer_data.data,
        })
          
    elif(oem == "Ericcsion"):
        obj=get_latest_record_per_site(Soft_AT_SAMSUNG_Rejected_Table)
        obj = obj.filter(Circle=circle, AT_STATUS__in=sts_dict[status])   
        serializer_data = ser_Soft_At_SAM_upload_table(obj, many=True)

        return Response({
            "Status": True,
            "message": "data sucessfully fetched....",
            "data": serializer_data.data,
        })
          
    elif(oem == "Samsung"):
        obj=get_latest_record_per_site(Soft_AT_SAMSUNG_Rejected_Table)
        obj = obj.filter(Circle=circle, AT_STATUS__in=sts_dict[status])   
        serializer_data = ser_Soft_At_SAM_upload_table(obj, many=True)

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
    if(oem == "Nokia"):
        obj = Soft_AT_NOKIA_Rejected_Table.objects.filter(Site_ID=site_id, AT_STATUS__in= sts_dict[status])
        # obj = Soft_AT_NOKIA_Rejected_Table.objects.filter(Site_ID=site_id, AT_STATUS =status)
        serializer_data = ser_Soft_At_NOK_upload_table(obj, many=True)
        return Response({
            "Status": True,
            "message": "data sucessfully fetched....",
            "data": serializer_data.data,
        }) 
    if(oem == "Huawei"):
        obj = Soft_AT_HUAWEI_Rejected_Table.objects.filter(Site_ID_2G=site_id, AT_STATUS__in= sts_dict[status])
        # obj = Soft_AT_HUAWEI_Rejected_Table.objects.filter(Site_ID_2G=site_id, AT_STATUS__in= status)
        serializer_data = ser_Soft_At_HUA_upload_table(obj, many=True)
        return Response({
            "Status": True,
            "message": "data sucessfully fetched....",
            "data": serializer_data.data,
        }) 
    if(oem == "Samsung"):
        obj = Soft_AT_SAMSUNG_Rejected_Table.objects.filter(Site_ID_2G=site_id, AT_STATUS__in= sts_dict[status])
        # obj = Soft_AT_SAMSUNG_Rejected_Table.objects.filter(Site_ID_2G=site_id, AT_STATUS__in= status)
        serializer_data = ser_Soft_At_SAM_upload_table(obj, many=True)
        return Response({
            "Status": True,
            "message": "data sucessfully fetched....",
            "data": serializer_data.data,
        }) 
    if(oem == "Ericcsion"):
        obj = Soft_AT_ERI_Rejected_Table.objects.filter(Site_ID=site_id, AT_STATUS__in= sts_dict[status])
        # obj = Soft_AT_SAMSUNG_Rejected_Table.objects.filter(Site_ID_2G=site_id, AT_STATUS__in= status)
        serializer_data = ser_Soft_At_ERI_upload_table(obj, many=True)
        return Response({
            "Status": True,
            "message": "data sucessfully fetched....",
            "data": serializer_data.data,
        }) 
    if(oem == "zte"):
        obj = Soft_AT_ZTE_Rejected_Table.objects.filter(Site_ID=site_id, AT_STATUS__in= sts_dict[status])
        # obj = Soft_AT_SAMSUNG_Rejected_Table.objects.filter(Site_ID_2G=site_id, AT_STATUS__in= status)
        serializer_data = ser_Soft_At_ZTE_upload_table(obj, many=True)
        return Response({
            "Status": True,
            "message": "data sucessfully fetched....",
            "data": serializer_data.data,
        }) 


@api_view(["POST","GET"])
def testing(request):
    data=call_stored_procedure()
    return Response({"data":data})



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

        nokia_count = Soft_AT_NOKIA_Rejected_Table.objects.filter(Date_Time__range=(from_date,to_date))
        samasung_count = Soft_AT_SAMSUNG_Rejected_Table.objects.filter(Date_Time__range=(from_date,to_date))
        huawei_count = Soft_AT_HUAWEI_Rejected_Table.objects.filter(Date_Time__range=(from_date,to_date))

        accepted_nokia_count = nokia_count.filter(AT_STATUS__in=["ACCEPTED","ACCEPT" ])
        accepted_samasung_count = samasung_count.filter(AT_STATUS__in = ["ACCEPTED","ACCEPT" ])
        accepted_huawei_count = huawei_count.filter(AT_STATUS__in = ["ACCEPTED","ACCEPT" ])
        
        rejected_nokia_count = nokia_count.filter(AT_STATUS__in = ["REJECTED", "REJECT"])
        rejected_samasung_count = samasung_count.filter(AT_STATUS__in = ["REJECTED", "REJECT"])
        rejected_huawei_count = huawei_count.filter(AT_STATUS__in = ["REJECTED", "REJECT"])
        
    else:
        nokia_count = Soft_AT_NOKIA_Rejected_Table.objects.all()
        samasung_count = Soft_AT_SAMSUNG_Rejected_Table.objects.all()
        huawei_count = Soft_AT_HUAWEI_Rejected_Table.objects.all()
        eri_count = Soft_AT_ERI_Rejected_Table.objects.all()
        zte_count = Soft_AT_ZTE_Rejected_Table.objects.all()

        accepted_nokia_count =nokia_count.filter(AT_STATUS__in=["ACCEPTED","ACCEPT" ])
        accepted_samasung_count = samasung_count.filter(AT_STATUS__in=["ACCEPTED","ACCEPT" ])
        accepted_huawei_count = huawei_count.filter(AT_STATUS__in=["ACCEPTED","ACCEPT" ])
        accepted_eri_count = eri_count.filter(AT_STATUS__in=["ACCEPTED","ACCEPT" ])
        accepted_zte_count = zte_count.filter(AT_STATUS__in=["ACCEPTED","ACCEPT" ])
        
        rejected_nokia_count = nokia_count.filter(AT_STATUS__in = ["REJECTED", "REJECT"])
        rejected_samasung_count = samasung_count.filter(AT_STATUS__in = ["REJECTED", "REJECT"])
        rejected_huawei_count = huawei_count.filter(AT_STATUS__in = ["REJECTED", "REJECT"])
        rejected_eri_count = eri_count.filter(AT_STATUS__in = ["REJECTED", "REJECT"])
        rejected_zte_count = zte_count.filter(AT_STATUS__in = ["REJECTED", "REJECT"])

        overall_min_date,overall_max_date=get_min_max_date_time(nokia_count,samasung_count, huawei_count, eri_count, zte_count)
   
    offered_count=nokia_count.count() + samasung_count.count() + huawei_count.count() + eri_count.count() + zte_count.count()
    accepted_count=accepted_nokia_count.count() + accepted_samasung_count.count()+ accepted_huawei_count.count() + accepted_eri_count.count() + accepted_zte_count.count()
    rejected_count=rejected_nokia_count.count() + rejected_samasung_count.count() + rejected_huawei_count.count() + rejected_eri_count.count() + rejected_zte_count.count()

    percent_accepted_count = round((accepted_count/offered_count)*100, 2)
    percent_rejected_count = round((rejected_count/offered_count)*100, 2)
        
        
    data={"offered_count":offered_count,"accepted_count":accepted_count,"rejected_count":rejected_count,"percent_accepted_count":percent_accepted_count,"percent_rejected_count":percent_rejected_count,"min_time_date": overall_min_date,"max_time_date":overall_max_date,}


    return Response({
        "Status": True,
        "message": "fetched......",
        "data": data,
    })


def process_oem_data_2(from_date, to_date,circle,status,oem_model,oem_name):
    obj=oem_model.objects.filter(Date_Time__range=(from_date,to_date))
    circle_count = obj.filter(Circle=circle, AT_STATUS__in=status).count()
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
    total_huawei=0
    total_nokia=0
    total_Samsung=0
    total_eri = 0
    total_zte =  0
    unique_circles = get_unique_circles()

 

    for circle in unique_circles:
            circle_data={}
            if accepted_and_rejected.lower() == "false":
                # data["Status"] = "Rejected"
                # Process Rejected Data
                nokia_data = process_oem_data_2(
                    oem_model=Soft_AT_NOKIA_Rejected_Table,
                    oem_name="Nokia",
                    status=["REJECTED", "REJECT"],
                    circle= circle,
                    from_date=from_date,
                    to_date=to_date
                )   
               
                circle_data["Nokia"] = nokia_data

                huawei_data = process_oem_data_2(
                    from_date=from_date,
                    to_date=to_date,
                    oem_model=Soft_AT_HUAWEI_Rejected_Table,
                    oem_name="Huawei",
                    status=["REJECTED", "REJECT"],
                    circle= circle
                )
                circle_data["Huawei"] = huawei_data 
                eri_data = process_oem_data_2(
                    from_date=from_date,
                    to_date=to_date,
                    oem_model=Soft_AT_ERI_Rejected_Table,
                    oem_name="Ericcsion",
                    status=["REJECTED", "REJECT"],
                    circle= circle
                )
                circle_data["Ericcsion"] = eri_data
                samsung_data = process_oem_data_2(
                    from_date=from_date,
                    to_date=to_date,
                    oem_model=Soft_AT_SAMSUNG_Rejected_Table,
                    oem_name="Samsung",
                    status=["REJECTED", "REJECT"],
                    circle= circle
                )
                circle_data["Samsung"] = samsung_data
                zte_data = process_oem_data_2(
                    from_date=from_date,
                    to_date=to_date,
                    oem_model=Soft_AT_ZTE_Rejected_Table,
                    oem_name="Zte",
                    status=["REJECTED", "REJECT"],
                    circle= circle
                )
                circle_data["Zte"] = zte_data

            elif(accepted_and_rejected.lower() == "true"):
                # data["Status"] = "Accepted"
                # Process Accepted Data
                nokia_data = process_oem_data_2(
                    from_date=from_date,
                    to_date=to_date,
                    oem_model=Soft_AT_NOKIA_Rejected_Table,
                    oem_name="Nokia",
                    status=["ACCEPTED", "ACCEPT"],
                    circle= circle
                )
                circle_data["Nokia"] = nokia_data 

                huawei_data = process_oem_data_2(
                    from_date=from_date,
                    to_date=to_date,
                    oem_model=Soft_AT_HUAWEI_Rejected_Table,
                    oem_name="Huawei",
                    status=["ACCEPTED", "ACCEPT"],
                    circle= circle
                )
                circle_data["Huawei"] = huawei_data   

                circle_data["Huawei"] = huawei_data 
                eri_data = process_oem_data_2(
                    from_date=from_date,
                    to_date=to_date,
                    oem_model=Soft_AT_ERI_Rejected_Table,
                    oem_name="Ericcsion",
                    status=["ACCEPTED", "ACCEPT"],
                    circle= circle
                )
                circle_data["Ericcsion"] = eri_data
                samsung_data = process_oem_data_2(
                    from_date=from_date,
                    to_date=to_date,
                    oem_model=Soft_AT_SAMSUNG_Rejected_Table,
                    oem_name="Samsung",
                    status=["ACCEPTED", "ACCEPT"],
                    circle= circle
                )
                circle_data["Samsung"] = samsung_data
                zte_data = process_oem_data_2(
                    from_date=from_date,
                    to_date=to_date,
                    oem_model=Soft_AT_ZTE_Rejected_Table,
                    oem_name="Zte",
                    status=["ACCEPTED", "ACCEPT"],
                    circle= circle
                )
                circle_data["Zte"] = zte_data
            else:
                nokia_data = process_oem_data_2(
                    from_date=from_date,
                    to_date=to_date,
                    oem_model=Soft_AT_NOKIA_Rejected_Table,
                    oem_name="Nokia",
                    status=["ACCEPTED", "ACCEPT", "REJECTED", "REJECT"],
                    circle= circle
                )
                circle_data["Nokia"] = nokia_data 

                huawei_data = process_oem_data_2(
                    from_date=from_date,
                    to_date=to_date,
                    oem_model=Soft_AT_HUAWEI_Rejected_Table,
                    oem_name="Huawei",
                    status=["ACCEPTED", "ACCEPT", "REJECTED", "REJECT"],
                    circle= circle
                )
                circle_data["Huawei"] = huawei_data   

                circle_data["Huawei"] = huawei_data 
                eri_data = process_oem_data_2(
                    from_date=from_date,
                    to_date=to_date,
                    oem_model=Soft_AT_ERI_Rejected_Table,
                    oem_name="Ericcsion",
                    status=["ACCEPTED", "ACCEPT", "REJECTED", "REJECT"],
                    circle= circle
                )
                circle_data["Ericcsion"] = eri_data
                samsung_data = process_oem_data_2(
                    from_date=from_date,
                    to_date=to_date,
                    oem_model=Soft_AT_SAMSUNG_Rejected_Table,
                    oem_name="Samsung",
                    status=["ACCEPTED", "ACCEPT", "REJECTED", "REJECT"],
                    circle= circle
                )
                circle_data["Samsung"] = samsung_data
                zte_data = process_oem_data_2(
                    from_date=from_date,
                    to_date=to_date,
                    oem_model=Soft_AT_ZTE_Rejected_Table,
                    oem_name="Zte",
                    status=["ACCEPTED", "ACCEPT", "REJECTED", "REJECT"],
                    circle= circle
                )
                circle_data["Zte"] = zte_data

            

            print("Nokia__________", nokia_data)
            data[circle] = circle_data  
            total_huawei=total_huawei + huawei_data
            total_nokia=total_nokia+nokia_data 
            total_Samsung=total_Samsung+samsung_data
            total_eri = total_eri+eri_data
            
    nok_obj=Soft_AT_NOKIA_Rejected_Table.objects.filter(Date_Time__range=(from_date,to_date))
    sam_obj=Soft_AT_SAMSUNG_Rejected_Table.objects.filter(Date_Time__range=(from_date,to_date))
    hua_obj=Soft_AT_HUAWEI_Rejected_Table.objects.filter(Date_Time__range=(from_date,to_date))
    eri_obj=Soft_AT_ERI_Rejected_Table.objects.filter(Date_Time__range=(from_date,to_date))
    zte_obj=Soft_AT_ZTE_Rejected_Table.objects.filter(Date_Time__range=(from_date,to_date))
             
    min_time_date = get_min_max_date_time(nok_obj, sam_obj, hua_obj, eri_obj, zte_obj)[0]
    max_time_date = get_min_max_date_time(nok_obj, sam_obj, hua_obj,eri_obj, zte_obj)[1]
    data["total"] ={"Huawei":total_huawei,"Samsung":total_Samsung,"Nokia":total_nokia, "Ericcsion":total_eri, "Zte": total_zte}
    
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
    if(oem == "Nokia"):
        obj = Soft_AT_NOKIA_Rejected_Table.objects.filter(Date_Time__range=(from_date, to_date),Circle=circle, AT_STATUS__in= sts_dict[status])
        
        serializer_data = ser_Soft_At_NOK_upload_table(obj, many=True)
        return Response({
            "Status": True,

            "message": "data sucessfully fetched....",
            "data": serializer_data.data,
        })
        
    elif(oem == "Huawei"):
        
        obj = Soft_AT_HUAWEI_Rejected_Table.objects.filter(Date_Time__range=(from_date, to_date),Circle=circle, AT_STATUS__in= sts_dict[status])
        serializer_data = ser_Soft_At_HUA_upload_table(obj, many=True)

        return Response({
            "Status": True,
            "message": "data sucessfully fetched....",
            "data": serializer_data.data,
        }) 
    elif(oem == "Samsung"):
        obj = Soft_AT_SAMSUNG_Rejected_Table.objects.filter(Date_Time__range=(from_date, to_date),Circle=circle, AT_STATUS__in= sts_dict[status])
        serializer_data = ser_Soft_At_SAM_upload_table(obj, many=True)

        return Response({
            "Status": True,
            "message": "data sucessfully fetched....",
            "data": serializer_data.data,
        })
    elif(oem == "ZTE"):
        obj = Soft_AT_ZTE_Rejected_Table.objects.filter(Date_Time__range=(from_date, to_date),Circle=circle, AT_STATUS__in= sts_dict[status])
        serializer_data = ser_Soft_At_SAM_upload_table(obj, many=True)

        return Response({
            "Status": True,
            "message": "data sucessfully fetched....",
            "data": serializer_data.data,
        })
    
    elif(oem == "Ericsson"):
        obj = Soft_AT_ERI_Rejected_Table.objects.filter(Date_Time__range=(from_date, to_date),Circle=circle, AT_STATUS__in= sts_dict[status])
        serializer_data = ser_Soft_At_SAM_upload_table(obj, many=True)

        return Response({
            "Status": True,
            "message": "data sucessfully fetched....",
            "data": serializer_data.data,
        })



def unique_offered_date():
    obj_nok = Soft_AT_NOKIA_Rejected_Table.objects.values('Offered_Date').distinct()
    obj_hua = Soft_AT_HUAWEI_Rejected_Table.objects.values('Offer_Reoffer_date').distinct()
    obj_sam = Soft_AT_SAMSUNG_Rejected_Table.objects.values('Offer_Reoffer_Date').distinct()
    obj_zte = Soft_AT_ZTE_Rejected_Table.objects.values('Offer_Reoffer_date').distinct()
    obj_ERI = Soft_AT_ERI_Rejected_Table.objects.values('AT_Offering_Date').distinct()

    unique_offered_dates= list(obj_nok.union(obj_hua).union(obj_sam).union(obj_zte).union(obj_ERI))

   
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
        nok_obj=Soft_AT_NOKIA_Rejected_Table.objects.all()
        sam_obj=Soft_AT_SAMSUNG_Rejected_Table.objects.all()
        hua_obj=Soft_AT_HUAWEI_Rejected_Table.objects.all()
        eri_obj = Soft_AT_ERI_Rejected_Table.objects.all()
        zte_obj = Soft_AT_ZTE_Rejected_Table.objects.all()
        from_date,to_date= get_min_max_date_time(nok_obj, sam_obj, hua_obj, eri_obj, zte_obj)
        print("inside_circle_summanry ",from_date,to_date)

    print("From date", from_date,"-",to_date)
  
    unique_offered_dates = unique_offered_date()
    
    unique_offered_date_list = [date["Offered_Date"] for date in unique_offered_dates]
    unique_offered_date_list.remove(None)
    print("Unique offeered dates :",unique_offered_date_list)
    unique_offered_date_list.sort()
    if str_from_date != "" and str_to_date != "":
        from_date=dt.strptime(str_from_date,"%Y-%m-%d").date()
        to_date=dt.strptime(str_to_date,"%Y-%m-%d").date()
        print(from_date)
        print(to_date)
        unique_offered_date_list = list(filter(lambda x: from_date <= x <= to_date, unique_offered_date_list))
    print("hiiiiiiiiiiiiiiiiiii",unique_offered_dates)
    data={}
    for date in unique_offered_date_list:
        print(date)
        nok_obj = Soft_AT_NOKIA_Rejected_Table.objects.filter(Date_Time__range = (from_date, to_date)).filter(Offered_Date=date)
        sam_obj = Soft_AT_SAMSUNG_Rejected_Table.objects.filter(Date_Time__range = (from_date, to_date)).filter(Offer_Reoffer_Date=date)
        hua_obj = Soft_AT_HUAWEI_Rejected_Table.objects.filter(Date_Time__range = (from_date, to_date)).filter(Offer_Reoffer_date=date)
        zte_obj = Soft_AT_ZTE_Rejected_Table.objects.filter(Date_Time__range = (from_date, to_date)).filter(Offer_Reoffer_date=date)
        ERI_obj = Soft_AT_ERI_Rejected_Table.objects.filter(Date_Time__range = (from_date, to_date)).filter(AT_Offering_Date=date)


        accepted_nokia_count = nok_obj.filter(AT_STATUS__in=["ACCEPTED","ACCEPT" ])
        accepted_samasung_count = sam_obj.filter(AT_STATUS__in = ["ACCEPTED","ACCEPT" ])
        accepted_huawei_count = hua_obj.filter(AT_STATUS__in = ["ACCEPTED","ACCEPT" ])
        accepted_zte_count = zte_obj.filter(AT_STATUS__in = ["ACCEPTED","ACCEPT" ])
        accepted_eri_count = ERI_obj.filter(AT_STATUS__in = ["ACCEPTED","ACCEPT" ])
        
        rejected_nokia_count = nok_obj.filter(AT_STATUS__in = ["REJECTED", "REJECT"])
        rejected_samasung_count = sam_obj.filter(AT_STATUS__in = ["REJECTED", "REJECT"])
        rejected_huawei_count = hua_obj.filter(AT_STATUS__in = ["REJECTED", "REJECT"])
        rejected_zte_count = zte_obj.filter(AT_STATUS__in = ["REJECTED", "REJECT"])
        rejected_eri_count = ERI_obj.filter(AT_STATUS__in = ["REJECTED", "REJECT"])

        offered_count=nok_obj.count() + sam_obj.count() + hua_obj.count() + zte_obj.count() + ERI_obj.count()
        accepted_count=accepted_nokia_count.count() + accepted_samasung_count.count()+ accepted_huawei_count.count() + accepted_zte_count.count()+ accepted_eri_count.count()
        rejected_count=rejected_nokia_count.count() + rejected_samasung_count.count() + rejected_huawei_count.count() + rejected_eri_count.count()+ rejected_zte_count.count()

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

    nokia_data = Soft_AT_NOKIA_Rejected_Table.objects.filter(Offered_Date=offered_date, AT_STATUS__in=sts_dict[status]).values()
    huawei_data = Soft_AT_HUAWEI_Rejected_Table.objects.filter(Offer_Reoffer_date=offered_date, AT_STATUS__in=sts_dict[status]).values()
    samsung_data = Soft_AT_SAMSUNG_Rejected_Table.objects.filter(Offer_Reoffer_Date=offered_date, AT_STATUS__in=sts_dict[status]).values()
    eri_data = Soft_AT_ERI_Rejected_Table.objects.filter(AT_Offering_Date=offered_date, AT_STATUS__in=sts_dict[status]).values()
    zte_data = Soft_AT_ZTE_Rejected_Table.objects.filter(Offer_Reoffer_date=offered_date, AT_STATUS__in=sts_dict[status]).values()

    print("Count____________________",nokia_data.count()+huawei_data.count()+samsung_data.count())

    # Combine data into a list
    combined_data = {
        'nokia_data': list(nokia_data),
        'huawei_data': list(huawei_data),
        'samsung_data': list(samsung_data),
        'eri_data': list(samsung_data),
        'zte_data': list(zte_data),
    }

    return Response({
        "Status": True,
        "message": "Data successfully fetched....",
        "data": combined_data,
        # "Staus1": sts_dict[status],
        
    })




def process_oem_data_offered_wise(offered_date,circle,status,oem_model,oem_name):
    if(oem_name == "Nokia"):
        obj = oem_model.objects.filter(Offered_Date=offered_date)
        

        circle_count = obj.filter(Circle=circle, AT_STATUS__in=status).count()
        return circle_count

    elif(oem_name == "Huawei"):
        obj = oem_model.objects.filter(Offer_Reoffer_date=offered_date)
        
        circle_count = obj.filter(Circle=circle, AT_STATUS__in=status).count()
        return circle_count
    
    elif(oem_name == "Samsung"):
        obj = oem_model.objects.filter(Offer_Reoffer_Date=offered_date)

        circle_count = obj.filter(Circle=circle, AT_STATUS__in=status).count()
        return circle_count
    elif(oem_name == "ZTE"):
        obj = oem_model.objects.filter(Offer_Reoffer_date=offered_date)

        circle_count = obj.filter(Circle=circle, AT_STATUS__in=status).count()
        return circle_count
    elif(oem_name == "Ericcson"):
        obj = oem_model.objects.filter(AT_Offering_Date=offered_date)

        circle_count = obj.filter(Circle=circle, AT_STATUS__in=status).count()
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
    total_huawei=0
    total_nokia=0
    total_Samsung=0
    total_Ericcson=0
    total_zte=0
    unique_circles = get_unique_circles()

    

    for circle in unique_circles:
            circle_data={}
            if accepted_and_rejected.lower() == "false":
                # data["Status"] = "Rejected"
                # Process Rejected Data
                nokia_data = process_oem_data_offered_wise(
                    oem_model=Soft_AT_NOKIA_Rejected_Table,
                    oem_name="Nokia",
                    status=["REJECTED", "REJECT"],
                    circle= circle,
                    offered_date=offered_date,
                )   
               
                circle_data["Nokia"] = nokia_data

                huawei_data = process_oem_data_offered_wise(
                    oem_model=Soft_AT_HUAWEI_Rejected_Table,
                    oem_name="Huawei",
                    status=["REJECTED", "REJECT"],
                    circle= circle,
                    offered_date=offered_date
                )
                circle_data["Huawei"] = huawei_data 
                eri_data = process_oem_data_offered_wise(
                    oem_model=Soft_AT_ERI_Rejected_Table,
                    oem_name="Ericcson",
                    status=["REJECTED", "REJECT"],
                    circle= circle,
                    offered_date=offered_date
                )
                circle_data["Ericcson"] = eri_data

                zte_data = process_oem_data_offered_wise(
                    oem_model=Soft_AT_ZTE_Rejected_Table,
                    oem_name="ZTE",
                    status=["REJECTED", "REJECT"],
                    circle= circle,
                    offered_date=offered_date
                )
                circle_data["ZTE"] = zte_data

                samsung_data = process_oem_data_offered_wise(
                    oem_model=Soft_AT_SAMSUNG_Rejected_Table,
                    oem_name="Samsung",
                    status=["REJECTED", "REJECT"],
                    circle= circle,
                    offered_date=offered_date
                )
                circle_data["Samsung"] = samsung_data

            elif(accepted_and_rejected.lower() == "true"):
                # data["Status"] = "Accepted"
                # Process Accepted Data
                nokia_data = process_oem_data_offered_wise(
                    oem_model=Soft_AT_NOKIA_Rejected_Table,
                    oem_name="Nokia",
                    status=["ACCEPTED", "ACCEPT"],
                    circle= circle,
                    offered_date=offered_date
                )
                circle_data["Nokia"] = nokia_data 

                huawei_data = process_oem_data_offered_wise(
                    oem_model=Soft_AT_HUAWEI_Rejected_Table,
                    oem_name="Huawei",
                    status=["ACCEPTED", "ACCEPT"],
                    circle= circle,
                    offered_date=offered_date
                )
                circle_data["Huawei"] = huawei_data   

                samsung_data = process_oem_data_offered_wise(
                    oem_model=Soft_AT_SAMSUNG_Rejected_Table,
                    oem_name="Samsung",
                    status=["ACCEPTED", "ACCEPT"],
                    circle= circle,
                    offered_date=offered_date
                )
                circle_data["Samsung"] = samsung_data

                eri_data = process_oem_data_offered_wise(
                    oem_model=Soft_AT_ERI_Rejected_Table,
                    oem_name="Ericcson",
                    status=["ACCEPTED", "ACCEPT"],
                    circle= circle,
                    offered_date=offered_date
                )
                circle_data["Ericcson"] = eri_data

                zte_data = process_oem_data_offered_wise(
                    oem_model=Soft_AT_ZTE_Rejected_Table,
                    oem_name="ZTE",
                    status=["ACCEPTED", "ACCEPT"],
                    circle= circle,
                    offered_date=offered_date
                )
                circle_data["ZTE"] = zte_data
            else:
                nokia_data = process_oem_data_offered_wise(
                    
                    oem_model=Soft_AT_NOKIA_Rejected_Table,
                    oem_name="Nokia",
                    status=["ACCEPTED", "ACCEPT", "REJECTED", "REJECT"],
                    circle= circle,
                    offered_date=offered_date
                )
                circle_data["Nokia"] = nokia_data 

                huawei_data = process_oem_data_offered_wise(
                  
                    oem_model=Soft_AT_HUAWEI_Rejected_Table,
                    oem_name="Huawei",
                    status=["ACCEPTED", "ACCEPT", "REJECTED", "REJECT"],
                    circle= circle,
                    offered_date=offered_date
                )
                circle_data["Huawei"] = huawei_data   

                samsung_data = process_oem_data_offered_wise(
                    oem_model=Soft_AT_SAMSUNG_Rejected_Table,
                    oem_name="Samsung",
                    status=["ACCEPTED", "ACCEPT", "REJECTED", "REJECT"],
                    circle= circle,
                    offered_date=offered_date
                )
                circle_data["Samsung"] = samsung_data

                eri_data = process_oem_data_offered_wise(
                    oem_model=Soft_AT_ERI_Rejected_Table,
                    oem_name="Ericcson",
                    status=["ACCEPTED", "ACCEPT", "REJECTED", "REJECT"],
                    circle= circle,
                    offered_date=offered_date
                )
                circle_data["Ericcson"] = eri_data

                zte_data = process_oem_data_offered_wise(
                    oem_model=Soft_AT_ZTE_Rejected_Table,
                    oem_name="ZTE",
                    status=["ACCEPTED", "ACCEPT", "REJECTED", "REJECT"],
                    circle= circle,
                    offered_date=offered_date
                )
                circle_data["ZTE"] = zte_data

            

            print("Nokia__________", circle_data)
            data[circle] = circle_data  
            total_huawei=total_huawei + huawei_data
            total_nokia=total_nokia+nokia_data 
            total_Samsung=total_Samsung+samsung_data
            total_Ericcson = total_Ericcson + eri_data
            total_zte = total_zte + zte_data
            
    # nok_obj=Soft_AT_NOKIA_Rejected_Table.objects.filter(Offered_Date=offered_date)
    # sam_obj=Soft_AT_SAMSUNG_Rejected_Table.objects.filter(Offer_Reoffer_Date=offered_date)
    # hua_obj=Soft_AT_HUAWEI_Rejected_Table.objects.filter(Offer_Reoffer_date=offered_date)
    # eri_obj=Soft_AT_ERI_Rejected_Table.objects.filter(Offer_Reoffer_date=offered_date)
    # zte_obj=Soft_AT_ZTE_Rejected_Table.objects.filter(AT_Offering_Date=offered_date)
             
    # min_time_date = get_min_max_date_time(nok_obj, sam_obj, hua_obj)[0]
    # max_time_date = get_min_max_date_time(nok_obj, sam_obj, hua_obj)[1]
    data["total"] ={"Huawei":total_huawei,"Samsung":total_Samsung,"Nokia":total_nokia, "Ericcson": total_Ericcson, "ZTE": total_zte}
    
    # get_latest_date()

    return Response({
        "message": "Script executed successfully.",
        "status": True,
        "data": data,
        # "min_time_date": min_time_date,
        # "max_time_date": max_time_date,
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
        nok_obj=Soft_AT_NOKIA_Rejected_Table.objects.all()
        sam_obj=Soft_AT_SAMSUNG_Rejected_Table.objects.all()
        hua_obj=Soft_AT_HUAWEI_Rejected_Table.objects.all()
        eri_obj = Soft_AT_ERI_Rejected_Table.objects.all()
        zte_obj = Soft_AT_ZTE_Rejected_Table.objects.all()
        from_date,to_date= get_min_max_date_time(nok_obj, sam_obj, hua_obj, eri_obj, zte_obj)
        print("inside_circle_summanry ",from_date,to_date)
    with connection.cursor() as cursor:

        query = f"""

WITH all_ranges AS (
    select start_range || '-' || end_range as "range", start_range from (SELECT generate_series(1, 28, 3) AS start_range,
           generate_series(3, 30, 3) AS end_range) q1
	union 
	select '>30' as "range", 100 as start_range
)
-- SELECT * FROM all_ranges;


-- Left join the generated ranges with your_table to fill in missing ranges with 0 values
SELECT  ar.range,
       COALESCE(yt.rejected_site_count, 0) AS rejected_site_count
FROM all_ranges ar
LEFT JOIN 
(select "range",sum("repetition_count") as "rejected_site_count" from (SELECT "oem","Site_ID","repetition_count",
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
		from 
(SELECT "OEM" as oem,"Site_ID_2G" as "Site_ID" , COUNT(*) AS repetition_count
FROM public."Soft_AT_Rejected_soft_at_huawei_rejected_table"
WHERE "AT_STATUS" in ('REJECTED','REJECT') AND "Date_Time" between '{from_date}' AND '{to_date}'
GROUP BY "OEM","Site_ID_2G"
ORDER BY repetition_count DESC ) AS counts_per_site

union


SELECT oem,"Site_ID","repetition_count",
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
		from 
(SELECT "OEM" as oem, "Site_ID", COUNT(*) AS repetition_count
FROM public."Soft_AT_Rejected_soft_at_nokia_rejected_table"
WHERE "AT_STATUS" in ('REJECTED','REJECT') AND "Date_Time" between '{from_date}' AND '{to_date}'
GROUP BY "OEM","Site_ID" 
ORDER BY repetition_count DESC ) AS counts_per_site

union

SELECT oem,"Site_ID","repetition_count",
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
		from 
(SELECT "OEM" as oem,"Site_ID_2G" as "Site_ID", COUNT(*) AS repetition_count
FROM public."Soft_AT_Rejected_soft_at_samsung_rejected_table"
WHERE "AT_STATUS" in ('REJECTED','REJECT') AND "Date_Time" between '{from_date}' AND '{to_date}'
GROUP BY "OEM","Site_ID_2G"
ORDER BY repetition_count DESC ) AS counts_per_site 
union
	SELECT oem,"Site_ID","repetition_count",
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
		from 
(SELECT "OEM" as oem,"Site_ID" as "Site_ID", COUNT(*) AS repetition_count
FROM public."Soft_AT_Rejected_soft_at_eri_rejected_table"
WHERE "AT_STATUS" in ('REJECTED','REJECT') AND "Date_Time" between '{from_date}' AND '{to_date}'
GROUP BY "OEM","Site_ID"
ORDER BY repetition_count DESC ) AS counts_per_site 
union
	SELECT oem,"Site_ID","repetition_count",
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
		from 
(SELECT "OEM" as oem,"Site_ID" as "Site_ID", COUNT(*) AS repetition_count
FROM public."Soft_AT_Rejected_soft_at_zte_rejected_table"
WHERE "AT_STATUS" in ('REJECTED','REJECT') AND "Date_Time" between '{from_date}' AND '{to_date}'
GROUP BY "OEM","Site_ID"
ORDER BY repetition_count DESC ) AS counts_per_site 
)as all_tabs

group by "range"
order by range) yt ON yt.range = ar."range" 
order by start_range
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
        nok_obj=Soft_AT_NOKIA_Rejected_Table.objects.all()
        sam_obj=Soft_AT_SAMSUNG_Rejected_Table.objects.all()
        hua_obj=Soft_AT_HUAWEI_Rejected_Table.objects.all()
        eri_obj = Soft_AT_ERI_Rejected_Table.objects.all()
        zte_obj = Soft_AT_ZTE_Rejected_Table.objects.all()
        from_date,to_date= get_min_max_date_time(nok_obj, sam_obj, hua_obj, eri_obj, zte_obj)
        print("inside_circle_summanry ",from_date,to_date)

    range=request.POST.get('range')
    with connection.cursor() as cursor:

        query = f"""
                

		select * from 
	 	(select "Site_ID" ||' '|| "Circle" as "site_circle",oem,"Circle","Site_ID", repetition_count, range from 
		 (SELECT "oem","Circle","Site_ID","repetition_count",
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
				from 
		(SELECT "OEM" as oem,"Circle","Site_ID_2G" as "Site_ID" , COUNT(*) AS repetition_count
		FROM public."Soft_AT_Rejected_soft_at_huawei_rejected_table"
		WHERE "AT_STATUS" in ('REJECTED','REJECT') AND "Date_Time" between '{from_date}' AND '{to_date}'
		GROUP BY "OEM","Circle","Site_ID_2G"
		ORDER BY repetition_count DESC ) AS counts_per_site

		union


		SELECT oem,"Circle","Site_ID","repetition_count",
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
				from 
		(SELECT "OEM" as oem, "Circle","Site_ID", COUNT(*) AS repetition_count
		FROM public."Soft_AT_Rejected_soft_at_nokia_rejected_table"
		WHERE "AT_STATUS" in ('REJECTED','REJECT') AND "Date_Time" between '{from_date}' AND '{to_date}'
		GROUP BY "OEM","Circle","Site_ID"
		ORDER BY repetition_count DESC ) AS counts_per_site

		union

		SELECT oem,"Circle","Site_ID","repetition_count",
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
				from 
		(SELECT "OEM" as oem, "Circle","Site_ID", COUNT(*) AS repetition_count
		FROM public."Soft_AT_Rejected_soft_at_eri_rejected_table"
		WHERE "AT_STATUS" in ('REJECTED','REJECT') AND "Date_Time" between '{from_date}' AND '{to_date}'
		GROUP BY "OEM","Circle","Site_ID"
		ORDER BY repetition_count DESC ) AS counts_per_site																											 
		union
			SELECT oem,"Circle","Site_ID","repetition_count",
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
				from 
		(SELECT "OEM" as oem, "Circle","Site_ID", COUNT(*) AS repetition_count
		FROM public."Soft_AT_Rejected_soft_at_zte_rejected_table"
		WHERE "AT_STATUS" in ('REJECTED','REJECT') AND "Date_Time" between '{from_date}' AND '{to_date}'
		GROUP BY "OEM","Circle","Site_ID"
		ORDER BY repetition_count DESC ) AS counts_per_site
		union				

		SELECT oem,"Circle","Site_ID","repetition_count",
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
				from 
		(SELECT "OEM" as oem,"Circle","Site_ID_2G" as "Site_ID", COUNT(*) AS repetition_count
		FROM public."Soft_AT_Rejected_soft_at_samsung_rejected_table"
		WHERE "AT_STATUS" in ('REJECTED','REJECT') AND "Date_Time" between '{from_date}' AND '{to_date}'
		GROUP BY "OEM","Circle","Site_ID_2G"
		ORDER BY repetition_count DESC ) AS counts_per_site ) as t1

		order by range ) as ultimate_table
	 
    left JOIN 	
	(SELECT * FROM crosstab( $$ select "Site_ID" ||' '||"Circle" as "site_circle", "AT_REMARK", "AT_REMARK" from public."Soft_AT_Rejected_soft_at_nokia_rejected_table" where "AT_STATUS" in ('REJECT','REJECTED') AND "Date_Time" between '{from_date}' AND '{to_date}' order by 1,2 $$)
		 AS final_result( site_circle text,  r1 varchar,r2 varchar,r3 varchar,r4 varchar,r5 varchar,r6 varchar,r7 varchar,r8 varchar,r9 varchar,r10 varchar,r11 varchar,r12 varchar,r13 varchar,r14 varchar,r15 varchar)
	union
	SELECT * FROM crosstab( $$ select "Site_ID_2G" ||' '||"Circle" as "site_circle", "AT_Remarks", "AT_Remarks" from public."Soft_AT_Rejected_soft_at_huawei_rejected_table" where "AT_STATUS" in ('REJECT','REJECTED') AND "Date_Time" between '{from_date}' AND '{to_date}' order by 1,2 $$)
		 AS final_result( site_circle text,  r1 varchar,r2 varchar,r3 varchar,r4 varchar,r5 varchar,r6 varchar,r7 varchar,r8 varchar,r9 varchar,r10 varchar,r11 varchar,r12 varchar,r13 varchar,r14 varchar,r15 varchar) 	 
	union	 
	SELECT * FROM crosstab( $$ select "Site_ID_2G" ||' '||"Circle" as "site_circle", "AT_Remarks", "AT_Remarks" from public."Soft_AT_Rejected_soft_at_samsung_rejected_table" where "AT_STATUS" in ('REJECT','REJECTED') AND "Date_Time" between '{from_date}' AND '{to_date}' order by 1,2 $$)
		 AS final_result( site_circle text,  r1 varchar,r2 varchar,r3 varchar,r4 varchar,r5 varchar,r6 varchar,r7 varchar,r8 varchar,r9 varchar,r10 varchar,r11 varchar,r12 varchar,r13 varchar,r14 varchar,r15 varchar) 
	union
	SELECT * FROM crosstab( $$ select "Site_ID" ||' '||"Circle" as "site_circle", "AT_Remarks", "AT_Remarks" from public."Soft_AT_Rejected_soft_at_zte_rejected_table" where "AT_STATUS" in ('REJECT','REJECTED') AND "Date_Time" between '{from_date}' AND '{to_date}' order by 1,2 $$)
		 AS final_result( site_circle text,  r1 varchar,r2 varchar,r3 varchar,r4 varchar,r5 varchar,r6 varchar,r7 varchar,r8 varchar,r9 varchar,r10 varchar,r11 varchar,r12 varchar,r13 varchar,r14 varchar,r15 varchar) 
	union
	SELECT * FROM crosstab( $$ select "Site_ID" ||' '||"Circle" as "site_circle", "AT_Remarks", "AT_Remarks" from public."Soft_AT_Rejected_soft_at_eri_rejected_table" where "AT_STATUS" in ('REJECT','REJECTED') AND "Date_Time" between '{from_date}' AND '{to_date}' order by 1,2 $$)
		 AS final_result( site_circle text,  r1 varchar,r2 varchar,r3 varchar,r4 varchar,r5 varchar,r6 varchar,r7 varchar,r8 varchar,r9 varchar,r10 varchar,r11 varchar,r12 varchar,r13 varchar,r14 varchar,r15 varchar) 


	) as t3 
		 on ultimate_table.site_circle =t3.site_circle 
	 
left JOIN 

 (select * from (select  "Site_ID" ||' '|| "Circle" as "site_circle" ,"Site_ID" as "site_id",CURRENT_DATE - "Offered_Date" as "ageing" from (select *, ROW_NUMBER() over (partition by "Site_ID" order by "Offered_Date") as "row_num"  from public."Soft_AT_Rejected_soft_at_nokia_rejected_table" where "AT_STATUS" in ('REJECTED','REJECT') AND "Date_Time" between '{from_date}' AND '{to_date}' ) as t1
where row_num =1

union

select  "Site_ID_2G" ||' '|| "Circle" as "site_circle" ,"Site_ID_2G" as "site_id",CURRENT_DATE - "Offer_Reoffer_date" as "ageing" from (select *, ROW_NUMBER() over (partition by "Site_ID_2G" order by "Offer_Reoffer_date") as "row_num"  from public."Soft_AT_Rejected_soft_at_huawei_rejected_table" where "AT_STATUS" in ('REJECTED','REJECT')AND "Date_Time" between '{from_date}' AND '{to_date}') as t1
where row_num =1

union

select  "Site_ID_2G" ||' '|| "Circle" as "site_circle" ,"Site_ID_2G" as "site_id",CURRENT_DATE - "Offer_Reoffer_Date" as "ageing" from (select *, ROW_NUMBER() over (partition by "Site_ID_2G" order by "Offer_Reoffer_Date") as "row_num"  from public."Soft_AT_Rejected_soft_at_samsung_rejected_table" where "AT_STATUS" in ('REJECTED','REJECT') AND "Date_Time" between '{from_date}' AND '{to_date}') as t1
where row_num =1

union

select  "Site_ID" ||' '|| "Circle" as "site_circle" ,"Site_ID" as "site_id",CURRENT_DATE - "AT_Offering_Date" as "ageing" from (select *, ROW_NUMBER() over (partition by "Site_ID" order by "AT_Offering_Date") as "row_num"  from public."Soft_AT_Rejected_soft_at_eri_rejected_table" where "AT_STATUS" in ('REJECTED','REJECT') AND "Date_Time" between '{from_date}' AND '{to_date}') as t1
where row_num =1 

union

select  "Site_ID" ||' '|| "Circle" as "site_circle" ,"Site_ID" as "site_id",CURRENT_DATE - "Offer_Reoffer_date" as "ageing" from (select *, ROW_NUMBER() over (partition by "Site_ID" order by "Offer_Reoffer_date") as "row_num"  from public."Soft_AT_Rejected_soft_at_zte_rejected_table" where "AT_STATUS" in ('REJECTED','REJECT') AND "Date_Time" between '{from_date}' AND '{to_date}') as t1
where row_num =1 ) as tt  ) as ageing_table 
on t3.site_circle = ageing_table.site_circle
where range ='{range}'
     ;

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


@api_view(["GET","POST"])
def OverAllCircleWiseSummary(request):

    str_from_date = request.POST.get("from_date")
    str_to_date = request.POST.get("to_date")
    if str_from_date != ""  and str_to_date !='':
        from_date=dt.strptime(str_from_date,"%Y-%m-%d %H:%M:%S")
        to_date=dt.strptime(str_to_date,"%Y-%m-%d %H:%M:%S")
    else:
        nok_obj=Soft_AT_NOKIA_Rejected_Table.objects.all()
        sam_obj=Soft_AT_SAMSUNG_Rejected_Table.objects.all()
        hua_obj=Soft_AT_HUAWEI_Rejected_Table.objects.all()
        eri_obj = Soft_AT_ERI_Rejected_Table.objects.all()
        zte_obj = Soft_AT_ZTE_Rejected_Table.objects.all()
        from_date,to_date= get_min_max_date_time(nok_obj, sam_obj, hua_obj, eri_obj, zte_obj)
        print("inside_circle_summanry ",from_date,to_date)

    unique_circle = get_unique_circles()
    data={}
    for circle in unique_circle:
        nok_obj = Soft_AT_NOKIA_Rejected_Table.objects.filter(Circle = circle, Date_Time__range=(from_date, to_date))
        sam_obj = Soft_AT_SAMSUNG_Rejected_Table.objects.filter(Circle = circle, Date_Time__range=(from_date, to_date))
        hua_obj = Soft_AT_HUAWEI_Rejected_Table.objects.filter(Circle = circle,Date_Time__range=(from_date, to_date))
        zte_obj = Soft_AT_ZTE_Rejected_Table.objects.filter(Circle = circle,Date_Time__range=(from_date, to_date))
        ERI_obj = Soft_AT_ERI_Rejected_Table.objects.filter(Circle = circle,Date_Time__range=(from_date, to_date))


        accepted_nokia_count = nok_obj.filter(AT_STATUS__in=["ACCEPTED","ACCEPT" ])
        accepted_samasung_count = sam_obj.filter(AT_STATUS__in = ["ACCEPTED","ACCEPT" ])
        accepted_huawei_count = hua_obj.filter(AT_STATUS__in = ["ACCEPTED","ACCEPT" ])
        accepted_zte_count = zte_obj.filter(AT_STATUS__in = ["ACCEPTED","ACCEPT" ])
        accepted_eri_count = ERI_obj.filter(AT_STATUS__in = ["ACCEPTED","ACCEPT" ])
        
        rejected_nokia_count = nok_obj.filter(AT_STATUS__in = ["REJECTED", "REJECT"])
        rejected_samasung_count = sam_obj.filter(AT_STATUS__in = ["REJECTED", "REJECT"])
        rejected_huawei_count = hua_obj.filter(AT_STATUS__in = ["REJECTED", "REJECT"])
        rejected_zte_count = zte_obj.filter(AT_STATUS__in = ["REJECTED", "REJECT"])
        rejected_eri_count = ERI_obj.filter(AT_STATUS__in = ["REJECTED", "REJECT"])

        offered_count=nok_obj.count() + sam_obj.count() + hua_obj.count() + zte_obj.count() + ERI_obj.count()
        accepted_count=accepted_nokia_count.count() + accepted_samasung_count.count()+ accepted_huawei_count.count() + accepted_zte_count.count()+ accepted_eri_count.count()
        rejected_count=rejected_nokia_count.count() + rejected_samasung_count.count() + rejected_huawei_count.count() + rejected_eri_count.count()+ rejected_zte_count.count()
        percent_accepted_count = round((accepted_count/offered_count)*100, 2)
        percent_rejected_count = round((rejected_count/offered_count)*100, 2)
        data[str(circle)]={"Offered_count":offered_count,"accepted_count":accepted_count,"rejected_count":rejected_count,"accepted_percentage":percent_accepted_count,"rejected_percentage":percent_rejected_count}
        
    return Response({
    "message": "Successfully.",
    "status": True,
    "data": data,
    })



@api_view(["GET","POST"])
def overall_oem_wise_circle_wise_summary(request):

    str_from_date = request.POST.get("from_date")
    str_to_date = request.POST.get("to_date")
    if str_from_date != ""  and str_to_date !='':
        from_date=dt.strptime(str_from_date,"%Y-%m-%d %H:%M:%S")
        to_date=dt.strptime(str_to_date,"%Y-%m-%d %H:%M:%S")
    else:
        nok_obj=Soft_AT_NOKIA_Rejected_Table.objects.all()
        sam_obj=Soft_AT_SAMSUNG_Rejected_Table.objects.all()
        hua_obj=Soft_AT_HUAWEI_Rejected_Table.objects.all()
        eri_obj = Soft_AT_ERI_Rejected_Table.objects.all()
        zte_obj = Soft_AT_ZTE_Rejected_Table.objects.all()
        from_date,to_date= get_min_max_date_time(nok_obj, sam_obj, hua_obj, eri_obj, zte_obj)
        print("inside_circle_summanry ",from_date,to_date)

    print("From date", from_date,"-",to_date)
    data={}
    unique_circle = get_unique_circles()
    for circle in unique_circle:
        circle_data={}
        nokia_rejected =  process_oem_data_2(
             from_date= from_date,
             to_date= to_date,
             circle= circle,
             status=["REJECTED", "REJECT"],
             oem_model=Soft_AT_NOKIA_Rejected_Table,
             oem_name="Nokia",
            )   
        nokia_accepted =  process_oem_data_2(
            oem_model=Soft_AT_NOKIA_Rejected_Table,
            oem_name="Nokia",
            status=["ACCEPTED", "ACCEPT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            )
        nokia_offered =  process_oem_data_2(
            oem_model=Soft_AT_NOKIA_Rejected_Table,
            oem_name="Nokia",
            status=["ACCEPTED","ACCEPT","REJECTED", "REJECT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            
            
            )
        if nokia_offered != 0:
            percent_accepted_count = round((nokia_accepted/nokia_offered)*100, 2)
            percent_rejected_count = round((nokia_rejected/nokia_offered)*100, 2)
        else:
            percent_accepted_count = 0
            percent_rejected_count = 0
            
        circle_data["Nokia"] = {"offered":nokia_offered,"accepted":nokia_accepted,"rejected":nokia_rejected,"accepted_percentage":percent_accepted_count,"rejected_percentage":percent_rejected_count}

        huawei_rejected = process_oem_data_2(
            oem_model=Soft_AT_HUAWEI_Rejected_Table,
            oem_name="Huawei",
            status=["REJECTED", "REJECT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            
        )
        huawei_accepted = process_oem_data_2(
            oem_model=Soft_AT_HUAWEI_Rejected_Table,
            oem_name="Huawei",
            status=["ACCEPTED", "ACCEPT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            
        )
        huawei_offered = process_oem_data_2(
            oem_model=Soft_AT_HUAWEI_Rejected_Table,
            oem_name="Huawei",
            status=["ACCEPTED", "ACCEPT", "REJECTED", "REJECT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            
        )

        if huawei_offered != 0:
            percent_accepted_count = round((huawei_accepted/huawei_offered)*100, 2)
            percent_rejected_count = round((huawei_rejected/huawei_offered)*100, 2)
        else:
            percent_accepted_count = 0
            percent_rejected_count = 0


        
        circle_data["Huawei"] = {"offered":huawei_offered,"accepted":huawei_accepted,"rejected":huawei_rejected,"accepted_percentage":percent_accepted_count,"rejected_percentage":percent_rejected_count}
        samsung_rejected = process_oem_data_2(
            oem_model=Soft_AT_SAMSUNG_Rejected_Table,
            oem_name="Samsung",
            status=["REJECTED", "REJECT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            
        )
        samsung_accepted = process_oem_data_2(
            oem_model=Soft_AT_SAMSUNG_Rejected_Table,
            oem_name="Samsung",
            status=["ACCEPT", "ACCEPTED"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            
        )
        samsung_offered =  process_oem_data_2(
            oem_model=Soft_AT_SAMSUNG_Rejected_Table,
            oem_name="Samsung",
            status=["REJECTED", "REJECT","ACCEPTED", "ACCEPT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            
        )

        if samsung_offered != 0:
            percent_accepted_count = round((samsung_accepted/samsung_offered)*100, 2)
            percent_rejected_count = round((samsung_rejected/samsung_offered)*100, 2)
        else:
            percent_accepted_count = 0
            percent_rejected_count = 0
        circle_data["Samsung"] = {"offered":samsung_offered,"accepted":samsung_accepted,"rejected":samsung_rejected,"accepted_percentage":percent_accepted_count,"rejected_percentage":percent_rejected_count}
        
        data[circle]=circle_data
        eri_rejected = process_oem_data_2(
            oem_model=Soft_AT_ERI_Rejected_Table,
            oem_name="Ericcsion",
            status=["REJECTED", "REJECT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            
        )
        eri_accepted = process_oem_data_2(
            oem_model=Soft_AT_ERI_Rejected_Table,
            oem_name="Ericcsion",
            status=["REJECTED", "REJECT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            
        )
        eri_offered =  process_oem_data_2(
            oem_model=Soft_AT_ERI_Rejected_Table,
            oem_name="Ericsion",
            status=["REJECTED", "REJECT","ACCEPTED", "ACCEPT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            
        )

        if eri_offered != 0:
            percent_accepted_count = round((eri_accepted/eri_offered)*100, 2)
            percent_rejected_count = round((eri_rejected/eri_offered)*100, 2)
        else:
            percent_accepted_count = 0
            percent_rejected_count = 0
        circle_data["Ericsson"] = {"offered":eri_accepted,"accepted":eri_rejected,"rejected":eri_offered,"accepted_percentage":percent_accepted_count,"rejected_percentage":percent_rejected_count}
        
        data[circle]=circle_data
        zte_rejected = process_oem_data_2(
            oem_model=Soft_AT_ZTE_Rejected_Table,
            oem_name="zte",
            status=["REJECTED", "REJECT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            
        )
        zte_accepted = process_oem_data_2(
            oem_model=Soft_AT_ZTE_Rejected_Table,
            oem_name="zte",
            status=["REJECTED", "REJECT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            
        )
        zte_offered =  process_oem_data_2(
            oem_model=Soft_AT_ZTE_Rejected_Table,
            oem_name="zte",
            status=["REJECTED", "REJECT","ACCEPTED", "ACCEPT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            
        )

        if zte_offered != 0:
            percent_accepted_count = round((zte_accepted/zte_offered)*100, 2)
            percent_rejected_count = round((zte_rejected/zte_offered)*100, 2)
        else:
            percent_accepted_count = 0
            percent_rejected_count = 0
        circle_data["ZTE"] = {"offered":zte_accepted,"accepted":zte_rejected,"rejected":zte_offered,"accepted_percentage":percent_accepted_count,"rejected_percentage":percent_rejected_count}
        
        data[circle]=circle_data

    return Response({
        "Status": True,
        "message": "data feteched successfully",
        "data": data
    })


        



        






    # {
    # ap:{nokia:{offered:29,accepte:20,rej:9,rej%:20,ac%20},huawei:{nokia:{offered:29,accepte:20,rej:9,rej%:20,ac%20}}
    # MP:{nokia:{offered:29,accepte:20,rej:9,rej%:20,ac%20},huawei:{nokia:{offered:29,accepte:20,rej:9,rej%:20,ac%20}
    # }
def process_oem_data_3(from_date, to_date,circle,status,oem_model,oem_name, offered_date):

    if(oem_name == "Nokia"):
        obj = oem_model.objects.filter(Date_Time__range = (from_date, to_date)).filter(Offered_Date=offered_date)
        
        circle_count = obj.filter(Circle=circle, AT_STATUS__in=status).count()
        return circle_count

    elif(oem_name == "Huawei"):
        obj = oem_model.objects.filter(Date_Time__range = (from_date, to_date)).filter(Offer_Reoffer_date=offered_date)
        circle_count = obj.filter(Circle=circle, AT_STATUS__in=status).count()
        return circle_count
    
    elif(oem_name == "Samsung"):
        obj = oem_model.objects.filter(Date_Time__range = (from_date, to_date)).filter(Offer_Reoffer_Date=offered_date)
        circle_count = obj.filter(Circle=circle, AT_STATUS__in=status).count()
        return circle_count
    elif(oem_name == "zte"):
        obj = oem_model.objects.filter(Date_Time__range = (from_date, to_date)).filter(Offer_Reoffer_date=offered_date)

        circle_count = obj.filter(Circle=circle, AT_STATUS__in=status).count()
        return circle_count
    elif(oem_name == "Ericcsion"):
        obj = oem_model.objects.filter(Date_Time__range = (from_date, to_date)).filter(AT_Offering_Date=offered_date)
        circle_count = obj.filter(Circle=circle, AT_STATUS__in=status).count()
        return circle_count
    else:
        pass
    # obj=oem_model.objects.all()
    # print("msmsmsmsmsmsmsmms",type(obj))
    # circle_count = obj.filter(Circle=circle, AT_STATUS__in=status).count()
    # return circle_count


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
        nok_obj=Soft_AT_NOKIA_Rejected_Table.objects.all()
        sam_obj=Soft_AT_SAMSUNG_Rejected_Table.objects.all()
        hua_obj=Soft_AT_HUAWEI_Rejected_Table.objects.all()
        eri_obj = Soft_AT_ERI_Rejected_Table.objects.all()
        zte_obj = Soft_AT_ZTE_Rejected_Table.objects.all()
        from_date,to_date= get_min_max_date_time(nok_obj, sam_obj, hua_obj, eri_obj, zte_obj)
        print("inside_circle_summanry ",from_date,to_date)

    print("From date", from_date,"-",to_date)
    data={}
    unique_circle = get_unique_circles()
    for circle in unique_circle:
        circle_data={}
        nokia_rejected =  process_oem_data_3(
             from_date= from_date,
             to_date= to_date,
             offered_date = offered_date,
             circle= circle,
             status=["REJECTED", "REJECT"],
             oem_model=Soft_AT_NOKIA_Rejected_Table,
             oem_name="Nokia",
            )   
        nokia_accepted =  process_oem_data_3(
            oem_model=Soft_AT_NOKIA_Rejected_Table,
            oem_name="Nokia",
            status=["ACCEPTED", "ACCEPT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            offered_date = offered_date
            )
        nokia_offered =  process_oem_data_3(
            oem_model=Soft_AT_NOKIA_Rejected_Table,
            oem_name="Nokia",
            status=["ACCEPTED","ACCEPT","REJECTED", "REJECT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            offered_date = offered_date
            
            
            )
        if nokia_offered != 0:
            percent_accepted_count = round((nokia_accepted/nokia_offered)*100, 2)
            percent_rejected_count = round((nokia_rejected/nokia_offered)*100, 2)
        else:
            percent_accepted_count = 0
            percent_rejected_count = 0
            
        circle_data["Nokia"] = {"offered":nokia_offered,"accepted":nokia_accepted,"rejected":nokia_rejected,"accepted_percentage":percent_accepted_count,"rejected_percentage":percent_rejected_count}

        huawei_rejected = process_oem_data_3(
            oem_model=Soft_AT_HUAWEI_Rejected_Table,
            oem_name="Huawei",
            status=["REJECTED", "REJECT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            offered_date = offered_date
            
        )
        huawei_accepted = process_oem_data_3(
            oem_model=Soft_AT_HUAWEI_Rejected_Table,
            oem_name="Huawei",
            status=["ACCEPTED", "ACCEPT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            offered_date = offered_date
            
        )
        huawei_offered = process_oem_data_3(
            oem_model=Soft_AT_HUAWEI_Rejected_Table,
            oem_name="Huawei",
            status=["ACCEPTED", "ACCEPT", "REJECTED", "REJECT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            offered_date = offered_date
            
        )

        if huawei_offered != 0:
            percent_accepted_count = round((huawei_accepted/huawei_offered)*100, 2)
            percent_rejected_count = round((huawei_rejected/huawei_offered)*100, 2)
        else:
            percent_accepted_count = 0
            percent_rejected_count = 0


        
        circle_data["Huawei"] = {"offered":huawei_offered,"accepted":huawei_accepted,"rejected":huawei_rejected,"accepted_percentage":percent_accepted_count,"rejected_percentage":percent_rejected_count}
        samsung_rejected = process_oem_data_3(
            oem_model=Soft_AT_SAMSUNG_Rejected_Table,
            oem_name="Samsung",
            status=["REJECTED", "REJECT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            offered_date = offered_date
            

            
        )
        samsung_accepted = process_oem_data_3(
            oem_model=Soft_AT_SAMSUNG_Rejected_Table,
            oem_name="Samsung",
            status=["ACCEPTED", "ACCEPT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            offered_date = offered_date
            
        )
        samsung_offered =  process_oem_data_3(
            oem_model=Soft_AT_SAMSUNG_Rejected_Table,
            oem_name="Samsung",
            status=["REJECTED", "REJECT","ACCEPTED", "ACCEPT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            offered_date = offered_date
        )

        if samsung_offered != 0:
            percent_accepted_count = round((samsung_accepted/samsung_offered)*100, 2)
            percent_rejected_count = round((samsung_rejected/samsung_offered)*100, 2)
        else:
            percent_accepted_count = 0
            percent_rejected_count = 0
        circle_data["Samsung"] = {"offered":samsung_offered,"accepted":samsung_accepted,"rejected":samsung_rejected,"accepted_percentage":percent_accepted_count,"rejected_percentage":percent_rejected_count}
        
        data[circle]=circle_data
        eri_rejected = process_oem_data_3(
            oem_model=Soft_AT_ERI_Rejected_Table,
            oem_name="Ericcsion",
            status=["REJECTED", "REJECT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            offered_date = offered_date
            
        )
        eri_accepted = process_oem_data_3(
            oem_model=Soft_AT_ERI_Rejected_Table,
            oem_name="Ericcsion",
            status=["ACCEPTED", "ACCEPT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            offered_date = offered_date
            
        )
        eri_offered =  process_oem_data_3(
            oem_model=Soft_AT_ERI_Rejected_Table,
            oem_name="Ericcsion",
            status=["REJECTED", "REJECT","ACCEPTED", "ACCEPT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            offered_date = offered_date
            
        )

        if eri_offered != 0:
            percent_accepted_count = round((eri_accepted/eri_offered)*100, 2)
            percent_rejected_count = round((eri_rejected/eri_offered)*100, 2)
        else:
            percent_accepted_count = 0
            percent_rejected_count = 0
        circle_data["Ericsson"] = {"offered":eri_offered,"accepted":eri_rejected,"rejected":eri_offered,"accepted_percentage":percent_accepted_count,"rejected_percentage":percent_rejected_count}
        
        data[circle]=circle_data
        zte_rejected = process_oem_data_3(
            oem_model=Soft_AT_ZTE_Rejected_Table,
            oem_name="zte",
            status=["REJECTED", "REJECT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            offered_date = offered_date
        )
        zte_accepted = process_oem_data_3(
            oem_model=Soft_AT_ZTE_Rejected_Table,
            oem_name="zte",
            status=["ACCEPTED", "ACCEPT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            offered_date = offered_date
            
        )
        zte_offered =  process_oem_data_3(
            oem_model=Soft_AT_ZTE_Rejected_Table,
            oem_name="zte",
            status=["REJECTED", "REJECT","ACCEPTED", "ACCEPT"],
            circle= circle,
            from_date= from_date,
            to_date= to_date,
            offered_date = offered_date
            
        )

        if zte_offered != 0:
            percent_accepted_count = round((zte_accepted/zte_offered)*100, 2)
            percent_rejected_count = round((zte_rejected/zte_offered)*100, 2)
        else:
            percent_accepted_count = 0
            percent_rejected_count = 0
        circle_data["ZTE"] = {"offered":zte_offered,"accepted":zte_rejected,"rejected":zte_offered,"accepted_percentage":percent_accepted_count,"rejected_percentage":percent_rejected_count}
        
        data[circle]=circle_data

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
        nok_obj=Soft_AT_NOKIA_Rejected_Table.objects.all()
        sam_obj=Soft_AT_SAMSUNG_Rejected_Table.objects.all()
        hua_obj=Soft_AT_HUAWEI_Rejected_Table.objects.all()
        eri_obj = Soft_AT_ERI_Rejected_Table.objects.all()
        zte_obj = Soft_AT_ZTE_Rejected_Table.objects.all()
        from_date,to_date= get_min_max_date_time(nok_obj, sam_obj, hua_obj, eri_obj, zte_obj)
        print("inside_circle_summanry ",from_date,to_date)

    print("From date", from_date,"-",to_date)
    # to_date=dt(2024,1,30)
    # from_date=dt(2024,1,27)
    
    data = {}
    total_huawei=0
    total_nokia=0
    total_Samsung=0
    total_eri = 0
    total_zte =  0
    # unique_circles = get_unique_circles()

    

    # for circle in unique_circles:
    circle_data={}
    if accepted_and_rejected.lower() == "false":
        # data["Status"] = "Rejected"
        # Process Rejected Data
        nokia_data = process_oem_data_2(
            oem_model=Soft_AT_NOKIA_Rejected_Table,
            oem_name="Nokia",
            status=["REJECTED", "REJECT"],
            circle= circle,
            from_date=from_date,
            to_date=to_date
        )   
        
        circle_data["Nokia"] = nokia_data

        huawei_data = process_oem_data_2(
            from_date=from_date,
            to_date=to_date,
            oem_model=Soft_AT_HUAWEI_Rejected_Table,
            oem_name="Huawei",
            status=["REJECTED", "REJECT"],
            circle= circle
        )
        circle_data["Huawei"] = huawei_data 
        eri_data = process_oem_data_2(
            from_date=from_date,
            to_date=to_date,
            oem_model=Soft_AT_ERI_Rejected_Table,
            oem_name="Ericcsion",
            status=["REJECTED", "REJECT"],
            circle= circle
        )
        circle_data["Ericcsion"] = eri_data
        samsung_data = process_oem_data_2(
            from_date=from_date,
            to_date=to_date,
            oem_model=Soft_AT_SAMSUNG_Rejected_Table,
            oem_name="Samsung",
            status=["REJECTED", "REJECT"],
            circle= circle
        )
        circle_data["Samsung"] = samsung_data
        zte_data = process_oem_data_2(
            from_date=from_date,
            to_date=to_date,
            oem_model=Soft_AT_ZTE_Rejected_Table,
            oem_name="Zte",
            status=["REJECTED", "REJECT"],
            circle= circle
        )
        circle_data["Zte"] = zte_data

    elif(accepted_and_rejected.lower() == "true"):
        # data["Status"] = "Accepted"
        # Process Accepted Data
        nokia_data = process_oem_data_2(
            from_date=from_date,
            to_date=to_date,
            oem_model=Soft_AT_NOKIA_Rejected_Table,
            oem_name="Nokia",
            status=["ACCEPTED", "ACCEPT"],
            circle= circle
        )
        circle_data["Nokia"] = nokia_data 

        huawei_data = process_oem_data_2(
            from_date=from_date,
            to_date=to_date,
            oem_model=Soft_AT_HUAWEI_Rejected_Table,
            oem_name="Huawei",
            status=["ACCEPTED", "ACCEPT"],
            circle= circle
        )
        circle_data["Huawei"] = huawei_data   

        circle_data["Huawei"] = huawei_data 
        eri_data = process_oem_data_2(
            from_date=from_date,
            to_date=to_date,
            oem_model=Soft_AT_ERI_Rejected_Table,
            oem_name="Ericcsion",
            status=["ACCEPTED", "ACCEPT"],
            circle= circle
        )
        circle_data["Ericcsion"] = eri_data
        samsung_data = process_oem_data_2(
            from_date=from_date,
            to_date=to_date,
            oem_model=Soft_AT_SAMSUNG_Rejected_Table,
            oem_name="Samsung",
            status=["ACCEPTED", "ACCEPT"],
            circle= circle
        )
        circle_data["Samsung"] = samsung_data
        zte_data = process_oem_data_2(
            from_date=from_date,
            to_date=to_date,
            oem_model=Soft_AT_ZTE_Rejected_Table,
            oem_name="Zte",
            status=["ACCEPTED", "ACCEPT"],
            circle= circle
        )
        circle_data["Zte"] = zte_data
    else:
        nokia_data = process_oem_data_2(
            from_date=from_date,
            to_date=to_date,
            oem_model=Soft_AT_NOKIA_Rejected_Table,
            oem_name="Nokia",
            status=["ACCEPTED", "ACCEPT", "REJECTED", "REJECT"],
            circle= circle
        )
        circle_data["Nokia"] = nokia_data 

        huawei_data = process_oem_data_2(
            from_date=from_date,
            to_date=to_date,
            oem_model=Soft_AT_HUAWEI_Rejected_Table,
            oem_name="Huawei",
            status=["ACCEPTED", "ACCEPT", "REJECTED", "REJECT"],
            circle= circle
        )
        circle_data["Huawei"] = huawei_data   

        circle_data["Huawei"] = huawei_data 
        eri_data = process_oem_data_2(
            from_date=from_date,
            to_date=to_date,
            oem_model=Soft_AT_ERI_Rejected_Table,
            oem_name="Ericcsion",
            status=["ACCEPTED", "ACCEPT", "REJECTED", "REJECT"],
            circle= circle
        )
        circle_data["Ericcsion"] = eri_data
        samsung_data = process_oem_data_2(
            from_date=from_date,
            to_date=to_date,
            oem_model=Soft_AT_SAMSUNG_Rejected_Table,
            oem_name="Samsung",
            status=["ACCEPTED", "ACCEPT", "REJECTED", "REJECT"],
            circle= circle
        )
        circle_data["Samsung"] = samsung_data
        zte_data = process_oem_data_2(
            from_date=from_date,
            to_date=to_date,
            oem_model=Soft_AT_ZTE_Rejected_Table,
            oem_name="Zte",
            status=["ACCEPTED", "ACCEPT", "REJECTED", "REJECT"],
            circle= circle
        )
        circle_data["Zte"] = zte_data

    

    print("Nokia__________", nokia_data)
    data[circle] = circle_data  
    total_huawei=total_huawei + huawei_data
    total_nokia=total_nokia+nokia_data 
    total_Samsung=total_Samsung+samsung_data
    total_eri = total_eri+eri_data
            
    nok_obj=Soft_AT_NOKIA_Rejected_Table.objects.filter(Date_Time__range=(from_date,to_date))
    sam_obj=Soft_AT_SAMSUNG_Rejected_Table.objects.filter(Date_Time__range=(from_date,to_date))
    hua_obj=Soft_AT_HUAWEI_Rejected_Table.objects.filter(Date_Time__range=(from_date,to_date))
    eri_obj=Soft_AT_ERI_Rejected_Table.objects.filter(Date_Time__range=(from_date,to_date))
    zte_obj=Soft_AT_ZTE_Rejected_Table.objects.filter(Date_Time__range=(from_date,to_date))
             
    min_time_date = get_min_max_date_time(nok_obj, sam_obj, hua_obj, eri_obj, zte_obj)[0]
    max_time_date = get_min_max_date_time(nok_obj, sam_obj, hua_obj,eri_obj, zte_obj)[1]
    data["total"] ={"Huawei":total_huawei,"Samsung":total_Samsung,"Nokia":total_nokia, "Ericcsion":total_eri, "Zte": total_zte}
    
    # get_latest_date()

    return Response({
        "message": "Script executed successfully.",
        "status": True,
        "data": data,
        "min_time_date": min_time_date,
        "max_time_date": max_time_date,
    })


@api_view(["POST", "GET"])
def central_spoc_performance_graph(request):
    str_from_date = request.POST.get("from_date")
    str_to_date = request.POST.get("to_date")


    if str_from_date != ""  and str_to_date != "":
        from_date=dt.strptime(str_from_date,"%Y-%m-%d %H:%M:%S")
        to_date=dt.strptime(str_to_date,"%Y-%m-%d %H:%M:%S")
    else:
        nok_obj=Soft_AT_NOKIA_Rejected_Table.objects.all()
        sam_obj=Soft_AT_SAMSUNG_Rejected_Table.objects.all()
        hua_obj=Soft_AT_HUAWEI_Rejected_Table.objects.all()
        eri_obj = Soft_AT_ERI_Rejected_Table.objects.all()
        zte_obj = Soft_AT_ZTE_Rejected_Table.objects.all()
        from_date,to_date= get_min_max_date_time(nok_obj, sam_obj, hua_obj, eri_obj, zte_obj)


    spoc_mails = Soft_AT_NOKIA_Rejected_Table.objects.filter(Date_Time__range = (from_date,to_date))