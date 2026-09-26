def test_create_account(account_manager):
    status, msg = account_manager.create_account("ihsan", "M. Ihsan", "1234")

    assert status is True
    assert msg == "Account Successfully created."

def test_create_duplicate_account(account_manager):
    account_manager.create_account("ihsan", "M. Ihsan", "1234")
    status, msg = account_manager.create_account("ihsan", "M. Ihsan", "1234")

    assert status is False
    assert msg == "Account already exists."

def test_login_account_success(account_manager):
    account_manager.create_account("ihsan", "M. Ihsan", "1234")
    status, msg = account_manager.login_account("ihsan", "1234")

    assert status is True
    assert msg == "Account login successfully."

def test_login_account_wrong_password(account_manager):
    account_manager.create_account("ihsan", "M. Ihsan", "1234")
    status, msg = account_manager.login_account("ihsan", "wrong")

    assert status is False
    assert msg == "Account not exists."

def test_login_account_not_found(account_manager):
    status, msg = account_manager.login_account("ghost", "1234")

    assert status is False
    assert msg == "Account not exists."

def test_get_account_by_id_found(account_manager):
    account_manager.create_account("ihsan", "M. Ihsan", "1234")
    status, msg, account = account_manager.get_account_by_id("ihsan")

    assert status is True
    assert account.user_id == "ihsan"

def test_get_account_by_id_not_found(account_manager):
    status, msg, account = account_manager.get_account_by_id("ghost")

    assert status is False
    assert msg == "Invalid user id no account found."
    assert account is None

def test_change_password_success(account_manager):
    account_manager.create_account("ihsan", "M. Ihsan", "1234")
    _, _, account = account_manager.get_account_by_id("ihsan")

    status, msg = account_manager.change_password("ihsan", account.password, "1234", "5678", "5678")

    assert status is True
    assert msg == "Password successfully changed."

    login_status, _ = account_manager.login_account("ihsan", "5678")
    assert login_status is True

def test_change_password_wrong_old_password(account_manager):
    account_manager.create_account("ihsan", "M. Ihsan", "1234")
    _, _, account = account_manager.get_account_by_id("ihsan")

    status, msg = account_manager.change_password("ihsan", account.password, "wrong", "5678", "5678")

    assert status is False
    assert msg == "Old password does not match."

def test_change_password_mismatch_confirm(account_manager):
    account_manager.create_account("ihsan", "M. Ihsan", "1234")
    _, _, account = account_manager.get_account_by_id("ihsan")

    status, msg = account_manager.change_password("ihsan", account.password, "1234", "5678", "0000")

    assert status is False
    assert msg == "New password and confirm password do not match."
    
def test_create_duplicate_account_returns_409(client):
    body = {"user_id": "ihsan", "user_name": "M. Ihsan", "password": "1234"}
    client.post("/create_account", json=body)
    response = client.post("/create_account", json=body)
    assert response.status_code == 409