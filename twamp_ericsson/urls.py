from django.urls import path
from .views import *

urlpatterns = [
      path("twamp_data/", twamp_data, name="twamp_data"),
]

