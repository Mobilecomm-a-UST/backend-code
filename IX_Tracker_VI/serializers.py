from rest_framework import serializers
from .models import *

class IntegrationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrationDataVI
        fields = '__all__'

from rest_framework import serializers
from .models import *

   
class  Approval_Serializer(serializers.ModelSerializer):
    class Meta:
        model= Approval   
        fields='__all__'
        
# class Relocation_RemarkSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Relocation_Remarks
#         fields = '__all__'
        
        

        