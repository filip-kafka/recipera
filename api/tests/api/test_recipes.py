from fastapi.testclient import TestClient


def test_create_and_read_recipe(client: TestClient):
    create_response = client.post("/api/v1/recipes", json={"title": "Test recipe"})

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["title"] == "Test recipe"
    assert isinstance(created["id"], int)
    assert created["created_at"] is not None
    assert created["updated_at"] is not None

    recipe_id = created["id"]
    read_response = client.get(f"/api/v1/recipes/{recipe_id}")

    assert read_response.status_code == 200
    fetched = read_response.json()
    assert fetched["id"] == recipe_id
    assert fetched["title"] == "Test recipe"


def test_get_missing_recipe_returns_404(client: TestClient):
    response = client.get("/api/v1/recipes/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


def test_create_recipe_rejects_empty_title(client: TestClient):
    response = client.post("/api/v1/recipes", json={"title": ""})

    assert response.status_code == 422
