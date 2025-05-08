from django.db import models

# class performanceAT(models.Model):
#     id = models.CharField(max_length = 500,primary_key=True)
#     CIRCLE=models.CharField(max_length=500)
#     SITE_ID=models.CharField(max_length=500)
#     UNIQUE_ID =models.CharField(max_length=500)
#     ENODEB_ID=models.CharField(max_length=500,null=True) 
#     BAND=models.CharField(max_length= 500,null=True) 
#     Circle_Project=models.CharField(max_length=500)
#     OEM_NAME_Nokia_ZTE_Ericsson_Huawei=models.CharField(max_length=500,null=True) 
#     MS1=models.DateField(null=True)
#     Performance_AT_Status_Accepted_Rejected=models.CharField(max_length=500)##max length pcolm
#     Internal_Ms1_Vs_Ms2_n_days=models.CharField(max_length=500,null=True) 
#     Total_Allocation=models.CharField(max_length=500,null=True)
#     Project=models.CharField(max_length=500,null=True)
#     Acceptance_Status_Accepted_Offered_Pending=models.CharField(max_length=500,null=True)
#     Accepted_Offered_Date=models.DateField(null=True)
#     Pending_Reason=models.CharField(max_length=500,null=True)
#     Action_Plan=models.CharField(max_length=500,null=True)
#     Ownership=models.CharField(max_length=500,null=True)
#     Ageing=models.CharField(max_length=500,null=True)
#     upload_date=models.DateField(null=True)
  

#     def __str__(self):
#         return (self.SITE_ID)
    
# class performance_At_upload_status(models.Model):
   
#     id=models.CharField(max_length = 500,primary_key=True)
#     Site_id=models.CharField(max_length=500,null=True,blank=True)
#     update_status=models.CharField(max_length=500,null=True,blank=True)
#     Remark=models.TextField(max_length=500,null=True,blank=True)    
class performanceAT(models.Model):
    id = models.CharField(max_length = 500,primary_key=True)
    CIRCLE=models.CharField(max_length=500)
    SITE_ID=models.CharField(max_length=500)
    UNIQUE_ID =models.CharField(max_length=500)
    OEM_NAME_Nokia_ZTE_Ericsson_Huawei=models.CharField(max_length=500,null=True) 
    Project=models.CharField(max_length=500,null=True)
    MS1=models.DateField(null=True)
    Ageing=models.CharField(max_length= 500,null=True) 
    Internal_Ms1_Vs_Ms2_n_days=models.CharField(max_length=500,null=True) 
    Only_KPI_AT_pending=models.CharField(max_length=500,null=True)
    Workable_date_If_pending_due_to_other_reason=models.DateField(null=True)##max length pcolm
    Reason_of_new_workable_date=models.CharField(max_length=500,null=True)
    No_of_Pending_layers=models.CharField(max_length=500)
    Status=models.CharField(max_length=500,null=True)
    Acceptance_Date=models.DateField(null=True)
    Impacted_KPIs=models.CharField(max_length=500,null=True)
    Analysis=models.CharField(max_length=500,null=True)
    Action_plan_Remarks=models.CharField(max_length=500,null=True)
    RCA_for_high_Ageing=models.CharField(max_length=500,null=True)
    TAT=models.DateField(null=True)
    Ownership=models.CharField(max_length=500,null=True)
    Ownership_Mcom_Internal=models.CharField(max_length=500,null=True)
    Tool_Bucket=models.CharField(max_length=500,null=True)
    upload_date=models.DateField(null=True)
  

    def __str__(self):
        return (self.SITE_ID)
    
class performance_At_upload_status(models.Model):
   
    id=models.CharField(max_length = 500,primary_key=True)
    Site_id=models.CharField(max_length=500,null=True,blank=True)
    update_status=models.CharField(max_length=500,null=True,blank=True)
    Remark=models.TextField(max_length=500,null=True,blank=True)    
