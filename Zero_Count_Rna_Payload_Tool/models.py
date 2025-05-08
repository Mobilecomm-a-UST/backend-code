from django.db import models
import uuid

# Create your models here.
import math
from django.db import models
import re
from datetime import datetime

from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils import timezone
from django.db import transaction


class Raw_Kpi_Table_4G(models.Model):
    Cell_Name = models.CharField(max_length=500)
    Site_ID = models.CharField(max_length=500)
    OEM = models.CharField(max_length=500)
    Technology = models.CharField(max_length=500)
    Payload_4G = models.CharField(max_length=500)
    RNA_4G = models.CharField(max_length=500)
    VOLTE_TRAFFIC = models.CharField(max_length=500)

    def __str__(self):
        return self.Site_ID


class Raw_Kpi_Table_2G(models.Model):
    Cell_Name = models.CharField(max_length=500)
    Site_ID = models.CharField(max_length=500)
    OEM = models.CharField(max_length=500)
    Technology = models.CharField(max_length=500)
    TRAFFIC_2G = models.CharField(max_length=500)
    RNA_2G = models.CharField(max_length=500)

    def __str__(self):
        return self.Site_ID


class Daily_4G_KPI(models.Model):
    Short_name = models.CharField(max_length=500)
    Date = models.DateField(null=True)
    ECGI_4G = models.CharField(max_length=500)
    MV_Site_Name = models.CharField(max_length=500)
    OEM_GGSN = models.CharField(max_length=500)
    MV_Freq_Band = models.CharField(max_length=500)
    MV_Freq_Bandwidth = models.CharField(max_length=500)
    MV_Radio_NW_Availability = models.FloatField(max_length=500, default=0)
    MV_4G_Data_Volume_GB = models.FloatField(max_length=500, default=0)
    MV_VoLTE_raffic = models.FloatField(max_length=500, default=0)
    name_SiteA = models.FloatField(max_length=500, default=0)
    name_SiteB = models.FloatField(max_length=500, default=0)
    MV_DL_User_Throughput_Kbps = models.FloatField(max_length=500, default=0)
    MV_E_UTRAN_Average_CQI = models.FloatField(max_length=500, default=0)
    UL_RSSI = models.FloatField(max_length=500, default=0)
    MV_Average_number_of_used_DL_PRBs = models.FloatField(max_length=500, default=0)
    MV_UL_RSSI_dBm_PRB = models.FloatField(max_length=500, default=0)
    MV_RRC_Setup_Success_Rate = models.FloatField(max_length=500, default=0)
    MV_ERAB_Setup_Success_Rate = models.FloatField(max_length=500, default=0)
    MV_PS_Drop_Call_Rate = models.FloatField(max_length=500, default=0)
    MV_UL_User_Throughput_Kbps = models.FloatField(max_length=500, default=0)
    MV_Max_Connecteda_User = models.FloatField(max_length=500, default=0)
    MV_PUCCH_SINR = models.FloatField(max_length=500, default=0)
    MV_Average_UE_Distance_KM = models.FloatField(max_length=500, default=0)
    MV_PS_handover_success_rate_LTE_INTER_SYSTEM = models.FloatField(
        max_length=500, default=0
    )
    MV_PS_handover_success_rate_LTE_INTRA_SYSTEM = models.FloatField(
        max_length=500, default=0
    )
    UL_RSSI_Nokia_RSSI_SINR = models.FloatField(max_length=500, default=0)
    MV_VoLTE_DCR = models.FloatField(max_length=500, default=0)
    MV_Packet_Loss_DL = models.FloatField(max_length=500, default=0)
    MV_Packet_Loss_UL = models.FloatField(max_length=500, default=0)
    PS_InterF_HOSR = models.FloatField(max_length=500, default=0)
    PS_IntraF_HOSR = models.FloatField(max_length=500, default=0)
    dlRsBoost = models.FloatField(null=True, blank=True, default=0)
    RS_Power_dB = models.FloatField(null=True, blank=True, default=0)

    def __str__(self):
        return self.Short_name


class MS1_SITE_DONE(models.Model):
    Short_name = models.CharField(max_length=500)
    Date = models.DateField(null=True)
    MOVED_AT = models.DateTimeField(auto_now_add=True)
    ECGI_4G = models.CharField(max_length=500)
    MV_Site_Name = models.CharField(max_length=500)
    OEM_GGSN = models.CharField(max_length=500)
    MV_Freq_Band = models.CharField(max_length=500)
    MV_Freq_Bandwidth = models.CharField(max_length=500)

    class Meta:
        verbose_name = "MS1_SITE_DONE"
        verbose_name_plural = "MS1_SITES_DONE"

    def __self__(self):
        return self.Short_name


class Daily_2G_KPI(models.Model):
    Short_name = models.CharField(max_length=500)
    Date = models.DateField(null=True)
    Cell_Name = models.CharField(max_length=500)
    MV_2G_Site_Name = models.CharField(max_length=500)
    Site_Name = models.CharField(max_length=500)
    CGI_2G = models.CharField(max_length=500)
    OEM_GGSN = models.CharField(max_length=500)
    MV_Total_Voice_Traffic_BBH = models.CharField(max_length=500)
    Network_availability_RNA = models.CharField(max_length=500)
    MV_of_2G_Cell_with_Network_Availability = models.CharField(max_length=500)

    def __str__(self):
        return self.Short_name


# Abstract base class for common fields
class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the record was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when the record was last updated."
    )
    # created_by = models.CharField(max_length=500, null=True, blank=True, help_text="User who created the record.")
    updated_by = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        help_text="User who last updated the record.",
    )

    class Meta:
        abstract = True


class TicketCounter(models.Model):
    id = models.AutoField(primary_key=True)
    counter = models.PositiveIntegerField(
        default=0, help_text="Auto-increment counter for ticket IDs."
    )

    def __str__(self):
        return f"Counter: {self.counter}"


class Ticket_Counter_Table_Data(BaseModel):
    ticket_id = models.CharField(
        primary_key=True,
        editable=False,
        max_length=2000,
        unique=True,
        help_text="Unique ticket identifier.",
    )
    Circle = models.CharField(
        max_length=500, default="", db_index=True, help_text="Circle of the ticket."
    )
    Short_name = models.CharField(
        max_length=500, null=True, help_text="Short name of the site."
    )
    Site_ID = models.CharField(max_length=500, help_text="Site identifier.")
    priority = models.CharField(
        max_length=500,
        choices=[
            ("P0", "P0"),
            ("P1", "P1"),
            ("P2", "P2"),
        ],
        help_text="Priority level of the ticket.",
    )
    Date = models.DateField(auto_now=True, help_text="Date associated with the ticket.")
    Open_Date = models.DateField(
        auto_now_add=True, help_text="Date when the ticket was opened."
    )
    Unique_Id = models.CharField(
        max_length=1000,
        editable=False,
        help_text="Unique identifier combining site and date.",
    )
    Status = models.CharField(max_length=500, help_text="Current status of the ticket.")
    Remarks = models.TextField(
        default="", help_text="Additional remarks about the ticket."
    )
    Ownership = models.CharField(
        max_length=500, default="", help_text="Ownership details."
    )
    Circle_Spoc = models.CharField(
        max_length=500, default="", help_text="Circle SPOC details."
    )
    Pre_Remarks = models.JSONField(
        default=list, help_text="Preliminary remarks about the ticket."
    )
    aging = models.PositiveIntegerField(
        default=0, help_text="Number of days since the ticket was opened."
    )
    auto_rca = models.CharField(
        max_length=500, default="", help_text="Auto root cause analysis."
    )
    proposed_solution = models.TextField(
        default="", help_text="Proposed solution for the issue."
    )
    category = models.CharField(
        max_length=500, default="", help_text="Detailed description of the ticket."
    )
    rca_feedback = models.BooleanField(null=True, blank=True)
    ticket_type = models.CharField(
        max_length=500, null=True, blank=True, help_text="Type of the ticket."
    )
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=["Short_name", "Date"], name="unique_shortname_date"
    #         )
    #     ]
    #     verbose_name = "Ticket Counter Table Data"
    #     verbose_name_plural = "Ticket Counter Table Data"

    @staticmethod
    def get_circle(short_name):
        """Extract Circle based on the short name format."""
        if "NE-ik" in short_name:
            return short_name.split("-")[4]
        elif "Sams" in short_name:
            return short_name.split(",")[1][:2]
        elif "@Nokia" in short_name:
            parts = re.split(r"(\\d+)", short_name.split("-")[1])
            return parts[0] if parts else None
        elif short_name.startswith("LD") or short_name.startswith("LU"):
            return "DL"
        else:
            return short_name.split("_")[0]

    def save(self, *args, **kwargs):

        if isinstance(self.Date, datetime):
            self.Date = self.Date.date()
        if isinstance(self.Open_Date, datetime):
            self.Open_Date = self.Open_Date.date()
 
        
        self.Unique_Id = f"{self.Short_name}_{self.Date}"

        latest_date = kwargs.pop("latest_date", datetime.now().date())
        self.aging = (latest_date - self.Open_Date).days if self.Open_Date else 0
            
        # Updating by using static Method...
        self.Circle = Ticket_Counter_Table_Data.get_circle(self.Short_name)

        if not self.ticket_id:
            counter, _ = TicketCounter.objects.get_or_create(id=1)
            counter.counter += 1
            counter.save()
            self.ticket_id = f"MCPSINC_00{counter.counter}"

        # if self.ticket_id and self.Status.upper() == "CLOSE":
        #     self.Open_Date = datetime.now().date()
        #     self.aging = 0
        #     counter, _ = TicketCounter.objects.get_or_create(id=1)
        #     counter.counter += 1
        #     counter.save()
            # self.ticket_id = f"MCPSINC_00{counter.counter}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.Unique_Id}_{self.ticket_id}"

class Daily_4G_KPI_REPORT(BaseModel):
    daily_4g_kpi_unique_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False,
        help_text="This is a unique identifier for the daily kpi's",
    )
    kpi_name = models.CharField(
        max_length=500, blank=True, null=True, default="No KPI Found"
    )
    Short_name = models.CharField(max_length=500, help_text="Short_name Corressponding to 4g_kpi")
    Date = models.DateField(
        null=True, blank=True, help_text="The date of the event (YYYY-MM-DD)."
    )
    Site_ID = models.CharField(max_length=500, blank=True, null=True, help_text="Site identifier.")
    
    oem = models.CharField(
        max_length=100,  
        blank=True,  
        null=True,  
        help_text="The Original Equipment Manufacturer of the software" 
    )
    ECGI_4G = models.CharField(
        max_length=500,  
        blank=True,  
        null=True,  
        help_text="this is a 4G_ECGI Field..." 
    )
    
    week_1_val = models.FloatField(max_length=500, default=0)
    week_2_val = models.FloatField(max_length=500, default=0)

    date_1_val = models.FloatField(max_length=500, default=0)
    date_2_val = models.FloatField(max_length=500, default=0)
    date_3_val = models.FloatField(max_length=500, default=0)
    date_4_val = models.FloatField(max_length=500, default=0)
    date_5_val = models.FloatField(max_length=500, default=0)
    date_6_val = models.FloatField(max_length=500, default=0)
    date_7_val = models.FloatField(max_length=500, default=0)
    date_8_val = models.FloatField(max_length=500, default=0)
    
    
    def _str_(self):
        return self.daily_4g_kpi_unique_id
    




class level1(models.Model):
    circle=models.CharField(max_length=250)
    person_name=models.CharField(max_length=250)
    email=models.EmailField()
    
    def __str__(self):
      return f"{self.circle}-{self.person_name}"
   
    
class level2(models.Model):
   circle=models.CharField(max_length=250)
   person_name=models.CharField(max_length=250)
   email=models.EmailField()
   
   def __str__(self):
      return f"{self.circle}-{self.person_name}"
    
class level3(models.Model):
    circle=models.CharField(max_length=250)
    person_name=models.CharField(max_length=250)
    email=models.EmailField()
    
    def __str__(self):
      return f"{self.circle}-{self.person_name}"
    
class level4(models.Model):
    circle=models.CharField(max_length=250)
    person_name=models.CharField(max_length=250)
    email=models.EmailField()
     
    def __str__(self):
      return f"{self.circle}-{self.person_name}"  
    

class  Threshold(models.Model):
      priority =models.CharField(max_length=2,unique=True, choices =[('P0','P0'),
                                          ('P1','P1'),
                                          ('P2','P2') ,
                                          ('P3','P3') ])
      threshold_aging_level_1 = models.IntegerField()
      threshold_aging_level_2 = models.IntegerField()
      threshold_aging_level_3 = models.IntegerField()
      threshold_aging_level_4 = models.IntegerField()
         
      def __str__(self):
        return f"{self.priority}"