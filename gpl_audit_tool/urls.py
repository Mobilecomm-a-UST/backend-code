from django.urls import path
from gpl_audit_tool.views import *



urlpatterns = [
    path('get_table_data/', get_table_data, name='gpl_extractor')
]
