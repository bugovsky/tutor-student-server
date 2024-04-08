from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas
from ..models import HomeTask
from ..schemas import HomeTaskStatus, Role


async def add_home_task(db: AsyncSession, home_task_form: schemas.HomeTaskCreate, tutor_id):
    home_task = HomeTask(**home_task_form.dict())
    home_task.tutor_id = tutor_id
    home_task.status = HomeTaskStatus.in_progress
    db.add(home_task)
    await db.commit()
    await db.refresh(home_task)
    return home_task


async def get_home_task_by_id(db: AsyncSession, home_task_id):
    query = select(HomeTask).where(HomeTask.id == home_task_id)
    result = await db.execute(query)
    return result.scalars().first()

async def get_home_tasks(db: AsyncSession, user_id: int, role : Role):
    if role == Role.tutor:
        query = select(HomeTask).where(HomeTask.tutor_id == user_id)
        result = await db.execute(query)
        return result.scalars().all()
    elif role == Role.student:
        query = select(HomeTask).where(HomeTask.student_id == user_id)
        result = await db.execute(query)
        return result.scalars().all()


async def add_response_to_task(db: AsyncSession, task_id: int, home_task_name: str):
    home_task = await get_home_task_by_id(db, task_id)
    home_task.filename = home_task_name
    if home_task.status == HomeTaskStatus.in_progress:
        home_task.status = HomeTaskStatus.done
    await db.commit()
    return home_task
