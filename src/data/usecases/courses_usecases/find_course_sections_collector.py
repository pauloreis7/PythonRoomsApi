from typing import Type, List

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.sections import Section
from src.domain.usecases.courses_usecases.find_course_sections_collector import (
    FindCourseSectionsCollectorInterface,
)
from src.data.interfaces.courses_repository import CoursesRepositoryInterface
from src.data.interfaces.sections_repository import SectionsRepositoryInterface
from src.errors.http_request_error import HttpRequestError


class FindCourseSectionsCollector(FindCourseSectionsCollectorInterface):
    """Find Course Sections collector usecase"""

    def __init__(
        self,
        courses_repository: Type[CoursesRepositoryInterface],
        sections_repository: Type[SectionsRepositoryInterface],
    ) -> None:
        self.__courses_repository = courses_repository
        self.__sections_repository = sections_repository

    async def find_course_sections(
        self, db_session: AsyncSession, course_id: str
    ) -> List[Section]:
        """
        Find course by id and return sections list
        :param  - db_session: ORM database session
                - course_id: Course id to find courses
        :returns - List with all course sections information
        """

        check_course_exists = await self.__courses_repository.get_course_by_id(
            db_session, course_id
        )

        if check_course_exists is None:
            raise HttpRequestError(status_code=404, detail="Course not found")

        api_response = await self.__sections_repository.get_course_sections(
            db_session, course_id
        )

        return api_response
