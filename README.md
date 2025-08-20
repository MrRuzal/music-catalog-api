# music-catalog-api

## Описание проекта
music-catalog-api — это REST API, разработанное с использованием Django REST Framework, предназначенное для управления музыкальной коллекцией. API позволяет создавать, просматривать, обновлять и удалять информацию об артистах, альбомах и песнях. Проект включает в себя документацию Swagger для удобного изучения и тестирования API, а также поддержку запуска через Docker.

## Стек технологий
- Python 3.x
- Django
- Django REST Framework
- drf-yasg (Swagger документация)
- Docker и Docker Compose

## Установка и запуск

### Локально
1. Клонируйте репозиторий:
   ```
   git clone <URL_репозитория>
   cd music-catalog-api
   ```
2. Создайте и активируйте виртуальное окружение:
   ```
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Установите зависимости:
   ```
   uv install
   ```
4. Выполните миграции базы данных:
   ```
   cd backend
   python manage.py migrate
   ```
5. Запустите сервер:
   ```
   python manage.py runserver
   ```
6. API будет доступно по адресу: `http://127.0.0.1:8000/`

### Через Docker
1. Убедитесь, что Docker и Docker Compose установлены.
2. Запустите контейнеры:
   ```
   docker-compose up --build
   ```
3. API будет доступно по адресу: `http://127.0.0.1:8000/`

## Запуск тестов
Для запуска тестов используйте команду:
```
uv run python backend/manage.py test music.tests
```

## Документация API (Swagger UI)
Swagger UI доступен по адресу:
```
http://127.0.0.1:8000/swagger/
```
Здесь вы можете ознакомиться с полным описанием API, посмотреть модели данных и протестировать запросы.

## Примеры запросов

### Создание артиста (Artist)
```
POST /api/artists/
Content-Type: application/json

{
  "name": "The Beatles"
}
```

### Создание песни (Song)
```
POST /api/songs/
Content-Type: application/json

{
  "title": "Let It Be"
}
```

### Создание альбома (Album)
```
POST /api/albums/
Content-Type: application/json

{
  "title": "Abbey Road",
  "release_year": 1969,
  "artist": 1,
  "track_data": [
    {"track_number": 1, "song": 1},
    {"track_number": 2, "song": 2},
    {"track_number": 3, "song": 3}
  ]
}
```

## Итог:
```
Проект реализован в рамках тестового задания. Все основные требования выполнены: поддержка CRUD-операций для артистов, альбомов и песен, документация через Swagger, запуск с помощью Docker, а также модульные тесты.
```
