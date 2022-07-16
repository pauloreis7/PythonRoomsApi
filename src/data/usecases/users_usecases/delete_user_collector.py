from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from src.domain.usecases.users_usecases.delete_user_collector import (
    DeleteUserCollectorInterface,
)
from src.data.interfaces.users_repository import UsersRepositoryInterface


class DeleteUserCollector(DeleteUserCollectorInterface):
    """Delete User collector usecase"""

    def __init__(self, users_repository: Type[UsersRepositoryInterface]) -> None:
        self.__users_repository = users_repository

    async def delete_user(self, db_session: AsyncSession, user_id: int) -> None:
        """
        Delete user model
        :param  - db_session: ORM database session
                - user_id: user id for delete
        :returns - None for delete user event status
        """

        check_user_exists = await self.__users_repository.get_user_by_id(
            db_session, user_id=user_id
        )

        if check_user_exists is None:
            raise HTTPException(status_code=404, detail="User not found")

        await self.__users_repository.delete_db_user(db_session, user_id)

        return
