from logger_setup import logger

class TransactionManager:
    def __init__(self, transaction_repo, account_repo, statement_repo):
        self.transaction_repo = transaction_repo
        self.account_repo = account_repo
        self.statement_repo = statement_repo

    def check_balance(self, user_id, password):
        account = self.account_repo.check_account_exists(user_id, password)

        if not account:
            logger.warning("Account does not exists.")
            return False, "Account does not exist.", None

        logger.info("Balance fetched successfully")
        return True, "Balance fetched successfully.", account.balance

    def deposit(self, account_no, balance, amount, user_id):
        if amount > 10000:
            logger.warning("amount must be less than Total Balance.")
            return False, "amount must be less than Total Balance.", None

        if amount <= 0:
            logger.warning("Amount must be grater than 0.")
            return False, "Amount must be grater than 0.", None

        self.transaction_repo.update_balance(amount, user_id)
        self.statement_repo.log_deposit(account_no, amount, balance + amount)
        logger.info(f"{amount} successfuly deposited Your total amount is {balance+amount}.")
        return True, f"{amount} successfuly deposited Your total amount is {balance+amount}.", balance + amount
