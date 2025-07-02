import uuid

from sqlalchemy import select
from src.auth.schemas import UserRegister
from src.auth.models import users
from src.auth.security import get_password_hash, verify_password


async def get_user_by_email(email: str, db):
    query = select(users).where(users.c.email == email)
    result = await db.fetch_one(query)
    return result


async def create_user(user: UserRegister, db):
    user_id = uuid.uuid4()
    query = users.insert().values(
        id=user_id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=get_password_hash(user.password),
        is_active=True,
    )

    result = await db.execute(query)
    return result


async def authenticate_user(email: str, password: str, db):
    db_usser = await get_user_by_email(email, db)
    if not db_usser:
        return False
    if not verify_password(password, db_usser.password):
        return False
    return db_usser


async def get_user_by_id(user_id: uuid.UUID, db):
    query = select(users).where(users.c.id == user_id)
    result = await db.fetch_one(query)
    return result
