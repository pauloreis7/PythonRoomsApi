from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.pydantic_schemas.course import Course, CourseCreate
from src.domain.usecases.courses_usecases.create_course_collector import (
    CreateCourseCollectorInterface,
)
from src.data.interfaces.users_repository import UsersRepositoryInterface
from src.data.interfaces.courses_repository import CoursesRepositoryInterface
from src.errors.http_request_error import HttpRequestError


class CreateCourseCollector(CreateCourseCollectorInterface):
    """Create Course collector usecase"""

    def __init__(
        self,
        courses_repository: Type[CoursesRepositoryInterface],
        users_repository: Type[UsersRepositoryInterface],
    ) -> None:
        self.__courses_repository = courses_repository
        self.__users_repository = users_repository

    async def create_course(
        self, db_session: AsyncSession, course: CourseCreate
    ) -> Course:
        """
        Create course model
        :param  - db_session: ORM database session
                - course: Course data for create
        :returns - Boolean for create course event status
        """

        check_course_exists = await self.__courses_repository.get_course_by_title(
            db_session, course_title=course.title
        )

        if check_course_exists:
            raise HttpRequestError(status_code=400, detail="Course already exists!")

        check_user_exists = await self.__users_repository.get_user_by_id(
            db_session, user_id=course.user_id
        )

        if check_user_exists is None:
            raise HttpRequestError(status_code=404, detail="User not found")

        if check_user_exists.role != 1:
            raise HttpRequestError(
                status_code=400, detail="Only a teacher user can create a course!"
            )

        api_response = await self.__courses_repository.create_db_course(
            db_session, course
        )

        return api_response
