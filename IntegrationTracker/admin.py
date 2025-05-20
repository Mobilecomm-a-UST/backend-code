from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Document)

admin.site.site_header = "NPN Technologies Admin"