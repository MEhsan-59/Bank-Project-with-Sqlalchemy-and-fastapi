from models import Transaction
from sqlalchemy.orm import Session

class StatmentRepository:
    def __init__(self, db=Session):
        self.db = db

    def log_transaction(self, account_no, type_, amount, balance_after, related_account=None):
        transaction = Transaction(
            account_no=account_no,
            type=type_,
            amount=amount,
            balance_after=balance_after,
            related_account=related_account,
        )
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def get_history(self, account_no):
        return (
            self.db.query(Transaction)
            .filter(Transaction.account_no == account_no)
            .order_by(Transaction.id.desc())
            .all()
        )

    def get_top_5_history(self, account_no, limit=5):
        return self.get_history(account_no, limit=limit)
