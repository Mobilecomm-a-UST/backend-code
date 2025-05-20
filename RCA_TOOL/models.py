from django.db import models

class RCA_TABLE(models.Model):
    KPI = models.CharField(max_length=255, null=True, blank=True)
    Probable_causes = models.CharField(max_length=255, null=True, blank=True)
    Data_source = models.CharField(max_length=255, null=True, blank=True)
    Tentative_counters = models.CharField(max_length=255, null=True, blank=True)
    Condition_check = models.FloatField(null=True, blank=True)
    Operator = models.CharField(max_length=255, null=True, blank=True)
    RCA = models.CharField(max_length=255, null=True, blank=True)
    Proposed_solution = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.KPI  


class KPI_TABLE(models.Model):
    KPI = models.CharField(max_length=500)
    threshold_value = models.FloatField()
    operator = models.CharField(max_length=100)
     

    def __str__(self) -> str:
        return self.KPI


class Daily_4G_KPI(models.Model):
    Short_name = models.CharField(max_length=500)
    Date = models.DateField(null=True)
    ECGI_4G = models.CharField(max_length=500)
    MV_Site_Name = models.CharField(max_length=500)
    OEM_GGSN = models.CharField(max_length=500)
    MV_Freq_Band = models.CharField(max_length=500)
    MV_Freq_Bandwidth = models.CharField(max_length=500)
    MV_Radio_NW_Availability = models.FloatField(default=0)
    MV_4G_Data_Volume_GB = models.FloatField(default=0)
    MV_VoLTE_raffic = models.FloatField(default=0)
    name_SiteA = models.FloatField(default=0)
    name_SiteB = models.FloatField(default=0)
    MV_DL_User_Throughput_Kbps = models.FloatField()   
    MV_E_UTRAN_Average_CQI = models.FloatField(default=0)
    UL_RSSI = models.FloatField(default=0)
    MV_Average_number_of_used_DL_PRBs = models.FloatField(
        default=0
    )
    MV_UL_RSSI_dBm_PRB = models.FloatField(default=0)
    MV_RRC_Setup_Success_Rate = models.FloatField(default=0)
    MV_ERAB_Setup_Success_Rate = models.FloatField(default=0)
    MV_PS_Drop_Call_Rate = models.FloatField(default=0)
    MV_UL_User_Throughput_Kbps = models.FloatField(default=0)
    MV_Max_Connecteda_User = models.FloatField(default=0)
    MV_PUCCH_SINR = models.FloatField(default=0)
    MV_Average_UE_Distance_KM = models.FloatField(default=0)
    MV_PS_handover_success_rate_LTE_INTER_SYSTEM = models.FloatField(
        default=0
    )
    MV_PS_handover_success_rate_LTE_INTRA_SYSTEM = models.FloatField(
        default=0
    )
    UL_RSSI_Nokia_RSSI_SINR = models.FloatField(default=0)
    MV_VoLTE_DCR = models.FloatField(default=0)
    MV_Packet_Loss_DL = models.FloatField(default=0)
    MV_Packet_Loss_UL = models.FloatField(default=0)
    PS_InterF_HOSR = models.FloatField(default=0)
    PS_IntraF_HOSR =  models.FloatField(default=0)
    MV_eCell_Data_BH = models.TimeField(null=True, blank=True)
    dlRsBoost = models.FloatField(null=True, blank=True, default=0)
    RS_Power_dB = models.FloatField(null=True, blank=True, default=0)


    MV_CSFB_Redirection_Success_Rate = models.FloatField(null=True, blank=True, default=0)
    VoLTE_Inter_Frequency_Handover_Success_Ratio = models.FloatField(null=True, blank=True, default=0)
    VoLTE_Intra_LTE_Handover_Success_Ratio = models.FloatField(null=True, blank=True, default=0)
    MV_RRC_Setup_Success_Rate_DENOM = models.FloatField(null=True, blank=True, default=0)
    
    
    MV_DL_User_Throughput_Kbps_CUBH = models.FloatField(null=True, blank=True, default=0)
    Sams_Average_UE_Distance_KM = models.FloatField(null=True, blank=True, default=0)
    
    MV_VoLTE_Packet_Loss_UL_CBBH = models.FloatField(null=True, blank=True, default=0)
    MV_VoLTE_Packet_Loss_DL_CBBH = models.FloatField(null=True, blank=True, default=0)

    def __str__(self):
        return self.Short_name


class Tantitive_Counters_24_Hours(models.Model):
    Short_name = models.CharField(max_length=500)
    DateTime = models.DateTimeField(null=True)
    S1_Failure_CDBH = models.FloatField(null=True, blank=True)
    Nokia_S1_Failures_MME_Issue = models.FloatField(null=True, blank=True)
    S1_Failures_MME_Issue = models.FloatField(null=True, blank=True)
    MME_Generated_Issues_on_Cells = models.FloatField(null=True, blank=True)
    LS1AP_S1AP_PARTIAL_RESET_INIT_MME = models.FloatField(null=True, blank=True)
    LS1AP_S1AP_KILL_REQ = models.FloatField(null=True, blank=True)
    LS1AP_S1AP_KILL_RESP = models.FloatField(null=True, blank=True)
    LRRC_REJ_RRC_CONN_RE_ESTAB = models.FloatField(null=True, blank=True)
    LRRC_RRC_PAGING_REQUESTS = models.FloatField(null=True, blank=True)
    LRRC_RRC_CON_RE_ESTAB_ATT_HO_FAIL = models.FloatField(null=True, blank=True)
    LRRC_RRC_CON_RE_ESTAB_ATT_OTHER = models.FloatField(null=True, blank=True)
    RRC_CONN_REL_TA_LIMIT = models.FloatField(null=True, blank=True)
    LEPSB_EPC_EPS_BEARER_REL_REQ_NORM = models.FloatField(null=True, blank=True)
    LEPSB_EPC_EPS_BEARER_REL_REQ_DETACH = models.FloatField(null=True, blank=True)
    LEPSB_EPC_EPS_BEARER_REL_REQ_RNL = models.FloatField(null=True, blank=True)
    LEPSB_EPC_EPS_BEARER_REL_REQ_OTH = models.FloatField(null=True, blank=True)
    LEPSB_EPC_EPS_BEAR_REL_REQ_N_QCI1 = models.FloatField(null=True, blank=True)
    LEPSB_EPC_EPS_BEAR_REL_REQ_D_QCI1 = models.FloatField(null=True, blank=True)
    LEPSB_EPC_EPS_BEAR_REL_REQ_R_QCI1 = models.FloatField(null=True, blank=True)
    LEPSB_EPC_EPS_BEAR_REL_REQ_O_QCI1 = models.FloatField(null=True, blank=True)
    LEPSB_ERAB_NBR_DL_FAIL_OVL = models.FloatField(null=True, blank=True)
    LEPSB_ERAB_NBR_UL_FAIL_OVL = models.FloatField(null=True, blank=True)
    LEPSB_EPC_EPS_BEAR_REL_REQ_R_QCI2 = models.FloatField(null=True, blank=True)
    LEPSB_EPC_EPS_BEAR_REL_REQ_O_QCI2 = models.FloatField(null=True, blank=True)
    LEPSB_ERAB_REL_DOUBLE_S1 = models.FloatField(null=True, blank=True)
    LEPSB_ERAB_REL_DOUBLE_S1_QCI1 = models.FloatField(null=True, blank=True)
    LEPSB_ERAB_REL_ALL_ABNORMAL_H_PWR_UE = models.FloatField(null=True, blank=True)
    LXPL_SCG_ADD_COMPLETION_FAIL_T = models.FloatField(null=True, blank=True)
    LXPL_SGNB_ADD_COMPL_FAIL_T = models.FloatField(null=True, blank=True)
    LXPL_SCG_MOD_ADD_MENB_COMPL_FAIL_T = models.FloatField(null=True, blank=True)
    NX2CC_NX2CC_RAB_REL_ATT_MENB = models.FloatField(null=True, blank=True)
    NX2CC_NX2CC_RAB_REL_NORM_MENB = models.FloatField(null=True, blank=True)
    NX2CC_NX2CC_RAB_REL_ATT_SGNB = models.FloatField(null=True, blank=True)
    NX2CC_NX2CC_RAB_REL_ABNORM_SGNB = models.FloatField(null=True, blank=True)
    NX2CC_NX2CC_RAB_REL_PREEM_SGNB = models.FloatField(null=True, blank=True)
    RSRP_Samples_lt_116_dBm = models.FloatField(null=True, blank=True)
    TNL_Failure_Count = models.FloatField(null=True, blank=True)
    TNL_Failure_Percent = models.FloatField(null=True, blank=True)
    LRRC_DISC_RRC_PAGING = models.FloatField(null=True, blank=True)
    MV_Radio_NW_Availability = models.FloatField(null=True, blank=True)
    
    UL_RSSI = models.FloatField(max_length=500, default=0)
    DL_BLER = models.FloatField(null=True, blank=True, default=0) 
    UL_BLER = models.FloatField(null=True, blank=True,default=0) 

    LEPSB_ERAB_INI_SETUP_FAIL_RNL_RIP = models.FloatField(null=True, blank=True)
    LEPSB_ERAB_INI_SETUP_FAIL_RNL_RNA = models.FloatField(null=True, blank=True, default=0)
    LEPSB_ERAB_INI_SETUP_FAIL_RNL_UEL = models.FloatField(null=True, blank=True, default=0)
    LEPSB_ERAB_INI_SETUP_FAIL_TNL_TRU = models.FloatField(null=True, blank=True, default=0)
    LEPSB_ERAB_REL_ENB_TNL_TRU = models.FloatField(null=True, blank=True, default=0)
    LUEST_SIGN_CONN_ESTAB_FAIL_PUCCH = models.FloatField(null=True, blank=True, default=0)
    LUEST_SIGN_CONN_ESTAB_FAIL_MAXRRC = models.FloatField(null=True, blank=True, default=0)
    LUEST_SIGN_EST_F_RRCCOMPL_MISSING = models.FloatField(null=True, blank=True, default=0)
    
    # to be added in the tentative excel sheet


    class Meta:
        verbose_name = "Tentative Counter"
        verbose_name_plural = "Tentative Counters"

    def __str__(self):
        return self.Short_name

 
class AlarmNotification(models.Model):
    NotificationId = models.CharField(max_length=255)
    AlarmNumber = models.CharField(max_length=255)
    Upload_date = models.DateField()
    AlarmType = models.CharField(max_length=255)
    Severity = models.CharField(max_length=50)
    AlarmTime = models.DateTimeField()
    ProbableCause = models.TextField()
    ProbableCauseCode = models.CharField(max_length=255)
    AlarmText = models.TextField()
    DistinguishedName = models.CharField(max_length=255)
    ObjectClass = models.CharField(max_length=255)
    AcknowledgementState = models.CharField(max_length=50)
    AcknowledgementTimeOrUnacknowledgementTime = models.CharField(max_length=255)
    AcknowledgementUser = models.CharField(max_length=255, blank=True, null=True)
    CancelState = models.CharField(max_length=50)
    CancelTime = models.CharField(max_length=50)
    CancelUser = models.CharField(max_length=255, blank=True, null=True)
    Name = models.CharField(max_length=255)
    MaintenanceRegionName = models.CharField(max_length=255)
    SiteName = models.CharField(max_length=255)
    SitePriority = models.CharField(max_length=50)
    SiteAddress = models.TextField()
    ExtraInformation = models.TextField(blank=True, null=True)
    DiagnosticInfo = models.TextField(blank=True, null=True)
    UserAdditionalInformation = models.TextField(blank=True, null=True)
    SupplementaryInformation = models.TextField(blank=True, null=True)
    AdditionalInformation1 = models.TextField(blank=True, null=True)
    AdditionalInformation2 = models.TextField(blank=True, null=True)
    AdditionalInformation3 = models.TextField(blank=True, null=True)
    CorrelationIndicator = models.CharField(max_length=50)
    NotesIndicator = models.CharField(max_length=50)
    TroubleTicketIndicator = models.CharField(max_length=50)
    AlarmSound = models.CharField(max_length=50)
    InstanceCounter = models.IntegerField()
    ConsecutiveNumber = models.IntegerField()
    AlarmInsertionTime = models.CharField(max_length=255,blank=True, null=True)
    AlarmUpdateTime = models.CharField(max_length=255,blank=True, null=True)
    ControllingObjectName = models.CharField(max_length=255)
    OriginAlarmTime = models.CharField(max_length=255,blank=True, null=True)
    OriginAlarmUpdateTime = models.CharField(max_length=255,blank=True, null=True)
    OriginAcknowledgementOrUnacknowledgementTime = models.CharField(max_length=255,blank=True, null=True)
    OriginCancelTime = models.CharField(max_length=255,blank=True, null=True)
    RelatedDns = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.NotificationId} - {self.AlarmNumber} - {self.AlarmType}"
    
    def save(self, *args, **kwargs): 
        if self.AlarmTime: 
            if self.AlarmTime.tzinfo is not None: 
                raise ValueError("datetime_field must be naive (timezone-unaware)") 
        super().save(*args, **kwargs)


class RCA_output_table(models.Model):
    Cell_name = models.CharField(max_length=100)
    OEM_GGSN= models.CharField(max_length=100)
    KPI = models.CharField(max_length=100)
    cell_value = models.FloatField()
    threshold_value = models.FloatField()
    check_condition = models.CharField(max_length=100)
    RCA = models.TextField()
    Proposed_Solution = models.TextField()
    history_alarms = models.TextField()
    circle = models.CharField(max_length=100)
    date = models.DateField()  # Add this line for the date column
    class meta:
        constraints=[models.UniqueConstraint(fields=['Cell_name ','date'],name='daywise_cells')]

    def __str__(self):
        return self.Cell_name
    

class RCA_payload_table(models.Model):
    KPI = models.CharField(max_length=255, null=True, blank=True)
    Probable_causes = models.CharField(max_length=255, null=True, blank=True)
    Data_source = models.CharField(max_length=255, null=True, blank=True)
    Tentative_counters = models.CharField(max_length=255, null=True, blank=True)
    Condition_check = models.FloatField(null=True, blank=True)
    Operator = models.CharField(max_length=255, null=True, blank=True)
    RCA = models.CharField(max_length=255, null=True, blank=True)
    Proposed_solution = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return self.KPI
