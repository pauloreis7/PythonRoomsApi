from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class PaginateUsersCollectorControllerInterface(ABC):
    """Paginate Users Colletor Controller Interface"""

    @abstractmethod
    async def handle(self, db_session: AsyncSession, skip: int = 0, limit: int = 100):
        """Method to handle request"""

        raise Exception("Must implement handler method")
