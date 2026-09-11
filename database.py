import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from logger_setup import logger

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    logger.critical("DATABASE_URL is not set. Check your .env file.")
    raise ValueError("DATABASE_URL environment variable is not set.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger.info("Database engine initialized successfully.")


def get_db():
    db = SessionLocal()
    logger.debug("Database session opened.")
    try:
        yield db
    finally:
        db.close()
        logger.debug("Database session closed.")
