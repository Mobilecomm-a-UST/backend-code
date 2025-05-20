from django.contrib import admin
from django.urls import path,include
from delTrendAPP import views
urlpatterns = [
   
    path("makeKpiTrend/old/",views.old_del_trend),
    


]