from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.pydantic_schemas.sections import SectionPatch
from src.domain.usecases.sections_usecases.patch_section_collector import (
    PatchSectionCollectorInterface,
)
from src.domain.controllers.sections_controllers.patch_section_collector_controller import (
    PatchSectionCollectorControllerInterface,
)


class PatchSectionCollectorController(PatchSectionCollectorControllerInterface):
    """Controller to patch section usecase"""

    def __init__(
        self, patch_section_collector: Type[PatchSectionCollectorInterface]
    ) -> None:
        self.__use_case = patch_section_collector

    async def handle(
        self, db_session: AsyncSession, section_id: int, section: SectionPatch
    ):
        """Handle to patch course section controller"""

        await self.__use_case.patch_section(
            db_session=db_session, section_id=section_id, section=section
        )

        response = {"status_code": 204, "data": None}

        return response
