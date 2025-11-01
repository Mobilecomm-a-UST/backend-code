from django.urls import path
from .views import relocationView, referenceView


urlpatterns = [
    path('relocation/', relocationView, name='relocationView'),
    path('reference/', referenceView, name='referenceView'),
]