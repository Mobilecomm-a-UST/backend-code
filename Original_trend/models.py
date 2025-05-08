from django.db import models
from mcom_website.settings import MEDIA_ROOT

# Create your models here.

class pre_post_report(models.Model):
    Post_cell_name=models.CharField(primary_key=True, max_length=100)
    Post_cell_site_id=models.CharField(blank=True, max_length=100)
    Post_trend_cell=models.CharField(blank=True, max_length=100)

    Pre_cell_name=models.CharField(blank=True, max_length=100)
    Pre_cell_site_id=models.CharField(blank=True, max_length=100)
    Pre_trend_cell=models.CharField(blank=True, max_length=100)
############################################################ Pre volte ############################################################
    Pre_Volte_Traffic_1=models.FloatField(blank=True,null=True,default=0.0)
    Pre_Volte_Traffic_2=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_3=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_4=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_5=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_6=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_7=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_8=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_9=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_10=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_11=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_12=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_13=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_14=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_15=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_16=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_17=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_18=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_19=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_20=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_21=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_22=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_23=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_24=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_25=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_26=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_27=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_28=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_29=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_30=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Volte_Traffic_31=models.FloatField(blank=True, max_length=100,default=0.0)

################################################################ Post volte ################################################
    
    Post_Volte_Traffic_1=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_2=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_3=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_4=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_5=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_6=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_7=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_8=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_9=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_10=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_11=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_12=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_13=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_14=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_15=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_16=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_17=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_18=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_19=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_20=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_21=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_22=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_23=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_24=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_25=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_26=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_27=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_28=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_29=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_30=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Volte_Traffic_31=models.FloatField(blank=True, max_length=100,default=0.0)

####################################################################  pre Data Volume ###########################################################

    Pre_Data_Volume_1=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_2=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_3=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_4=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_5=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_6=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_7=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_8=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_9=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_10=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_11=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_12=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_13=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_14=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_15=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_16=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_17=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_18=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_19=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_20=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_21=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_22=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_23=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_24=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_25=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_26=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_27=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_28=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_29=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_30=models.FloatField(blank=True, max_length=100,default=0.0)
    Pre_Data_Volume_31=models.FloatField(blank=True, max_length=100,default=0.0)



####################################################################  Post Data Volume ###########################################################

    Post_Data_Volume_1=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_2=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_3=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_4=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_5=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_6=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_7=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_8=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_9=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_10=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_11=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_12=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_13=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_14=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_15=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_16=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_17=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_18=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_19=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_20=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_21=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_22=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_23=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_24=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_25=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_26=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_27=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_28=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_29=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_30=models.FloatField(blank=True, max_length=100,default=0.0)
    Post_Data_Volume_31=models.FloatField(blank=True, max_length=100,default=0.0)




class pre_post_report2(models.Model):
        Post_cell_name=models.CharField(primary_key=True, max_length=100)
        Pre_cell_name=models.CharField(blank=True, max_length=100)
        Post_cell_site_id=models.CharField(blank=True, max_length=100)

        Pre_cell_site_id=models.CharField(blank=True, max_length=100)

        # Post_trend_cell=models.CharField(blank=True, max_length=100)
        # Pre_trend_cell=models.CharField(blank=True, max_length=100)

        Relocation_date= models.DateField(null=True,blank=True)
        Today_date = models.DateField(null=True,blank=True)
        
        Pre_Volte_Traffic_Day1=models.FloatField(blank=True, max_length=100,default=0.0)
        Pre_Volte_Traffic_Day2=models.FloatField(blank=True, max_length=100,default=0.0)
        Pre_Volte_Traffic_Day3=models.FloatField(blank=True, max_length=100,default=0.0)
        Pre_Volte_Traffic_Day4=models.FloatField(blank=True, max_length=100,default=0.0)
        Pre_Volte_Traffic_Day5=models.FloatField(blank=True, max_length=100,default=0.0)
        Pre_Volte_Traffic_Day6=models.FloatField(blank=True, max_length=100,default=0.0)
        Pre_Volte_Traffic_Day7=models.FloatField(blank=True, max_length=100,default=0.0)

        Post_Volte_Traffic_Day1=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Volte_Traffic_Day2=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Volte_Traffic_Day3=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Volte_Traffic_Day4=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Volte_Traffic_Day5=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Volte_Traffic_Day6=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Volte_Traffic_Day7=models.FloatField(blank=True, max_length=100,default=0.0)

       
        Blank=models.CharField(blank=True, max_length=100)

        Pre_Data_Volume_Day1=models.FloatField(blank=True, max_length=100,default=0.0)
        Pre_Data_Volume_Day2=models.FloatField(blank=True, max_length=100,default=0.0)
        Pre_Data_Volume_Day3=models.FloatField(blank=True, max_length=100,default=0.0)
        Pre_Data_Volume_Day4=models.FloatField(blank=True, max_length=100,default=0.0)
        Pre_Data_Volume_Day5=models.FloatField(blank=True, max_length=100,default=0.0)
        Pre_Data_Volume_Day6=models.FloatField(blank=True, max_length=100,default=0.0)
        Pre_Data_Volume_Day7=models.FloatField(blank=True, max_length=100,default=0.0)

        Post_Data_Volume_Day1=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Data_Volume_Day2=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Data_Volume_Day3=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Data_Volume_Day4=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Data_Volume_Day5=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Data_Volume_Day6=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Data_Volume_Day7=models.FloatField(blank=True, max_length=100,default=0.0)

        Pre_Volte_Traffic_AVG=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Volte_Traffic_AVG=models.FloatField(blank=True, max_length=100,default=0.0)

        Pre_Data_Volume_AVG=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Data_Volume_AVG=models.FloatField(blank=True, max_length=100,default=0.0)
        Percentage_change_Volte_Traffic=models.FloatField(blank=True, max_length=100,default=0.0)
        Percentage_change_Data_Volume=models.FloatField(blank=True, max_length=100,default=0.0)


class pre_post_report_siteWise(models.Model):
       
        Post_cell_site_id=models.CharField(blank=True, max_length=100)

        Pre_cell_site_id=models.CharField(blank=True, max_length=100)

       

        Relocation_date= models.DateField(null=True,blank=True)
        Today_date = models.DateField(null=True,blank=True)
        
        Pre_Volte_Traffic_Day1=models.FloatField(blank=True, max_length=100,default=0.0)
        Pre_Volte_Traffic_Day2=models.FloatField(blank=True, max_length=100,default=0.0)
        Pre_Volte_Traffic_Day3=models.FloatField(blank=True, max_length=100,default=0.0)
        Pre_Volte_Traffic_Day4=models.FloatField(blank=True, max_length=100,default=0.0)
        Pre_Volte_Traffic_Day5=models.FloatField(blank=True, max_length=100,default=0.0)
        Pre_Volte_Traffic_Day6=models.FloatField(blank=True, max_length=100,default=0.0)
        Pre_Volte_Traffic_Day7=models.FloatField(blank=True, max_length=100,default=0.0)

        Post_Volte_Traffic_Day1=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Volte_Traffic_Day2=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Volte_Traffic_Day3=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Volte_Traffic_Day4=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Volte_Traffic_Day5=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Volte_Traffic_Day6=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Volte_Traffic_Day7=models.FloatField(blank=True, max_length=100,default=0.0)

        Blank=models.CharField(blank=True, max_length=100)

        Pre_Data_Volume_Day1=models.FloatField(blank=True, max_length=100,default=0.0)
        Pre_Data_Volume_Day2=models.FloatField(blank=True, max_length=100,default=0.0)
        Pre_Data_Volume_Day3=models.FloatField(blank=True, max_length=100,default=0.0)
        Pre_Data_Volume_Day4=models.FloatField(blank=True, max_length=100,default=0.0)
        Pre_Data_Volume_Day5=models.FloatField(blank=True, max_length=100,default=0.0)
        Pre_Data_Volume_Day6=models.FloatField(blank=True, max_length=100,default=0.0)
        Pre_Data_Volume_Day7=models.FloatField(blank=True, max_length=100,default=0.0)

        Post_Data_Volume_Day1=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Data_Volume_Day2=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Data_Volume_Day3=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Data_Volume_Day4=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Data_Volume_Day5=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Data_Volume_Day6=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Data_Volume_Day7=models.FloatField(blank=True, max_length=100,default=0.0)

        Pre_Volte_Traffic_AVG=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Volte_Traffic_AVG=models.FloatField(blank=True, max_length=100,default=0.0)

        Pre_Data_Volume_AVG=models.FloatField(blank=True, max_length=100,default=0.0)
        Post_Data_Volume_AVG=models.FloatField(blank=True, max_length=100,default=0.0)
        Percentage_change_Volte_Traffic=models.FloatField(blank=True, max_length=100,default=0.0)
        Percentage_change_Data_Volume=models.FloatField(blank=True, max_length=100,default=0.0)

from .storage import OverwriteStorage
import os
def get_file_path(instance, filename):
    # define the custom file name
    # filename = instance.upload_date
    # get the file extension
    ext = filename.split('.')[-1]
    # return the file path
    return os.path.join('Original_trend/Raw_Kpis/', f'Post_kpi_{instance.upload_date}.{ext}')
class raw_kpis(models.Model):
       upload_date=models.DateField(primary_key=True)
       file=models.FileField(max_length=100,upload_to=get_file_path)

       def save(self, *args, **kwargs):
        # check if there's already an existing file
        if self.pk:
            try:
                old_file = raw_kpis.objects.get(pk=self.pk).file
            except:
                old_file=None
            if old_file:
                # delete the previous file
                file_path = os.path.join(MEDIA_ROOT, str(old_file))
                os.remove(file_path)

        # call the parent class's save method to save the new file
        super().save(*args, **kwargs)
    #    upload_date= models.DateTimeField( auto_now_add=True)
       
       


class integrated_sites(models.Model):
    Site=models.CharField(primary_key=True, max_length=100)

    def __str__(self):
         return self.pk
    
