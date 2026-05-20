from django.db import models
class NTSiteTracker(models.Model):
    circle = models.CharField(max_length=100, null=True, blank=True)
    site_id = models.CharField(max_length=100, null=True, blank=True)

    project_nt = models.CharField(max_length=150, null=True, blank=True)
    tur_breakup= models.CharField(max_length=100, null=True, blank=True)

    new_toco_name = models.CharField(max_length=150, null=True, blank=True)
    sr_number = models.CharField(max_length=100, null=True, blank=True)

    ran_oem = models.CharField(max_length=100, null=True, blank=True)
    media_type = models.CharField(max_length=100, null=True, blank=True)
    mw_oem = models.CharField(max_length=100, null=True, blank=True)
    mw_nstallation_partner = models.CharField(max_length=100, null=True, blank=True)

    site_band=models.CharField(max_length=50, null=True, blank=True)
    rfai_date = models.DateField(null=True, blank=True)
    allocation_date = models.DateField(null=True, blank=True)
    rfai_survey_date = models.DateField(null=True, blank=True)

    survey_status = models.CharField(max_length=50, null=True, blank=True)   # Accepted / Rejected
    wrfai = models.CharField(max_length=10, null=True, blank=True)          # YES / NO
   
    mo_punch_date = models.DateField(null=True, blank=True)
    material_dispatch_date = models.DateField(null=True, blank=True)
    material_delivered_date = models.DateField(null=True, blank=True)

    material_type_hw=models.CharField(max_length=100, null=True, blank=True)
    material_type_im=models.CharField(max_length=100, null=True, blank=True)
    

    installation_start_date = models.DateField(null=True, blank=True)
    installation_end_date = models.DateField(null=True, blank=True)
    integration_date = models.DateField(null=True, blank=True)
    Sacfa_Appied_date=models.DateField(null=True, blank=True)
    wpc_no=models.CharField(max_length=100, null=True, blank=True)
    wpc_date=models.DateField(null=True, blank=True)

    nep_id = models.CharField(max_length=100, null=True, blank=True)
    emf_submission_date = models.DateField(null=True, blank=True)

    ran_lkf_status = models.CharField(max_length=100, null=True, blank=True)
    alarm_status = models.CharField(max_length=100, null=True, blank=True)
    alarm_rectification_done_date = models.DateField(null=True, blank=True)

    scft_done_date = models.DateField(null=True, blank=True)
    scft_offered_date = models.DateField(null=True, blank=True)

    ran_pat_offer_date = models.DateField(null=True, blank=True)
    ran_sat_offer_date = models.DateField(null=True, blank=True)

    mw_plan_id = models.CharField(max_length=100, null=True, blank=True)
    mw_pat_offer_date = models.DateField(null=True, blank=True)

    rsl_value_status = models.CharField(max_length=100, null=True, blank=True)
    enm_status = models.CharField(max_length=100, null=True, blank=True)
    mw_lkf = models.CharField(max_length=100, null=True, blank=True)
    mw_sat_offer_date = models.DateField(null=True, blank=True)
    mw_ms1_mids_date = models.DateField(null=True, blank=True)
    
    mw_sacfa_a_end = models.CharField(max_length=100, null=True, blank=True)
    mw_wpc_a_end   = models.CharField(max_length=100, null=True, blank=True)
    mw_sacfa_b_end = models.CharField(max_length=100, null=True, blank=True)
    mw_wpc_b_end   = models.CharField(max_length=100, null=True, blank=True)


    site_onair_date = models.DateField(null=True, blank=True)
    i_deploy_onair_date = models.DateField(null=True, blank=True)


    current_status = models.CharField(max_length=120, null=True, blank=True)
    ideploy_status= models.CharField(max_length=120, null=True, blank=True)
    detailed_remarks = models.TextField(null=True, blank=True)
   

    rfai_rejected_date = models.DateField(null=True, blank=True)
    ideploy_pri_taging =models.CharField(max_length=120, null=True, blank=True)
    re_rfai_date = models.DateField(null=True, blank=True)


    pri_count = models.IntegerField(null=True, blank=True)
    pri_issue_ageing = models.IntegerField(null=True, blank=True)
    other_ust_issue_ageing = models.IntegerField(null=True, blank=True)
    other_airtel_issue_ageing = models.IntegerField(null=True, blank=True)
    total_issue_ageing = models.IntegerField(null=True, blank=True)
    clear_rfai_ms1_ageing=models.IntegerField(null=True, blank=True)
    
    rfai_to_ms1_ageing = models.IntegerField(null=True, blank=True)


    ran_pat_accepted_date = models.DateField(null=True, blank=True)
    ran_sat_accepted_date = models.DateField(null=True, blank=True)
    mw_pat_accepted_date = models.DateField(null=True, blank=True)
    mw_sat_accepted_date = models.DateField(null=True, blank=True)
    scft_accepted_date = models.DateField(null=True, blank=True)

    kpi_at_offer_date = models.DateField(null=True, blank=True)
    kpi_at_accepted_date = models.DateField(null=True, blank=True)


    four_g_ms2_date = models.DateField(null=True, blank=True)
    ssid= models.CharField(max_length=150, null=True, blank=True)
    pmis_month = models.DateField(null=True, blank=True)
    airtel_sign_off=models.CharField(max_length=150, null=True, blank=True)

    last_updated_date = models.DateTimeField(null=True, blank=True)
    last_updated_by = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        db_table = "nt_site_tracker"
        indexes = [
            models.Index(fields=["circle"]),
            models.Index(fields=["site_id"]),
            models.Index(fields=["current_status"]),
        ]

    def __str__(self):
        return f"{self.circle} - {self.site_id}"



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
   