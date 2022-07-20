from src.infra.repositories.courses_repository import CoursesRepository
from src.infra.repositories.users_repository import UsersRepository
from src.data.usecases.courses_usecases.patch_course_collector import (
    PatchCourseCollector,
)
from src.presenters.controllers import PatchCourseCollectorController


def patch_course_composer():
    """patch course composer"""

    courses_infra = CoursesRepository()
    users_infra = UsersRepository()
    use_case = PatchCourseCollector(courses_infra, users_infra)
    controller = PatchCourseCollectorController(use_case)

    return controller
