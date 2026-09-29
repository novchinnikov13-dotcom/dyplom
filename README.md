## Структура проекта

diplom_advance_new/
|- app/
|  |- api/ (users.py, tweets.py, medias.py)
|  |- tests/ (conftest.py, test_*.py)
  |- config.py, database.py, models.py, schemas.py, main.py
|- static/, templates/, media/
|- .env.example, requirements.txt, pytest.ini, README.md

## Быстрый старт

1. pip install -r requirements.txt
2. cp .env.example .env
3. uvicorn app.main:app --reload
4. pytest -v app/tests/

## API Endpoints

GET /api/users — список пользователей
GET /api/users/me?current_user_id=1 — профиль текущего
POST /api/users/{id}/follow?current_user_id=1 — подписаться
DELETE /api/users/{id}/follow?current_user_id=1 — отписаться

POST /api/tweets?current_user_id=1 — создать твит
GET /api/tweets?current_user_id=1 — лента
DELETE /api/tweets/{id}?current_user_id=1 — удалить твит
POST /api/tweets/{id}/likes?current_user_id=1 — лайк
DELETE /api/tweets/{id}/likes?current_user_id=1 — убрать лайк

POST /api/medias?current_user_id=1 — загрузить изображение