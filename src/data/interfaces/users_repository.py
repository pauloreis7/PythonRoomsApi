from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.user import UserCreate, UserPatch
from src.infra.models.user import User


class UsersRepositoryInterface(ABC):
    """Users Repository Interface"""

    @abstractmethod
    async def get_users(
        self, db_session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[User]:
        """Must implement"""

        raise Exception("Must implement get_users method")

    @abstractmethod
    async def get_user_by_id(self, db_session: AsyncSession, user_id: int) -> User:
        """Must implement"""

        raise Exception("Must implement get_user_by_id method")

    @abstractmethod
    async def get_user_by_email(
        self, db_session: AsyncSession, user_email: str
    ) -> User:
        """Must implement"""

        raise Exception("Must implement get_user_by_email method")

    @abstractmethod
    async def create_db_user(self, db_session: AsyncSession, user: UserCreate) -> User:
        """Must implement"""

        raise Exception("Must implement create_db_user method")

    @abstractmethod
    async def patch_db_user(
        self, db_session: AsyncSession, user_id: int, user: UserPatch
    ) -> User:
        """Must implement"""

        raise Exception("Must implement patch_db_user method")

    @abstractmethod
    async def delete_db_user(self, db_session: AsyncSession, user_id: int) -> None:
        """Must implement"""

        raise Exception("Must implement delete_db_user method")
