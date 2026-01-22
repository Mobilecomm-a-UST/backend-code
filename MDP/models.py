from django.db import models

class upload_report_table(models.Model):
    id=models.CharField(primary_key=True,max_length=500)
    YEAR=models.PositiveIntegerField()
    MONTH=models.CharField(max_length=500)
    circle=models.CharField(max_length=500)
    project=models.CharField(max_length=500)
    COMPATITOR=models.CharField(max_length=500)
    DONE_COUNT=models.IntegerField(null=True,blank=True)
    PROJECTED_COUNT=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return (self.id)
   
class ProjectedData(models.Model):
    circle = models.CharField(max_length=100)
    month = models.CharField(max_length=100)
    aop=models.CharField(max_length=50)
    project = models.CharField(max_length=100)
    airtel_projection = models.IntegerField()
    mobilecomm_projection = models.IntegerField()
    uploaded_by = models.CharField(max_length=500, blank=True) 
    upload_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'Projected_data'
        unique_together = ['aop','circle', 'month', 'project']

    def __str__(self):
        return f"{self.circle} - {self.month} - {self.project}"



class ActualData(models.Model):
    circle = models.CharField(max_length=100)
    month = models.CharField(max_length=100)
    aop=models.CharField(max_length=50)
    project = models.CharField(max_length=100)
    airtel_actual = models.IntegerField()
    mobilecomm_actual = models.IntegerField()
    Ericsson_Actual = models.IntegerField()
    Nokia_Actual = models.IntegerField()
    vedang_actual = models.IntegerField()
    frog_cell_actual = models.IntegerField()
    ariel_actual = models.IntegerField()
    others_actual = models.IntegerField()

    uploaded_by = models.CharField(max_length=500, blank=True) 
    upload_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Actual_data'
        unique_together = ['aop','circle', 'month', 'project']

    def __str__(self):
        return f"{self.circle} - {self.month} - {self.project}"