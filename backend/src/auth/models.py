import datetime
import uuid
from dataclasses import dataclass

from sqlalchemy import UUID, Column, DateTime, ForeignKey, String, func
from sqlalchemy.orm import mapped_column, relationship

from ..database import Base


@dataclass
class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # relationships
    tokens = relationship("UserToken", back_populates="user")


@dataclass
class UserToken(Base):
    __tablename__ = "user_tokens"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = mapped_column(ForeignKey("users.id"))
    access_key = Column(String(250), nullable=True, index=True, default=None)
    refresh_key = Column(String(250), nullable=True, index=True, default=None)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="tokens")
