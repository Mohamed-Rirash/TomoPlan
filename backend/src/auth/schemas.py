from typing import Optional

from pydantic import BaseModel, EmailStr


class User_Base(BaseModel):
    first_name: str
    last_name: str


class User_Create(User_Base):
    email: EmailStr
    password: str


class User_login(User_Base):
    email: EmailStr
    password: str


class User_ForgotPassword(User_Base):
    email: EmailStr


class ResetRequest(BaseModel):
    token: str
    email: EmailStr
    password: str


class VerifyUserRequest(BaseModel):
    token: str
    email: EmailStr
