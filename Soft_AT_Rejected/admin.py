from django.contrib import admin
from Soft_AT_Rejected.models import *

# Register your models here.

class RejectionRearksAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Rejection_Remarks._meta.fields]
    list_filter =[field.name for field in Rejection_Remarks._meta.fields]


class Circle_Responsible_Spoc_Admin(admin.ModelAdmin):
    list_display = [field.name for field in Circle_Responsible_Spoc._meta.fields]


class Centeral_Responsible_Spoc_Mail_Admin(admin.ModelAdmin):
    list_display = [field.name for field in Centeral_Responsible_Spoc_Mail._meta.fields]



class Central_Management_Admin(admin.ModelAdmin):
    list_display = [field.name for field in Central_Management._meta.fields]

class Circle_PM_Admin(admin.ModelAdmin):
    list_display = [field.name for field in Circle_PM._meta.fields]


class Soft_AT_Rejection_Mail_Saved_Status_Admin(admin.ModelAdmin):
    list_display = [field.name for field in Soft_AT_Rejection_Mail_Saved_Status._meta.fields]

class Soft_AT_NOKIA_Rejected_Table_Admin(admin.ModelAdmin):
    list_display = [field.name for field in Soft_AT_NOKIA_Rejected_Table._meta.fields]

class Soft_AT_SAMSUNG_Rejected_Table_Admin(admin.ModelAdmin):
    list_display = [field.name for field in Soft_AT_SAMSUNG_Rejected_Table._meta.fields]


class Soft_AT_ERI_Rejected_Table_Admin(admin.ModelAdmin):
    list_display = [field.name for field in Soft_AT_ERI_Rejected_Table._meta.fields]

class Soft_AT_HUAWEI_Rejected_Table_Admin(admin.ModelAdmin):
    list_display = [field.name for field in Soft_AT_HUAWEI_Rejected_Table._meta.fields]

class Soft_AT_ZTE_Rejected_Table_Admin(admin.ModelAdmin):
    list_display = [field.name for field in Soft_AT_ZTE_Rejected_Table._meta.fields]


admin.site.register(Rejection_Remarks, RejectionRearksAdmin)
admin.site.register(Centeral_Responsible_Spoc_Mail, Centeral_Responsible_Spoc_Mail_Admin)
admin.site.register(Circle_Responsible_Spoc,Circle_Responsible_Spoc_Admin)
admin.site.register(Central_Management, Central_Management_Admin)
admin.site.register(Circle_PM, Circle_PM_Admin)
admin.site.register(Soft_AT_NOKIA_Rejected_Table, Soft_AT_NOKIA_Rejected_Table_Admin)
admin.site.register(Soft_AT_SAMSUNG_Rejected_Table, Soft_AT_SAMSUNG_Rejected_Table_Admin)
admin.site.register(Soft_AT_ERI_Rejected_Table, Soft_AT_ERI_Rejected_Table_Admin)
admin.site.register(Soft_AT_HUAWEI_Rejected_Table, Soft_AT_HUAWEI_Rejected_Table_Admin)
admin.site.register(Soft_AT_ZTE_Rejected_Table, Soft_AT_ZTE_Rejected_Table_Admin)
admin.site.register(Soft_AT_Rejection_Mail_Saved_Status, Soft_AT_Rejection_Mail_Saved_Status_Admin)
