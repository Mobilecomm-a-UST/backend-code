from django.db import models
from django.utils import timezone
import random


# Task model
class AddTaskTable(models.Model):
    task = models.CharField(max_length=255,blank=True,null=True)
    userID = models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return self.task

class ReportingEmailHierarchy(models.Model):
    userID = models.CharField(max_length=255,blank=True,null=True)
    assigned_to = models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return self.assigned_to



# Main Daily Task Review Model
# class Dailytaskreviewmodel(models.Model):
#     oem = models.CharField(max_length=255,blank=True,null=True)
#     task = models.CharField(max_length=255,blank=True,null=True)
#     slot = models.CharField(max_length=25,blank=True,null=True)
#     time = models.TimeField()
#     owner = models.JSONField(default=list)
#     status = models.CharField(max_length=55,blank=True,null=True)
#     starttime = models.TimeField()
#     startdate = models.DateField()
#     enddate = models.DateField()
#     endtime = models.TimeField()
#     priority=models.TextField()

class TaskTemplate(models.Model):

    # ---------------- Basic Information ----------------
    template_name = models.CharField(max_length=255,unique=True)
    oem = models.CharField(max_length=100)
    task = models.CharField(max_length=500)
    owners = models.JSONField(default=list)
    status = models.CharField(max_length=55,blank=True,null=True)
    assigned_by = models.CharField(max_length=255)
    priority = models.CharField(max_length=20,default="Medium")
    remarks = models.TextField(blank=True)

    # ---------------- Scheduling ----------------

    recurrence_rule = models.JSONField()
    deadline_rule = models.JSONField()
    start_date = models.DateField()
    end_date = models.DateField(null=True,blank=True)
    is_active = models.BooleanField(default=True)

    # ---------------- Audit ----------------

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task


class TaskGenerationLog(models.Model):

    template = models.ForeignKey(TaskTemplate,on_delete=models.CASCADE)
    owner = models.CharField(max_length=255)
    task_id = models.CharField(max_length=50)
    scheduled_datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "template",
            "owner",
            "scheduled_datetime",
        )


class Dailytaskreviewmodel(models.Model):
    oem = models.CharField(max_length=255,blank=True,null=True)
    task = models.CharField(max_length=255,blank=True,null=True)
    slot = models.CharField(max_length=25,blank=True,null=True)
    owner = models.JSONField(default=list)
    status = models.CharField(max_length=55,blank=True,null=True)
    assigned_at = models.DateTimeField(blank=True,null=True)
    assigned_by = models.CharField(max_length=255,blank=True,null=True)
    frequency = models.CharField(max_length=50,blank=True,null=True)
    deadline = models.DateTimeField(blank=True,null=True)
    remarks = models.TextField(blank=True,null=True,max_length=250)
    priority = models.CharField(max_length=50,default='Medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=255,blank=True,null=True)
    task_id = models.CharField(max_length=255,blank=True,null=True, unique=True)
    task_type = models.CharField(max_length=50,blank=True,null=True)
    reassign_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):

        # First save object to generate id
        if not self.pk:
            super().save(*args, **kwargs)

            date_str = timezone.now().strftime("%d%m%Y")

            self.task_id = f"DTR{date_str}/{self.id:06d}"

            super().save(update_fields=['task_id'])

        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.oem} - {self.task}"