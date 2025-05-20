from django.urls import path, include
from Zero_Count_Rna_Payload_Tool.views import *
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('level1',level1View )
router.register('level2',level2View )
router.register('level3',level3View ) 
router.register('level4',level4View )

router.register('thershold',ThresholdView)

urlpatterns = [
    path("save_database_4G", save_database_RAW_4G),
    path("Daily_RAW_KPI_4G", Daily_RAW_KPI_4G),
    path("template", template_links),
    path("Daily_RAW_KPI_2G", Daily_RAW_KPI_2G),
    path("kpi_trend_4g_api", kpi_trend_4g_api),
    path("kpi_trend_2g_api", kpi_trend_2g_api),
    path("master-dashboard_api/", Master_Dashboard_api),
    path(
        "circle_based_rna_count/", circle_based_rna_count, name="circle_based_rna_count"
    ),
    path("Date_Wise_Dashboard/", Date_Wise_Dashboard, name="Date_Wise_Dashboard"),
    path(
        "hyperlink_Date_wise_dashboard/",
        hyperlink_Date_wise_dashboard,
        name="hyperlink_Date_wise_dashboard",
    ),
    path(
        "hyperlink_circle_based_rna_count/",
        hyperlink_circle_based_rna_count,
        name="hyperlink_circle_based_rna_count",
    ),
    path(
        "Week_Wise_Dashboard/",
        Week_Wise_Dashboard,
        name="Week_Wise_Dashboard",
    ),
    path(
        "Hyperlink_Week_Wise_Dashboard/",
        Hyperlink_Week_Wise_Dashboard,
        name="Hyperlink_Week_Wise_Dashboard",
    ),
    path(
        "hyperlink_week_to_week_all/",
        hyperlink_week_to_week_all,
        name="hyperlink_week_to_week_all", 
    ),
    path(
        "hyperlink_day_to_day_all/",
        hyperlink_day_to_day_all,
        name="hyperlink_day_to_day_all",
    ),
    path(
        "ticket_counter_api/",
        ticket_counter_api,
        name="ticket_counter_api",
    ),
    path(
        "hyperlink_Date_wise_dashboard/",
        hyperlink_Date_wise_dashboard,
        name="hyperlink_Date_wise_dashboard",
    ),
    path(
        "ms1_site_deletion/",
        ms1_site_deletion,
        name="ms1_site_deletion",
    ),
    path(
        "ticket_counter_hyperlink_data/",
        hyperlink_Date_wise_dashboard_payload_dip,
        name="hyperlink_dashboard",
    ),
    # path(
    #     "ticket_counter_upload_report/",
    #     ticket_counter_upload_report,
    #     name="ticket_counter_upload_report",
    # ),
    path(
        "get_ticket_status_data/",
        get_ticket_status_data,
        name="get_ticket_status_data",
    ),
    path(
        "ticket_status_open_close/",
        ticket_status_open_close,
        name="ticket_status_open_close",
    ),
    path(
        "ticket_status_open_close/<str:ticket_id>/",
        ticket_status_open_close,
        name="ticket_status_open_close",
    ),
    path(
        "circle_wise_open_close_dashboard/",
        circle_wise_open_close_dashboard,
        name="circle_wise_open_close_dashboard",
    ),
    path(
        "get_data_from_url/",
        get_data_from_url,
        name="get_data_from_url",
    ),
    path(
        "get_category/",
        get_unique_category,
        name="category-list",
    ),

    path("get_daily_4g_kpi_report_by_date_and_kpi/",get_daily_4g_kpi_report_by_date_and_kpi,name="get_daily_4g_kpi_report_by_date"),
    path("data/", include(router.urls)),
]
