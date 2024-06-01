import typing as t

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .. import database, schemas, oauth2
from ..schemas import Role
from ..service.query import students

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


@router.post("/tutors", status_code=status.HTTP_200_OK, response_model=t.List[schemas.TutorOut])
async def get_tutors_to_add(
        subjects: schemas.SubjectsCreate,
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: AsyncSession = Depends(database.get_db)
):
    if user.role == Role.tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только студенты могут искать репетиторов"
        )

    if len(subjects.subject_ids) == 0:
        rows =await students.get_all_tutors(db)
    else:
        rows = await students.get_all_tutors_by_subjects(db, subject_ids=subjects.subject_ids)
    tutors = {}
    for row in rows:
        tutor_id, first_name, last_name, subject_name = row.id, row.firstname, row.lastname, row.subject_name
        if tutor_id not in tutors:
            tutors[tutor_id] = {'firstname': first_name, 'lastname': last_name, 'subjects': []}
        tutors[tutor_id]['subjects'].append(subject_name)

    tutors_out = []
    for tutor_id, tutor_info in tutors.items():
        tutor_out = schemas.TutorOut(
            id=tutor_id,
            firstname=tutor_info['firstname'],
            lastname=tutor_info['lastname'],
            subjects=tutor_info["subjects"]
        )
        tutors_out.append(tutor_out)
    return tutors_out

@router.get("/tutors", status_code=status.HTTP_200_OK, response_model=t.List[schemas.UserOut])
async def get_tutors(
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: AsyncSession = Depends(database.get_db)
):
    if user.role == Role.tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только ученики могут просматривать своих репетиторов"
        )
    tutors = await students.get_tutors(db, student_id=user.id)

    return [tutor for tutor in tutors]