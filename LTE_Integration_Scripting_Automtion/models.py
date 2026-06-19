from django.db import models

# Create your models here.

class LTELogTable(models.Model):
    Site_ID = models.CharField(max_length=500)
    User_ID = models.EmailField(max_length=254)
    CIRCLE =  models.CharField(max_length=500)
    output_file_path = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)


