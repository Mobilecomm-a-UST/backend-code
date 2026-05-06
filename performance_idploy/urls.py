from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('upload/',   upload_file),
    path('months/',   get_months),
    path('generate-offered/', generate_offered),
    path('generate-performance/', generate_performance),
    path('cleanup/',  cleanup),
]