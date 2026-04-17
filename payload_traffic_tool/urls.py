from django.urls import path
from .views import *


urlpatterns = [
    path('upload4g/',upload_4g_payload),
    path('upload5g/',upload_5g_payload),
    path('get_traffic/',get_traffic),
    path('get_history/',get_history),

    path('4g_delete/',delete_data_4g),
    path('5g_delete/',delete_data_5g),
    path('delete_history/',delete_history)
 
]