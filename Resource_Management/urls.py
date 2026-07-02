# from django.urls import path
# from .views import *

# urlpatterns = [
#     path("Details/",rru_details_upload, name="RRU_Details"),
# ]


from django.urls import path
from .views import *

urlpatterns = [
    path('api/monthly-report/upsert/', MonthlyReportUpsertView.as_view()),
    path('api/monthly-report/bulk-upsert/',  MonthlyReportBulkUpsertView.as_view()),
    path('template/',get_excel_temp_link , name='get_excel_temp_link'),
]