from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class DeleteUserCollectorInterface(ABC):
    """Delete User Collector Usecase Interface"""

    @abstractmethod
    async def delete_user(self, db_session: AsyncSession, user_id: int) -> None:
        """Must implement"""

        raise Exception("Must implement delete_user method")
