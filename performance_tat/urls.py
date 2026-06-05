from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('upload/', upload_file),
    path('generate-tat-report/', generate_tat_report),
    
]