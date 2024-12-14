from django.db import models
from django.contrib.auth.models import User
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    chat_id = models.BigIntegerField(unique=True, null=True, blank=True)
    access_token = models.CharField(max_length=64, unique=True, blank=True, null=True)

    def generate_token(self):
        self.access_token = uuid.uuid4().hex
        self.save()

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    text = models.CharField(max_length=255)
    reminder_time = models.DateTimeField(null=True, blank=True)
    reminder_set = models.BooleanField(default=False)
    reminder_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.text
