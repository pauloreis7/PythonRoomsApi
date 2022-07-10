from sqlalchemy import select, insert, update, delete

from database.models.user import User
from api.config.connection import session
from pydantic_schemas.user import UserCreate, UserPatch


async def get_user_by_id(user_id: int):
    """Get a user by id"""

    async with session() as db_session:
        query = select(User).where(User.id == user_id)

        query_response = await db_session.execute(query)

        user = query_response.scalars().first()

        return user


async def get_user_by_email(email: str):
    """Get a user by email"""

    async with session() as db_session:
        query = select(User).where(User.email == email)

        query_response = await db_session.execute(query)

        user = query_response.scalars().first()

        return user


async def get_users(skip: int = 0, limit: int = 100):
    """Get all users list"""

    async with session() as db_session:
        query = select(User).offset(skip).limit(limit)

        query_response = await db_session.execute(query)

        users = query_response.scalars().all()

        return users


async def create_db_user(user: UserCreate):
    """Create a user"""

    async with session() as db_session:
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


async def patch_db_user(user_id: int, user: UserPatch):
    """Patch a user"""

    async with session() as db_session:
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


async def delete_db_user(user_id: int):
    """Delete a user"""

    async with session() as db_session:
        query = delete(User).where(User.id == user_id)

        await db_session.execute(query)

        await db_session.commit()

        return
