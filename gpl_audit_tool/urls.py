from django.urls import path
from gpl_audit_tool.views import *
from gpl_audit_tool_V1_1.views import get_pre_post_audit



urlpatterns = [
    path('get_table_data/', get_table_data, name='gpl_extractor'),
    path('get_audit_data/', get_pre_post_audit, name='gpl_extractor-audit')
]
