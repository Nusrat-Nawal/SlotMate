from django.utils import timezone
from datetime import timedelta
from .models import SlotRequest, Match

def delete_old_data():
    cutoff = timezone.now() - timedelta(days=30)

    # delete old requests
    SlotRequest.objects.filter(
        created_at__lt=cutoff
    ).delete()

    # delete old matches
    Match.objects.filter(
        created_at__lt=cutoff
    ).delete()