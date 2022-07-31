from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.sections import SectionCreate


class CreateSectionCollectorControllerInterface(ABC):
    """Create Section Collector Controller Interface"""

    @abstractmethod
    async def handle(self, db_session: AsyncSession, section: SectionCreate):
        """Method to handle request"""

        raise Exception("Must implement handler method")
