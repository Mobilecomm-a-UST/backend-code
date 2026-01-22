# Soft_AT_Nokia/urls.py

from django.urls import path

from Soft_At_Nokia.views import *


urlpatterns = [
    path('process-xml/', upload_and_compare_xml_files, name="upload_and_compare_xml_files"),
    path('get/', upload_and_compare_xml, name="upload_and_compare_xml"),
    path('upload-excel/', upload_excel, name="upload_excel"),

    path('upload_Summary_excel/', upload_Summary_excel, name="upload_Summary_excel"),
    path('add_excel', get_summary_data, name="get_summary_data"),
    path('upload_Summary_excel/', upload_Summary_excel, name="upload_Summary_excel"),
    path('get_summary/', get_summary_data, name="get_summary_data"),
    path('upload_summary_xml_files/', upload_summary_xml_files, name="upload_summary_xml_files"),
    path('user_count/', user_count, name="user_count"),
]
