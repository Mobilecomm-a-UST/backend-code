from django.urls import path
from Soft_AT_APP.views import *

urlpatterns = [
    path('upload/',SoftAt_Report_Upload),
    path('view/',SoftAt_Circlewise_Dashboard),
    path('template/',softAtTemplate),
    path('view_report/',View_Soft_At_Report),
    path('weekly_comparision_dashboard/',weeklyComparision),
    
]