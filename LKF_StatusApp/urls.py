from django.urls import path
from . import views

urlpatterns = [
    path('LKF_status/', views.LKF_Upload),
]

