import os
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import uuid
from logger_setup import logger
from schema import (
    CreateAccountResponse, CreateAccountSchema,
    LoginAccountSchema, TokenResponse, ProfileResponse,
    CheckBalanceResponse, DepositSchema, DepositResponse,
    SendMoneySchema, SendMoneyPreviewResponse, ConfirmTransferSchema,
    Change_password_Schema, ChangePasswordResponse,
    TransactionItem, StatementResponse
)
from account_manager import AccountManager
from account_repository import AccountRepository
from database import get_db
from auth import decode_access_token, create_access_token
from transaction_manager import TransactionManager
from transaction_repository import TransactionRepository
from statement_manager import Statement
from statement_repository import StatementRepository
from admin_manager import AdminManager
from admin_repository import AdminRepository
app = FastAPI(title="Bank Manager API", version="6.0")
security_scheme = HTTPBearer()
pending_transfers = {}

BASE_DIR = Path(__file__).resolve().parent
ADMIN_FILE_NAME = os.getenv("ADMIN_FILE_NAME", "admin.json")
ADMIN_FILE_PATH = str(BASE_DIR / ADMIN_FILE_NAME)


admin = False

def get_admin_manager(db: Session = Depends(get_db)) -> AdminManager:
    repo = AdminRepository(ADMIN_FILE_PATH, db)
    return AdminManager(repo)


def get_account_manager(db: Session = Depends(get_db)) -> AccountManager:
    repo = AccountRepository(db)
    admin_repo = AdminRepository(ADMIN_FILE_PATH)
    return AccountManager(repo, admin_repo)


def get_statement_manager(db: Session = Depends(get_db)) -> Statement:
    repo = StatementRepository(db)
    return Statement(repo)


def get_transaction_manager(db: Session = Depends(get_db)) -> TransactionManager:
    transaction_repo = TransactionRepository(db)
    account_repo = AccountRepository(db)
    return TransactionManager(transaction_repo, account_repo, get_statement_manager(db), get_admin_manager(db).admin_repo)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    manager: AccountManager = Depends(get_account_manager)):
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None or payload.get("role") != "user":
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    account = manager.account_repo.get_account_by_id(payload.get("sub"))

    if account is None:
        raise HTTPException(status_code=401, detail="User not found")

    return account


def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
):
    payload = decode_access_token(credentials.credentials)
    if payload is None or payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return payload

@app.post("/create_account", response_model=CreateAccountResponse)
def create_account(data: CreateAccountSchema, manager: AccountManager = Depends(get_account_manager)):
    logger.info("API : Create account.")
    status, msg = manager.create_account(data.user_id, data.user_name, data.password)

    if not status:
        logger.warning(msg)
        if msg == "Account already exists.":
            raise HTTPException(status_code=409, detail=msg)
        raise HTTPException(status_code=400, detail=msg)

    return CreateAccountResponse(status=True, message=msg)

@app.post("/login_account", response_model=TokenResponse)
def login_account(
    data: LoginAccountSchema,
    manager: AccountManager = Depends(get_account_manager),
    admin_manager: AdminManager = Depends(get_admin_manager),
):
    logger.info("API : Login Account.")
    admin, _ = admin_manager.check_admin(data.user_id, data.password)

    if admin:
        admin_record = admin_manager.admin_repo.get_admin_by_username(data.user_id)
        token = create_access_token(
            data.user_id,
            role="admin",
            extra_claims={"permissions": admin_record["permissions"]}
        )
        return {"access_token": token, "token_type": "bearer"}

    status, msg = manager.login_account(data.user_id, data.password)
    if not status:
        logger.warning(msg)
        raise HTTPException(status_code=401, detail=msg)

    token = create_access_token(data.user_id, role="user")
    return {"access_token": token, "token_type": "bearer"}


@app.get("/me", response_model=ProfileResponse)
def get_profile(current_user=Depends(get_current_user)):
    return {
        "message": f"Welcome, {current_user.user_name}!",
        "account_no": current_user.account_no,
        "name": current_user.user_name,
        "balance": current_user.balance
    }


@app.get("/check_balance", response_model=CheckBalanceResponse)
def check_balance(
    current_user=Depends(get_current_user)):
    logger.info("API : Check Balance.")
    return {"success": True, "balance": current_user.balance}


@app.post("/deposit", response_model=DepositResponse)
def deposit(
    data: DepositSchema,
    current_user=Depends(get_current_user),
    transaction_manager: TransactionManager = Depends(get_transaction_manager)
):
    logger.info("API : Deposit")
    status, message, new_balance = transaction_manager.deposit(current_user.account_no, current_user.balance, data.amount, current_user.user_id)

    if not status:
        logger.warning(message)
        raise HTTPException(status_code=400, detail=message)

    return {"success": status, "message": message, "balance": new_balance}


@app.post("/send_money/preview", response_model=SendMoneyPreviewResponse)
def send_money_preview(
    data: SendMoneySchema,
    current_user=Depends(get_current_user),
    manager: AccountManager = Depends(get_account_manager),
    admin_manager: AdminManager = Depends(get_admin_manager)
):
    logger.info("API : Send Money Preview")
    if admin_manager.admin_repo.check_is_frozen(current_user.account_no):
        logger.warning("Your account is frozen. Please contact the admin.")
        raise HTTPException(status_code=403, detail="Your account is frozen. Please contact the admin.")
    receiver = manager.account_repo.get_account_by_account_no(data.receiver_account_no)
    if not receiver:
        logger.warning("Receiver account not found.")
        raise HTTPException(status_code=404, detail="Receiver account not found.")

    if current_user.balance < data.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance.")

    transaction_id = str(uuid.uuid4())
    pending_transfers[transaction_id] = {
        "sender_user_id": current_user.user_id,
        "receiver_account_no": data.receiver_account_no,
        "amount": data.amount
    }

    return {
        "receiver_account_no": receiver.account_no,
        "receiver_name": receiver.user_name,
        "amount": data.amount,
        "transaction_id": transaction_id
    }
@app.post("/send_money/confirm")
def send_money_confirm(
    data: ConfirmTransferSchema,
    current_user=Depends(get_current_user),
    transaction_manager: TransactionManager = Depends(get_transaction_manager)):
    logger.info("API : Send money confirm.")
    pending = pending_transfers.get(data.transaction_id)

    if not pending:
        logger.warning("Transaction id not found or already used.")
        raise HTTPException(status_code=404, detail="Transaction not found or already used.")

    if pending["sender_user_id"] != current_user.user_id:
        logger.warning("This transaction does not belong to you.")
        raise HTTPException(status_code=403, detail="This transaction does not belong to you.")

    status, message = transaction_manager.send_money(
        current_user,
        pending["receiver_account_no"],
        pending["amount"],
    )

    if not status:
        raise HTTPException(status_code=400, detail=message)

    del pending_transfers[data.transaction_id]
    return {"success": status, "message": message}
@app.get("/statements", response_model=StatementResponse)
def get_statements(
    current_user=Depends(get_current_user),
    get_statement_manager: Statement = Depends(get_statement_manager)):

    logger.info(f"API : Get statements for user {current_user.user_id}")
    history = get_statement_manager.get_history(current_user.account_no)
    return {"transactions": history}

@app.get("/mini_statements", response_model=StatementResponse)
def get_mini_statements(
    current_user=Depends(get_current_user),
    get_statement_manager: Statement = Depends(get_statement_manager)):

    logger.info(f"API : Get mini statements for user {current_user.user_id}")
    history = get_statement_manager.get_top_5_history(current_user.account_no)
    return {"transactions": history}

@app.get("/admin/statements/{account_no}", response_model=StatementResponse)
def show_user_history_for_admin(
    account_no: str,
    statement_manager: Statement = Depends(get_statement_manager),
    current_admin=Depends(get_current_admin),
):
    logger.info(f"API : Admin fetching history for account {account_no}")
    history = statement_manager.get_history(account_no)
    return {"transactions": history}


@app.post("/admin/freeze_account/{account_no}")
def freeze_account_for_admin(
    account_no: str,
    admin_manager: AdminManager = Depends(get_admin_manager),
    current_admin=Depends(get_current_admin),
):
    logger.info(f"API : Admin freezing account {account_no}")
    success, message = admin_manager.freeze_account(account_no)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found or already frozen")

    return {"success": True, "message": message}