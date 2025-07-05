from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.schemas import (
    LoginResponse,
    UpdatePassword,
    UserRegister,
    UserUpdateMe,
)
from src.auth.security import create_access_token, get_password_hash, verify_password
from src.auth.services import (
    authenticate_user,
    create_user,
    get_user_by_email,
    update_current_user,
    update_current_user_password,
)
from src.config import settings
from src.dependency import db_dependency, user_dependecy

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/sign up", status_code=status.HTTP_201_CREATED)
async def register_user(*, data: UserRegister, db: db_dependency):
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
    db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()
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


@router.patch("/me")
async def update_user_me(user: user_dependecy, data: UserUpdateMe, db: db_dependency):  # type: ignore
    user_id = user.id  # type: ignore
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    # TODO: check if user is active
    if not user.is_active:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not active"
        )
    return await update_current_user(user_id, data, db)


@router.patch("/me/password")
async def update_user_password(
    user: user_dependecy,
    data: UpdatePassword,
    db: db_dependency,  # type: ignore
):
    # verify the user
    if not verify_password(data.current_password, user.password):  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
        )
    hashed_password = get_password_hash(data.new_password)

    # check if the new password is == convermin the passowrd
    if user.password == hashed_password:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password is same as old password",
        )
    return await update_current_user_password(user.id, hashed_password, db)  # type: ignore


# then update the user password in the db
