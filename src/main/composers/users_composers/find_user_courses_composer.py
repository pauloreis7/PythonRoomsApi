from src.infra.repositories.users_repository import UsersRepository
from src.infra.repositories.courses_repository import CoursesRepository
from src.data.usecases.users_usecases.find_user_courses_collector import (
    FindUserCoursesCollector,
)
from src.presenters.controllers import FindUserCoursesCollectorController


def find_user_courses_composer():
    """find user courses composer"""

    users_infra = UsersRepository()
    courses_infra = CoursesRepository()
    use_case = FindUserCoursesCollector(users_infra, courses_infra)
    controller = FindUserCoursesCollectorController(use_case)

    return controller
