from django.db import models

# model for 4G payload------------------
class PayloadTraffic4G(models.Model):
    site_id = models.CharField(max_length=200, null=True, blank=True)
    short_name = models.CharField(max_length=200, null=True, blank=True)
    traffic_value = models.FloatField(null=True, blank=True)
    traffic_date = models.DateField()

    class Meta:
        db_table = "payload_traffic_4g"
        indexes = [
            models.Index(fields=["site_id"]),
        ]
        constraints = [
        models.UniqueConstraint(
            fields=["site_id", "traffic_date", "short_name"],
            name="unique_4g_site_date_sector"
        )
    ]

    def __str__(self):
        return f"{self.site_id} - {self.short_name}"


# model for 5G payload------------------
class PayloadTraffic5G(models.Model):
    site_id = models.CharField(max_length=200, null=True, blank=True)
    short_name = models.CharField(max_length=200, null=True, blank=True)
    traffic_value = models.FloatField(null=True, blank=True)
    traffic_date = models.DateField()

    class Meta:
        db_table = "payload_traffic_5g"
        indexes = [
            models.Index(fields=["site_id"]),
        ]
        constraints = [
        models.UniqueConstraint(
            fields=["site_id", "traffic_date", "short_name"],
            name="unique_5g_site_date_sector"
        )
]
    def __str__(self):
        return f"{self.site_id} - {self.short_name}"

#upload history model--
class UploadHistory(models.Model):
    user = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    traffic_date = models.DateField(null=True, blank=True)
    table_name = models.CharField(max_length=100)
    row_inserted=models.CharField(max_length=100)
    upload_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.filename} - {self.user}"
       