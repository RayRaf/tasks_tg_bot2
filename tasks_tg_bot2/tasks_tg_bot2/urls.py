from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),
    path('telegram/webhook/', include('tasks.urls_telegram'))  # отдельный URL для вебхука бота
]
