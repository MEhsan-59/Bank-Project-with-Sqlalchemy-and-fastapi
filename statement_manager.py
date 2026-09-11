# statement_manager.py

class Statement:
    def __init__(self, repo):
        self.repo = repo

    def log_deposit(self, account_no, amount, balance_after):
        self.repo.log_transaction(account_no, "deposit", amount, balance_after)
