from django.core.management.base import BaseCommand
from django.utils import timezone
import os
from telebot import TeleBot
from tasks.models import Task

TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = TeleBot(TOKEN)

class Command(BaseCommand):
    help = 'Отправка напоминаний о задачах'

    def handle(self, *args, **options):
        now = timezone.now()
        tasks_to_notify = Task.objects.filter(reminder_set=True, reminder_sent=False, reminder_time__lte=now)
        for task in tasks_to_notify:
            if task.user.userprofile.chat_id:
                chat_id = task.user.userprofile.chat_id
                bot.send_message(chat_id, f"Напоминание: {task.text}")
                task.reminder_sent = True
                task.save()
