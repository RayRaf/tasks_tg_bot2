# Telegram Tasks Bot 2

**[@RaysNotifficationBot](https://t.me/RaysNotifficationBot)** – это вторая версия Telegram-бота для управления задачами. Новый бот был переработан с использованием Django и вебхуков, чтобы обеспечить более стабильную работу по сравнению с первой версией, где использовался метод поллинга.

Репозиторий проекта доступен по адресу: [https://github.com/RayRaf/tasks_tg_bot2.git](https://github.com/RayRaf/tasks_tg_bot2.git).

## Основные возможности

- **Управление задачами**:
  - Создание задач через Telegram.
  - Просмотр, редактирование и удаление задач через Telegram и веб-интерфейс.
  - Установка напоминаний на задачи.

- **Интеграция**:
  - Уникальные токенизированные ссылки для веб-доступа к задачам.
  - Веб-интерфейс для просмотра и редактирования задач.

- **Система уведомлений**:
  - Использование Celery и Redis для обработки фоновых задач и отправки напоминаний.

- **Оптимизация для продакшн-среды**:
  - Использование асинхронного сервера Uvicorn для высокой производительности.

## Что нового во второй версии?

- **Переход на Django и вебхуки**: Обеспечивает стабильность и скорость работы по сравнению с поллингом.
- **Адаптация для асинхронных операций**: Сервер Uvicorn обеспечивает надежную работу в продакшн-среде.
- **Улучшение архитектуры**: Гибкость и удобство разработки.
- **Масштабируемость**: Подходит для больших объемов данных и пользователей.

## Предыдущая версия бота

Первая версия бота, основанная на методе поллинга, доступна по адресу:  
[https://github.com/RayRaf/tasks_tg_bot](https://github.com/RayRaf/tasks_tg_bot).  

Эта версия проще в развертывании и использовании, но подходит для небольших проектов и имеет ограничения по стабильности из-за особенностей метода поллинга. Вы можете попробовать обе версии и выбрать ту, которая лучше подходит под ваши задачи.

## Требования

- Python 3.8+
- Docker
- Redis

## Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/RayRaf/tasks_tg_bot2.git
cd tasks_tg_bot2
```

### 2. Настройка переменных окружения

Создайте файл `.env` в корневой директории проекта и укажите следующие переменные:

```env
DJANGO_SECRET_KEY=ваш_секретный_ключ
TELEGRAM_TOKEN=ваш_токен_бота
REDIS_URL=redis://redis:6379/0
```

### 3. Сборка и запуск через Docker

```bash
docker-compose up --build
```

Эта команда запустит следующие сервисы:
- **Redis**: для управления очередями задач.
- **Web**: Django-приложение с поддержкой ASGI через Uvicorn.
- **Celery**: для обработки фоновых задач.
- **Celery Beat**: для планирования периодических задач.

### 4. Настройка вебхука Telegram

Укажите вебхук для вашего Telegram-бота, например:

```bash
curl -X POST "https://api.telegram.org/bot<ваш_токен_бота>/setWebhook" -d "url=https://ваш-домен.com/"
```

## Структура проекта

- **`docker-compose.yml`**: конфигурация сервисов для работы Redis, Django, Celery и Celery Beat.
- **`telegram.py`**: обработка команд и взаимодействия с пользователями через Telegram.
- **`urls.py`**: маршруты для веб-интерфейса.
- **`views.py`**: логика отображения и редактирования задач через токенизированные ссылки.
- **`urls_telegram.py`**: маршрут для вебхука Telegram.

## Использование

1. Взаимодействуйте с ботом через команды:
   - **Новая задача**: создание новой задачи.
   - **Список задач**: просмотр всех задач.
   - **Удалить задачу**: удаление определенной задачи.
   - **Установить время**: установка напоминания для задачи.
   - **Ссылка на веб**: получение уникальной ссылки на задачи.

2. Используйте веб-интерфейс для редактирования задач и управления напоминаниями.

## Разработка

### Запуск локально

Установите зависимости:

```bash
pip install -r requirements.txt
```

Запустите сервер разработки:

```bash
python manage.py runserver
```

### Запуск Celery локально

```bash
celery -A tasks_tg_bot2 worker --loglevel=info
```

### Запуск Celery Beat локально

```bash
celery -A tasks_tg_bot2 beat --loglevel=info
```

## Вклад в проект

Будем рады вашему участию! Открывайте issues или отправляйте pull requests в репозиторий [https://github.com/RayRaf/tasks_tg_bot2.git](https://github.com/RayRaf/tasks_tg_bot2.git) для обсуждения улучшений.

