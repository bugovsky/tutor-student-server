import typing as t

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .. import database, schemas, oauth2
from ..schemas import Role
from ..service.query import reschedule

router = APIRouter(prefix="/reschedule", tags=['Reschedule'])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.LessonRequestOut
)
async def send_reschedule_request_to_tutor(
        lesson_request: schemas.LessonRequestCreate,
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: AsyncSession = Depends(database.get_db)
):
    if user.role == Role.tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Репетиторы не могут отправлять запрос на изменение расписания"
        )
    new_lesson_request = await reschedule.add_lesson_request(db, lesson_request=lesson_request)
    return new_lesson_request


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=t.List[schemas.LessonRequestOut]
)
async def get_reschedule_requests(
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: AsyncSession = Depends(database.get_db)
):
    if user.role == Role.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только репетиторы могут просматривать запросы изменения расписания"
        )
    reschedule_requests = await reschedule.get_lesson_requests(db, user.id)
    return [request for request in reschedule_requests]


@router.patch(
    "/{lesson_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.LessonOut
)
async def respond_to_reschedule_request(
        lesson_id: int,
        lesson_respond: schemas.LessonRespondCreate,
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: AsyncSession = Depends(database.get_db)
):
    if user.role == Role.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только репетиторы могут отвечать на запрос изменения расписания"
        )
    lesson_request = await reschedule.get_lesson_request_by_lesson_id(db, lesson_id)
    return await reschedule.update_lesson_request(db, lesson_request, lesson_respond.status)
