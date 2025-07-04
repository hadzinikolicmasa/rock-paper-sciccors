def test_register_user_missing_username(client):
    response = client.post("/register", json={})
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Username required"

def test_register_user_duplicate(client):
    client.post("/register", json={"username": "testuser"})
    response = client.post("/register", json={"username": "testuser"})
    assert response.status_code == 409

def test_register_success(client):
    response = client.post("/register", json={"username": "masah"})
    data = response.get_json()
    assert response.status_code == 200
    assert data["message"] == "User registered"