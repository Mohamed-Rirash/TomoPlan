from datetime import timedelta
from databases import Database
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.schemas import (
    LoginResponse,
    UserPublic,
    UserRegister,
    UserUpdateMe,
)
from src.auth.security import create_access_token
from src.auth.services import authenticate_user, create_user, get_user_by_email
from src.dependency import get_db
from src.config import settings

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/sign up", status_code=status.HTTP_201_CREATED)
async def register_user(*, data: UserRegister, db: Database = Depends(get_db)):
    # TODO: check if user already exists
    user = await get_user_by_email(data.email, db)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists please login",
        )
    # TODO: if not there, create user
    user = await create_user(data, db)

    # TODO: then send email to user to confirm account
    return {"message": "User created successfully"}


@router.post("/login", response_model=LoginResponse)
async def login_user(
    db: Database = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    # TODO: 1- authenticate the user
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    # then check the user is active
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not active"
        )
    # TODO: 2- create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(user.id, access_token_expires)
    # return Token(token=access_token, exp=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # return {"access_token": access_token, "token_type": "bearer"}
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "id": str(user.id),
        "exp": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    }


@router.patch("/me", response_model=UserPublic)
async def update_user_me(data: UserUpdateMe, db: Database = Depends(get_db)):
    pass
