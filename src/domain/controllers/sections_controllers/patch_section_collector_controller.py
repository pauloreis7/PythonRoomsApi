from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.pydantic_schemas.sections import SectionPatch


class PatchSectionCollectorControllerInterface(ABC):
    """Patch Section Collector Controller Interface"""

    @abstractmethod
    async def handle(
        self, db_session: AsyncSession, section_id: int, section: SectionPatch
    ):
        """Method to handle request"""

        raise Exception("Must implement handler method")
