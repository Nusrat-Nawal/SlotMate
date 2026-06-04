from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.CharField(max_length=100)
    department = models.TextField(max_length=50)
    
    def __str__(self):
        return self.user.username
        
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)

    notification_type = models.CharField(max_length=50, null=True, blank=True)
    related_id = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

class SlotRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #Current Slots
    current_course_code = models.CharField(max_length=20,blank=False,null=False)
    current_section = models.CharField(max_length=10 ,blank=False,null=False)
    current_faculty = models.CharField(max_length=10,blank=False,null=False)
    current_time = models.CharField(max_length=50,blank=False,null=False)
    current_days = models.CharField(max_length=100,blank=False,null=False)
    #Preferred Slots
    preferred_course_code = models.CharField(max_length=20,blank=False,null=False)
    preferred_section = models.CharField(max_length=10,null=True, blank=True)
    preferred_faculty = models.CharField(max_length=10,null=True, blank=True)
    preferred_time = models.CharField(max_length=50,null=True, blank=True)
    preferred_days = models.CharField(max_length=100,null=True, blank=True)

    #For Any Options
    any_day = models.BooleanField(default=False)
    any_time = models.BooleanField(default=False)
    any_section = models.BooleanField(default=False)
    any_faculty = models.BooleanField(default=False)

    status = models.CharField(max_length=20, default="Pending")  
    created_at = models.DateTimeField(auto_now_add=True)
    
class Match(models.Model):
    user_a = models.ForeignKey(User, on_delete=models.CASCADE, related_name="matches_as_a")
    user_b = models.ForeignKey(User, on_delete=models.CASCADE, related_name="matches_as_b")

    request_a = models.ForeignKey(SlotRequest, on_delete=models.CASCADE, related_name="request_a")
    request_b = models.ForeignKey(SlotRequest, on_delete=models.CASCADE, related_name="request_b")

    score_a_to_b = models.FloatField()
    score_b_to_a = models.FloatField()
    mutual_score = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user_a", "user_b")  
    @property
    def a_reveal_status(self):
        reveal = RevealRequest.objects.filter(match=self, sender=self.user_a).first()
        return reveal.status if reveal else "not_sent"

    @property
    def b_reveal_status(self):
        reveal = RevealRequest.objects.filter(match=self, sender=self.user_b).first()
        return reveal.status if reveal else "not_sent" 

class RevealRequest(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_reveals")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_reveals")

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)