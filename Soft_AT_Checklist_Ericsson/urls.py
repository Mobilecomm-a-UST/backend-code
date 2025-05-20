from django.urls import path
from .views import *

urlpatterns = [
      path("soft_at_checkpoint/", soft_at_checkpoint, name="soft_at_checkpoint"),
]

