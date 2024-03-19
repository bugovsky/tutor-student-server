import typing as t

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .. import database, schemas, oauth2
from ..models import TutorToSubject, Subject, User, TutorToStudentRequest, TutorToStudent, Lesson
from ..schemas import Role, Status

router = APIRouter(prefix="/tutors", tags=['Tutors'])


@router.post("/subjects", status_code=status.HTTP_200_OK, response_model=schemas.TutorOut)
def add_subjects_to_tutor(
        subjects: schemas.SubjectsCreate,
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: Session = Depends(database.get_db)
):
    if user.role == Role.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only tutors can add subjects."
        )
    for subject_id in subjects.subject_ids:
        tutor_to_subject = TutorToSubject(tutor_id=user.id, subject_id=subject_id)
        db.add(tutor_to_subject)
    db.commit()
    tutor_subjects = (
        db.query(Subject).
        join(TutorToSubject).
        filter(TutorToSubject.tutor_id == user.id).
        all()
    )

    tutor_out = schemas.TutorOut(
        id=user.id,
        email=user.email,
        subjects=[subject.subject_name for subject in tutor_subjects]
    )

    return tutor_out


@router.delete("/subjects", status_code=status.HTTP_200_OK, response_model=schemas.TutorOut)
def delete_tutors_subjects(
        subjects: schemas.SubjectsCreate,
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: Session = Depends(database.get_db)
):
    if user.role == Role.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only tutors can add subjects."
        )
    for subject_id in subjects.subject_ids:
        db.query(TutorToSubject).filter(
            TutorToSubject.tutor_id == user.id,
            TutorToSubject.subject_id == subject_id
        ).delete()
    db.commit()
    tutor_subjects = (
        db.query(Subject).
        join(TutorToSubject).
        filter(TutorToSubject.tutor_id == user.id).
        all()
    )

    tutor_out = schemas.TutorOut(
        id=user.id,
        email=user.email,
        subjects=[subject.subject_name for subject in tutor_subjects]
    )

    return tutor_out


@router.get("/students", status_code=status.HTTP_200_OK, response_model=t.List[schemas.UserOut])
def get_students(
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: Session = Depends(database.get_db)
):
    if user.role == Role.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only tutors can view their students."
        )
    tutor_to_students = (
        db.query(User).
        join(
            TutorToStudent,
            User.id == TutorToStudent.student_id
        ).
        filter(TutorToStudent.tutor_id == user.id)
        .all()
    )

    return [student for student in tutor_to_students]


@router.post("/lesson", status_code=status.HTTP_201_CREATED, response_model=schemas.TutorLessonOut)
def add_lesson(
        lesson: schemas.LessonCreate,
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: Session = Depends(database.get_db)):
    if user.role == Role.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only tutors can add lessons to schedule."
        )

    new_lesson = Lesson(
        tutor_id=user.id,
        student_id=lesson.student_id,
        subject_id=lesson.subject_id,
        date_at=lesson.date_at
    )

    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return new_lesson


@router.get("/schedule", status_code=status.HTTP_200_OK, response_model=t.List[schemas.TutorLessonOut])
def get_schedule(
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: Session = Depends(database.get_db)):
    if user.role == Role.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only tutors can view schedule by their students."
        )

    schedule = db.query(Lesson).filter(Lesson.tutor_id == user.id).all()

    return [lesson for lesson in schedule]


@router.get("/schedule/{student_id}", status_code=status.HTTP_200_OK, response_model=t.List[schemas.TutorLessonOut])
def get_schedule_by_student(
        student_id: int,
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: Session = Depends(database.get_db)):
    if user.role == Role.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only tutors can view schedule by their student."
        )

    schedule_by_student = (
        db.query(Lesson).
        filter(
            Lesson.tutor_id == user.id, Lesson.student_id == student_id
        ).
        all()
    )

    return [lesson for lesson in schedule_by_student]
