from django.contrib import admin
from .models import SlotRequest, StudentProfile , Match

# Register your models here.
admin.site.register(StudentProfile)
admin.site.register(SlotRequest)
admin.site.register(Match)