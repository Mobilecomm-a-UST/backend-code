from rest_framework import serializers
from .models import MonthlyReport

class MonthlyReportSerializer(serializers.Serializer):
    circle    = serializers.CharField(max_length=100)
    category  = serializers.ChoiceField(choices=['A','B','C','D'])
    customer  = serializers.CharField(max_length=100)
    month     = serializers.CharField(max_length=10)   
    year      = serializers.CharField(max_length=4)   
    costCenter = serializers.CharField(max_length=10)

    costs           = serializers.DictField()
    resources       = serializers.DictField()
    other_resources = serializers.DictField(required=False, default=dict)

    def validate_costs(self, value):
        required = ['c1', 'c2', 'c4']
        for key in required:
            if key not in value or value[key] == "" or value[key] is None:
                raise serializers.ValidationError(f"costs.{key} required")
        return value