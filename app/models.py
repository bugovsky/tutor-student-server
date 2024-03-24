from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database import Base
from app.schemas import Role, TutorSubject, Status, HomeTaskStatus


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str]
    lastname: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    role: Mapped[Role]


class Subject(Base):
    __tablename__ = 'subjects'
    id: Mapped[int] = mapped_column(primary_key=True)
    subject_name: Mapped[TutorSubject]


class TutorToSubject(Base):
    __tablename__ = 'tutor_to_subjects'
    tutor_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey('subjects.id'), primary_key=True)


class TutorToStudent(Base):
    __tablename__ = 'tutor_to_students'
    tutor_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)


class TutorToStudentRequest(Base):
    __tablename__ = 'tutor_to_student_requests'
    id: Mapped[int] = mapped_column(primary_key=True)
    tutor_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    student_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    status: Mapped[Status]


class Lesson(Base):
    __tablename__ = 'lessons'
    id: Mapped[int] = mapped_column(primary_key=True)
    tutor_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    student_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    subject_id: Mapped[int] = mapped_column(ForeignKey('subjects.id'))
    date_at: Mapped[datetime] = mapped_column(nullable=True)


class LessonRequest(Base):
    __tablename__ = 'lesson_requests'
    id: Mapped[int] = mapped_column(primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey('lessons.id'))
    status: Mapped[Status]
    reason: Mapped[str]
    new_date_at: Mapped[datetime] = mapped_column(nullable=True)


class HomeTask(Base):
    __tablename__ = 'home_tasks'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    tutor_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    student_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    deadline: Mapped[datetime] = mapped_column(nullable=True)
    filename: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[HomeTaskStatus]
