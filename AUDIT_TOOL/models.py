from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    task_id = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    app_name = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    circle = models.CharField(max_length=50, null=True, blank = True)
    file_link=models.CharField(max_length=1000,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Task {self.task_id} - User {self.user.username}"