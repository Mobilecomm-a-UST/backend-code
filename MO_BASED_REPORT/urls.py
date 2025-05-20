from django.contrib import admin
from django.urls import path
from MO_BASED_REPORT.views import *

urlpatterns = [
    path("upload/", Mo_Based_Report_Upload),
    path("cats_tracker_dashboard/", cats_tracker_dashboard),
    path("unique_circle_status_month/", unique_circle_status_month),
    path("shipment_dump/", shipment_dump),
    # path("testing_api/", testing_api),
    path("monthly_signoff_cats_vs_mobinet/", monthly_signoff_cats_vs_mobinet),
]
