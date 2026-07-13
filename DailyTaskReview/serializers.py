from rest_framework import serializers
from .models import *


class AddTaskTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddTaskTable
        fields = '__all__'

class ReportingEmailHierarchySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportingEmailHierarchy
        fields = '__all__'

        



class DailytaskreviewmodelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dailytaskreviewmodel
        fields = '__all__'


class TaskTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTemplate
        fields = '__all__'