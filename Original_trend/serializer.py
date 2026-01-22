from rest_framework import serializers
from .models import *

class ser_raw_kpis(serializers.ModelSerializer):
    class Meta:
        model = raw_kpis
        fields = '__all__'

class ser_integrated_site(serializers.ModelSerializer):
    class Meta:
        model = integrated_sites
        fields = '__all__'