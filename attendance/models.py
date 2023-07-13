from django.db import models
from student.models import Student
from mess.models import Mess

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status_choices = (
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('LEAVE', 'Leave'),
    )
    status = models.CharField(max_length=10, choices=status_choices, default='ABSENT')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'date')
    
    def __str__(self):
        return f"{self.student.get_roll_number()} - {self.date} - {self.get_status_display()}"

class Leave(models.Model):
    leave_id = models.IntegerField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    leave_from = models.DateField()
    leave_to = models.DateField()
    leave_location = models.CharField(max_length=200)
    reason_for_leave = models.CharField(max_length=200)
    status_choices = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )
    status = models.CharField(max_length=10, choices=status_choices, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return f"{self.student.get_roll_number()} - {self.leave_from} to {self.leave_to} - {self.get_status_display()}"

class Rebate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    leave_id = models.OneToOneField(Leave, on_delete=models.CASCADE)
    total_contiguous_leaves = models.PositiveIntegerField(default=0)
    rebate_id = models.IntegerField(primary_key=True)
    rebate_amount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.get_roll_number()} - {self.rebate_amount}"