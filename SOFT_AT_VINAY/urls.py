from django.urls import path
from SOFT_AT_VINAY.views import *

urlpatterns = [
    path('upload/',SoftAt_Report_Upload),
    path('create/',SoftAt_Report_create),
    path('view/',SoftAt_Circlewise_Dashboard),
    path('template/',get_soft_at_status_blank_template),
    path('view_report/',View_Soft_At_Report),
    path('weekly_comparision_dashboard/',weeklyComparision),
    path('ageing_count_changes/',SoftAt_Aging_Count),
    path('week_wise_accepted/',week_wise_accepted_sites),
    path('week_wise_pending/',ageing_wise_pending_sites),
    # path('date_wise_delete/', SoftAt_Delete_Report, name='softat-delete'),
    path('OverAll/', overallAcceptedRejected),
    path('week_ageing_wise_accepted_pending_sites/', week_ageing_wise_accepted_pending_sites),
    path('softAt-status-update-template/',softAt_status_upload_template_download, name='softAt_status_upload_template_download'),
    path('get-integration-circle/', get_integration_circle, name=' get_integration_circle'),
    path('softAt-offering-templates/', softAT_offering_template_download, name=' SoftAT_offering_template_download'),
    path('create-combination/', create_combination, name='one_time_code'),
    path('copying-oneday-record-to-next-day/', copying_oneday_record_to_next_day, name='just_for_now'),
    # path('update-offering-date',update_the_missing_offered_date, name='update_the_missing_offered_date'),
    path('hyperlink-circle-wise-dashboard/',hyperlink_circle_wise_dashboard, name='hyperlink-circle-wise-dashb'),
    path('edit-softat-report/<str:unique_key>/',edit_soft_at_report, name='edit_softat_report'),
    path('reset-to-previous-status/<str:unique_key>/',reset_to_previous_state, name='reset_softat_report'),
    path('complete-missing-data/',complete_missing_data, name='complete_missing_records'),
]