from src.infra.repositories.sections_repository import SectionsRepository
from src.data.usecases.sections_usecases.delete_section_collector import (
    DeleteSectionCollector,
)
from src.presenters.controllers import DeleteSectionCollectorController


def delete_section_composer():
    """delete section composer"""

    infra = SectionsRepository()
    use_case = DeleteSectionCollector(infra)
    controller = DeleteSectionCollectorController(use_case)

    return controller
