from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.pydantic_schemas.user import User


class PaginateUsersCollectorInterface(ABC):
    """Paginate Users Colletor Usecase Interface"""

    @abstractmethod
    async def paginate_users(
        self, db_session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[User]:
        """Must implement"""

        raise Exception("Must implement paginate_users method")
