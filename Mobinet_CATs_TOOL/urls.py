from django.contrib import admin
from django.urls import path
from  . import views

urlpatterns = [
 path("mobinet/",views.mobinet_dump),
 path("cats/",views.rfs_dump),
# path("mobinet_dump/", views.upload_mobinet_dumps),
#  path("mobinet_cats/",views.mobinet_rfslocator_dump)
#  path("nms/",views.mobinet_Site_match),
 ]
