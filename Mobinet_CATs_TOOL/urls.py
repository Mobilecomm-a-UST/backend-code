from django.contrib import admin
from django.urls import path
from  Mobinet_CATs_TOOL import views

urlpatterns = [
    path("mobinate/",views.mobinet_dump),
    path("cats/",views.rfs_dump),
    path('delete_mobinet_file/', views.delete_single_mobinet_file),
    
     #api for uploading data----------
    path("mobinet_dump/", views.upload_mobinet_dumps),
    path('rfs/', views.upload_rfs_data),
    path('msmf/', views.upload_msmf_data),
    path('locator/', views.upload_locator_data),
    path('stock/', views.upload_stock_report_data),
    path('rfs_site_mapping/', views.rfs_site_mapping),
    path('ms_mf_site_mapping/', views.ms_mf_site_mapping),
    path('site_sn/', views.mobinet_sitecircle_match), #new api site+sn

    # upload Mobinet baseline file 
    path("mobinet_baseline_upload/",views.upload_mobinet_baseline),
    # upload TOD file 
    path('tod_file_upload/',views.upload_tod_file),
    # forward_material_reconciliation
    path('forward_material_reconciliation/',views.forward_material_reconciliation),


    path("dismental_dash/",views.dismental_desh),
    path("temp_dash/",views.dismental_template),


]


 
