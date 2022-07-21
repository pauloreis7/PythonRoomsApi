from src.infra.repositories.sections_repository import SectionsRepository
from src.data.usecases.sections_usecases.find_sections_by_title_collector import (
    FindSectionsByTitleCollector,
)
from src.presenters.controllers import FindSectionsByTitleCollectorController


def find_sections_by_title_composer():
    """find sections by title composer"""

    infra = SectionsRepository()
    use_case = FindSectionsByTitleCollector(infra)
    controller = FindSectionsByTitleCollectorController(use_case)

    return controller
