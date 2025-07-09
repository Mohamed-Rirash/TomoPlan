import uuid
from collections.abc import Generator
from typing import Annotated

import jwt
from databases import Database
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from src.auth.services import get_user_by_id
from src.config import settings
from src.database import session

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"  # ✅ full relative path, no hostname
)


def get_db() -> Generator[Database, None, None]:
    yield session


db_dependency = Annotated[Database, Depends(get_db)]
token_dependency = Annotated[str, Depends(reusable_oauth2)]


async def get_current_user(
    db: db_dependency,
    token: Annotated[str, Depends(reusable_oauth2)],
) -> str:
    try:
        jwt_decoded = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = uuid.UUID(jwt_decoded["sub"])

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


user_dependecy = Annotated[str, Depends(get_current_user)]
