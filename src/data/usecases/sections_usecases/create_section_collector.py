from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.pydantic_schemas.sections import Section, SectionCreate
from src.domain.usecases.sections_usecases.create_section_collector import (
    CreateSectionCollectorInterface,
)
from src.data.interfaces.courses_repository import CoursesRepositoryInterface
from src.data.interfaces.sections_repository import SectionsRepositoryInterface
from src.errors.http_request_error import HttpRequestError


class CreateSectionCollector(CreateSectionCollectorInterface):
    """Create Section collector usecase"""

    def __init__(
        self,
        sections_repository: Type[SectionsRepositoryInterface],
        courses_repository: Type[CoursesRepositoryInterface],
    ) -> None:
        self.__sections_repository = sections_repository
        self.__courses_repository = courses_repository

    async def create_section(
        self, db_session: AsyncSession, section: SectionCreate
    ) -> Section:
        """
        Create section model
        :param  - db_session: ORM database session
                - section: Section data for create
        :returns - Boolean for create section event status
        """

        check_course_exists = await self.__courses_repository.get_course_by_id(
            db_session, course_id=section.course_id
        )

        if check_course_exists is None:
            raise HttpRequestError(status_code=404, detail="Course not found")

        api_response = await self.__sections_repository.create_db_section(
            db_session, section
        )

        return api_response
