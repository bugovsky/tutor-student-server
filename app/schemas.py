import typing as t

from pydantic import BaseModel, EmailStr
from enum import Enum


class Role(Enum):
    tutor = "tutor"
    student = "student"
    admin = "admin"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Role


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: t.Optional[str] = None
