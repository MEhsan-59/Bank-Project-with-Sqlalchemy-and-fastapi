def test_login_and_get_profile(client):
    client.post("/create_account", json={
        "user_id": "ihsan",
        "user_name": "M. Ihsan",
        "password": "1234"
    })

    login_response = client.post("/login_account", json={
        "user_id": "ihsan",
        "password": "1234"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    profile_response = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert profile_response.status_code == 200
    body = profile_response.json()
    assert body["name"] == "M. Ihsan"
    assert body["account_no"] == "AC4000"

def test_login_wrong_password_returns_401(client):
    client.post("/create_account", json={
        "user_id": "ihsan",
        "user_name": "M. Ihsan",
        "password": "1234"
    })

    login_response = client.post("/login_account", json={
        "user_id": "ihsan",
        "password": "wrong"
    })
    assert login_response.status_code == 401

def test_profile_without_token_is_rejected(client):
    response = client.get("/me")
    assert response.status_code in (401, 403)
