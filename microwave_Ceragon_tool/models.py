from django.db import models

class Microwavepara(models.Model):
    idu_model= models.CharField(max_length=50,null=True,blank=True)
    parameter = models.CharField(max_length=200)
    value = models.TextField()

    def __str__(self):
        return f"{self.idu_model} - {self.parameter}"