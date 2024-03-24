from typing import Sequence

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User, LessonRequest, TutorToStudentRequest, TutorToStudent
from ..schemas import Status


async def add_enrollment_request(db: AsyncSession, student_id, tutor_id):
    tutor_to_student_request = TutorToStudentRequest(
        tutor_id=tutor_id,
        student_id=student_id,
        status=Status.pending
    )
    db.add(tutor_to_student_request)
    await db.commit()
    await db.refresh(tutor_to_student_request)


async def get_students_to_enroll(db: AsyncSession, tutor_id: int) -> Sequence[User]:
    query = (
        select(User).join(TutorToStudentRequest, and_(
            TutorToStudentRequest.student_id == User.id,
            TutorToStudentRequest.tutor_id == tutor_id,
            TutorToStudentRequest.status == Status.pending))
    )
    result = await db.execute(query)
    return result.scalars().all()


async def get_enrollment_request_by_student_id(
        db: AsyncSession, tutor_id: int,
        student_id: int
) -> TutorToStudentRequest:
    query = select(TutorToStudentRequest).where(
        TutorToStudentRequest.student_id == student_id,
        TutorToStudentRequest.tutor_id == tutor_id,
        TutorToStudentRequest.status == Status.pending)
    result = await db.execute(query)
    return result.scalars().first()


async def update_enrollment_request(db: AsyncSession, enrollment_request: TutorToStudentRequest,
                                    status: Status) -> None:
    enrollment_request.status = status
    if status == Status.accepted:
        tutor_to_student = TutorToStudent(tutor_id=enrollment_request.tutor_id,
                                          student_id=enrollment_request.student_id)
        db.add(tutor_to_student)
    await db.commit()
