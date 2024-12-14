FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

CMD ["uvicorn", "tasks_tg_bot2.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
