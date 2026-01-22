from django.db import models
from django.utils import timezone

class UBR_Soft_Phy_AT_Rejection_Table(models.Model):
    Circle	=models.CharField(max_length=500,null=True)
    Site_ID	=models.CharField(max_length=500,null=True)
    Site_Type	=models.CharField(max_length=500,null=True)
    TSP	=models.CharField(max_length=500,null=True)
    Link_Id	=models.CharField(max_length=500,null=True)
    RA_Number	=models.CharField(max_length=500,null=True)
    CKT_ID	=models.CharField(max_length=500,null=True)
    UBR_Make_OEM	=models.CharField(max_length=500,null=True)
    UBR_Model	=models.CharField(max_length=500,null=True)
    Site_A_IP	=models.CharField(max_length=500,null=True)
    Site_B_IP	=models.CharField(max_length=500,null=True)
    Re_offer	=models.CharField(max_length=500,null=True)
    Soft_Physical 	=models.CharField(max_length=500,null=True)
    Offered_Date =models.DateField(null=True)	
    AT_Status	=models.CharField(max_length=500,null=True)
    Reasons=models.CharField(max_length=500,null=True)
    Date_Time=models.DateTimeField(default= timezone.now)

    
    def __str__(self):
        return (self.Site_ID)
