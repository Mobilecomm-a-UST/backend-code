from django.urls import path
from .views import xml_bulk_to_excel,nrrel_parse_status

urlpatterns = [
    path("parse_dump/", xml_bulk_to_excel),
    path("nrrel_parser/",nrrel_parse_status)

]
