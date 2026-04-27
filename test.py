import requests
import json

BASE_URL = "http://127.0.0.1:8080"

def print_response(title, response):
    """Вспомогательная функция для красивого вывода."""
    print(f"\n=== {title} ===")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response Body: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception:
        print(f"Response Text: {response.text}")

# ================= USERS =================

def test_get_users_list():
    """Получить список всех пользователей."""
    response = requests.get(f"{BASE_URL}/api/users")
    print_response("GET /api/users", response)
    assert response.status_code == 200

def test_get_single_user():
    """Получить конкретного пользователя."""
    response = requests.get(f"{BASE_URL}/api/users/1")
    print_response("GET /api/users/1", response)
    # Если пользователя нет, будет 404
    assert response.status_code in [200, 404]

def test_create_user():
    """Создать нового пользователя."""
    new_user = {
        "login": "testuser_req",
        "password": "password123",
        "email": "test_req@example.com"
    }
    response = requests.post(
        f"{BASE_URL}/api/users",
        json=new_user  # requests сам сделает dumps и выставит заголовки
    )
    print_response("POST /api/users", response)
    assert response.status_code in [201, 400]

# ================= NEWS =================

def test_get_news_list():
    """Получить список новостей."""
    response = requests.get(f"{BASE_URL}/api/news")
    print_response("GET /api/news", response)
    assert response.status_code == 200

def test_get_single_news():
    """Получить конкретную новость."""
    response = requests.get(f"{BASE_URL}/api/news/1")
    print_response("GET /api/news/1", response)
    assert response.status_code in [200, 404]

# ================= STORIES =================

def test_get_stories_list():
    """Получить список историй."""
    response = requests.get(f"{BASE_URL}/api/stories")
    print_response("GET /api/stories", response)
    assert response.status_code == 200

def test_get_single_story():
    """Получить конкретную историю."""
    response = requests.get(f"{BASE_URL}/api/stories/1")
    print_response("GET /api/stories/1", response)
    assert response.status_code in [200, 404]

def test_update_story():
    """Обновить историю."""
    updated_data = {"title": "Updated Title", "content": "Updated content"}
    response = requests.put(
        f"{BASE_URL}/api/stories/1",
        json=updated_data
    )
    print_response("PUT /api/stories/1", response)
    assert response.status_code in [200, 404, 405]

def test_delete_story():
    """Удалить историю."""
    response = requests.delete(f"{BASE_URL}/api/stories/1")
    print_response("DELETE /api/stories/1", response)
    assert response.status_code in [200, 404, 405]

# ================= FORM DATA (LOGIN) =================

def test_login_with_form_data():
    """Отправка логина через form-data."""
    # Чтобы отправить form-data, используем data= вместо json=
    form_data = {
        "email": "user@test.com",
        "password": "123456"
    }
    response = requests.post(f"{BASE_URL}/auth/login", data=form_data)
    print_response("POST /auth/login (form-data)", response)
    # 302 - это Redirect (после успешного логина)
    assert response.status_code in [200, 302, 401]

# ================= ЗАПУСК =================

if __name__ == '__main__':
    print("Начинаем тестирование API...")
    
    # Убедитесь, что main.py запущен (python main.py) перед запуском этого скрипта!
    
    try:
        test_get_users_list()
        test_get_single_user()
        test_create_user()
        
        test_get_news_list()
        test_get_single_news()
        
        test_get_stories_list()
        test_get_single_story()
        test_update_story()
        test_delete_story()
        
        test_login_with_form_data()
        
        print("\n✅ Все тесты пройдены успешно!")
        
    except AssertionError as e:
        print(f"\n❌ Тест упал: {e}")
    except requests.exceptions.ConnectionError:
        print("\n❌ Ошибка подключения! Убедитесь, что сервер запущен на 127.0.0.1:8080")