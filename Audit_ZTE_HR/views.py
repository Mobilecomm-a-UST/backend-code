from rest_framework.response import Response
from rest_framework.decorators import api_view
from Audit_ZTE_HR.models import *
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
import os
from django.core.files.storage import FileSystemStorage
from Audit_ZTE_HR.serializers import *

import pandas as pd





def process_save_to_database(df):
    try:
        instances = []
        for i, d in df.iterrows():
            instance = ZTE_HR_Report(
                Technology=str(d['TECHNOLOGY']),
                MO_FDD=str(d['MO FDD']),
                MO_TDD=str(d['MO TDD']),
                ZTE_parameter=str(d['ZTE PARAMETER']),
                Parameter_type=str(d['PARAMETER TYPE']),
                L2100=str(d['L2100']),
                L1800=str(d['L1800']),
                TD20=str(d['TD20']),
                Meascinfigindx=str(d['MEASCINFIGINDX']),
                Category=str(d['CATEGORY']),
                Remarks=str(d['REMARKS'])
            )
            instances.append(instance)

        ZTE_HR_Report.objects.bulk_create(instances)

        print("Objects created successfully")

    except Exception as e:
        print("Error:", e)
        error = str(e)
        return Response({
            'Status': False,
            "message": error
        })





@api_view(["POST"])
def zte_hr_upload_report(request):
    Audit_hr_report_file = (
        request.FILES["Audit_hr_report_file"]
        if "Audit_hr_report_file" in request.FILES
        else None
    )
    if Audit_hr_report_file:
        location = os.path.join(MEDIA_ROOT, "Audit_ZTE_HR", "temporary_files")
        fs = FileSystemStorage(location=location)
        file = fs.save(Audit_hr_report_file.name, Audit_hr_report_file)
        filepath = fs.path(file)
        print("file_path:-", filepath)

        try:
            df = pd.read_excel(filepath, sheet_name="HAR")
            os.remove(filepath)
            print(filepath, "deleted........")

            df.columns = df.columns.str.upper().str.strip()
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

            print(df.columns)

            process_save_to_database(df)

            objs = ZTE_HR_Report.objects.all()
            serializers = ser_ZTE_HR_Report(objs, many=True)

            return Response(
                {
                    "status": True,
                    "message": "Report uploaded Successfully .",
                    "status_obj": serializers.data,
                }
            )
        except Exception as e:
            print("Error:", e)
            os.remove(filepath)  # Clean up in case of an error
            error = str(e)
            return Response({"status": False, "message": f"Error uploading report: {error}"})
    else:
        return Response({"status": False, "message": "No report file sent"})
