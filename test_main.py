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

def _login_and_get_token(client, user_id="ihsan", password="1234"):
    client.post("/create_account", json={
        "user_id": user_id,
        "user_name": "M. Ihsan",
        "password": password
    })
    login_response = client.post("/login_account", json={
        "user_id": user_id,
        "password": password
    })
    return login_response.json()["access_token"]

def test_check_balance_endpoint(client):
    token = _login_and_get_token(client)

    response = client.get("/check_balance", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["balance"] == 0

def test_deposit_endpoint(client):
    token = _login_and_get_token(client)

    response = client.post(
        "/deposit",
        json={"amount": 500},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["balance"] == 500

def test_deposit_endpoint_rejects_too_large_amount(client):
    token = _login_and_get_token(client)

    response = client.post(
        "/deposit",
        json={"amount": 50000},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
