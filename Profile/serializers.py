from rest_framework import serializers
from Profile.models import *


class ProfileModelSer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = "__all__"
