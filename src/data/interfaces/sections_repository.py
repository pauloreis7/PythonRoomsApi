from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.sections import SectionCreate, SectionPatch
from src.infra.models.course import Section


class SectionsRepositoryInterface(ABC):
    """Sections Repository Interface"""

    @abstractmethod
    async def get_section_by_id(
        self, db_session: AsyncSession, section_id: int
    ) -> Section:
        """Must implement"""

        raise Exception("Must implement get_section_by_id method")

    @abstractmethod
    async def get_sections_by_title(
        self, db_session: AsyncSession, sections_title: str
    ) -> List[Section]:
        """Must implement"""

        raise Exception("Must implement get_sections_by_title method")

    @abstractmethod
    async def get_course_sections(
        self, db_session: AsyncSession, course_id: str
    ) -> List[Section]:
        """Must implement"""

        raise Exception("Must implement get_course_sections method")

    @abstractmethod
    async def create_db_section(
        self, db_session: AsyncSession, section: SectionCreate
    ) -> Section:
        """Must implement"""

        raise Exception("Must implement create_db_section method")

    @abstractmethod
    async def patch_db_section(
        self, db_session: AsyncSession, section_id: int, section: SectionPatch
    ) -> Section:
        """Must implement"""

        raise Exception("Must implement patch_db_section method")

    @abstractmethod
    async def delete_db_section(
        self, db_session: AsyncSession, section_id: int
    ) -> None:
        """Must implement"""

        raise Exception("Must implement delete_db_section method")
