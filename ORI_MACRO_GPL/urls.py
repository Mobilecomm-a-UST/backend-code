from django.urls import path
from .views import nokia_slicing_dump,upload_fix_parameter

urlpatterns = [
    path("fix_para/", upload_fix_parameter),
    path("ori_slicing/",nokia_slicing_dump),

]
