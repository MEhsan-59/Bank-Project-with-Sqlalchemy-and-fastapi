import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEFAULT_BALANCE = int(os.getenv("DEFAULT_BALANCE", "0"))
