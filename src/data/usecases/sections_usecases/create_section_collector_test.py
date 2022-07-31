from unittest.mock import MagicMock
from pytest import mark

from src.errors.http_request_error import HttpRequestError

from src.domain.models.sections import Section
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


@mark.asyncio
async def test_create_section():
    """Testing create_section method"""

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

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    fake_course = create_fake_course(user_id=user.id)

    course = await create_course_collector.create_course(
        db_session=session, course=fake_course
    )

    fake_section = create_fake_section(course_id=course.id)

    response = await create_section_collector.create_section(
        db_session=session, section=fake_section
    )

    assert sections_repository.create_db_section_attributes["title"] == response.title
    assert (
        sections_repository.create_db_section_attributes["description"]
        == response.description
    )
    assert (
        sections_repository.create_db_section_attributes["content_type"]
        == response.content_type
    )
    assert (
        sections_repository.create_db_section_attributes["grade_media"]
        == response.grade_media
    )
    assert (
        sections_repository.create_db_section_attributes["course_id"]
        == response.course_id
    )

    assert isinstance(response, Section)
    assert isinstance(response.id, int)
    assert response.title == fake_section.title


@mark.asyncio
async def test_create_section_not_found_error():
    """Testing course not found error in create_section method"""

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

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    fake_course = create_fake_course(user_id=user.id)

    course = await create_course_collector.create_course(
        db_session=session, course=fake_course
    )

    fake_section = create_fake_section(course_id=course.id + 1)

    try:
        await create_section_collector.create_section(
            db_session=session, section=fake_section
        )

        assert True is False
    except HttpRequestError as error:

        assert error.detail is not None
        assert error.status_code == 404
