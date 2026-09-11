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

    def transfer_money(self, sender_no, receiver_no, amount):
        sender = self.db.query(Account).filter_by(account_no=sender_no).with_for_update().first()
        receiver = self.db.query(Account).filter_by(account_no=receiver_no).with_for_update().first()

        if sender and receiver:
            sender.balance -= amount
            receiver.balance += amount
            self.db.commit()
