# Django проект visited_links

Инструкция к запуску

## Установка

1. Клонируйте репозиторий:

```
git clone https://github.com/SofiyaBochina/visited_domains
```

2. Перейдите в директорию проекта:

```
cd visited_domains
```

3. Создайте виртуальное окружение и активируйте его:

```
python3 -m venv venv
source venv/bin/activate
```

4. Установите зависимости проекта:

```
pip install -r requirements.txt
```

## Настройка

1. Создайте файл .env в корневой директории проекта.
2. Откройте файл .env и заполните его данными:

```
SECRET_KEY = your_secret_key
DEBUG = True/False
POSTGRES_DB = your_postgres_db_name
POSTGRES_USER = your_postgres_username
POSTGRES_PASSWORD = your_postgres_password
POSTGRES_HOST = your_postgres_host
POSTGRES_PORT = your_postgres_port
```

## Запуск миграций

1. Выполните миграции для создания таблиц базы данных:

```
python manage.py migrate
```

2. Запустите команду для сбора статики:

```
python manage.py collectstatic
```

Протестировать можно с помощью:
```
python manage.py test
```

## Запуск проекта

```
python manage.py runserver
```

Проект станет доступен по адресу http://localhost:8000/.
Эндпоинты:
```
GET visited_domains/
POST visited_links/
```
