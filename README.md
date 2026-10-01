
Backend для корпоративного микроблога.

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone <repo-url>
cd microblog
```

### 2. Запуск через Docker Compose

```bash
docker compose up --build
```

Приложение доступно на http://localhost:8000

## API ключи

При инициализации создаются пользователи:

| Пользователь | API ключ |
|--------------|----------|
| test         | test     |
| alice        | alice    |
| bob          | bob      |
| carol        | carol    |

**Пользователь `test` подписан на alice, bob, carol** — лента не будет пустой.

## Примеры запросов

### Получить ленту твитов

```bash
curl -H "api-key: test" http://localhost:8000/api/tweets
```

### Получить профиль текущего пользователя

```bash
curl -H "api-key: test" http://localhost:8000/api/users/me
```

### Подписаться на пользователя

```bash
curl -X POST \
  -H "api-key: test" \
  http://localhost:8000/api/users/2/follow
```



### Загрузить медиа

```bash
curl -X POST \
  -H "api-key: test" \
  -F "file=@image.jpg" \
  http://localhost:8000/api/medias/upload
```

## Тесты

```bash
docker compose exec app pytest -v
```




## Структура проекта
microblog/
├── app/
│ ├── api/
│ │ ├── tweets.py
│ │ ├── users.py
│ │ └── medias.py
│ ├── database.py
│ ├── models.py
│ ├── schemas.py
│ └── main.py
├── create.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md

text

## Ответы API

### Успешный ответ

```json
{
  "result": true
}
```

### Ответ с ошибкой

```json
{
  "result": false,
  "error_type": "not_found",
  "error_message": "User not found"
}
```

### Возможные error_type

- `unauthorized` — неверный API ключ
- `not_found` — пользователь или твит не найден
- `forbidden` — нет прав на операцию
- `bad_request` — некорректный запрос

