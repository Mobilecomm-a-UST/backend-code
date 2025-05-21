# Soft_AT_Nokia/urls.py

from django.urls import path

from .views import upload_and_compare_xml_files,upload_and_compare_xml, upload_excel,upload_Summary_excel


urlpatterns = [
    path('process-xml/',upload_and_compare_xml_files ),
    path('get/',upload_and_compare_xml),
    path('upload-excel/', upload_excel),
    path('upload_Summary_excel/', upload_Summary_excel),

  
   
]
