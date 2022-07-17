from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.usecases.users_usecases.paginate_users_collector import (
    PaginateUsersCollectorInterface,
)
from src.domain.controllers.users_usecases.paginate_users_collector_controller import (
    PaginateUsersCollectorControllerInterface,
)


class PaginateUsersCollectorController(PaginateUsersCollectorControllerInterface):
    """Controller to paginate users usecase"""

    def __init__(
        self, paginate_users_collector: Type[PaginateUsersCollectorInterface]
    ) -> None:
        self.__use_case = paginate_users_collector

    async def handle(self, db_session: AsyncSession, skip: int = 0, limit: int = 100):
        """Handle to paginate users controller"""

        users_pagination = await self.__use_case.paginate_users(
            db_session=db_session, skip=skip, limit=limit
        )

        response = {"status_code": 200, "data": users_pagination}

        return response
