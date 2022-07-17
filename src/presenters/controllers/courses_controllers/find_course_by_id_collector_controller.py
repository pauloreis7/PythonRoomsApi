from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.usecases.courses_usecases.find_course_by_id_collector import (
    FindCourseByIdCollectorInterface,
)
from src.domain.controllers.courses_controllers.find_course_by_id_collector_controller import (
    FindCourseByIdCollectorControllerInterface,
)


class FindCourseByIdCollectorController(FindCourseByIdCollectorControllerInterface):
    """Controller to find course by id usecase"""

    def __init__(
        self, find_course_by_id_collector: Type[FindCourseByIdCollectorInterface]
    ) -> None:
        self.__use_case = find_course_by_id_collector

    async def handle(self, db_session: AsyncSession, course_id: int):
        """Handle to find course by id controller"""

        course = await self.__use_case.find_course_by_id(
            db_session=db_session, course_id=course_id
        )

        response = {"status_code": 200, "data": course}

        return response
