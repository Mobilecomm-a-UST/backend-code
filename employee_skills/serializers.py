from rest_framework import serializers
from .models import EmployeeSkillTable

class EmployeeSkillTableSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(EmployeeSkillTableSerializer, self).__init__(*args, **kwargs)

    active = serializers.BooleanField(read_only=True)
    class Meta:
        model = EmployeeSkillTable
        # fields = ['id','Employee_name', 'Circle', 'Department', 'Key_Responsibilities_area', 'skillsets']
        # fields = ['emp_id', 'Employee_name', 'Circle', 'Department', 'Key_Responsibilities_area', 'skillsets', 'oem', 'Mobile_no', 'email_id', 'year_of_experiance',"designation",'reporting_manager',"working_status","team_category","mcom_date_of_joining"]
        fields = '__all__'
        
    def create(self, validated_data):
        request = self.context.get('request')
        print('here in create')

        validated_data['uploaded_by'] = self.request.user.username
            
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        print('here in update')

        validated_data['uploaded_by'] = self.request.user.username
    
        return super().update(instance, validated_data)
        
       
class EmployeeSkillTableSerializer_create(serializers.ModelSerializer):
    active = serializers.BooleanField(read_only=True)
    class Meta:
        model = EmployeeSkillTable
        # fields = ['id','Employee_name', 'Circle', 'Department', 'Key_Responsibilities_area', 'skillsets']
        # fields = ['emp_id', 'Employee_name', 'Circle', 'Department', 'Key_Responsibilities_area', 'skillsets', 'oem', 'Mobile_no', 'email_id', 'year_of_experiance',"designation",'reporting_manager',"working_status","team_category","mcom_date_of_joining"]
        fields = '__all__'

        def validate(self, attrs):
            # if attrs.get('active', False):  # Only check if we're trying to create/activate a record
                if EmployeeSkillTable.objects.filter(emp_code=attrs['emp_code'], active=False).exists():
                    # raise serializers.ValidationError("An active record with this employee ID already exists.")
                    print("deleted the employ")
                    obj=EmployeeSkillTable.objects.get(emp_code=attrs['emp_code'])
                    obj.delete()
                    # obj.save()
                else :
                    print("nhi gaya")
                    return  attrs