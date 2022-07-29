from typing import List

from sqlalchemy import literal_column, select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.models.user import User
from src.pydantic_schemas.user import UserCreate, UserPatch
from src.data.interfaces.users_repository import UsersRepositoryInterface


class UsersRepository(UsersRepositoryInterface):
    """Class to users repository"""

    async def get_users(
        self, db_session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[User]:
        """Get all users list"""

        query = select(User).offset(skip).limit(limit)

        query_response = await db_session.execute(query)

        users = query_response.scalars().all()

        return users

    async def get_user_by_id(self, db_session: AsyncSession, user_id: int) -> User:
        """Get a user by id"""

        query = select(User).where(User.id == user_id)

        query_response = await db_session.execute(query)

        user = query_response.scalars().first()

        return user

    async def get_user_by_email(
        self, db_session: AsyncSession, user_email: str
    ) -> User:
        """Get a user by email"""

        query = select(User).where(User.email == user_email)

        query_response = await db_session.execute(query)

        user = query_response.scalars().first()

        return user

    async def create_db_user(self, db_session: AsyncSession, user: UserCreate) -> User:
        """Create a user"""

        query = (
            insert(User)
            .values(
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                bio=user.bio,
                role=user.role,
                is_active=user.is_active,
            )
            .returning(literal_column("*"))
        )

        query_response = await db_session.execute(query)

        await db_session.commit()

        created_user = query_response.fetchone()

        return created_user

    async def patch_db_user(
        self, db_session: AsyncSession, user_id: int, user: UserPatch
    ) -> User:
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
            .returning(literal_column("*"))
        )

        query_response = await db_session.execute(query)

        await db_session.commit()

        patched_user = query_response.fetchone()

        return patched_user

    async def delete_db_user(self, db_session: AsyncSession, user_id: int) -> None:
        """Delete a user"""

        query = delete(User).where(User.id == user_id)

        await db_session.execute(query)

        await db_session.commit()

        return
