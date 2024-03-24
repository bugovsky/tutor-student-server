import typing as t

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .. import database, schemas, oauth2
from ..models import TutorToSubject, Subject, User, TutorToStudentRequest, TutorToStudent
from ..schemas import Role, Status

router = APIRouter(prefix="/requests", tags=['Requests'])


@router.get("/students", status_code=status.HTTP_200_OK, response_model=t.List[schemas.UserOut])
def get_requests_from_students(
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: Session = Depends(database.get_db)
):
    if user.role == Role.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only tutors can view requests from students."
        )
    tutor_students_requests = (
        db.query(User).
        join(
            TutorToStudentRequest,
            User.id == TutorToStudentRequest.student_id
        ).
        filter(
            TutorToStudentRequest.tutor_id == user.id,
            TutorToStudentRequest.status == Status.pending)
        .all()
    )

    return [student for student in tutor_students_requests]


@router.put("/students/{student_id}", status_code=status.HTTP_200_OK)
def respond_to_students_request(
        student_id: int,
        response: schemas.TutorResponse,
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: Session = Depends(database.get_db)
):
    if user.role == Role.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only tutors can respond to requests from students."
        )

    student = db.query(User).filter(User.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found."
        )

    request = (
        db.query(TutorToStudentRequest).
        filter(
            TutorToStudentRequest.tutor_id == user.id,
            TutorToStudentRequest.student_id == student_id,
            TutorToStudentRequest.status == Status.pending).
        first()
    )

    if response.status == Status.accepted:
        request.status = Status.accepted
        tutor_to_student = TutorToStudent(tutor_id=user.id, student_id=student_id)
        db.add(tutor_to_student)
        db.commit()
    elif response.status == Status.rejected:
        request.status = Status.rejected
        db.commit()

    return {"message": "success"}


@router.post("/tutors/{tutor_id}", status_code=status.HTTP_200_OK)
def send_request_to_tutor(
        tutor_id: int,
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: Session = Depends(database.get_db)
):
    if user.role == Role.tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can send request to tutor."
        )

    tutor_to_subject = TutorToStudentRequest(
        tutor_id=tutor_id,
        student_id=user.id,
        status=Status.pending
    )
    db.add(tutor_to_subject)
    db.commit()
    return {"message": "success"}
