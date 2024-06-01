from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TutorToSubject, Subject, User, TutorToStudent, Lesson


async def get_students(db: AsyncSession, tutor_id: int) -> Sequence[User]:
    query = (
        select(User).
        join(
            TutorToStudent,
            User.id == TutorToStudent.student_id
        ).
        filter(TutorToStudent.tutor_id == tutor_id)
    )
    result = await db.execute(query)
    return result.scalars().all()


async def get_subject_name_by_id(db: AsyncSession, subject_id: int) -> str:
    query = select(Subject.subject_name).where(Subject.id == subject_id)
    result = await db.execute(query)
    return result.scalars().first()


async def get_subjects_by_tutor_id(db: AsyncSession, tutor_id: int) -> Sequence[Subject]:
    query = select(Subject).join(TutorToSubject).where(TutorToSubject.tutor_id == tutor_id)
    result = await db.execute(query)
    return result.scalars().all()


async def get_schedule(db: AsyncSession, tutor_id: int) -> Sequence[Lesson]:
    query = select(Lesson).where(Lesson.tutor_id == tutor_id).order_by(Lesson.date_at)
    result = await db.execute(query)
    return result.scalars().all()


async def get_schedule_by_student(db: AsyncSession, tutor_id: int, student_id: int) -> Sequence[Lesson]:
    query = select(Lesson).where(Lesson.tutor_id == tutor_id, Lesson.student_id == student_id).order_by(Lesson.date_at)
    result = await db.execute(query)
    return result.scalars().all()
