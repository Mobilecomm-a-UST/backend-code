from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path("upload/",views.WPR_DPR2_Upload), 
    # path("overAll_Dashboard/",views.overall_Dashboard), 
    path("project_ageing/",views.projectAgeing),
    path("site_list_request_handler_projectWise/",views.site_list_request_handler_projectWise),
    path("weeklyComparision/",views.weeklyComparision),
    path("weeklyComparision/dashboard/",views.weeklyComparision_dashboard),
    path("testing/",views.testing),
    path("overAll_Dashboard/",views.overAll_Dashboard),
    
         
    ]