from datetime import datetime, timedelta, timezone
from typing import Any
from passlib.context import CryptContext
import jwt
from src.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# create_access_token
async def create_access_token(subject: str | Any, expires_delta: timedelta):
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {
        "sub": subject,
        "exp": expire,
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
