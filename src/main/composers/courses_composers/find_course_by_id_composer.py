from src.infra.repositories.courses_repository import CoursesRepository
from src.data.usecases.courses_usecases.find_course_by_id_collector import (
    FindCourseByIdCollector,
)
from src.presenters.controllers import FindCourseByIdCollectorController


def find_course_by_id_composer():
    """find course by id composer"""

    infra = CoursesRepository()
    use_case = FindCourseByIdCollector(infra)
    controller = FindCourseByIdCollectorController(use_case)

    return controller
