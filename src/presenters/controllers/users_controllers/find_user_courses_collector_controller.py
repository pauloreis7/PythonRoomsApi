from typing import Type


from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.usecases.users_usecases.find_user_courses_collector import (
    FindUserCoursesCollectorInterface,
)
from src.domain.controllers.users_usecases.find_user_courses_collector_controller import (
    FindUserCoursesCollectorControllerInterface,
)


class FindUserCoursesCollectorController(FindUserCoursesCollectorControllerInterface):
    """Controller to find user courses usecase"""

    def __init__(
        self, find_user_courses_collector: Type[FindUserCoursesCollectorInterface]
    ) -> None:
        self.__use_case = find_user_courses_collector

    async def handle(self, db_session: AsyncSession, user_id: int):
        """Handle to find user courses controller"""

        user_courses = await self.__use_case.find_user_courses(
            db_session=db_session, user_id=user_id
        )

        response = {"status_code": 200, "data": user_courses}

        return response
