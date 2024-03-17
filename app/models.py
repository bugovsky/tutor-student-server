from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    subject_name = Column(String, unique=True)

    tutors = relationship("Tutor", secondary="tutor_to_subject", back_populates="subjects")


class Tutor(Base):
    __tablename__ = "tutors"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)

    subjects = relationship("Subject", secondary="tutor_to_subject", back_populates="tutors")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)


class TutorToSubject(Base):
    __tablename__ = "tutor_to_subject"

    tutor_id = Column(Integer, ForeignKey('tutors.id'), primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), primary_key=True)

    tutor = relationship("Tutor", back_populates="subjects")
    subject = relationship("Subject", back_populates="tutors")


class TutorToStudent(Base):
    __tablename__ = "tutor_to_student"

    tutor_id = Column(Integer, ForeignKey('tutors.id'), primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)

    tutor = relationship("Tutor")
    student = relationship("Student")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    tutor_id = Column(Integer, ForeignKey('tutors.id'))
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    date_at = Column(TIMESTAMP)

    tutor = relationship("Tutor")
    student = relationship("Student")
    subject = relationship("Subject")


class LessonRequest(Base):
    __tablename__ = "lesson_request"

    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    status_id = Column(Integer, ForeignKey('request_statuses.id'))

    lesson = relationship("Lesson")
    status = relationship("RequestStatus")


class RequestStatus(Base):
    __tablename__ = "request_statuses"

    id = Column(Integer, primary_key=True)
    status = Column(String, unique=True)

    lesson_requests = relationship("LessonRequest")
