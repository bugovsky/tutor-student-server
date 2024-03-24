from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import security
from app.models import User
from app.schemas import UserCreate


async def get_user_by_email(db: AsyncSession, email: str) -> User:
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalars().first()


async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    return result.scalars().first()


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    user.password = security.generate_hash(user.password)
    db_user = User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
