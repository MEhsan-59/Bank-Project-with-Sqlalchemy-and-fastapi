from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class CreateAccountSchema(BaseModel):
    user_id: str = Field(..., min_length=3, max_length=30)
    user_name: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8, max_length=72)

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


class StatementResponse(BaseModel):
    transactions: List[TransactionItem]

class DepositSchema(BaseModel):
    amount: Decimal = Field(..., gt=0, le=10000) 

class SendMoneySchema(BaseModel):
    receiver_account_no: str = Field(..., min_length=6)
    amount: Decimal = Field(..., gt=0)           

class TransactionItem(BaseModel):
    type: str
    amount: Decimal    
    balance_after: Decimal
    related_account: Optional[str] = None
    created_at: datetime