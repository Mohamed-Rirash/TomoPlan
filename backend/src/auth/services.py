from sqlalchemy import select
from src.auth.schemas import UserRegister
from src.auth.models import users


async def get_user_by_email(email: str, db):
    query = select(users).where(users.c.email == email)
    result = await db.fetch_one(query)
    return result


async def create_user(user: UserRegister, db):
    query = users.insert().values(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=user.password,
    )
    result = await db.execute(query)
    return result
