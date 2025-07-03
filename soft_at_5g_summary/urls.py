from django.urls import path
from .views import *

urlpatterns = [
      path("summary/", soft_at_5G_Summary_Ericsson, name="soft_at_soft_at_5g_summary_ericsson"),
      path("list/", soft_at_5G_checkpoint, name="soft_at_5G_checkpoint"),
]

