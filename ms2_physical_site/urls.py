from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('ms2/', MS2_upload, name='MS2')
]
