from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.models import Lesson, LessonRequest
from app.schemas import Status


async def add_lesson_request(db: AsyncSession, lesson_request: schemas.LessonRequestCreate):
    new_lesson_request = LessonRequest(**lesson_request.dict())
    new_lesson_request.status = Status.pending
    db.add(new_lesson_request)
    await db.commit()
    await db.refresh(new_lesson_request)
    return new_lesson_request


async def update_lesson_request(db: AsyncSession, reschedule_request: LessonRequest, status: Status) -> Lesson:
    reschedule_request.status = status
    query = select(Lesson).where(Lesson.id == reschedule_request.lesson_id)
    result = await db.execute(query)
    lesson = result.scalars().first()
    if status == Status.accepted:
        lesson.date_at = reschedule_request.new_date_at
    await db.commit()
    return lesson
