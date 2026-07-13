from django.urls import path
from .views import *






urlpatterns = [

    # add task in task table
    path('add-task/', add_task_to_table),
    path('get-task/', get_tasks_from_table),
    path('update-task/<int:pk>/', update_task_in_table),
    path('delete-task/<int:pk>/', delete_task_from_table),

    # Reporting Email Hierarchy
    path('reporting-email-hierarchy/create/', add_email_hierarchy),
    path('reporting-email-hierarchy/get/', get_email_hierarchy),
    path('reporting-email-hierarchy/update/<int:pk>/', update_email_hierarchy),
    path('reporting-email-hierarchy/delete/<int:pk>/', delete_email_hierarchy),

# ========== Task Template API ==========
    path('task-template/create/', create_template),
    path('task-template/get/', get_all_templates),
    path('task-template/update/<int:pk>/', update_template),
    path('task-template/delete/<int:pk>/', delete_template),
    path('task-template/status/<int:pk>/', change_template_status),

    
#   ======= Assign Task API =======
    path('assign_task/create/', create_task),
    path('assign_task/get/', get_all_tasks),
    path('assign_task/update-task/<int:pk>/', update_task),
    path('assign_task/delete-task/<int:pk>/', delete_task),
    path('assign_task/reassign/<int:pk>/', reassigned_task),


#  ==========   My Task API  ==========
    path('mytask/get/', get_my_tasks),
    path('mytask/update/<int:pk>/', update_my_task),

#  ==========  Assign Task Dashboard API  ==========

    path('analytics/assigned/', get_user_wise_analytics),

# ==========  MYTask Dashboard API  ==========

    path('analytics/mytasks/', get_my_tasks_analytics),
    

]