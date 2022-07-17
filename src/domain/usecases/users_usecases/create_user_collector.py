from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.pydantic_schemas.user import UserCreate


class CreateUserCollectorInterface(ABC):
    """Create User Collector Usecase Interface"""

    @abstractmethod
    async def create_user(self, db_session: AsyncSession, user: UserCreate) -> bool:
        """Must implement"""

        raise Exception("Must implement create_user method")
