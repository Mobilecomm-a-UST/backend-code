from django.urls import path
from . import views


urlpatterns = [
   path("makeKpiTrend/zte/old",views.old_pb_trend),
   path('makeKpiTrend/nok/smallcell/old',views.old_pb_nok_smallcell_trend),
   path('makeKpiTrend/nok/hpsccell/old',views.old_pb_nok_hpsccell_trend)
  


    
]