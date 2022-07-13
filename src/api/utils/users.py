from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.user import User
from src.pydantic_schemas.user import UserCreate, UserPatch


async def get_users(db_session: AsyncSession, skip: int = 0, limit: int = 100):
    """Get all users list"""

    query = select(User).offset(skip).limit(limit)

    query_response = await db_session.execute(query)

    users = query_response.scalars().all()

    return users


async def get_user_by_id(db_session: AsyncSession, user_id: int):
    """Get a user by id"""

    query = select(User).where(User.id == user_id)

    query_response = await db_session.execute(query)

    user = query_response.scalars().first()

    return user


async def get_user_by_email(db_session: AsyncSession, user_email: str):
    """Get a user by email"""

    query = select(User).where(User.email == user_email)

    query_response = await db_session.execute(query)

    user = query_response.scalars().first()

    return user


async def create_db_user(db_session: AsyncSession, user: UserCreate):
    """Create a user"""

    query = insert(User).values(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        bio=user.bio,
        role=user.role,
        is_active=user.is_active,
    )

    await db_session.execute(query)

    await db_session.commit()

    return True


async def patch_db_user(db_session: AsyncSession, user_id: int, user: UserPatch):
    """Patch a user"""

    query = (
        update(User)
        .where(User.id == user_id)
        .values(
            email=user.email,
            role=user.role,
            first_name=user.first_name,
            last_name=user.last_name,
            bio=user.bio,
        )
    )

    await db_session.execute(query)

    await db_session.commit()

    return


async def delete_db_user(db_session: AsyncSession, user_id: int):
    """Delete a user"""

    query = delete(User).where(User.id == user_id)

    await db_session.execute(query)

    await db_session.commit()

    return
