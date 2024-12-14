# tasks/management/commands/setwebhook.py
from django.core.management.base import BaseCommand
import os
from telebot import TeleBot

TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = TeleBot(TOKEN)

class Command(BaseCommand):
    help = 'Set Telegram webhook'

    def handle(self, *args, **options):
        url = "https://tasks-tg-bot.astrolis.ru/telegram/webhook/"
        bot.set_webhook(url=url)
        self.stdout.write(self.style.SUCCESS("Webhook set successfully"))
