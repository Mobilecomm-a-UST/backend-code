from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class EmployeeSkillTable(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    emp_code = models.CharField(primary_key=True, max_length=20)
    employee_name = models.CharField(max_length=500)
    designation = models.CharField(max_length=500)
    doj = models.DateField(blank=True,null=True)
    circle = models.CharField(max_length=500)
    project_name = models.CharField(max_length=500)
    manager_emp_code = models.CharField(max_length=100)
    reporting_manager_name = models.CharField(max_length=500)
    mobile_no = models.CharField(max_length=15)
    email_id = models.EmailField()
    domain = models.CharField(max_length=500)
    project = models.CharField(max_length=500)
    current_role = models.CharField(max_length=500)
    key_responsibility = models.TextField()
    skillsets = models.TextField()
    oem = models.CharField(max_length=500)
    total_exp = models.FloatField()
    mobilecomm_exp = models.FloatField()
    previous_org1 = models.CharField(max_length=500,blank=True)
    previous_org2 = models.CharField(max_length=500,blank=True)
    previous_org3 = models.CharField(max_length=500,blank=True)
    current_designation = models.CharField(max_length=500)
    working_status = models.CharField(max_length=500)
    team_category = models.CharField(max_length=500)
    current_circle = models.CharField(max_length=500,default="-")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted_by=models.CharField(max_length=500,default="-")
    delete_remark=models.CharField(max_length=1000,default="-")
    uploaded_by = models.CharField(max_length=500,default="-")
    def __str__(self):
        return self.emp_code