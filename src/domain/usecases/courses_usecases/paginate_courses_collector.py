from abc import ABC, abstractmethod
from typing import Dict, List

from sqlalchemy.ext.asyncio import AsyncSession


class PaginateCoursesCollectorInterface(ABC):
    """Paginate Courses Colletor Usecase Interface"""

    @abstractmethod
    async def paginate_courses(
        self, db_session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Dict]:
        """Must implement"""

        raise Exception("Must implement paginate_courses method")
