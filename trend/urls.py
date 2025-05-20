from django.contrib import admin
from django.urls import path,include
from trend import views

from rest_framework.authtoken import views as v
urlpatterns = [  
   
    path("upload_key_dpr/",views.dpr_key_upload, name="dpr_key_upload"), #api post
    path("dpr_report_upload/",views.dpr_report_upload, name="dpr_report_upload"), #api post
    path("mapa_status_upld/",views.mapa_status_upld, name="mapa_status_upld"),#api post
    # http://127.0.0.1:8001/trend/single_site_view/APBKD0071G1800_L1800ATCulsuls
    
    path("dpr_site_list/",views.dpr_site_list, name="dpr_update"), #api get
    path("single_site_view/<str:pk>/",views.single_site_view, name="single_site_view"), #api get
    
    path("soft_at_update/<str:pk>/<str:at_status>",views.soft_at_update, name="soft_at_update"), #api patch
    path("physical_at_update/<str:pk>/<str:at_status>",views.physical_at_update, name="physical_at_update"), #api patch
    path("performance_at_update/<str:pk>/<str:at_status>/<str:band>",views.performance_at_update, name="performance_at_update"), #api patch
    
    path("dashboard/",views.all_dashboard, name="dashboard"),#api get
    path("circle_wise_dashboard/",views.circle_wise_dashboard, name="circle_wise_dashboard"), #api get

    path("dpr_view/<str:circle>",views.dpr_view, name="dpr_view"),#api get

    path("performance_at_tat_date/<str:pk>",views.performance_at_tat_date, name="performance_at_tat_date"),#api post
    path("mapa_single_site_update/<str:pk>",views.mapa_single_site_update, name="mapa_single_site_update"), #api post

    path("get_dpr_key_temp/",views.get_dpr_key_temp, name="get_dpr_key_temp"), #api get
    path("get_dpr_temp/",views.get_dpr_temp, name="get_dpr_temp"), #api get
    path("get_circle/",views.get_circle, name="get_circle"), #api get
    path("MasterDashboard/",views.MasterDashboard, name="MasterDashboard"), # api get
    


]

urlpatterns += [
    path('api-token-auth/', v.obtain_auth_token) 
    
]
 