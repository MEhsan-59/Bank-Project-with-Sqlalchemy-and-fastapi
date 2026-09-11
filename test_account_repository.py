def test_create_account_creates_and_returns_account(account_repo):
    account = account_repo.create_account("ihsan", "M. Ihsan", "1234")

    assert account.user_id == "ihsan"
    assert account.user_name == "M. Ihsan"
    assert account.account_no == "AC4000"
    assert account.password != "1234"

def test_generate_account_number_increments(account_repo):
    first = account_repo.create_account("ihsan", "M. Ihsan", "1234")
    second = account_repo.create_account("jalal", "M. Jalal", "5678")

    assert first.account_no == "AC4000"
    assert second.account_no == "AC4001"

def test_check_account_exists_true_after_creating(account_repo):
    account_repo.create_account("ihsan", "M. Ihsan", "1234")

    assert account_repo.check_account_exists("ihsan", skip_password_check=True) is not None

def test_check_account_exists_false_when_not_present(account_repo):
    assert account_repo.check_account_exists("ghost", skip_password_check=True) is None

def test_check_account_exists_with_correct_password(account_repo):
    account_repo.create_account("ihsan", "M. Ihsan", "1234")

    assert account_repo.check_account_exists("ihsan", "1234") is not None

def test_check_account_exists_with_wrong_password(account_repo):
    account_repo.create_account("ihsan", "M. Ihsan", "1234")

    assert account_repo.check_account_exists("ihsan", "wrong") is None
