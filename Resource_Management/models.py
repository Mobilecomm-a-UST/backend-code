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
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'resource_mgt_reports'
        constraints = [models.UniqueConstraint(fields=['month','costCenter'],name='unique_month_costCenter')]

    def __str__(self):
        return f"{self.month} | {self.costCenter}"


class Employee(models.Model):

    emp_code = models.CharField(max_length=20)
    ust_id = models.CharField(max_length=30, unique=True)
    emp_name = models.CharField(max_length=100)
    designation_name = models.CharField(max_length=100)
    department_name = models.CharField(max_length=100)
    state_name = models.CharField(max_length=100)
    project_code = models.CharField(max_length=50)
    project_name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    manager_emp_code = models.CharField(max_length=20)
    reporting_manager_name = models.CharField(max_length=100)
    status = models.CharField(max_length=30)
    official_email_id = models.EmailField()
    contact_no = models.CharField(max_length=20)
    team_category = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "employee_master"

    def __str__(self):
        return f"{self.emp_name} ({self.ust_id})"
