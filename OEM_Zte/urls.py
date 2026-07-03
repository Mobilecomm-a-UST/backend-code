from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('SA_NSA/', fileupload, name='zte_MS2'),
    path('zte/', alarmfileUpload, name='zte_MS2'),
    path('old_vs_new/', manage_sites),
    path('mapping_file/', upload_mapping_file),
]