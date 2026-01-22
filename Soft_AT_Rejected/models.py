from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from mailapp.tasks import send_email
from django.contrib.postgres.fields import ArrayField
# from Soft_AT_Rejected.signals import *

class Soft_AT_NOKIA_Rejected_Table(models.Model):

    Reference_Id=models.CharField(max_length=500,null=True)
    AoP=models.CharField(max_length=500,null=True)
    Circle=models.CharField(max_length=500,null=True)
    OEM=models.CharField(max_length=500,null=True)
    TSP=models.CharField(max_length=500,null=True)
    Offered_Date=models.DateField(null=True)
    AT_Type=models.CharField(max_length=500,null=True)
    Site_ID=models.CharField(max_length=500,null=True)
    MRBTS_ID=models.CharField(max_length=500,null=True)
    # Uname=models.CharField(max_length=500,null=True)
    Cell_ID=models.CharField(max_length=500,null=True)
    Cell_ID_2G=models.CharField(max_length=500,null=True)
    DPR_Cell_Name=models.CharField(max_length=500,null=True)
    LNCEL_ID=models.CharField(max_length=500,null=True)
    LNCEL_ID_PCI=models.CharField(max_length=500,null=True)
    MRBTS_Name=models.CharField(max_length=500,null=True)
    OSS_FDD_OSS_2G_OSS=models.CharField(max_length=500,null=True)
    Toco=models.CharField(max_length=500,null=True)
    Tech_info=models.CharField(max_length=500,null=True)
    Tech=models.CharField(max_length=500,null=True)
    Band=models.CharField(max_length=500,null=True)
    Activity_Type=models.CharField(max_length=500,null=True)
    Integration_date=models.DateField(null=True)
    On_Air_DATE=models.DateField(null=True)
    Mplane=models.CharField(max_length=500,null=True)
    Sync_Status=models.CharField(max_length=500,null=True)
    Profile=models.CharField(max_length=500,null=True)
    BSC=models.CharField(max_length=500,null=True)
    BCF=models.CharField(max_length=500,null=True)
    Offer_Reoffer=models.CharField(max_length=500,null=True)
    LAC=models.CharField(max_length=500,null=True)
    TAC=models.CharField(max_length=500,null=True)
    Latitude_N=models.CharField(max_length=500,null=True)
    Longitude_E=models.CharField(max_length=500,null=True)
    FDD_MRBTS_ID=models.CharField(max_length=500,null=True)
    FDD_Mplane_IP=models.CharField(max_length=500,null=True)
    RET_Count=models.CharField(max_length=500,null=True)
    Nominal_Type=models.CharField(max_length=500,null=True)
    Project_Remarks=models.CharField(max_length=500,null=True)
    Rejection_Remarks=models.CharField(max_length=500,null=True)
    Media=models.CharField(max_length=500,null=True)
    Ckt_Id=models.CharField(max_length=500,null=True)
    SMP_ID=models.CharField(max_length=500,null=True)
    Processed_By=models.CharField(max_length=500,null=True)
    AT_REMARK=models.CharField(max_length=500,null=True)
    AT_STATUS =models.CharField(max_length=500,null=True)
    CENTRAL_SPOC= models.CharField(max_length=500,null=True)
    # Received_date=models.DateField()
    Date_Time=models.DateTimeField(default= timezone.now)
    def __str__(self):
        return (self.Site_ID)

    def __str__(self):
        return (self.Site_ID)
class Soft_AT_HUAWEI_Rejected_Table(models.Model):
    Circle=models.CharField(max_length=500,null=True)
    REGION=models.CharField(max_length=500,null=True)
    OEM=models.CharField(max_length=500,null=True)
    TSP=models.CharField(max_length=500,null=True)
    Site_ID_2G=models.CharField(max_length=500,null=True)
    Site_ID_4G=models.CharField(max_length=500,null=True)
    Cell_ID_Parent=models.CharField(max_length=500,null=True)
    Cell_ID_New=models.CharField(max_length=500,null=True)
    Technology=models.CharField(max_length=500,null=True)
    Other_Tech_Info=models.CharField(max_length=500,null=True)
    On_Air_Date=models.DateField(null=True)
    Activity=models.CharField(max_length=500,null=True)
    Unique_ID=models.CharField(max_length=500,null=True)
    Type_of_Cell=models.CharField(max_length=500,null=True)
    Frequency_Band=models.CharField(max_length=500,null=True)
    MME_0=models.CharField(max_length=500,null=True)
    MME_1=models.CharField(max_length=500,null=True)
    MME_2=models.CharField(max_length=500,null=True)
    MME_3=models.CharField(max_length=500,null=True)
    MME_4=models.CharField(max_length=500,null=True)
    SGW_IP=models.CharField(max_length=500,null=True)
    UPEU_Count=models.CharField(max_length=500,null=True)
    VSWR_Alarm_Threshold=models.CharField(max_length=500,null=True)
    Sync_Status_GPS_status_IP=models.CharField(max_length=500,null=True)
    EMF_Status_Yes_No=models.CharField(max_length=500,null=True)
    BSC_RNC_detail=models.CharField(max_length=500,null=True)
    OSS=models.CharField(max_length=500,null=True)
    OSS_IP=models.CharField(max_length=500,null=True)
    Site_OSS_Name=models.CharField(max_length=500,null=True)
    PHYSICAL_ID=models.CharField(max_length=500,null=True)
    TRX_configuration_Detail_900=models.CharField(max_length=500,null=True)
    TRX_configuration_Detail_900_Required=models.CharField(max_length=500,null=True)
    TRX_configuration_Detail_1800=models.CharField(max_length=500,null=True)
    TRX_configuration_Detail_1800_Required=models.CharField(max_length=500,null=True)
    Sector_Count=models.CharField(max_length=500,null=True)
    TX_RX_configuration_Detail=models.CharField(max_length=500,null=True)
    Type_Physical_AT_Soft_AT=models.CharField(max_length=500,null=True)
    Offer_Reoffer=models.CharField(max_length=500,null=True)
    Offer_Reoffer_date=models.DateField(null=True)
    LAC=models.CharField(max_length=500,null=True)
    TAC=models.CharField(max_length=500,null=True)
    LAST_REJECTION_REMARKS=models.CharField(max_length=500,null=True)
    RET_Status=models.CharField(max_length=500,null=True)
    AT_STATUS=models.CharField(max_length=500,null=True)
    AT_Remarks=models.CharField(max_length=500,null=True)
    # Received_date=models.DateField()
    Date_Time=models.DateTimeField(default= timezone.now)
    CENTRAL_SPOC= models.CharField(max_length=500,null=True)
    def __str__(self):
        return (self.Site_ID_2G)

class Soft_AT_SAMSUNG_Rejected_Table(models.Model):
    Circle=models.CharField(max_length=500,null=True)
    OEM=models.CharField(max_length=500,null=True)
    TSP=models.CharField(max_length=500,null=True)
    SR_UNIQUE_Project_ID=models.CharField(max_length=500,null=True)
    AT_Type=models.CharField(max_length=500,null=True)
    Physical_Cascade_ID=models.CharField(max_length=500,null=True)
    Site_ID_2G=models.CharField(max_length=500,null=True)
    Site_ID_4G_MRBTS_ID=models.CharField(max_length=500,null=True)
    Technology=models.CharField(max_length=500,null=True)
    Other_Tech_Info_Band=models.CharField(max_length=500,null=True)
    On_Air_Date=models.DateField(null=True)
    Activity_Type_Swap_New_Site=models.CharField(max_length=500,null=True)
    Parent_Cell_Id_Name_In_Case_Of_Twin_Beam=models.CharField(max_length=500,null=True)
    Newly_Added_In_Case_Of_SA_Twin_Beam_MIMO_Cell_Id_Name=models.CharField(max_length=500,null=True)
    Node_4G_IP_Mplane_IP=models.CharField(max_length=500,null=True)
    OSS_Name=models.CharField(max_length=500,null=True)
    OSS_IP=models.CharField(max_length=500,null=True)
    ENodeB_ID=models.CharField(max_length=500,null=True)
    BSC_In_Case_Of_NT_2G=models.CharField(max_length=500,null=True)
    BSC_OSS_In_Case_Of_NT=models.CharField(max_length=500,null=True)
    R_Site_Name_Ericsson_2G_BCF_ID_Nokia_2G=models.CharField(max_length=500,null=True)
    OLD_Cell_Count_No_Of_Cells=models.CharField(max_length=500,null=True)
    New_Cell_Count_No_Of_Cells=models.CharField(max_length=500,null=True)
    TRX_Configuration_in_case_of_2G=models.CharField(max_length=500,null=True)
    Site_4G_Configuration=models.CharField(max_length=500,null=True)
    No_Of_RRU=models.CharField(max_length=500,null=True)
    Other_Hardware_Related_Additional_Information=models.CharField(max_length=500,null=True)
    TAC=models.CharField(max_length=500,null=True)
    MME_IP=models.CharField(max_length=500,null=True)
    SGW_IP=models.CharField(max_length=500,null=True)
    VSWR_current_value=models.CharField(max_length=500,null=True)
    BBU_Type_Model=models.CharField(max_length=500,null=True)
    OD_ID_Configuration=models.CharField(max_length=500,null=True)
    RET_Configuration=models.CharField(max_length=500,null=True)
    hrs24_Alarm_History=models.CharField(max_length=500,null=True)
    NE_Version=models.CharField(max_length=500,null=True)
    Integration_Date=models.DateField(null=True)
    SW_Version=models.CharField(max_length=500,null=True)
    Sync_status_GPS_clock_NTP=models.CharField(max_length=500,null=True)
    GPL_compliance=models.CharField(max_length=500,null=True)
    LMS_compliance=models.CharField(max_length=500,null=True)
    Power_compliance=models.CharField(max_length=500,null=True)
    IFLB_Compliance=models.CharField(max_length=500,null=True)
    CA_compliance=models.CharField(max_length=500,null=True)
    QoS_Compliance=models.CharField(max_length=500,null=True)
    Ducting_compliance=models.CharField(max_length=500,null=True)
    Energy_saving_fetaures_compliance=models.CharField(max_length=500,null=True)
    Features_implemented_compliance=models.CharField(max_length=500,null=True)
    Nomenclature_Compliance=models.CharField(max_length=500,null=True)
    PCI_RSI_PRACH_definition_compliance=models.CharField(max_length=500,null=True)
    Critical_Major_Alarms=models.CharField(max_length=500,null=True)
    # Observed_after_activity_and_not_there_pre_activity=models.CharField(max_length=500,null=True)
    Splitting_Details=models.CharField(max_length=500,null=True)
    RET_Details_Cell_Name=models.CharField(max_length=500,null=True)
    Toco_Type_Shared_Anchor=models.CharField(max_length=500,null=True)
    Project_Remarks=models.CharField(max_length=500,null=True)
    Rejection_Remarks_in_Case_of_Re_offer=models.CharField(max_length=500,null=True)
    All_approved_features_compliance_implemented=models.CharField(max_length=500,null=True)
    Offer_Reoffer=models.CharField(max_length=500,null=True)
    Offer_Reoffer_Date=models.DateField(null=True)
    GPL_Type=models.CharField(max_length=500,null=True)
    Scope=models.CharField(max_length=500,null=True)
    External_Alarm_Status_YES_NO=models.CharField(max_length=500,null=True)
    LTE_Technology_for_GPL_Validation=models.CharField(max_length=500,null=True)
    Carrier_Type=models.CharField(max_length=500,null=True)
    Radio_Unit_Info_Connected_digital_unit_port_id=models.CharField(max_length=500,null=True)
    Type_of_Media=models.CharField(max_length=500,null=True)
    MW_Link_Id_Ckt_Id=models.CharField(max_length=500,null=True)
    AT_STATUS=models.CharField(max_length=500,null=True)
    AT_Remarks=models.CharField(max_length=500,null=True)
    # Received_date=models.DateField()
    Date_Time=models.DateTimeField(default= timezone.now)
    CENTRAL_SPOC= models.CharField(max_length=500,null=True)
    def __str__(self):
        return (self.Site_ID_2G)
    
class Soft_AT_ZTE_Rejected_Table(models.Model):  
    Circle=models.CharField(max_length=500)
    OEM=models.CharField(max_length=500)
    TSP=models.CharField(max_length=500)
    Site_ID=models.CharField(max_length=500)
    No_of_Cell=models.CharField(max_length=500)
    Cell_ID_Parent=models.CharField(max_length=500)
    Cell_ID_New=models.CharField(max_length=500)
    Technology=models.CharField(max_length=500)
    Other_Tech_Info_Band=models.CharField(max_length=500)
    Integration_Date=models.DateField(null=True)
    Activity_Type=models.CharField(max_length=500)
    OSS=models.CharField(max_length=500)
    BSC=models.CharField(max_length=500)
    Offer_Reoffer=models.CharField(max_length=500)
    Offer_Reoffer_date=models.DateField(null=True)
    AT_Type_Physical_AT_Soft_AT=models.CharField(max_length=500)
    Cascaded_Remarks=models.CharField(max_length=500)
    LAC=models.CharField(max_length=500)
    TAC=models.CharField(max_length=500)
    SiteID_MEID=models.CharField(max_length=500)
    RET_Configuration_Remarks_Cell_Name=models.CharField(max_length=500)
    Toco_Type_Shared_Anchor=models.CharField(max_length=500)
    LAST_REJECTION_REMARKS=models.CharField(max_length=500)
    DPR_Cell_Name=models.CharField(max_length=500)
    Media=models.CharField(max_length=500)
    Duplex=models.CharField(max_length=500)
    Detected_Speed_Duplex=models.CharField(max_length=500)
    M_plane=models.CharField(max_length=500)
    Sync_Status=models.CharField(max_length=500)
    User_Plane_IP=models.CharField(max_length=500)
    TAC_ID=models.CharField(max_length=500)
    CIRCUITID=models.CharField(max_length=500)
    AT_STATUS=models.CharField(max_length=500,null=True)
    AT_Remarks=models.CharField(max_length=500,null=True)
    Date_Time=models.DateTimeField(default= timezone.now)
    CENTRAL_SPOC= models.CharField(max_length=500,null=True)
    def __str__(self):
            return (self.Site_ID)

class Soft_AT_ERI_Rejected_Table(models.Model):   
    AOP=models.CharField(max_length=500)
    Circle=models.CharField(max_length=500)
    OEM=models.CharField(max_length=500)
    # Hardware_Made_OEM=models.CharField(max_length=500)
  
    Offered_AT_Type=models.CharField(max_length=500)
    Physical_Site_Id=models.CharField(max_length=500)
    Site_ID=models.CharField(max_length=500)
    Technology=models.CharField(max_length=500)
    Layers_Other_Tech_Info=models.CharField(max_length=500)
    Activity_Name=models.CharField(max_length=500)
    RET_Configuration_Cell_Name=models.CharField(max_length=500)
    RET_Configured_on_Layer=models.CharField(max_length=500)
    Parent_Cell_Name_In_Case_Of_Twin_Beam=models.CharField(max_length=500)
    Cell_Name_New=models.CharField(max_length=500)
    MO_Name=models.CharField(max_length=500)
    Node_IP=models.CharField(max_length=500)
    OSS_Name_IP=models.CharField(max_length=500)
    BSC_In_Case_Of_NT_2G=models.CharField(max_length=500)
    OSS_ENM_For_BSC_In_Case_Of_NT_2G=models.CharField(max_length=500)
    TAC_Name=models.CharField(max_length=500)
    Cells_Configuration=models.CharField(max_length=500)
    Scenario_In_Case_Of_Swap=models.CharField(max_length=500)
    Hardware_RRU=models.CharField(max_length=500)
    Hardware_BBU=models.CharField(max_length=500)
    Antenna=models.CharField(max_length=500)
    CPRI=models.CharField(max_length=500)
    On_Air_Date=models.DateField(null=True)
    SW_Version=models.CharField(max_length=500)
    Sync_status_GPS_clock_NTP=models.CharField(max_length=500)
    AT_Offering_Date=models.DateField(null=True)
    MIMO_Power_configuration=models.CharField(max_length=500)
    Media_Type=models.CharField(max_length=500)
    Link_id=models.CharField(max_length=500)
    Project_remarks=models.CharField(max_length=500)
    AT_STATUS=models.CharField(max_length=500,null=True)
    AT_Remarks=models.CharField(max_length=500,null=True)
    Date_Time=models.DateTimeField(default= timezone.now)
    CENTRAL_SPOC= models.CharField(max_length=500,null=True)

    def __str__(self):
            return (self.Site_ID)
       

    
    
class Soft_AT_Accepted_Rejected_Table(models.Model):

    Reference_Id=models.CharField(max_length=500,null=True)
    AoP=models.CharField(max_length=500,null=True)
    Circle=models.CharField(max_length=500,null=True)
    OEM=models.CharField(max_length=500,null=True)
    TSP=models.CharField(max_length=500,null=True)
    Offered_Date=models.DateField(null=True)
    AT_Type=models.CharField(max_length=500,null=True)
    Site_ID=models.CharField(max_length=500,null=True)
    MRBTS_ID=models.CharField(max_length=500,null=True)
    # Uname=models.CharField(max_length=500,null=True)
    Cell_ID=models.CharField(max_length=500,null=True)
    DPR_Cell_Name=models.CharField(max_length=500,null=True)
    LNCEL_ID=models.CharField(max_length=500,null=True)
    MRBTS_Name=models.CharField(max_length=500,null=True)
    OSS_FDD_OSS_2G_OSS=models.CharField(max_length=500,null=True)
    Toco=models.CharField(max_length=500,null=True)
    Tech_info=models.CharField(max_length=500,null=True)
    Tech=models.CharField(max_length=500,null=True)
    Band=models.CharField(max_length=500,null=True)
    Activity_Type=models.CharField(max_length=500,null=True)
    Integration_date=models.DateField(null=True)
    On_Air_DATE=models.DateField(null=True)
    Mplane=models.CharField(max_length=500,null=True)
    Sync_Status=models.CharField(max_length=500,null=True)
    Profile=models.CharField(max_length=500,null=True)
    BSC=models.CharField(max_length=500,null=True)
    BCF=models.CharField(max_length=500,null=True)
    Offer_Reoffer=models.CharField(max_length=500,null=True)
    LAC=models.CharField(max_length=500,null=True)
    TAC=models.CharField(max_length=500,null=True)
    Latitude_N=models.CharField(max_length=500,null=True)
    Longitude_E=models.CharField(max_length=500,null=True)
    FDD_MRBTS_ID=models.CharField(max_length=500,null=True)
    FDD_Mplane_IP=models.CharField(max_length=500,null=True)
    RET_Count=models.CharField(max_length=500,null=True)
    Nominal_Type=models.CharField(max_length=500,null=True)
    Project_Remarks=models.CharField(max_length=500,null=True)
    Rejection_Remarks=models.CharField(max_length=500,null=True)
    Media=models.CharField(max_length=500,null=True)
    Ckt_Id=models.CharField(max_length=500,null=True)
    SMP_ID=models.CharField(max_length=500,null=True)
    Processed_By=models.CharField(max_length=500,null=True)
    AT_REMARK=models.CharField(max_length=500,null=True)
    AT_STATUS =models.CharField(max_length=500,null=True)
    upload_date=models.DateField(null=True)
    CENTRAL_SPOC= models.CharField(max_length=500,null=True)

    def __str__(self):
        return (self.Site_ID)    
    
class Soft_At_Rejected_status(models.Model):
   
    id=models.CharField(max_length = 500,primary_key=True)
    Site_id=models.CharField(max_length=500,null=True,blank=True)
    update_status=models.CharField(max_length=500,null=True,blank=True)
    Remark=models.TextField(max_length=500,null=True,blank=True)




class Rejection_Remarks(models.Model):
    OEM = models.CharField(max_length=500, null=True)
    Alarm_Bucket = models.CharField(max_length=500, null=True)
    Rejection_Remark = models.CharField(max_length=1000, null=True, blank=True)
    Final_Responsibility = models.CharField(max_length=500, null=True)
    
   

    def __str__(self):
        return self.Rejection_Remark

class Centeral_Responsible_Spoc_Mail(models.Model):
    OEM = models.CharField(max_length=500, null=True)
    Circle = models.CharField(max_length=254, null=True)
    Central_Soft_At_Prime_Spoc_Mail = ArrayField(models.EmailField(max_length = 254), size=15, blank=True)
    Central_Soft_At_Spoc_Mail = ArrayField(
        models.EmailField(max_length=254, blank=True),
        size=15,
        blank=True
    )

    def __str__(self):
        return self.OEM+" "+self.Circle

class Circle_Responsible_Spoc(models.Model):
    OEM = models.CharField(max_length=500, null=True)
    Circle = models.CharField(max_length=254, null=True)
    Circle_Soft_At_Spoc_Mail = models.EmailField(max_length = 254)

    def __str__(self):
        return self.Circle_Soft_At_Spoc_Mail
    
class Central_Management(models.Model):
    OEM = models.CharField(max_length=500, null=True)
    Circle = models.CharField(max_length=254, null=True)
    Central_Management_Mails = ArrayField(models.EmailField(max_length = 254), size=15, blank=True)

    def __str__(self):
        return self.Central_Management_Mails[0]+" Cricle"+self.Circle+" OEM "+self.OEM
    
class Circle_PM (models.Model):
    OEM = models.CharField(max_length=500, null=True)
    Circle = models.CharField(max_length=254, null=True)
    Circle_PM_Mail = models.EmailField(max_length = 254)

    def __str__(self):
        return self.Circle_PM_Mail




class Soft_AT_Rejection_Mail_Saved_Status(models.Model):
    OEM = models.CharField(max_length = 500)
    Date_Time = models.DateTimeField(default= timezone.now)
    Sender_Mail = models.EmailField(max_length = 254)
    Saved_Status = models.BooleanField(default = False)
    Error_Status = models.CharField(max_length = 500)

    

    def __str__(self):
        return self.OEM
    
    

