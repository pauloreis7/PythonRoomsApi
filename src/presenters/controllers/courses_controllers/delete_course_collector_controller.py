from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.usecases.courses_usecases.delete_course_collector import (
    DeleteCourseCollectorInterface,
)
from src.domain.controllers.courses_controllers.delete_course_collector_controller import (
    DeleteCourseCollectorControllerInterface,
)


class DeleteCourseCollectorController(DeleteCourseCollectorControllerInterface):
    """Controller to delete course usecase"""

    def __init__(
        self, delete_course_collector: Type[DeleteCourseCollectorInterface]
    ) -> None:
        self.__use_case = delete_course_collector

    async def handle(self, db_session: AsyncSession, course_id: int):
        """Handle to delete course controller"""

        await self.__use_case.delete_course(db_session=db_session, course_id=course_id)

        response = {"status_code": 204, "data": None}

        return response
