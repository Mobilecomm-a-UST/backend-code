from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
   
    path("upload/",views.upload_report),
    path("get_data/",views.graph_data), #  first 1 and 2 graphs total site allocated
    path("all_data/",views.circle_wise_vendor_comparision), # 3 graph /circle wise vandor camparision
    path("project_comparision/", views.project_comparision),  # 4th circle wise project comparision
    # path("projectWise_circle_comparision_pichart/",views.projectWise_circle_comparision_pichart),
    path("unique_column_value/", views.unique_coloumn_values),
    # path("pro_wise_partners_rank/",views.project_wise_partners_ranking_of_perticular_circle_and_month), # 1st dash board
    


]