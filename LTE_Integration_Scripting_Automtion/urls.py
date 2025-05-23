from django.urls import path
from LTE_Integration_Scripting_Automtion.views import *

<<<<<<< HEAD

urlpatterns = [
    path(
        "generating_scripts/",
        generate_integration_script,
        name="GENERATE_LTE_INTEGRATION_SCRIPT",
    )
=======
urlpatterns = [
    path('Integration/generating_scripts/', generate_integration_script, name='integration_scripts')
>>>>>>> vinay_duke_work
]
