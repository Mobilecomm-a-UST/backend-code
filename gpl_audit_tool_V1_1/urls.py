from django.urls import path
from gpl_audit_tool_V1_1.views import get_log_parser



urlpatterns = [
    path('get_parsed_data/', get_log_parser, name='parser_generator')
]
