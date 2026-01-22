from django.urls import path
from .views import *

urlpatterns = [
    path("Details/",rru_details_upload, name="RRU_Details"),
]

