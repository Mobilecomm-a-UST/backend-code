from rest_framework import serializers
from .models import *

class ser_Soft_At_upload_status(serializers.ModelSerializer):
    class Meta:
        model = WPR_DPR2_Table_upload_status
        fields = '__all__'

class ser_Soft_At_Table(serializers.ModelSerializer):
    class Meta:
        model = WPR_DPR2_Table
        fields = ["WEEK","CIRCLE","Internal_RFAI_Vs_Ms1_In_Days","Internal_Ms1_Vs_Ms2_In_days","MS1","MAPA","Project"]
        