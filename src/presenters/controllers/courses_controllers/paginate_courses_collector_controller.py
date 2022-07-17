from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.usecases.courses_usecases.paginate_courses_collector import (
    PaginateCoursesCollectorInterface,
)
from src.domain.controllers.courses_controllers.paginate_courses_collector_controller import (
    PaginateCoursesCollectorControllerInterface,
)


class PaginateCoursesCollectorController(PaginateCoursesCollectorControllerInterface):
    """Controller to paginate courses usecase"""

    def __init__(
        self, paginate_courses_collector: Type[PaginateCoursesCollectorInterface]
    ) -> None:
        self.__use_case = paginate_courses_collector

    async def handle(self, db_session: AsyncSession, skip: int = 0, limit: int = 100):
        """Handle to paginate courses controller"""

        courses_pagination = await self.__use_case.paginate_courses(
            db_session=db_session, skip=skip, limit=limit
        )

        response = {"status_code": 200, "data": courses_pagination}

        return response
