from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()
# router.register(r'tracker', Relocation_trackerViewSet)

urlpatterns = [
    path("upload/",upload_excel),
    path('datewise-integration-data/', datewise_integration_data, name='datewise-integration-data'),
    path('monthwise-integration-data/', monthwise_integration_data, name='monthwise-integration-data'),
    path('template/',get_excel_temp_link , name='get_excel_temp_link'),
    path('monthly-oemwise-integration-data/',monthly_oemwise_integration_data),
    path('hyperlink-monthly-oemwise-integration-data/',hyperlink_monthly_oemwise_integration_data),
    path('hyperlink-datewise-integration-data/',hyperlink_datewise_integration_data),
    path('hyperlink-monthwise-integration-data/',hyperlink_monthwise_integration_data),
    path('hyperlink-hyperlink-monthwise-integration-data/',hyperlink_hyperlink_monthly_oemwise_integration_data),
    path('overall-record-summary/',overall_record_summary),
    path('date-range-integration-data/',date_range_wise_integration_data),
    path('hyperlink-date-range-integration-data/',hyperlink_date_range_integration_data),
    path('delete-integration-record/<int:pk>/', delete_integration_record, name='delete_my_model'),
    path('edit-integration-record/<int:id>/',integration_table_update, name='update_my_model'),
    path('oem_wise_integration_data/',overall_integration_for_perticular_oem),
    
    # relocation apis
    path('relocation/tracker/',Relocation_trackerViewSet.as_view() ),
   
    path('New_site_locked_unlocked_date/',New_site_locked_unlocked_dateView.as_view() ),
    path('old_site_locked_unlocked_date/',old_site_locked_unlocked_dateView.as_view() ),
   
    path("upload-relocation-excel/", upload_relocation_excel, name="upload_relocation_excel"),
    path('relocation-template/',get_relocation_excel_temp_link , name='get_relocation_excel_temp_link'),
    path('get_old_site_locked_unlocked_date/',get_old_site_locked_unlocked_date ),
    path('get_new_site_locked_unlocked_date/',get_new_site_locked_unlocked_date ),
]