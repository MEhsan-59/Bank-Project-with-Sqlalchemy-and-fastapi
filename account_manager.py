from logger_setup import logger
import security

class AccountManager:

    def __init__(self, account_repo, admin_repo):
        self.account_repo = account_repo
        self.admin_repo = admin_repo

    def create_account(self, user_id, user_name, password):

        if self.account_repo.check_account_exists(user_id, skip_password_check=True):
            logger.warning("Account already exists.")
            return False, "Account already exists."

        if self.admin_repo.username_exists(user_id):
            logger.warning("This user_id is reserved for admin.")
            return False, "This user_id is not allowed."

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

    def login_account(self, user_id, password):
        account = self.account_repo.check_account_exists(user_id, password)
        if not account:
            logger.warning("Account not exists.")
            return False, "Account not exists."
        admin = self.admin_repo.check_admin(user_id, password)
        if admin:
            logger.warning("Admin login successfully.")
            return True, "Admin login successfully."
                
        logger.info("Account login successfully.")
        return True, "Account login successfully."

    def get_account_by_id(self, user_id):
        account = self.account_repo.get_account_by_id(user_id)
        if not account:
            logger.warning("Invalid user id no account found.")
            return False, "Invalid user id no account found.", account
        return True, "Account found.", account

    def change_password(self, user_id, current_hashed_password, old_pass, new_pass, confirm_pass):
        if not security.SecurityHelper.verify_password(old_pass, current_hashed_password):
            logger.warning("Old password does not match.")
            return False, "Old password does not match."
        if new_pass != confirm_pass:
            logger.warning("New password and confirm password do not match.")
            return False, "New password and confirm password do not match."
        hashed_new = security.SecurityHelper.hash_password(new_pass)
        self.account_repo.update_password(user_id, hashed_new)
        logger.info("Password successfully changed for user: %s", user_id)
        return True, "Password successfully changed."
