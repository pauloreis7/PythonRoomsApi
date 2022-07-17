from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.pydantic_schemas.user import UserPatch
from src.domain.usecases.users_usecases.patch_user_collector import (
    PatchUserCollectorInterface,
)
from src.data.interfaces.users_repository import UsersRepositoryInterface
from src.errors.http_request_error import HttpRequestError


class PatchUserCollector(PatchUserCollectorInterface):
    """Patch User collector usecase"""

    def __init__(self, users_repository: Type[UsersRepositoryInterface]) -> None:
        self.__users_repository = users_repository

    async def patch_user(
        self, db_session: AsyncSession, user_id: int, user: UserPatch
    ) -> None:
        """
        Patch user model
        :param  - db_session: ORM database session
                - user: User data for patch
        :returns - None for patch user event status
        """

        check_user_exists = await self.__users_repository.get_user_by_id(
            db_session, user_id=user_id
        )

        if check_user_exists is None:
            raise HttpRequestError(status_code=404, detail="User not found")

        check_user_email_already_exists = (
            await self.__users_repository.get_user_by_email(
                db_session, user_email=user.email
            )
        )

        if (
            check_user_email_already_exists
            and check_user_email_already_exists.id is not user_id
        ):
            raise HttpRequestError(status_code=400, detail="Email already in use!")

        await self.__users_repository.patch_db_user(db_session, user_id, user)

        return
