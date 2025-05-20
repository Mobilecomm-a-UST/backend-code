from django.db import models

# Create your models here.
class ZTE_HR_Report(models.Model):
    Technology = models.CharField(max_length = 500, null=True)
    MO_FDD = models.CharField(max_length = 500, null=True)
    MO_TDD = models.CharField(max_length = 500, null=True)
    ZTE_parameter = models.CharField(max_length = 500, null=True)
    Parameter_type = models.CharField(max_length = 500, null=True)
    L2100 = models.CharField(max_length = 1000, null=True)
    L1800 = models.CharField(max_length = 1000, null=True)
    TD20 = models.CharField(max_length = 1000, null=True)
    Meascinfigindx = models.CharField(max_length = 500, null=True)
    Category = models.CharField(max_length = 500, null=True)
    Remarks = models.CharField(max_length = 500, null=True)


    def __str__(self):
        return self.Technology



