from typing import Type, List

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.sections import Section
from src.domain.usecases.sections_usecases.find_sections_by_title_collector import (
    FindSectionsByTitleCollectorInterface,
)
from src.data.interfaces.sections_repository import SectionsRepositoryInterface


class FindSectionsByTitleCollector(FindSectionsByTitleCollectorInterface):
    """Find Sections By Title collector usecase"""

    def __init__(self, sections_repository: Type[SectionsRepositoryInterface]) -> None:
        self.__sections_repository = sections_repository

    async def find_sections_by_title(
        self, db_session: AsyncSession, sections_title: str
    ) -> List[Section]:
        """
        Find sections by title and return it
        :param  - db_session: ORM database session
                - sections_title: Sections title to find
        :returns - List with sections information
        """

        api_response = await self.__sections_repository.get_sections_by_title(
            db_session, sections_title
        )

        return api_response
