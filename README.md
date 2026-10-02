
Backend для корпоративного микроблога.

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone <repo-url>
cd microblog
```

##  Запуск через Docker Compose


### Шаг 2: Запуск контейнеров

В терминале перейдите в папку проекта и выполните:

```bash
# Запускаем контейнеры (сборка + старт)
docker compose up --build
```


### Шаг 3: Проверка работы

Откройте браузер и перейдите на:

- **Главная страница**: http://127.0.0.1:8000
- **Swagger UI (документация API)**: http://127.0.0.1:8000/docs

Или проверьте через терминал:

```bash
# Проверяем, что сервер отвечает
curl -H "api-key: test" http://127.0.0.1:8000/api/users/me
```

**Ожидаемый ответ:**
```json
{
  "result": true,
  "user": {
    "id": 1,
    "name": "test",
    "followers": [],
    "following": [
      {"id": 2, "name": "alice"},
      {"id": 3, "name": "bob"},
      {"id": 4, "name": "carol"}
    ]
  }
}
```

---

## 🔑 API ключи

При инициализации создаются 4 пользователя:

| Пользователь | API ключ | Описание |
|--------------|----------|----------|
| test         | test     | Основной пользователь (подписан на всех) |
| alice        | alice    | Тестовый пользователь 1 |
| bob          | bob      | Тестовый пользователь 2 |
| carol        | carol    | Тестовый пользователь 3 |

**Подписки:**
- `test` подписан на `alice`, `bob`, `carol`
- Лента `test` будет содержать твиты от всех троих

---

## 📡 Примеры запросов

### Получить профиль текущего пользователя

```bash
curl -H "api-key: test" http://127.0.0.1:8000/api/users/me
```

### Получить ленту твитов

```bash
curl -H "api-key: test" http://127.0.0.1:8000/api/tweets
```

**Ответ с картинками:**
```json
{
  "result": true,
  "tweets": [
    {
      "id": 1,
      "content": "Твит с картинкой",
      "attachments": ["/media/abc123.jpg"],
      "author": {"id": 2, "name": "alice"},
      "likes": []
    }
  ]
}
```

### Подписаться на пользователя

```bash
# Подписаться на bob (ID=3)
curl -X POST -H "api-key: alice" http://127.0.0.1:8000/api/users/3/follow
```

### Создать твит

```bash
curl -X POST \
  -H "api-key: test" \
  -H "Content-Type: application/json" \
  -d '{"tweet_data": "Мой первый твит!"}' \
  http://127.0.0.1:8000/api/tweets
```

---

##  Загрузка медиа

### POST /api/medias/upload

Загружает картинку и возвращает её ID.

**Пример:**

```bash
curl -X POST \
  -H "api-key: test" \
  -F "file=@photo.jpg" \
  http://127.0.0.1:8000/api/medias/upload
```

**Ответ:**
```json
{
  "result": true,
  "media_id": 1
}
```


---

##  Доступ к файлам

### GET /media/{filename}

Отдаёт загруженный файл по имени.

**Пример:**

```bash
# Файл доступен по URL /media/{filename}
curl http://127.0.0.1:8000/media/abc123.jpg
```

**В браузере:**
http://127.0.0.1:8000/media/abc123.jpg

text

**В ленте твитов:**
```json
{
  "attachments": ["/media/abc123.jpg"]
}
```

**Использование в HTML:**
```html
<img src="http://127.0.0.1:8000/media/abc123.jpg" alt="Картинка" />
```

---


