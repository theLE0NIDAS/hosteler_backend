from django.db import models
from cloudinary.models import CloudinaryField

class Mess(models.Model):
    mess_id = models.IntegerField(primary_key=True)
    vendor_name = models.CharField(max_length=100)
    manager_name = models.CharField(max_length=100, default='')
    contact_number = models.CharField(max_length=10)
    cost_per_day = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    rebate_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    contract_start_date = models.DateField()
    contract_end_date = models.DateField()
    contract_duration = models.IntegerField()  # Duration in months
    menu_image = CloudinaryField('image', null=True)
    
    def __str__(self):
        return self.vendor_name
