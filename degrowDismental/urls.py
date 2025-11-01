from django.urls import path
from degrowDismental.views import degrow_dismantle,get_Files,upload_msmf_data,upload_rfs_data,upload_locator_data,delete_single_file

urlpatterns = [
    path("upload/", degrow_dismantle, name="degrow_dismantle"),
    path("files/", get_Files, name="get_files"),
    path("upload_msmf/", upload_msmf_data, name="upload_msmf"),
    path("upload_rfs/", upload_rfs_data, name="upload_rfs"),
    path("upload_locator/", upload_locator_data, name="upload_locator"),
    path("delete_file/", delete_single_file, name="delete_file"),

]