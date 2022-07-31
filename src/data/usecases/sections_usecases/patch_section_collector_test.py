from unittest.mock import MagicMock
from pytest import mark

from src.errors.http_request_error import HttpRequestError

from src.data.usecases.utils.fake_user_data import create_fake_user
from src.data.usecases.utils.fake_course_data import create_fake_course
from src.data.usecases.utils.fake_section_data import (
    create_fake_section,
    patch_fake_section,
)
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
from src.data.usecases.sections_usecases.patch_section_collector import (
    PatchSectionCollector,
)


@mark.asyncio
async def test_patch_section():
    """Testing patch_section method"""

    session = MagicMock()

    users_repository = UsersRepositorySpy()
    courses_repository = CoursesRepositorySpy()
    sections_repository = SectionsRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    create_course_collector = CreateCourseCollector(
        courses_repository, users_repository
    )
    create_section_collector = CreateSectionCollector(
        sections_repository, courses_repository
    )
    patch_section_collector = PatchSectionCollector(
        sections_repository, courses_repository
    )

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    fake_course = create_fake_course(user_id=user.id)

    course = await create_course_collector.create_course(
        db_session=session, course=fake_course
    )

    fake_section = create_fake_section(course_id=course.id)
    patch_fake_section_data = patch_fake_section(course_id=course.id)

    created_section = await create_section_collector.create_section(
        db_session=session, section=fake_section
    )

    response = await patch_section_collector.patch_section(
        db_session=session,
        section_id=created_section.id,
        section=patch_fake_section_data,
    )

    assert (
        sections_repository.patch_db_section_attributes["section_id"]
        == created_section.id
    )
    assert (
        sections_repository.patch_db_section_attributes["title"]
        == created_section.title
    )
    assert (
        sections_repository.patch_db_section_attributes["description"]
        == created_section.description
    )
    assert (
        sections_repository.patch_db_section_attributes["content_type"]
        == created_section.content_type
    )
    assert (
        sections_repository.patch_db_section_attributes["grade_media"]
        == created_section.grade_media
    )
    assert (
        sections_repository.patch_db_section_attributes["course_id"]
        == created_section.course_id
    )

    assert response is None

    assert sections_repository.sections[0].id == created_section.id
    assert sections_repository.sections[0].title == patch_fake_section_data.title
    assert (
        sections_repository.sections[0].course_id == patch_fake_section_data.course_id
    )


@mark.asyncio
async def test_patch_section_not_found_error():
    """Testing section not found error in patch_section method"""

    session = MagicMock()

    users_repository = UsersRepositorySpy()
    courses_repository = CoursesRepositorySpy()
    sections_repository = SectionsRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    create_course_collector = CreateCourseCollector(
        courses_repository, users_repository
    )
    create_section_collector = CreateSectionCollector(
        sections_repository, courses_repository
    )
    patch_section_collector = PatchSectionCollector(
        sections_repository, courses_repository
    )

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    fake_course = create_fake_course(user_id=user.id)

    course = await create_course_collector.create_course(
        db_session=session, course=fake_course
    )

    fake_section = create_fake_section(course_id=course.id)
    patch_fake_section_data = patch_fake_section(course_id=course.id)

    created_section = await create_section_collector.create_section(
        db_session=session, section=fake_section
    )

    try:
        await patch_section_collector.patch_section(
            db_session=session,
            section_id=created_section.id + 1,
            section=patch_fake_section_data,
        )

        assert True is False
    except HttpRequestError as error:

        assert error.detail is not None
        assert error.status_code == 404


@mark.asyncio
async def test_patch_section_course_not_found_error():
    """Testing course not found error in patch_section method"""

    session = MagicMock()

    users_repository = UsersRepositorySpy()
    courses_repository = CoursesRepositorySpy()
    sections_repository = SectionsRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    create_course_collector = CreateCourseCollector(
        courses_repository, users_repository
    )
    create_section_collector = CreateSectionCollector(
        sections_repository, courses_repository
    )
    patch_section_collector = PatchSectionCollector(
        sections_repository, courses_repository
    )

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    fake_course = create_fake_course(user_id=user.id)

    course = await create_course_collector.create_course(
        db_session=session, course=fake_course
    )

    fake_section = create_fake_section(course_id=course.id)
    patch_fake_section_data = patch_fake_section(course_id=course.id)

    created_section = await create_section_collector.create_section(
        db_session=session, section=fake_section
    )

    patch_fake_section_data.course_id = patch_fake_section_data.course_id + 1

    try:
        await patch_section_collector.patch_section(
            db_session=session,
            section_id=created_section.id,
            section=patch_fake_section_data,
        )

        assert True is False
    except HttpRequestError as error:

        assert error.detail is not None
        assert error.status_code == 404
