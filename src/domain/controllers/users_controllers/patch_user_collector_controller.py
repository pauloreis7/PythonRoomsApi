from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.pydantic_schemas.user import UserPatch


class PatchUserCollectorControllerInterface(ABC):
    """Patch User Collector Controller Interface"""

    @abstractmethod
    async def handle(self, db_session: AsyncSession, user_id: int, user: UserPatch):
        """Method to handle request"""

        raise Exception("Must implement handler method")
