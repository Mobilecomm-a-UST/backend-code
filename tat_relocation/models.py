from django.db import models

class TrackerModel(models.Model):

    # -------------------- BASIC DETAILS --------------------
    circle = models.CharField(max_length=100, null=True, blank=True, db_column="Circle")
    site_tagging = models.CharField(max_length=100, null=True, blank=True, db_column="Site Tagging")
    old_toco_name = models.CharField(max_length=100, null=True, blank=True, db_column="Old TOCO Name")
    old_site_id = models.CharField(max_length=100, null=True, blank=True, db_column="Old Site Id")
    new_site_id = models.CharField(max_length=100, null=True, blank=True, db_column="New Site ID")
    new_toco_name = models.CharField(max_length=100, null=True, blank=True, db_column="New TOCO Name")
    sr_number = models.CharField(max_length=100, null=True, blank=True, db_column="SR Number")
    ran_oem = models.CharField(max_length=100, null=True, blank=True, db_column="RAN OEM")
    media_type = models.CharField(max_length=100, null=True, blank=True, db_column="Media Type")
    mw_oem = models.CharField(max_length=100, null=True, blank=True, db_column="MW OEM")
    relocation_method = models.CharField(max_length=100, null=True, blank=True, db_column="Relocation Method")
    relocation_type = models.CharField(max_length=100, null=True, blank=True, db_column="Relocation Type")
    old_site_band = models.CharField(max_length=100, null=True, blank=True, db_column="OLD Site Band")
    new_site_band = models.CharField(max_length=100, null=True, blank=True, db_column="New Site Band")
    nbd = models.CharField(max_length=100, null=True, blank=True, db_column="NBD")

    # -------------------- RFAI --------------------
    workable_rfai_date = models.DateField(null=True, blank=True, db_column="Workable RFAI Date")
    short_reason_for_workable_rfai = models.CharField(max_length=255, null=True, blank=True, db_column="Short Reason for Workable RFAI Date")
    reason_for_workable_rfai = models.TextField(null=True, blank=True, db_column="Reason for Workable RFAI Date")
    rerfai_date = models.DateField(null=True, blank=True, db_column="ReRFAI Date")
    rfai_date = models.DateField(null=True, blank=True, db_column="RFAI Date")

    # -------------------- ALLOCATION --------------------
    allocation_date = models.DateField(null=True, blank=True, db_column="Allocation Date")
    rfai_vs_allocation_gap_days = models.IntegerField(null=True, blank=True, db_column="Rfai Vs Allocation Gap in Days")
    rfai_vs_allocation_gap_group = models.IntegerField(null=True, blank=True, db_column="Rfai Vs Allocation-Gap group")
    rfai_vs_allocation_tat_matrix = models.IntegerField(null=True, blank=True, db_column="Rfai Vs Allocation-TAT Matrix")
    short_allocation_remarks = models.CharField(max_length=255, null=True, blank=True, db_column="Short Allocation Remarks")
    allocation_owner = models.CharField(max_length=100, null=True, blank=True, db_column="Allocation Owner")

    # -------------------- SURVEY --------------------
    rfai_survey_date = models.DateField(null=True, blank=True, db_column="RFAI Survey Date")
    allocation_vs_survey_gap_days = models.IntegerField(null=True, blank=True, db_column="Allocation Vs Survey Gap in Days")
    allocation_vs_survey_gap_group = models.IntegerField(null=True, blank=True, db_column="Allocation Vs Survey-Gap group")
    allocation_vs_survey_tat_matrix = models.IntegerField(null=True, blank=True, db_column="Allocation Vs Survey-TAT Matrix")
    short_survey_remarks = models.CharField(max_length=255, null=True, blank=True, db_column="Short Survey Remarks")
    survey_owner = models.CharField(max_length=100, null=True, blank=True, db_column="Survey Owner")

    # -------------------- MO --------------------
    mo_punch_date = models.DateField(null=True, blank=True, db_column="MO Punch Date")
    survey_vs_mo_gap_days = models.IntegerField(null=True, blank=True, db_column="Survey Vs MO Gap in Days")
    survey_vs_mo_gap_group = models.IntegerField(null=True, blank=True, db_column="Survey Vs MO -Gap group")
    survey_vs_mo_tat_matrix = models.IntegerField(null=True, blank=True, db_column="Survey Vs MO -TAT Matrix")
    short_mo_remarks = models.CharField(max_length=255, null=True, blank=True, db_column="Short MO Remarks")
    mo_owner = models.CharField(max_length=100, null=True, blank=True, db_column="MO Owner")
    rfai_vs_mo_reason = models.CharField(max_length=255, null=True, blank=True, db_column="RFAI Vs MO reason")

    # -------------------- MATERIAL --------------------
    material_dispatch_date = models.DateField(null=True, blank=True, db_column="Material Dispatch Date")
    mo_vs_md_gap_days = models.IntegerField(null=True, blank=True, db_column="MO Vs MD Gap in Days")
    mo_vs_md_gap_group = models.IntegerField(null=True, blank=True, db_column="MO Vs MD -Gap group")
    mo_vs_md_tat_matrix = models.IntegerField(null=True, blank=True, db_column="MO Vs MD -TAT Matrix")
    short_md_remarks = models.CharField(max_length=255, null=True, blank=True, db_column="Short MD Remarks")
    md_owner = models.CharField(max_length=100, null=True, blank=True, db_column="MD Owner")

    material_delivered_date = models.DateField(null=True, blank=True, db_column="Material Delivered Date")
    md_vs_mos_gap_days = models.IntegerField(null=True, blank=True, db_column="MD Vs MOS Gap in Days")
    md_vs_mos_gap_group = models.IntegerField(null=True, blank=True, db_column="MD Vs MOS -Gap group")
    md_vs_mos_tat_matrix = models.IntegerField(null=True, blank=True, db_column="MD Vs MOS -TAT Matrix")
    short_mos_remarks = models.CharField(max_length=255, null=True, blank=True, db_column="Short MOS Remarks")
    mos_owner = models.CharField(max_length=100, null=True, blank=True, db_column="MOS Owner")

    # -------------------- INSTALLATION --------------------
    installation_start_date = models.DateField(null=True, blank=True, db_column="Installation Start Date")
    installation_end_date = models.DateField(null=True, blank=True, db_column="Installation End Date")
    mos_vs_inc_gap_days = models.IntegerField(null=True, blank=True, db_column="MOS Vs INC Gap in Days")
    mos_vs_inc_gap_group = models.IntegerField(null=True, blank=True, db_column="MOS Vs INC -Gap group")
    mos_vs_inc_tat_matrix = models.IntegerField(null=True, blank=True, db_column="MOS Vs INC -TAT Matrix")
    short_inc_remarks = models.CharField(max_length=255, null=True, blank=True, db_column="Short INC Remarks")
    inc_owner = models.CharField(max_length=100, null=True, blank=True, db_column="INC Owner")

    # -------------------- INTEGRATION --------------------
    integration_date = models.DateField(null=True, blank=True, db_column="Integration Date")
    inc_vs_ix_gap_days = models.IntegerField(null=True, blank=True, db_column="INC Vs IX Gap in Days")
    inc_vs_ix_gap_group = models.IntegerField(null=True, blank=True, db_column="INC Vs IX -Gap group")
    inc_vs_ix_tat_matrix = models.IntegerField(null=True, blank=True, db_column="INC Vs IX -TAT Matrix")
    short_ix_remarks = models.CharField(max_length=255, null=True, blank=True, db_column="Short IX Remarks")
    ix_owner = models.CharField(max_length=100, null=True, blank=True, db_column="IX Owner")

    # -------------------- EMF --------------------
    emf_submission_date = models.DateField(null=True, blank=True, db_column="EMF Submission Date")
    ix_vs_emf_gap_days = models.IntegerField(null=True, blank=True, db_column="IX Vs EMF Gap in Days")
    ix_vs_emf_gap_group = models.IntegerField(null=True, blank=True, db_column="IX Vs EMF -Gap group")
    ix_vs_emf_tat_matrix = models.IntegerField(null=True, blank=True, db_column="IX Vs EMF -TAT Matrix")
    short_emf_remarks = models.CharField(max_length=255, null=True, blank=True, db_column="Short EMF Remarks")
    emf_owner = models.CharField(max_length=100, null=True, blank=True, db_column="EMFOwner")

    # -------------------- SCFT --------------------
    ran_lkf_status = models.CharField(max_length=100, null=True, blank=True, db_column="RAN LKF Status")
    alarm_status = models.CharField(max_length=100, null=True, blank=True, db_column="Alarm Status")
    alarm_rectification_done_date = models.DateField(null=True, blank=True, db_column="Alarm Rectification Done Date")
    scft_done_date = models.DateField(null=True, blank=True, db_column="SCFT Done Date")
    scft_i_deploy_offered_date = models.DateField(null=True, blank=True, db_column="SCFT I-Deploy Offered Date")
    emf_vs_scft_gap_days = models.IntegerField(null=True, blank=True, db_column="EMF Vs SCFT Gap in Days")
    emf_vs_scft_gap_group = models.IntegerField(null=True, blank=True, db_column="EMF Vs SCFT -Gap group")
    emf_vs_scft_tat_matrix = models.IntegerField(null=True, blank=True, db_column="EMF Vs SCFT -TAT Matrix")
    short_scft_remarks = models.CharField(max_length=255, null=True, blank=True, db_column="Short SCFT Remarks")
    scft_owner = models.CharField(max_length=100, null=True, blank=True, db_column="SCFT Owner")

    #-------------------- PAT  --------------------
    ran_pat_offer_date = models.DateField(null=True, blank=True, db_column="RAN PAT Offer Date")
    ix_vs_pat_gap_in_days = models.IntegerField(null=True, blank=True, db_column="IX Vs PAT Gap in Days")
    ix_vs_pat_gap_group = models.CharField(max_length=100, null=True, blank=True, db_column="IX Vs PAT -Gap group")
    short_pat_remarks = models.CharField(max_length=255, null=True, blank=True, db_column="Short PAT Remarks")
    pat_owner = models.CharField(max_length=100, null=True, blank=True, db_column="PAT Owner")


    #--------------------SAT --------------------
    ran_sat_offer_date = models.DateField(null=True, blank=True, db_column="RAN SAT Offer Date")
    emf_vs_sat_gap_in_days = models.IntegerField(null=True, blank=True, db_column="EMF Vs SAT Gap in Days")
    emf_vs_sat_gap_group = models.CharField(max_length=100, null=True, blank=True, db_column="EMF Vs SAT -Gap group")
    short_sat_remarks = models.CharField(max_length=255, null=True, blank=True, db_column="Short SAT Remarks")
    sat_owner = models.CharField(max_length=100, null=True, blank=True, db_column="SAT Owner")
    mw_plane_id = models.CharField(max_length=100, null=True, blank=True, db_column="MW Plan ID")
    mw_pat_offer_date = models.DateField(null=True, blank=True, db_column="MW PAT Offer Date")
    rsl_value_status = models.CharField(max_length=100, null=True, blank=True, db_column="RSL Value Status")
    enm_status = models.CharField(max_length=100, null=True, blank=True, db_column="ENM Status")
    mw_lkf = models.CharField(max_length=100, null=True, blank=True, db_column="MW LKF")
    mw_sat_offer_date = models.DateField(null=True, blank=True, db_column="MW SAT Offer Date")
    mw_ms1_mids_date = models.DateField(null=True, blank=True, db_column="MW MS1 MIDS Date")



    # ============================= MS1 / STATUS =============================
    site_onair_date = models.DateField(null=True, blank=True, db_column="Site ONAIR Date")
    i_deploy_onair_date = models.DateField(null=True, blank=True, db_column="I-Deploy ONAIR Date")
    ms1_month = models.CharField(max_length=50, null=True, blank=True, db_column="MS1 Month")
    scft_vs_ms1_gap_days = models.IntegerField(null=True, blank=True, db_column="SCFT Vs MS1 Gap in Days")
    scft_vs_ms1_gap_group = models.CharField(max_length=100, null=True, blank=True, db_column="SCFT Vs MS1 -Gap group")
    scft_vs_ms1_tat = models.IntegerField(null=True, blank=True, db_column="SCFT Vs MS1 -TAT Matrix")
    short_ms1_remarks = models.CharField(max_length=255, null=True, blank=True, db_column="Short MS1 Remarks")
    ms1_owner = models.CharField(max_length=100, null=True, blank=True, db_column="MS1 Owner")


    # ============================= OWNERSHIP / AGEING =============================
    ownership_airtel_days = models.IntegerField(null=True, blank=True, db_column="Ownership Airtel - days")
    ownership_airtel_reasons = models.TextField(null=True, blank=True, db_column="Ownership Airtel - Reasons")

    ownership_toco_days = models.IntegerField(null=True, blank=True, db_column="Ownership Toco - days")
    ownership_toco_reasons = models.TextField(null=True, blank=True, db_column="Ownership Toco -Reasons")

    ownership_mcomm_days = models.IntegerField(null=True, blank=True, db_column="Ownership Mcomm - days")
    ownership_mcomm_reasons = models.TextField(null=True, blank=True, db_column="Ownership Mcomm - Reasons")

    total_issue_days_airtel_toco = models.IntegerField(
        null=True, blank=True,
        db_column="ToTal No of Issues days- (Airtel Days +Toco Days)"
    )

    # ============================= RFAI vs MS1 Ageing =============================
    rfai_vs_ms1_ageing = models.IntegerField(null=True, blank=True, db_column="RFAI vs MS1 Ageing")
    rfai_vs_ms1_ageing_group = models.CharField(max_length=100, null=True, blank=True, db_column="RFAI vs MS1 Ageing  Group")
    rfai_vs_ms1_ageing_tat = models.IntegerField(null=True, blank=True, db_column="RFAI vs MS1 Ageing TAT")

    rfai_vs_ms1_ageing_excluding_issues_days = models.IntegerField(
        null=True, blank=True,
        db_column="RFAI vs MS1 Ageing (Excluding Issues days)"
    )
    rfai_vs_ms1_ageing_group_excluding_issues_days = models.CharField(
        max_length=100, null=True, blank=True,
        db_column="RFAI vs MS1 Ageing  Group  (Excluding Issues days)"
    )
    rfai_vs_ms1_ageing_tat_excluding_issues_days = models.IntegerField(
        null=True, blank=True,
        db_column="RFAI vs MS1 Ageing TAT  (Excluding Issues days)"
    )

    wrfai_vs_ms1_ageing = models.IntegerField(null=True, blank=True, db_column="WRFAI vs MS1 Ageing")
    wrfai_vs_ms1_ageing_group = models.CharField(max_length=100, null=True, blank=True, db_column="WRFAI vs MS1 Ageing  Group")
    wrfai_vs_ms1_ageing_tat = models.IntegerField(null=True, blank=True, db_column="WRFAI vs MS1 Ageing TAT")

    # ============================= STAGE & STATUS =============================
    stage = models.CharField(max_length=100, null=True, blank=True, db_column="Stage")
    tat_matrix_remarks = models.TextField(null=True, blank=True, db_column="TAT Matrix Remarks")
    current_status = models.CharField(max_length=200, null=True, blank=True, db_column="Current Status")
    detailed_remarks = models.TextField(null=True, blank=True, db_column="Detailed Remarks")
    manual_history = models.TextField(null=True, blank=True, db_column="Manual History")

    # ============================= FIBRE DEPENDENCY =============================
    dependency_fibre = models.BooleanField(default=False, db_column="Dependency Fibre")
    for_fiber_so_target_date = models.DateField(null=True, blank=True, db_column="For Fiber -SO_TARGET_DATE")
    for_fiber_so_target_date_plus_1_month = models.DateField(null=True, blank=True, db_column="For Fiber -SO_TARGET_DATE+1 month")
    for_fiber_so_target_date_ageing = models.DateField(null=True, blank=True, db_column="For Fiber -SO_TARGET_DATE-Ageing")
    for_fiber_so_target_date_groupageing = models.DateField(null=True, blank=True, db_column="For Fiber -SO_TARGET_DATE-GroupAgeing")

    fibre_issue_occurred_post_workable = models.BooleanField(default=False, db_column="Fibre issue occoured post Workable")
    fibre_issue_occurred_post_workable_tat = models.IntegerField(null=True, blank=True, db_column="Fibre issue occoured post Workable -TAT")

    # ============================= MW / FTTH / MATERIAL =============================
    mw_issue_occurred_post_workable = models.BooleanField(default=False, db_column="MW issue occoured post Workable")
    mw_issue_occurred_post_workable_tat = models.IntegerField(null=True, blank=True, db_column="MW issue occoured post Workable -TAT")

    ftth_issue_occurred_post_workable = models.BooleanField(default=False, db_column="FTTH issue occoured post Workable")
    ftth_issue_occurred_post_workable_tat = models.IntegerField(null=True, blank=True, db_column="FTTH issue occoured post Workable -TAT")

    dependency_material = models.BooleanField(default=False, db_column="Dependency Material")
    dependency_material_tat = models.IntegerField(null=True, blank=True, db_column="Dependency Material-TAT")

    material_faulty_post_mos = models.BooleanField(default=False, db_column="Material faulty post MOS")
    material_faulty_post_mos_tat = models.IntegerField(null=True, blank=True, db_column="Material faulty post MOS TAT")

    material_shortage_srn_kitty = models.BooleanField(
    default=False,
    db_column="Material Shortage from SRN kitty"
    )

    material_shortage_srn_kitty_tat = models.IntegerField(
        null=True,
        blank=True,
        db_column="Material Shortage from SRN kitty TAT"
    )

    material_stuck_at_old_site = models.BooleanField(
        default=False,
        db_column="Material stuck at Old site (BBM case)"
    )
    material_stuck_at_old_site_tat = models.IntegerField(
        null=True, blank=True,
        db_column="Material stuck at Old site (BBM case) TAT"
    )

    # ============================= PRI / RFAI REJECTION =============================
    pri_rfai_rejected_tagged_on_ideploy = models.BooleanField(
        default=False,
        db_column="PRI/RFAI Rejected Tagged on I-deploy (Yes /No)"
    )
    rfai_rejected_date = models.DateField(null=True, blank=True, db_column="RFAI Rejected Date")
    re_rfai_ideploy_date = models.DateField(null=True, blank=True, db_column="Re-RFAI -I-deploy Date")
    rfai_rejected_reason = models.TextField(null=True, blank=True, db_column="RFAI Rejected Reason")

    dependency_toco_issue_pre_workable_ageing = models.IntegerField(
        null=True, blank=True,
        db_column="Dependency  toco issue pre workable (PRI/RFI Rejection/Far end)-Ageing"
    )
    dependency_toco_issue_pre_workable_tat = models.IntegerField(
        null=True, blank=True,
        db_column="Dependency; toco issue pre workable (PRI/RFI Rejection/Far end)-TAT"
    )

    dependency_toco_issue_post_workable_ageing = models.IntegerField(
        null=True, blank=True,
        db_column="Dependency; toco issue post workable-Ageing"
    )
    dependency_toco_issue_post_workable_tat = models.IntegerField(
        null=True, blank=True,
        db_column="Dependency; toco issue post workable-TAT"
    )

    # ============================= PRI DETAILS =============================
    pri_issue = models.CharField(max_length=200, null=True, blank=True, db_column="PRI Issue")
    pri_sub_issue = models.CharField(max_length=200, null=True, blank=True, db_column="PRI Sub Issue")
    pri_count = models.IntegerField(null=True, blank=True, db_column="PRI Count")
    total_pri_days = models.IntegerField(null=True, blank=True, db_column="Total PRI Days")

    dependency_toco_issue_cleared_pre_workable = models.IntegerField(
        null=True, blank=True,
        db_column="Dependency; toco issue cleared pre workable (PRI/RFI /Far endRejection)"
    )
    dependency_toco_issue_cleared_post_workable = models.IntegerField(
        null=True, blank=True,
        db_column="Dependency; toco issue cleared post workable (PRI/RFI/Far end Rejection)"
    )

    pri_issue_ageing = models.IntegerField(null=True, blank=True, db_column="PRI Issue Ageing")
    other_issue_ageing = models.IntegerField(null=True, blank=True, db_column="Other Issue Ageing")
    total_issue_ageing = models.IntegerField(null=True, blank=True, db_column="Total Issue Ageing")
    rfai_to_ms1_ageing = models.IntegerField(null=True, blank=True, db_column="RFAI to MS1 Ageing")

    # ============================= ACCEPTANCE / KPI / MS2 =============================
    ran_pat_accepted_date = models.DateField(null=True, blank=True, db_column="RAN PAT Accepted Date")
    ran_sat_accepted_date = models.DateField(null=True, blank=True, db_column="RAN SAT Accepted Date")
    mw_pat_accepted_date = models.DateField(null=True, blank=True, db_column="MW PAT Accepted Date")
    mw_sat_accepted_date = models.DateField(null=True, blank=True, db_column="MW SAT Accepted Date")
    scft_accepted_date = models.DateField(null=True, blank=True, db_column="SCFT Accepted Date")

    kpi_at_offer_date = models.DateField(null=True, blank=True, db_column="KPI AT offer Date")
    kpi_at_accepted_date = models.DateField(null=True, blank=True, db_column="KPI AT Accepted Date")

    ms2_4g_date = models.DateField(null=True, blank=True, db_column="4G MS2 Date")
    ms2_5g_date = models.DateField(null=True, blank=True, db_column="5G MS2 Date")
    final_ms2_date = models.DateField(null=True, blank=True, db_column="Final MS2 Date")

    # ============================= DISMANTLING =============================
    dismantling_survey_date = models.DateField(db_column="Dismantling Survey Date", null=True, blank=True)
    sreq_creq_raised_date = models.DateField(null=True, blank=True, db_column="SREQ/CREQ Raised Date")

    dismantle_date = models.DateField(db_column="Dismantle Date", null=True, blank=True)
    material_pickup_date = models.DateField(db_column="Material Pickup Date", null=True, blank=True)
    material_submission_date = models.DateField(db_column="Material Submission Date", null=True, blank=True)
    oci_done_date = models.DateField(db_column="OCI Done Date", null=True, blank=True)
    sign_off_date = models.DateField(db_column="Sign-off Date", null=True, blank=True)
    dismantling_status = models.CharField(max_length=100, db_column="Dismantling Status", null=True, blank=True)

    # ============================= AUDIT =============================
    last_updated_date = models.DateTimeField(db_column="Last Updated Date", auto_now=True)
    last_updated_by = models.CharField(max_length=150, db_column="Last Updated By", null=True, blank=True)
    rfai_rejected = models.CharField(max_length=50, db_column="RFAI Rejected", null=True, blank=True)
    reason = models.CharField(max_length=50, db_column= "reason", null=True, blank=True)
    His = models.CharField(max_length=50, db_column= "His", null=True, blank=True)
    rerfai = models.CharField(max_length=50, db_column= "Rerfai", null=True, blank=True)
    class Meta:
        unique_together = ('circle', 'new_site_id')

    def __str__(self):
        return f"SiteTracking - {self.id}"



    # Continue same pattern for remaining fields...
# class TrackerModel(models.Model):

#     # -------------------- BASIC DETAILS --------------------
#     circle = models.CharField(max_length=100, null=True, blank=True)
#     site_tagging = models.CharField(max_length=100, null=True, blank=True)
#     old_toco_name = models.CharField(max_length=100, null=True, blank=True)
#     old_site_id = models.CharField(max_length=100, null=True, blank=True)
#     new_site_id = models.CharField(max_length=100, null=True, blank=True)
#     new_toco_name = models.CharField(max_length=100, null=True, blank=True)
#     sr_number = models.CharField(max_length=100, null=True, blank=True)
#     ran_oem = models.CharField(max_length=100, null=True, blank=True)
#     media_type = models.CharField(max_length=100, null=True, blank=True)
#     mw_oem = models.CharField(max_length=100, null=True, blank=True)
#     relocation_method = models.CharField(max_length=100, null=True, blank=True)
#     relocation_type = models.CharField(max_length=100, null=True, blank=True)
#     old_site_band = models.CharField(max_length=100, null=True, blank=True)
#     new_site_band = models.CharField(max_length=100, null=True, blank=True)
#     nbd = models.CharField(max_length=100, null=True, blank=True)

#     # -------------------- RFAI --------------------
#     workable_rfai_date = models.DateField(null=True, blank=True)
#     short_reason_for_workable_rfai = models.CharField(max_length=255, null=True, blank=True)
#     reason_for_workable_rfai = models.TextField(null=True, blank=True)
#     rerfai_date = models.DateField(null=True, blank=True)
#     rfai_date = models.DateField(null=True, blank=True)

#     # -------------------- ALLOCATION --------------------
#     allocation_date = models.DateField(null=True, blank=True)
#     rfai_vs_allocation_gap_days = models.IntegerField(null=True, blank=True)
#     rfai_vs_allocation_gap_group = models.IntegerField(null=True, blank=True)
#     rfai_vs_allocation_tat_matrix = models.IntegerField(null=True, blank=True)
#     short_allocation_remarks = models.CharField(max_length=255, null=True, blank=True)
#     allocation_owner = models.CharField(max_length=100, null=True, blank=True)

#     # -------------------- SURVEY --------------------
#     rfai_survey_date = models.DateField(null=True, blank=True)
#     allocation_vs_survey_gap_days = models.IntegerField(null=True, blank=True)
#     allocation_vs_survey_gap_group = models.IntegerField(null=True, blank=True)
#     allocation_vs_survey_tat_matrix = models.IntegerField(null=True, blank=True)
#     short_survey_remarks = models.CharField(max_length=255, null=True, blank=True)
#     survey_owner = models.CharField(max_length=100, null=True, blank=True)

#     # -------------------- MO --------------------
#     mo_punch_date = models.DateField(null=True, blank=True)
#     survey_vs_mo_gap_days = models.IntegerField(null=True, blank=True)
#     survey_vs_mo_gap_group = models.IntegerField(null=True, blank=True)
#     survey_vs_mo_tat_matrix = models.IntegerField(null=True, blank=True)
#     short_mo_remarks = models.CharField(max_length=255, null=True, blank=True)
#     mo_owner = models.CharField(max_length=100, null=True, blank=True)

#     # -------------------- MATERIAL --------------------
#     material_dispatch_date = models.DateField(null=True, blank=True)
#     mo_vs_md_gap_days = models.IntegerField(null=True, blank=True)
#     mo_vs_md_gap_group = models.IntegerField(null=True, blank=True)
#     mo_vs_md_tat_matrix = models.IntegerField(null=True, blank=True)
#     short_md_remarks = models.CharField(max_length=255, null=True, blank=True)
#     md_owner = models.CharField(max_length=100, null=True, blank=True)

#     material_delivered_date = models.DateField(null=True, blank=True)
#     md_vs_mos_gap_days = models.IntegerField(null=True, blank=True)
#     md_vs_mos_gap_group = models.IntegerField(null=True, blank=True)
#     md_vs_mos_tat_matrix = models.IntegerField(null=True, blank=True)
#     short_mos_remarks = models.CharField(max_length=255, null=True, blank=True)
#     mos_owner = models.CharField(max_length=100, null=True, blank=True)

#     # -------------------- INSTALLATION --------------------
#     installation_start_date = models.DateField(null=True, blank=True)
#     installation_end_date = models.DateField(null=True, blank=True)
#     mos_vs_inc_gap_days = models.IntegerField(null=True, blank=True)
#     mos_vs_inc_gap_group = models.IntegerField(null=True, blank=True)
#     mos_vs_inc_tat_matrix = models.IntegerField(null=True, blank=True)
#     short_inc_remarks = models.CharField(max_length=255, null=True, blank=True)
#     inc_owner = models.CharField(max_length=100, null=True, blank=True)

#     # -------------------- INTEGRATION --------------------
#     integration_date = models.DateField(null=True, blank=True)
#     inc_vs_ix_gap_days = models.IntegerField(null=True, blank=True)
#     inc_vs_ix_gap_group = models.IntegerField(null=True, blank=True)
#     inc_vs_ix_tat_matrix = models.IntegerField(null=True, blank=True)
#     short_ix_remarks = models.CharField(max_length=255, null=True, blank=True)
#     ix_owner = models.CharField(max_length=100, null=True, blank=True)

#     # -------------------- EMF --------------------
#     emf_submission_date = models.DateField(null=True, blank=True)
#     ix_vs_emf_gap_days = models.IntegerField(null=True, blank=True)
#     ix_vs_emf_gap_group = models.IntegerField(null=True, blank=True)
#     ix_vs_emf_tat_matrix = models.IntegerField(null=True, blank=True)
#     short_emf_remarks = models.CharField(max_length=255, null=True, blank=True)
#     emf_owner = models.CharField(max_length=100, null=True, blank=True)

#     # -------------------- SCFT --------------------
#     ran_lkf_status = models.CharField(max_length=100, null=True, blank=True)
#     alarm_status = models.CharField(max_length=100, null=True, blank=True)
#     alarm_rectification_done_date = models.DateField(null=True, blank=True)

#     scft_done_date = models.DateField(null=True, blank=True)
#     scft_i_deploy_offered_date = models.DateField(null=True, blank=True)
#     emf_vs_scft_gap_days = models.IntegerField(null=True, blank=True)
#     emf_vs_scft_gap_group = models.IntegerField(null=True, blank=True)
#     emf_vs_scft_tat_matrix = models.IntegerField(null=True, blank=True)
#     short_scft_remarks = models.CharField(max_length=255, null=True, blank=True)
#     scft_owner = models.CharField(max_length=100, null=True, blank=True)

#     # -------------------- PAT  --------------------
#     ran_pat_offer_date = models.DateField(null=True, blank=True)
#     ix_vs_pat_gap_in_days = models.IntegerField(null=True, blank=True)
#     ix_vs_pat_gap_group = models.IntegerField(null=True, blank=True)
#     short_pat_remarks = models.CharField(max_length=255, null=True, blank=True)
#     pat_owner = models.CharField(max_length=100, null=True, blank=True)

#     #--------------------SAT --------------------
#     ran_sat_offer_date = models.DateField(null=True, blank=True)
#     emf_vs_sat_gap_in_days = models.IntegerField(null=True, blank=True)
#     emf_vs_sat_gap_group = models.IntegerField(null=True, blank=True)
#     short_sat_remarks = models.CharField(max_length=255, null=True, blank=True)
#     sat_owner = models.CharField(max_length=100, null=True, blank=True)
#     mw_plane_id = models.CharField(max_length=100, null=True, blank=True)
#     mw_pat_offer_date = models.DateField(null=True, blank=True)
#     rsl_value_status = models.CharField(max_length=100, null=True, blank=True)
#     enm_status = models.CharField(max_length=100, null=True, blank=True)
#     mw_lkf = models.CharField(max_length=100, null=True, blank=True)
#     mw_sat_offer_date = models.DateField(null=True, blank=True)
#     mw_ms1_mids_date = models.DateField(null=True, blank=True)



#     # -------------------- ONAIR / MS1 --------------------
#     site_onair_date = models.DateField(null=True, blank=True)
#     i_deploy_onair_date = models.DateField(null=True, blank=True)
#     ms1_month = models.CharField(max_length=50, null=True, blank=True)

#     scft_vs_ms1_gap_days = models.IntegerField(null=True, blank=True)
#     scft_vs_ms1_gap_group = models.IntegerField(null=True, blank=True)
#     scft_vs_ms1_tat = models.IntegerField(null=True, blank=True)
#     short_ms1_remarks = models.CharField(max_length=255, null=True, blank=True)
#     ms1_owner = models.CharField(max_length=100, null=True, blank=True)

#     # -------------------- OWNERSHIP / AGEING --------------------
#     ownership_airtel_days = models.IntegerField(null=True, blank=True)
#     ownership_airtel_reasons = models.TextField(null=True, blank=True)

#     ownership_toco_days = models.IntegerField(null=True, blank=True)
#     ownership_toco_reasons = models.TextField(null=True, blank=True)

#     ownership_mcomm_days = models.IntegerField(null=True, blank=True)
#     ownership_mcomm_reasons = models.TextField(null=True, blank=True)

#     total_issue_days_airtel_toco = models.IntegerField(null=True, blank=True)


#     # RFAI vs MS1 Ageing
 
#     rfai_vs_ms1_ageing = models.IntegerField(null=True, blank=True)
#     rfai_vs_ms1_ageing_group = models.CharField(max_length=100, null=True, blank=True)
#     rfai_vs_ms1_ageing_tat = models.IntegerField(null=True, blank=True)

#     rfai_vs_ms1_ageing_excluding_issues_days = models.IntegerField(null=True, blank=True)
#     rfai_vs_ms1_ageing_group_excluding_issues_days = models.CharField(max_length=100, null=True, blank=True)
#     rfai_vs_ms1_ageing_tat_excluding_issues_days = models.IntegerField(null=True, blank=True)

#     wrfai_vs_ms1_ageing = models.IntegerField(null=True, blank=True)
#     wrfai_vs_ms1_ageing_group = models.CharField(max_length=100, null=True, blank=True)
#     wrfai_vs_ms1_ageing_tat = models.IntegerField(null=True, blank=True)

#     # =============================
#     # Stage & Status
#     # =============================
#     stage = models.CharField(max_length=100, null=True, blank=True)
#     tat_matrix_remarks = models.TextField(null=True, blank=True)
#     current_status = models.CharField(max_length=200, null=True, blank=True)
#     detailed_remarks = models.TextField(null=True, blank=True)
#     manual_history = models.TextField(null=True, blank=True)

#     # =============================
#     # Fibre Dependency
#     # =============================
#     dependency_fibre = models.BooleanField(default=False)
#     for_fiber_so_target_date = models.DateField(null=True, blank=True)
#     for_fiber_so_target_date_plus_1_month = models.DateField(null=True, blank=True)
#     for_fiber_so_target_date_ageing = models.DateField(null=True, blank=True)
#     for_fiber_so_target_date_groupageing = models.DateField(null=True, blank=True)

#     fibre_issue_occurred_post_workable = models.BooleanField(default=False)
#     fibre_issue_occurred_post_workable_tat = models.IntegerField(null=True, blank=True)

#     # =============================
#     # MW Dependency
#     # =============================
#     mw_issue_occurred_post_workable = models.BooleanField(default=False)
#     mw_issue_occurred_post_workable_tat = models.IntegerField(null=True, blank=True)

#     ftth_issue_occurred_post_workable = models.BooleanField(default=False)
#     ftth_issue_occurred_post_workable_tat = models.IntegerField(null=True, blank=True)


#     dependency_material = models.BooleanField(default=False)
#     dependency_material_tat = models.IntegerField(null=True, blank=True)

#     material_faulty_post_mos = models.BooleanField(default=False)
#     material_faulty_post_mos_tat = models.IntegerField(null=True, blank=True)

#     material_shortage_srn_kitty = models.BooleanField(default=False)
#     material_shortage_srn_kitty_tat = models.IntegerField(null=True, blank=True)

#     material_stuck_at_old_site = models.BooleanField(default=False)
#     material_stuck_at_old_site_tat = models.IntegerField(null=True, blank=True)


#     pri_rfai_rejected_tagged_on_ideploy = models.BooleanField(default=False)
#     rfai_rejected_date = models.DateField(null=True, blank=True)
#     re_rfai_ideploy_date = models.DateField(null=True, blank=True)
#     rfai_rejected_reason = models.TextField(null=True, blank=True)

#     dependency_toco_issue_pre_workable_ageing= models.IntegerField(null=True, blank=True)
#     dependency_toco_issue_pre_workable_tat = models.IntegerField(null=True, blank=True)
#     dependency_toco_issue_post_workable_ageing= models.IntegerField(null=True, blank=True)
#     dependency_toco_issue_post_workable_tat = models.IntegerField(null=True, blank=True)
    

#     pri_issue = models.CharField(max_length=200, null=True, blank=True)
#     pri_sub_issue = models.CharField(max_length=200, null=True, blank=True)
#     pri_count = models.IntegerField(null=True, blank=True)
#     total_pri_days = models.IntegerField(null=True, blank=True)

#     dependency_toco_issue_cleared_pre_workable= models.IntegerField(null=True, blank=True)
#     dependency_toco_issue_cleared_post_workable = models.IntegerField(null=True, blank=True)
    

#     pri_issue_ageing = models.IntegerField(null=True, blank=True)
#     other_issue_ageing = models.IntegerField(null=True, blank=True)
#     total_issue_ageing = models.IntegerField(null=True, blank=True)
#     rfai_to_ms1_ageing = models.IntegerField(null=True, blank=True)

#     ran_pat_accepted_date = models.DateField(null=True, blank=True)
#     ran_sat_accepted_date = models.DateField(null=True, blank=True)
#     mw_pat_accepted_date = models.DateField(null=True, blank=True)
#     mw_sat_accepted_date = models.DateField(null=True, blank=True)
#     scft_accepted_date = models.DateField(null=True, blank=True)

#     kpi_at_offer_date = models.DateField(null=True, blank=True)
#     kpi_at_accepted_date = models.DateField(null=True, blank=True)

#     ms2_4g_date = models.DateField(null=True, blank=True)
#     ms2_5g_date = models.DateField(null=True, blank=True)
#     final_ms2_date = models.DateField(null=True, blank=True)

#     dismantling_survey_date = models.DateField(null=True, blank=True)
#     sreq_creq_raised_date = models.DateField(null=True, blank=True)
#     dismantle_date = models.DateField(null=True, blank=True)
#     material_pickup_date = models.DateField(null=True, blank=True)
#     material_submission_date = models.DateField(null=True, blank=True)
#     oci_done_date = models.DateField(null=True, blank=True)
#     sign_off_date = models.DateField(null=True, blank=True)

#     dismantling_status = models.CharField(max_length=100, null=True, blank=True)

#     last_updated_date = models.DateTimeField(auto_now=True)
#     last_updated_by = models.CharField(max_length=150, null=True, blank=True)

    
#     class Meta:
#         unique_together = ("circle", "new_site_id")

#     def __str__(self):
#         return f"SiteTracking - {self.id}"