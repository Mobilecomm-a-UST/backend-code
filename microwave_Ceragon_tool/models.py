from django.db import models

class Microwavepara(models.Model):
    idu_model= models.CharField(max_length=50,null=True,blank=True)
    parameter = models.CharField(max_length=200)
    value = models.TextField()

    def __str__(self):
        return f"{self.idu_model} - {self.parameter}"
    

class CircleServerIP(models.Model):
    circle = models.CharField(max_length=20)
    ip = models.GenericIPAddressField()
    is_active = models.BooleanField(default=True)


from django.db import models


class CeragonATP(models.Model):
    sl_no = models.IntegerField()

    mw_plan_id = models.CharField(max_length=100)
    link_id = models.CharField(max_length=255)
    site_id = models.CharField(max_length=100)
    site_name = models.CharField(max_length=100)
    server_rdp_ip = models.CharField(max_length=100, blank=True)
    type_of_equipment = models.CharField(max_length=100)
    odu_idu = models.CharField(max_length=50)
    mrmc_script_id = models.CharField(max_length=100, blank=True)
    mrmc_profile = models.CharField(max_length=100, blank=True)
    link_configuration = models.CharField(max_length=100)
    idu_model = models.TextField()
    link_slot_number = models.CharField(max_length=20)
    link_port_number = models.CharField(max_length=20)
    frequency_tx = models.CharField(max_length=50)
    frequency_rx = models.CharField(max_length=50)
    tx_power = models.CharField(max_length=50)
    rsl = models.CharField(max_length=50)
    modulation = models.CharField(max_length=100)
    atpc = models.CharField(max_length=50)
    acm_mode = models.CharField(max_length=100)
    odu_ip_address = models.CharField(max_length=100)
    idu_ip_address_remarks = models.TextField(blank=True)
    odu_ip_ethernet_slot_port_detail = models.TextField(blank=True)
    gnoc_link_id = models.CharField(max_length=255, blank=True)
    gnoc_site_name = models.CharField(max_length=100, blank=True)
    gnoc_equipment = models.TextField(blank=True)
    hop_visible = models.CharField(max_length=20, blank=True)
    software_version = models.CharField(max_length=100, blank=True)
    gnoc_frequency_tx = models.CharField(max_length=50, blank=True)
    gnoc_frequency_rx = models.CharField(max_length=50, blank=True)
    gnoc_tx_power = models.CharField(max_length=50, blank=True)
    gnoc_rsl = models.CharField(max_length=50, blank=True)
    gnoc_mrmc_script = models.CharField(max_length=100, blank=True)
    gnoc_mrmc_profile = models.CharField(max_length=100, blank=True)
    gnoc_modulation = models.CharField(max_length=100, blank=True)
    gnoc_acm = models.CharField(max_length=100, blank=True)
    gnoc_atpc = models.CharField(max_length=50, blank=True)
    gnoc_high_low_violation = models.CharField(max_length=50, blank=True)
    gnoc_qos = models.CharField(max_length=50, blank=True)
    gnoc_performance = models.CharField(max_length=100, blank=True)
    gnoc_datetime = models.CharField(max_length=100, blank=True)
    gnoc_mstp = models.CharField(max_length=100, blank=True)
    gnoc_undervoltage_clear = models.CharField(max_length=50, blank=True)
    gnoc_undervoltage_raise = models.CharField(max_length=50, blank=True)
    gnoc_critical_alarm = models.CharField(max_length=100, blank=True)
    gnoc_ethernet_port_speed = models.CharField(max_length=100, blank=True)
    gnoc_final_remarks = models.TextField(blank=True)
    gnoc_final_status = models.CharField(max_length=100, blank=True)
    done_by = models.CharField(max_length=100, blank=True)
    date = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = "ceragon_atp"

    def __str__(self):
        return f"{self.mw_plan_id} - {self.site_id}"    