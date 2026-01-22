from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import localtime

class IntegrationDataVI(models.Model):
    unique_key=models.CharField(max_length=500, blank=True)
    OEM = models.CharField(max_length=500, blank=True)  # Allow no value
    Integration_Date = models.DateField(null=True)  # Allow no value
    CIRCLE = models.CharField(max_length=500, blank=True)  # Allow no value
    Activity_Name = models.CharField(max_length=500, blank=True)  # Allow no value
    Site_ID = models.CharField(max_length=500, blank=True)  # Allow no value
    MO_NAME = models.CharField(max_length=500, blank=True)  # Allow no value
    NO_OF_BBU = models.CharField(max_length=500, blank=True)  # Allow no value
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

    FR_Date = models.DateField(null=True, blank=True)
    HOTO_Offered_Date_4g = models.DateField(null=True, blank=True)
    HOTO_Accepted_Date_4g = models.DateField(null=True, blank=True)
    HOTO_Offered_Date_2g = models.DateField(null=True, blank=True)
    HOTO_Accepted_Date_2g = models.DateField(null=True, blank=True)
    # Old_Site_Tech= models.CharField(max_length=500, blank=True)
    # Allocated_Tech= models.CharField(max_length=500, blank=True)
    # Deployed_Tech= models.CharField(max_length=500, blank=True)

    uploaded_by = models.CharField(max_length=500, blank=True) 
    upload_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

  
    def __str__(self):
        return self.Site_ID  # or any other field to represent the object

from django.utils import timezone
from django.contrib.auth.models import User
class Document(models.Model):
    file_name = models.CharField(max_length=255)
    uploaded_file = models.FileField(upload_to='IntegrationTrackerVI/documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="integration_vi_documents"   # ✅ IMPORTANT
    )

    uploaded_by_username = models.CharField(max_length=150)

    def save(self, *args, **kwargs):
        timestamp_str = localtime(timezone.now()).strftime('%Y-%m-%d,%H:%M:%S')
        self.file_name = f"{self.uploaded_file.name}_{self.uploaded_by_username}_{timestamp_str}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.file_name

   



class Approval(models.Model):
    circle = models.CharField(max_length=10, unique=True)
    approver_name = models.JSONField()  