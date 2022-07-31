from unittest.mock import MagicMock
from pytest import mark

from src.errors.http_request_error import HttpRequestError

from src.domain.models.user import User
from src.infra.repositories.tests.users_repository import UsersRepositorySpy
from src.data.usecases.utils.fake_user_data import create_fake_user
from src.data.usecases.users_usecases.create_user_collector import CreateUserCollector


@mark.asyncio
async def test_create_user():
    """Testing test_create_user method"""

    session = MagicMock()

    users_repository = UsersRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)

    fake_user = create_fake_user()

    response = await create_user_collector.create_user(
        db_session=session, user=fake_user
    )

    assert users_repository.create_db_user_attributes["email"] == response.email
    assert users_repository.create_db_user_attributes["role"] == response.role
    assert (
        users_repository.create_db_user_attributes["first_name"] == response.first_name
    )
    assert users_repository.create_db_user_attributes["last_name"] == response.last_name
    assert users_repository.create_db_user_attributes["bio"] == response.bio
    assert users_repository.create_db_user_attributes["is_active"] == response.is_active

    assert isinstance(response, User)
    assert isinstance(response.id, int)
    assert response.email == fake_user.email


@mark.asyncio
async def test_create_user_already_exists_error():
    """Testing user already exists error in create_user method"""

    session = MagicMock()

    users_repository = UsersRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)

    fake_user = create_fake_user()

    try:
        await create_user_collector.create_user(db_session=session, user=fake_user)

        await create_user_collector.create_user(db_session=session, user=fake_user)

        assert True is False
    except HttpRequestError as error:

        assert error.detail is not None
        assert error.status_code == 400


@mark.asyncio
async def test_create_user_invalid_email_error():
    """Testing invalid email error in create_user method"""

    session = MagicMock()

    users_repository = UsersRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)

    fake_user = create_fake_user()

    fake_user.email = "invalid_email"

    try:
        await create_user_collector.create_user(db_session=session, user=fake_user)

        assert True is False
    except HttpRequestError as error:

        assert error.detail is not None
        assert error.status_code == 422
