from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
   
    path('makeKpiTrend/old/4G',views.old_or_trend),
    path('makeKpiTrend/old/RNA',views.old_or_Trend_rna),
]