from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.models.user import UserCreate

from src.domain.usecases.users_usecases.create_user_collector import (
    CreateUserCollectorInterface,
)
from src.domain.controllers.users_controllers.create_user_collector_controller import (
    CreateUserCollectorControllerInterface,
)


class CreateUserCollectorController(CreateUserCollectorControllerInterface):
    """Controller to create user usecase"""

    def __init__(
        self, create_user_collector: Type[CreateUserCollectorInterface]
    ) -> None:
        self.__use_case = create_user_collector

    async def handle(self, db_session: AsyncSession, user: UserCreate):
        """Handle to create user controller"""

        await self.__use_case.create_user(db_session=db_session, user=user)

        response = {"status_code": 201, "data": True}

        return response
