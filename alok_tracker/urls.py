from django.urls import path 
from alok_tracker.views import *

urlpatterns = [
    path("upload_file/", upload_tracker_data_view, name="upload_alok_data"),
    path("download_tracker_file/", download_tracker_data_view, name="download_alok_data"),
    path("daily_dashboard_file/", daily_dashboard_file, name="daily_dashboard"),
    path("weekly_monthly_dashboard_file/", weekly_monthly_dashboard_view, name="weekly_monthly_dashboard")
]
