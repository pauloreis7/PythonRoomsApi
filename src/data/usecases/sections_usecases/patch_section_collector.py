from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from src.pydantic_schemas.sections import SectionPatch
from src.domain.usecases.sections_usecases.patch_section_collector import (
    PatchSectionCollectorInterface,
)
from src.data.interfaces.courses_repository import CoursesRepositoryInterface
from src.data.interfaces.sections_repository import SectionsRepositoryInterface


class PatchSectionCollector(PatchSectionCollectorInterface):
    """Patch Section collector usecase"""

    def __init__(
        self,
        sections_repository: Type[SectionsRepositoryInterface],
        courses_repository: Type[CoursesRepositoryInterface],
    ) -> None:
        self.__sections_repository = sections_repository
        self.__courses_repository = courses_repository

    async def patch_section(
        self, db_session: AsyncSession, section_id: int, section: SectionPatch
    ) -> None:
        """
        Patch section model
        :param  - db_session: ORM database session
                - section: Section data for patch
        :returns - None for patch section event status
        """

        check_section_exists = await self.__sections_repository.get_section_by_id(
            db_session, section_id
        )

        if check_section_exists is None:
            raise HTTPException(status_code=404, detail="Course section not found")

        check_course_exists = await self.__courses_repository.get_course_by_id(
            db_session, course_id=section.course_id
        )

        if check_course_exists is None:
            raise HTTPException(status_code=404, detail="Course not found")

        await self.__sections_repository.patch_db_section(
            db_session, section_id=section_id, section=section
        )

        return
