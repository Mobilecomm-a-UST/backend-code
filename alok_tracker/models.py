from django.db import models
from django.db.models import JSONField
 
class AlokTrackerModel(models.Model):
    circle = models.CharField(max_length=100, null=True, blank=True)
    site_tagging = models.CharField(max_length=100, null=True, blank=True)
    old_toco_name = models.CharField(max_length=100, null=True, blank=True)
    old_site_id = models.CharField(max_length=100, null=True, blank=True)
    new_site_id = models.CharField(max_length=100, null=True, blank=True)
    new_toco_name = models.CharField(max_length=100, null=True, blank=True)
    sr_number = models.CharField(max_length=100, null=True, blank=True)
    ran_oem = models.CharField(max_length=100, null=True, blank=True)
    media_type = models.CharField(max_length=100, null=True, blank=True)
    mw_oem = models.CharField(max_length=100, null=True, blank=True)
    relocation_method = models.CharField(max_length=100, null=True, blank=True)
    relocation_type = models.CharField(max_length=100, null=True, blank=True)
    old_site_band = models.CharField(max_length=100, null=True, blank=True)
    new_site_band = models.CharField(max_length=100, null=True, blank=True)
    rfai_date = models.DateField(null=True, blank=True)
    allocation_date = models.DateField(null=True, blank=True)
    rfai_survey_date = models.DateField(null=True, blank=True)
    # rfai_survey_done_date = models.DateField(null=True, blank=True)
    mo_punch_date = models.DateField(null=True, blank=True)
    material_dispatch_date = models.DateField(null=True, blank=True)
    material_delivered_date = models.DateField(null=True, blank=True)
    installation_start_date = models.DateField(null=True, blank=True)
    installation_end_date = models.DateField(null=True, blank=True)
    integration_date = models.DateField(null=True, blank=True)
    emf_submission_date = models.DateField(null=True, blank=True)
    ran_lkf_status = models.CharField(max_length=100, null=True, blank=True)
    alarm_status = models.CharField(max_length=100, null=True, blank=True)
    alarm_rectification_done_date = models.DateField(null=True, blank=True)
    # scft_offered_date = models.DateField(null=True, blank=True)
    scft_done_date = models.DateField(null=True, blank=True)
    scft_i_deploy_offered_date = models.DateField(null=True, blank=True)
    ran_pat_offer_date = models.DateField(null=True, blank=True)
    ran_sat_offer_date = models.DateField(null=True, blank=True)
    mw_plan_id = models.CharField(max_length=100, null=True, blank=True)
    mw_pat_offer_date = models.DateField(null=True, blank=True)
    rsl_value_status = models.CharField(max_length=100, null=True, blank=True)
    enm_status = models.CharField(max_length=100, null=True, blank=True)
    mw_lkf = models.CharField(max_length=100, null=True, blank=True)
    mw_sat_offer_date = models.DateField(null=True, blank=True)
    mw_ms1_mids_date = models.DateField(null=True, blank=True)
    site_onair_date = models.DateField(null=True, blank=True)
    i_deploy_onair_date = models.DateField(null=True, blank=True)
    current_status = models.CharField(max_length=100, null=True, blank=True)
    # five_g_onair_date = models.DateField(null=True, blank=True)
    rfai_rejected_date = models.DateField(null=True, blank=True)
    re_rfai_date = models.DateField(null=True, blank=True)

    # pri_start_date = models.DateField(null=True, blank=True)
    # pri_close_date = models.DateField(null=True, blank=True)
    # pri_history = models.CharField(max_length=500, null=True, blank=True)
    pri_count = models.IntegerField(null=True, blank=True)
    pri_issue_ageing = models.IntegerField(null=True, blank=True)

    # fiber_issue_start_date = models.DateField(null=True, blank=True)
    # fiber_issue_close_date = models.DateField(null=True, blank=True)
    # material_issue_start_date = models.DateField(null=True, blank=True)
    # material_issue_close_date = models.DateField(null=True, blank=True)
    # mw_issue_start_date = models.DateField(null=True, blank=True)
    # mw_issue_close_date = models.DateField(null=True, blank=True)

    detailed_remarks = models.CharField(max_length=100, null=True, blank=True)
    # manual_history = models.CharField(max_length=100, null=True, blank=True)

    # issue = models.CharField(max_length=100, null=True, blank=True)
    # issue_start_date = models.DateField(null=True, blank=True)
    # issue_close_date = models.DateField(null=True, blank=True)
    # issue_history = models.CharField(max_length=500, null=True, blank=True)
    other_ust_issue_ageing = models.IntegerField(null=True, blank=True)
    other_airtel_issue_ageing = models.IntegerField(null=True, blank=True)

    # clear_rfai_to_ms1_ageing = models.IntegerField(null=True, blank=True)
    total_issue_ageing = models.IntegerField(null=True, blank=True)
    rfai_to_ms1_ageing = models.IntegerField(null=True, blank=True)
    
    ran_pat_accepted_date = models.DateField(null=True, blank=True)
    ran_sat_accepted_date = models.DateField(null=True, blank=True)
    mw_pat_accepted_date = models.DateField(null=True, blank=True)
    mw_sat_accepted_date = models.DateField(null=True, blank=True)
    scft_accepted_date = models.DateField(null=True, blank=True)
    kpi_at_offer_date = models.DateField(null=True, blank=True)
    kpi_at_accepted_date = models.DateField(null=True, blank=True)
    four_g_ms2_date = models.DateField(null=True, blank=True)
    five_g_ms2_date = models.DateField(null=True, blank=True)
    final_ms2_date = models.DateField(null=True, blank=True)
    
     # --- Dismantling & Exit Milestones ---
    dismantling_survey_date = models.DateField(null=True, blank=True)
    sreq_creq_raised_date = models.DateField(null=True, blank=True)
    dismantle_date = models.DateField(null=True, blank=True)
    material_pickup_date = models.DateField(null=True, blank=True)
    material_submission_date = models.DateField(null=True, blank=True)
    oci_done_date = models.DateField(null=True, blank=True)
    sign_off_date = models.DateField(null=True, blank=True)

    # --- Blocking / Issue Flags ---
    dismantling_status = models.CharField(max_length=100, null=True, blank=True)
    # toco_owner_issue = models.CharField(max_length=100, null=True, blank=True)
    # exit_notice_issue = models.CharField(max_length=100, null=True, blank=True)
    # commercial_issue = models.CharField(max_length=100, null=True, blank=True)
    # workable_sites = models.CharField(max_length=100, null=True, blank=True)
    
    last_updated_date = models.DateTimeField(null=True, blank=False)
    last_updated_by = models.CharField(max_length=250, null=True, blank=True)
 
    class Meta:
        db_table = "relocation_tracker"
        # unique_together = ('circle', 'new_site_id')
 
    def __str__(self):
        return f"{self.circle} - {self.new_site_id}"
    
    
class RelocationUser(models.Model):
    RIGHT_CHOICES = [
        ("Admin", "Admin"),
        ("Read", "Read"),
        ("Write", "Write")
    ]
    
    name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=True)
    circles = JSONField(default=list)
    columns = JSONField(default=list)
    right = models.CharField(max_length=50, choices=RIGHT_CHOICES, default="Read")
    updated_by = models.EmailField()
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "relocation_users_live"
        indexes = [
            models.Index(fields=["email"]),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.email})"



class RelocationIssue(models.Model):
    CIRCLE_CHOICES = [
        ("RAJ", "RAJ"),
        ("ASM", "ASM"),
        ("UPW", "UPW"),
        ("AP", "AP"),
        ("JK", "JK"),
        ("CHN", "CHN"),
        ("KK", "KK"),
        ("ROTN", "ROTN"),
        ("MUM", "MUM"),
        ("DEL", "DEL"),
        ("MP", "MP"),
        ("KOL", "KOL"),
        ("ORI", "ORI"),
        ("UPE", "UPE"),
        ("NE", "NE"),
        ("WB", "WB"),
        ("BIH", "BIH"),
        ("PUN", "PUN"),
        ("JRK", "JRK"),
        ("HRY", "HRY"),
    ]
    OWNER_CHOICES = [
        ('MobileComm', 'MobileComm'),
        ('Airtel', 'Airtel')
    ]
    ISSUE_CHOICES = [
        ("PRI", "PRI"),
        ("Fiber", "Fiber"),
        ("MW", "MW"),
        ('Material', 'Material')
    ]
    milestones = [
        "RFAI",
        "Allocation",
        "RFAI Survey",
        "MO Punch",
        "Material Dispatch",
        "Material Delivered",
        "Installation Start",
        "Installation End",
        "Integration",
        "EMF Submission",
        "Alarm Rectification Done",
        "SCFT Done",
        "SCFT I-Deploy Offered",
        "RAN PAT Offer",
        "RAN SAT Offer",
        "MW PAT Offer",
        "MW SAT Offer",
        "MW MS1 MIDS",
        "Site ONAIR",
    ]

    MILESTONE_CHOICES = [(m, m) for m in milestones]
    
    circle = models.CharField(max_length=50, choices=CIRCLE_CHOICES, default="AP")
    site_id = models.CharField(max_length=100, null=True, blank=True)
    issue_owner = models.CharField(max_length=50, choices=OWNER_CHOICES, default="Airtel")
    milestone = models.CharField(max_length=50, choices=MILESTONE_CHOICES, default="RFAI Survey")
    issue_name = models.CharField(max_length=50, choices=ISSUE_CHOICES, default="PRI")
    start_date = models.DateField(null=True, blank=True)
    close_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('Open', 'Open'), ('Closed', 'Closed')], default="Open")
    duration = models.IntegerField(null=True, blank=True)
    remarks = models.CharField(max_length=500, null=True, blank=True)
    updated_by = models.EmailField()
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "relocation_issues"
        indexes = [
            models.Index(fields=["circle"]),
            models.Index(fields=["site_id"]),
            models.Index(fields=["milestone"]),
            models.Index(fields=["issue_owner"]),
        ]
    
    def __str__(self):
        return f"{self.circle} | {self.site_id} | {self.issue_owner} | {self.milestone}"
    

class ATDumpData(models.Model):
    circle = models.CharField(max_length=10)
    site_id = models.CharField(max_length=50)

    on_air_date = models.DateField(null=True, blank=True)
    
    band = models.CharField(max_length=100, null=True, blank=True)

    physical_at_status = models.CharField(max_length=50, null=True, blank=True)
    physical_at_rejection_counter = models.IntegerField(default=0)

    performance_at_status = models.CharField(max_length=50, null=True, blank=True)
    performance_at_rejection_counter = models.IntegerField(default=0)

    soft_at_status = models.CharField(max_length=50, null=True, blank=True)
    soft_at_rejection_counter = models.IntegerField(default=0)

    scft_at_status = models.CharField(max_length=50, null=True, blank=True)
    scft_at_rejection_counter = models.IntegerField(default=0)

    class Meta:
        db_table = "at_dump_data"
        indexes = [
            models.Index(fields=["circle"]),
            models.Index(fields=["site_id"]),
        ]

    def __str__(self):
        return f"{self.site_id} ({self.circle})"
    

class SiteStatus(models.Model):
    site_id = models.CharField(max_length=100)
    date = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.site_id} - {self.date} - {self.status}"