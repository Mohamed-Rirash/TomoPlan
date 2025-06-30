from databases import Database
from fastapi import APIRouter, Depends, HTTPException, status

from src.auth.schemas import UserRegister
from src.auth.services import create_user, get_user_by_email
from src.dependency import get_db

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/sign up", status_code=status.HTTP_201_CREATED)
async def register_user(*, data: UserRegister, db: Database = Depends(get_db)):
    # TODO: check if user already exists
    user = await get_user_by_email(data.email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists please login",
        )
    # TODO: if not there, create user
    user = await create_user(data, db)
    return {"message": "User created successfully"}
    # TODO: then send email to user to confirm account


@router.post("/login")
async def login():
    pass


@router.post("/forgetpassword")
async def forget_password():
    pass
