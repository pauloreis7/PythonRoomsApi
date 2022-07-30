from unittest.mock import MagicMock
from pytest import mark

from src.errors.http_request_error import HttpRequestError

from src.infra.repositories.tests.users_repository import UsersRepositorySpy
from src.infra.repositories.tests.courses_repository import CoursesRepositorySpy
from src.data.usecases.utils.fake_user_data import create_fake_user
from src.data.usecases.utils.fake_course_data import create_fake_course
from src.data.usecases.users_usecases.create_user_collector import CreateUserCollector
from src.data.usecases.courses_usecases.create_course_collector import (
    CreateCourseCollector,
)
from src.data.usecases.users_usecases.find_user_courses_collector import (
    FindUserCoursesCollector,
)


@mark.asyncio
async def test_find_user_courses():
    """Testing find_user_courses method"""

    session = MagicMock()

    users_repository = UsersRepositorySpy()
    courses_repository = CoursesRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    create_course_collector = CreateCourseCollector(
        courses_repository, users_repository
    )
    find_user_courses_collector = FindUserCoursesCollector(
        users_repository, courses_repository
    )

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    create_first_fake_course_data = create_fake_course(user_id=user.id)
    create_second_fake_course_data = create_fake_course(user_id=user.id)

    await create_course_collector.create_course(
        db_session=session, course=create_first_fake_course_data
    )

    await create_course_collector.create_course(
        db_session=session, course=create_second_fake_course_data
    )

    response = await find_user_courses_collector.find_user_courses(
        db_session=session, user_id=user.id
    )

    assert users_repository.get_user_by_id_attributes["user_id"] == user.id

    assert isinstance(response, list)
    assert len(response) == 2

    assert isinstance(response[0].title, str)
    assert response[0].user_id == user.id


@mark.asyncio
async def test_find_user_courses_not_found_error():
    """Testing not found error in find_user_courses method"""

    session = MagicMock()

    users_repository = UsersRepositorySpy()
    courses_repository = CoursesRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    find_user_courses_collector = FindUserCoursesCollector(
        users_repository, courses_repository
    )

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    try:
        await find_user_courses_collector.find_user_courses(
            db_session=session, user_id=user.id + 1
        )

        assert True is False
    except HttpRequestError as error:

        assert error.detail is not None
        assert error.status_code == 404
