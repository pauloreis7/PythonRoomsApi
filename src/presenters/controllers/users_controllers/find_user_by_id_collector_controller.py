from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.usecases.users_usecases.find_user_by_id_collector import (
    FindUserByIdCollectorInterface,
)
from src.domain.controllers.users_usecases.find_user_by_id_collector_controller import (
    FindUserByIdCollectorControllerInterface,
)


class FindUserByIdCollectorController(FindUserByIdCollectorControllerInterface):
    """Controller to find user by id usecase"""

    def __init__(
        self, find_user_by_id_collector: Type[FindUserByIdCollectorInterface]
    ) -> None:
        self.__use_case = find_user_by_id_collector

    async def handle(self, db_session: AsyncSession, user_id: int):
        """Handle to find user by id controller"""

        user = await self.__use_case.find_user_by_id(
            db_session=db_session, user_id=user_id
        )

        response = {"status_code": 200, "data": user}

        return response
