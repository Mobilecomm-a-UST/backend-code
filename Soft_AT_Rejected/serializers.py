from rest_framework import serializers
from .models import *

class ser_Soft_At_upload_status(serializers.ModelSerializer):
    class Meta:
        model = Soft_At_Rejected_status
        fields = '__all__'

class ser_Soft_At_NOK_upload_table(serializers.ModelSerializer):
    class Meta:
        model = Soft_AT_NOKIA_Rejected_Table
        fields = '__all__'

class ser_Soft_At_HUA_upload_table(serializers.ModelSerializer):
    class Meta:
        model = Soft_AT_HUAWEI_Rejected_Table
        fields = '__all__'

class ser_Soft_At_SAM_upload_table(serializers.ModelSerializer):
    class Meta:
        model = Soft_AT_SAMSUNG_Rejected_Table
        fields = '__all__'

class ser_Soft_At_ZTE_upload_table(serializers.ModelSerializer):
    class Meta:
        model = Soft_AT_ZTE_Rejected_Table
        fields = '__all__'
class ser_Soft_At_ERI_upload_table(serializers.ModelSerializer):
    class Meta:
        model = Soft_AT_ERI_Rejected_Table
        fields = '__all__'        

class ser_Soft_At_Accept_Reject_table(serializers.ModelSerializer):
    class Meta:
        model = Soft_AT_Accepted_Rejected_Table
        fields = '__all__'       




