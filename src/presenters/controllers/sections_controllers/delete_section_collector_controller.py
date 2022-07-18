from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.usecases.sections_usecases.delete_section_collector import (
    DeleteSectionCollectorInterface,
)
from src.domain.controllers.sections_controllers.delete_section_collector_controller import (
    DeleteSectionCollectorControllerInterface,
)


class DeleteSectionCollectorController(DeleteSectionCollectorControllerInterface):
    """Controller to delete section usecase"""

    def __init__(
        self, delete_section_collector: Type[DeleteSectionCollectorInterface]
    ) -> None:
        self.__use_case = delete_section_collector

    async def handle(self, db_session: AsyncSession, section_id: int):
        """Handle to delete course section controller"""

        await self.__use_case.delete_section(
            db_session=db_session, section_id=section_id
        )

        response = {"status_code": 204, "data": None}

        return response
