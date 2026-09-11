from pydantic import BaseModel

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
