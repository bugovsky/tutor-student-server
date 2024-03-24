from fastapi import FastAPI
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
import yadisk

from app.utils import cloud
from app.database import engine, Base, async_session
from app.models import Subject
from app import config
from app.routers import users, auth, tutors, students, reschedule, enrollment, hometask
from app.schemas import TutorSubject

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tutors.router)
app.include_router(students.router)
app.include_router(enrollment.router)
app.include_router(reschedule.router)
app.include_router(hometask.router)


async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def populate_subjects_table(db: AsyncSession):
    query = select(func.count(Subject.id))
    res = await db.execute(query)
    if res.scalars().first() == 0:
        subjects = [Subject(subject_name=subject) for subject in TutorSubject]
        db.add_all(subjects)
        await db.commit()


@app.on_event("startup")
async def init():
    await init_models()
    y = yadisk.AsyncClient(token=config.settings.yandex_disk_token)
    async with y:
        await cloud.create_folder_disk(y, "/TutorStudentApp")
    async with async_session() as db:
        await populate_subjects_table(db)
