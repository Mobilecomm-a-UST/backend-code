from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.HealthCheckView.as_view(), name="gpl-audit-health"),
    path("run/", views.RunGPLAuditView.as_view(), name="gpl-audit-run"),
    path(
        "download/<str:job_id>/",
        views.DownloadZipView.as_view(),
        name="gpl-audit-download-zip",
    ),
    path(
        "download-excel/<str:job_id>/",
        views.DownloadExcelView.as_view(),
        name="gpl-audit-download-excel",
    ),
]
