import typing as t
from datetime import datetime

from pydantic import BaseModel, EmailStr
from enum import Enum


class Role(Enum):
    tutor = "tutor"
    student = "student"
    admin = "admin"


class TutorSubject(Enum):
    russian = "Русский язык"
    literature = "Литература"
    mathematics = "Математика"
    history = "История"
    biology = "Биология"
    chemistry = "Химия"
    english = "Английский язык"
    physics = "Физика"


class Status(Enum):
    pending = "pending"
    rejected = "rejected"
    accepted = "accepted"


class HomeTaskStatus(Enum):
    in_progress = "in progress"
    done = "done"
    expired = "expired"


class TutorResponse(BaseModel):
    status: Status


class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    role: Role


class UserOut(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
    role: Role

    class Config:
        from_attributes = True


class LessonCreate(BaseModel):
    student_id: int
    subject_id: int
    date_at: datetime = datetime.now().strftime('%Y-%m-%d %H:%M')


class LessonOut(BaseModel):
    id: int
    tutor_id: int
    student_id: int
    subject_id: int
    date_at: t.Optional[datetime]

    class Config:
        from_attributes = True


class TutorToAdd(BaseModel):
    id: int


class TutorOut(BaseModel):
    id: int
    firstname: str
    lastname: str
    subjects: t.List[TutorSubject]


class SubjectsCreate(BaseModel):
    subject_ids: t.List[int]

class SubjectOut(BaseModel):
    id: int
    subject_name: TutorSubject
    class Config:
        from_attributes = True


class LessonRequestCreate(BaseModel):
    lesson_id: int
    reason: str
    new_date_at: t.Optional[datetime] = datetime.now().strftime('%Y-%m-%d %H:%M')


class LessonRespondCreate(BaseModel):
    status: Status


class LessonRequestOut(BaseModel):
    id: int
    lesson_id: int
    reason: str
    status_id: Status = Status.pending
    new_date_at: t.Optional[datetime]

    class Config:
        from_attributes = True


class HomeTaskCreate(BaseModel):
    title: str
    student_id: int
    description: t.Optional[str]
    deadline: t.Optional[datetime] = datetime.now().strftime('%Y-%m-%d %H:%M')


class HomeTaskOut(BaseModel):
    id: int
    title: str
    tutor_id: int
    student_id: int
    status: HomeTaskStatus
    description: t.Optional[str]
    deadline: t.Optional[datetime]

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: t.Optional[int] = None