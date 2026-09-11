from models import Account
from sqlalchemy.orm import Session

class TransactionRepository:
    def __init__(self, Session=Session):
        self.db = Session

    def update_balance(self, amount, user_id):
        result = self.db.query(Account).filter(Account.user_id == user_id).update(
            {Account.balance: Account.balance + amount},
            synchronize_session=False
        )
        self.db.commit()
        return result > 0
