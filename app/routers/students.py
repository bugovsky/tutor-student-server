import typing as t

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .. import database, schemas, oauth2
from ..schemas import Role
from ..service import students

router = APIRouter(prefix="/students", tags=['Students'])


@router.get("/schedule", status_code=status.HTTP_200_OK, response_model=t.List[schemas.LessonOut])
async def get_schedule(
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: AsyncSession = Depends(database.get_db)):
    if user.role == Role.tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Репетиторы не могут просматривать расписание учеников"
        )

    schedule = await students.get_schedule(db, user.id)
    return [lesson for lesson in schedule]


@router.get("/schedule/{tutor_id}", status_code=status.HTTP_200_OK, response_model=t.List[schemas.LessonOut])
async def get_schedule_by_tutor(
        tutor_id: int,
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: AsyncSession = Depends(database.get_db)):
    if user.role == Role.tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Репетиторы не могут просматривать расписание учеников"
        )

    schedule_by_tutor = await students.get_schedule_by_tutor(db, student_id=user.id, tutor_id=tutor_id)

    return [lesson for lesson in schedule_by_tutor]
