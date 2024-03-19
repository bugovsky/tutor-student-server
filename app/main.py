from fastapi import FastAPI
from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models
from .database import engine, SessionLocal
from .models import Subject
from .routers import user, auth, tutor, student, request
from .schemas import TutorSubject

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(tutor.router)
app.include_router(student.router)
app.include_router(request.router)


def populate_subjects_table(db: Session):
    if db.query(func.count(Subject.id)).scalar() == 0:
        for subject_name in TutorSubject:
            db_subject = Subject(subject_name=subject_name)
            db.add(db_subject)
        db.commit()


def startup():
    # models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    populate_subjects_table(db)
    db.close()


@app.on_event("startup")
async def startup_event():
    startup()
