from rest_framework import serializers
from microwave_Ceragon_tool.models import Microwavepara


class MicrowaveparaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Microwavepara
        fields = "__all__"