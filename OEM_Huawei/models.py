from django.db import models

class HuaweiAlarm(models.Model):
    oem= models.CharField(max_length=255, default='Huawei')
    alarm_name = models.CharField(max_length=255, blank=True, null=True)
    alarm_type = models.CharField(max_length=255, blank=True, null=True)
    sa_nsa = models.CharField(max_length=255, blank=True, null=True)
    noc_circle = models.CharField(max_length=255, blank=True, null=True)
    remark = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.sa_nsa


class Old_New(models.Model):
    new_site = models.CharField(max_length=100)
    old_site = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.new_site} -> {self.old_site}"
