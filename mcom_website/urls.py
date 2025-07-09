"""mcom_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from trend import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    # path('',views.index,name="main"),
    path("trend/", include("trend.urls")),
    # path('trend/OriginalTrend/', include("Original_trend.urls")),
    path("accounts/", include("accounts.urls")),
    path("trend/bih/", include("Bihar_trend.urls")),
    path("trend/raj/", include("rajTrendAPP.urls")),
    path("trend/kol/", include("kolTrendAPP.urls")),
    path("vendor_management/", include("vendor_management.urls")),
    path("Soft_At/", include("SOFT_AT_VINAY.urls")),
    path("trend/hr/", include("hrTrendAPP.urls")),
    path("trend/ap/", include("apTrendAPP.urls")),
    path("trend/pb/", include("pbTrendAPP.urls")),
    path("trend/del/", include("delTrendAPP.urls")),
    path("trend/mp/", include("mpTrendAPP.urls")),
    path("trend/or/", include("orishaTrendAPP.urls")),
    path("Physical_At/", include("Physical_AT_APP.urls")),
    path("Performance_AT/", include("Performance_AT_APP.urls")),
    path("WPR_DPR2/", include("WPR_DPR2.urls")),
    path("Degrow/", include("Degrow.urls")),
    path("trend/OriginalTrend/", include("TNCHTrendAPP.urls")),
    path("trend/kol_degrow/", include("kol_degrow.urls")),
    path("merge_file/", include("Merged_APP.urls")),
    path("schedular/", include("scheduled_rna_Pld_alarm_app.urls")),
    path("trend/mum/", include("mumTrendAPP.urls")),
    path("trend/jk/", include("jkTrendAPP.urls")),
    path("trend/ktk/", include("ktkTrendAPP.urls")),
    path("trend/upw/", include("upwTrendAPP.urls")),
    path("trend/upe/", include("UE_degrow.urls")),
    path("testinAPP/", include("testingAPP.urls")),
    path("MDP/", include("MDP.urls")),
    path("panIndiaRnaPayloadAlarm/", include("panIndiaRnaPayloadAlarm.urls")),
    path("equipmentInventory/", include("equipmentInventory.urls")),
    path("MDP/UBR/", include("MDP_UBR.urls")),
    path("Scriptor/", include("Mcom_scriptor.urls")),
    path("softat_rej/", include("Soft_AT_Rejected.urls")),
    path("UBR_Soft_AT_Rej/", include("UBR_Soft_Phy_AT_Rejection_App.urls")),
    path("mailapp/", include("mailapp.urls")),
    path("/", include("mailapp.urls")),
    path("", include("Profile.urls")),
    path("UBR_Soft_Phy_AT/", include("UBR_Soft_Phy_AT_Rejection_App.urls")),
    path("Zero_Count_Rna_Payload_Tool/", include("Zero_Count_Rna_Payload_Tool.urls")),
    path("Degrow_HR_V2/", include("Degrow_HR_V2.urls")),
    path("Degrow_PB_V1/", include("Degrow_PB_V1.urls")),
    path("Audit_ZTE_HR/", include("Audit_ZTE_HR.urls")),
    path("MO_BASED_REPORT/", include("MO_BASED_REPORT.urls")),
    path("employee_skills/", include("employee_skills.urls")),
    path("IntegrationTracker/", include("IntegrationTracker.urls")),
    path("AUDIT_TOOL/", include("AUDIT_TOOL.urls")),
    path("RCA_TOOL/", include("RCA_TOOL.urls")),
    path("Degrow_PB_V2/", include("Degrow_PB_V2.urls")),
    path("NOM_AUDIT/", include("NOM_AUDIT.urls")),
    path("universal_alarm/", include("universal_alarm.urls")),
    path("dpr/sdir_status/", include("Daily_Alarm_Status.urls")),
    path("LKF/", include("LKF_StatusApp.urls")),
    path('soft_at_status/', include('soft_at_status_tech.urls')),
    path("gpl_audit/", include("gpl_audit_tool_V1_1.urls")),
    path("Soft_AT_Checklist_Ericsson/", include("Soft_AT_Checklist_Ericsson.urls")),
    path("Soft_AT_Checklist_Nokia/", include("Soft_AT_Checklist_Nokia.urls")),
    path("LTE/", include("LTE_Integration_Scripting_Automtion.urls")),
    path("soft_at_5g_summary/", include("soft_at_5g_summary.urls")),
    path ("soft_at_5g_checklist/", include("soft_at_5g_summary.urls")),
    path("twamp_ericsson/", include("twamp_ericsson.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

