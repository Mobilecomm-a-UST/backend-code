from django.db import models
import datetime
# Create your models here.
class Progress_report(models.Model):
    ############################ Basic input #########################
    MDP_Month=models.CharField(max_length=100)
    Unique_Site_Id_As_per_central_DPR = models.CharField(primary_key=True,max_length=100)
    Circle = models.CharField(max_length=100)
    Site_ID = models.CharField(max_length=100)
    Site_Name = models.CharField(max_length=100)
    Activity_Name = models.CharField(max_length=100)
    Activity_Discription = models.CharField(max_length=100)
    Line_Item = models.CharField(max_length=100)
    Alotment_date_To_Vendor = models.DateField(null=True)
    Vendor_Name = models.CharField(max_length=100)
    Vendor_Code = models.CharField(max_length=100)
    
    ################################ Progress ##########################
    Activity_Date = models.DateField(null=True)
    Activity_Completion_Status = models.CharField(max_length=100)
    Material_Reco_Status = models.CharField(max_length=100)
    Material_Reco_Date=models.DateField(null=True)
    Activity_AT_Status=models.CharField(max_length=100)
    Activity_AT_Date=models.DateField(null=True)


    ############################## op1 #################################

    Vendor_PO_Eligible = models.CharField(max_length=100,null=True)
    Vendor_PO_Approver = models.CharField(max_length=100,null=True)
    Vendor_PO_Requestor = models.CharField(max_length=100,null=True)
    Vendor_PO_Date = models.DateField(null=True)
    Vendor_PO_No = models.CharField(max_length=100,null=True)
 
   ################################ op2 ################################
    Vendor_Invoice_Eligiblity = models.CharField(max_length=100,null=True)
    Vendor_Invoice_Approval_Name_from_Circle = models.CharField(max_length=100,null=True)
    Vendor_Invoice_Approval_Name_from_Central =  models.CharField(max_length=100,null=True)
    Vendor_PO_Date = models.DateField(null=True)
    Invoice_No =  models.CharField(max_length=100,null=True)



class upload_status(models.Model):
   
    id=models.CharField(max_length = 100,primary_key=True)

    update_status=models.CharField(max_length=100,null=True,blank=True)
    Remark=models.TextField(max_length=100,null=True,blank=True)

    
    def __str__ ( self ) :
        return str(self.SITE_ID)

class vendor_po_approver_upload_status(models.Model):
   
    id=models.CharField(max_length = 100,primary_key=True)

    update_status=models.CharField(max_length=100,null=True,blank=True)
    Remark=models.TextField(max_length=100,null=True,blank=True)

    
    def __str__ ( self ) :
        return str(self.SITE_ID)
    
class vendor_po_No_upload_status(models.Model):
   
    id=models.CharField(max_length = 100,primary_key=True)

    update_status=models.CharField(max_length=100,null=True,blank=True)
    Remark=models.TextField(max_length=100,null=True,blank=True)

    
    def __str__ ( self ) :
        return str(self.SITE_ID)
    


class circle_list(models.Model):
    name=models.CharField(max_length=100)