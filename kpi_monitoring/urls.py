from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('upload/', upload_file),
    path('generate-kpi-monitoring-report/', generate_kpi_monitoring_report),
    path('filter-kpi-report/', filter_kpi_report),
    

    ]