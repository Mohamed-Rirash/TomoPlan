from datetime import timedelta
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserUpdateMe(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UpdatePassword(BaseModel):
    current_password: str
    new_password: str


class UserPublic(UserBase):
    id: str


class UsersPublic(BaseModel):
    data: List[UserPublic]
    count: int


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    id: str
    exp: int


class TokenPayload(BaseModel):
    sub: str | None = None
