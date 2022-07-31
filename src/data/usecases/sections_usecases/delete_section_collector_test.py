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
from src.data.usecases.sections_usecases.delete_section_collector import (
    DeleteSectionCollector,
)


@mark.asyncio
async def test_delete_section():
    """Testing delete_section method"""

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
    delete_section_collector = DeleteSectionCollector(sections_repository)

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    fake_course = create_fake_course(user_id=user.id)

    course = await create_course_collector.create_course(
        db_session=session, course=fake_course
    )

    fake_section = create_fake_section(course_id=course.id)

    section = await create_section_collector.create_section(
        db_session=session, section=fake_section
    )

    response = await delete_section_collector.delete_section(
        db_session=session, section_id=section.id
    )

    assert sections_repository.delete_db_section_attributes["section_id"] == section.id

    assert response is None

    assert len(sections_repository.sections) == 0


@mark.asyncio
async def test_delete_section_not_found_error():
    """Testing not found error in delete_section method"""

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
    delete_section_collector = DeleteSectionCollector(sections_repository)

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    fake_course = create_fake_course(user_id=user.id)

    course = await create_course_collector.create_course(
        db_session=session, course=fake_course
    )

    fake_section = create_fake_section(course_id=course.id)

    section = await create_section_collector.create_section(
        db_session=session, section=fake_section
    )

    try:
        await delete_section_collector.delete_section(
            db_session=session, section_id=section.id + 1
        )

        assert True is False
    except HttpRequestError as error:

        assert error.detail is not None
        assert error.status_code == 404
