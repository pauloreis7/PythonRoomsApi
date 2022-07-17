from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.usecases.users_usecases.delete_user_collector import (
    DeleteUserCollectorInterface,
)
from src.domain.controllers.users_controllers.delete_user_collector_controller import (
    DeleteUserCollectorControllerInterface,
)


class DeleteUserCollectorController(DeleteUserCollectorControllerInterface):
    """Controller to delete user usecase"""

    def __init__(
        self, delete_user_collector: Type[DeleteUserCollectorInterface]
    ) -> None:
        self.__use_case = delete_user_collector

    async def handle(self, db_session: AsyncSession, user_id: int):
        """Handle to delete user controller"""

        await self.__use_case.delete_user(db_session=db_session, user_id=user_id)

        response = {"status_code": 204, "data": None}

        return response
