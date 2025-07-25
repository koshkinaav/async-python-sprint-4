# Проектное задание четвёртого спринта

Спроектируйте и реализуйте сервис для создания сокращённой формы передаваемых URL и анализа активности их использования.

Кроме этого, выберите из списка дополнительные требования и тоже реализуйте их. У каждого задания есть определённая сложность, от которой зависит количество баллов. Вам необходимо выбрать такое количество заданий, чтобы общая сумма баллов была больше 4. Выбор заданий никак не ограничен: можно выбрать все простые или одно среднее и два простых, или одно продвинутое, или решить все.

## Описание задания

Реализовать `http`-сервис, который обрабатывает поступающие запросы. Сервер стартует по адресу `http://127.0.0.1:8080` (значение по умолчанию, можно изменять).

<details>
<summary> Список возможных эндпойнтов (можно изменять) </summary>

1. Получить сокращённый вариант переданного URL.

```python
POST /
```

Метод принимает в теле запроса строку URL для сокращения и возвращает ответ с кодом `201`.

2. Вернуть оригинальный URL.

```python
GET /<shorten-url-id>
```

Метод принимает в качестве параметра идентификатор сокращённого URL и возвращает ответ с кодом `307` и оригинальным URL в заголовке `Location`.

3. Вернуть статус использования URL.

```python
GET /<shorten-url-id>/status?[full-info]&[max-result=10]&[offset=0]
```

Метод принимает в качестве параметра идентификатор сокращённого URL и возвращает информацию о количестве переходов, совершенных по ссылке.

В ответе может содержаться как общее количество совершенных переходов, так и дополнительная детализированная информация о каждом переходе (наличие **query**-параметра **full-info** и параметров пагинации):
- дата и время перехода/использования ссылки;
- информация о клиенте, выполнившем запрос;

</details>


## Дополнительные требования (отметьте [Х] выбранные пункты):

- [x] (1 балл) Реализуйте метод `GET /ping`, который возвращает информацию о статусе доступности БД.
- [ ] (1 балл) Реализуйте возможность «удаления» сохранённого URL. Запись должна остаться, но помечаться как удалённая. При попытке получения полного URL возвращать ответ с кодом `410 Gone`.
- [x] (2 балла) Реализуйте middlware, блокирующий доступ к сервису из запрещённых подсетей (black list).
- [x] (2 балла) Реализуйте возможность передавать ссылки пачками (batch upload).

<details>
<summary> Описание изменений </summary>

- Метод `POST /shorten` принимает в теле запроса список URL в формате:

```python
[
    {
        "original-url": "<URL-for-shorten>"
    },
    ...
]

```
... и возвращает данные в следующем формате:

```python
[
    {
        "short-id": "<shoten-id>",
        "short-url": "http://...",
    },
    ...
]
```
</details>


- [ ] (3 балла) Реализуйте взаимодействие с сервисом авторизованного пользователя. Пользователь может создавать как приватные, так и публичные ссылки или изменять видимость ссылок. Вызов метода `GET /user/status` возвращает все созданные ранее ссылки в формате:

```
[
    {
        "short-id": "<text-id>",
        "short-url": "http://...",
        "original-url": "http://...",
        "type": "<public|private>"
    },
    ...
]
```

- [ ] **(5 баллов) Реализуйте кастомное взаимодействия с БД. Необходимо учесть возможность работы с транзакциями.


## Требования к решению

1. Используйте фреймворк FastAPI. В качестве СУБД используйте PostgreSQL (не ниже 10 версии).
2. Используйте концепции ООП.
3. Предусмотрите обработку исключительных ситуаций.
4. Приведите стиль кода в соответствие pep8, flake8, mypy.
5. Логируйте результаты действий.
6. Покройте написанный код тестами.

## Решение
Добавлены Response Model в base.py

В директории проекта выполните для создания БД

```bash
docker run -d \
    --name postgres \
    -e POSTGRES_DB=short_urls \
    -e POSTGRES_USER=alex \
    -e POSTGRES_PASSWORD=xxx \
    -p 5432:5432 \
    postgres:latest
```
Затем можно запустить сервер
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
**SWAGGER** доступен по следующему адресу:
http://0.0.0.0:8080/api/openapi

Реализованы следующие методы:
```python
GET /api/v1/ping - проверка доступности БД
POST /api/v1/url - получить сокращенную ссылку
POST /api/v1/batch_urls - получить сокращенные ссылки для списка ссылок
GET /api/v1/shorten-url-id - получить информацию об исходной ссылке по исходной
GET  api/v1/f7872e0f/status -- вернуть статус использования URL.
```
Если вы захотите полность очистить БД то, выполните
```bash
/bin/bash create_data_base.sh
```

