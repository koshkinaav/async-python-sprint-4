import requests
import unittest


class TestApp(unittest.TestCase):
    def test_ping(self) -> None:
        response = requests.get("http://0.0.0.0:8000/api/v1/ping")
        # Проверяем, что запрос успешно обработан...
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "status": "Database is accessible"
        })

    def test_post_url(self) -> None:
        response = requests.post(
            "http://localhost:8000/api/v1/url?url=https://wiki.postgresql.org/wiki/Homebrew")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            "short_url": "http://localhost:8000/748eb096"
        })

    def test_batch_urls(self) -> None:
        js = [
            "https://ru.wikipedia.org/wiki/Заглавная_страница",
            "https://ru.wikipedia.org/wiki/Ренданг_(блюдо)"
        ]
        response = requests.post('http://localhost:8000/api/v1/batch_urls', json=js)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            "short_urls": [
                "http://localhost:8000/4fe23092",
                "http://localhost:8000/8124e9c6"
            ]
        }
                         )
