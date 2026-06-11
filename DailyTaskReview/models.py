from django.db import models


# Task model
class DailyreviewTask(models.Model):
    task = models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return self.task



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



class Dailytaskreviewmodel(models.Model):
    oem = models.CharField(max_length=255,blank=True,null=True)
    task = models.CharField(max_length=255,blank=True,null=True)
    slot = models.CharField(max_length=25,blank=True,null=True)
    owner = models.JSONField(default=list)
    status = models.CharField(max_length=55,blank=True,null=True)
    assigned_at = models.DateTimeField(blank=True,null=True)
    assigned_by = models.CharField(max_length=255,blank=True,null=True)
    frequency = models.CharField(max_length=50,blank=True,null=True)
    deadline = models.DateField(blank=True,null=True)
    remarks = models.TextField(blank=True,null=True,max_length=250)
    startdatetime = models.DateTimeField(blank=True,null=True)
    enddatetime = models.DateTimeField(blank=True,null=True)
    priority = models.CharField(max_length=50,default='Medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.oem} - {self.task}"