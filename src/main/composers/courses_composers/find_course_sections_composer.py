from src.infra.repositories.courses_repository import CoursesRepository
from src.infra.repositories.sections_repository import SectionsRepository
from src.data.usecases.courses_usecases.find_course_sections_collector import (
    FindCourseSectionsCollector,
)
from src.presenters.controllers import FindCourseSectionsCollectorController


def find_course_sections_composer():
    """find course sections composer"""

    courses_infra = CoursesRepository()
    sections_infra = SectionsRepository()
    use_case = FindCourseSectionsCollector(courses_infra, sections_infra)
    controller = FindCourseSectionsCollectorController(use_case)

    return controller
