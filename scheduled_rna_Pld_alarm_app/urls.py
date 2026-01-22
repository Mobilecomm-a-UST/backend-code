from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('make_alarm_trend/',views.generat_rna_ply_alrm_trend),
    
]