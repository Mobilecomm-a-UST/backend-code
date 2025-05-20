from Audit_ZTE_HR.views import *
from django.urls import path

urlpatterns = [
    path('upload/',zte_hr_upload_report),
]