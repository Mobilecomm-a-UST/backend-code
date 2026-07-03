from django.db import models

class SamsungAlarm(models.Model):
    oem= models.CharField(max_length=255, default='Samsung')
    alarm_name = models.CharField(max_length=255, blank=True, null=True)
    alarm_type = models.CharField(max_length=255, blank=True, null=True)
    sa_nsa = models.CharField(max_length=255, blank=True, null=True)
    noc_circle = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.sa_nsa


class Old_New(models.Model):
    new_site = models.CharField(max_length=100)
    old_site = models.CharField(max_length=100)

    new_4g_mrbts = models.CharField(max_length=100, null=True, blank=True)
    old_4g_mrbts = models.CharField(max_length=100, null=True, blank=True)

    new_5g_nrbts = models.CharField(max_length=100, null=True, blank=True)
    old_5g_nrbts = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.new_site} -> {self.old_site}"
