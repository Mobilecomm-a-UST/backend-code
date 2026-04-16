from django.contrib import admin
from django.urls import path
from  . import views


urlpatterns = [
    path("crf_data/",views.nokia_2g),

  
]