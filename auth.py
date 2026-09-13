#auth.py
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from config import Config


def create_access_token(user_id: str, role: str = "user", extra_claims: dict | None = None):
    payload = {"sub": user_id, "role": role, "exp": datetime.now(timezone.utc) + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)}
    if extra_claims:
        payload.update(extra_claims)
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return token


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        return payload
    except JWTError:
        return None
