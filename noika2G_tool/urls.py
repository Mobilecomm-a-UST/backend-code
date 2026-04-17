from django.contrib import admin
from django.urls import path
from .import views


urlpatterns = [
    path("script/",views.nokia_2g),

  
]