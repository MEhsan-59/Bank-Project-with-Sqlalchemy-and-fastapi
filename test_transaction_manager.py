def test_check_balance_success(transaction_manager, account_repo):
    account_repo.create_account("ihsan", "M. Ihsan", "1234")

    status, msg, balance = transaction_manager.check_balance("ihsan", "1234")

    assert status is True
    assert msg == "Balance fetched successfully."
    assert balance == 0

def test_check_balance_account_not_found(transaction_manager):
    status, msg, balance = transaction_manager.check_balance("ghost", "1234")

    assert status is False
    assert msg == "Account does not exist."
    assert balance is None

def test_deposit_success(transaction_manager, account_repo):
    account = account_repo.create_account("ihsan", "M. Ihsan", "1234")

    status, msg, new_balance = transaction_manager.deposit(account.account_no, account.balance, 500, "ihsan")

    assert status is True
    assert new_balance == 500

def test_deposit_amount_too_large(transaction_manager, account_repo):
    account = account_repo.create_account("ihsan", "M. Ihsan", "1234")

    status, msg, new_balance = transaction_manager.deposit(account.account_no, account.balance, 20000, "ihsan")

    assert status is False
    assert msg == "amount must be less than Total Balance."
    assert new_balance is None

def test_deposit_amount_must_be_positive(transaction_manager, account_repo):
    account = account_repo.create_account("ihsan", "M. Ihsan", "1234")

    status, msg, new_balance = transaction_manager.deposit(account.account_no, account.balance, 0, "ihsan")

    assert status is False
    assert msg == "Amount must be grater than 0."
    assert new_balance is None

def test_deposit_updates_account_balance(transaction_manager, account_repo):
    account = account_repo.create_account("ihsan", "M. Ihsan", "1234")

    transaction_manager.deposit(account.account_no, account.balance, 500, "ihsan")

    updated = account_repo.get_account_by_id("ihsan")
    assert updated.balance == 500
