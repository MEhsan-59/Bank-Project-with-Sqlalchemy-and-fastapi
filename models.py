from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from config import Config

Base = declarative_base()

class Account(Base):
    __tablename__ = "Account"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(String, nullable=False, unique=True, index=True)
    user_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    account_no = Column(String, nullable=False, unique=True, index=True)
    balance = Column(Integer, nullable=False, default=Config.DEFAULT_BALANCE)
