from django.db import models

class Microwavepara(models.Model):
    parameter= models.CharField(max_length=50, null=True, blank=True)
    value =    models.CharField(max_length=50, null=True, blank=True)
    class Meta:
        db_table = "microwave_ceragone_parameter"
     

    def __str__(self):
        return self.parameter
