# tasks/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import Task
from .bot_instance import bot

@shared_task
def send_notifications():
    now = timezone.now()
    tasks_to_notify = Task.objects.filter(
        reminder_set=True,
        reminder_sent=False,
        reminder_time__lte=now
    )
    for task in tasks_to_notify:
        if task.user.userprofile.chat_id:
            chat_id = task.user.userprofile.chat_id
            bot.send_message(chat_id, f"Напоминание: {task.text}")
            task.reminder_sent = True
            task.save()
