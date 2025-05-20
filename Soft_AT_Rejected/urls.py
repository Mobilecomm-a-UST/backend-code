from django.urls import path
from Soft_AT_Rejected.views import *

urlpatterns = [
    path('save_database',save_database),
   
    path('Soft_At_Rejected_Report',Soft_Rejection_Report),
    
   
    path('graph',graph_data),

    path('SoftAt_Circlewise_Rejected_Dashboard',SoftAt_Circlewise_Rejected_Dashboard),

    path('count_of_circle', count_of_circle),

    path('site_wise_view', site_wise_view),

    path('testing', testing),

    path("master_dashbord_api", master_dashbord_api),
    path("oem_wise_master_dashbord_api", oem_wise_master_dashbord),
    path("oem_wise_site_details_master_dashbord", oem_wise_site_details_master_dashbord),
    
    path("date_wise_offering_status", date_wise_offering_status),
    path("range_wise_rejected_site_count", range_wise_rejected_site_count),
    path("offered_date_wise_site_view", offered_date_wise_site_view),
  
    path("offered_date_wise_oemWise_site_count", offered_date_wise_oemWise_site_count),
    path("range_wise_rejected_remark", range_wise_rejected_remark),
    path("range_wise_rejected_remark", range_wise_rejected_remark),
    path("OverAllCircleWiseSummary", OverAllCircleWiseSummary),
    path("overall_oem_wise_circle_wise_summary", overall_oem_wise_circle_wise_summary),
    path("offer_date_wise_oem_wise_circle_wise_summary", offer_date_wise_oem_wise_circle_wise_summary),
    path("oem_wise_hyper_link_over_overall_circlewie", oem_wise_hyper_link_over_overall_circlewie_summary),

  
]