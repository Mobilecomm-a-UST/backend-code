from django.contrib import admin
from django.urls import path
from Physical_AT_APP.views import *

urlpatterns = [
   path('upload/',Physical_At_Report_Upload),
   path('view/',Physical_Circlewise_Dashboard),
  
]