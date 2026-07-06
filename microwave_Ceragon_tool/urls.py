from django.contrib import admin
from django.urls import path
from .import views


urlpatterns = [

    path('linkbudget/',views.upload_link_budget),
    path('upload_traffic/',views.upload_traffic_shifting),
    path("upload_dump/",views.upload_cergon_dump),
    path("parameter/",views.microwave_para),
    path("parameter/<int:pk>/",views.microwave_para),
    path("search_planid/",views.search_plan_id),
  
    path("upload_serverip/",views.circle_server_ip),
    path("get_serverip/",views.get_server_ip),

   
    
]