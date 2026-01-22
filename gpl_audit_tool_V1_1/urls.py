from django.urls import path
from gpl_audit_tool_V1_1.views import get_log_parser, get_pre_post_audit
from gpl_audit_tool_V1_1.NRLTEViews import get_LTE_NR_pre_post_audit


urlpatterns = [
    path('get_parsed_data/', get_log_parser, name='parser_generator'),
    path('get_audit_data/', get_pre_post_audit, name='gpl_extractor_audit'),
    path('get_4G_5G_audit_data/', get_LTE_NR_pre_post_audit, name='gpl_extractor_audit')
]
