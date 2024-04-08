from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.service import users
from app.database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    user_by_email = await users.get_user_by_email(db, email=user.email)
    if user_by_email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Данная почта уже зарегестрирована")
    new_user = await users.create_user(db, user=user)
    return new_user


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user_by_id = await users.get_user_by_id(db, user_id=user_id)
    if not user_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Пользователь с id: {user_id} не найден")

    return user_by_id

@router.get('/subject/{lesson_id}', status_code=status.HTTP_200_OK, response_model=schemas.SubjectOut)
async def get_subject_by_lesson(lesson_id: int, db: AsyncSession = Depends(get_db)):
    subject_by_id = await users.get_subject_by_lesson_id(db, lesson_id=lesson_id)
    return subject_by_id

