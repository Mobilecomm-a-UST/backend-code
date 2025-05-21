from django.db import models
import re

class ExpectedParameter(models.Model):
    path = models.CharField(max_length=500)
    parameter_name = models.CharField(max_length=200)
    expected_value = models.CharField(max_length=500)

    # def normalize_path(self, path):
    #     path = path.strip().upper()
    #     path = re.sub(r'/+', '/', path)

    #     parts = path.split('/')
    #     normalized_parts = [p.split('-')[0] for p in parts if not p.startswith('PLMN')]

    #     return '/'.join(normalized_parts)


    # def save(self, *args, **kwargs):
    #     if self.path:
    #         self.path = self.normalize_path(self.path)
    #     if self.parameter_name:
    #         self.parameter_name = self.parameter_name.strip().lower()
    #     if self.expected_value:
    #         self.expected_value = self.expected_value.strip()
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.path} - {self.parameter_name}: {self.expected_value}"




class SummaryData(models.Model):
    MO_Class = models.CharField(max_length=500)
    Parameter = models.CharField(max_length=200)
   

    def __str__(self):
        return f"{self.MO_Class}-{self.Parameter}"

   
