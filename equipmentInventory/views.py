from rest_framework.decorators import api_view
from rest_framework.response import Response
from equipmentInventory.models import *
from equipmentInventory.serializers import *

import pandas as pd
import os
# from rest_framework.views import APIView

@ api_view(["POST"])
def equipment_inventory_upload(request):
    
    Equipment_upload_status.objects.all().delete()
    Eqi_inv = request.FILES["equi_file"] if 'equi_file' in request.FILES else None
    if Eqi_inv:
            df=pd.read_excel(Eqi_inv)
            df_header_list= df.columns.tolist()
            print("Header Name-------------------",df_header_list)
            required_header_list=["SR NO","OEM","Hardware Type","Equipment description(BBU & RRU NAME AS PER C Column SELECTION )",
                                "Supported Cards","Technology Supported","Techninal Description","Capacity","MAX POWER",
                                "Remarks"]
            for header_name in required_header_list:
                if header_name not in df_header_list:
                     message= "Did not get " + header_name + " Column in the uploaded Report"
                     return Response({"status":False,"message":message})

            for i, d in df.iterrows():         
                    try:
                        # obj=Equipment.objects.update_or_create(
                        #                                 defaults={"OEM":str(d["OEM"]),
                        #                                 "Hardware_Type":str(d["Hardware Type"]),
                        #                                 "Equipment_description":str(d["Equipment description(BBU & RRU NAME AS PER C Column SELECTION )"]),
                        #                                 "Supported_Cards":str(d["Supported Cards"]),
                        #                                 "Technology_Supported":str(d["Technology Supported"]),
                        #                                 "Techninal_Description":str(d["Techninal Description"]),  
                        #                                 "Capacity":str(d["Capacity"]),
                        #                                 "MAX_POWER":str(d["MAX POWER"]),
                        #                                 "Remarks":str(d["Remarks"])}
                        #                                 )


                        obj=Equipment.objects.create(
                                                        OEM=str(d["OEM"]),
                                                        Hardware_Type=str(d["Hardware Type"]),
                                                        Equipment_description=str(d["Equipment description(BBU & RRU NAME AS PER C Column SELECTION )"]),
                                                        Supported_Cards=str(d["Supported Cards"]),
                                                        Technology_Supported=str(d["Technology Supported"]),
                                                        Techninal_Description=str(d["Techninal Description"]),  
                                                        Capacity=str(d["Capacity"]),
                                                        MAX_POWER=str(d["MAX POWER"]),
                                                        Remarks=str(d["Remarks"])
                                                    )
                        
                    except Exception as e:
                            print(e)
                            error=str(e)
                            # Equipment_upload_status.objects.create(update_status="Not Uploaded",Remark=error)
                            # continue 

                            return Response({
                                'status':False,
                                'message':str(error),
                            })

            objs=Equipment_upload_status.objects.all()
            serializers=ser_equipment_upload_status(objs,many=True)
                 


            return Response({"status": True,"message":"Report uploaded Successfully .","status_obj":serializers.data})
    else:
         return Response({"status": False,"message":"No report file Sent"})
    
    
@ api_view(["GET"])
def equpment_inventory_data(request):
    try:
        print("Current_User---------------",request.user)
        objs=Equipment.objects.all()

        ser=ser_equipment_table(objs,many=True)
        return Response({"status":True,"data":ser.data,})
    except Equipment.DoesNotExist:
         return Response(
            {
                'status':False,
                'message':"No file expected",
            }
         )
         





@api_view(["POST"])
def delete_equipment_inventry(request,id):
    try:
        
        item = Equipment.objects.get(pk = id)
        item.delete()
        total_number_objects = len(Equipment.objects.all())
        print("Instance deleted successfully.")
        
        return Response({
            'status':True,
            'message':"data deleted successfully",
            'total number of objects':total_number_objects,
        })
    except Equipment.DoesNotExist:
            print("Instance with the specified ID does not exist.")
            return  Response(
                {
                    'status':False,
                    'message':"Instance with the specified ID does not exist"
                }
            )
    

@api_view(["PATCH","POST"])
def update_equipment_inventry(request, id):
    try:
        item = Equipment.objects.get(pk=id)
    except Equipment.DoesNotExist:
        return Response({"status": False, "message": "Equipment not found.",},)

    data = ser_equipment_table(instance=item, data=request.data, partial=True)

    if data.is_valid():
        data.save()
        return Response({
            'status': True,
            'message': "Updated successfully.",
            "data": data.data,
        })
    else:
        return Response({
            'status': False,
            'message': "Validation error.",
            "errors": data.errors, 
        })


@api_view(["POST"])
def create_equipment_inventry(request):
    try:
        item = ser_equipment_table(data = request.data)
        if Equipment.objects.filter(**request.data).exists():
            raise serializers.ValidationError('This data already exists')
    
        if item.is_valid():
            item.save()
            return Response({
                'status':True,
                'data':item.data,
            })
        else:
            return Response({
                'status':False,
                "error": item.errors,
            })
    except serializers.ValidationError as e:
        return Response(
            {
                'status':False,
                'error':str(e)
            }
        )
    




