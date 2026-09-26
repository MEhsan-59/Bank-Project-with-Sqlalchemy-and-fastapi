import json
from models import Account
import security

class AdminRepository:
    def __init__(self, file_name: str, db=None):
        self.file_name = file_name
        self.db = db

    def load_admins(self) -> list[dict]:
        with open(self.file_name, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data.get("admins", [])

    def get_admin_by_username(self, username):
        admins = self.load_admins()
        return next((a for a in admins if a.get("username") == username), None)

    def username_exists(self, username):
        return self.get_admin_by_username(username) is not None

    def check_admin(self, admin_id: str, admin_password: str):
        admins = self.load_admins()
        for admin in admins:
            if admin.get("username") == admin_id:
                if security.SecurityHelper.verify_password(admin_password, admin.get("password")):
                    return admin
                return None
        return None

    def freeze_account(self, account_no: str):
        account = self.db.query(Account).filter(Account.account_no == account_no).first()
        if account:
            account.freeze = True
            self.db.commit()
            return True
        return False

    def check_is_frozen(self, account_id: str):
        account = self.db.query(Account).filter(Account.account_no == account_id).first()
        if account:
            return account.freeze
        return False