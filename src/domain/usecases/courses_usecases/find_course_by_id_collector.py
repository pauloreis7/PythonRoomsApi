from abc import ABC, abstractmethod
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession


class FindCourseByIdCollectorInterface(ABC):
    """Find Course By Id Collector Usecase Interface"""

    @abstractmethod
    async def find_course_by_id(self, db_session: AsyncSession, course_id: int) -> Dict:
        """Must implement"""

        raise Exception("Must implement find_course_by_id method")
