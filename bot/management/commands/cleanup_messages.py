from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from bot.models import ChatMessage

class Command(BaseCommand):
    help = 'Cleanup old chat messages based on retention policy'

    def handle(self, *args, **options):
        # Delete messages older than retention period
        retention_date = timezone.now() - timedelta(days=settings.CHAT_MESSAGE_RETENTION_DAYS)
        old_messages = ChatMessage.objects.filter(timestamp__lt=retention_date)
        deleted_count = old_messages.count()
        old_messages.delete()

        # Keep only last N messages per user
        for sender in ChatMessage.objects.values_list('sender', flat=True).distinct():
            messages = ChatMessage.objects.filter(sender=sender).order_by('-timestamp')[settings.CHAT_MESSAGE_MAX_PER_USER:]
            messages.delete()

        self.stdout.write(
            self.style.SUCCESS(f'Successfully cleaned up {deleted_count} old messages')
        )