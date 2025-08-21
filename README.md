# Task Manager API

FastAPI приложение для управления задачами с CRUD операциями.

## Features
- FastAPI + SQLAlchemy + PostgreSQL
- Alembic миграции
- Pytest тесты
- Swagger документация
- Логирование с ротацией

## Установка
```
pip install -r requirements.txt
```

## Настройка БД
```
alembic upgrade head
```

## Запуск.
```
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints.
- GET http://localhost:8000/docs - Swagger документация.
- GET http://localhost:8000/health - Health check.
- GET http://localhost:8000/api/v1/tasks - Список задач.
- POST http://localhost:8000/api/v1/tasks - Создать задачу.
- GET http://localhost:8000/api/v1/tasks/{id} - Получить задачу.
- PUT http://localhost:8000/api/v1/tasks/{id} - Обновить задачу.
- DELETE http://localhost:8000/api/v1/tasks/{id} - Удалить задачу.

## Переменные окружения (.env)
```
APP_NAME=some_task_manager
APP_NAME_DESCRIPTION=Название приложения для идентификации.
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/some_task_manager # Свой адресс бд.
ENV=dev
ENV_DESCRIPTION=Среда выполнения: dev, prod или test.
LOG_LEVEL=INFO
LOG_LEVEL_DESCRIPTION=Уровень детализации логов.
LOG_LEVEL_ERROR=Некорректный уровень логирования.
LOG_DIR=logs
LOG_DIR_DESCRIPTION=Директория для хранения файлов с логами.
```

## Тестирование (pytest).

При включёном сервере в корневой папке ввести команду.
```
python -m pytest tests/task.py -v -s
```
