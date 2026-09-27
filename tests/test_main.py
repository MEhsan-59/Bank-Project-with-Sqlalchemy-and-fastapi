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

def test_send_money_preview_and_confirm(client):
    sender_token = _login_and_get_token(client, "ihsan", "1234")

    client.post("/create_account", json={
        "user_id": "jalal",
        "user_name": "M. Jalal",
        "password": "5678"
    })

    client.post(
        "/deposit",
        json={"amount": 1000},
        headers={"Authorization": f"Bearer {sender_token}"}
    )

    preview = client.post(
        "/send_money/preview",
        json={"receiver_account_no": "AC4001", "amount": 300},
        headers={"Authorization": f"Bearer {sender_token}"}
    )
    assert preview.status_code == 200
    transaction_id = preview.json()["transaction_id"]

    confirm = client.post(
        "/send_money/confirm",
        json={"transaction_id": transaction_id},
        headers={"Authorization": f"Bearer {sender_token}"}
    )
    assert confirm.status_code == 200
    assert confirm.json()["success"] is True

    balance_response = client.get("/check_balance", headers={"Authorization": f"Bearer {sender_token}"})
    assert balance_response.json()["balance"] == 700

def test_send_money_preview_insufficient_balance(client):
    sender_token = _login_and_get_token(client, "ihsan", "1234")
    client.post("/create_account", json={
        "user_id": "jalal",
        "user_name": "M. Jalal",
        "password": "5678"
    })

    preview = client.post(
        "/send_money/preview",
        json={"receiver_account_no": "AC4001", "amount": 300},
        headers={"Authorization": f"Bearer {sender_token}"}
    )
    assert preview.status_code == 400

def test_change_password_endpoint_and_relogin(client):
    token = _login_and_get_token(client, "ihsan", "1234")

    response = client.post(
        "/change_password",
        json={"old_password": "1234", "new_password": "5678", "confirm_password": "5678"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["success"] is True

    old_login = client.post("/login_account", json={"user_id": "ihsan", "password": "1234"})
    assert old_login.status_code == 401

    new_login = client.post("/login_account", json={"user_id": "ihsan", "password": "5678"})
    assert new_login.status_code == 200

def test_statements_reflect_deposit_and_transfer(client):
    sender_token = _login_and_get_token(client, "ihsan", "1234")
    client.post("/create_account", json={
        "user_id": "jalal",
        "user_name": "M. Jalal",
        "password": "5678"
    })

    client.post("/deposit", json={"amount": 1000}, headers={"Authorization": f"Bearer {sender_token}"})

    preview = client.post(
        "/send_money/preview",
        json={"receiver_account_no": "AC4001", "amount": 300},
        headers={"Authorization": f"Bearer {sender_token}"}
    )
    client.post(
        "/send_money/confirm",
        json={"transaction_id": preview.json()["transaction_id"]},
        headers={"Authorization": f"Bearer {sender_token}"}
    )

    statements = client.get("/statements", headers={"Authorization": f"Bearer {sender_token}"})
    assert statements.status_code == 200
    transactions = statements.json()["transactions"]
    types = {t["type"] for t in transactions}
    assert types == {"deposit", "transfer_out"}

def test_mini_statements_returns_at_most_five(client):
    token = _login_and_get_token(client)

    for _ in range(7):
        client.post("/deposit", json={"amount": 100}, headers={"Authorization": f"Bearer {token}"})

    response = client.get("/mini_statements", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()["transactions"]) == 5