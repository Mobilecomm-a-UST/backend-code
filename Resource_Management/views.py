from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MonthlyReport,Employee
from .serializers import MonthlyReportSerializer,MonthlyReportBulkSerializer,EmployeeBulkUploadSerializer
from rest_framework.decorators import api_view
import os
from django.conf import settings
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
import pandas as pd
import re
from django.db.models import F


required_columns = [
    "Year",
    "Month",
    "Customer",
    "Cost Center",
    "UST ID",
    "Circle",
    "Total Revenue",
    "Salary and other component",
    "Partner Cost",
    "Emp. Expenses",
    "Other Fixed Costs",
]


def validate_headers(df):
    missing = [c for c in required_columns if c not in df.columns]
    return missing


def validate_rows(df):

    errors = []

    valid_months = [
        "Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"
    ]

    for index, row in df.iterrows():

        row_no = index + 2

        # Year

        year = str(row["Year"]).strip()

        if year == "":
            errors.append(f"Row {row_no} : Year Required")

        elif not year.isdigit():

            errors.append(f"Row {row_no} : Invalid Year")

        # Month

        month = str(row["Month"]).strip().title()

        if month not in valid_months:

            errors.append(f"Row {row_no} : Invalid Month")

        # Cost Center

        if str(row["Cost Center"]).strip() == "":

            errors.append(f"Row {row_no} : Cost Center Required")

        # Circle

        if str(row["Circle"]).strip() == "":

            errors.append(f"Row {row_no} : Circle Required")

    return errors

def clean_money_columns(df):

    money_columns = [
        "Total Revenue",
        "Salary and other component",
        "Partner Cost",
        "Emp. Expenses",
        "Other Fixed Costs"
    ]

    for col in money_columns:

        df[col] = (

            df[col]

            .astype(str)

            .str.replace("₹", "", regex=False)

            .str.replace(",", "", regex=False)

            .str.replace("-", "0", regex=False)

            .str.replace(r"\s+", "", regex=True)

        )

        df[col] = pd.to_numeric(df[col],errors="coerce").fillna(0)
        df[col] *= 100000

    return df


def format_month(df):

    df["Month"] = (
        df["Month"].astype(str).str.strip().str.title()
        + "-"
        + df["Year"].astype(str).str[-2:]
    )

    return df



CATEGORY_MAP = {
    "MCT0385": "A",
    "MCT0380": "A",
    "MCT0384": "A",
    "MCT0356": "B",
    "MCT0381": "B",
    "MCT0292": "B",
    "MCT0376": "B",
    "MCT0353": "B",
    "MCT0370": "B",
    "MCT0394": "B",
    "MCT0383": "C",
    "MCT0392": "C",
    "MCT0395": "C",
    "MCT0354": "C",
    "MCT0408": "C",
    "MCT0388": "C",
    "MCT0396": "C",
    "MCT0361": "C",
    "MCT0391": "C",
    "MCT0409": "C",
    "MCT0414": "C",
    "MCT0406": "C",
}

class MonthlyReportUpsertView(APIView):

    def get(self, request):
        month    = request.query_params.get('month')
        costCenter = request.query_params.get('costCenter')

        if not all([month, costCenter]):
            return Response({'error': 'Month And Cost Center Required'},status=status.HTTP_400_BAD_REQUEST)

        try:
            report = MonthlyReport.objects.get(month=month,costCenter = costCenter)
        except MonthlyReport.DoesNotExist:
            return Response({'error': 'Record Not found'},status=status.HTTP_404_NOT_FOUND)

        return Response({
            'id':              report.id,
            'circle':          report.circle,
            'category':        report.category,
            'customer':        report.customer,
            'month':           report.month,
            'year':            report.year,
            "costCenter":      report.costCenter,
            'costs':           report.costs,
            'resources':       report.resources,
            'other_resources': report.other_resources,
            'created_at':      report.created_at,
            'updated_at':      report.updated_at,
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MonthlyReportSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'error': serializer.errors},status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        report, created = MonthlyReport.objects.update_or_create(
            
            month    = data['month'],
            costCenter = data['costCenter'],
            defaults = {
                "circle" :data['circle'],
                "category" :data['category'],
                "customer" :data['customer'],
                'year':data['year'],
                'resources':data.get('resources',{}),
                'other_resources':data.get('other_resources', {}),
            }
        )

        return Response({
            'message':  'Created' if created else 'Updated',
            'id':       report.id,
            'month':    report.month,
            'costCenter':report.costCenter,
            'created_at':      report.created_at,
            'updated_at':      report.updated_at,
        }, status=status.HTTP_200_OK)




class MonthlyReportBulkUpsertView(APIView):

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "Excel file is required"},status=status.HTTP_400_BAD_REQUEST)

        df = pd.read_excel(file)
        df = df.fillna("")

        missing = validate_headers(df)
        if missing:
            return Response({"error":f"Missing Columns:-{missing}"},status=status.HTTP_400_BAD_REQUEST)

        df = df[required_columns]

        validation_errors = validate_rows(df)
        if validation_errors:
            return Response({"error":f"Validation Failed:-{validation_errors}"},status=status.HTTP_400_BAD_REQUEST)

        duplicate = df[df["Cost Center"].duplicated()]

        if not duplicate.empty:
            return Response({"error":f"Duplicate Cost Center:-{duplicate['Cost Center'].tolist()}"},status=400)

        df = clean_money_columns(df)

        df = format_month(df)

        df["Category"] = df["Cost Center"].map(CATEGORY_MAP)

        missing_category = df[df["Category"].isna()]

        if not missing_category.empty:
            return Response(
                {
                    "error": f"Circle Category mapping not found for some Cost Centers.-{missing_category['Cost Center'].unique().tolist()}",
                },
                status=400,
            )

        df.rename(columns={
            "Year":"year",
            "Month":"month",
            "Customer":"customer",
            "Cost Center":"costCenter",
            "Category":"category",
            "UST ID":"ustId",
            "Circle":"circle",
            "Total Revenue":"c1",
            "Salary and other component":"c2",
            "Partner Cost":"c3",
            "Emp. Expenses":'c4',
            "Other Fixed Costs":"c5",
        }, inplace=True)

        results = []
        errors = []

        for index,row in df.iterrows():
            row = row.to_dict()
            row["costs"] = {
                "c1": row.pop("c1"),
                "c2": row.pop("c2"),
                "c3": row.pop("c3"),
                "c4": row.pop("c4"),
                "c5": row.pop("c5"),
            }
            row.pop("ustId",None)
            serializer = MonthlyReportBulkSerializer(data=row)

            if not serializer.is_valid():
                errors.append({ 'index': index, 'error': serializer.errors })
                continue

            data = serializer.validated_data

            report, created = MonthlyReport.objects.update_or_create(
                month      = data['month'],
                costCenter = data['costCenter'],
                defaults   = {
                    "customer" : data['customer'],
                    "circle": data['circle'],
                    "category": data['category'],
                    'year':            data['year'],
                    'costs':           data['costs'],
                }
            )

            results.append({
                'index':      index,
                'message':    'Created' if created else 'Updated',
                'id':         report.id,
                'month':      report.month,
                'costCenter': report.costCenter,
                'created_at': report.created_at,
                'updated_at': report.updated_at,
            })

        return Response({
            'total':    len(df),
            'success':  len(results),
            'failed':   len(errors),
            'results':  results,
            'errors':   errors,
        }, status=status.HTTP_200_OK)



class EmployeeBulkUploadView(APIView):

    def post(self, request):

        # if not isinstance(request.data, list):
        #     return Response(
        #         {"error": "Please send array"},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        file = request.FILES.get("file")

        if not file:
            return Response({"error": "Excel file is required"},status=status.HTTP_400_BAD_REQUEST)
        
        df = pd.read_excel(file)
        df = df.fillna("")

        df.rename(columns={
            "Emp. Code": "emp_code",
            "UST ID": "ust_id",
            "Emp Name": "emp_name",
            "Designation Name": "designation_name",
            "Department Name": "department_name",
            "DOJ": "doj",
            "State name": "state_name",
            "Project Code": "project_code",
            "Project Name": "project_name",
            "Location": "location",
            "Manager Emp. Code": "manager_emp_code",
            "Reporting Manager Name": "reporting_manager_name",
            "Status Working/ Not Working": "status",
            "Date of Exit": "date_of_exit",
            "Official email id": "official_email_id",
            "Contact No": "contact_no",
            "Team Category-Backend/Field": "team_category",
        }, inplace=True)

        results = []
        errors = []

        for index, row in df.iterrows():

            serializer = EmployeeBulkUploadSerializer( data=row.to_dict())

            if not serializer.is_valid():
                errors.append({
                    "index": index,
                    "error": serializer.errors
                })
                continue

            data = serializer.validated_data

            employee, created = Employee.objects.update_or_create(
                ust_id=data["ust_id"],
                defaults={
                    "emp_code": data["emp_code"],
                    "emp_name": data["emp_name"],
                    "designation_name": data["designation_name"],
                    "department_name": data["department_name"],
                    "state_name": data["state_name"],
                    "project_code": data["project_code"],
                    "project_name": data["project_name"],
                    "location": data["location"],
                    "manager_emp_code": data.get("manager_emp_code", ""),
                    "reporting_manager_name": data.get("reporting_manager_name", ""),
                    "status": data["status"],
                    "official_email_id": data["official_email_id"],
                    "contact_no": data.get("contact_no", ""),
                    "team_category": data["team_category"],
                }
            )

            results.append({
                "index": index,
                "message": "Created" if created else "Updated",
                "id": employee.id,
                "ust_id": employee.ust_id,
                "emp_name": employee.emp_name,
            })

        return Response({
            "total": len(df),
            "success": len(results),
            "failed": len(errors),
            "results": results,
            "errors": errors,
        })




class EmployeeListView(APIView):

    def get(self, request):
        project_code = request.GET.get("project_code")

        if not project_code:
            return Response({"error": "project_code is required"},status=status.HTTP_400_BAD_REQUEST)

        employees = list(Employee.objects.filter(project_code=project_code).values("emp_code","emp_name","ust_id","team_category"))

        result = [
            {
                "id": emp["emp_code"],
                "name": emp["emp_name"],
                "ustId": emp["ust_id"],
                "category": emp["team_category"],
            }
            for emp in employees
        ]

        return Response(result, status=status.HTTP_200_OK)




@api_view(['GET'])
def get_excel_temp_link(request):
    fileName = request.query_params.get("fileName", "")
    file_path = os.path.join(settings.MEDIA_ROOT, 'ResourceManagement',fileName)
    if os.path.exists(file_path):
        file_url = os.path.join(settings.MEDIA_URL ,'ResourceManagement',fileName)              
        return Response({'file_url': file_url,'template_version':'v1'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Excel file not found'}, status=status.HTTP_404_NOT_FOUND)