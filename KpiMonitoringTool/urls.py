from django.urls import path
from KpiMonitoringTool.views import *

urlpatterns = [
    path("get/kpis/",get_kpi_monitoring_files, name="get_kpi_monitoring_files")  # noqa: F405
]
