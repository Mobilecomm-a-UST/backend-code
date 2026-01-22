from rest_framework import serializers
from RCA_TOOL.models import RCA_TABLE, KPI_TABLE, AlarmNotification, RCA_output_table, RCA_payload_table

class RCATableSerializer(serializers.ModelSerializer):
    class Meta:
        model = RCA_TABLE
        fields = '__all__'


class KPITableSerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI_TABLE
        fields = '__all__'


class AlarmNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlarmNotification
        fields = '__all__'
    
    


class CellDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RCA_output_table
        fields = '__all__'



import math

class FloatJSONSerializerField(serializers.FloatField):
    def to_representation(self, value):
        if math.isnan(value) or math.isinf(value):
            return None
        return super().to_representation(value)
    


class CellDataSerializer(serializers.ModelSerializer):
    cell_value = FloatJSONSerializerField()
    threshold_value = FloatJSONSerializerField()

    class Meta:
        model = RCA_output_table
        fields = '__all__'



class RCA_PayloadTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = RCA_payload_table
        fields = '__all__'