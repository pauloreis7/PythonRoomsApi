from abc import ABC, abstractmethod
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession


class FindSectionByIdCollectorInterface(ABC):
    """Find Section By Id Collector Usecase Interface"""

    @abstractmethod
    async def find_section_by_id(
        self, db_session: AsyncSession, section_id: int
    ) -> Dict:
        """Must implement"""

        raise Exception("Must implement find_section_by_id method")
