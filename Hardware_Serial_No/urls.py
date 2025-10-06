from django.urls import path
from .views import *

urlpatterns = [
    path("hsn/", upload_hsn, name="twamp_data"),
]

