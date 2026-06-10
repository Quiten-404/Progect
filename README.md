# 💰 Учёт личных финансов

Веб-приложение для учёта доходов и расходов с авторизацией, категориями и статистикой.

## 🚀 Функционал

- Регистрация и авторизация (JWT, HttpOnly cookie)
- Управление счетами (CRUD)
- Управление категориями (расход / доход)
- Управление транзакциями (автообновление баланса)
- Поиск по описанию
- Фильтрация по категории и диапазону дат
- Статистика расходов и доходов по месяцам
- Профиль пользователя

## 🛠️ Стек технологий

- Python 3.11
- FastAPI — веб-фреймворк
- SQLite — база данных
- Jinja2 — шаблонизатор
- JWT (python-jose) — авторизация
- Pydantic — валидация
- Uvicorn — ASGI сервер

## 📁 Структура проекта
Progect/
├── src/
│ ├── api_db.py # FastAPI приложение (эндпоинты)
│ ├── database.py # Работа с SQLite
│ ├── auth.py # JWT, хеширование паролей
│ └── schemas.py # Pydantic модели
├── templates/ # HTML шаблоны (Jinja2)
├── database/
│ ├── finance.db # Файл базы данных
│ └── finance.sql # SQL схема
├── static/ # Статические файлы (CSS, иконки)
├── requirements.txt
└── README.md

text

## 🚀 Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/ваш-аккаунт/название-репозитория.git
cd Progect
2. Создание виртуального окружения
Windows:

bash
python -m venv venv
venv\Scripts\activate
Linux / Mac / WSL:

bash
python3 -m venv venv
source venv/bin/activate
3. Установка зависимостей
bash
pip install -r requirements.txt
4. Инициализация базы данных
bash
python -c "from src.database import init_database; init_database()"
5. Запуск сервера
bash
python -m uvicorn src.api_db:app --reload
6. Открыть в браузере
text
http://127.0.0.1:8000/web/register
📱 Страницы приложения
Страница	URL
Регистрация	/web/register
Вход	/web/login
Счета	/web/accounts
Транзакции	/web/transactions
Категории	/web/categories
Поиск	/web/transactions/search
Статистика	/web/statistics
Профиль	/web/profile
📊 API документация
После запуска сервера доступна автоматическая документация:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

👤 Автор
Глинкин Алексей Максимович
Группа БПИ2501
Москва, 2026

📅 Дата сдачи
11.06.2026
