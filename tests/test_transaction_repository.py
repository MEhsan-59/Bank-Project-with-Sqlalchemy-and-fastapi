def test_update_balance_increases_amount(account_repo, transaction_repo):
    account = account_repo.create_account("ihsan", "M. Ihsan", "1234")

    result = transaction_repo.update_balance(500, "ihsan")

    updated_account = account_repo.get_account_by_id("ihsan")
    assert result is True
    assert updated_account.balance == 500

def test_update_balance_negative_amount_decreases(account_repo, transaction_repo):
    account = account_repo.create_account("ihsan", "M. Ihsan", "1234")
    account.balance = 1000
    account_repo.db.commit()

    result = transaction_repo.update_balance(-300, "ihsan")

    updated_account = account_repo.get_account_by_id("ihsan")
    assert result is True
    assert updated_account.balance == 700

def test_update_balance_nonexistent_user_returns_false(transaction_repo):
    result = transaction_repo.update_balance(500, "ghost")

    assert result is False
