from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, Subject, Lesson


async def get_user_by_email(db: AsyncSession, email: str) -> User:
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalars().first()


async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    return result.scalars().first()


async def get_subject_by_lesson_id(db: AsyncSession, lesson_id: int) -> Subject:
    query = select(Subject).join(Lesson).where(Lesson.id == lesson_id)
    result = await db.execute(query)
    return result.scalars().first()
