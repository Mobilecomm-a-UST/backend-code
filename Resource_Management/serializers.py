from rest_framework import serializers

class MonthlyReportSerializer(serializers.Serializer):
    circle    = serializers.CharField(max_length=100)
    category  = serializers.ChoiceField(choices=['A','B','C','D'])
    customer  = serializers.CharField(max_length=100)
    month     = serializers.CharField(max_length=10)   
    year      = serializers.CharField(max_length=4)   
    costCenter = serializers.CharField(max_length=10)
    resources       = serializers.DictField()
    other_resources = serializers.DictField()
    # other_resources = serializers.DictField(required=False, default=dict)


class MonthlyReportBulkSerializer(serializers.Serializer):
    circle = serializers.CharField(max_length=100)
    category = serializers.ChoiceField(choices=['A','B','C','D'])
    customer = serializers.CharField(max_length=100)
    month = serializers.CharField(max_length=10)
    year = serializers.CharField(max_length=4)
    costCenter = serializers.CharField(max_length=10)
    costs = serializers.DictField()

    def validate_costs(self, value):
        required = ['c1', 'c2', 'c4']

        for key in required:
            if key not in value or value[key] in ("", None):
                raise serializers.ValidationError(f"costs.{key} required")

        return value



class EmployeeBulkUploadSerializer(serializers.Serializer):
    emp_code = serializers.CharField(max_length=20)
    ust_id = serializers.CharField(max_length=30)
    emp_name = serializers.CharField(max_length=100)
    designation_name = serializers.CharField(max_length=100)
    department_name = serializers.CharField(max_length=100)
    state_name = serializers.CharField(max_length=100)
    project_code = serializers.CharField(max_length=50)
    project_name = serializers.CharField(max_length=200)
    location = serializers.CharField(max_length=100)
    manager_emp_code = serializers.CharField(max_length=20, required=False, allow_blank=True)
    reporting_manager_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    status = serializers.CharField(max_length=30)
    official_email_id = serializers.EmailField()
    contact_no = serializers.CharField(max_length=20,required=False,allow_blank=True)
    team_category = serializers.CharField(max_length=50)
