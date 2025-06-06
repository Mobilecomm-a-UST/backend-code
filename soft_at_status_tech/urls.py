from django.urls import path
from soft_at_status_tech.views import *


urlpatterns = [
    path("extract_data/", extract_data_from_log, name="extract_data"),
]
