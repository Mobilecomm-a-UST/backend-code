from django.contrib import admin
from django.urls import path
from .import views


urlpatterns = [
    
    path('linkbudget/',views.upload_link_budget),
    path("upload_dump/",views.upload_cergon_dump),
    path("parameter/",views.microwave_para),
    path("parameter/<int:pk>/",views.microwave_para)
]