from django.contrib import admin
from django.urls import path,include
from .views import *
# suffix url should be : vendor_management
# urlpatterns = [
#     path("",circle_progress_report_upload),
#     path("view_report/circle",circle_team_report_view),
#     path("op1",vendor_po_eligible_upload),
#     path("view",Progress_report_view),
#     path("po_eligible_report_view",po_eligible_report_view),
#     path("vendor_po_No_upload",vendor_po_No_upload),

    
 

# ]


urlpatterns = [
    path("circle_team/upload/",circle_progress_report_upload),  #vendor_management/
    path("circle_team/view",circle_team_report_view),           #vendor_management/view_report/circle new

    path("po_approval/view",po_approval_view),              #vendor_management/view
    path("po_approval/upload",po_approval_upload),       #vendor_management/op1

    path("allocate_po/view",allocate_po_view),           #vendor_management/po_eligible_report_view
    path("allocate_po/upload",allocate_po_upload),             #vendor_management/vendor_po_No_upload
    path("circle_list",get_circle_list),        
    ]