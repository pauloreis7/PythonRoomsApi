from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.course import CourseCreate
from src.domain.usecases.courses_usecases.create_course_collector import (
    CreateCourseCollectorInterface,
)
from src.domain.controllers.courses_controllers.create_course_collector_controller import (
    CreateCourseCollectorControllerInterface,
)


class CreateCourseCollectorController(CreateCourseCollectorControllerInterface):
    """Controller to create course usecase"""

    def __init__(
        self, create_course_collector: Type[CreateCourseCollectorInterface]
    ) -> None:
        self.__use_case = create_course_collector

    async def handle(self, db_session: AsyncSession, course: CourseCreate):
        """Handle to create course controller"""

        await self.__use_case.create_course(db_session=db_session, course=course)

        response = {"status_code": 201, "data": True}

        return response
