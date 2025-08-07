from django.contrib import admin
from django.urls import path
from  Mobinet_CATs_TOOL import views

urlpatterns = [
    path("mobinate/",views.mobinet_dump),
    path("cats/",views.rfs_dump),
    path("mobinet_dump/", views.upload_mobinet_dumps),

 ]
