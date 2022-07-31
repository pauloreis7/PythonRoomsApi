from unittest.mock import MagicMock
from pytest import mark

from src.errors.http_request_error import HttpRequestError

from src.data.usecases.utils.fake_user_data import create_fake_user
from src.data.usecases.utils.fake_course_data import create_fake_course
from src.data.usecases.utils.fake_section_data import create_fake_section
from src.infra.repositories.tests.users_repository import UsersRepositorySpy
from src.infra.repositories.tests.courses_repository import CoursesRepositorySpy
from src.infra.repositories.tests.sections_repository import SectionsRepositorySpy
from src.data.usecases.users_usecases.create_user_collector import CreateUserCollector
from src.data.usecases.courses_usecases.create_course_collector import (
    CreateCourseCollector,
)
from src.data.usecases.sections_usecases.create_section_collector import (
    CreateSectionCollector,
)
from src.data.usecases.courses_usecases.find_course_sections_collector import (
    FindCourseSectionsCollector,
)


@mark.asyncio
async def test_find_course_sections():
    """Testing find_course_sections method"""

    session = MagicMock()

    courses_repository = CoursesRepositorySpy()
    users_repository = UsersRepositorySpy()
    sections_repository = SectionsRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    create_course_collector = CreateCourseCollector(
        courses_repository, users_repository
    )
    create_section_collector = CreateSectionCollector(
        sections_repository, courses_repository
    )
    find_course_sections_collector = FindCourseSectionsCollector(
        courses_repository, sections_repository
    )

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    fake_course = create_fake_course(user_id=user.id)

    course = await create_course_collector.create_course(
        db_session=session, course=fake_course
    )

    fake_section = create_fake_section(course_id=course.id)

    await create_section_collector.create_section(
        db_session=session, section=fake_section
    )
    await create_section_collector.create_section(
        db_session=session, section=fake_section
    )

    response = await find_course_sections_collector.find_course_sections(
        db_session=session, course_id=course.id
    )

    assert sections_repository.get_course_sections_attributes["course_id"] == course.id

    assert isinstance(response, list)
    assert len(response) == 2

    assert isinstance(response[0].title, str)
    assert response[0].course_id == course.id


@mark.asyncio
async def test_find_course_sections_not_found_error():
    """Testing not found error in find_course_sections method"""

    session = MagicMock()

    courses_repository = CoursesRepositorySpy()
    users_repository = UsersRepositorySpy()
    sections_repository = SectionsRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    create_course_collector = CreateCourseCollector(
        courses_repository, users_repository
    )
    find_course_sections_collector = FindCourseSectionsCollector(
        courses_repository, sections_repository
    )

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    fake_course = create_fake_course(user_id=user.id)

    course = await create_course_collector.create_course(
        db_session=session, course=fake_course
    )

    try:
        await find_course_sections_collector.find_course_sections(
            db_session=session, course_id=course.id + 1
        )

        assert True is False
    except HttpRequestError as error:

        assert error.detail is not None
        assert error.status_code == 404
