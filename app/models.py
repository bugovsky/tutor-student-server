from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from datetime import datetime

from app.database import Base
from app.schemas import Role


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    role = Column(Enum(Role))


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    subject_name = Column(String)


class TutorToSubject(Base):
    __tablename__ = 'tutor_to_subject'
    tutor_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), primary_key=True)


class TutorToStudent(Base):
    __tablename__ = 'tutor_to_student'
    tutor_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    student_id = Column(Integer, ForeignKey('users.id'), primary_key=True)


class Lesson(Base):
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True)
    tutor_id = Column(Integer, ForeignKey('users.id'))
    student_id = Column(Integer, ForeignKey('users.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    date_at = Column(DateTime, default=datetime.utcnow)


class LessonRequest(Base):
    __tablename__ = 'lesson_request'
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    status_id = Column(Integer, ForeignKey('request_statuses.id'))


class RequestStatus(Base):
    __tablename__ = 'request_statuses'
    id = Column(Integer, primary_key=True)
    status = Column(String)
