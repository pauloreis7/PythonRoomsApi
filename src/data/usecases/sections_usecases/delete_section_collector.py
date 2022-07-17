from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from src.domain.usecases.sections_usecases.delete_section_collector import (
    DeleteSectionCollectorInterface,
)
from src.data.interfaces.sections_repository import SectionsRepositoryInterface


class DeleteSectionCollector(DeleteSectionCollectorInterface):
    """Delete Section collector usecase"""

    def __init__(self, sections_repository: Type[SectionsRepositoryInterface]) -> None:
        self.__sections_repository = sections_repository

    async def delete_section(self, db_session: AsyncSession, section_id: int) -> None:
        """
        Delete section model
        :param  - db_session: ORM database session
                - section_id: Section id for delete
        :returns - None for delete section event status
        """

        check_section_exists = await self.__sections_repository.get_section_by_id(
            db_session, section_id
        )

        if check_section_exists is None:
            raise HTTPException(status_code=404, detail="Course section not found")

        await self.__sections_repository.delete_db_section(db_session, section_id)

        return
