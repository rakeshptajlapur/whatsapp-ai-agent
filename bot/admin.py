from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'message', 'response', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['sender', 'message', 'response']
