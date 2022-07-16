from abc import ABC, abstractmethod
from typing import Dict, List

from sqlalchemy.ext.asyncio import AsyncSession


class FindUserCoursesCollectorInterface(ABC):
    """Find User Courses Collector Usecase Interface"""

    @abstractmethod
    async def find_user_courses(
        self, db_session: AsyncSession, user_id: int
    ) -> List[Dict]:
        """Must implement"""

        raise Exception("Must implement find_user_courses method")
