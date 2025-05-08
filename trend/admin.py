from django.contrib import admin

# Register your models here.
from .models import DPR_table1,DPR_update_status,DPR_file,performance_at_table

# # Register your models her
admin.site.register(DPR_table1 )
admin.site.register(DPR_update_status)
admin.site.register(DPR_file)
admin.site.register(performance_at_table)
