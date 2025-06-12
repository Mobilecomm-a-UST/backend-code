from django.urls import path
from .views import *


urlpatterns = [
      path("extract_data/", extract_data_from_log, name="extract_data"),
]
