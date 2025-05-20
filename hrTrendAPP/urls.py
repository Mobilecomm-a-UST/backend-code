from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
   
    path("makeKpiTrend/old/",views.old_hr_trend),
    # path("logout/",views.logout, name="logout"),


]