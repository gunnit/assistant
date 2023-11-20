from django.contrib import admin
from .models import OpenAIThread

@admin.register(OpenAIThread)
class OpenAIThreadAdmin(admin.ModelAdmin):
    list_display = ('user', 'thread_id', 'assistant_id', 'created_at')
    list_filter = ('user',)
