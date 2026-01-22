from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
   
    path("makeKpiTrend/degrow",views.UE_degrow),
   


]