from django.db import models
from cloudinary.models import CloudinaryField

class Resource(models.Model):
    name = models.CharField(max_length=50)
    resource_id = models.CharField(primary_key=True, max_length=25)
    description = models.TextField()
    correct_count = models.PositiveIntegerField()
    damaged_count = models.PositiveIntegerField()
    total_count = models.PositiveIntegerField(default=0)
    resource_type_choices = (
        ('ELECTRICAL', 'Electrical'),  
        ('PLUMBING', 'Plumbing'),
        ('CARPENTRY', 'Carpentry'),
        ('SANITATION', 'Sanitation'),
        ('OTHERS', 'Others'),
    )
    resource_type = models.CharField(max_length=15, choices=resource_type_choices, default='OTHERS')
    resource_photo = CloudinaryField('images', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.total_count}"

