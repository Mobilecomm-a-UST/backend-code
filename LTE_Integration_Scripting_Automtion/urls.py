from django.urls import path
from LTE_Integration_Scripting_Automtion.views import *

urlpatterns = [
    path('Integration/generating_scripts/', generate_integration_script, name='integration_scripts')
]

