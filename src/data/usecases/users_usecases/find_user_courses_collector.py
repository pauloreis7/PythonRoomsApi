from typing import Type, Dict, List

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from src.domain.usecases.users_usecases.find_user_courses_collector import (
    FindUserCoursesCollectorInterface,
)
from src.data.interfaces.users_repository import UsersRepositoryInterface
from src.data.interfaces.courses_repository import CoursesRepositoryInterface


class FindUserCoursesCollector(FindUserCoursesCollectorInterface):
    """Find User Courses By Id collector usecase"""

    def __init__(
        self,
        users_repository: Type[UsersRepositoryInterface],
        courses_repository: Type[CoursesRepositoryInterface],
    ) -> None:
        self.__users_repository = users_repository
        self.__courses_repository = courses_repository

    async def find_user_courses(
        self, db_session: AsyncSession, user_id: int
    ) -> List[Dict]:
        """
        Find user courses by id and return courses list
        :param  - db_session: ORM database session
                - user_id: User id to find courses
        :returns - List with all user courses information
        """

        check_user_exists = await self.__users_repository.get_user_by_id(
            db_session, user_id=user_id
        )

        if check_user_exists is None:
            raise HTTPException(status_code=404, detail="User not found")

        api_response = await self.__courses_repository.get_user_courses(
            db_session, user_id
        )

        return api_response
