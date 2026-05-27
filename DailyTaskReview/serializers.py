from rest_framework import serializers
from .models import *


class DailyreviewTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyreviewTask
        fields = '__all__'



class DailytaskreviewmodelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dailytaskreviewmodel
        fields = '__all__'