def test_get_history_returns_logged_deposits(statement_manager, statement_repo):
    statement_repo.log_transaction("AC4000", "deposit", 500, 500)
    statement_repo.log_transaction("AC4000", "deposit", 200, 700)

    history = statement_manager.get_history("AC4000")

    assert len(history) == 2
    assert history[0].amount == 200  # most recent first

def test_get_history_only_returns_matching_account(statement_manager, statement_repo):
    statement_repo.log_transaction("AC4000", "deposit", 500, 500)
    statement_repo.log_transaction("AC4001", "deposit", 300, 300)

    history = statement_manager.get_history("AC4000")

    assert len(history) == 1
    assert history[0].account_no == "AC4000"

def test_get_top_5_history_limits_results(statement_manager, statement_repo):
    for i in range(7):
        statement_repo.log_transaction("AC4000", "deposit", 100, 100 * (i + 1))

    history = statement_manager.get_top_5_history("AC4000")

    assert len(history) == 5
