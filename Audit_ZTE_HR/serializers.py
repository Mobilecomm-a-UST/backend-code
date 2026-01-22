from rest_framework import serializers
from Audit_ZTE_HR.models import *

class ser_ZTE_HR_Report(serializers.ModelSerializer):
    class Meta:
        model = ZTE_HR_Report
        fields = '__all__'
