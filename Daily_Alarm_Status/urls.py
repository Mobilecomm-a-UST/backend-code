from django.urls import path
from Daily_Alarm_Status.views import process_sdir_and_rru_status

urlpatterns = [
    path('', process_sdir_and_rru_status, name='process sdir command process')
]
