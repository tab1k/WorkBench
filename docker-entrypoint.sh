#!/bin/sh
set -e

# Ожидаем запуска базы данных
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q'; do
  >&2 echo "База данных недоступна - ожидание запуска..."
  sleep 1
done



# Запускаем сервер Django
exec "$@"
