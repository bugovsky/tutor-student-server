from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import security
from app.models import User
from app.schemas import UserCreate


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    user.password = security.generate_hash(user.password)
    db_user = User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
