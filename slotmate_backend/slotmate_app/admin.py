from django.contrib import admin
from .models import SlotRequest, StudentProfile

# Register your models here.
admin.site.register(StudentProfile)
admin.site.register(SlotRequest)