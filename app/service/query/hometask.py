from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import HomeTask
from app.schemas import Role


async def get_home_task_by_id(db: AsyncSession, home_task_id):
    query = select(HomeTask).where(HomeTask.id == home_task_id)
    result = await db.execute(query)
    return result.scalars().first()


async def get_home_tasks(db: AsyncSession, user_id: int, role: Role):
    if role == Role.tutor:
        query = select(HomeTask).where(HomeTask.tutor_id == user_id)
        result = await db.execute(query)
        return result.scalars().all()
    elif role == Role.student:
        query = select(HomeTask).where(HomeTask.student_id == user_id)
        result = await db.execute(query)
        return result.scalars().all()
