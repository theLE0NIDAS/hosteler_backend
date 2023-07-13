from rest_framework import serializers
from .models import Attendance
from .models import Leave
from .models import Rebate

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = '__all__'

class RebateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rebate
        fields = '__all__'