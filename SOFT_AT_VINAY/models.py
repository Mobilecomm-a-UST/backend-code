from django.db import models
from IntegrationTracker.models import IntegrationData

# Create your models here.
class Soft_At_Table(models.Model):
    upload_date = models.DateField(blank=True, null=True)
    unique_key = models.CharField(max_length=1000,primary_key=True)
    IntegrationData = models.ForeignKey(IntegrationData, on_delete=models.SET_NULL, blank=True, null=True)
    combination=models.CharField(max_length=1000,blank=True,default="",null=True)
    # integration Data
    OEM = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    Integration_Date = models.DateField(null=True, blank=True)  # Allow no value
    CIRCLE = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    Activity_Name = models.CharField(max_length=500, blank=True,   null=True)  # Allow no value
    Site_ID = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    MO_NAME = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    LNBTS_ID = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    Technology_SIWA = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    OSS_Details = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    Cell_ID = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    CELL_COUNT = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    TRX_Count = models.CharField(max_length=500, blank=True,       null=True)  # Allow no value
    PRE_ALARM = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    GPS_IP_CLK = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    RET = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    POST_VSWR = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    POST_Alarms = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    Activity_Mode = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    CELL_STATUS = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    CTR_STATUS = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    Integration_Remark = models.TextField(blank=True, null=True)  # Allow no value
    T2T4R = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    BBU_TYPE = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    BB_CARD = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    RRU_Type = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    Media_Status = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    Mplane_IP = models.CharField(max_length=500, blank=True , null=True)  # Allow no value
    SCF_PREPARED_BY = models.CharField(max_length=500, blank=True , null=True )  # Allow no value
    SITE_INTEGRATE_BY = models.CharField(max_length=500, blank=True, null=True )  # Allow no value
    Site_Status = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    External_Alarm_Confirmation = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    SOFT_AT_STATUS = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    LICENCE_Status = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    ESN_NO = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    Responsibility_for_alarm_clearance = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    TAC = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    PCI_TDD_20 = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    PCI_TDD_10_20 = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    PCI_FDD_2100 = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    PCI_FDD_1800 = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    PCI_L900 = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    PCI_5G = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    RSI_TDD_20 = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    RSI_TDD_10_20 = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    RSI_FDD_2100 = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    RSI_FDD_1800 = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    RSI_L900 = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    RSI_5G = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    GPL = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    Pre_Post_Check = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    Activity_Type_SIWA = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    Band_SIWA = models.CharField(max_length=500, blank=True, null=True)  # Allow no value
    
    BSC_NAME =models.CharField(max_length=500, blank=True, null=True)
    BCF=models.CharField(max_length=500, blank=True, null=True)
    # SOFT AT DATA
    spoc_name = models.CharField(max_length=255, blank=True, null=True)
    offering_type = models.CharField(max_length=255, blank=True, null=True)
    first_offering_date = models.DateField(blank=True, null=True)
    soft_at_status = models.CharField(max_length=255, blank=True, null=True)
    offering_date = models.DateField(blank=True, null=True)
    acceptance_rejection_date = models.DateField(blank=True, null=True)
    alarm_bucket = models.CharField(max_length=255, blank=True, null=True)
    alarm_details = models.TextField(blank=True, null=True)
    final_responsibility = models.CharField(max_length=255, blank=True, null=True)
    workable_non_workable = models.CharField(max_length=255, blank=True, null=True)
    ubr_ms2_status = models.CharField(max_length=255, blank=True, null=True)
    ubr_link_id = models.CharField(max_length=255, blank=True, null=True)
    twamp_status = models.CharField(max_length=255, blank=True, null=True)
    status_check_date = models.DateField(blank=True, null=True)
    ageing_in_days = models.IntegerField(blank=True, null=True)
    actual_ageing = models.CharField(max_length=255, blank=True, null=True)
    toco_partner = models.CharField(max_length=255, blank=True, null=True)
    support_required_ubr_team = models.CharField(max_length=255, blank=True, null=True)
    support_required_circle_team = models.CharField(max_length=255, blank=True, null=True)
    support_required_noc_team = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    problem_statement = models.TextField(blank=True, null=True)
    final_remarks = models.TextField(blank=True, null=True)
    ms1 = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status_updated_by = models.CharField(max_length=255, blank=True, null=True,default='')
    
    soft_delete=models.BooleanField(default=False)
    def __str__(self):
        return self.unique_key
    
    

    
class Soft_At_upload_status(models.Model):
    id = models.CharField(max_length=500, primary_key=True)
    Site_id = models.CharField(max_length=500, null=True, blank=True)
    UNIQUE_ID = models.CharField(max_length=500, null=True, blank=True)
    update_status = models.CharField(max_length=500, null=True, blank=True)
    Remark = models.TextField(max_length=500, null=True, blank=True)
    CIRCLE = models.CharField(max_length=500, null=True, blank=True)
    SITE_ID = models.CharField(max_length=500, null=True, blank=True)
    BAND = models.CharField(max_length=500, null=True, blank=True)
    OEM_NAME = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        unique_together = ("CIRCLE", "SITE_ID", "BAND", "UNIQUE_ID","OEM_NAME")
