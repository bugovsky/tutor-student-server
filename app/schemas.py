import typing as t
from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator
from enum import Enum

from pydantic.v1 import root_validator


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


class Status(Enum):
    pending = "pending"
    rejected = "rejected"
    accepted = "accepted"


class TutorResponse(BaseModel):
    status: Status


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


class LessonCreate(BaseModel):
    student_id: int
    subject_id: int
    date_at: str = datetime.now().strftime('%Y-%m-%d %H:%M')


class TutorLessonOut(BaseModel):
    id: int
    student_id: int
    subject_id: int
    date_at: datetime

    class Config:
        from_attributes = True


class StudentLessonOut(BaseModel):
    id: int
    tutor_id: int
    subject_id: int
    date_at: datetime

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
