from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
import datetime 

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# 


# Create your models here.
class DPR_table1(models.Model):
    def filename_SOFT_AT_ACCEPTANCE_MAIL(instance, filename):
      
      return '/'.join(["dpr/dpr_acceptance_mail/soft_at",str(datetime.date.today().year),str(datetime.date.today().strftime("%B")),str(datetime.date.today().day),filename])
    def filename_PHYSICAL_AT_ACCEPTANCE_MAIL(instance, filename):
      
      return '/'.join(["dpr/dpr_acceptance_mail/physical_at",str(datetime.date.today().year),str(datetime.date.today().strftime("%B")),str(datetime.date.today().day),filename])
    id=models.CharField(max_length = 100,primary_key=True)
    SITE_ID=models.CharField(max_length = 100)
    CIRCLE=models.CharField(max_length = 100)
    Unique_SITE_ID=models.CharField(max_length = 100)
    BAND=models.CharField(max_length = 100)
    TOCO_NAME=models.CharField(max_length=255)
    OA_COMMERCIAL_TRAFFIC_PUT_ON_AIR_MS1_DATE=models.CharField(max_length = 100, blank=True)
    Project =models.CharField(max_length = 100)
    Activity=models.CharField(max_length = 100)
    # uploaded_date= models.DateTimeField( auto_now_add=True)
   
    Soft_AT_Status=models.CharField(max_length=100,null=True,blank=True)

    SOFT_AT_ACCEPTANCE_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    SOFT_AT_ACCEPTANCE_MAIL=models.FileField(upload_to=filename_SOFT_AT_ACCEPTANCE_MAIL,null=True,blank=True)
    
    SOFT_AT_REJECTION_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    SOFT_AT_REJECTION_REASON=models.TextField(max_length=100,null=True,blank=True)
    # SOFT_AT_REJECTED_TAT_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    
    SOFT_AT_OFFERED_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    SOFT_AT_OFFERED_REMARKS=models.TextField(max_length=100,null=True,blank=True)
    
    SOFT_AT_PENDING_REASON=models.TextField(max_length=100,null=True,blank=True)
    SOFT_AT_PENDING_REMARK=models.TextField(max_length=100,null=True,blank=True)
    SOFT_AT_PENDING_TAT_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    
    PHYSICAL_AT_Status=models.CharField(max_length=100,null=True,blank=True)
    
    PHYSICAL_AT_ACCEPTANCE_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    PHYSICAL_AT_ACCEPTANCE_MAIL=models.FileField(upload_to=filename_PHYSICAL_AT_ACCEPTANCE_MAIL,null=True,blank=True)
    
    PHYSICAL_AT_REJECTION_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    PHYSICAL_AT_REJECTION_REASON=models.TextField(max_length=100,null=True,blank=True)
    # PHYSICAL_AT_REJECTED_TAT_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    
    PHYSICAL_AT_OFFERED_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    PHYSICAL_AT_OFFERED_REMARKS=models.TextField(max_length=100,null=True,blank=True)
    
    PHYSICAL_AT_PENDING_REASON=models.TextField(max_length=100,null=True,blank=True)
    PHYSICAL_AT_PENDING_REMARK=models.TextField(max_length=100,null=True,blank=True)
    PHYSICAL_AT_PENDING_TAT_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
  
    Performance_AT_Status=models.CharField(max_length=100,null=True,blank=True)
    
    
    PERFORMANCE_AT_ACCEPTANCE_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    # PERFORMANCE_AT_ACCEPTANCE_MAIL=models.FileField(upload_to="dpr/dpr_acceptance_mail/performance_at/",null=True,blank=True)
    
    PERFORMANCE_AT_REJECTION_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    PERFORMANCE_AT_REJECTION_REASON=models.TextField(max_length=100,null=True,blank=True)
    # PERFORMANCE_AT_REJECTED_TAT_DATE=models.DateField(null=True,blank=True)
    
    PERFORMANCE_AT_OFFERED_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    PERFORMANCE_AT_OFFERED_REMARKS=models.TextField(max_length=100,null=True,blank=True)
    
    PERFORMANCE_AT_PENDING_REASON=models.TextField(max_length=100,null=True,blank=True)
    PERFORMANCE_AT_PENDING_REMARK=models.TextField(max_length=100,null=True,blank=True)
    PERFORMANCE_AT_PENDING_TAT_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])

    MAPA_STATUS=models.CharField(max_length=100,null=True,blank=True,default="NOT OK")

    ################################################################# Master Dashboard #####################################################
    RFAI_DATE=models.DateField(null=True,blank=True)
    MAPA_INCLUSION_DATE=models.DateField(null=True,blank=True)
    Internal_RFAI_Vs_Ms1_In_Days=models.CharField(max_length=100,null=True,blank=True)
    Internal_Ms1_Vs_Ms2_In_days=models.CharField(max_length=100,null=True,blank=True)




    def __str__ ( self ) :
        return str(self.SITE_ID)
   
class DPR_file(models.Model):
   
    dpr_file=models.FileField(upload_to="dpr_files/")
    uploaded_date= models.DateTimeField( auto_now_add=True)
    
    def __str__ ( self ) :
        return str(self.dpr_file)


class DPR_update_status(models.Model):
   
    id=models.CharField(max_length = 100,primary_key=True)
    SITE_ID = models.CharField(max_length = 100)
    update_status=models.CharField(max_length=100,null=True,blank=True)
    Remark=models.TextField(max_length=100,null=True,blank=True)

    
    def __str__ ( self ) :
        return str(self.SITE_ID)

class performance_at_table(models.Model):
    def filename_perfornamance_at_acceptance(instance, filename):

      return '/'.join(["dpr/dpr_acceptance_mail/performance_at", str(instance.band), str(datetime.date.today().year),str(datetime.date.today().strftime("%B")),str(datetime.date.today().day),filename])
    key= models.ForeignKey(DPR_table1, max_length = 100, on_delete=models.CASCADE)
    band=models.CharField(max_length=100,blank=True)
    Performance_AT_Status=models.CharField(max_length=100,blank=True)
    PERFORMANCE_AT_ACCEPTANCE_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    PERFORMANCE_AT_ACCEPTANCE_MAIL=models.FileField(upload_to=filename_perfornamance_at_acceptance,null=True,blank=True)
    PERFORMANCE_AT_REJECTION_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    PERFORMANCE_AT_REJECTION_REASON=models.TextField(max_length=100,null=True,blank=True)
    PERFORMANCE_AT_OFFERED_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    PERFORMANCE_AT_OFFERED_REMARKS=models.TextField(max_length=100,null=True,blank=True)
    PERFORMANCE_AT_PENDING_REASON=models.TextField(max_length=100,null=True,blank=True)
    PERFORMANCE_AT_PENDING_REMARK=models.TextField(max_length=100,null=True,blank=True)
    
    def __str__ ( self ) :
        return  str(self.band)



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)