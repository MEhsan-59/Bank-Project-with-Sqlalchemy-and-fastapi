from logger_setup import logger

class AccountManager:

    def __init__(self, account_repo):
        self.account_repo = account_repo

    def create_account(self, user_id, user_name, password):

        if self.account_repo.check_account_exists(user_id, skip_password_check=True):
            logger.warning("Account already exists.")
            return False, "Account already exists."

        account = self.account_repo.create_account(
            user_id,
            user_name,
            password
        )

        if account:
            logger.info("Account Successfully created.")
            return True, "Account Successfully created."

        logger.warning("Account creation failed.")
        return False, "Account creation failed."
