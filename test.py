from requests import get, post, delete, put

response = post(
    "http://127.0.0.1:8080/api/news",
    json={
        "title": "Тест",
        "content": "Контент",
        "date": "2026-04-01",
        "user_id": 1
    }
)

put(
    "http://127.0.0.1:8080/api/news/1",
    json={
        "title": "Тест1",
        "content": "Контент1",
        "date": "2026-04-02",
        "user_id": 2
    })