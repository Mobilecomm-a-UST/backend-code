from django.contrib import admin
from django.urls import path,include
from mumTrendAPP import views
urlpatterns = [
   
    path("makeKpiTrend/old/",views.old_mum_trend),
    


]