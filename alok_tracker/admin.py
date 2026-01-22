from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(RelocationUser)
class RelocationUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'circles', 'columns', 'right', 'updated_by', 'updated_at', 'created_by', 'created_at')
    search_fields = ('name', 'email')
    readonly_fields = ('updated_by', 'updated_at', 'created_by', 'created_at')
    list_filter = ('right', 'circles', 'columns')
    
    

@admin.register(RelocationIssue)
class RelocationIssuesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'circle',
        'site_id',
        'milestone',
        'issue_name',
        'issue_owner',
        'start_date',
        'close_date',
        'status',
        'duration',
        'updated_by',
        'updated_at',
        'created_by',
        'created_at',
    )

    search_fields = ('site_id',)

    list_filter = ( 'circle', 'milestone', 'issue_owner', 'issue_name', 'site_id', 'status',)

    readonly_fields = ('updated_by', 'updated_at', 'created_by', 'created_at', 'duration', 'status', )
