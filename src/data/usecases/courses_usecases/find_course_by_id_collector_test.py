from unittest.mock import MagicMock
from pytest import mark

from src.errors.http_request_error import HttpRequestError

from src.pydantic_schemas.course import Course
from src.data.usecases.utils.fake_user_data import create_fake_user
from src.data.usecases.utils.fake_course_data import create_fake_course
from src.infra.repositories.tests.users_repository import UsersRepositorySpy
from src.infra.repositories.tests.courses_repository import CoursesRepositorySpy
from src.data.usecases.users_usecases.create_user_collector import CreateUserCollector
from src.data.usecases.courses_usecases.create_course_collector import (
    CreateCourseCollector,
)
from src.data.usecases.courses_usecases.find_course_by_id_collector import (
    FindCourseByIdCollector,
)


@mark.asyncio
async def test_find_course_by_id():
    """Testing find_course_by_id method"""

    session = MagicMock()

    courses_repository = CoursesRepositorySpy()
    users_repository = UsersRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    create_course_collector = CreateCourseCollector(
        courses_repository, users_repository
    )
    find_course_by_id_collector = FindCourseByIdCollector(courses_repository)

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    fake_course = create_fake_course(user_id=user.id)

    course = await create_course_collector.create_course(
        db_session=session, course=fake_course
    )

    response = await find_course_by_id_collector.find_course_by_id(
        db_session=session, course_id=course.id
    )

    assert courses_repository.get_course_by_id_attributes["course_id"] == course.id

    assert isinstance(response, Course)
    assert isinstance(response.title, str)
    assert isinstance(response.user_id, int)


@mark.asyncio
async def test_find_course_by_id_not_found_error():
    """Testing not found error in find_course_by_id method"""

    session = MagicMock()

    courses_repository = CoursesRepositorySpy()
    users_repository = UsersRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    create_course_collector = CreateCourseCollector(
        courses_repository, users_repository
    )
    find_course_by_id_collector = FindCourseByIdCollector(courses_repository)

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    fake_course = create_fake_course(user_id=user.id)

    course = await create_course_collector.create_course(
        db_session=session, course=fake_course
    )

    try:
        await find_course_by_id_collector.find_course_by_id(
            db_session=session, course_id=course.id + 1
        )

        assert True is False
    except HttpRequestError as error:

        assert error.detail is not None
        assert error.status_code == 404
