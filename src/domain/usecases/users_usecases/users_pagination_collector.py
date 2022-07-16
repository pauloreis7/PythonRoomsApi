from abc import ABC, abstractmethod
from typing import Dict, List

from sqlalchemy.ext.asyncio import AsyncSession


class UsersPaginationCollectorInterface(ABC):
    """Read Users Colletor Usecase Interface"""

    @abstractmethod
    async def users_pagination(
        self, db_session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Dict]:
        """Must implement"""

        raise Exception("Must implement users_pagination method")
