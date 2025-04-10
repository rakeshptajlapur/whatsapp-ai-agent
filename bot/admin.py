from django.contrib import admin
from .models import ChatMessage, TrainingContent

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'message', 'response', 'timestamp']
    list_filter = ['timestamp', 'sender']
    search_fields = ['sender', 'message', 'response']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
    date_hierarchy = 'timestamp'
    list_per_page = 50

    fieldsets = (
        ('Chat Details', {
            'fields': ('sender', 'timestamp')
        }),
        ('Conversation', {
            'fields': ('message', 'response'),
            'classes': ('wide',)
        })
    )

@admin.register(TrainingContent)
class TrainingContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'is_active', 'priority', 'updated_at']
    list_filter = ['content_type', 'is_active']
    search_fields = ['title', 'content']
    list_editable = ['is_active', 'priority']
