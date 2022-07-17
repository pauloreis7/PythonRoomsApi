from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.pydantic_schemas.course import CoursePatch
from src.domain.usecases.courses_usecases.patch_course_collector import (
    PatchCourseCollectorInterface,
)
from src.data.interfaces.users_repository import UsersRepositoryInterface
from src.data.interfaces.courses_repository import CoursesRepositoryInterface
from src.errors.http_request_error import HttpRequestError


class PatchCourseCollector(PatchCourseCollectorInterface):
    """Patch Course collector usecase"""

    def __init__(
        self,
        courses_repository: Type[CoursesRepositoryInterface],
        users_repository: Type[UsersRepositoryInterface],
    ) -> None:
        self.__courses_repository = courses_repository
        self.__users_repository = users_repository

    async def patch_course(
        self, db_session: AsyncSession, course_id: int, course: CoursePatch
    ) -> None:
        """
        Patch course model
        :param  - db_session: ORM database session
                - course: Course data for patch
        :returns - None for patch course event status
        """

        check_course_exists = await self.__courses_repository.get_course_by_id(
            db_session, course_id=course_id
        )

        if check_course_exists is None:
            raise HttpRequestError(status_code=404, detail="Course not found")

        check_course_name_already_exists = (
            await self.__courses_repository.get_course_by_title(
                db_session, course_title=course.title
            )
        )

        if (
            check_course_name_already_exists
            and check_course_name_already_exists.id is not course_id
        ):
            raise HttpRequestError(status_code=400, detail="Name already in use!")

        check_user_exists = await self.__users_repository.get_user_by_id(
            db_session, user_id=course.user_id
        )

        if check_user_exists is None:
            raise HttpRequestError(status_code=404, detail="User not found")

        if check_user_exists.role != 1:
            raise HttpRequestError(
                status_code=400, detail="Only a teacher user can have a course!"
            )

        await self.__courses_repository.patch_db_course(db_session, course_id, course)

        return
