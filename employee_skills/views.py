
import pandas as pd
from django.http import JsonResponse
from .models import EmployeeSkillTable
import numpy as np
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import EmployeeSkillTable
from .serializers import EmployeeSkillTableSerializer, EmployeeSkillTableSerializer_create
from Profile.models import userCircle
from datetime import datetime
def get_user_circle(request):
        user = request.user
        print("usrname: ",user)
        user_circle = user.usercircle.Circle
        if user_circle:
            user_circle=user_circle.split(",")
        else:
            user_circle=[]
        return user_circle

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def employee_skill_table(request):
    print(request.user)
    if request.method == 'GET':
        
        user_circle=get_user_circle(request)
        if "Admin" in user_circle:
            print("admin",user_circle)
            employee_skill_table = EmployeeSkillTable.objects.filter(active=True)
        else:
            print(user_circle)
            employee_skill_table = EmployeeSkillTable.objects.filter(circle__in=user_circle,active=True)
        
        serializer = EmployeeSkillTableSerializer(employee_skill_table, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = EmployeeSkillTableSerializer(data=request.data,request=request)
        emp_code=request.data.get('emp_code')
        print("emp_code",emp_code)
        # print(request.data)
        if EmployeeSkillTable.objects.filter(emp_code=emp_code, active=False).exists():
                    # raise serializers.ValidationError("An active record with this employee ID already exists.")
                    print("deleted the employ")
                    obj=EmployeeSkillTable.objects.get(emp_code=emp_code)
                    obj.delete()
        if EmployeeSkillTable.objects.filter(emp_code=emp_code, active=True).exists():
            return Response({'error':"Employee with this employee code already exists"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def employee_skill_table_update(request, id=None,remark=None):
    user = request.user
    print("usrname: ",user)
    if request.method == 'POST':
        try:
            employee_skill_table = EmployeeSkillTable.objects.get(pk=id)
        except EmployeeSkillTable.DoesNotExist:
            return Response({'message': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeSkillTableSerializer(employee_skill_table, data=request.data,request=request)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        print("delete Remark",remark)
        try:
            print("ID : ",id)
            employee_skill_table = EmployeeSkillTable.objects.get(pk=id)
        except EmployeeSkillTable.DoesNotExist:
            return Response({'message': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)

        employee_skill_table.active=False
        employee_skill_table.deleted_by=request.user.username 
        employee_skill_table.delete_remark=remark
        print("user....",request.user.pk)
        employee_skill_table.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)
    


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def upload_excel_1(request):
    user = request.user
    user_circle = get_user_circle(request)
    print("usrname: ", user)
    if request.method == 'POST' and request.FILES['file']:
        excel_file = request.FILES['file']
        # Check if the uploaded file is an Excel file
        if not excel_file.name.endswith('.xlsx'):
            return JsonResponse({'error': 'Only Excel files are allowed.'}, status=400)
        
        # Read the Excel file
        try:
            df = pd.read_excel(excel_file, skiprows=2,keep_default_na=False)

            df.columns = [col.strip() for col in df.columns]
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

        # Loop through each row in the DataFrame and save to EmployeeSkillTable
        for _, row in df.iterrows():
            # Check and handle non-numeric values in total_exp and mobilecomm_exp
            total_exp = row['Total Exp']
            if not isinstance(total_exp, (int, float)) or np.isnan(total_exp):
                total_exp = 0
            
            mobilecomm_exp = row['Mobilecomm Exp']
            if not isinstance(mobilecomm_exp, (int, float)) or np.isnan(mobilecomm_exp):
                mobilecomm_exp = 0
            
            # Check and handle blank or invalid values in doj
            doj = row["DOJ"]
            if pd.isnull(doj) or (isinstance(doj, str) and doj.strip() == ""):
                doj = None
            # else:
            #     # Parse and convert the date string to the YYYY-MM-DD format
            #     try:
                   
            #         doj=str(doj)
            #         print(doj)
            #         doj = datetime.strptime(doj, "%m/%d/%Y").strftime("%Y-%m-%d")
            #     except ValueError:
            #         print('error')
            #         return Response({'error': 'Invalid date format. Date must be in MM/DD/YYYY format.'}, status=400)

            # Save to EmployeeSkillTable
            EmployeeSkillTable.objects.update_or_create(
                emp_code=row['emp_Code'],
                defaults={
                    'employee_name': row['Employee_name'],
                    'designation': row['Designation'],
                    'doj': doj,
                    'circle': row['Circle'],
                    'project_name': row['Project Name'],
                    'manager_emp_code': row['Manager Emp. Code'],
                    'reporting_manager_name': row['Reporting Manager Name'],
                    'mobile_no': row['Mobile_no'],
                    'email_id': row['email_id'],
                    'domain': row['Domain'],
                    'project': row['Project'],
                    'current_role': row['Current Role'],
                    'key_responsibility': row['Key Responsibility'],
                    'skillsets': row['skillsets'],
                    'oem': row['oem'],
                    'total_exp': total_exp,
                    'mobilecomm_exp': mobilecomm_exp,
                    'previous_org1': row['Previous Org1'],
                    'previous_org2': row['Previous Org2'],
                    'previous_org3': row['Previous Org3'],
                    'current_designation': row['Current designation'],
                    'working_status': row['working_status'],
                    'team_category': row['Team Category'],
                    'current_circle': row['Current Circle']
                }
            )
        return JsonResponse({'success': 'Data uploaded successfully.'}, status=200)

    return JsonResponse({'error': 'Invalid request method or no file provided.'}, status=400)

import openpyxl
from io import BytesIO

def read_excel_cell(file_contents, sheet_name, cell):
    # Load the Excel file from memory
    wb = openpyxl.load_workbook(filename=BytesIO(file_contents))
    
    # Select the specific sheet by name
    sheet = wb[sheet_name]
    
    # Get the value of the specified cell
    cell_value = sheet[cell].value
    
    return cell_value

from django.db.models import Q
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def upload_excel(request):
    user = request.user
    user_circle = get_user_circle(request)
    print("usrname: ", user)
    if request.method == 'POST' and request.FILES['file']:
        excel_file = request.FILES['file']
        # Check if the uploaded file is an Excel file
        if not excel_file.name.endswith('.xlsm'):
            return JsonResponse({'error': 'Only Excel files are allowed.'}, status=400)
        
        # Read the Excel file
        value_in_cell = read_excel_cell(excel_file.read(), sheet_name='Sheet2', cell='BE37')
        print("cell_value:",value_in_cell)
        if value_in_cell == "mcom123":
            try:
                df = pd.read_excel(excel_file, skiprows=2,keep_default_na=False)

                df.columns = [col.strip() for col in df.columns]
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
            

            allowed_values = {
                'Circle': ['AP', 'BIH', 'CHN', 'ROTN', 'DEL', 'HRY', 'JK', 'JRK', 'KOL', 'MAH', 'MP', 'MUM', 'ORI', 'PUN', 'RAJ', 'UPE', 'UPW', 'WB', 'KK'],
                'Domain': ['RAN', 'TX', ],
                'Project': ['ULS_HPSC', 'Relocation', 'MACRO', 'De-Grow', 'MW LOS Survey', 'MW LOS  Survey','UBR', 'RET', 'Cluster AT', 'RF Survey', 'MW NT', 'IBS', 'ODSC', 'IDSC', 'HT Increment', 'FEMTO','E2E Project Management', 'Others'],
                'Current Role': ['PM', 'Cordinator', 'FE', 'Technician', 'RNO', 'Ix Engg', 'AM', 'Engg', 'CDH'],
                'Key Responsibility': ['Survey', 'I&C', 'Phy AT', 'SCFT', 'Soft AT', 'Ware house Coordinator', 'MIS', 'Integration', 'KPI AT', 'SCFT Coordinator', 'Customer Support'],
                'oem': ['Nokia', 'Ericsson', 'Samsung', 'ZTE', 'Huawei','Ceragon','Cambium','Radwin'],
                'working_status': ['On Job', 'On Leave', 'Abscond', 'Resigned', 'LWP', 'Irregular', 'Maternity Leave'],
                'Team Category': ['Field', 'Backend']
            }

            # Define columns where only emptiness needs to be checked
            empty_check_columns = ['Employee_name', 'Designation', 'DOJ', 'Project Name', 'Mobile_no', 'email_id', 'skillsets', 'Total Exp', 'Mobilecomm Exp', 'Current designation', 'emp_Code']

            invalid_rows=[]
            def check_multiple_values(value, allowed_list):
                values = [v.strip() for v in value.split(',')]
                return all(v in allowed_list for v in values)
            # Loop through each row in the DataFrame and save to EmployeeSkillTable
            for _, row in df.iterrows():
                # Check and handle non-numeric values in total_exp and mobilecomm_exp
                # invalid_cols = [col for col in allowed_values 
                #                 if col not in df.columns 
                #                 or pd.isnull(row[col]) 
                #                 or str(row[col]).strip() == '' 
                #                 or row[col] not in allowed_values[col]]

                invalid_cols = []
                for col in allowed_values:
                    if col not in df.columns or pd.isnull(row[col]) or str(row[col]).strip() == '':
                        invalid_cols.append(col)
                    else:
                        if ',' in str(row[col]):  # Check for multiple values
                            if not check_multiple_values(str(row[col]), allowed_values[col]):
                                invalid_cols.append(col)                
                        else:
                            if row[col] not in allowed_values[col]:
                                invalid_cols.append(col)

                empty_cols= [col for col in empty_check_columns
                                if col not in df.columns 
                                or pd.isnull(row[col]) 
                                or str(row[col]).strip() == '' 
                                ]
                
                invalid_fields= invalid_cols + empty_cols
                con1=False
                con2=False
                con3=False
                if invalid_fields:
                    con1=True
                    # Store the employee code and column names for invalid fields
                    invalid_row = {'emp_code': row['emp_Code'], 'invalid_fields': invalid_fields, 'remarks':'These columns are mandatory OR value out of specified options'}
                    invalid_rows.append(invalid_row)
                    

                if row["Circle"] not in user_circle:
                    con2=True
                    invalid_row = {'emp_code': row['emp_Code'], 'invalid_fields':[row["Circle"]], 'remarks':f'You Can not assign Circle out of your Scope'}
                    invalid_rows.append(invalid_row)

                if EmployeeSkillTable.objects.filter(Q(emp_code=row['emp_Code']) & ~Q(circle__in=user_circle) & Q(active=True)).exists():
                    emp=EmployeeSkillTable.objects.filter(emp_code=row['emp_Code'])
                    con3=True
                    invalid_row = {'emp_code': row['emp_Code'], 'invalid_fields':["Circle"], 'remarks':f'This user already exist in another Circle, If you want to add in your circle Ask the CDH of that circle to delete him'}
                    invalid_rows.append(invalid_row)
                    

                if con1 or con2 or con3:
                    continue   



                total_exp = row['Total Exp']
                if not isinstance(total_exp, (int, float)) or np.isnan(total_exp):
                    total_exp = 0
                
                mobilecomm_exp = row['Mobilecomm Exp']
                if not isinstance(mobilecomm_exp, (int, float)) or np.isnan(mobilecomm_exp):
                    mobilecomm_exp = 0
                
                # Check and handle blank or invalid values in doj
                doj = row["DOJ"]
                if pd.isnull(doj) or (isinstance(doj, str) and doj.strip() == ""):
                    doj = None
                # else:
                #     # Parse and convert the date string to the YYYY-MM-DD format
                #     try:
                    
                #         doj=str(doj)
                #         print(doj)
                #         doj = datetime.strptime(doj, "%m/%d/%Y").strftime("%Y-%m-%d")
                #     except ValueError:
                #         print('error')
                #         return Response({'error': 'Invalid date format. Date must be in MM/DD/YYYY format.'}, status=400)
                 
                # Save to EmployeeSkillTable
                EmployeeSkillTable.objects.update_or_create(
                    emp_code=row['emp_Code'],
                    defaults={
                        'employee_name': row['Employee_name'],
                        'designation': row['Designation'],
                        'doj': doj,
                        'circle': row['Circle'],
                        'project_name': row['Project Name'],
                        'manager_emp_code': row['Manager Emp. Code'],
                        'reporting_manager_name': row['Reporting Manager Name'],
                        'mobile_no': row['Mobile_no'],
                        'email_id': row['email_id'],
                        'domain': row['Domain'],
                        'project': row['Project'],
                        'current_role': row['Current Role'],
                        'key_responsibility': row['Key Responsibility'],
                        'skillsets': row['skillsets'],
                        'oem': row['oem'],
                        'total_exp': total_exp,
                        'mobilecomm_exp': mobilecomm_exp,
                        'previous_org1': row['Previous Org1'],
                        'previous_org2': row['Previous Org2'],
                        'previous_org3': row['Previous Org3'],
                        'current_designation': row['Current designation'],
                        'working_status': row['working_status'],
                        'team_category': row['Team Category'],
                        'current_circle': row['Current Circle'],
                        'active':True,
                        'uploaded_by':request.user.username


                    }
                )
            return JsonResponse({'success': 'Data uploaded successfully.','error_rows':invalid_rows}, status=200)
        else:
            JsonResponse({'error': 'invalid template'}, status=400)
    return JsonResponse({'error': 'Invalid request method or no file provided.'}, status=400)









# views.py
import os
# from django.http import HttpResponse
from django.conf import settings
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status

@api_view(['GET'])
def get_excel_temp_link(request):
    #mcom123 temp id.
    # Path to the Excel file
    file_path = os.path.join(settings.MEDIA_ROOT, 'employee_skills', 'SkillSetTemplate.xlsm')

    # Check if the file exists
    if os.path.exists(file_path):
        # Construct the URL to access the file
        file_url = os.path.join(settings.MEDIA_URL ,'employee_skills' , 'SkillSetTemplate.xlsm')              
        return Response({'file_url': file_url}, status=status.HTTP_200_OK)
    else:
        # Return a 404 response if the file does not exist
        return Response({'error': 'Excel file not found'}, status=status.HTTP_404_NOT_FOUND)






