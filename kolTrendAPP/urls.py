from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
   
    path("makeKpiTrend/old/uls",views.old_kol_trend_uls),
    path("makeKpiTrend/old/sam",views.old_kol_trend_sam),
    path("makeKpiTrend/old/relocation",views.old_kol_trend_relocation),
    path("makeKpiTrend/old/gsm",views.old_kol_trend_gsm_2g),
]