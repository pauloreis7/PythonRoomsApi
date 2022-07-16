from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from src.pydantic_schemas.user import UserCreate
from src.domain.usecases.users_usecases.create_user_collector import (
    CreateUserCollectorInterface,
)
from src.data.interfaces.users_repository import UsersRepositoryInterface


class CreateUserCollector(CreateUserCollectorInterface):
    """Create User collector usecase"""

    def __init__(self, users_repository: Type[UsersRepositoryInterface]) -> None:
        self.__users_repository = users_repository

    async def create_user(self, db_session: AsyncSession, user: UserCreate) -> bool:
        """
        Create user model
        :param  - db_session: ORM database session
                - user: User data for create
        :returns - Boolean for create user event status
        """

        check_user_exists = await self.__users_repository.get_user_by_email(
            db_session, user_email=user.email
        )

        if check_user_exists:
            raise HTTPException(status_code=400, detail="User already exists!")

        api_response = await self.__users_repository.create_db_user(db_session, user)

        return api_response
