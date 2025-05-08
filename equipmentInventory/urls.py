from django.contrib import admin
from django.urls import path,include
from equipmentInventory import views
urlpatterns = [
   
    path("equipment_upload/",views.equipment_inventory_upload),
    path("create_equipment_inventry/",views.create_equipment_inventry),
    path("delete_equipment_inventry/<int:id>",views.delete_equipment_inventry),
    path("update_equipment_inventry/<int:id>",views.update_equipment_inventry),
    path("equpment_inventory_data/",views.equpment_inventory_data),

    


]