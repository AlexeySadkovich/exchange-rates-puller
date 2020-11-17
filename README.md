# exchange-rates-puller
***Переменные окружения:***
```
MONGO_HOST
MONGO_PORT

MONGO_INITDB_DATABASE
MONGO_INITDB_ROOT_USERNAME
MONGO_INITDB_ROOT_PASSWORD
```
Расположить в файле .env в корне проекта

***Запуск:***
```
$ docker-compose up --build
```

***Адрес интерфейса:*** 
```
http://127.0.0.1
```

***Маршрутизация:***

```/``` - Интерфейс для получения и сохранения данных о курсах валют<br>
```/saved``` - Интерфейс для просмотра сохраненных<br>

***API:***

```/rates/get``` - Поучить курсы валют<br>
```/rates/save``` - Сохранить курсы валют в базу данных<br>
```/rates``` - Получить сохраненные курсы валют<br>
