1. Клонирование репозитория

```bash
git clone [https://github.com/novchinnikov13-dotcom/dyplom.git](https://github.com/novchinnikov13-dotcom/dyplom.git)
cd diplom_advance
```

2. Создание виртуального окружения


```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Установка зависимостей

```bash
pip install -r requirements.txt
```

4. Настройка PostgreSQL



1. Убедитесь, что служба PostgreSQL запущена:

Должно показать `Running`.

2. Создайте базу данных и пользователя:

Откройте **SQL Shell (psql)** и выполните:

```sql
CREATE DATABASE microblog;
CREATE USER microblog WITH PASSWORD 'microblog';
GRANT ALL PRIVILEGES ON DATABASE microblog TO microblog;
```



5. Настройка окружения

Скопируйте пример файла настроек:

```bash
cp .env.example .env
```

Отредактируйте `.env` при необходимости:

```env
DATABASE_URL=postgresql://microblog:microblog@localhost:5432/microblog
MEDIA_ROOT=media
```



6. Запуск сервера

```bash
uvicorn app.main:app --reload
```

Сервер запустится на `http://127.0.0.1:8000`

- **Swagger UI (документация API):** http://127.0.0.1:8000/docs
- **Главная страница:** http://127.0.0.1:8000/

7. Запуск тестов

```bash
pytest -v app/tests/
```


##  Зависимости

- **FastAPI 0.115.0** — веб-фреймворк
- **SQLAlchemy 2.0.35** — ORM
- **Psycopg2** — драйвер PostgreSQL
- **Pydantic 2.9.2** — валидация данных
- **pytest 9.1.1** — тестирование
- **uvicorn 0.30.6** — ASGI-сервер

Полный список в `requirements.txt`




