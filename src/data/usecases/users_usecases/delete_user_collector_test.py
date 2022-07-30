from unittest.mock import MagicMock
from pytest import mark

from src.errors.http_request_error import HttpRequestError

from src.infra.repositories.tests.users_repository import UsersRepositorySpy
from src.data.usecases.utils.fake_user_data import create_fake_user
from src.data.usecases.users_usecases.create_user_collector import CreateUserCollector
from src.data.usecases.users_usecases.delete_user_collector import DeleteUserCollector


@mark.asyncio
async def test_delete_user():
    """Testing test_delete_user method"""

    session = MagicMock()

    users_repository = UsersRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    delete_user_collector = DeleteUserCollector(users_repository)

    fake_user = create_fake_user()

    created_user = await create_user_collector.create_user(
        db_session=session, user=fake_user
    )

    response = await delete_user_collector.delete_user(
        db_session=session, user_id=created_user.id
    )

    assert users_repository.delete_db_user_attributes["user_id"] == created_user.id

    assert response is None

    assert len(users_repository.users) == 0


@mark.asyncio
async def test_delete_user_not_found_error():
    """Testing not found error in delete_user method"""

    session = MagicMock()

    users_repository = UsersRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    delete_user_collector = DeleteUserCollector(users_repository)

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    try:
        await delete_user_collector.delete_user(db_session=session, user_id=user.id + 1)

        assert True is False
    except HttpRequestError as error:

        assert error.detail is not None
        assert error.status_code == 404
