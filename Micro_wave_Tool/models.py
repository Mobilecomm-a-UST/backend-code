from django.db import models

class MicrowaveAviat(models.Model):
    circle = models.CharField(max_length=50, null=True, blank=True)
    reference_key = models.CharField(max_length=100, db_index=True)
    site_id = models.CharField(max_length=100, null=True, blank=True)
    equipment_make = models.CharField(max_length=50, null=True, blank=True)
    plan_id = models.CharField(max_length=100, null=True, blank=True)

    polarization = models.CharField(max_length=20, null=True, blank=True)

    site_id_a = models.CharField(max_length=50, null=True, blank=True)
    tx_frequency_mhz = models.CharField(max_length=50, null=True, blank=True)
    ber10e6_rx_level_dbm = models.CharField(max_length=50, null=True, blank=True)

    site_id_b = models.CharField(max_length=50, null=True, blank=True)
    rx_frequency_mhz = models.CharField(max_length=50, null=True, blank=True)
    bandwidth_mhz = models.CharField(max_length=50, null=True, blank=True)

    acm_status = models.CharField(max_length=20, null=True, blank=True)
    acm_min_qam = models.CharField(max_length=20, null=True, blank=True)
    acm_max_qam = models.CharField(max_length=20, null=True, blank=True)

    atpc_status = models.CharField(max_length=50, null=True, blank=True)
    atpc_min = models.CharField(max_length=50, null=True, blank=True)
    atpc_max = models.CharField(max_length=50, null=True, blank=True)

    rsl_min_dbm = models.CharField(max_length=50, null=True, blank=True)
    rsl_max_dbm = models.CharField(max_length=50, null=True, blank=True)

    tx_power_max_dbm = models.CharField(max_length=50, null=True, blank=True)
    snr_min_db = models.CharField(max_length=50, null=True, blank=True)

    xpd_min_dbm = models.CharField(max_length=50, null=True, blank=True)
    xpd_max_dbm = models.CharField(max_length=50, null=True, blank=True)

    polarization_radio = models.CharField(max_length=20, null=True, blank=True)

    site_a_current_rsl = models.CharField(max_length=50, null=True, blank=True)
    site_z_current_rsl = models.CharField(max_length=50, null=True, blank=True)

    freq_tx = models.CharField(max_length=50, null=True, blank=True)
    freq_rx = models.CharField(max_length=50, null=True, blank=True)

    site_a_modulation_mode = models.CharField(max_length=50, null=True, blank=True)
    site_z_modulation_mode = models.CharField(max_length=50, null=True, blank=True)

    site_a_min_mod_last_24h = models.CharField(max_length=50, null=True, blank=True)
    site_z_min_mod_last_24h = models.CharField(max_length=50, null=True, blank=True)

    site_a_max_mod_last_24h = models.CharField(max_length=50, null=True, blank=True)
    site_z_max_mod_last_24h = models.CharField(max_length=50, null=True, blank=True)

    site_a_min_configured_mod = models.CharField(max_length=50, null=True, blank=True)
    site_z_min_configured_mod = models.CharField(max_length=50, null=True, blank=True)

    site_a_max_configured_mod = models.CharField(max_length=50, null=True, blank=True)
    site_z_max_configured_mod = models.CharField(max_length=50, null=True, blank=True)

    atpc_status_link = models.CharField(max_length=50, null=True, blank=True)
    remark=models.CharField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "microwave_aviat"
        constraints = [
            models.UniqueConstraint(
                fields=["reference_key", "circle"],
                name="uniq_reference_circle"
            )
        ]
        indexes = [
            models.Index(fields=["reference_key"]),
            models.Index(fields=["circle"]),
        ]

    
    def __str__(self):
        return self.reference_key
