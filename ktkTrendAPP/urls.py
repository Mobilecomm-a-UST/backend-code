from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
   
    path("makeKpiTrend/old/2G",views.G2_trend),
    path("makeKpiTrend/old/",views.old_ktk_trend),
    path("makeKpiTrend/pre_post/",views.pre_post_tech),

]