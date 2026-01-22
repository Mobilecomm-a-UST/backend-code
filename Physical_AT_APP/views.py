from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from rest_framework.decorators import api_view
from mcom_website.settings import MEDIA_ROOT
from rest_framework.response import Response

from django.core.files.storage import FileSystemStorage
import pandas as pd
import os
from .models import *   
import datetime
# Create your views here.
import json
from .serialzers import *
def circle_list(objs):
    cir=[]
    
    for obj in objs:
        cir.append(obj.CIRCLE)

    cir_set=set(cir)
    cir=list(cir_set)
    return cir



@api_view(["POST"])
def Physical_At_Report_Upload(request):
    Physical_At_upload_status.objects.all().delete()
    Physical_At_Report_file = request.FILES['Physical_At_Report_file'] if 'Physical_At_Report_file' in request.FILES else None
    if Physical_At_Report_file:
        location=MEDIA_ROOT+r'\Physical_AT\temporary_files'
        fs=FileSystemStorage(location=location)
        file=fs.save(Physical_At_Report_file.name,Physical_At_Report_file)
        file_path=fs.path(file)
        df=pd.read_excel(file_path)
        df=pd.read_excel(file_path,sheet_name="ATP")
        print(Physical_At_Report_file)
        upload_date=request.POST.get("upload_date")
        print("upload date is......................",upload_date)


        df_header_list= df.columns.tolist()
        print("Header Name-------------------",df_header_list)
        required_header_list=["CIRCLE","SITE_ID","UNIQUE ID","ENODEB_ID","BAND","Circle Project","BTS_TYPE","OEM_NAME(Nokia/ZTE/Ericsson/Huawei)","MS1","PHYSICAL_AT_Offered_DATE","PHYSICAL_AT_ACCEPTANCE_DATE",'PHYSICAL_AT_Status(Accepted/Rejected/Offered/Pending/Dismantle)',"CURRENT_STATUS_OF_SITE","Total  Allocation",'Project',
                              'Current PHY AT Status','Expected Closer Date','Additional PHY AT Remarks','Ericsson PHY AT Status','Ericsson PHY AT Date','Huawei PHY AT Status','Huawei PHY AT Date','Nokia PHY AT Status','Nokia PHY AT Date','Samsung PHY AT Status','Samsung PHY AT Date','ZTE PHY AT Status','ZTE PHY AT Date','MS1 to PHY AT Ageing','Ageing','Plan Date','Plan Status','Expected Closer Date']
        for header_name in required_header_list:
                if header_name in df_header_list:
                     pass
                else:
                     message= "Did not get " + header_name + " Column in the uploaded Report"
                     return Response({"status":False,"message":message})

        for i, d in df.iterrows():
                    

                    pk=str(d["CIRCLE"])+str(d["SITE_ID"])+str(d["UNIQUE ID"])+str(d["BAND"])+str(d["OEM_NAME(Nokia/ZTE/Ericsson/Huawei)"])+str(upload_date)

                    if pd.isnull(d['Expected Closer Date']):
                          Expected_Closer_Date=None
                    else:
                          Expected_Closer_Date=(d["Expected Closer Date"])

                    if pd.isnull(d['Ericsson PHY AT Date']):
                           Ericsson_PHY_AT_Date=None
                    else:
                           Ericsson_PHY_AT_Date=(d["Ericsson PHY AT Date"])

                    if pd.isnull(d['Huawei PHY AT Date']):
                           Huawei_PHY_AT_Date=None
                    else:
                           Huawei_PHY_AT_Date=(d["Huawei PHY AT Date"])

                    if pd.isnull(d['Nokia PHY AT Date']):
                           Nokia_PHY_AT_Date=None
                    else:
                           Nokia_PHY_AT_Date=(d["Nokia PHY AT Date"])

                    if pd.isnull(d['Samsung PHY AT Date']):
                           Samsung_PHY_AT_Date=None
                    else:
                           Samsung_PHY_AT_Date=(d["Samsung PHY AT Date"])
                    
                    if pd.isnull(d['ZTE PHY AT Date']):
                        ZTE_PHY_AT_Date=None
                    else:
                        ZTE_PHY_AT_Date=(d["ZTE PHY AT Date"])

                    if pd.isnull(d['Plan Date']):
                           Plan_Date=None
                    else:
                           Plan_Date=(d['Plan Date'])
                   


                    if pd.isnull(d['PHYSICAL_AT_Offered_DATE']):
                           PHYSICAL_AT_Offered_DATE=None
                    else:
                           PHYSICAL_AT_Offered_DATE=(d['PHYSICAL_AT_Offered_DATE'])
                     
                    if pd.isnull(d['PHYSICAL_AT_ACCEPTANCE_DATE']):
                           PHYSICAL_AT_ACCEPTANCE_DATE=None
                    else:
                          PHYSICAL_AT_ACCEPTANCE_DATE=(d['PHYSICAL_AT_ACCEPTANCE_DATE'])




                    try:

                        updated_values={  "CIRCLE":str(d["CIRCLE"]),
                                          "SITE_ID":str(d["SITE_ID"]),"UNIQUE_ID":str(d["UNIQUE ID"]),
                                          "ENODEB_ID":str(d["ENODEB_ID"]),
                                          "BAND": str(d["BAND"]),
                                          "Circle_Project":str(d["Circle Project"]),
                                          "BTS_TYPE":str(d["BTS_TYPE"]),
                                          "OEM_NAME_Nokia_ZTE_Ericsson_Huawei":str(d["OEM_NAME(Nokia/ZTE/Ericsson/Huawei)"]),
                                          "MS1":d["MS1"],
                                          "PHYSICAL_AT_Offered_DATE":PHYSICAL_AT_Offered_DATE,
                                          "PHYSICAL_AT_ACCEPTANCE_DATE":PHYSICAL_AT_ACCEPTANCE_DATE,
                                          "PHYSICAL_AT_Status_Accepted_Rejected_Offered_Pending_Dismantle":str(d["PHYSICAL_AT_Status(Accepted/Rejected/Offered/Pending/Dismantle)"]),
                                          "CURRENT_STATUS_OF_SITE":str(d["CURRENT_STATUS_OF_SITE"]),
                                          "Project":str(d["Project"]),
                                          "Current_PHY_AT_Status":str(d["Current PHY AT Status"]),
                                          "Expected_Closer_Date":Expected_Closer_Date,
                                          "Expected_Closer_Status":str(d["Expected Closer Status"]),
                                          "Additional_PHY_AT_Remarks":str(d["Additional PHY AT Remarks"]),
                                          "Ericsson_PHY_AT_Status":str(d["Ericsson PHY AT Status"]),
                                          "Ericsson_PHY_AT_Date":Ericsson_PHY_AT_Date,
                                          "Huawei_PHY_AT_Status":str(d["Huawei PHY AT Status"]),
                                          "Huawei_PHY_AT_Date":Huawei_PHY_AT_Date,
                                          "Nokia_PHY_AT_Status":str(d["Nokia PHY AT Status"]),
                                          "Nokia_PHY_AT_Date":Nokia_PHY_AT_Date,
                                          "Samsung_PHY_AT_Status":str(d["Samsung PHY AT Status"]),
                                          "Samsung_PHY_AT_Date":Samsung_PHY_AT_Date,
                                          "ZTE_PHY_AT_Status":str(d["ZTE PHY AT Status"]),
                                          "ZTE_PHY_AT_Date":ZTE_PHY_AT_Date,
                                          "MS1_to_PHY_AT_Ageing":str(d["MS1 to PHY AT Ageing"]),
                                          "Ageing":str(d["Ageing"]),
                                          "Plan_Date":Plan_Date,
                                          "Plan_Status":str(d["Plan Status"]),
                                          "Upload_date":upload_date}
                    
                             

                            
                        obj=Physical_AT_Table.objects.update_or_create(id=pk,Upload_date=upload_date,
                                                    defaults=updated_values,
                                                                )
           
                    except Exception as e:
                       print(e)
                       error=str(e)
                       Physical_At_upload_status.objects.create(id=pk,Site_id=d["SITE_ID"],update_status="Not Uploaded",Remark=error)
                       continue 
                
        objs=Physical_At_upload_status.objects.all()
        serializers=ser_Physical_At_upload_status(objs,many=True) 
        
        return Response({"status": True,"message":"Report uploaded Successfully .","status_obj":serializers.data})
    else:
                    
      

     return Response({"status": True,"message":"Report uploaded Successfully ."})
    



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
        df.loc['Grand Total'] = df.sum()
        # add a sum column at the right end of the dataframe
        df['Grand Total'] = df["Ageing_0_15"] + df["Ageing_16_30"] +df["Ageing_31_60"] + df["Ageing_61_90"] + df["ageing_GT90"] +df["close"]
        json_data = df.to_json(orient='index') # here json_data  converts the dataframe to a string json
        json_data=json.loads(json_data) # json.loads - Which converts the string form of json data to a dictionary in python.
        print(df)
        return(json_data)
        
     

@api_view(["GET","POST"])
def Physical_Circlewise_Dashboard(request):
   
       objs=Physical_AT_Table.objects.all()
       circles= circle_list(objs) 
       print("Circle_list: ",circles)
       data={}

       ageing_circleWise={}   
       for circle in circles:
              
         
              obj=Physical_AT_Table.objects.filter(CIRCLE=circle)


              ageing_0_15=obj.filter(Ageing = "0-15").count()
              ageing_16_30=obj.filter(Ageing = "16-30").count()
              ageing_31_60=obj.filter(Ageing = "31-60").count()
              ageing_61_90=obj.filter(Ageing = "61-90").count()
              ageing_GT90=obj.filter(Ageing = "GT90").count()
              close=obj.filter(Ageing="Close") .count() 

              ageing_circleWise[circle]={"ageing_0_15":ageing_0_15,
                                          "ageing_16_30":ageing_16_30,
                                          "ageing_31_60":ageing_31_60,
                                          "ageing_61_90":ageing_61_90,
                                          "ageing_GT90":ageing_GT90,
                                          "Close":close, 
                                     }
       ageing_circleWise_data= df_raw_column_total(ageing_circleWise)
       print(ageing_circleWise_data)
       Latest_date =Physical_AT_Table.objects.latest('Upload_date').Upload_date

       objs_all=Physical_AT_Table.objects.all()

       ############################## code for expected closure date #########################
       circles= circle_list(objs_all) 
       print("Circle_list: ",circles)

       querySet_unique_date=objs_all.order_by().values_list('Expected_Closer_Date',flat=True).distinct()
       list_of_unique_date=list(querySet_unique_date)
       list_of_unique_date.remove(None)

       print("list_converted.....................",querySet_unique_date)
       print("list of unique dates..............................",list_of_unique_date)

       ECD_data={}
       for circle in circles: 
              cir_obj=objs_all.filter(CIRCLE=circle)
              print("cir_obj.............................",cir_obj)
              date_wise_data={}

              for date in list_of_unique_date:
                     print("in report...............",date)
                     date_str=str(date)
                     date_str= "_" + date_str.replace("-", "_" )
                     date_wise_data[date_str]=cir_obj.filter(Expected_Closer_Date = date).count()                
              ECD_data[circle]=date_wise_data
       return Response({"status":True, 
                            "Data":data,
                            "ageing_circleWise":ageing_circleWise_data,
                            "Latest_date":Latest_date,
                            "ECD_data":ECD_data
                            })



      


























