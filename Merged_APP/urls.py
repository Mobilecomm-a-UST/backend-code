
from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.urls import path,include
from .import views
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


from django.contrib import admin
from django.urls import path,include
# from .views import merge_csv_files
from . import views
urlpatterns = [
   
    path("excel",views.merge_App),
]