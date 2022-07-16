from typing import Type, List, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.usecases.users_usecases.paginate_users_collector import (
    PaginateUsersCollectorInterface,
)
from src.data.interfaces.users_repository import UsersRepositoryInterface


class PaginateUsersCollector(PaginateUsersCollectorInterface):
    """Users Pagination collector usecase"""

    def __init__(self, users_repository: Type[UsersRepositoryInterface]) -> None:
        self.__users_repository = users_repository

    async def paginate_users(
        self, db_session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Dict]:
        """
        Read users and return pagination
        :param  - db_session: ORM database session
                - skip: Pagination skip item
                - limit: Pagination limit item
        :returns - List with all users information
        """

        api_response = await self.__users_repository.get_users(db_session, skip, limit)

        return api_response
