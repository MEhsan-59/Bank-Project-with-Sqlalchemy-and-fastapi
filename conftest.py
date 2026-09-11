import os
import sys

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("DEFAULT_BALANCE", "0")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from models import Base
from account_repository import AccountRepository
from account_manager import AccountManager


@pytest.fixture()
def db_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture()
def account_repo(db_session):
    return AccountRepository(db_session)


@pytest.fixture()
def account_manager(account_repo):
    return AccountManager(account_repo)


@pytest.fixture()
def client(db_session):
    """
    FastAPI TestClient wired to the isolated in-memory test database,
    using FastAPI's dependency_overrides so every request gets the
    same test session instead of a real Postgres connection.
    """
    from fastapi.testclient import TestClient
    import main

    main.app.dependency_overrides[main.get_db] = lambda: db_session
    try:
        yield TestClient(main.app)
    finally:
        main.app.dependency_overrides.clear()
