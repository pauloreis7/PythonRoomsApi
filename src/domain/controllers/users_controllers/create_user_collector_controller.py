from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from src.pydantic_schemas.user import UserCreate


class CreateUserCollectorControllerInterface(ABC):
    """Create User Collector Controller Interface"""

    @abstractmethod
    async def handle(self, db_session: AsyncSession, user: UserCreate):
        """Method to handle request"""

        raise Exception("Must implement handler method")
