from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmployeeViewSet,
    DriveTestSurveyViewSet,
    DailyTrackingViewSet,
    EmployeeDatewiseViewSet,
    UploadFileView,
    ExportExcelView,
    ExportDateRangeView,
    AnalyticsView,
    DateSummaryView,
    CircleSummaryView,
    DepartmentSummaryView,
    SkillSummaryView,
    ProjectSummaryView,
    EmployeeSearchView,
    ReportingManagerSummaryView,
    IdleEmployeesView,
    WorkingEmployeesView,
    AvailableDatesView,
    DashboardView,
    DateRangeView,
)

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'surveys', DriveTestSurveyViewSet)
router.register(r'daily', DailyTrackingViewSet, basename='daily')
router.register(r'employeedatewise', EmployeeDatewiseViewSet, basename='employeedatewise')

urlpatterns = [
    path('', include(router.urls)),

    path('upload/', UploadFileView.as_view(), name='upload'),
    path('export/', ExportExcelView.as_view(), name='export'),
    path('export/daterange/', ExportDateRangeView.as_view(), name='export-daterange'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
    path('date-summary/', DateSummaryView.as_view(), name='date-summary'),
    path('circle-summary/', CircleSummaryView.as_view(), name='circle-summary'),
    path('dept-summary/', DepartmentSummaryView.as_view(), name='dept-summary'),
    path('skill-summary/', SkillSummaryView.as_view(), name='skill-summary'),
    path('project-summary/', ProjectSummaryView.as_view(), name='project-summary'),
    path('search/', EmployeeSearchView.as_view(), name='search'),
    path('manager-summary/', ReportingManagerSummaryView.as_view(), name='manager-summary'),
    path('idle/', IdleEmployeesView.as_view(), name='idle'),
    path('working/', WorkingEmployeesView.as_view(), name='working'),
    path('dates/', AvailableDatesView.as_view(), name='dates'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path("date-range/", DateRangeView.as_view(), name="date-range"),
]