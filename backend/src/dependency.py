# we need to make get_db function so we can use it as a dependency injection for our endpoints

# import session
# create the generator

from collections.abc import Generator
from typing import Annotated

from databases import Database
from fastapi.security import OAuth2PasswordBearer

from src.auth.services import get_user_by_id
from src.config import settings
from src.database import session
from fastapi import Depends, HTTPException, status
import jwt

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"  # ✅ full relative path, no hostname
)


def get_db() -> Generator[Database, None, None]:
    yield session


db_dependency = Annotated[Database, Depends(get_db)]
token_dependency = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(
    db: db_dependency,
    token: Annotated[str, Depends(reusable_oauth2)],
):
    try:
        jwt_decoded = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = jwt_decoded["sub"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


user_dependecy = Annotated[str, Depends(get_current_user)]
# and return the user object
