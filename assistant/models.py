from django.db import models
from django.conf import settings

class OpenAIThread(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    thread_id = models.CharField(max_length=100)
    assistant_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)