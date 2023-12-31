from django.forms import ModelForm
from .models import Mess

class MessForm(ModelForm):
    class Meta:
        model = Mess
        fields = '__all__'
        exclude = ['mess_id', 'contract_end_date', 'mess_image']

class MessUpdateForm(ModelForm):
    class Meta:
        model = Mess
        fields = '__all__'
        exclude = ['mess_id', 'contract_end_date', 'mess_image']

# class MessMenuForm(ModelForm):
#     class Meta:
#         model = MessMenu
#         fields = '__all__'