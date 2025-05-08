from django.urls import path
from Profile.models import *
from Profile.views import *

urlpatterns = [
    path("profile/<str:employee_name>/", get_profile_data),
    path("profileSetting/<str:employee_name>/", update_profile_data),
    path("get_user_circle", get_user_circle),
    path("data",data),
]
