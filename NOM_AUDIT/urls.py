from django.urls import path
from NOM_AUDIT.views import *

urlpatterns = [
    path("generate_site_scripts/", generate_site_scripts, name='generate_site_scripts'),
    path("pre_post_audit_process/", pre_post_audit_process, name='pre_post_audit_process'),
]