from django.contrib import admin
from django.urls import path,include
from jkTrendAPP import views
urlpatterns = [
   
    path("makeKpiTrend/old/",views.old_jk_trend),
    


]