from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class ChatMessage(models.Model):
    sender = models.CharField(max_length=100)
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']

    @classmethod
    def cleanup_old_messages(cls, sender):
        """Clean up old messages for a specific sender"""
        # Delete messages older than retention period
        retention_date = timezone.now() - timedelta(days=settings.CHAT_MESSAGE_RETENTION_DAYS)
        cls.objects.filter(sender=sender, timestamp__lt=retention_date).delete()

        # Keep only last N messages
        messages = cls.objects.filter(sender=sender).order_by('-timestamp')[settings.CHAT_MESSAGE_MAX_PER_USER:]
        messages.delete()
