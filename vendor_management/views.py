from django.shortcuts import render
from rest_framework.decorators import api_view,parser_classes
from .models import *
from mcom_website.settings import MEDIA_ROOT
from django.core.files.storage import FileSystemStorage
import pandas as pd
import os
from rest_framework.response import Response
from .serializer import *

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes,permission_classes

from django.contrib.auth.decorators import permission_required
from accounts.models import *

##################################### Phase 1 circle team ##########################################
 
# @api_view(["POST"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# # @permission_required('vendor_management.change_progress_report')
# def circle_progress_report_upload(request):
#     upload_status.objects.all().delete()  # to delete all previous instances 
#     alloted_circle="###"
#     user=request.user
#     # print("circle team or not : ",user.groups.filter(name="Circle_level")).exists()
#     print('Circle_level' in user.groups.values_list('name', flat=True))
#     print(user.groups.values_list('name', flat=True))
#     if user.has_perm("vendor_management.add_progress_report"): # to check if the user  has permission to make changes in the progress_report table.
#             if not request.user.is_superuser:
                   
#                     try:
#                         alloted_circle= circle_model.objects.get(user=user).circle
#                         print("alloted circle:",alloted_circle)
#                     except:
#                         return Response({"status":False,"message":"Not authorised to upload file of any Circle"})
#             print("Superuser name:",request.user)
#             circle = request.POST.get("circle")
#             print("Circle:",circle)
#             if alloted_circle == circle or request.user.is_superuser:
#                     Progress_report_file = request.FILES["Progress_report_file"] if 'Progress_report_file' in request.FILES else None
#                     if Progress_report_file:
#                             location=MEDIA_ROOT + r"\vendor management\temporary_files"
#                             fs = FileSystemStorage(location=location)
#                             file = fs.save(Progress_report_file.name, Progress_report_file)
#                             # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
#                             filepath = fs.path(file)
#                             print("file_path:-",filepath)
#                             df=pd.read_excel(filepath, header=1) # should do something if a csv file is coming from the frontend and the csv file should be deleted from the temp files
#                             os.remove(path=filepath)
#                             print(filepath,"deleted...............")
#                             print(df)
#                             # return Response({"status":True})
                            
                            
#                             if not(df.empty):
#                                 for i,d in df.iterrows():
                                
                                            
#                                             try:
#                                                 if not pd.isnull(d["MDP Month"]) and  isinstance(d["Alotment date To Vendor"], datetime.datetime):
#                                                     MDP_Month=d["MDP Month"]
#                                                 else:
#                                                     status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Alotment date To Vendor' is missing or date formate is not correct" ) 
#                                                     continue
                                                
                                                
#                                                 if not pd.isnull(d["Alotment date To Vendor"]) and  isinstance(d["Alotment date To Vendor"], datetime.datetime):
#                                                     Alotment_date_To_Vendor=d["Alotment date To Vendor"]
#                                                 else:
#                                                     status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Alotment date To Vendor' is missing or date formate is not correct" ) 
#                                                     continue

#                                                 if not pd.isnull(d["Activity Date"]) and  isinstance(d["Activity Date"], datetime.datetime):
#                                                     Activity_Date=d["Activity Date"]
#                                                 else:
#                                                     status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Activity Date' is missing or date formate is not correct" ) 
#                                                     continue
                                                
#                                                 if not pd.isnull(d["Material Reco Date"]) and  isinstance(d["Material Reco Date"], datetime.datetime):
#                                                     Material_Reco_Date=d["Material Reco Date"]
#                                                 else:
#                                                     status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Material Reco Date' is missing or date formate is not correct" ) 
#                                                     continue

#                                                 if not pd.isnull(d["Activity AT Date"]) and  isinstance(d["Activity AT Date"], datetime.datetime):
#                                                     Activity_AT_Date=d["Activity AT Date"]
#                                                 else:
#                                                     status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Activity AT Date' is missing or date formate is not correct" ) 
#                                                     continue
                                                
#                                                 if not pd.isnull(d["Circle"]) and alloted_circle.upper() == str(d["Circle"]).upper():
#                                                      Circle = d["Circle"]
#                                                 else:
#                                                     status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Circle name' is missing or circle is incorrect" ) 
#                                                     continue

#                                                 if not pd.isnull(d["Site ID"]):
#                                                      Site_ID = d["Site ID"]
#                                                 else:
#                                                     status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Site ID' is missing" ) 
#                                                     continue
                                                
#                                                 if not pd.isnull(d["Site Name"]):
#                                                     Site_Name = d["Site Name"]
#                                                 else:
#                                                     status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Site Name' is missing" ) 
#                                                     continue

#                                                 if not pd.isnull(d["Activity Name"]):
#                                                      Activity_Name = d["Activity Name"]
#                                                 else:
#                                                     status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Activity Name' is missing" ) 
#                                                     continue
#                                                 if not pd.isnull(d["Activity Discription"]):
#                                                      Activity_Discription = d["Activity Discription"]
#                                                 else:
#                                                     status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Activity Discription' is missing" ) 
#                                                     continue
#                                                 if not pd.isnull(d["Line Item"]):
#                                                      Line_Item = d["Line Item"]
#                                                 else:
#                                                     status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Line Item' is missing" ) 
#                                                     continue
#                                                 if not pd.isnull(d["Vendor Name"]):
#                                                       Vendor_Name =  d["Vendor Name"]
#                                                 else:
#                                                     status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Vendor Name' is missing" ) 
#                                                     continue
#                                                 if not pd.isnull(d["Vendor Code"]):
#                                                       Vendor_Code = d["Vendor Code"]
#                                                 else:
#                                                     status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Vendor Code' is missing" ) 
#                                                     continue
                                                
#                                                 if not pd.isnull(d["Activity Completion Status"]):
#                                                       Activity_Completion_Status = d["Activity Completion Status"]
#                                                 else:
#                                                     status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Activity Completion Status' is missing" ) 
#                                                     continue
                                               
#                                                 if not pd.isnull(d["Material Reco Status"]):
#                                                      Material_Reco_Status = d["Material Reco Status"]
#                                                 else:
#                                                     status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Material Reco Status' is missing" ) 
#                                                     continue
#                                                 if not pd.isnull(d["Activity AT Status"]):
#                                                      Activity_AT_Status = d["Activity AT Status"]
#                                                 else:
#                                                     status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Activity AT Status' is missing" ) 
#                                                     continue

#                                                 obj,created=Progress_report.objects.update_or_create(Unique_Site_Id_As_per_central_DPR=d["Unique Site Id As per central DPR"], defaults={"Alotment_date_To_Vendor":Alotment_date_To_Vendor,
#                                                                                                                                                                                          "Activity_Date":Activity_Date,
#                                                                                                                                                                                          "Material_Reco_Date":Material_Reco_Date,
#                                                                                                                                                                                          "Activity_AT_Date":Activity_AT_Date,
#                                                                                                                                                                                          "MDP_Month":MDP_Month,
#                                                                                                                                                                                          "Circle":Circle,
#                                                                                                                                                                                          "Site_ID":Site_ID,
#                                                                                                                                                                                          "Site_Name":Site_Name,
#                                                                                                                                                                                          "Activity_Name":Activity_Name,
#                                                                                                                                                                                          "Activity_Discription":Activity_Discription,
#                                                                                                                                                                                          "Line_Item":Line_Item,
#                                                                                                                                                                                          "Vendor_Name":Vendor_Name,
#                                                                                                                                                                                          "Vendor_Code":Vendor_Code,
#                                                                                                                                                                                          "Activity_Completion_Status":Activity_Completion_Status,
#                                                                                                                                                                                          "Material_Reco_Status":Material_Reco_Status,
#                                                                                                                                                                                          "Activity_AT_Status":Activity_AT_Status,
#                                                                                                                                                                                          "Vendor_PO_Requestor":str(request.user),})
                                                
                                                 
                                                            
#                                             except Exception as e:
#                                                 print(e)
#                                                 return Response({"status":False,"message":str(e)}) 
#                                 else:
#                                     ob=upload_status.objects.all()
#                                     serializer=ser_upload_status(ob,many=True)
#                                     return Response({"status":True,"message":"Report uploaded succesfully","status_obj":serializer.data})
#                             else:
#                                 context={"status":False,"message":"DPR Report is empty"}
#                                 return Response(context)                      
#             else:
#                 message="You are not authorised to upload data of " + str(circle) +" circle"
#                 return Response({"status":False,"message":message})                       
#     else:
#           return Response({"status":False,"message":"Not authorised to upload files"})
    
# @api_view(["GET"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def circle_team_report_view(request):
#             user=request.user
#             print(user)
#             if user.has_perm("vendor_management.view_progress_report"):
#                 if not user.is_superuser:
#                     try:
#                         alloted_circle= circle_model.objects.get(user=user).circle
#                     except:
#                            return Response({"status":False,"message":"Not authorised to view report of any Circle"}) 
#                     objs=Progress_report.objects.filter(Circle = alloted_circle)
#                 else:
#                            objs=Progress_report.objects.all()
#                 ser=ser_progress_report(objs,many=True)
                    
#                 context={"status":True,"data":ser.data}
                
#                 return Response(context)
#             else:
#                  return Response({"status":False,"message":"Not authorised to View Report"})
# ##################################### Phase 2 Ravi Sir ################################################
         
# @api_view(["GET"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def po_approval_view(request):
             
#             user=request.user
#             if "po_approvers" in user.groups.values_list('name', flat=True):
#                 print(user)
#                 if user.has_perm("vendor_management.view_progress_report"):
            
                        
#                         objs=Progress_report.objects.all()
#                         ser=ser_progress_report(objs,many=True)
                        
#                         context={"data":ser.data}
                    
#                         return Response(context)
#                 else:
#                     return Response({"status":False,"message":"Not authorised to View Report"})
                
#             else:
#                     return Response({"status":False,"message":"Not authorised to View Report..."})
            

# @api_view(["POST"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def po_approval_upload(request):

#     user=request.user
#     if user.has_perm("vendor_management.change_progress_report"):
#                     vendor_po_approver_upload_status.objects.all().delete()
        
           
#                     circle = request.POST.get("circle")
#                     Progress_report_file = request.FILES["Progress_report_file"] if 'Progress_report_file' in request.FILES else None
#                     if Progress_report_file:
#                             location=MEDIA_ROOT + r"\vendor management\temporary_files"
#                             fs = FileSystemStorage(location=location)
#                             file = fs.save(Progress_report_file.name, Progress_report_file)
#                             # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
#                             filepath = fs.path(file)
#                             print("file_path:-",filepath)
#                             df=pd.read_excel(filepath) # should do something if a csv file is coming from the frontend and the csv file should be deleted from the temp files
#                             os.remove(path=filepath)
#                             print(filepath,"deleted...............")
#                             print(df)
#                             # return Response({"status":True})
                            
                            
#                             if not(df.empty):
#                                 for i,d in df.iterrows():
                                
                                            
#                                             try:
                                               
#                                                 # obj=Progress_report.objects.get(Unique_Site_Id_As_per_central_DPR=d["Unique Site Id As per central DPR"],Circle=circle)
#                                                 obj=Progress_report.objects.get(Unique_Site_Id_As_per_central_DPR=d["Unique Site Id As per central DPR"])
                                                
#                                                 if not pd.isnull(d["Vendor PO (Eligible)"]):
#                                                       obj.Vendor_PO_Eligible=d["Vendor PO (Eligible)"]
#                                                 else:
#                                                     vendor_po_approver_upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Vendor PO (Eligible)' is missing" ) 
#                                                     continue
                                                
#                                                 obj.Vendor_PO_Approver= str(request.user)
#                                                 obj.save()
                                                            
#                                             except Exception as e:
#                                                 print(e)
#                                                 return Response({"status":False,"message":str(e)}) 
#                                 else:
#                                     ob=vendor_po_approver_upload_status.objects.all()
#                                     serializer=ser_vendor_po_approver_upload_status(ob,many=True)
#                                     return Response({"status":True,"message":"Report uploaded succesfully","status_obj":serializer.data})
#                             else:
#                                 context={"status":False,"message":"DPR Report is empty"}
#                                 return Response(context)                      
                                 
#     else:
#           return Response({"status":False,"message":"Not authorised to upload files"})



# ##################################### 3rd phase Hardesh Sir ##############################################
# @api_view(["GET"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def allocate_po_view(request):
            

#             user=request.user
#             print(user)
#             if user.has_perm("vendor_management.view_progress_report"):
           
                    
#                     objs=Progress_report.objects.filter(Vendor_PO_Eligible = "Approved" )
#                     ser=ser_progress_report(objs,many=True)
                    
#                     context={"status":True, "data":ser.data}
                
#                     return Response(context)
#             else:
#                  return Response({"status":False,"message":"Not authorised to View Report"})
            


# @api_view(["POST"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def allocate_po_upload(request):



#     user=request.user
#     if user.has_perm("vendor_management.change_progress_report"):
#                     vendor_po_No_upload_status.objects.all().delete()
        
           
#                     circle = request.POST.get("circle")
#                     Progress_report_file = request.FILES["Progress_report_file"] if 'Progress_report_file' in request.FILES else None
#                     if Progress_report_file:
#                             location=MEDIA_ROOT + r"\vendor management\temporary_files"
#                             fs = FileSystemStorage(location=location)
#                             file = fs.save(Progress_report_file.name, Progress_report_file)
#                             # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
#                             filepath = fs.path(file)
#                             print("file_path:-",filepath)
#                             df=pd.read_excel(filepath) # should do something if a csv file is coming from the frontend and the csv file should be deleted from the temp files
#                             os.remove(path=filepath)
#                             print(filepath,"deleted...............")
#                             print(df)
#                             # return Response({"status":True})
                            
                            
#                             if not(df.empty):
#                                 for i,d in df.iterrows():
                                
                                            
#                                             try:
                                               
#                                                 # obj=Progress_report.objects.get(Unique_Site_Id_As_per_central_DPR=d["Unique Site Id As per central DPR"],Circle=circle)
#                                                 obj=Progress_report.objects.get(Unique_Site_Id_As_per_central_DPR=d["Unique Site Id As per central DPR"])
                                                
#                                                 if not pd.isnull(d["Vendor PO No."]):
#                                                       obj.Vendor_PO_No=d["Vendor PO No."]
#                                                 else:
#                                                     vendor_po_No_upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Vendor PO No.' is missing" ) 
#                                                     continue
#                                                 if not pd.isnull(d["Vendor PO Date"]) and  isinstance(d["Vendor PO Date"], datetime.datetime):
#                                                       obj.Vendor_PO_Date=d["Vendor PO Date"]
#                                                 else:
#                                                     vendor_po_No_upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Vendor PO Date.' is missing or 'Vendor PO Date' format is incorrect"  ) 
#                                                     continue
                                                
                                            
#                                                 obj.save()
                                                            
#                                             except Exception as e:
#                                                 print(e)
#                                                 return Response({"status":False,"message":str(e)}) 
#                                 else:
#                                     ob=vendor_po_No_upload_status.objects.all()
#                                     serializer=ser_vendor_po_No_upload_status(ob,many=True)
#                                     return Response({"status":True,"message":"Report uploaded succesfully","status_obj":serializer.data})
#                             else:
#                                 context={"status":False,"message":"DPR Report is empty"}
#                                 return Response(context)                      
#                     else:
#                           return Response({"status":False,"message":"No report file is selected"})
                                       
#     else:
#           return Response({"status":False,"message":"Not authorised to upload files"})
    








##################################### Phase 1 circle team ##########################################
 
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
# @permission_required('vendor_management.change_progress_report')
def circle_progress_report_upload(request):
    upload_status.objects.all().delete()  # to delete all previous instances 
    alloted_circle="###"
    user=request.user

    print('Circle_level' in user.groups.values_list('name', flat=True))
    print(user.groups.values_list('name', flat=True))
    if 'Circle_level' in user.groups.values_list('name', flat=True) : # to check if the user  has permission to make changes in the progress_report table
            
                   
            try:
                alloted_circle= circle_model.objects.get(user=user).circle
                print("alloted circle:",alloted_circle)
            except:
                return Response({"status":False,"message":"Not authorised to upload file of any Circle"})
            print("Superuser name:",request.user)
            circle = request.POST.get("circle")
            print("Circle:",circle)
            if alloted_circle == circle or request.user.is_superuser:
                    Progress_report_file = request.FILES["Progress_report_file"] if 'Progress_report_file' in request.FILES else None
                    if Progress_report_file:
                            location=MEDIA_ROOT + r"\vendor management\temporary_files"
                            fs = FileSystemStorage(location=location)
                            file = fs.save(Progress_report_file.name, Progress_report_file)
                            # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
                            filepath = fs.path(file)
                            print("file_path:-",filepath)
                            df=pd.read_excel(filepath, header=1) # should do something if a csv file is coming from the frontend and the csv file should be deleted from the temp files
                            os.remove(path=filepath)
                            print(filepath,"deleted...............")
                            print(df)
                            # return Response({"status":True})
                            
                            
                            if not(df.empty):
                                for i,d in df.iterrows():
                                
                                            
                                            try:
                                                if not pd.isnull(d["Unique Site Id As per central DPR"]):
                                                    if not pd.isnull(d["MDP Month"]) and  isinstance(d["Alotment date To Vendor"], datetime.datetime):
                                                        MDP_Month=d["MDP Month"]
                                                    else:
                                                        status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Alotment date To Vendor' is missing or date formate is not correct" ) 
                                                        continue
                                                    
                                                    
                                                    if not pd.isnull(d["Alotment date To Vendor"]) and  isinstance(d["Alotment date To Vendor"], datetime.datetime):
                                                        Alotment_date_To_Vendor=d["Alotment date To Vendor"]
                                                    else:
                                                        status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Alotment date To Vendor' is missing or date formate is not correct" ) 
                                                        continue

                                                    if not pd.isnull(d["Activity Date"]) and  isinstance(d["Activity Date"], datetime.datetime):
                                                        Activity_Date=d["Activity Date"]
                                                    else:
                                                        status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Activity Date' is missing or date formate is not correct" ) 
                                                        continue
                                                    
                                                    if not pd.isnull(d["Material Reco Date"]) and  isinstance(d["Material Reco Date"], datetime.datetime):
                                                        Material_Reco_Date=d["Material Reco Date"]
                                                    else:
                                                        status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Material Reco Date' is missing or date formate is not correct" ) 
                                                        continue

                                                    if not pd.isnull(d["Activity AT Date"]) and  isinstance(d["Activity AT Date"], datetime.datetime):
                                                        Activity_AT_Date=d["Activity AT Date"]
                                                    else:
                                                        status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Activity AT Date' is missing or date formate is not correct" ) 
                                                        continue
                                                    
                                                    if not pd.isnull(d["Circle"]) and alloted_circle.upper() == str(d["Circle"]).upper():
                                                        Circle = d["Circle"]
                                                    else:
                                                        status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Circle name' is missing or circle is incorrect" ) 
                                                        continue

                                                    if not pd.isnull(d["Site ID"]):
                                                        Site_ID = d["Site ID"]
                                                    else:
                                                        status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Site ID' is missing" ) 
                                                        continue
                                                    
                                                    if not pd.isnull(d["Site Name"]):
                                                        Site_Name = d["Site Name"]
                                                    else:
                                                        status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Site Name' is missing" ) 
                                                        continue

                                                    if not pd.isnull(d["Activity Name"]):
                                                        Activity_Name = d["Activity Name"]
                                                    else:
                                                        status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Activity Name' is missing" ) 
                                                        continue
                                                    if not pd.isnull(d["Activity Discription"]):
                                                        Activity_Discription = d["Activity Discription"]
                                                    else:
                                                        status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Activity Discription' is missing" ) 
                                                        continue
                                                    if not pd.isnull(d["Line Item"]):
                                                        Line_Item = d["Line Item"]
                                                    else:
                                                        status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Line Item' is missing" ) 
                                                        continue
                                                    if not pd.isnull(d["Vendor Name"]):
                                                        Vendor_Name =  d["Vendor Name"]
                                                    else:
                                                        status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Vendor Name' is missing" ) 
                                                        continue
                                                    if not pd.isnull(d["Vendor Code"]):
                                                        Vendor_Code = d["Vendor Code"]
                                                    else:
                                                        status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Vendor Code' is missing" ) 
                                                        continue
                                                    
                                                    if not pd.isnull(d["Activity Completion Status"]):
                                                        Activity_Completion_Status = d["Activity Completion Status"]
                                                    else:
                                                        status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Activity Completion Status' is missing" ) 
                                                        continue
                                                
                                                    if not pd.isnull(d["Material Reco Status"]):
                                                        Material_Reco_Status = d["Material Reco Status"]
                                                    else:
                                                        status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Material Reco Status' is missing" ) 
                                                        continue
                                                    if not pd.isnull(d["Activity AT Status"]):
                                                        Activity_AT_Status = d["Activity AT Status"]
                                                    else:
                                                        status_obj=upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Activity AT Status' is missing" ) 
                                                        continue

                                                    obj,created=Progress_report.objects.update_or_create(Unique_Site_Id_As_per_central_DPR=d["Unique Site Id As per central DPR"], defaults={"Alotment_date_To_Vendor":Alotment_date_To_Vendor,
                                                                                                                                                                                            "Activity_Date":Activity_Date,
                                                                                                                                                                                            "Material_Reco_Date":Material_Reco_Date,
                                                                                                                                                                                            "Activity_AT_Date":Activity_AT_Date,
                                                                                                                                                                                            "MDP_Month":MDP_Month,
                                                                                                                                                                                            "Circle":Circle,
                                                                                                                                                                                            "Site_ID":Site_ID,
                                                                                                                                                                                            "Site_Name":Site_Name,
                                                                                                                                                                                            "Activity_Name":Activity_Name,
                                                                                                                                                                                            "Activity_Discription":Activity_Discription,
                                                                                                                                                                                            "Line_Item":Line_Item,
                                                                                                                                                                                            "Vendor_Name":Vendor_Name,
                                                                                                                                                                                            "Vendor_Code":Vendor_Code,
                                                                                                                                                                                            "Activity_Completion_Status":Activity_Completion_Status,
                                                                                                                                                                                            "Material_Reco_Status":Material_Reco_Status,
                                                                                                                                                                                            "Activity_AT_Status":Activity_AT_Status,
                                                                                                                                                                                            "Vendor_PO_Requestor":str(request.user),})
                                                else:
                                                    continue                   
                                            except Exception as e:
                                                print(e)
                                                error=str(e) + " column name may be wrong in the the report file "
                                                return Response({"status":False,"message":str(e)}) 
                                else:
                                    ob=upload_status.objects.all()
                                    serializer=ser_upload_status(ob,many=True)
                                    return Response({"status":True,"message":"Report uploaded succesfully","status_obj":serializer.data})
                            else:
                                context={"status":False,"message":"DPR Report is empty"}
                                return Response(context)                      
            else:
                message="You are not authorised to upload data of " + str(circle) +" circle"
                return Response({"status":False,"message":message})                       
    else:
          return Response({"status":False,"message":"Not authorised to upload files"})
    
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def circle_team_report_view(request):
            user=request.user
            print(user)
            if 'Circle_level' in user.groups.values_list('name', flat=True):
                
                try:
                        alloted_circle= circle_model.objects.get(user=user).circle
                except:
                           return Response({"status":False,"message":"Not authorised to view report of any Circle"}) 
                objs=Progress_report.objects.filter(Circle = alloted_circle)
               
                ser=ser_progress_report(objs,many=True)
                    
                context={"status":True,"data":ser.data}
                
                return Response(context)
            else:
                 return Response({"status":False,"message":"Not authorised to View Report"})
##################################### Phase 2 Ravi Sir ################################################
         
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def po_approval_view(request):
             
            user=request.user
            print(user)
            if "po_approvers" in user.groups.values_list('name', flat=True):
               
               
            
                        
                        objs=Progress_report.objects.all()
                        ser=ser_progress_report(objs,many=True)
                        
                        context={"data":ser.data}
                    
                        return Response(context)
            else:
                    return Response({"status":False,"message":"Not authorised to View Report"})
                
        
            

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def po_approval_upload(request):

    user=request.user
    if "po_approvers" in user.groups.values_list('name', flat=True):
                    print(user)
                    vendor_po_approver_upload_status.objects.all().delete()
        
           
                    circle = request.POST.get("circle")
                    print("Circle: ",circle)
                    circle_list = [x.upper() for x in circle.split(",")]
                    print("Circle List:",circle_list)
                    Progress_report_file = request.FILES["Progress_report_file"] if 'Progress_report_file' in request.FILES else None
                    if Progress_report_file:
                            location=MEDIA_ROOT + r"\vendor management\temporary_files"
                            fs = FileSystemStorage(location=location)
                            file = fs.save(Progress_report_file.name, Progress_report_file)
                            # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
                            filepath = fs.path(file)
                            print("file_path:-",filepath)
                            df=pd.read_excel(filepath) # should do something if a csv file is coming from the frontend and the csv file should be deleted from the temp files
                            os.remove(path=filepath)
                            print(filepath,"deleted...............")
                            print(df)
                            # return Response({"status":True})
                            
                            
                            if not(df.empty):
                                for i,d in df.iterrows():                                                                           
                                            try:
                                               
                                                # obj=Progress_report.objects.get(Unique_Site_Id_As_per_central_DPR=d["Unique Site Id As per central DPR"],Circle=circle)
                                                obj=Progress_report.objects.get(Unique_Site_Id_As_per_central_DPR=d["Unique Site Id As per central DPR"])
                                                if str(d["Circle"]).upper() in circle_list or "ALL" in circle_list:
                                                      
                                                      
                                                    if not pd.isnull(d["Vendor PO (Eligible)"]):
                                                        obj.Vendor_PO_Eligible=d["Vendor PO (Eligible)"]
                                                    else:
                                                        vendor_po_approver_upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Vendor PO (Eligible)' is missing" ) 
                                                        continue
                                                    
                                                    obj.Vendor_PO_Approver= str(request.user)
                                                    obj.save()
                                                else:
                                                      vendor_po_approver_upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Circle' did not match" )   
                                            except Exception as e:
                                                print(e)
                                                return Response({"status":False,"message":str(e)}) 
                                else:
                                    ob=vendor_po_approver_upload_status.objects.all()
                                    serializer=ser_vendor_po_approver_upload_status(ob,many=True)
                                    return Response({"status":True,"message":"Report uploaded succesfully","status_obj":serializer.data})
                            else:
                                context={"status":False,"message":"DPR Report is empty"}
                                return Response(context)                      
                    else:
                          return Response({"status":False,"message":"please upload file upload files"})
                                      
    else:
          return Response({"status":False,"message":"Not authorised to upload files"})



##################################### 3rd phase Hardesh Sir ##############################################
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def allocate_po_view(request):
            

            user=request.user
            print(user)
            if  "po_allocators" in user.groups.values_list('name', flat=True):
           
                    
                    objs=Progress_report.objects.filter(Vendor_PO_Eligible = "Approved" )
                    ser=ser_progress_report(objs,many=True)
                    
                    context={"status":True, "data":ser.data}
                
                    return Response(context)
            else:
                 return Response({"status":False,"message":"Not authorised to View Report"})
            


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def allocate_po_upload(request):



    user=request.user
    if "po_allocators" in user.groups.values_list('name', flat=True):
                    vendor_po_No_upload_status.objects.all().delete()
        
           
                    circle = request.POST.get("circle")
                    
                    print("Circle: ",circle)
                    circle_list = [x.upper() for x in circle.split(",")]
                    print("Circle List:",circle_list)
                    Progress_report_file = request.FILES["Progress_report_file"] if 'Progress_report_file' in request.FILES else None
                    if Progress_report_file:
                            location=MEDIA_ROOT + r"\vendor management\temporary_files"
                            fs = FileSystemStorage(location=location)
                            file = fs.save(Progress_report_file.name, Progress_report_file)
                            # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
                            filepath = fs.path(file)
                            print("file_path:-",filepath)
                            df=pd.read_excel(filepath) # should do something if a csv file is coming from the frontend and the csv file should be deleted from the temp files
                            os.remove(path=filepath)
                            print(filepath,"deleted...............")
                            print(df)
                            # return Response({"status":True})
                            
                            
                            if not(df.empty):
                                for i,d in df.iterrows():
                                
                                            
                                            try:
                                               
                                                # obj=Progress_report.objects.get(Unique_Site_Id_As_per_central_DPR=d["Unique Site Id As per central DPR"],Circle=circle)
                                                obj=Progress_report.objects.get(Unique_Site_Id_As_per_central_DPR=d["Unique Site Id As per central DPR"])
                                                if str(d["Circle"]).upper() in circle_list or "ALL" in circle_list:
                                                    if not pd.isnull(d["Vendor PO No."]):
                                                        obj.Vendor_PO_No=d["Vendor PO No."]
                                                    else:
                                                        vendor_po_No_upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Vendor PO No.' is missing" ) 
                                                        continue
                                                    if not pd.isnull(d["Vendor PO Date"]) and  isinstance(d["Vendor PO Date"], datetime.datetime):
                                                        obj.Vendor_PO_Date=d["Vendor PO Date"]
                                                    else:
                                                        vendor_po_No_upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Vendor PO Date.' is missing or 'Vendor PO Date' format is incorrect"  ) 
                                                        continue
                                                    
                                                
                                                    obj.save()
                                                else: 
                                                    vendor_po_No_upload_status.objects.create(id=d["Unique Site Id As per central DPR"],update_status="NOT UPDATED", Remark="'Circle' did not match" )     
                                                            
                                            except Exception as e:
                                                print(e)
                                                return Response({"status":False,"message":str(e)}) 
                                else:
                                    ob=vendor_po_No_upload_status.objects.all()
                                    serializer=ser_vendor_po_No_upload_status(ob,many=True)
                                    return Response({"status":True,"message":"Report uploaded succesfully","status_obj":serializer.data})
                            else:
                                context={"status":False,"message":"DPR Report is empty"}
                                return Response(context)                      
                    else:
                          return Response({"status":False,"message":"No report file is selected"})
                                       
    else:
          return Response({"status":False,"message":"Not authorised to upload files"})
    

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_circle_list(request):
      objs= circle_list.objects.all()
      seriaizer=ser_circle_list(objs, many=True)
      return Response({"status":True,"circle_list":seriaizer.data})