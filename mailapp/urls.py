from django.urls import path
from mailapp.views import send_email_view


urlpatterns = [
    path("", send_email_view, name="mail"),
]
