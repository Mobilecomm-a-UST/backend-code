from django.urls import path
from . import views

urlpatterns = [
    path('linkfile/',views.upload_link_budget),
    path('microwave/', views.microwave_upload),
    path('get_delete/',views.get_delete_file),
    path('get_table/',views.final_excel_indb),
    path('auto_delete_avait/',views.auto_delete_reports)  
     
]
