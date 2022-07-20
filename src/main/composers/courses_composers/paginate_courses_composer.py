from src.infra.repositories.courses_repository import CoursesRepository
from src.data.usecases.courses_usecases.paginate_courses_collector import (
    PaginateCoursesCollector,
)
from src.presenters.controllers import PaginateCoursesCollectorController


def paginate_courses_composer():
    """paginate courses composer"""

    infra = CoursesRepository()
    use_case = PaginateCoursesCollector(infra)
    controller = PaginateCoursesCollectorController(use_case)

    return controller
