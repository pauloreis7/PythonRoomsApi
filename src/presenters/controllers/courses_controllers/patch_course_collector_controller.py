from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.pydantic_schemas.course import CoursePatch
from src.domain.usecases.courses_usecases.patch_course_collector import (
    PatchCourseCollectorInterface,
)
from src.domain.controllers.courses_controllers.patch_course_collector_controller import (
    PatchCourseCollectorControllerInterface,
)


class PatchCourseCollectorController(PatchCourseCollectorControllerInterface):
    """Controller to patch course usecase"""

    def __init__(
        self, patch_course_collector: Type[PatchCourseCollectorInterface]
    ) -> None:
        self.__use_case = patch_course_collector

    async def handle(
        self, db_session: AsyncSession, course_id: int, course: CoursePatch
    ):
        """Handle to patch course controller"""

        await self.__use_case.patch_course(
            db_session=db_session, course_id=course_id, course=course
        )

        response = {"status_code": 204, "data": None}

        return response
