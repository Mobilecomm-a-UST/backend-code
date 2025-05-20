from django.db.models.signals import pre_delete,post_delete
from .models import DPR_file, DPR_table1, performance_at_table
from django.dispatch import receiver

import os

# @receiver(pre_delete, sender=DPR_file)
# def pre_delete_profile(sender, **kwargs):
#     print("You are about to delete something!")

@receiver(pre_delete, sender=DPR_file)
def delete_profile(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.dpr_file:
        if os.path.isfile(instance.dpr_file.path):
            os.remove(instance.dpr_file.path)
            print("File deleted")
            


@receiver(pre_delete, sender=DPR_table1)
def delete_profile(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.SOFT_AT_ACCEPTANCE_MAIL:
        if os.path.isfile(instance.SOFT_AT_ACCEPTANCE_MAIL.path):
            os.remove(instance.SOFT_AT_ACCEPTANCE_MAIL.path)
            print(instance.SITE_ID,"Soft at acceptance mail deleted")
       
    if instance.PHYSICAL_AT_ACCEPTANCE_MAIL:
        if os.path.isfile(instance.PHYSICAL_AT_ACCEPTANCE_MAIL.path):
            os.remove(instance.PHYSICAL_AT_ACCEPTANCE_MAIL.path)
            print(instance.SITE_ID,"Physical at acceptance mail deleted")
            

    band_objs = performance_at_table.objects.filter(key=instance)
    for band_obj in band_objs :
        print(band_obj.band) 
        # if os.path.isfile(band_obj.PERFORMANCE_AT_ACCEPTANCE_MAIL.path):
        #     os.remove(band_obj.PERFORMANCE_AT_ACCEPTANCE_MAIL.path)
        #     print(band_obj.PERFORMANCE_AT_ACCEPTANCE_MAIL.path,"Performance at acceptance mail deleted")
    

