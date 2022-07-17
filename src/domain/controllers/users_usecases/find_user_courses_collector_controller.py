from abc import ABC, abstractmethod
from typing import Dict, List

from sqlalchemy.ext.asyncio import AsyncSession


class FindUserCoursesCollectorControllerInterface(ABC):
    """Find User Courses Collector Controller Interface"""

    @abstractmethod
    async def handle(self, db_session: AsyncSession, user_id: int) -> List[Dict]:
        """Method to handle request"""

        raise Exception("Must implement handler method")
