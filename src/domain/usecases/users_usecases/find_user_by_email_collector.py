from abc import ABC, abstractmethod
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession


class FindUserByEmailCollectorInterface(ABC):
    """Find User By Email Collector Usecase Interface"""

    @abstractmethod
    async def find_user_by_email(
        self, db_session: AsyncSession, user_email: str
    ) -> Dict:
        """Must implement"""

        raise Exception("Must implement find_user_by_email method")
