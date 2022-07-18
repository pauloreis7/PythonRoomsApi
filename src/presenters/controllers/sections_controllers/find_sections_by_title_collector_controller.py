from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.usecases.sections_usecases.find_sections_by_title_collector import (
    FindSectionsByTitleCollectorInterface,
)
from src.domain.controllers.sections_controllers import (
    FindSectionsByTitleCollectorControllerInterface,
)


class FindSectionsByTitleCollectorController(
    FindSectionsByTitleCollectorControllerInterface
):
    """Controller to find sections by title usecase"""

    def __init__(
        self,
        find_sections_by_title_collector: Type[FindSectionsByTitleCollectorInterface],
    ) -> None:
        self.__use_case = find_sections_by_title_collector

    async def handle(self, db_session: AsyncSession, sections_title: str):
        """Handle to find sections by title controller"""

        sections = await self.__use_case.find_sections_by_title(
            db_session=db_session, sections_title=sections_title
        )

        response = {"status_code": 200, "data": sections}

        return response
