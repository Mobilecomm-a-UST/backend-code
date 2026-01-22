from django.db import models

class NokiaAlarm(models.Model):
    SA = models.CharField(max_length=255, blank=True, null=True)
    NSA = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.SA or self.NSA
