import typing as t

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .. import database, schemas, oauth2
from ..models import TutorToStudentRequest, TutorToStudent, Lesson
from ..schemas import Role, Status

router = APIRouter(prefix="/students", tags=['Students'])


@router.get("/schedule", status_code=status.HTTP_200_OK, response_model=t.List[schemas.StudentLessonOut])
def get_schedule(
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: Session = Depends(database.get_db)):
    if user.role == Role.tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can view schedule by their tutors."
        )

    schedule = db.query(Lesson).filter(Lesson.student_id == user.id).all()

    return [lesson for lesson in schedule]


@router.get("/schedule/{tutor_id}", status_code=status.HTTP_200_OK, response_model=t.List[schemas.StudentLessonOut])
def get_schedule_by_tutor(
        tutor_id: int,
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: Session = Depends(database.get_db)):
    if user.role == Role.tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can view schedule by their tutor."
        )

    schedule_by_tutor = (
        db.query(Lesson).
        filter(
            Lesson.student_id == user.id, Lesson.tutor_id == tutor_id
        ).
        all()
    )

    return [lesson for lesson in schedule_by_tutor]
