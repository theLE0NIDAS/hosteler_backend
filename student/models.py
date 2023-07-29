from django.db import models
from cloudinary.models import CloudinaryField

class Student(models.Model):
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=10)
    blood_group_choices = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    )
    blood_group = models.CharField(max_length=3, choices=blood_group_choices, default='')
    photo = CloudinaryField('image', null=True) 
    # models.ImageField(upload_to='images/', null=True, blank=True)
    
    # Academic Information
    roll_number = models.CharField(primary_key=True, max_length=20)
    email_address = models.EmailField()
    batch = models.IntegerField()
    department = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    
    # Parent/Guardian Information
    parent_first_name = models.CharField(max_length=100)
    parent_last_name = models.CharField(max_length=100)
    parent_email = models.EmailField()
    parent_contact_number = models.CharField(max_length=10)
    
    # Additional Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['roll_number']

    def __str__(self):
        return self.roll_number

