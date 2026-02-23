from django.urls import path
from degrowDismental.views import degrow_dismantle,get_Files,upload_msmf_data,upload_rfs_data,upload_locator_data,delete_single_file

urlpatterns = [
    path("upload/", degrow_dismantle, name="degrow_dismantle"),
    path("files/", get_Files, name="get_files"),
    path("upload_msmf/", upload_msmf_data, name="upload_msmf"),
    path("upload_mobinet/", upload_mobinet_data, name="upload_mobinet"),
    path("upload_aw_rfs/", upload_aw_rfs_data, name="upload_aw_rfs"),
    path("upload_aw_msmf/", upload_aw_msmf_data, name="upload_aw_msmf"),
    path("upload_rfs/", upload_rfs_data, name="upload_rfs"),
    path("upload_locator/", upload_locator_data, name="upload_locator"),
    path("delete_file/", delete_single_file, name="delete_file"),
    # path("data_fetch/", data_fetch, name="delete_file"),
    path("mobinet_data_fetch/", mobinet_data_fetch, name="mobinet_data_fetch"),
    path("mobinet_data_submit/", mobinet_data_submit, name="mobinet_data_submit"),
]