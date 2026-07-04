from django.urls import path
from .views import nokia_slicing_dump,upload_fix_parameter,get_users

urlpatterns = [
    path("fix_para/", upload_fix_parameter),
    path("slicing/",nokia_slicing_dump),

    path("get_users/",get_users)
]
