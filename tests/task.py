from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_endpoints():
    """Тест всех эндпоинты."""

    print("Тестирую /health.")
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("/health работает.")

    print("Тестирую /docs.")
    response = client.get("/docs")
    assert response.status_code == 200
    print("/docs работает.")

    print("Тестирую /api/v1/tasks (POST).")
    payload = {
        "title": "Тестовая задача.", "description": "Тестовое описание."
    }
    response = client.post("/api/v1/tasks", json=payload)
    assert response.status_code == 201
    task_data = response.json()
    assert "id" in task_data
    print("POST /api/v1/tasks работает.")

    print("Тестирую /api/v1/tasks/{id} (GET).")
    response = client.get(f"/api/v1/tasks/{task_data['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Тестовая задача."
    print("GET /api/v1/tasks/{id} работает.")

    print("Тестирую /api/v1/tasks (GET list).")
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
    print("GET /api/v1/tasks работает.")

    print("Тестирую /api/v1/tasks/{id} (PATCH).")
    update_payload = {"title": "Обновленная задача."}
    response = client.patch(
        f"/api/v1/tasks/{task_data['id']}", json=update_payload
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Обновленная задача."
    print("PATCH /api/v1/tasks/{id} работает.")

    print("Тестирую /api/v1/tasks/{id} (DELETE).")
    response = client.delete(f"/api/v1/tasks/{task_data['id']}")
    assert response.status_code == 204
    print("DELETE /api/v1/tasks/{id} работает.")

    print("Тестирую получение несуществующей задачи.")
    response = client.get("/api/v1/tasks/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    print("404 для несуществующей задачи работает.")

    print("Все эндпоинты отвечают на тесты.")
