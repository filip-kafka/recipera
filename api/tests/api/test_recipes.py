from fastapi.testclient import TestClient


def test_create_and_read_recipe(client: TestClient):
    create_response = client.post(
        "/api/v1/recipes",
        json={
            "title": "Test recipe",
            "description": "Test recipe description",
            "servings": 4,
            "prep_time_min": 30,
            "cook_time_min": 90,
            "source": "example.test",
        },
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["title"] == "Test recipe"
    assert created["description"] == "Test recipe description"
    assert created["servings"] == 4
    assert created["prep_time_min"] == 30
    assert created["cook_time_min"] == 90
    assert created["source"] == "example.test"
    assert isinstance(created["id"], int)
    assert created["created_at"] is not None
    assert created["updated_at"] is not None

    recipe_id = created["id"]
    read_response = client.get(f"/api/v1/recipes/{recipe_id}")

    assert read_response.status_code == 200
    fetched = read_response.json()
    assert fetched["id"] == recipe_id
    assert fetched["title"] == "Test recipe"
    assert fetched["description"] == "Test recipe description"
    assert fetched["servings"] == 4
    assert fetched["prep_time_min"] == 30
    assert fetched["cook_time_min"] == 90
    assert fetched["source"] == "example.test"
    assert fetched["slug"] == "test-recipe"


def test_colliding_slugs_are_suffixed(client: TestClient):
    create_response = client.post(
        "/api/v1/recipes",
        json={
            "title": "Test recipe",
        },
    )
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["slug"] == "test-recipe"

    create_response = client.post(
        "/api/v1/recipes",
        json={
            "title": "Test recipe",
        },
    )
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["slug"] == "test-recipe-2"

    create_response = client.post(
        "/api/v1/recipes",
        json={
            "title": "Test recipe",
        },
    )
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["slug"] == "test-recipe-3"


def test_slug_transliteration(client: TestClient):
    create_response = client.post(
        "/api/v1/recipes",
        json={
            "title": "Smørrebrød",
        },
    )
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["slug"] == "smorrebrod"

    create_response = client.post(
        "/api/v1/recipes",
        json={
            "title": "dědečkovy knedlíčky",
        },
    )
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["slug"] == "dedeckovy-knedlicky"


def test_get_missing_recipe_returns_404(client: TestClient):
    response = client.get("/api/v1/recipes/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


def test_create_recipe_rejects_empty_title(client: TestClient):
    response = client.post("/api/v1/recipes", json={"title": ""})

    assert response.status_code == 422
