# Smart Design Тестовое задание

Для установки тестового виртуального окружения следующие команды:
```sh
virtualenv venv
venv/Scripts/activate
pip install -r requirements.txt
```

Для запуска Docker контейнера(база данных Mongodb) а так же сервера на Python следующие команды:
```sh
docker run -d -p 27017:27017 mongo
python shop__main__.py
```

## Тестовые сценарии:

Для создания товаров:
```sh
curl --header "Content-Type: application/json" --request POST --data '{"title": "iPhone", "description": "It lives a long time but is expensive", "display": 6.1}' http://localhost:8080/api/create_item
curl --header "Content-Type: application/json" --request POST --data '{"_id": 0, "title": "Xiaomi", "description": "lives a little, but cheaper", "display": 6.5}' http://localhost:8080/api/create_item
```

Ответ должен быть:
```json
{"статус": "выполнено"}
```

Получить список названий товаров
```sh
curl --header "Content-Type: application/json" --request POST http://localhost:8080/api/get_items_titles
```

Ответ должен быть:
```json
{"titles": ["iPhone", "Xiaomi"]}
```

Для получения списка товаров (без сортировки):
```sh
curl -X POST http://localhost:8080/api/get_items
```

Ответ должен быть (_id может отличаться):
```json
{"items": [{"_id": {"$oid": "5fbcc2b4d6c1afa7c348aa35"}, "title": "iPhone", "description": "It lives a long time but is expensive", "display": 6.1}, {"_id": 0, "title": "Xiaomi", "description": "lives a little, but cheaper", "display": 6.5}]}
```

Для получения списка товаров (сортировка по title):
```sh
curl --header "Content-Type: application/json" --request POST --data '{"sort": "title"}' http://localhost:8080/api/get_items
```

Ответ должен быть:
```json
{"items": [{"_id": {"$oid": "5fbcc2b4d6c1afa7c348aa35"}, "title": "iPhone", "description": "It lives a long time but is expensive", "display": 6.1}, {"_id": 0, "title": "Xiaomi", "description": "lives a little, but cheaper", "display": 6.5}]}
```

Для получения товара по _id:
```sh
curl --header "Content-Type: application/json" --request POST --data '{"_id": 0}' http://localhost:8080/api/get_item
```

Ответ должен быть:
```json
{"item": {"_id": 0, "title": "Xiaomi", "description": "lives a little, but cheaper", "display": 6.5}}
```

Получить список названий товаров (Фильтрация по полю description)
```sh
curl --header "Content-Type: application/json" --request POST --data '{"description": "It lives a long time but is expensive"}' http://localhost:8080/api/get_items_titles
```

Ответ должен быть:
```json
{"titles": ["iPhone"]}
```