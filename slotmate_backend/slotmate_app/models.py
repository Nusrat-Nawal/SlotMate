from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.CharField(max_length=100)
    department = models.TextField(max_length=50)
    
    def __str__(self):
        return self.user.username
class SlotRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #Current Slots
    current_course_code = models.CharField(max_length=20)
    current_section = models.CharField(max_length=10)
    current_faculty = models.CharField(max_length=10)
    current_time = models.CharField(max_length=50)
    current_days = models.CharField(max_length=100)
    #Preferred Slots
    preferred_course_code = models.CharField(max_length=20)
    preferred_section = models.CharField(max_length=10)
    preferred_faculty = models.CharField(max_length=10)
    preferred_time = models.CharField(max_length=50)
    preferred_days = models.CharField(max_length=100)

    #For Any Options
    any_day = models.BooleanField(default=False)
    any_time = models.BooleanField(default=False)
    any_section = models.BooleanField(default=False)
    any_faculty = models.BooleanField(default=False)

    status = models.CharField(max_length=20, default="Pending")  
    created_at = models.DateTimeField(auto_now_add=True)
    
    