# tasks/telegram.py
import os
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User
from telebot import TeleBot, types
from .models import UserProfile, Task
from .bot_instance import bot



def ensure_user_registered(chat_id):
    profile = UserProfile.objects.filter(chat_id=chat_id).first()
    if not profile:
        # Создаем нового пользователя при первом обращении
        user = User.objects.create_user(username=f'tg_{chat_id}', password='somepassword')
        profile = UserProfile.objects.create(user=user, chat_id=chat_id)
        profile.generate_token()
        send_unique_link(chat_id, profile)
    return profile.user

def send_unique_link(chat_id, profile):
    unique_link = f"https://tasks-tg-bot.astrolis.ru/tasks/view/?token={profile.access_token}"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Открыть список задач", url=unique_link))
    bot.send_message(chat_id, "Вот ваша персональная ссылка на веб-страницу со списком задач:", reply_markup=markup)

@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        json_data = request.body.decode('utf-8')
        update = types.Update.de_json(json_data)
        bot.process_new_updates([update])  # Передаем обновление боту
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': True})

def create_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    # Добавляем команду для повторного получения ссылки
    buttons = ["Новая задача", "Список задач", "Удалить все", "Удалить задачу", "Помощь", "Установить время", "Ссылка на веб"]
    keyboard.add(*buttons)
    return keyboard

@bot.message_handler(func=lambda message: True)
def handle_commands(message):
    user = ensure_user_registered(message.chat.id)
    text = message.text
    if text == "Новая задача":
        msg = bot.send_message(message.chat.id, "Введите текст задачи:")
        bot.register_next_step_handler(msg, lambda m: add_task(m, user))
    elif text == "Список задач":
        list_tasks(message, user)
    elif text == "Удалить все":
        confirm_removal_all(message, user)
    elif text == "Удалить задачу":
        delete_task(message, user)
    elif text == "Установить время":
        set_time(message, user)
    elif text == "Помощь":
        bot.send_message(message.chat.id, "Используйте кнопки для управления задачами.", reply_markup=create_keyboard())
    elif text == "Ссылка на веб":
        # Повторно отправляем уникальную ссылку
        profile = UserProfile.objects.get(user=user)
        send_unique_link(message.chat.id, profile)
    else:
        bot.send_message(message.chat.id, "Неизвестная команда", reply_markup=create_keyboard())

def add_task(message, user):
    Task.objects.create(user=user, text=message.text)
    bot.send_message(message.chat.id, "Задача добавлена!", reply_markup=create_keyboard())

def list_tasks(message, user):
    tasks = user.tasks.all()
    if tasks:
        response = ''
        for idx, task in enumerate(tasks):
            if task.reminder_set:
                reminder_time = task.reminder_time.strftime('%Y-%m-%d %H:%M')
                response += f"{idx + 1}. {task.text} (Когда: {reminder_time})\n"
            else:
                response += f"{idx + 1}. {task.text}\n"
        bot.send_message(message.chat.id, f"Ваши задачи:\n{response}", reply_markup=create_keyboard())
    else:
        bot.send_message(message.chat.id, "У вас пока нет задач.", reply_markup=create_keyboard())

def confirm_removal_all(message, user):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Да, удалить все", callback_data="confirm_delete_all"))
    keyboard.add(types.InlineKeyboardButton("Нет, оставить", callback_data="cancel_delete_all"))
    bot.send_message(message.chat.id, "Вы уверены, что хотите удалить все задачи?", reply_markup=keyboard)

def delete_task(message, user):
    tasks = user.tasks.all()
    if not tasks:
        bot.send_message(message.chat.id, "У вас нет задач для удаления.")
        return
    keyboard = types.InlineKeyboardMarkup()
    for task in tasks:
        button = types.InlineKeyboardButton(task.text, callback_data=f'delete_task_{task.id}')
        keyboard.add(button)
    bot.send_message(message.chat.id, "Выберите задачу для удаления:", reply_markup=keyboard)

def set_time(message, user):
    tasks = user.tasks.all()
    if not tasks:
        bot.send_message(message.chat.id, "У вас нет задач для установки времени.")
        return
    keyboard = types.InlineKeyboardMarkup()
    for task in tasks:
        button = types.InlineKeyboardButton(task.text, callback_data=f'set_time_{task.id}')
        keyboard.add(button)
    bot.send_message(message.chat.id, "Выберите задачу для установки времени:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    user = ensure_user_registered(call.message.chat.id)
    data = call.data
    if data == "confirm_delete_all":
        user.tasks.all().delete()
        bot.edit_message_text("Все задачи удалены.", call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id, "Все задачи удалены")
    elif data == "cancel_delete_all":
        bot.edit_message_text("Удаление всех задач отменено.", call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id, "Удаление отменено")
    elif data.startswith('delete_task_'):
        task_id = int(data.split('_')[-1])
        delete_specific_task(call, user, task_id)
    elif data.startswith('set_time_'):
        task_id = int(data.split('_')[-1])
        msg = bot.send_message(call.message.chat.id, "Введите время для задачи в формате ГГГГ-ММ-ДД ЧЧ:ММ:")
        bot.register_next_step_handler(msg, lambda m: set_reminder_time(m, user, task_id))

def delete_specific_task(call, user, task_id):
    task = user.tasks.filter(pk=task_id).first()
    if task:
        task.delete()
        bot.answer_callback_query(call.id, "Задача удалена")
        message = call.message
        list_tasks(message, user)
    else:
        bot.answer_callback_query(call.id, "Задача не найдена")

def set_reminder_time(message, user, task_id):
    try:
        reminder_time = datetime.datetime.strptime(message.text, '%Y-%m-%d %H:%M')
        if reminder_time < datetime.datetime.now():
            bot.send_message(message.chat.id, "Нельзя установить время в прошлом.")
            return
        task = user.tasks.filter(pk=task_id).first()
        if task:
            task.reminder_time = reminder_time
            task.reminder_set = True
            task.reminder_sent = False
            task.save()
            bot.send_message(message.chat.id, "Время установлено.")
            list_tasks(message, user)
        else:
            bot.send_message(message.chat.id, "Задача не найдена.")
    except ValueError:
        bot.send_message(message.chat.id, "Неправильный формат времени. Используйте ГГГГ-ММ-ДД ЧЧ:ММ.")
