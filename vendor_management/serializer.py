from rest_framework import serializers
from .models import *

class ser_progress_report(serializers.ModelSerializer):
    class Meta:
        model = Progress_report
        fields = '__all__'

class ser_upload_status(serializers.ModelSerializer):
    class Meta:
        model = upload_status
        fields = '__all__'

class ser_vendor_po_approver_upload_status(serializers.ModelSerializer):
    class Meta:
        model = vendor_po_approver_upload_status
        fields = '__all__'


class ser_vendor_po_No_upload_status(serializers.ModelSerializer):
    class Meta:
        model = vendor_po_approver_upload_status
        fields = '__all__'

class ser_circle_list(serializers.ModelSerializer):
    class Meta:
        model = circle_list
        fields = '__all__'