from django.urls import path
from .views import token_task_list, token_task_edit

app_name = 'tasks'

urlpatterns = [
    # Просмотр задач по токену
    path('view/', token_task_list, name='token_task_list'),
    # Редактирование задачи по токену
    path('view/edit/<int:task_id>/', token_task_edit, name='token_task_edit'),
]
