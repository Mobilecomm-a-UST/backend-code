# from django.db import models
# # Create your models here.
# class MobinetDump(models.Model):
#     node_type = models.CharField(max_length=100, db_column='Node type', null=True, blank=True)
#     object_id = models.CharField(max_length=100, db_column='Object ID', null=True, blank=True)
#     object_name = models.CharField(max_length=100, db_column='Object Name', null=True, blank=True)
#     model = models.CharField(max_length=100, db_column='Model', null=True, blank=True)
#     parent_site = models.CharField(max_length=100, db_column='Parent Site', null=True, blank=True)
#     zone = models.CharField(max_length=100, db_column='Zone', null=True, blank=True)
#     cabinet = models.CharField(max_length=100, db_column='Cabinet', null=True, blank=True)
#     cabinet_type = models.CharField(max_length=100, db_column='Cabinet Type', null=True, blank=True)
#     cabinet_part_number = models.CharField(max_length=100, db_column='Cabinet Part Number', null=True, blank=True)
#     cabinet_sn = models.CharField(max_length=100, db_column='Cabinet SN', null=True, blank=True)
#     shelf = models.CharField(max_length=100, db_column='Shelf', null=True, blank=True)
#     shelf_type = models.CharField(max_length=100, db_column='Shelf Type', null=True, blank=True)
#     ru_index = models.CharField(max_length=100, db_column='RU Index', null=True, blank=True)
#     shelf_manufacturer = models.CharField(max_length=100, db_column='Shelf Manufacturer', null=True, blank=True)
#     shelf_part_number = models.CharField(max_length=100, db_column='Shelf Part Number', null=True, blank=True)
#     shelf_sn = models.CharField(max_length=100, db_column='Shelf SN', null=True, blank=True)
#     slot = models.CharField(max_length=100, db_column='Slot', null=True, blank=True)
#     index_on_slot = models.CharField(max_length=100, db_column='Index On Slot', null=True, blank=True)
#     board_type = models.CharField(max_length=100, db_column='Board Type', null=True, blank=True)
#     category = models.CharField(max_length=100, db_column='Category', null=True, blank=True)
#     board_model = models.CharField(max_length=100, db_column='Board Model', null=True, blank=True)
#     board_manufacturer = models.CharField(max_length=100, db_column='Board Manufacturer', null=True, blank=True)
#     board_manufacturing_date = models.CharField(max_length=100, db_column='Board Manufacturing Date', null=True, blank=True)
#     board_part_number = models.CharField(max_length=100, db_column='Board Part Number', null=True, blank=True)
#     board_serial_number = models.CharField(max_length=100, db_column='Board Serial Number', null=True, blank=True)
#     type_category = models.CharField(max_length=100, db_column='Type Category', null=True, blank=True)
#     technology = models.CharField(max_length=100, db_column='Technology', null=True, blank=True)
#     serial_number = models.CharField(max_length=100, db_column='Serial Number', null=True, blank=True)
#     insert_date = models.CharField(max_length=100, db_column='Insert Date', null=True, blank=True)
#     update_date = models.CharField(max_length=100, db_column='Update Date', null=True, blank=True)
#     hardware_version = models.CharField(max_length=100, db_column='Hardware Version', null=True, blank=True)

 
#     def __str__(self):
#         return f"{self.parent_site} | {self.object_name}"
 