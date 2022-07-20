from src.infra.repositories.courses_repository import CoursesRepository
from src.infra.repositories.users_repository import UsersRepository
from src.data.usecases.courses_usecases.create_course_collector import (
    CreateCourseCollector,
)
from src.presenters.controllers import CreateCourseCollectorController


def create_course_composer():
    """create course composer"""

    courses_infra = CoursesRepository()
    users_infra = UsersRepository()
    use_case = CreateCourseCollector(courses_infra, users_infra)
    controller = CreateCourseCollectorController(use_case)

    return controller
