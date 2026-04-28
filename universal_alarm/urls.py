from django.urls import path
from universal_alarm.views import *

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path( 'upload_4g/' ,upload_log_file  ),
    # path('upload_4g/', upload_log_file, ),
    path('upload_4g/', upload_4g_log_file, ),
    path('upload_5g/', upload_5g_log_file, ),
    path('upload_site/', upload_site_list, ),
    path('delete_site/', delete_site, ),
    path('get_site/', get_sites, ),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)