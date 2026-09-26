from logger_setup import logger

class TransactionManager:
    def __init__(self, transaction_repo, account_repo, statement_repo, admin_repo):
        self.transaction_repo = transaction_repo
        self.account_repo = account_repo
        self.statement_repo = statement_repo
        self.admin_repo = admin_repo

    def check_balance(self, user_id, password):
        account = self.account_repo.check_account_exists(user_id, password)

        if not account:
            logger.warning("Account does not exists.")
            return False, "Account does not exist.", None

        logger.info("Balance fetched successfully")
        return True, "Balance fetched successfully.", account.balance

    def deposit(self, account_no, balance, amount, user_id):
        if amount > 10000:
            logger.warning("amount must be less than 10000.")
            return False, "amount must be less than 10000.", None

        if amount <= 0:
            logger.warning("Amount must be greater than 0.")
            return False, "Amount must be greater than 0.", None

        self.transaction_repo.update_balance(amount, user_id)
        self.statement_repo.log_deposit(account_no, amount, balance + amount)
        logger.info(f"{amount} successfully deposited Your total amount is {balance+amount}.")
        return True, f"{amount} successfully deposited Your total amount is {balance+amount}.", balance + amount

    def send_money(self, current_user, receiver_account_no, amount):
        sender = self.account_repo.check_account_exists(current_user.user_id, current_user.password, True)
        receiver = self.account_repo.get_account_by_account_no(receiver_account_no)

        if not receiver:
            logger.warning("Receiver account not found.")
            return False, "Receiver account not found."

        if current_user.account_no == receiver_account_no:
            logger.warning("You cannot send money to your own account.")
            return False, "You cannot send money to your own account."

        if amount <= 0:
            logger.warning("Amount must be greater than zero.")
            return False, "Amount must be greater than zero."

        if sender.balance < amount:
            logger.warning("Insufficient balance.")
            return False, "Insufficient balance."

        sender_balance_after = sender.balance - amount
        receiver_balance_after = receiver.balance + amount

        self.transaction_repo.transfer_money(sender.account_no, receiver.account_no, amount)
        self.statement_repo.log_transfer(
            sender.account_no, receiver.account_no, amount,
            sender_balance_after, receiver_balance_after
        )

        logger.info("Money transfered successfully.")
        return True, "Money transferred successfully."
