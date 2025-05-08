from django.contrib import admin
from RCA_TOOL.models import *
# Register your models here.

class RCA_TABLE_Admin(admin.ModelAdmin):
    list_display = [field.name for field in RCA_TABLE._meta.fields]
    ordering = ['id']


class KPI_TABLE_Admin(admin.ModelAdmin):
    list_display = [field.name for field in KPI_TABLE._meta.fields]
    ordering = ['id']




admin.site.register(RCA_TABLE, RCA_TABLE_Admin)

admin.site.register(KPI_TABLE, KPI_TABLE_Admin)
admin.site.register(RCA_payload_table)