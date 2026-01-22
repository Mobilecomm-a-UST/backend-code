from rest_framework import serializers
from .models import * 

class ser_upload_report_table(serializers.ModelSerializer):
    class Meta:
        model = upload_report_table
        fields = '__all__'

class ProjectedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectedData
        fields = '__all__'

class ActualDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActualData
        fields = '__all__'