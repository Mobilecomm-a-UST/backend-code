from rest_framework import serializers
from .models import *

class IntegrationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrationData
        fields = '__all__'

from rest_framework import serializers
from .models import Relocation_tracker



class New_site_locked_unlocked_date_serializer(serializers.ModelSerializer):
    class Meta:
        model=New_site_locked_unlocked_date
        fields = '__all__'
    
    # def create(self, validated_data):
    #     """Handles creation of a new record"""
    #     return New_site_locked_unlocked_date.objects.create(**validated_data)

class old_site_locked_unlocked_date_serializer(serializers.ModelSerializer):
    class Meta:
        model=old_site_locked_unlocked_date
        fields = '__all__'

class Relocation_trackerSerializer(serializers.ModelSerializer):
    new_site_locked_unlocked_date=New_site_locked_unlocked_date_serializer(many=True,read_only=True)
    old_site_locked_unlocked_date=old_site_locked_unlocked_date_serializer(many=True,read_only=True)
    class Meta:
        model = Relocation_tracker
        fields = '__all__'
    
class  Approval_Serializer(serializers.ModelSerializer):
    class Meta:
        model= Approval   
        fields='__all__'
        
# class Relocation_RemarkSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Relocation_Remarks
#         fields = '__all__'
        
        

        