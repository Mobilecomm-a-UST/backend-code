from django.urls import path
from Original_trend import views


urlpatterns = [
   path("tnch/KpiTrend/",views.tnch_Trend),
   path("makeKpiTrend/old",views.old_tnch_Trend_v3),
   path("tnch/pre_post_upload_7/",views.tnch_pre_post_upload_7),
   path("tnch/raw_kpi_upload/",views.raw_Kpi_upload),
   path("tnch/integrated_sites",views.get_integ_site_list),


    
]