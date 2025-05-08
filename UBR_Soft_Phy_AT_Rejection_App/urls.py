from django.urls import path
from UBR_Soft_Phy_AT_Rejection_App.views import *

urlpatterns = [
    path('save_database',save_database),
    path('Soft_Phy_Rejection_Report', Soft_Phy_Rejection_Report),
    path('count_of_circle', count_of_circle),
    path('site_wise_view', site_wise_view),
    path('master_dashbord_api', master_dashbord_api),
    path('oem_wise_master_dashbord_api', oem_wise_master_dashbord),
    path('oem_wise_site_details_master_dashbord', oem_wise_site_details_master_dashbord),
    path('date_wise_offering_status', date_wise_offering_status),
    path('offered_date_wise_site_view', offered_date_wise_site_view),
    path('offered_date_wise_oemWise_site_count', offered_date_wise_oemWise_site_count),
    path('OverAllCircleWiseSummary', OverAllCircleWiseSummary),
    path('offer_date_wise_oem_wise_circle_wise_summary', offer_date_wise_oem_wise_circle_wise_summary),
    path('oem_wise_hyper_link_over_overall_circlewie', oem_wise_hyper_link_over_overall_circlewie_summary),
    path('overall_oem_wise_circle_wise_summary', overall_oem_wise_circle_wise_summary),
    path('range_wise_rejected_site_count', range_wise_rejected_site_count),
    path('range_wise_rejected_remark', range_wise_rejected_remark),
]