from unittest.mock import MagicMock
from pytest import mark

from src.errors.http_request_error import HttpRequestError

from src.data.usecases.utils.fake_user_data import create_fake_user
from src.data.usecases.utils.fake_course_data import (
    create_fake_course,
    patch_fake_course,
)
from src.infra.repositories.tests.users_repository import UsersRepositorySpy
from src.infra.repositories.tests.courses_repository import CoursesRepositorySpy
from src.data.usecases.users_usecases.create_user_collector import CreateUserCollector
from src.data.usecases.courses_usecases.create_course_collector import (
    CreateCourseCollector,
)
from src.data.usecases.courses_usecases.patch_course_collector import (
    PatchCourseCollector,
)


@mark.asyncio
async def test_patch_course():
    """Testing test_patch_course method"""

    session = MagicMock()

    courses_repository = CoursesRepositorySpy()
    users_repository = UsersRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    create_course_collector = CreateCourseCollector(
        courses_repository, users_repository
    )
    patch_course_collector = PatchCourseCollector(courses_repository, users_repository)

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    fake_course = create_fake_course(user_id=user.id)
    patch_fake_course_data = patch_fake_course(user_id=user.id)

    created_course = await create_course_collector.create_course(
        db_session=session, course=fake_course
    )

    response = await patch_course_collector.patch_course(
        db_session=session,
        course_id=created_course.id,
        course=patch_fake_course_data,
    )

    assert (
        courses_repository.patch_db_course_attributes["course_id"] == created_course.id
    )
    assert (
        courses_repository.patch_db_course_attributes["user_id"]
        == created_course.user_id
    )
    assert (
        courses_repository.patch_db_course_attributes["title"] == created_course.title
    )
    assert (
        courses_repository.patch_db_course_attributes["description"]
        == created_course.description
    )
    assert courses_repository.patch_db_course_attributes["url"] == created_course.url

    assert response is None

    assert courses_repository.courses[0].id == created_course.id
    assert courses_repository.courses[0].title == patch_fake_course_data.title
    assert courses_repository.courses[0].user_id == patch_fake_course_data.user_id


@mark.asyncio
async def test_patch_course_not_found_error():
    """Testing course not found error in patch_course method"""

    session = MagicMock()

    courses_repository = CoursesRepositorySpy()
    users_repository = UsersRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    create_course_collector = CreateCourseCollector(
        courses_repository, users_repository
    )
    patch_course_collector = PatchCourseCollector(courses_repository, users_repository)

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    fake_course = create_fake_course(user_id=user.id)
    patch_fake_course_data = patch_fake_course(user_id=user.id)

    created_course = await create_course_collector.create_course(
        db_session=session, course=fake_course
    )

    try:
        await patch_course_collector.patch_course(
            db_session=session,
            course_id=created_course.id + 1,
            course=patch_fake_course_data,
        )

        assert True is False
    except HttpRequestError as error:

        assert error.detail is not None
        assert error.status_code == 404


@mark.asyncio
async def test_patch_course_name_already_exists_error():
    """Testing course name already exists error in patch_course method"""

    session = MagicMock()

    courses_repository = CoursesRepositorySpy()
    users_repository = UsersRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    create_course_collector = CreateCourseCollector(
        courses_repository, users_repository
    )
    patch_course_collector = PatchCourseCollector(courses_repository, users_repository)

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    create_first_fake_course_data = create_fake_course(user_id=user.id)
    create_second_fake_course_data = create_fake_course(user_id=user.id)
    patch_fake_course_data = patch_fake_course(user_id=user.id)

    first_created_course = await create_course_collector.create_course(
        db_session=session, course=create_first_fake_course_data
    )

    second_created_course = await create_course_collector.create_course(
        db_session=session, course=create_second_fake_course_data
    )

    patch_fake_course_data.title = first_created_course.title

    try:
        await patch_course_collector.patch_course(
            db_session=session,
            course_id=second_created_course.id,
            course=patch_fake_course_data,
        )

        assert True is False
    except HttpRequestError as error:

        assert error.detail is not None
        assert error.status_code == 400


@mark.asyncio
async def test_patch_course_user_not_found_error():
    """Testing course user not found error in patch_course method"""

    session = MagicMock()

    courses_repository = CoursesRepositorySpy()
    users_repository = UsersRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    create_course_collector = CreateCourseCollector(
        courses_repository, users_repository
    )
    patch_course_collector = PatchCourseCollector(courses_repository, users_repository)

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    fake_course = create_fake_course(user_id=user.id)
    patch_fake_course_data = patch_fake_course(user_id=user.id)

    created_course = await create_course_collector.create_course(
        db_session=session, course=fake_course
    )

    patch_fake_course_data.user_id = patch_fake_course_data.user_id + 1

    try:
        await patch_course_collector.patch_course(
            db_session=session,
            course_id=created_course.id,
            course=patch_fake_course_data,
        )

        assert True is False
    except HttpRequestError as error:

        assert error.detail is not None
        assert error.status_code == 404


@mark.asyncio
async def test_patch_course_user_student_role_error():
    """Testing user student role error in patch_course method"""

    session = MagicMock()

    courses_repository = CoursesRepositorySpy()
    users_repository = UsersRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    create_course_collector = CreateCourseCollector(
        courses_repository, users_repository
    )
    patch_course_collector = PatchCourseCollector(courses_repository, users_repository)

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    fake_course = create_fake_course(user_id=user.id)
    patch_fake_course_data = patch_fake_course(user_id=user.id)

    created_course = await create_course_collector.create_course(
        db_session=session, course=fake_course
    )

    user.role = 2

    try:
        await patch_course_collector.patch_course(
            db_session=session,
            course_id=created_course.id,
            course=patch_fake_course_data,
        )

        assert True is False
    except HttpRequestError as error:

        assert error.detail is not None
        assert error.status_code == 400
