from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class CreateAccountSchema(BaseModel):
    user_id: str
    user_name: str
    password: str

class CreateAccountResponse(BaseModel):
    status: bool
    message: str

class LoginAccountSchema(BaseModel):
    user_id: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class ProfileResponse(BaseModel):
    message: str
    account_no: str
    name: str
    balance: float

class CheckBalanceResponse(BaseModel):
    success: bool
    balance: float

class DepositResponse(BaseModel):
    success: bool
    message: str
    balance: float

class DepositSechema(BaseModel):
    amount: int

class SendMoneySchema(BaseModel):
    receiver_account_no: str = Field(..., min_length=6)
    amount: int = Field(..., gt=0)

class SendMoneyPreviewResponse(BaseModel):
    receiver_account_no: str
    receiver_name: str
    amount: int
    transaction_id: str

class ConfirmTransferSchema(BaseModel):
    transaction_id: str

class Change_password_Schema(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str

class ChangePasswordResponse(BaseModel):
    success: bool
    message: str

class TransactionItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    type: str
    amount: float
    balance_after: float
    related_account: Optional[str] = None
    created_at: datetime

class StatementResponse(BaseModel):
    transactions: List[TransactionItem]
