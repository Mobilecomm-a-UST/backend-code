from django.db import models

# Create your models here.

class DismantleModelData(models.Model):
    zone = models.CharField(max_length=100, null=True, blank=True)
    site_id = models.CharField(max_length=100, null=True, blank=True)
    approval_date = models.DateField(null=True, blank=True)
    model_name = models.CharField(max_length=100, null=True, blank=True)
    expected_quantity = models.IntegerField(null=True, blank=True)
    serial_number = models.CharField(max_length=100, null=True, blank=True)
    is_found = models.BooleanField(default=False)
    is_in_mobinet = models.BooleanField(default=True)
    srn_number = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.CharField(max_length=500, null=True, blank=True)
    
    class Meta:
        db_table = "dismantle_model_data"
        indexes = [
            models.Index(fields=["zone"]),
            models.Index(fields=["site_id"]),
        ]

    def __str__(self):
        return f"{self.zone} - {self.site_id}"
    
    

class DismantleCircleData(models.Model):
    circle = models.CharField(max_length=100, null=True, blank=True)
    site_id = models.CharField(max_length=100, null=True, blank=True)
    is_approved = models.DateField(null=True, blank=True)
    is_surveyed = models.DateField(null=True, blank=True)
    is_srn_done = models.DateField(null=True, blank=True)
    remarks = models.CharField(max_length=500, null=True, blank=True)
    
    class Meta:
        db_table = "dismantle_circle_data"
        unique_together = ("circle", "site_id")
        indexes = [
            models.Index(fields=["circle"]),
            models.Index(fields=["site_id"]),
        ]

    def __str__(self):
        return f"{self.circle} - {self.site_id}"