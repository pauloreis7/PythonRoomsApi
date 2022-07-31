from typing import Type, List

from sqlalchemy.ext.asyncio import AsyncSession

from src.pydantic_schemas.course import Course
from src.domain.usecases.courses_usecases.paginate_courses_collector import (
    PaginateCoursesCollectorInterface,
)
from src.data.interfaces.courses_repository import CoursesRepositoryInterface


class PaginateCoursesCollector(PaginateCoursesCollectorInterface):
    """Paginate Courses collector usecase"""

    def __init__(self, courses_repository: Type[CoursesRepositoryInterface]) -> None:
        self.__courses_repository = courses_repository

    async def paginate_courses(
        self, db_session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Course]:
        """
        Read courses and return pagination
        :param  - db_session: ORM database session
                - skip: Pagination skip item
                - limit: Pagination limit item
        :returns - List with all courses information
        """

        api_response = await self.__courses_repository.get_courses(
            db_session, skip, limit
        )

        return api_response
