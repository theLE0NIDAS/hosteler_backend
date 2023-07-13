from django.forms import ModelForm
from .models import Leave, Attendance

class AttendanceForm(ModelForm):
    class Meta:
        model = Attendance
        fields = ['status']

class LeaveForm(ModelForm):
    class Meta:
        model = Leave
        fields = ['student', 'leave_from', 'leave_to', 'leave_location', 'reason_for_leave']

class LeaveUpdateForm(ModelForm):
    class Meta:
        model = Leave
        fields = ['status']