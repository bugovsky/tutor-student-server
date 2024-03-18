import typing as t

from pydantic import BaseModel, EmailStr
from enum import Enum


class Role(Enum):
    tutor = "tutor"
    student = "student"
    admin = "admin"


class TutorSubject(Enum):
    russian = "russian"
    literature = "literature"
    mathematics = "mathematics"
    history = "history"
    biology = "biology"
    chemistry = "chemistry"
    english = "english"
    physics = "physics"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Role


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: Role

    class Config:
        from_attributes = True


class TutorToAdd(BaseModel):
    id: int


class TutorOut(BaseModel):
    id: int
    email: EmailStr
    subjects: t.List[TutorSubject]


class SubjectsCreate(BaseModel):
    subject_ids: t.List[int]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: t.Optional[int] = None
