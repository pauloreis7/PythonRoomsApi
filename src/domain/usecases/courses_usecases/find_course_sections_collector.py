from abc import ABC, abstractmethod
from typing import Dict, List

from sqlalchemy.ext.asyncio import AsyncSession


class FindCourseSectionsCollectorInterface(ABC):
    """Find Course Sections Collector Usecase Interface"""

    @abstractmethod
    async def find_course_sections(
        self, db_session: AsyncSession, course_id: str
    ) -> List[Dict]:
        """Must implement"""

        raise Exception("Must implement find_course_sections method")
