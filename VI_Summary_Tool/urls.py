from django.contrib import admin
from django.urls import path
from .import views


urlpatterns = [
    path("vi_summary_4g/",views.vi_4g_summary),
    path("vi_summary_5g/",views.vi_5g_summary),
    path("temp/",views.vi_summary_template)

  ]