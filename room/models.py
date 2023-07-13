from django.db import models
from student.models import Student

class Room(models.Model):
    room_number = models.CharField(primary_key=True, max_length=3)
    floor_number = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField(default=1)
    
    OCCUPANCY_STATUS = (
        ('OCCUPIED', 'Occupied'),
        ('VACANT', 'Vacant'),
    )
    occupancy_status = models.CharField(max_length=10, choices=OCCUPANCY_STATUS, default='VACANT')
    student = models.OneToOneField(Student, on_delete=models.SET_NULL, null=True, blank=True)
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['room_number']
    
    def __str__(self):
        return f"{self.room_number} - {self.get_occupancy_status_display()} - {self.student}"
