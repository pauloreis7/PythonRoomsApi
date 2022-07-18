from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.usecases.sections_usecases.find_section_by_id_collector import (
    FindSectionByIdCollectorInterface,
)
from src.domain.controllers.sections_controllers.find_section_by_id_collector_controller import (
    FindSectionByIdCollectorControllerInterface,
)


class FindSectionByIdCollectorController(FindSectionByIdCollectorControllerInterface):
    """Controller to find section by id usecase"""

    def __init__(
        self, find_section_by_id_collector: Type[FindSectionByIdCollectorInterface]
    ) -> None:
        self.__use_case = find_section_by_id_collector

    async def handle(self, db_session: AsyncSession, section_id: int):
        """Handle to find course section by id controller"""

        section = await self.__use_case.find_section_by_id(
            db_session=db_session, section_id=section_id
        )

        response = {"status_code": 200, "data": section}

        return response
