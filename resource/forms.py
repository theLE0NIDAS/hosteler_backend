from django.forms import ModelForm
from .models import Resource

class ResourceForm(ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'description', 'correct_count', 'damaged_count', 'resource_type']

class ResourceUpdateForm(ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'description', 'correct_count', 'damaged_count', 'resource_photo']