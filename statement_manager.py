# statement_manager.py

class Statement:
    def __init__(self, repo):
        self.repo = repo

    def log_deposit(self, account_no, amount, balance_after):
        self.repo.log_transaction(account_no, "deposit", amount, balance_after)

    def log_transfer(self, sender_account_no, receiver_account_no, amount,
                      sender_balance_after, receiver_balance_after):
        self.repo.log_transaction(sender_account_no, "transfer_out", amount,
                                   sender_balance_after, receiver_account_no)
        self.repo.log_transaction(receiver_account_no, "transfer_in", amount,
                                   receiver_balance_after, sender_account_no)

    def get_history(self, account_no):
        return self.repo.get_history(account_no)

    def get_top_5_history(self, account_no):
        return self.repo.get_top_5_history(account_no)
