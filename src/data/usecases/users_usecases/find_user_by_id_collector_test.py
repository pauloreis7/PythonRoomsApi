from unittest.mock import MagicMock
from pytest import mark

from src.errors.http_request_error import HttpRequestError

from src.pydantic_schemas.user import User
from src.infra.repositories.tests.users_repository import UsersRepositorySpy
from src.data.usecases.utils.fake_user_data import create_fake_user
from src.data.usecases.users_usecases.create_user_collector import CreateUserCollector
from src.data.usecases.users_usecases.find_user_by_id_collector import (
    FindUserByIdCollector,
)


@mark.asyncio
async def test_find_user_by_id():
    """Testing find_user_by_id method"""

    session = MagicMock()

    users_repository = UsersRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    find_user_by_id_collector = FindUserByIdCollector(users_repository)

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    response = await find_user_by_id_collector.find_user_by_id(
        db_session=session, user_id=user.id
    )

    assert users_repository.get_user_by_id_attributes["user_id"] == user.id

    assert isinstance(response, User)
    assert isinstance(response.email, str)
    assert isinstance(response.first_name, str)


@mark.asyncio
async def test_find_user_by_id_not_found_error():
    """Testing not found error in find_user_by_id method"""

    session = MagicMock()

    users_repository = UsersRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    find_user_by_id_collector = FindUserByIdCollector(users_repository)

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    try:
        await find_user_by_id_collector.find_user_by_id(
            db_session=session, user_id=user.id + 1
        )

        assert True is False
    except HttpRequestError as error:

        assert error.detail is not None
        assert error.status_code == 404
