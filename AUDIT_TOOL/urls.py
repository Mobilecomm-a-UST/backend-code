from django.urls import path
from . import views
urlpatterns = [
 path('api/tasks/', views.TaskList.as_view(), name='task-list'),
 path('2G_AUDIT/', views.audit_2g),
 path('dashboard/', views.dashboard),
]
