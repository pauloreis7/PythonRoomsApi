from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.usecases.courses_usecases.delete_course_collector import (
    DeleteCourseCollectorInterface,
)
from src.data.interfaces.courses_repository import CoursesRepositoryInterface
from src.errors.http_request_error import HttpRequestError


class DeleteCourseCollector(DeleteCourseCollectorInterface):
    """Delete Course collector usecase"""

    def __init__(self, courses_repository: Type[CoursesRepositoryInterface]) -> None:
        self.__courses_repository = courses_repository

    async def delete_course(self, db_session: AsyncSession, course_id: int) -> None:
        """
        Delete course model
        :param  - db_session: ORM database session
                - course_id: Course id for delete
        :returns - None for delete course event status
        """

        check_course_exists = await self.__courses_repository.get_course_by_id(
            db_session, course_id
        )

        if check_course_exists is None:
            raise HttpRequestError(status_code=404, detail="Course not found")

        await self.__courses_repository.delete_db_course(db_session, course_id)

        return
