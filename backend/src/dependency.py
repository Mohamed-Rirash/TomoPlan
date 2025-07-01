# we need to make get_db function so we can use it as a dependency injection for our endpoints

# import session
# create the generator

from collections.abc import Generator
from typing import Annotated

from databases import Database
from fastapi.security import OAuth2PasswordBearer

from src.auth import services
from src.auth.services import get_user_by_id
from src.config import settings
from src.database import session
from fastapi import Depends
import jwt

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}auth/login")


def get_db() -> Generator[Database, None, None]:
    db = session
    try:
        yield db
    finally:
        db.disconnect()


db_dependency = Annotated[Database, Depends(get_db)]
token_dependency = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(db: db_dependency, token: token_dependency):
    # decoding the token to extract the user id
    jwt_decoded = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[services.ALGORITHM]
    )
    user_id = jwt_decoded["sub"]

    # then we can use the user id to get the user from the database
    user = get_user_by_id(user_id, db)


# and return the user object
