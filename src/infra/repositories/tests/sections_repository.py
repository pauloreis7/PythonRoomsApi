from typing import List
from faker import Faker
from httpx import AsyncClient

from src.pydantic_schemas.sections import SectionCreate, SectionPatch


fake = Faker()


def mock_sections():
    """
    mock data for sections
    :return - list with sections dict
    """

    return [
        {
            "id": 1,
            "course_id": 1,
            "title": fake.sentence(),
            "content_type": 1,
            "description": fake.text(),
            "grade_media": 5,
            "created_at": fake.date_time(),
            "updated_at": fake.date_time(),
        },
        {
            "id": 2,
            "course_id": 1,
            "title": fake.sentence(),
            "content_type": 2,
            "description": fake.text(),
            "grade_media": 10,
            "created_at": fake.date_time(),
            "updated_at": fake.date_time(),
        },
        {
            "id": 3,
            "course_id": 1,
            "title": fake.sentence(),
            "content_type": 3,
            "description": fake.text(),
            "grade_media": 1,
            "created_at": fake.date_time(),
            "updated_at": fake.date_time(),
        },
    ]


class SectionsRepositorySpy:
    """Spy to sections repository"""

    def __init__(self) -> None:
        self.get_section_by_id_attributes = {}
        self.get_sections_by_title_attributes = {}
        self.get_course_sections_attributes = {}
        self.create_db_section_attributes = {}
        self.patch_db_section_attributes = {}
        self.delete_db_section_attributes = {}

    async def get_section_by_id(self, _: AsyncClient, section_id: int) -> dict:
        """Get a section by id test"""

        self.get_section_by_id_attributes["section_id"] = section_id

        sections = mock_sections()

        check_section_exists = None

        for section in sections:
            if section["id"] == section_id:
                check_section_exists = section
                break

        return check_section_exists

    async def get_sections_by_title(
        self, _: AsyncClient, sections_title: str
    ) -> List[dict]:
        """Get sections by title test"""

        self.get_sections_by_title_attributes["sections_title"] = sections_title

        sections = mock_sections()

        check_section_exists = None

        for section in sections:
            if section["title"] == sections_title:
                check_section_exists = section
                break

        return check_section_exists

    async def get_course_sections(self, _: AsyncClient, course_id: str) -> List[dict]:
        """Get a course's sections test"""

        self.get_course_sections_attributes["course_id"] = course_id

        sections = mock_sections()

        courses_sections = []

        for section in sections:
            if section["course_id"] == course_id:
                courses_sections.append(section)
                break

        return courses_sections

    async def create_db_section(self, _: AsyncClient, section: SectionCreate) -> bool:
        """Create a section test"""

        self.create_db_section_attributes["title"] = section.title
        self.create_db_section_attributes["description"] = section.description
        self.create_db_section_attributes["content_type"] = section.content_type
        self.create_db_section_attributes["grade_media"] = section.grade_media
        self.create_db_section_attributes["course_id"] = section.course_id

        return True

    async def patch_db_section(
        self, _: AsyncClient, section_id: int, section: SectionPatch
    ) -> None:
        """Patch a section test"""

        self.patch_db_section_attributes["section_id"] = section_id
        self.patch_db_section_attributes["title"] = section.title
        self.patch_db_section_attributes["description"] = section.description
        self.patch_db_section_attributes["content_type"] = section.content_type
        self.patch_db_section_attributes["grade_media"] = section.grade_media
        self.patch_db_section_attributes["course_id"] = section.course_id

        sections_mock = mock_sections()

        for section_mock in sections_mock:
            if section_mock["id"] == section_id:
                section_mock = section
                break

        return

    async def delete_db_section(self, _: AsyncClient, section_id: int) -> None:
        """Delete a section test"""

        self.delete_db_section_attributes["section_id"] = section_id

        sections = mock_sections()

        for index, _ in enumerate(sections):
            if sections[index]["id"] == section_id:
                del sections[index]
                break

        return
