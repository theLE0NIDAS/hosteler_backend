from django.db import models
from student.models import Student
from room.models import Room
from datetime import datetime
from cloudinary.models import CloudinaryField

class Complaint(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    complaint_id = models.IntegerField(primary_key=True)
    category_choices = (
        ('ELECTRICAL', 'Electrical'),
        ('PLUMBING', 'Plumbing'),
        ('CARPENTRY', 'Carpentry'),
        ('SANITATION', 'Sanitation'),
        ('OTHERS', 'Others'),
    )
    category = models.CharField(max_length=15, choices=category_choices, default='OTHERS')
    location = models.CharField(max_length=50, default='')

    description = models.TextField()
    photo = CloudinaryField('images', null=True)
    status_choices = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    )
    status = models.CharField(max_length=15, choices=status_choices, default='PENDING')

    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']
    
    def __str__(self):
        return self.category