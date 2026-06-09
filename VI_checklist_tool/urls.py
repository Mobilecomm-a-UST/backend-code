from django.contrib import admin
from django.urls import path
from .import views


urlpatterns = [
    path("vi_checklist/",views.vi_tracker_dump),

  ]