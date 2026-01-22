from django.urls import path
from Alarm_old_new_Tool.views import upload_4g_new_old,upload_5g_new_old


urlpatterns = [
    path('upload_4g/', upload_4g_new_old, ),
    path('upload_5g/', upload_5g_new_old, )
]
