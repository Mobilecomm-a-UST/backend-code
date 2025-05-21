# Soft_AT_Nokia/serializers.py
from rest_framework import serializers
from .models import ExpectedParameter ,SummaryData

class ExpectedParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpectedParameter
        fields = '__all__'

class SummaryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummaryData
        fields = '__all__'
