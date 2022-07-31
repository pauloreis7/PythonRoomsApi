from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.user import UserPatch


class PatchUserCollectorInterface(ABC):
    """Patch User Collector Usecase Interface"""

    @abstractmethod
    async def patch_user(
        self, db_session: AsyncSession, user_id: int, user: UserPatch
    ) -> None:
        """Must implement"""

        raise Exception("Must implement patch_user method")
