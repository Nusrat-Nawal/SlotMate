from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from slotmate_app.models import SlotRequest, Match


class Command(BaseCommand):
    help = "Delete requests and matches older than 30 days"

    def handle(self, *args, **kwargs):
        cutoff = timezone.now() - timedelta(days=30)

        deleted_requests = SlotRequest.objects.filter(
            created_at__lt=cutoff
        ).delete()

        deleted_matches = Match.objects.filter(
            created_at__lt=cutoff
        ).delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Cleanup done. Requests deleted: {deleted_requests[0]}, Matches deleted: {deleted_matches[0]}"
            )
        )