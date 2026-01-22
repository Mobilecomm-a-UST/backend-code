from django.contrib import admin
from django.urls import path
from RCA_TOOL.views import *

urlpatterns = [
    path('kpi-tables/', kpi_table_list, name='kpi-table-list'),
    path('kpi-tables/<int:pk>/', kpi_table_detail, name='kpi-table-detail'),
    path('rca-tables/', rca_table_list, name='rca-table-list'),
    path('rca-tables/<int:pk>/', rca_table_detail, name='rca-table-detail'),
    path('unique_kpi/', unique_kpi, name='unique_kpi'),
    path("Daily_RAW_KPI_4G/",Daily_RAW_KPI_4G),
    path('AlarmFileUpload/', AlarmFileUpload, name='bulk-upload'),
    path('tantative_counters_save_data_upload/', tantitive_counters_save_data, name='tantitive_counters_save_data'),
    path("Generate-RCA/",main_process),
    path("latest_record_date/",latest_record_data),
    path("RCA_Table_output/",get_RCA_Table_Output),
    path("rca_payload_tables/",rca_payload_list, name='rca-payload-table-list'),
    path("rca_payload_tables/<int:pk>/",rca_payload_detail, name='rca-payload-table-detail'),
    path("pyl_rca/",payload_rca, name='rca-payload-table-detail'),
    path('get-rca-output-dated/', get_rca_output_dated, name='get_rca_output'),
    path('rca-dashboard/',rca_dashboard),
    path('filter_tantitive_data_postgres/',filter_tantitive_data_postgres)
]