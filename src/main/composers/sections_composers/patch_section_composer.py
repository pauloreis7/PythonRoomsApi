from src.infra.repositories.sections_repository import SectionsRepository
from src.infra.repositories.courses_repository import CoursesRepository
from src.data.usecases.sections_usecases.patch_section_collector import (
    PatchSectionCollector,
)
from src.presenters.controllers import PatchSectionCollectorController


def patch_section_composer():
    """patch section composer"""

    sections_infra = SectionsRepository()
    courses_infra = CoursesRepository()
    use_case = PatchSectionCollector(sections_infra, courses_infra)
    controller = PatchSectionCollectorController(use_case)

    return controller
