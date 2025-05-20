from django.db import models

class Physical_AT_Table(models.Model):
    id = models.CharField(max_length = 500,primary_key=True)
    CIRCLE = models.CharField(max_length=500)
    SITE_ID = models.CharField(max_length=500)
    UNIQUE_ID = models.CharField(max_length=500)
    ENODEB_ID=models.CharField(max_length=500)
    BAND=models.CharField(max_length=500)
    Circle_Project=models.CharField(max_length=500)
    BTS_TYPE=models.CharField(max_length=500)
    OEM_NAME_Nokia_ZTE_Ericsson_Huawei =models.CharField(max_length=500) 
    MS1=models.DateField(null=True)
    PHYSICAL_AT_Offered_DATE=models.DateField(null=True)
    PHYSICAL_AT_ACCEPTANCE_DATE=models.DateField(null=True)
    PHYSICAL_AT_Status_Accepted_Rejected_Offered_Pending_Dismantle=models.CharField(max_length=500)
    CURRENT_STATUS_OF_SITE=models.CharField(max_length=500)
    Total_Allocation=models.CharField(max_length=500)
    Project=models.CharField(max_length=500)
    Current_PHY_AT_Status=models.CharField(max_length=500)   
    Expected_Closer_Status=models.CharField(max_length=500)
    Additional_PHY_AT_Remarks=models.CharField (max_length=500) 
    Ericsson_PHY_AT_Status=models.CharField(max_length=500)  
    Ericsson_PHY_AT_Date=models.DateField(null=True)
    Huawei_PHY_AT_Status=models.CharField (max_length=500) 
    Huawei_PHY_AT_Date=models.DateField(null=True)
    Nokia_PHY_AT_Status=models.CharField(max_length=500)  
    Nokia_PHY_AT_Date=models.DateField(null=True)
    Samsung_PHY_AT_Status=models.CharField(max_length=500)  
    Samsung_PHY_AT_Date=models.DateField(null=True)
    ZTE_PHY_AT_Status=models.CharField (max_length=500) 
    ZTE_PHY_AT_Date=models.DateField(null=True)
    MS1_to_PHY_AT_Ageing=models.CharField(max_length=500)
    Ageing= models.CharField (max_length=500)
    Plan_Date=models.DateField(null=True)
    Plan_Status=models.CharField(max_length=500)
    Upload_date=models.DateField(null=True)
    Expected_Closer_Date=models.DateField(null=True)
    
    # Current_PHY_Status=models.CharField(max_length=100)
    

    def __str__(self):
        return (self.SITE_ID)
    
class Physical_At_upload_status(models.Model):
   
    id=models.CharField(max_length = 500,primary_key=True)
    Site_id=models.CharField(max_length=500,null=True,blank=True)
    update_status=models.CharField(max_length=500,null=True,blank=True)
    Remark=models.TextField(max_length=500,null=True,blank=True)



