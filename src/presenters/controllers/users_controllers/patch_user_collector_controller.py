from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from src.pydantic_schemas.user import UserPatch

from src.domain.usecases.users_usecases.patch_user_collector import (
    PatchUserCollectorInterface,
)
from src.domain.controllers.users_controllers.patch_user_collector_controller import (
    PatchUserCollectorControllerInterface,
)


class PatchUserCollectorController(PatchUserCollectorControllerInterface):
    """Controller to patch user usecase"""

    def __init__(self, patch_user_collector: Type[PatchUserCollectorInterface]) -> None:
        self.__use_case = patch_user_collector

    async def handle(self, db_session: AsyncSession, user_id: int, user: UserPatch):
        """Handle to patch user controller"""

        await self.__use_case.patch_user(
            db_session=db_session, user_id=user_id, user=user
        )

        response = {"status_code": 204, "data": None}

        return response
