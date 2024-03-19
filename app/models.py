from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from datetime import datetime

from app.database import Base
from app.schemas import Role, TutorSubject, Status


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    role = Column(Enum(Role))


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    subject_name = Column(Enum(TutorSubject))


class TutorToSubject(Base):
    __tablename__ = 'tutor_to_subjects'
    tutor_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), primary_key=True)


class TutorToStudent(Base):
    __tablename__ = 'tutor_to_students'
    tutor_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    student_id = Column(Integer, ForeignKey('users.id'), primary_key=True)


class TutorToStudentRequest(Base):
    __tablename__ = 'tutor_to_student_requests'
    id = Column(Integer, primary_key=True)
    tutor_id = Column(Integer, ForeignKey('users.id'))
    student_id = Column(Integer, ForeignKey('users.id'))
    status = Column(Enum(Status))


class Lesson(Base):
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True)
    tutor_id = Column(Integer, ForeignKey('users.id'))
    student_id = Column(Integer, ForeignKey('users.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    date_at = Column(DateTime, default=datetime.now().strftime('%Y-%m-%d %H:%M'))


class LessonRequest(Base):
    __tablename__ = 'lesson_request'
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    status_id = Column(Enum(Status))
    new_date_at = Column(DateTime, default=datetime.utcnow, nullable=True)
