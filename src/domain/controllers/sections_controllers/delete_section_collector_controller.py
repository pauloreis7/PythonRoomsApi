from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class DeleteSectionCollectorControllerInterface(ABC):
    """Delete Section Collector Controller Interface"""

    @abstractmethod
    async def handle(self, db_session: AsyncSession, section_id: int):
        """Method to handle request"""

        raise Exception("Must implement handler method")
