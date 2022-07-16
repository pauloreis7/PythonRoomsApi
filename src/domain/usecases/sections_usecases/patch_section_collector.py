from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from src.pydantic_schemas.sections import SectionPatch


class PatchSectionCollectorInterface(ABC):
    """Patch Section Collector Usecase Interface"""

    @abstractmethod
    async def patch_section(
        self, db_session: AsyncSession, section_id: int, section: SectionPatch
    ) -> None:
        """Must implement"""

        raise Exception("Must implement patch_section method")
