from django.contrib import admin
from django.urls import path,include
from Bihar_trend import views
urlpatterns = [
   
    path("makeKpiTrend/old/smallcell",views.old_bih_trend_smallcell),
    path("makeKpiTrend/old/macro",views.old_bih_trend_macro),
    path("makeKpiTrend/old/degrow",views.old_bih_trend_degrow),
    


]