from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class FindSectionsByTitleCollectorControllerInterface(ABC):
    """Find Sections By Title Collector Controller Interface"""

    @abstractmethod
    async def handle(self, db_session: AsyncSession, sections_title: str):
        """Method to handle request"""

        raise Exception("Must implement handler method")
