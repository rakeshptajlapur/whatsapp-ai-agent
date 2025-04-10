from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render
from django.db import models  # Add this import
from django.db.models import Count, Max
from .models import ChatMessage, TrainingContent

class ChatThreadFilter(admin.SimpleListFilter):
    title = 'Chat Thread'
    parameter_name = 'sender'

    def lookups(self, request, model_admin):
        senders = ChatMessage.get_sender_stats()
        return [(sender['sender'], f"{sender['sender']} ({sender['total_messages']})") 
                for sender in senders]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(sender=self.value())
        return queryset

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'message', 'response', 'timestamp']
    list_filter = ['sender']
    search_fields = ['sender', 'message']
    ordering = ['-timestamp']

@admin.register(TrainingContent)
class TrainingContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'is_active']
    list_filter = ['content_type', 'is_active']
    search_fields = ['title', 'content']
