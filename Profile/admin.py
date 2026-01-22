from django.contrib import admin
from Profile.models import *

# Register your models here.
admin.site.register(ProfileModel)
# admin.site.register(userCircle)

class UserCircleAdmin(admin.ModelAdmin):
    list_display = ('user', 'Circle', 'user_catagory')  # Display all fields
    list_filter = ('user__username', 'Circle', 'user_catagory')  # Add filters for all fields
    search_fields = ('user__username', 'Circle', 'user_catagory')  # Add search option for specified fields

admin.site.register(userCircle, UserCircleAdmin)