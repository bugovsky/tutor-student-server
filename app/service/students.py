from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Lesson


async def get_schedule_by_tutor(db: AsyncSession, student_id: int, tutor_id: int) -> Sequence[Lesson]:
    query = select(Lesson).where(Lesson.tutor_id == tutor_id, Lesson.student_id == student_id)
    result = await db.execute(query)
    return result.scalars().all()


async def get_schedule(db: AsyncSession, student_id: int) -> Sequence[Lesson]:
    query = select(Lesson).where(Lesson.student_id == student_id)
    result = await db.execute(query)
    return result.scalars().all()
