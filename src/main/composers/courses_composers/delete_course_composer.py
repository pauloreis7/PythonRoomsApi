from src.infra.repositories.courses_repository import CoursesRepository
from src.data.usecases.courses_usecases.delete_course_collector import (
    DeleteCourseCollector,
)
from src.presenters.controllers import DeleteCourseCollectorController


def delete_course_composer():
    """delete course composer"""

    infra = CoursesRepository()
    use_case = DeleteCourseCollector(infra)
    controller = DeleteCourseCollectorController(use_case)

    return controller
