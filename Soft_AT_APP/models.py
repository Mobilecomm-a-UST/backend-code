from django.db import models

# Create your models here.
class Soft_At_Table(models.Model):
    id = models.CharField(max_length = 100,primary_key=True)
    CIRCLE=models.CharField(max_length=100)
    SITE_ID=models.CharField(max_length=100) 
    UNIQUE_ID =models.CharField(max_length=100)
    ENODEB_ID=models.CharField(max_length=100,null=True) # can be blank
    BAND=models.CharField(max_length= 100,null=True) # can be blank
    Circle_Project=models.CharField(max_length=100)
    OEM_NAME=models.CharField(max_length=100,null=True) # can be blank
    # RFAI_DATE=models.DateField(null=True)
    # OA_COMMERCIAL_TRAFFIC_PUT_ON_AIR_MS1_DATE=models.CharField(max_length=100)
   
    Status=models.CharField(max_length=100)
    Date=models.DateField(null=True)
    Pending_Bucket=models.CharField(max_length=100,null=True)
    Alarm_Bucket=models.CharField(max_length=100,null=True)
    Ageing=models.CharField(max_length=100,null=True)
    Upload_date=models.DateField(null=True)
    Remarks=models.CharField(max_length=500,null=True)
    def __str__(self):
        return (self.SITE_ID)
    

class Soft_At_upload_status(models.Model):
    id=models.CharField(max_length = 100,primary_key=True)
    Site_id=models.CharField(max_length=100,null=True,blank=True)
    update_status=models.CharField(max_length=100,null=True,blank=True)
    Remark=models.TextField(max_length=100,null=True,blank=True)

