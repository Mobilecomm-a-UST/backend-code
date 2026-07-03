from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('SA_NSA/', fileupload, name='Huawei_SA_NSA'),
    path('Huawei/', alarmfileUpload, name='Huawei_Alarm_Upload'),
    path('upload_site/', upload_site_list, ),
    path('delete_site/', delete_sites, ),
    path('get_site/', get_sites, ),

]
