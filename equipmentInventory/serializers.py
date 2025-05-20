from rest_framework import serializers
from .models import *

class ser_equipment_upload_status(serializers.ModelSerializer):
    class Meta:
        model = Equipment_upload_status
        fields = '__all__'

class ser_equipment_table(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'  
