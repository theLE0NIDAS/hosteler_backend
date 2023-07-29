from django.forms import ModelForm
from .models import Complaint

class ComplaintForm(ModelForm):
    class Meta:
        model = Complaint
        fields = ['student', 'category', 'location', 'description']

class ComplaintUpdateForm(ModelForm):
    class Meta:
        model = Complaint
        fields = ['status', 'remarks']