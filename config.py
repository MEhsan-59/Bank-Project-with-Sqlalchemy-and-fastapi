import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEFAULT_BALANCE = int(os.getenv("DEFAULT_BALANCE", "0"))
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    ADMIN_FILE_NAME = os.getenv("ADMIN_FILE_NAME", "admins.json")