from pydantic import BaseModel

class CreateAccountSchema(BaseModel):
    user_id: str
    user_name: str
    password: str

class CreateAccountResponse(BaseModel):
    status: bool
    message: str
