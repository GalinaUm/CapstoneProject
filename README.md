# DRF Ads Marketplace API

REST API проект на базе Django REST Framework для размещения объявлений и отзывов с JWT-аутентификацией, системой ролей, фильтрацией, пагинацией и тестированием через pytest.

---

# Стек технологий

- Python 3.12
- Django
- Django REST Framework
- PostgreSQL
- JWT (SimpleJWT)
- Django Filter
- Pytest
- Pytest-Django
- DRF-YASG (Swagger)
- Docker / Docker Compose
- Poetry
- Black
- Flake8
- Isort

---

# Возможности проекта

## Пользователи

- Регистрация
- JWT авторизация
- Обновление профиля
- Просмотр своего профиля
- Смена пароля
- Восстановление пароля через email
- Роли:
  - user
  - admin

## Объявления

- Создание объявлений
- Просмотр списка объявлений
- Детальная информация
- Редактирование своих объявлений
- Удаление своих объявлений
- Фильтрация
- Пагинация

## Отзывы

- Создание отзывов
- Просмотр отзывов
- Ограничение:
  - один пользователь может оставить только один отзыв на объявление
- Рейтинг от 1 до 5

---

# Структура проекта

```text
project/
├── ads/
├── config/
├── htmlcov/
├── media/
├── tests/
├── users/
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── poetry.lock
├── pyproject.toml
├── pytest.ini
└── README.md
```

---

# Установка проекта

## Клонирование

```bash
git clone <repo_url>
cd project
```

---

# Установка через Poetry

## Установка зависимостей

```bash
poetry install
```

## Активация окружения

```bash
poetry shell
```

---

# ENV настройки

Создать файл `.env`

```env
DEBUG=

SECRET_KEY=your_secret_key

NAME=
USER=
PASSWORD=
HOST=
PORT=
```

---

# Docker запуск

## Сборка контейнеров

```bash
docker compose build
```

## Запуск

```bash
docker compose up
```

---

# Миграции

```bash
python manage.py migrate
```

---

# Создание суперпользователя

```bash
python manage.py createsuperuser
```

---

# Запуск проекта

```bash
python manage.py runserver
```

API будет доступен:

```text
http://127.0.0.1:8000/
```

---

# Swagger документация

## Swagger UI

```text
http://127.0.0.1:8000/swagger/
```

## ReDoc

```text
http://127.0.0.1:8000/redoc/
```

---

# JWT авторизация

## Получение токена

POST:

```text
/users/login/
```

Пример:

```json
{
  "email": "user@test.com",
  "password": "password"
}
```

Ответ:

```json
{
  "refresh": "token",
  "access": "token"
}
```

---

# API endpoints

## Users

| Метод | Endpoint | Описание |
|---|---|---|
| POST | `/users/create/` | Регистрация |
| POST | `/users/login/` | Авторизация |
| GET/PATCH | `/users/me/` | Профиль |
| GET | `/users/list/` | Список пользователей |
| GET | `/users/<id>/` | Детальный пользователь |
| PATCH | `/users/update/<id>/` | Обновление |
| DELETE | `/users/delete/<id>/` | Удаление |

---

## Ads

| Метод | Endpoint | Описание |
|---|---|---|
| GET | `/ads/` | Список объявлений |
| POST | `/ads/` | Создание объявления |
| GET | `/ads/<id>/` | Детальное объявление |
| PATCH | `/ads/<id>/` | Обновление |
| DELETE | `/ads/<id>/` | Удаление |

---

## Reviews

| Метод | Endpoint | Описание |
|---|---|---|
| GET | `/ads/<ad_id>/reviews/` | Список отзывов |
| POST | `/ads/<ad_id>/reviews/` | Создание отзыва |
| GET | `/ads/<ad_id>/reviews/<id>/` | Детальный отзыв |
| PATCH | `/ads/<ad_id>/reviews/<id>/` | Обновление |
| DELETE | `/ads/<ad_id>/reviews/<id>/` | Удаление |

---

# Фильтрация объявлений

Поддерживаются параметры:

| Параметр | Описание |
|---|---|
| title | Поиск по заголовку |
| description | Поиск по описанию |
| min_price | Минимальная цена |
| max_price | Максимальная цена |
| author | Email автора |

Пример:

```text
/ads/?min_price=1000&max_price=5000
```

---

# Пагинация

```python
page_size = 4
max_page_size = 10
```

Пример:

```text
/ads/?page=2&page_size=4
```

---

# Тестирование

## Установка dev-зависимостей

```bash
poetry add --group dev pytest pytest-django pytest-cov pytest-mock flake8 black isort coverage
```

---

# Запуск тестов

```bash
pytest -v
```

---

# Coverage

```bash
pytest --cov=ads --cov=users --cov-report=term-missing --cov-report=html
```

HTML отчет:

```text
htmlcov/index.html
```

---

# Линтеры

## Black

```bash
poetry run black .
```

## Isort

```bash
poetry run isort .
```

## Flake8

```bash
poetry run flake8 .
```

---

# Настройка Black

```toml
[tool.black]
line-length = 88
target-version = ['py312']

[tool.isort]
profile = "black"
```

---

# Структура тестов

```text
tests/
├── conftest.py
├── test_users_auth.py
├── test_users_permissions.py
├── test_ads.py
└── test_reviews.py
```

---

# Полезные команды

## Создание миграций

```bash
python manage.py makemigrations
```

## Применение миграций

```bash
python manage.py migrate
```

## Shell

```bash
python manage.py shell
```

## Сборка Docker

```bash
docker compose build
```

## Остановка контейнеров

```bash
docker compose down
```

---

# Galina Umerzakova

Учебный проект на Django REST Framework.