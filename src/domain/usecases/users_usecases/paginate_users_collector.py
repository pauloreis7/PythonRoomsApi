from abc import ABC, abstractmethod
from typing import Dict, List

from sqlalchemy.ext.asyncio import AsyncSession


class PaginateUsersCollectorInterface(ABC):
    """Paginate Users Colletor Usecase Interface"""

    @abstractmethod
    async def paginate_users(
        self, db_session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Dict]:
        """Must implement"""

        raise Exception("Must implement users_pagination method")
