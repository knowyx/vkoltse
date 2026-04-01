from requests import get, post, delete, put

post(
"http://127.0.0.1:8080/api/users",
    json={
        "permissions": "Лох",
        "email": "perdun322@gmail.com",
        "login": "2026-04-01",
        "password": "322"
    }
)