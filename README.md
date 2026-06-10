# Учёт личных финансов

Веб-приложение для учёта доходов и расходов с авторизацией, категориями и статистикой.

## Функционал

- Регистрация и авторизация (JWT, HttpOnly cookie)
- Управление счетами (CRUD)
- Управление категориями (расход / доход)
- Управление транзакциями (автообновление баланса)
- Поиск по описанию
- Фильтрация по категории и диапазону дат
- Статистика расходов и доходов по месяцам
- Профиль пользователя

## Стек технологий

- Python 3.11
- FastAPI
- SQLite
- Jinja2
- JWT (python-jose)
- Pydantic
- Uvicorn

## Структура проекта

```
Progect/
├── src/
│   ├── api_db.py
│   ├── database.py
│   ├── auth.py
│   └── schemas.py
├── templates/
├── database/
│   ├── finance.db
│   └── finance.sql
├── static/
├── requirements.txt
└── README.md
```

## Установка и запуск

1. Клонирование репозитория

git clone https://github.com/Quiten-404/Progect.git
cd Progect

2. Создание виртуального окружения

Windows:
python -m venv venv
venv\Scripts\activate

Linux / Mac / WSL:
python3 -m venv venv
source venv/bin/activate

3. Установка зависимостей

pip install -r requirements.txt

4. Инициализация базы данных

python -c "from src.database import init_database; init_database()"

5. Запуск сервера

python -m uvicorn src.api_db:app --reload

6. Открыть в браузере

http://127.0.0.1:8000/web/register

## Страницы приложения

- Регистрация: /web/register
- Вход: /web/login
- Счета: /web/accounts
- Транзакции: /web/transactions
- Категории: /web/categories
- Поиск: /web/transactions/search
- Статистика: /web/statistics
- Профиль: /web/profile

## API документация

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Автор

Глинкин Алексей Максимович
Группа БПИ2501
Москва, 2026
