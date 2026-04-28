from django.db import models

class UniversalAlarm(models.Model):
    site_id = models.CharField(max_length=100)
    mplane_ip = models.CharField(max_length=255 )
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Site ID: {self.site_id}, M-Plane IP: {self.mplane_ip}, Status: {self.status}"
    

class OldvsNew(models.Model):
    new_site = models.CharField(max_length=100)
    old_site = models.CharField(max_length=50)

    def __str__(self):
        return f"New Site: {self.new_site}, Old Site: {self.old_site}"