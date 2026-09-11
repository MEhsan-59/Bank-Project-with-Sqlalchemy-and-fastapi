from unittest.mock import MagicMock


def test_send_money_success(transaction_manager, account_repo):
    sender = account_repo.create_account("ihsan", "M. Ihsan", "1234")
    receiver = account_repo.create_account("jalal", "M. Jalal", "5678")
    account_repo.db.query(type(sender)).filter_by(account_no=sender.account_no).update({"balance": 1000})
    account_repo.db.commit()
    sender = account_repo.get_account_by_id("ihsan")

    status, msg = transaction_manager.send_money(sender, receiver.account_no, 300)

    assert status is True
    assert msg == "Money transferred successfully."

    updated_sender = account_repo.get_account_by_account_no(sender.account_no)
    updated_receiver = account_repo.get_account_by_account_no(receiver.account_no)
    assert updated_sender.balance == 700
    assert updated_receiver.balance == 300

def test_send_money_receiver_not_found(transaction_manager, account_repo):
    sender = account_repo.create_account("ihsan", "M. Ihsan", "1234")

    status, msg = transaction_manager.send_money(sender, "AC9999", 100)

    assert status is False
    assert msg == "Receiver account not found."

def test_send_money_cannot_send_to_self(transaction_manager, account_repo):
    sender = account_repo.create_account("ihsan", "M. Ihsan", "1234")

    status, msg = transaction_manager.send_money(sender, sender.account_no, 100)

    assert status is False
    assert msg == "You cannot send money to your own account."

def test_send_money_amount_must_be_positive(transaction_manager, account_repo):
    sender = account_repo.create_account("ihsan", "M. Ihsan", "1234")
    receiver = account_repo.create_account("jalal", "M. Jalal", "5678")

    status, msg = transaction_manager.send_money(sender, receiver.account_no, 0)

    assert status is False
    assert msg == "Amount must be greater than zero."

def test_send_money_insufficient_balance(transaction_manager, account_repo):
    sender = account_repo.create_account("ihsan", "M. Ihsan", "1234")
    receiver = account_repo.create_account("jalal", "M. Jalal", "5678")

    status, msg = transaction_manager.send_money(sender, receiver.account_no, 100)

    assert status is False
    assert msg == "Insufficient balance."
