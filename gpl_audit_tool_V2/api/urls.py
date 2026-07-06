from django.urls import path

from . import views

urlpatterns = [
    path("gpl-audit/health/", views.HealthCheckView.as_view(), name="gpl-audit-health"),
    path("gpl-audit/run/", views.RunGPLAuditView.as_view(), name="gpl-audit-run"),
    path(
        "gpl-audit/download/<str:job_id>/",
        views.DownloadZipView.as_view(),
        name="gpl-audit-download-zip",
    ),
    path(
        "gpl-audit/download-excel/<str:job_id>/",
        views.DownloadExcelView.as_view(),
        name="gpl-audit-download-excel",
    ),
]
