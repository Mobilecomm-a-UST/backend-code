from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
   
    path("makeKpiTrend/old/4G",views.old_ap4G_trend),
    path("makeKpiTrend/old/2G",views.old_ap2G_trend),

   


]