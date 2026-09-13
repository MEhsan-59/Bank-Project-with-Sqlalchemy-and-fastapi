import json
from logger_setup import logger

class AdminManager:
    def __init__(self, admin_repo):
        self.admin_repo = admin_repo

    def check_admin(self, admin_id, admin_password):
        logger.info("Checking admin credentials.")
        if not admin_id.strip() or not admin_password.strip():
            logger.warning("Admin ID and password cannot be empty.")
            return False, "Admin ID and password cannot be empty."

        admin = self.admin_repo.check_admin(admin_id, admin_password)
        if admin:
            logger.info("Admin credentials are valid.")
            return True, "Admin authenticated successfully."
        else:
            logger.warning("Invalid admin ID or password.")
            return False, "Invalid admin ID or password."

    def freeze_account(self, account_id):
        logger.info("Freezing account with ID: %s", account_id)
        if not account_id.strip():
            logger.warning("Account ID cannot be empty.")
            return False, "Account ID cannot be empty."

        success = self.admin_repo.freeze_account(account_id)
        if success:
            logger.info("Account with ID %s has been frozen.", account_id)
            return True, "Account has been frozen successfully."
        else:
            logger.warning("No account found with ID: %s", account_id)
            return False, "No account found with the provided ID."