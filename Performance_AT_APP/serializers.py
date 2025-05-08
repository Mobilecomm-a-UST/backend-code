from rest_framework import serializers
from .models import *

class ser_performance_At_upload_status(serializers.ModelSerializer):
    class Meta:
        model = performance_At_upload_status
        fields = '__all__'