from unittest.mock import MagicMock
from pytest import mark

from src.data.usecases.utils.fake_user_data import create_fake_user
from src.data.usecases.utils.fake_course_data import create_fake_course
from src.infra.repositories.tests.users_repository import UsersRepositorySpy
from src.infra.repositories.tests.courses_repository import CoursesRepositorySpy
from src.data.usecases.courses_usecases.create_course_collector import (
    CreateCourseCollector,
)
from src.data.usecases.courses_usecases.paginate_courses_collector import (
    PaginateCoursesCollector,
)
from src.data.usecases.users_usecases.create_user_collector import CreateUserCollector


@mark.asyncio
async def test_paginate_courses():
    """Testing test_paginate_courses method"""

    session = MagicMock()

    courses_repository = CoursesRepositorySpy()
    users_repository = UsersRepositorySpy()
    create_user_collector = CreateUserCollector(users_repository)
    create_course_collector = CreateCourseCollector(
        courses_repository, users_repository
    )
    paginate_courses_collector = PaginateCoursesCollector(courses_repository)

    skip = 0
    limit = 100

    fake_user = create_fake_user()

    user = await create_user_collector.create_user(db_session=session, user=fake_user)

    fake_course = create_fake_course(user_id=user.id)

    await create_course_collector.create_course(db_session=session, course=fake_course)

    response = await paginate_courses_collector.paginate_courses(
        db_session=session, skip=skip, limit=limit
    )

    assert courses_repository.get_courses_attributes["skip"] == skip
    assert courses_repository.get_courses_attributes["limit"] == limit

    assert isinstance(response, list)
    assert isinstance(response[0].title, str)
    assert isinstance(response[0].user_id, int)
