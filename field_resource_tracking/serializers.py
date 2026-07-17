from rest_framework import serializers
from .models import Employee, DriveTestSurvey


class DriveTestSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = DriveTestSurvey
        fields = '__all__'


class DailyUpdateSerializer(serializers.ModelSerializer):
    emp_name = serializers.CharField(
        source='employee.emp_name', read_only=True)
    emp_code = serializers.CharField(
        source='employee.emp_code', read_only=True)

    class Meta:
        model = DriveTestSurvey
        fields = [
            'emp_code',
            'emp_name',
            'date',
            'working_status',
            'project',
            'activity_assigned',
            'site_id',
            'ssid',
            'activity_status',
            'detailed_remarks',
            'owner'
        ]


class EmployeeDatewiseSerializer(serializers.ModelSerializer):
    surveys = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            'emp_code',
            'emp_name',
            'circle',
            'designation_name',
            'department_name',
            'skill_set',
            'surveys'
        ]

    def get_surveys(self, obj):
        surveys = DriveTestSurvey.objects.filter(
            employee=obj
        ).order_by('date')
        return DriveTestSurveySerializer(surveys, many=True).data


class EmployeeSerializer(serializers.ModelSerializer):
    surveys = DriveTestSurveySerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'