from unittest.mock import MagicMock
from pytest import mark

from src.errors.http_request_error import HttpRequestError

from src.domain.models.course import Course
from src.data.usecases.utils.fake_user_data import create_fake_user
from src.data.usecases.utils.fake_course_data import create_fake_course
from src.infra.repositories.tests.users_repository import UsersRepositorySpy
from src.infra.repositories.tests.courses_repository import CoursesRepositorySpy
from src.data.usecases.users_usecases.create_user_collector import CreateUserCollector
from src.data.usecases.courses_usecases.create_course_collector import (
    CreateCourseCollector,
)


@mark.asyncio
async def test_create_course():
    """Testing create_course method"""

    session = MagicMock()

    courses_repository = CoursesRepositorySpy()
    users_repository = UsersRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    create_course_collector = CreateCourseCollector(
        courses_repository, users_repository
    )

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    fake_course = create_fake_course(user_id=user.id)

    response = await create_course_collector.create_course(
        db_session=session, course=fake_course
    )

    assert courses_repository.create_db_course_attributes["title"] == response.title
    assert (
        courses_repository.create_db_course_attributes["description"]
        == response.description
    )
    assert courses_repository.create_db_course_attributes["url"] == response.url
    assert courses_repository.create_db_course_attributes["user_id"] == response.user_id

    assert isinstance(response, Course)
    assert isinstance(response.id, int)
    assert response.title == fake_course.title


@mark.asyncio
async def test_create_course_already_exists_error():
    """Testing course already exists error in create_course method"""

    session = MagicMock()

    courses_repository = CoursesRepositorySpy()
    users_repository = UsersRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    create_course_collector = CreateCourseCollector(
        courses_repository, users_repository
    )

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    fake_course = create_fake_course(user_id=user.id)

    try:
        await create_course_collector.create_course(
            db_session=session, course=fake_course
        )
        await create_course_collector.create_course(
            db_session=session, course=fake_course
        )

        assert True is False
    except HttpRequestError as error:

        assert error.detail is not None
        assert error.status_code == 400


@mark.asyncio
async def test_create_course_user_not_found_error():
    """Testing user not found error in create_course method"""

    session = MagicMock()

    courses_repository = CoursesRepositorySpy()
    users_repository = UsersRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    create_course_collector = CreateCourseCollector(
        courses_repository, users_repository
    )

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    fake_course = create_fake_course(user_id=user.id + 1)

    try:
        await create_course_collector.create_course(
            db_session=session, course=fake_course
        )

        assert True is False
    except HttpRequestError as error:

        assert error.detail is not None
        assert error.status_code == 404


@mark.asyncio
async def test_create_course_user_student_role_error():
    """Testing user student role error in create_course method"""

    session = MagicMock()

    courses_repository = CoursesRepositorySpy()
    users_repository = UsersRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    create_course_collector = CreateCourseCollector(
        courses_repository, users_repository
    )

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    fake_course = create_fake_course(user_id=user.id)

    user.role = 2

    try:
        await create_course_collector.create_course(
            db_session=session, course=fake_course
        )

        assert True is False
    except HttpRequestError as error:

        assert error.detail is not None
        assert error.status_code == 400
