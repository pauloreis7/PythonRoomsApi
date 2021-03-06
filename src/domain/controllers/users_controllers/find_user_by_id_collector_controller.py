from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class FindUserByIdCollectorControllerInterface(ABC):
    """Find User By Id Collector Controller Interface"""

    @abstractmethod
    async def handle(self, db_session: AsyncSession, user_id: int):
        """Method to handle request"""

        raise Exception("Must implement handler method")
