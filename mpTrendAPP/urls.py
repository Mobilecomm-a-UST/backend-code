from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('makeKpiTrend/old/4G',views.old_mp_trend),
    path('makeKpiTrend/old/2G',views.old_mp2G_trend),
]