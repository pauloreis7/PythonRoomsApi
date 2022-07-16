from abc import ABC, abstractmethod
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession


class FindUserByIdCollectorInterface(ABC):
    """Find User By Id Collector Usecase Interface"""

    @abstractmethod
    async def find_user_by_id(self, db_session: AsyncSession, user_id: int) -> Dict:
        """Must implement"""

        raise Exception("Must implement find_user_by_id method")
