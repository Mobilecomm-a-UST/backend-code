from rest_framework import serializers
from MO_BASED_REPORT.models import *


class ser_Mo_Based_upload_status(serializers.ModelSerializer):
    class Meta:
        model = Mo_Based_upload_status
        fields = "__all__"


class ser_Consolidate_MO_based_Table(serializers.ModelSerializer):
    class Meta:
        model = Consolidate_MO_based_Table
        fields = "__all__"
        
class ser_Monthly_Signoff_CATS_VS_Mobinet(serializers.ModelSerializer):
    class Meta:
        model = Monthly_Signoff_CATS_VS_Mobinet
        fields = "__all__"
