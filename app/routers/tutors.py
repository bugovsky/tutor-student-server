import typing as t

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .. import database, schemas, oauth2
from ..schemas import Role
from ..service.query import tutors
from app.utils.redis import RedisHandler

router = APIRouter(prefix="/tutors", tags=['Tutors'])


@router.post("/subjects", status_code=status.HTTP_200_OK, response_model=schemas.TutorOut)
async def add_subjects_to_tutor(
        subjects: schemas.SubjectsCreate,
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: AsyncSession = Depends(database.get_db)
):
    if user.role == Role.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Студенты не могут добавлять предметы"
        )
    for subject_id in subjects.subject_ids:
        await tutors.add_subject(db, tutor_id=user.id, subject_id=subject_id)
    subject_names = [
        await tutors.get_subject_name_by_id(db, subject_id=subject_id)
        for subject_id in subjects.subject_ids
    ]

    tutor_out = schemas.TutorOut(
        id=user.id,
        firstname=user.firstname,
        lastname=user.lastname,
        subjects=subject_names
    )
    return tutor_out


@router.delete("/subjects", status_code=status.HTTP_200_OK, response_model=schemas.TutorOut)
async def delete_tutors_subjects(
        subjects: schemas.SubjectsCreate,
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: AsyncSession = Depends(database.get_db)
):
    if user.role == Role.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Студенты не могут удалять предметы"
        )
    for subject_id in subjects.subject_ids:
        await tutors.delete_subject(db, tutor_id=user.id, subject_id=subject_id)
    subject_names = [
        subject.subject_name
        for subject in
        await tutors.get_subjects_by_tutor_id(db, user.id)
    ]

    tutor_out = schemas.TutorOut(
        id=user.id,
        firstname=user.firstname,
        lastname=user.lastname,
        subjects=subject_names
    )
    return tutor_out


@router.get("/students", status_code=status.HTTP_200_OK, response_model=t.List[schemas.UserOut])
async def get_students(
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: AsyncSession = Depends(database.get_db)
):
    if user.role == Role.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только репетиторы могут просматривать своих студентов"
        )
    students = await tutors.get_students(db, tutor_id=user.id)

    return [student for student in students]


@router.post("/lesson", status_code=status.HTTP_201_CREATED, response_model=schemas.LessonOut)
async def add_lesson(
        lesson: schemas.LessonCreate,
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: AsyncSession = Depends(database.get_db)):
    if user.role == Role.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только репетиторы могут редактировать расписание"
        )
    new_lesson = await tutors.add_lesson(db, lesson=lesson, tutor_id=user.id)
    return new_lesson


@router.get("/schedule", status_code=status.HTTP_200_OK, response_model=t.List[schemas.LessonOut])
async def get_schedule(
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: AsyncSession = Depends(database.get_db)):
    if user.role == Role.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ученик не может просматривать расписание репетитора"
        )

    redis_handler = RedisHandler()
    cached_schedule = await redis_handler.get(key=f"schedule_{user.id}")
    if cached_schedule:
        return redis_handler.deserialize_schedule(cached_schedule)

    schedule = await tutors.get_schedule(db, user.id)
    await redis_handler.set(f"schedule_{user.id}", redis_handler.serialize_schedule(schedule), ex=3600)

    return [lesson for lesson in schedule]


@router.get("/schedule/{student_id}",
            status_code=status.HTTP_200_OK,
            response_model=t.List[schemas.LessonOut])
async def get_schedule_by_student(
        student_id: int,
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: AsyncSession = Depends(database.get_db)):
    if user.role == Role.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ученик не может просматривать расписание репетитора"
        )
    schedule_by_student = await tutors.get_schedule_by_student(db, tutor_id=user.id, student_id=student_id)
    return [lesson for lesson in schedule_by_student]
