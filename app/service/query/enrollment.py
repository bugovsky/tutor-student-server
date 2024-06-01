from typing import Sequence

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, TutorToStudentRequest
from app.schemas import Status


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
