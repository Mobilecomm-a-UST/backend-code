from django.db import models

# Create your models here.


class NTSiteTracker(models.Model):

    # ================= Core =================
    circle = models.CharField(max_length=100, null=True, blank=True)
    site_tagging = models.CharField(max_length=100, null=True, blank=True)

    old_toco_name = models.CharField(max_length=150, null=True, blank=True)
    old_site_id = models.CharField(max_length=100, null=True, blank=True)

    new_site_id = models.CharField(max_length=100, null=True, blank=True)
    new_toco_name = models.CharField(max_length=150, null=True, blank=True)

    sr_number = models.CharField(max_length=100, null=True, blank=True)

    # ================= OEM / Partner =================
    ran_oem = models.CharField(max_length=100, null=True, blank=True)
    media_type = models.CharField(max_length=100, null=True, blank=True)
    mw_oem = models.CharField(max_length=100, null=True, blank=True)
    mw_partner = models.CharField(max_length=100, null=True, blank=True)

    # ================= Relocation =================
    relocation_method = models.CharField(max_length=100, null=True, blank=True)
    relocation_type = models.CharField(max_length=100, null=True, blank=True)

    old_site_band = models.CharField(max_length=50, null=True, blank=True)
    new_site_band = models.CharField(max_length=50, null=True, blank=True)

    # ================= RFAI / Survey =================
    rfai_date = models.DateField(null=True, blank=True)
    allocation_date = models.DateField(null=True, blank=True)
    rfai_survey_date = models.DateField(null=True, blank=True)

    survey_status = models.CharField(max_length=50, null=True, blank=True)   # Accepted / Rejected
    wrfai = models.CharField(max_length=10, null=True, blank=True)          # YES / NO

    nwrfai_reason = models.CharField(max_length=200, null=True, blank=True)
    remarks_for_nwrfai = models.TextField(null=True, blank=True)
    nwrfai_to_wrfai_date = models.DateField(null=True, blank=True)

    # ================= Execution =================
    mo_punch_date = models.DateField(null=True, blank=True)
    material_dispatch_date = models.DateField(null=True, blank=True)
    material_delivered_date = models.DateField(null=True, blank=True)

    installation_start_date = models.DateField(null=True, blank=True)
    installation_end_date = models.DateField(null=True, blank=True)
    integration_date = models.DateField(null=True, blank=True)

    nep_id = models.CharField(max_length=100, null=True, blank=True)
    emf_submission_date = models.DateField(null=True, blank=True)

    # ================= LKF / Alarm =================
    ran_lkf_status = models.CharField(max_length=100, null=True, blank=True)
    alarm_status = models.CharField(max_length=100, null=True, blank=True)
    alarm_rectification_done_date = models.DateField(null=True, blank=True)

    # ================= SCFT / PAT / SAT =================
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

    # ================= ONAIR =================
    site_onair_date = models.DateField(null=True, blank=True)
    i_deploy_onair_date = models.DateField(null=True, blank=True)

    # ================= Status =================
    current_status = models.CharField(max_length=120, null=True, blank=True)
    detailed_remarks = models.TextField(null=True, blank=True)
    manual_history = models.TextField(null=True, blank=True)

    # ================= Rework =================
    rfai_rejected_date = models.DateField(null=True, blank=True)
    re_rfai_date = models.DateField(null=True, blank=True)

    # ================= PRI / Issues =================
    pri_count = models.IntegerField(null=True, blank=True)
    pri_issue_ageing = models.IntegerField(null=True, blank=True)
    other_issue_ageing = models.IntegerField(null=True, blank=True)
    total_issue_ageing = models.IntegerField(null=True, blank=True)
    rfai_to_ms1_ageing = models.IntegerField(null=True, blank=True)

    # ================= Acceptance =================
    ran_pat_accepted_date = models.DateField(null=True, blank=True)
    ran_sat_accepted_date = models.DateField(null=True, blank=True)
    mw_pat_accepted_date = models.DateField(null=True, blank=True)
    mw_sat_accepted_date = models.DateField(null=True, blank=True)
    scft_accepted_date = models.DateField(null=True, blank=True)

    kpi_at_offer_date = models.DateField(null=True, blank=True)
    kpi_at_accepted_date = models.DateField(null=True, blank=True)

    # ================= MS2 =================
    four_g_ms2_date = models.DateField(null=True, blank=True)
    five_g_ms2_date = models.DateField(null=True, blank=True)
    final_ms2_date = models.DateField(null=True, blank=True)

    # ================= Audit =================
    last_updated_date = models.DateTimeField(null=True, blank=True)
    last_updated_by = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        db_table = "nt_site_tracker"
        indexes = [
            models.Index(fields=["circle"]),
            models.Index(fields=["new_site_id"]),
            models.Index(fields=["current_status"]),
        ]

    def __str__(self):
        return f"{self.circle} - {self.new_site_id}"



class NTIssue(models.Model):
    circle = models.CharField(max_length=100, null=True, blank=True)
    site_id = models.CharField(max_length=100, null=True, blank=True)
    issue_owner = models.CharField(max_length=100, null=True, blank=True)
    milestone = models.CharField(max_length=100, null=True, blank=True)
    issue_name = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    close_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    remarks = models.CharField(max_length=500, null=True, blank=True)
    updated_by = models.EmailField()
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "nt_tracking_issues"
        indexes = [
            models.Index(fields=["circle"]),
            models.Index(fields=["site_id"]),
            models.Index(fields=["milestone"]),
            models.Index(fields=["issue_owner"]),
        ]
    
    def __str__(self):
        return f"{self.circle} | {self.site_id} | {self.issue_owner} | {self.milestone}"
   