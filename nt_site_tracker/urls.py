from django.urls import path 
from nt_site_tracker.views import *

urlpatterns = [
    path("upload_file/", upload_tracker_data_view, name="upload_tracker_data"),
    path("download_tracker_file/", download_tracker_data_view, name="download_tracker_data"),
    path("delete_tracker_data/", delete_tracker_data_view, name="delete_tracker_data"),
    path("daily_dashboard_file/", daily_dashboard_view, name="daily_dashboard"),
    path("weekly_monthly_dashboard_file/", weekly_monthly_dashboard_view, name="weekly_mpnthly_dashboard"),
    path("gap_view/", gap_view, name="GAP"),

    path("hyperlink_frontend_editing/",frontend_nt_display_view),
    path("frontend_nt_update_view/",frontend_nt_update_view),

    path("update_nt_template/",updtae_nt_template),
    path("delete_nt_data/",delete_nt_tracker),
    path("delete_ntissue/",delete_ntissue),
    
    path("ms1_ageing_dashboard_table1/", ms1_ageing_dashboard_table1, name="ms1_ageing_dashboard_table1"),
    path("ms1_ageing_dashboard_table2/", ms1_ageing_dashboard_table2, name="ms1_ageing_dashboard_table2"),
    path("graphs/", graphs_view, name="graphs"),
    path("monthly_graph/", monthly_graph, name="monthly_graph"),
    
    

    path("lifecycle_display/", lifecycle_display, name="lifecycle_display"),
    path("issue_timeline_display/", issue_timeline_display, name="issue_timeline"),
    path("issue_timeline_add/", issue_timeline_add, name="issue_timeline_add"),
    path("issue_timeline_update/", issue_timeline_update, name="issue_timeline_update"),
    path("issue_timeline_delete/", issue_timeline_delete, name="issue_timeline_delete"),
    #changes done --

     
    #ms2----------- # changes start--


    path("ms2_daily_dashboard/", ms2_daily_waterfall, name="ms2_daily_dashboard"),
    path("ms2_weekly_monthly_dashboard/", ms2_weekly_monthly_waterfall, name="ms2_weekly_monthly_dashboard"),    

    path("ms2_ageing_dashboard_table1/", ms2_ageing_dashboard_table1, name="ms2_ageing_dashboard_table1"),
    path("ms2_ageing_dashboard_table2/", ms2_ageing_dashboard_table2, name="ms2_ageing_dashboard_table2"),
    path("ms2_graphs/", ms2_graphs_view, name="graphs"),
    path("ms2_monthly_graph/", ms2_monthly_graph, name="monthly_graph"),

#add new api-
    path("nt_issue_summary/",nt_issue_summary),
    path("upload_nt_issue/",upload_nt_issue_view),
    path("sync_nt_site_status",sync_nt_site_status),
    path("nt_issue_frontend_hyperlink/",nt_issue_summary_frontend),
    path("nt_aging_frontend_hyperlink/",ageing_dashboard_hyperlink)
]

