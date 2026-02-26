from django.urls import path
from degrowDismental.views import *

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
    path("mobinet_data_fetch_from_file/", mobinet_data_fetch_from_file, name="mobinet_data_fetch_from_file"),
    path("mobinet_data_submit_central/", mobinet_data_submit_by_central, name="mobinet_data_submit"),
    path("fetch_site_status/", fetch_site_status, name="fetch site status"),
    path("empty_my_model/", empty_my_model, name="empty_my_model"),
]