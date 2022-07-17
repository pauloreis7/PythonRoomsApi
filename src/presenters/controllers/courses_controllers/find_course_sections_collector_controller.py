from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.usecases.courses_usecases.find_course_sections_collector import (
    FindCourseSectionsCollectorInterface,
)
from src.domain.controllers.courses_controllers.find_course_sections_collector_controller import (
    FindCourseSectionsCollectorControllerInterface,
)


class FindCourseSectionsCollectorController(
    FindCourseSectionsCollectorControllerInterface
):
    """Controller to find course sections usecase"""

    def __init__(
        self, find_course_sections_collector: Type[FindCourseSectionsCollectorInterface]
    ) -> None:
        self.__use_case = find_course_sections_collector

    async def handle(self, db_session: AsyncSession, course_id: str):
        """Handle to find course sections controller"""

        course_sections = await self.__use_case.find_course_sections(
            db_session=db_session, course_id=course_id
        )

        response = {"status_code": 200, "data": course_sections}

        return response
