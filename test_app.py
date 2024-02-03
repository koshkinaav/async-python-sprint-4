import requests


def test_ping():
    response = requests.get("http://localhost:8000/api/v1/ping")
    # Проверяем, что запрос успешно обработан...
    assert response.status_code == 200
    assert response.json() == {
        "status": "Database is accessible"
    }


def test_post_url():
    response = requests.post(
        "http://localhost:8000/api/v1/url?url=https://wiki.postgresql.org/wiki/Homebrew")
    # Проверяем, что запрос успешно обработан...
    assert response.status_code == 201
    assert response.json() == {
        "short_url": "http://localhost:8000/748eb096"
    }


def test_batch_urls():
    js = [
        "https://ru.wikipedia.org/wiki/Заглавная_страница",
        "https://ru.wikipedia.org/wiki/Ренданг_(блюдо)"
    ]
    response = requests.post('http://localhost:8000/api/v1/batch_urls', json=js)
    assert response.status_code == 201
    assert response.json() == {
        "short_urls": [
            "http://localhost:8000/4fe23092",
            "http://localhost:8000/8124e9c6"
        ]
    }
