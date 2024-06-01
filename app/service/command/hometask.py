from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.models import HomeTask
from app.schemas import HomeTaskStatus
from app.service.query.hometask import get_home_task_by_id


async def add_home_task(db: AsyncSession, home_task_form: schemas.HomeTaskCreate, tutor_id):
    home_task = HomeTask(**home_task_form.dict())
    home_task.tutor_id = tutor_id
    home_task.status = HomeTaskStatus.in_progress
    db.add(home_task)
    await db.commit()
    await db.refresh(home_task)
    return home_task


async def add_response_to_task(db: AsyncSession, task_id: int, home_task_name: str):
    home_task = await get_home_task_by_id(db, task_id)
    home_task.filename = home_task_name
    if home_task.status == HomeTaskStatus.in_progress:
        home_task.status = HomeTaskStatus.done
    await db.commit()
    return home_task
