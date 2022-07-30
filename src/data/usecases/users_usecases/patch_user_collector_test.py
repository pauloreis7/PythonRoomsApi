from unittest.mock import MagicMock
from pytest import mark

from src.errors.http_request_error import HttpRequestError

from src.infra.repositories.tests.users_repository import UsersRepositorySpy
from src.data.usecases.utils.fake_user_data import (
    create_fake_user,
    patch_fake_user,
)
from src.data.usecases.users_usecases.create_user_collector import CreateUserCollector
from src.data.usecases.users_usecases.patch_user_collector import PatchUserCollector


@mark.asyncio
async def test_patch_user():
    """Testing test_patch_user method"""

    session = MagicMock()

    users_repository = UsersRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    patch_user_collector = PatchUserCollector(users_repository)

    create_fake_user_data = create_fake_user()
    patch_fake_user_data = patch_fake_user()

    created_user = await create_user_collector.create_user(
        db_session=session, user=create_fake_user_data
    )

    response = await patch_user_collector.patch_user(
        db_session=session, user_id=created_user.id, user=patch_fake_user_data
    )

    assert users_repository.patch_db_user_attributes["user_id"] == created_user.id
    assert (
        users_repository.patch_db_user_attributes["email"] == patch_fake_user_data.email
    )
    assert (
        users_repository.patch_db_user_attributes["role"] == patch_fake_user_data.role
    )
    assert (
        users_repository.patch_db_user_attributes["first_name"]
        == patch_fake_user_data.first_name
    )
    assert (
        users_repository.patch_db_user_attributes["last_name"]
        == patch_fake_user_data.last_name
    )
    assert users_repository.patch_db_user_attributes["bio"] == patch_fake_user_data.bio

    assert response is None

    assert users_repository.users[0].id == created_user.id
    assert users_repository.users[0].first_name == patch_fake_user_data.first_name
    assert users_repository.users[0].email == patch_fake_user_data.email


@mark.asyncio
async def test_patch_user_not_found_error():
    """Testing not found error in patch_user method"""

    session = MagicMock()

    users_repository = UsersRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    patch_user_collector = PatchUserCollector(users_repository)

    create_fake_user_data = create_fake_user()
    patch_fake_user_data = patch_fake_user()

    created_user = await create_user_collector.create_user(
        db_session=session, user=create_fake_user_data
    )

    try:
        await patch_user_collector.patch_user(
            db_session=session,
            user_id=created_user.id + 1,
            user=patch_fake_user_data,
        )

        assert True is False
    except HttpRequestError as error:

        assert error.detail is not None
        assert error.status_code == 404


@mark.asyncio
async def test_patch_user_email_already_exists_error():
    """Testing user email already exists error in patch_user method"""

    session = MagicMock()

    users_repository = UsersRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    patch_user_collector = PatchUserCollector(users_repository)

    create_first_fake_user_data = create_fake_user()
    create_second_fake_user_data = create_fake_user()
    patch_fake_user_data = patch_fake_user()

    first_created_user = await create_user_collector.create_user(
        db_session=session, user=create_first_fake_user_data
    )

    second_created_user = await create_user_collector.create_user(
        db_session=session, user=create_second_fake_user_data
    )

    patch_fake_user_data.email = first_created_user.email

    try:
        await patch_user_collector.patch_user(
            db_session=session,
            user_id=second_created_user.id,
            user=patch_fake_user_data,
        )

        assert True is False
    except HttpRequestError as error:

        assert error.detail is not None
        assert error.status_code == 400
