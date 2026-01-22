from django.urls import path
from .views import xml_bulk_to_excel

urlpatterns = [
    path("parse_dump/", xml_bulk_to_excel),
]
