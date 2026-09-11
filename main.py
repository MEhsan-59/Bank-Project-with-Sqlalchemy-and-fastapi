from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from logger_setup import logger
from schema import CreateAccountResponse, CreateAccountSchema
from account_manager import AccountManager
from account_repository import AccountRepository
from database import get_db

app = FastAPI(title="Bank Manager API", version="1.0")


def get_account_manager(db: Session = Depends(get_db)) -> AccountManager:
    repo = AccountRepository(db)
    return AccountManager(repo)


@app.post("/create_account", response_model=CreateAccountResponse)
def create_account(data: CreateAccountSchema, manager: AccountManager = Depends(get_account_manager)):
    logger.info("API : Create account.")
    status, msg = manager.create_account(data.user_id, data.user_name, data.password)
    return CreateAccountResponse(status=status, message=msg)
