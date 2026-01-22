from rest_framework import serializers
from UBR_Soft_Phy_AT_Rejection_App.models import *



class ser_UBR_Soft_Phy_AT_Rejection_Table(serializers.ModelSerializer):
    class Meta:
        model = UBR_Soft_Phy_AT_Rejection_Table
        fields = '__all__'
