from django.urls import path
from .views import *

urlpatterns = [
    path("RCC/", relocation_configration, name="relocation_configration"),
]

