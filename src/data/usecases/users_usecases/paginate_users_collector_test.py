from unittest.mock import MagicMock
from pytest import mark

from src.infra.repositories.tests.users_repository import UsersRepositorySpy
from src.data.usecases.users_usecases.paginate_users_collector import (
    PaginateUsersCollector,
)
from src.data.usecases.utils.fake_user_data import create_fake_user
from src.data.usecases.users_usecases.create_user_collector import CreateUserCollector


@mark.asyncio
async def test_paginate_users():
    """Testing test_paginate_users method"""

    session = MagicMock()

    users_repository = UsersRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    paginate_users_collector = PaginateUsersCollector(users_repository)

    skip = 0
    limit = 100

    fake_user = create_fake_user()

    await create_user_collector.create_user(db_session=session, user=fake_user)

    response = await paginate_users_collector.paginate_users(
        db_session=session, skip=skip, limit=limit
    )

    assert users_repository.get_users_attributes["skip"] == skip
    assert users_repository.get_users_attributes["limit"] == limit

    assert isinstance(response, list)
    assert isinstance(response[0].id, int)
    assert isinstance(response[0].email, str)
