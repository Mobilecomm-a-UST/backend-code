from django.db import models

class Equipment(models.Model):
    # id=models.CharField(max_length=500,primary_key=True)
    OEM=models.CharField(max_length=500)
    Hardware_Type=models.CharField(max_length=500)
    Equipment_description=models.CharField(max_length=500)
    Supported_Cards=models.CharField(max_length=500) 
    Technology_Supported =models.CharField(max_length=500) 
    Techninal_Description =models.CharField(max_length=500) 
    Capacity =models.CharField(max_length=500) 
    MAX_POWER =models.CharField(max_length=500) 
    Remarks =models.CharField(max_length=500) 

    def __str__(self):
        return (self.OEM)


class Equipment_upload_status(models.Model): 
   
    # id=models.CharField(max_length = 500,primary_key=True)
    # OEM=models.CharField(max_length=500,null=True,blank=True)
    update_status=models.CharField(max_length=500,null=True,blank=True)
    Remark=models.TextField(max_length=500,null=True,blank=True)
