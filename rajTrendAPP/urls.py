from django.urls import path
from . import views


urlpatterns = [
   path("makeKpiTrend/old",views.old_raj_trend),
   path("makeKpiTrend/4g",views.KpiTrend_4g, name="KpiTrend_4g"),
   path("makeKpiTrend/2g",views.KpiTrend_2g, name="KpiTrend_2g"),

]