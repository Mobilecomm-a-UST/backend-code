# Soft_AT_Nokia/urls.py

from django.urls import path

from Soft_AT_Checklist_Nokia.views import *


urlpatterns = [
    path('process-xml/',upload_and_compare_xml_files ),
    path('get/',upload_and_compare_xml),
    path('upload-excel/', upload_excel),
    
    path('upload_Summary_excel/', upload_Summary_excel),
    path('add_excel',get_summary_data),
    #################3surrmay#################
    path('upload_Summary_excel/', upload_Summary_excel),
    path('get_summary/',get_summary_data),
    path('upload_summary_xml_files/', upload_summary_xml_files),

    # upload_Summary_xml_data

  
   
]
