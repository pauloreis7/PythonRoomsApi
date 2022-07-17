from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class FindSectionByIdCollectorControllerInterface(ABC):
    """Find Section By Id Collector Controller Interface"""

    @abstractmethod
    async def handle(self, db_session: AsyncSession, section_id: int):
        """Method to handle request"""

        raise Exception("Must implement handler method")
