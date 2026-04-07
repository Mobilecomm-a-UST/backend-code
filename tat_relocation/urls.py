from django.urls import path
from .views import *


urlpatterns = [
path("download_tracker_data/", download_tracker_data_view, name="download_tracker_data"), 
path('upload-tracker/', upload_tracker_data_view),   
]
