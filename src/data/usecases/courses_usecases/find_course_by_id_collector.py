from typing import Type, Dict

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from src.domain.usecases.courses_usecases.find_course_by_id_collector import (
    FindCourseByIdCollectorInterface,
)
from src.data.interfaces.courses_repository import CoursesRepositoryInterface


class FindCourseByIdCollector(FindCourseByIdCollectorInterface):
    """Find Course By Id collector usecase"""

    def __init__(self, courses_repository: Type[CoursesRepositoryInterface]) -> None:
        self.__courses_repository = courses_repository

    async def find_course_by_id(self, db_session: AsyncSession, course_id: int) -> Dict:
        """
        Find course by id and return it
        :param  - db_session: ORM database session
                - course_id: Course id to find
        :returns - Dictionary with user information
        """

        api_response = await self.__courses_repository.get_course_by_id(
            db_session, course_id
        )

        if api_response is None:
            raise HTTPException(status_code=404, detail="Course not found")

        return api_response
