from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.sections import SectionCreate


class CreateSectionCollectorInterface(ABC):
    """Create Section Collector Usecase Interface"""

    @abstractmethod
    async def create_section(
        self, db_session: AsyncSession, section: SectionCreate
    ) -> bool:
        """Must implement"""

        raise Exception("Must implement create_section method")
