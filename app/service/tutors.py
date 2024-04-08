from typing import Sequence

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas
from ..models import TutorToSubject, Subject, User, TutorToStudent, Lesson


async def add_subject(db: AsyncSession, tutor_id, subject_id: int):
    await delete_subject(db, tutor_id, subject_id)
    new_tutor_subject = TutorToSubject(tutor_id=tutor_id, subject_id=subject_id)
    db.add(new_tutor_subject)
    await db.commit()
    await db.refresh(new_tutor_subject)


async def delete_subject(db: AsyncSession, tutor_id: int, subject_id: int):
    query = (delete(TutorToSubject).
             where(TutorToSubject.tutor_id == tutor_id).
             where(TutorToSubject.subject_id == subject_id)
             )
    await db.execute(query)
    await db.commit()


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


async def add_lesson(db: AsyncSession, lesson: schemas.LessonCreate, tutor_id: int) -> Lesson:
    new_lesson = Lesson(**lesson.dict())
    new_lesson.tutor_id = tutor_id
    db.add(new_lesson)
    await db.commit()
    await db.refresh(new_lesson)
    return new_lesson


async def get_schedule(db: AsyncSession, tutor_id: int) -> Sequence[Lesson]:
    query = select(Lesson).where(Lesson.tutor_id == tutor_id).order_by(Lesson.date_at)
    result = await db.execute(query)
    return result.scalars().all()


async def get_schedule_by_student(db: AsyncSession, tutor_id: int, student_id: int) -> Sequence[Lesson]:
    query = select(Lesson).where(Lesson.tutor_id == tutor_id, Lesson.student_id == student_id).order_by(Lesson.date_at)
    result = await db.execute(query)
    return result.scalars().all()
