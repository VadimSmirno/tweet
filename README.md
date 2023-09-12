# FastAPI Tweet App

Этот проект представляет собой упрощенный аналог приложения для сообщений типа "Твит". Он использует FastAPI для создания API, PostgreSQL для хранения данных и Docker/Docker Compose для контейнеризации приложения.

## Структура проекта

Проект имеет следующую структуру:

├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── alembic.ini
├── app/
│   ├── frontend/
│   ├── add_test_data/
│   ├── app.py
│   ├── database.py
│   ├── Dockerfile
│   ├── functions.py
│   ├── models.py
│   ├── requirements.txt
│   ├── schemas.py
├── config.py
├── docker-compose.yml
├── README.md


## Использование Docker и Docker Compose

Для запуска приложения и базы данных с использованием Docker и Docker Compose, выполните следующие шаги:

1. Убедитесь, что у вас установлены Docker и Docker Compose.

2. Создайте файл `.env` в корневой папке проекта и установите следующие переменные окружения:

```dotenv
POSTGRES_DB=your_database_name
POSTGRES_USER=your_database_user
POSTGRES_PASSWORD=your_database_password


## Запустите приложение и базу данных с помощью Docker Compose:

docker-compose up -d --build
После запуска, приложение будет доступно по адресу http://localhost:1111. Документация API будет доступна по адресу http://localhost:8000/docs.

Для остановки приложения и базы данных выполните:

docker-compose down

## Миграции базы данных

* Для управления миграциями базы данных используется Alembic. Вы можете создавать и применять миграции с помощью следующих команд:
    alembic revision -m "Название миграции"
* Применить миграции:
    alembic upgrade head
* Откатить миграции:
    alembic downgrade -1  # Откатить последнюю миграцию

 ## Зависимости Python
Зависимости Python указаны в файле requirements.txt. Вы можете установить их с помощью pip:   
pip install -r requirements.txt

