from django.db import models

class UBR_MDP_Table(models.Model):
    id=models.CharField(primary_key=True,max_length=500)
    Year=models.PositiveIntegerField()
    Month=models.CharField(max_length=500)
    Circle=models.CharField(max_length=500)
    Project=models.CharField(max_length=500)
    Partner=models.CharField(max_length=500)
    Done_Count=models.IntegerField(null=True,blank=True)
    Projected_Count=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return (self.id)