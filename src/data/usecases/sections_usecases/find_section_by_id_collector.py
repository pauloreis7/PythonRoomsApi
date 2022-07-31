from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.sections import Section
from src.domain.usecases.sections_usecases.find_section_by_id_collector import (
    FindSectionByIdCollectorInterface,
)
from src.data.interfaces.sections_repository import SectionsRepositoryInterface
from src.errors.http_request_error import HttpRequestError


class FindSectionByIdCollector(FindSectionByIdCollectorInterface):
    """Find Section By Id collector usecase"""

    def __init__(self, sections_repository: Type[SectionsRepositoryInterface]) -> None:
        self.__sections_repository = sections_repository

    async def find_section_by_id(
        self, db_session: AsyncSession, section_id: int
    ) -> Section:
        """
        Find section by id and return it
        :param  - db_session: ORM database session
                - section_id: Section id to find
        :returns - Dictionary with section information
        """

        api_response = await self.__sections_repository.get_section_by_id(
            db_session, section_id
        )

        if api_response is None:
            raise HttpRequestError(status_code=404, detail="Course section not found")

        return api_response
