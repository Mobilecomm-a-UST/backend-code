from django.db import models
from django.utils import timezone

class MonthlyReport(models.Model):
    circle    = models.CharField(max_length=100)
    category  = models.CharField(max_length=1)
    customer  = models.CharField(max_length=100)
    month     = models.CharField(max_length=10)
    year      = models.CharField(max_length=4)
    costCenter = models.CharField(max_length=10)
    
    costs           = models.JSONField(default=dict)
    resources       = models.JSONField(default=dict)
    other_resources = models.JSONField(default=dict)
    month_wise_data = models.JSONField(default=dict)  
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'resource_mgt_reports'
        constraints = [
            models.UniqueConstraint(
                fields=['month','costCenter'],
                name='unique_month_costCenter'
            )
        ]

    def __str__(self):
        return f"{self.month} | {self.costCenter}"
