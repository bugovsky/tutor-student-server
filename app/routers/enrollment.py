import typing as t

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .. import database, schemas, oauth2
from ..schemas import Role
from ..service.command import enrollment

router = APIRouter(prefix="/enroll", tags=['Enrollment'])


@router.get("/", status_code=status.HTTP_200_OK, response_model=t.List[schemas.UserOut])
async def get_enrollment_requests(
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: AsyncSession = Depends(database.get_db)
):
    if user.role == Role.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только репетиторы могут видеть заявки от учеников"
        )
    tutor_students_requests = await enrollment.get_students_to_enroll(db, user.id)
    return [student for student in tutor_students_requests]


@router.patch("/{student_id}", status_code=status.HTTP_200_OK)
async def respond_to_enrollment_request(
        student_id: int,
        response: schemas.TutorResponse,
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: AsyncSession = Depends(database.get_db)
):
    if user.role == Role.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только репетиторы могут отвечать на входящий запрос от ученика"
        )
    enrollment_request = await enrollment.get_enrollment_request_by_student_id(
        db, tutor_id=user.id, student_id=student_id
    )
    await enrollment.update_enrollment_request(db, enrollment_request, response.status)
    return {"message": "success"}


@router.post("/{tutor_id}", status_code=status.HTTP_201_CREATED)
async def send_enrollment_request_to_tutor(
        tutor_id: int,
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: AsyncSession = Depends(database.get_db)
):
    if user.role == Role.tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can enroll to tutor."
        )
    await enrollment.add_enrollment_request(db, user.id, tutor_id=tutor_id)
    return {"message": "success"}
