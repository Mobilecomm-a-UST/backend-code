from django.urls import path
from .views import *

urlpatterns = [

    # Daily task review
    path('create/', create_daily_task_review),
    path('reviews/', get_daily_task_reviews),
    path('get_users/',get_users),
    path('fatch_username/',fatch_username),
    
     # Task CRUD
    path('tasks/create/', create_task),
    path('tasks/', get_tasks),
    path('tasks/<int:pk>/', get_task),
    path('tasks/update/<int:pk>/', update_task),
    path('tasks/delete/<int:pk>/', delete_task),

    # Overall data
    path('all-data/', get_all_data),
]