def test_create_account(account_manager):
    status, msg = account_manager.create_account("ihsan", "M. Ihsan", "1234")

    assert status is True
    assert msg == "Account Successfully created."

def test_create_duplicate_account(account_manager):
    account_manager.create_account("ihsan", "M. Ihsan", "1234")
    status, msg = account_manager.create_account("ihsan", "M. Ihsan", "1234")

    assert status is False
    assert msg == "Account already exists."
