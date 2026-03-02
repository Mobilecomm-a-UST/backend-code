# Soft_AT_Nokia/serializers.py
from rest_framework import serializers
from .models import ExpectedParameter ,SummaryData , ExpectedParameter_5G, SummaryData_5G

class ExpectedParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpectedParameter
        fields = '__all__'

class SummaryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummaryData
        fields = '__all__'

from .models import UserCounter


class UserCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCounter
        fields = '__all__'


#-----------------------5G Serializers-----------------------
class ExpectedParameterSerializer_5G(serializers.ModelSerializer):
    class Meta:
        model = ExpectedParameter_5G
        fields = '__all__'

class SummaryDataSerializer_5G(serializers.ModelSerializer):
    class Meta:
        model = SummaryData_5G
        fields = '__all__'
