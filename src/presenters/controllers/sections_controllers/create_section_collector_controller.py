from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.pydantic_schemas.sections import SectionCreate
from src.domain.usecases.sections_usecases.create_section_collector import (
    CreateSectionCollectorInterface,
)
from src.domain.controllers.sections_controllers.create_section_collector_controller import (
    CreateSectionCollectorControllerInterface,
)


class CreateSectionCollectorController(CreateSectionCollectorControllerInterface):
    """Controller to create section usecase"""

    def __init__(
        self, create_section_collector: Type[CreateSectionCollectorInterface]
    ) -> None:
        self.__use_case = create_section_collector

    async def handle(self, db_session: AsyncSession, section: SectionCreate):
        """Handle to create course section controller"""

        section_create_status = await self.__use_case.create_section(
            db_session=db_session, section=section
        )

        response = {"status_code": 201, "data": section_create_status}

        return response
