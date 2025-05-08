from django.urls import path
from . import views

urlpatterns = [
    path('employee-skill-table', views.employee_skill_table),
    path('employee-skill-table/<str:id>/<str:remark>/', views.employee_skill_table_update),
    path('upload-excel/', views.upload_excel, name='upload_excel'),
    path('template/', views.get_excel_temp_link),
]



