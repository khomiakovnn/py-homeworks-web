# Домашнее задание к лекции «Docker-compose»

Конфигурация состоит из трех контейнеров:
* Backend
* Nginx
* Postgres

Каждый контейнер (dockerfile) в отдельной папке.

## Контейнеры:

### Backend
Backend построен на образе Python с дополнительно установленным в контейнер и настроенным Gunicorn
* Папка проекта CRUD - stocks_products
* Настройки gunicorn в папке Gunicorn_settings

#### REST API приложения:
1. *"/api/v1/stocks/"* - склады
2. *"/api/v1/products/"* - продукты

### Nginx
* Настройки nginx в папке отдельным файлом nginx.conf

### Postgres
* Базовый образ без изменений

## Описание:
* Проверить можно на [localhost:1337/admin](localhost:1337/admin)
* После установки контейнеров нужно сделать миграции
* Статику не пробрасывал

## Использованы команды:
* docker-compose build
* docker-compose up -d
* docker-compose exec web python manage.py migrate --noinput