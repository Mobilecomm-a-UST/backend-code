"""performanceAT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('upload/',views.performanceAT_Report_Upload,name='AT'),
    path('view/',views.PerformanceAT_Circlewise_Dashboard),
    path("ownership_circlewise/",views.ownership_wise_pending_ageing),
    path("ownership_list/",views.ownership),
    path("site_list_request_handler/",views.site_list_request_handler),
    path("filter_by_tool_bucket/",views.filter_by_tool_bucket),


]
