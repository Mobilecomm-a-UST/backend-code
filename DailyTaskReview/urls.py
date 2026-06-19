from django.urls import path
from .views import *






urlpatterns = [

    # add task in task table
    path('add-task/', add_task_to_table),
    path('get-task/', get_tasks_from_table),
    path('update-task/<int:pk>/', update_task_in_table),
    path('delete-task/<int:pk>/', delete_task_from_table),

    
#   ======= Assign Task API =======
    path('assign_task/create/', create_task),
    path('assign_task/get/', get_all_tasks),
    path('assign_task/update-task/<int:pk>/', update_task),
    path('assign_task/delete-task/<int:pk>/', delete_task),


#  ==========   My Task API  ==========
    path('mytask/get/', get_my_tasks),
    path('mytask/update/<int:pk>/', update_my_task),
    

]