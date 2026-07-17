from django.urls import path
from .views import *

urlpatterns = [
    path('api/monthly-report/upsert/', MonthlyReportUpsertView.as_view()),
    path('api/monthly-report/bulk-upsert/',  MonthlyReportBulkUpsertView.as_view()),
    path('template/',get_excel_temp_link , name='get_excel_temp_link'),
    path('resource/bulk-upload/',  EmployeeBulkUploadView.as_view()),
    path("employees/", EmployeeListView.as_view()),
    path("graph-report/", GraphData.as_view()),
    path("admin-table/", AdminTable.as_view()),
]