from django.db import models
import re

class ExpectedParameter(models.Model):
    path = models.CharField(max_length=500)
    parameter_name = models.CharField(max_length=200)
    expected_value = models.CharField(max_length=500)

  
    def __str__(self):
        return f"{self.path} - {self.parameter_name}: {self.expected_value}"

class MOData(models.Model):
    mo_class = models.CharField(max_length=500)  # stores strings like "MRBTS/.../EAC_IN-1 TO MRBTS/.../EAC_IN-4"
    parameter = models.CharField(max_length=100)  # 'descr', 'polarity', 'value' etc
    value = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.mo_class} - {self.parameter}"


class SummaryData(models.Model):
    MO_Class = models.CharField(max_length=500)
    Parameter = models.CharField(max_length=200)
   

    def __str__(self):
        return f"{self.MO_Class}-{self.Parameter}"
    



   
