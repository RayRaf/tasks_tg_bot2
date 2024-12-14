from django.urls import path
from .telegram import telegram_webhook

urlpatterns = [
    path('', telegram_webhook, name='telegram_webhook'),
]
