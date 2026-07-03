from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('upload/',   upload_file),
    path('months/',   get_months),
    path('date-range-selection/', date_range_selection),
    path('generate-offered/', generate_offered),
    path('generate-performance/', generate_performance),
    path('generate-performance-at-srwise-report/', performance_at_sr_wise_tracking),
    path("generate-atsrwise-summary/", performance_at_srwise_summary),
    path('generate-ftr/', generate_ftr),
    path('generate-scft/', generate_scft),
    path('generate-scft-offered/',generate_scft_offered),
    path('generate-scft-performance/',generate_scft_performance), 
    path('generate-offered-graph/', generate_offered_graph),
    path('generate-performance-graph/',generate_performance_graph),
    path('generate-scft-offered-graph/', generate_scft_offered_graph),
    path('generate-scft-performance-graph/', generate_scft_performance_graph),
    path('generate-offered-circle-graph/', generate_offered_circle_graph),
    path('generate-performance-circle-graph/', generate_performance_circle_graph),
    path('generate-scft-offered-circle-graph/', generate_scft_offered_circle_graph),
    path('generate-scft-performance-circle-graph/', generate_scft_performance_circle_graph),
    path('cleanup/',  cleanup),
    path("performance-at-pending-report/",performance_at_pending_report),
]