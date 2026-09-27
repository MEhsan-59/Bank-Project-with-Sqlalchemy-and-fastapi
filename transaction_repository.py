from models import Account, Pending_transfer
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

    def add_pendeing_transfer(self, transfer_id, sender_user_id, receiver_account_no, amount):
        transfer = Pending_transfer(transfer_id=transfer_id, sender_user_id=sender_user_id, receiver_account_no=receiver_account_no, amount=amount)
        self.db.add(transfer)
        self.db.commit()
        self.db.refresh(transfer)
        return transfer

    def view_pendeing_transfer(self, transfer_id):
        transfer = self.db.query(Pending_transfer).filter(Pending_transfer.transfer_id == transfer_id).first()
        return transfer

    def delete_pendeing_transfer(self, transfer_id):
        transfer = self.db.query(Pending_transfer).filter(Pending_transfer.transfer_id == transfer_id).first()
        if transfer:
            self.db.delete(transfer)
            self.db.commit()
            return True
        return False