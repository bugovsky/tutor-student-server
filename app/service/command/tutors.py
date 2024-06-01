from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.models import TutorToSubject, Lesson


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


async def add_lesson(db: AsyncSession, lesson: schemas.LessonCreate, tutor_id: int) -> Lesson:
    new_lesson = Lesson(**lesson.dict())
    new_lesson.tutor_id = tutor_id
    db.add(new_lesson)
    await db.commit()
    await db.refresh(new_lesson)
    return new_lesson
