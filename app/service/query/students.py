from typing import Sequence, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Lesson, User, TutorToSubject, Subject, TutorToStudent


async def get_schedule_by_tutor(db: AsyncSession, student_id: int, tutor_id: int) -> Sequence[Lesson]:
    query = select(Lesson).where(Lesson.tutor_id == tutor_id, Lesson.student_id == student_id).order_by(Lesson.date_at)
    result = await db.execute(query)
    return result.scalars().all()


async def get_schedule(db: AsyncSession, student_id: int) -> Sequence[Lesson]:
    query = select(Lesson).where(Lesson.student_id == student_id).order_by(Lesson.date_at)
    result = await db.execute(query)
    return result.scalars().all()


async def get_all_tutors(db: AsyncSession):
    query = (
        select(User.id, User.firstname, User.lastname, Subject.subject_name)
        .join(TutorToSubject, User.id == TutorToSubject.tutor_id)
        .join(Subject, TutorToSubject.subject_id == Subject.id)
    )
    result = await db.execute(query)
    return result.all()


async def get_all_tutors_by_subjects(db: AsyncSession, subject_ids: List[int]):
    query = (
        select(User.id, User.firstname, User.lastname, Subject.subject_name)
        .join(TutorToSubject, User.id == TutorToSubject.tutor_id)
        .join(Subject, TutorToSubject.subject_id == Subject.id)
        .where(
            TutorToSubject.subject_id.in_(subject_ids)
        )
    )
    result = await db.execute(query)
    return result.all()


async def get_tutors(db: AsyncSession, student_id: int) -> Sequence[User]:
    query = (
        select(User).
        join(
            TutorToStudent,
            User.id == TutorToStudent.tutor_id
        ).
        filter(TutorToStudent.student_id == student_id)
    )
    result = await db.execute(query)
    return result.scalars().all()
