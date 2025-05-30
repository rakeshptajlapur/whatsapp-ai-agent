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

    def __str__(self):
        return f"{self.sender} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    @property
    def short_message(self):
        """Return truncated message for display"""
        return self.message[:50] + '...' if len(self.message) > 50 else self.message

    @classmethod
    def get_sender_stats(cls):
        """Get statistics for each sender"""
        from django.db.models import Count
        return cls.objects.values('sender').annotate(
            total_messages=Count('id')
        ).order_by('-total_messages')

    @classmethod
    def cleanup_old_messages(cls, sender):
        """Clean up old messages for a specific sender"""
        # Delete messages older than retention period
        retention_date = timezone.now() - timedelta(days=settings.CHAT_MESSAGE_RETENTION_DAYS)
        cls.objects.filter(sender=sender, timestamp__lt=retention_date).delete()

        # Keep only last N messages
        messages = cls.objects.filter(sender=sender).order_by('-timestamp')[settings.CHAT_MESSAGE_MAX_PER_USER:]
        messages.delete()

class TrainingContent(models.Model):
    CONTENT_TYPES = (
        ('rules', 'Business Rules'),
        ('faq', 'FAQ'),
        ('policy', 'Policies'),
        ('pricing', 'Pricing'),
        ('service', 'Services'),
    )
    
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)
    source_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', '-updated_at']
