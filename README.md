# Bank Manager API

A layered banking API built with **FastAPI**, **SQLAlchemy**, and **Pydantic**.

## Current Status (v1)

- `POST /create_account` — create a new bank account (passwords are bcrypt-hashed, account numbers auto-generated)

## Quick Start

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Configure environment

Copy `.env.example` to `.env` and fill in your own values:

```
cp .env.example .env
```

```
DATABASE_URL=postgresql://username:password@localhost:5432/bank
DEFAULT_BALANCE=0
```

### 3. Create the tables

```
python create_table.py
```

### 4. Start the development server

```
uvicorn main:app --reload
```

Open <http://127.0.0.1:8000/docs> for the interactive Swagger UI.

## Testing

```
pytest
```

## Project Structure

```
.
├── main.py                  # FastAPI app and HTTP routes
├── schema.py                # Pydantic request and response schemas
├── account_manager.py       # Account business rules
├── account_repository.py    # SQLAlchemy database operations for accounts
├── security.py               # Password hashing/verification (bcrypt)
├── models.py                  # SQLAlchemy models
├── database.py                 # Engine, sessions, and DB dependency
├── config.py                    # Environment-driven settings
├── create_table.py             # Database table initialization script
├── requirements.txt             # Python dependencies
└── test_*.py                    # Tests
```

## Roadmap

- Login with JWT authentication
- Check balance and deposit
- Send money between accounts
- Change password
- Transaction statements
