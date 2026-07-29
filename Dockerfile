# Используем официальный образ Python
FROM python:3.12-slim

# # Устанавливаем системные зависимости для MySQL
# RUN apt-get update && apt-get install -y \
#     gcc \
#     default-libmysqlclient-dev \
#     && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Копируем весь проект
COPY . .

ENV SECRET_KEY=build-key
ENV DB_NAME=build
ENV DB_USER=build
ENV DB_PASSWORD=build
ENV DB_HOST=build
ENV EMAIL_HOST_USER=build
ENV EMAIL_HOST_PASSWORD=build

# Собираем статику
RUN python manage.py collectstatic --noinput

# Открываем порт для Django
EXPOSE 8000

# Запускаем сервер
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
