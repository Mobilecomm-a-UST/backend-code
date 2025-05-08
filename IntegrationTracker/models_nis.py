from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import localtime

class IntegrationData(models.Model):
    unique_key=models.CharField(max_length=500, blank=True)
    OEM = models.CharField(max_length=500, blank=True)  # Allow no value
    Integration_Date = models.DateField(null=True)  # Allow no value
    CIRCLE = models.CharField(max_length=500, blank=True)  # Allow no value
    Activity_Name = models.CharField(max_length=500, blank=True)  # Allow no value
    Site_ID = models.CharField(max_length=500, blank=True)  # Allow no value
    MO_NAME = models.CharField(max_length=500, blank=True)  # Allow no value
    # NO_OF_BBU = models.CharField(max_length=500, blank=True)  # Allow no value
    LNBTS_ID = models.CharField(max_length=500, blank=True)  # Allow no value
    Technology_SIWA = models.CharField(max_length=500, blank=True)  # Allow no value
    OSS_Details = models.CharField(max_length=500, blank=True)  # Allow no value
    Cell_ID = models.CharField(max_length=500, blank=True)  # Allow no value
    CELL_COUNT = models.CharField(max_length=500, blank=True)  # Allow no value
    TRX_Count = models.CharField(max_length=500, blank=True)  # Allow no value
    PRE_ALARM = models.CharField(max_length=500, blank=True)  # Allow no value
    GPS_IP_CLK = models.CharField(max_length=500, blank=True)  # Allow no value
    RET = models.CharField(max_length=500, blank=True)  # Allow no value
    POST_VSWR = models.CharField(max_length=500, blank=True)  # Allow no value
    POST_Alarms = models.CharField(max_length=500, blank=True)  # Allow no value
    Activity_Mode = models.CharField(max_length=500, blank=True)  # Allow no value
    CELL_STATUS = models.CharField(max_length=500, blank=True)  # Allow no value
    CTR_STATUS = models.CharField(max_length=500, blank=True)  # Allow no value
    Integration_Remark = models.TextField(blank=True)  # Allow no value
    T2T4R = models.CharField(max_length=500, blank=True)  # Allow no value
    BBU_TYPE = models.CharField(max_length=500, blank=True)  # Allow no value
    BB_CARD = models.CharField(max_length=500, blank=True)  # Allow no value
    RRU_Type = models.CharField(max_length=500, blank=True)  # Allow no value
    Media_Status = models.CharField(max_length=500, blank=True)  # Allow no value
    Mplane_IP = models.CharField(max_length=500, blank=True)  # Allow no value
    SCF_PREPARED_BY = models.CharField(max_length=500, blank=True)  # Allow no value
    SITE_INTEGRATE_BY = models.CharField(max_length=500, blank=True)  # Allow no value
    Site_Status = models.CharField(max_length=500, blank=True)  # Allow no value
    External_Alarm_Confirmation = models.CharField(max_length=500, blank=True)  # Allow no value
    SOFT_AT_STATUS = models.CharField(max_length=500, blank=True)  # Allow no value
    LICENCE_Status = models.CharField(max_length=500, blank=True)  # Allow no value
    ESN_NO = models.CharField(max_length=500, blank=True)  # Allow no value
    Responsibility_for_alarm_clearance = models.CharField(max_length=500, blank=True)  # Allow no value
    TAC = models.CharField(max_length=500, blank=True)  # Allow no value
    PCI_TDD_20 = models.CharField(max_length=500, blank=True)  # Allow no value
    PCI_TDD_10_20 = models.CharField(max_length=500, blank=True)  # Allow no value
    PCI_FDD_2100 = models.CharField(max_length=500, blank=True)  # Allow no value
    PCI_FDD_1800 = models.CharField(max_length=500, blank=True)  # Allow no value
    PCI_L900 = models.CharField(max_length=500, blank=True)  # Allow no value
    PCI_5G = models.CharField(max_length=500, blank=True)  # Allow no value
    RSI_TDD_20 = models.CharField(max_length=500, blank=True)  # Allow no value
    RSI_TDD_10_20 = models.CharField(max_length=500, blank=True)  # Allow no value
    RSI_FDD_2100 = models.CharField(max_length=500, blank=True)  # Allow no value
    RSI_FDD_1800 = models.CharField(max_length=500, blank=True)  # Allow no value
    RSI_L900 = models.CharField(max_length=500, blank=True)  # Allow no value
    RSI_5G = models.CharField(max_length=500, blank=True)  # Allow no value
    GPL = models.CharField(max_length=500, blank=True)  # Allow no value
    Pre_Post_Check = models.CharField(max_length=500, blank=True)  # Allow no value
    Activity_Type_SIWA = models.CharField(max_length=500, blank=True)  # Allow no value
    Band_SIWA = models.CharField(max_length=500, blank=True)  # Allow no value
    
    BSC_NAME =models.CharField(max_length=500, blank=True)
    BCF=models.CharField(max_length=500, blank=True)
    
    CRQ=models.CharField(max_length=500, blank=True,null=True)
    Customer_Approval = models.CharField(max_length=500, blank =True, null = True)

    Old_Site_ID = models.CharField(max_length=500, blank=True)
    Old_Site_Tech= models.CharField(max_length=500, blank=True)
    Allocated_Tech= models.CharField(max_length=500, blank=True)
    Deployed_Tech= models.CharField(max_length=500, blank=True)

    uploaded_by = models.CharField(max_length=500, blank=True) 
    upload_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

  
    def __str__(self):
        return self.Site_ID  # or any other field to represent the object
from django.utils import timezone
from django.contrib.auth.models import User
class Document(models.Model):
    file_name = models.CharField(max_length=255)
    uploaded_file = models.FileField(upload_to='IntegrationTracker/documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_by_username = models.CharField(max_length=150)
    def save(self, *args, **kwargs):
        # Combine uploaded by username, uploaded at, and filename
        # self.file_name = f"{self.uploaded_by_username}_{self.uploaded_at}_{self.uploaded_file.name}"
        timestamp_str = localtime(timezone.now()).strftime('%Y-%m-%d,%H:%M:%S')
        self.file_name = f"{self.uploaded_file.name}_{self.uploaded_by_username}_{timestamp_str}"
        super().save(*args, **kwargs)
    def __str__(self):
        return self.file_name
   




class Relocation_tracker(models.Model): 
    ix_unique_key=models.CharField(max_length=500, blank=True)
    circle = models.CharField(max_length=255, null=True, blank=True)
    old_site_id = models.CharField(max_length=255, null=True, blank=True)
    new_site_id = models.CharField(max_length=255, null=True, blank=True)
    mo_name = models.CharField(max_length=255, null=True, blank=True)
    no_of_BBUs = models.CharField(max_length=255, null=True, blank=True)
    integration_date = models.DateField(null=True)
    ms1_date = models.DateField(null=True)
    old_site_technology = models.CharField(max_length=255, null=True, blank=True)
    allocated_technology = models.CharField(max_length=255, null=True, blank=True)
    deployed_technology = models.CharField(max_length=255, null=True, blank=True)
    allocated_vs_deployed_tech_deviation = models.CharField(max_length=255, null=True, blank=True)
    old_vs_deployed_tech_deviation = models.CharField(max_length=255, null=True, blank=True)
    old_site_traffic_fixed = models.CharField(max_length=255, null=True, blank=True)
    old_site_traffic_variable = models.CharField(max_length=255, null=True, blank=True)
    existing_traffic = models.CharField(max_length=255, null=True, blank=True)
    old_site_admin_status = models.CharField(max_length=255, null=True, blank=True)
    new_site_admin_status = models.CharField(max_length=255, null=True, blank=True) 
    both_site_unlocked = models.CharField(max_length=255, null=True, blank=True)  
    both_site_locked = models.CharField(max_length=255, null=True, blank=True)  
    pre_less_than_3_mbps = models.CharField(max_length=255, null=True, blank=True)  
    current_less_than_3_mbps = models.CharField(max_length=255, null=True, blank=True)  
    old_vs_deployed_tech= models.CharField(max_length=255, null=True, blank=True)
    allocated_vs_deployed_tech= models.CharField(max_length=255, null=True, blank=True)
    payload_dip = models.CharField(max_length=255, null=True, blank=True)
  # for the purpose of date


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)






class fixed_pre_traffic(models.Model):
    date = models.DateField()  # Stores only the date
    siteID = models.CharField(max_length=255)  # Adjust max_length as needed
    traffic = models.IntegerField(null=True)  # Stores structured data in JSON format
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updated on save
    def __str__(self):
        return f"Site: {self.siteID}, Date: {self.date}"
    
class daily_pre_traffic(models.Model):
    date = models.DateField()  # Stores only the date
    siteID = models.CharField(max_length=255)  # Adjust max_length as needed
    traffic = models.IntegerField(null=True)  # Stores structured data in JSON format
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updated on save
    def __str__(self):
        return f"Site: {self.siteID}, Date: {self.date}"
    
class daily_post_traffic(models.Model):
    date = models.DateField()  # Stores only the date
    siteID = models.CharField(max_length=255)  # Adjust max_length as needed
    traffic = models.IntegerField(null=True)  # Stores structured data in JSON format
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updated on save
    def __str__(self):
        return f"Site: {self.siteID}, Date: {self.date}"
    
class New_site_locked_unlocked_date(models.Model):
    Relocation_id=models.ForeignKey(Relocation_tracker,on_delete=models.CASCADE,related_name='new_site_locked_unlocked_date')
    circle = models.CharField(max_length=255, null=True, blank=True)
    site_locked_by=models.CharField(max_length=255, null=True, blank=True)
    status=models.CharField(max_length=255, null=True, blank=True)
    approval_given_by=models.CharField(max_length=255, null=True, blank=True)
    purpose=models.CharField(max_length=255, null=True, blank=True)
    no_of_BBUs = models.CharField(max_length=255, null=True, blank=True)
    OEM = models.CharField(max_length=255, null=True, blank=True)
    Technology = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class old_site_locked_unlocked_date(models.Model):
    Relocation_id=models.ForeignKey(Relocation_tracker,on_delete=models.CASCADE,related_name='old_site_locked_unlocked_date')
    circle = models.CharField(max_length=255, null=True, blank=True)
    status=models.CharField(max_length=255, null=True, blank=True)
    site_locked_by=models.CharField(max_length=255, null=True, blank=True)
    approval_given_by=models.CharField(max_length=255, null=True, blank=True)
    purpose=models.CharField(max_length=255, null=True, blank=True,)
    no_of_BBUs = models.CharField(max_length=255, null=True, blank=True)
    OEM = models.CharField(max_length=255, null=True, blank=True)
    Technology = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

