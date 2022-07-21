from src.infra.repositories.sections_repository import SectionsRepository
from src.data.usecases.sections_usecases.find_section_by_id_collector import (
    FindSectionByIdCollector,
)
from src.presenters.controllers import FindSectionByIdCollectorController


def find_section_by_id_composer():
    """find section by id composer"""

    infra = SectionsRepository()
    use_case = FindSectionByIdCollector(infra)
    controller = FindSectionByIdCollectorController(use_case)

    return controller
