from rest_framework import serializers
from Zero_Count_Rna_Payload_Tool.models import *


class ser_Raw_Kpi_Table_4G(serializers.ModelSerializer):
    class Meta:
        model = Raw_Kpi_Table_4G
        fields = "__all__"


class ser_Raw_Kpi_Table_2G(serializers.ModelSerializer):
    class Meta:
        model = Raw_Kpi_Table_2G
        fields = "__all__"


class ser_Daily_4G_KPI(serializers.ModelSerializer):
    class Meta:
        model = Daily_4G_KPI
        fields = "__all__"


class ser_Daily_4G_KPI_2(serializers.ModelSerializer):
    class Meta:
        model = Daily_4G_KPI
        fields = [
            "Short_name",
            "Date",
            "MV_4G_Data_Volume_GB",
            "MV_Radio_NW_Availability",
            "MV_VoLTE_raffic",
            "name_SiteA",
            "name_SiteB",
        ]


class ser_Daily_2G_KPI(serializers.ModelSerializer):
    class Meta:
        model = Daily_2G_KPI
        fields = "__all__"


class ser_Ticket_Counter(serializers.ModelSerializer):
    Ownership = serializers.CharField(allow_blank=True)
    Site_ID = serializers.CharField(allow_blank=True)
    category = serializers.CharField(allow_blank=True)

    class Meta:
        model = Ticket_Counter_Table_Data
        fields = "__all__"
        

from rest_framework import serializers
from .models import Daily_4G_KPI_REPORT

class Daily4GKPIReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Daily_4G_KPI_REPORT
        fields = '__all__'




class level1Serializer(serializers.ModelSerializer):
    class Meta:
        model = level1
        fields = '__all__'
        
class level2Serializer(serializers.ModelSerializer):
    class Meta:
        model = level2
        fields = '__all__'
        
        
class level3Serializer(serializers.ModelSerializer):
    class Meta:
        model = level3
        fields = '__all__'

class level4Serializer(serializers.ModelSerializer):
    class Meta:
        model = level4
        fields = '__all__'                
                

        
class  ThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Threshold
        fields = '__all__'