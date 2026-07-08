from django.urls import path
from .views import nokia_slicing_dump,upload_fix_parameter

urlpatterns = [
    path("fix_para_uls/", upload_fix_parameter),
    path("uls_slicing/",nokia_slicing_dump),

]
