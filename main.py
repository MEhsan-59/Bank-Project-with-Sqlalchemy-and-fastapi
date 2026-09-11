from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from logger_setup import logger
from schema import (
    CreateAccountResponse, CreateAccountSchema,
    LoginAccountSchema, TokenResponse, ProfileResponse,
    CheckBalanceResponse, DepositSechema, DepositResponse
)
from account_manager import AccountManager
from account_repository import AccountRepository
from database import get_db
from auth import decode_access_token, create_access_token
from transaction_manager import TransactionManager
from transaction_repository import TransactionRepository
from statement_manager import Statement
from statement_repository import StatmentRepository

app = FastAPI(title="Bank Manager API", version="3.0")
security_scheme = HTTPBearer()


def get_account_manager(db: Session = Depends(get_db)) -> AccountManager:
    repo = AccountRepository(db)
    return AccountManager(repo)


def get_statement_manager(db: Session = Depends(get_db)) -> Statement:
    repo = StatmentRepository(db)
    return Statement(repo)


def get_transaction_manager(db: Session = Depends(get_db)) -> TransactionManager:
    transaction_repo = TransactionRepository(db)
    account_repo = AccountRepository(db)
    return TransactionManager(transaction_repo, account_repo, get_statement_manager(db))


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


@app.post("/create_account", response_model=CreateAccountResponse)
def create_account(data: CreateAccountSchema, manager: AccountManager = Depends(get_account_manager)):
    logger.info("API : Create account.")
    status, msg = manager.create_account(data.user_id, data.user_name, data.password)
    return CreateAccountResponse(status=status, message=msg)


@app.post("/login_account", response_model=TokenResponse)
def login_account(data: LoginAccountSchema, manager: AccountManager = Depends(get_account_manager)):
    logger.info("API : Login Account.")
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
    data: DepositSechema,
    current_user=Depends(get_current_user),
    transaction_manager: TransactionManager = Depends(get_transaction_manager)
):
    logger.info("API : Deposit")
    status, message, new_balance = transaction_manager.deposit(current_user.account_no, current_user.balance, data.amount, current_user.user_id)

    if not status:
        logger.warning(message)
        raise HTTPException(status_code=400, detail=message)

    return {"success": status, "message": message, "balance": new_balance}
