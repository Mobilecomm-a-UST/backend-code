from django.db import models

class ZteAlarm(models.Model):
    alarm_name = models.TextField(db_column="MO", null=True, blank=True)
    alarm_status = models.CharField(max_length=100, db_column="Alarm/No Alarm", null=True, blank=True)
    sa_nsa = models.CharField(max_length=50, db_column="SA/NSA", null=True, blank=True)
    alarm_bucket = models.CharField(max_length=200, null=True, blank=True)
    responsibility = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.alarm_name)


class Old_New(models.Model):
    new_site = models.CharField(max_length=100)
    old_site = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.new_site} -> {self.old_site}"
