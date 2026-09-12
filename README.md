# Bank Manager API

A layered banking API built with **FastAPI**, **SQLAlchemy**, and **Pydantic**.

## Current Status (v5)

- `POST /create_account` — create a new bank account (passwords are bcrypt-hashed, account numbers auto-generated)
- `POST /login_account` — log in and receive a JWT access token
- `GET /me` — get the logged-in user's profile (requires `Authorization: Bearer <token>`)
- `GET /check_balance` — view your current balance
- `POST /deposit` — deposit money into your own account (max 10,000 per deposit)
- `POST /send-money/preview` — preview a transfer to another account (returns a `transaction_id`)
- `POST /send-money/confirm` — confirm a previewed transfer using its `transaction_id`
- `POST /change_password` — change your account password

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

- Change password
- Transaction statements
