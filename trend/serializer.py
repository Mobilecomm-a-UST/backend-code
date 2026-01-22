from rest_framework import serializers
from .models import *

class serializer_DPR_table1(serializers.ModelSerializer):
    class Meta:
        model=DPR_table1
        fields=["id","SITE_ID",
        "Unique_SITE_ID",
    "CIRCLE",
    "BAND",
    "TOCO_NAME",
    "OA_COMMERCIAL_TRAFFIC_PUT_ON_AIR_MS1_DATE",
    "Project",
    "Activity",]
        # exclude=["title"]



class serializer_DPR_table1_all(serializers.ModelSerializer):
    class Meta:
        model=DPR_table1
        fields="__all__"
        # exclude=["title"]


######################################### soft at ######################################################################33

class  ser_soft_at_acceptance( serializers.ModelSerializer ):
    class Meta :
        model = DPR_table1
        fields = ["SOFT_AT_ACCEPTANCE_DATE","SOFT_AT_ACCEPTANCE_MAIL"]
        
        

class  ser_soft_at_rejection( serializers.ModelSerializer ):
    class Meta :
        model = DPR_table1
        fields = ("SOFT_AT_REJECTION_DATE","SOFT_AT_REJECTION_REASON")
     
class  ser_soft_at_offered( serializers.ModelSerializer ):
    class Meta :
        model = DPR_table1
        fields = ("SOFT_AT_OFFERED_DATE","SOFT_AT_OFFERED_REMARKS")

class  ser_soft_at_pending(serializers.ModelSerializer):
    class Meta :
        model = DPR_table1
        fields = ("SOFT_AT_PENDING_REASON","SOFT_AT_PENDING_REMARK","SOFT_AT_PENDING_TAT_DATE")
       
######################################### physical at ######################################################################33
class  ser_physical_at_acceptance( serializers.ModelSerializer ):
    class Meta :
        model = DPR_table1
        fields = ("PHYSICAL_AT_ACCEPTANCE_DATE","PHYSICAL_AT_ACCEPTANCE_MAIL")
  


class  ser_physical_at_rejection( serializers.ModelSerializer ):
    class Meta :
        model = DPR_table1
        fields = ("PHYSICAL_AT_REJECTION_DATE","PHYSICAL_AT_REJECTION_REASON")
    

class  ser_physical_at_offered( serializers.ModelSerializer ):
    class Meta :
        model = DPR_table1
        fields = ("PHYSICAL_AT_OFFERED_DATE","PHYSICAL_AT_OFFERED_REMARKS")
   
class  ser_physical_at_pending( serializers.ModelSerializer ):
    class Meta :
        model = DPR_table1
        fields = ("PHYSICAL_AT_PENDING_REASON","PHYSICAL_AT_PENDING_REMARK","PHYSICAL_AT_PENDING_TAT_DATE")


#################################################### performance at ########################################################3
class  ser_performance_at_acceptance( serializers.ModelSerializer ):
    class Meta :
        model = performance_at_table
        fields = ("PERFORMANCE_AT_ACCEPTANCE_DATE","PERFORMANCE_AT_ACCEPTANCE_MAIL")
      
class  ser_performance_at_rejection( serializers.ModelSerializer):
    class Meta :
        model = performance_at_table
        fields = ("PERFORMANCE_AT_REJECTION_DATE","PERFORMANCE_AT_REJECTION_REASON")
   
class  ser_performance_at_offered( serializers.ModelSerializer ):
    class Meta :
        model = performance_at_table
        fields = ("PERFORMANCE_AT_OFFERED_DATE","PERFORMANCE_AT_OFFERED_REMARKS")
   
class  ser_performance_at_pending( serializers.ModelSerializer ):
    class Meta :
        model = performance_at_table
        fields = ("PERFORMANCE_AT_PENDING_REASON",)
  


class  ser_DPR_update_status( serializers.ModelSerializer ):
    class Meta :
        model = DPR_update_status
        fields = "__all__"

class  ser_performance_at_table( serializers.ModelSerializer ):
    class Meta :
        model = performance_at_table
        fields = ["band","Performance_AT_Status"]