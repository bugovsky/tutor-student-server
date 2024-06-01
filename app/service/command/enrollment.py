from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TutorToStudentRequest, TutorToStudent
from app.schemas import Status


async def add_enrollment_request(db: AsyncSession, student_id, tutor_id):
    tutor_to_student_request = TutorToStudentRequest(
        tutor_id=tutor_id,
        student_id=student_id,
        status=Status.pending
    )
    db.add(tutor_to_student_request)
    await db.commit()
    await db.refresh(tutor_to_student_request)


async def update_enrollment_request(db: AsyncSession, enrollment_request: TutorToStudentRequest,
                                    status: Status) -> None:
    enrollment_request.status = status
    if status == Status.accepted:
        tutor_to_student = TutorToStudent(tutor_id=enrollment_request.tutor_id,
                                          student_id=enrollment_request.student_id)
        db.add(tutor_to_student)
    await db.commit()
