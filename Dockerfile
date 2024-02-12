# Используем базовый образ Python 3.10
FROM python:3.10

# Устанавливаем переменную окружения для отключения вывода логов Python в консоль
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы зависимостей в рабочую директорию
COPY requirements.txt /app/

# Устанавливаем зависимости Python из файла requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы из текущей директории хоста в рабочую директорию контейнера
COPY . /app/

# Запускаем миграции Django
RUN python manage.py migrate

# Команда для запуска сервера Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
