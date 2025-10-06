from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
   
    path('makeKpiTrend/old/4G',views.old_or_trend),
    path('makeKpiTrend/old/RNA',views.old_or_Trend_rna),
    path('makeKpiTrend/old/2G_trend',views.trendfor2g),
    path('makeKpiTrend/old/4G_trend',views.trendfor4g),
    
]