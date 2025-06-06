# Soft_AT_Nokia/urls.py

from django.urls import path

from .views import *


urlpatterns = [
    path('process-xml/',upload_and_compare_xml_files ),
    path('get/',upload_and_compare_xml),
    path('upload-excel/', upload_excel),
    #################3surrmay#################
    path('upload_Summary_excel/', upload_Summary_excel),
    path('add_excel',get_summary_data),
    path('upload_summary_xml_files/', upload_summary_xml_files),

    # upload_Summary_xml_data

  
   
]
