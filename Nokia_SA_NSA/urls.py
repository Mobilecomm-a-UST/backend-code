from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('SA_NSA/', fileupload, name='Nokia_MS2'),
    path('Nokia/', alarmfileUpload, name='Nokia_MS2'),
]