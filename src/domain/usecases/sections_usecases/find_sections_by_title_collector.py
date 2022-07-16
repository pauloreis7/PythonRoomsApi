from abc import ABC, abstractmethod
from typing import List, Dict

from sqlalchemy.ext.asyncio import AsyncSession


class FindSectionsByTitleCollectorInterface(ABC):
    """Find Sections By Title Collector Usecase Interface"""

    @abstractmethod
    async def find_sections_by_title(
        self, db_session: AsyncSession, sections_title: str
    ) -> List[Dict]:
        """Must implement"""

        raise Exception("Must implement find_sections_by_title method")
