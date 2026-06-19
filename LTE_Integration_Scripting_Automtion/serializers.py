from rest_framework import serializers
from .models import *

class LTELogTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = LTELogTable
        fields = '__all__'