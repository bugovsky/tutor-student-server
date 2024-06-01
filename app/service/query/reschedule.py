from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Lesson, LessonRequest
from app.schemas import Status


async def get_lesson_request_by_lesson_id(db: AsyncSession, lesson_id: int) -> LessonRequest:
    query = select(LessonRequest).where(
        LessonRequest.lesson_id == lesson_id,
        LessonRequest.status == Status.pending)
    result = await db.execute(query)
    return result.scalars().first()


async def get_lesson_requests(db: AsyncSession, tutor_id: int) -> Sequence[LessonRequest]:
    query = (
        select(LessonRequest).join(Lesson).
        where(
            Lesson.tutor_id == tutor_id,
            LessonRequest.status == Status.pending)
    )
    result = await db.execute(query)
    return result.scalars().all()
