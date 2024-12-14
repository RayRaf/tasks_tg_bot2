# tasks/bot_instance.py
import os
from telebot import TeleBot

TOKEN = os.environ.get('TELEGRAM_TOKEN')
if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN is not set")

bot = TeleBot(TOKEN)
