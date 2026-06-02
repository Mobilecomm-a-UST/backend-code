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
    path('generate-ftr/', generate_ftr),
    path('generate-scft/', generate_scft),
    path('generate-scft-offered/',generate_scft_offered),
    path('generate-scft-performance/',generate_scft_performance), 
    path('cleanup/',  cleanup),
]