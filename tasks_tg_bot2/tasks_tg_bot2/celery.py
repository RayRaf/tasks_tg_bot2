# myproject/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tasks_tg_bot2.settings')
app = Celery('tasks_tg_bot2')

# Читает настройки из django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находит задачи в tasks.py приложений
app.autodiscover_tasks()
