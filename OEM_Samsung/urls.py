from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('SA_NSA/', fileupload, name='SAMSUNG_SA_NSA'),
    path('Samsung/', alarmfileUpload, name='SAMSUNG_Alarm_Upload'),
    path('upload_site/', upload_site_list, ),
    path('delete_site/', delete_sites, ),
    path('get_site/', get_sites, ),

]
