from django.db import models

class Employee(models.Model):

    SKILL_CHOICES = [
        ('Survey', 'Survey'),
        ('MW INC', 'MW INC'),
        ('RAN INC', 'RAN INC'),
        ('Integration', 'Integration'),
        ('Drive Test', 'Drive Test'),
    ]

    sr_no               = models.IntegerField()
    circle              = models.CharField(max_length=100)
    emp_code            = models.CharField(max_length=50, primary_key=True)
    ust_id              = models.CharField(max_length=50, unique=True)
    emp_name            = models.CharField(max_length=150)
    contact_no          = models.CharField(max_length=15)
    designation_name    = models.CharField(max_length=100)
    department_name     = models.CharField(max_length=100)
    reporting_manager   = models.CharField(max_length=150)
    skill_set = models.CharField(max_length=50, choices=SKILL_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.emp_code} - {self.emp_name}"


class DriveTestSurvey(models.Model):

    STATUS_CHOICES = [
        ('Idle', 'Idle'),
        ('Working', 'Working'),
        ('Leave', 'Leave'),
        ('Week off', 'Week off'),
    ]

    PROJECT_CHOICES = [
        ('Relocation', 'Relocation'),
        ('MW', 'MW'),
        ('Degrow', 'Degrow'),
        ('New Tower', 'New Tower'),
        ('Upgrade', 'Upgrade'),
        ('IBS', 'IBS'),
        ('Survey', 'Survey'),
    ]

    employee            = models.ForeignKey(
                            Employee,
                            on_delete=models.CASCADE,
                            to_field='emp_code',
                            related_name='surveys'
                          )
    date                = models.DateField(null=True, blank=True)
    working_status = models.CharField(max_length=50, blank=True, null=True)
    project = models.CharField(max_length=50, blank=True, null=True)
    activity_assigned   = models.TextField(blank=True, null=True)
    
    site_id             = models.CharField(max_length=100, blank=True, null=True)
    ssid                = models.CharField(max_length=100, blank=True, null=True)
    activity_status     = models.CharField(max_length=100, blank=True, null=True)
    detailed_remarks    = models.TextField(blank=True, null=True)
    owner               = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        unique_together = ('employee', 'date')
        verbose_name="Field Resource Tracking"
        verbose_name_plural="Field Resource Tracking"

    def __str__(self):
        return f"{self.employee.emp_name} | {self.date} | {self.working_status}"