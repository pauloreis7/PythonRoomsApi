from src.infra.repositories.sections_repository import SectionsRepository
from src.infra.repositories.courses_repository import CoursesRepository
from src.data.usecases.sections_usecases.create_section_collector import (
    CreateSectionCollector,
)
from src.presenters.controllers import CreateSectionCollectorController


def create_section_composer():
    """create section composer"""

    sections_infra = SectionsRepository()
    courses_infra = CoursesRepository()
    use_case = CreateSectionCollector(sections_infra, courses_infra)
    controller = CreateSectionCollectorController(use_case)

    return controller
