from typing import List
from faker import Faker
from httpx import AsyncClient

from src.domain.models.sections import Section, SectionCreate, SectionPatch
from src.data.interfaces.sections_repository import SectionsRepositoryInterface

fake = Faker()


class SectionsRepositorySpy(SectionsRepositoryInterface):
    """Spy to sections repository"""

    def __init__(self) -> None:
        self.sections: List[Section] = []
        self.get_section_by_id_attributes = {}
        self.get_sections_by_title_attributes = {}
        self.get_course_sections_attributes = {}
        self.create_db_section_attributes = {}
        self.patch_db_section_attributes = {}
        self.delete_db_section_attributes = {}

    async def get_section_by_id(self, _: AsyncClient, section_id: int) -> Section:
        """Get a section by id test"""

        self.get_section_by_id_attributes["section_id"] = section_id

        check_section_exists = None

        for section in self.sections:
            if section.id == section_id:
                check_section_exists = section
                break

        return check_section_exists

    async def get_sections_by_title(
        self, _: AsyncClient, sections_title: str
    ) -> List[Section]:
        """Get sections by title test"""

        self.get_sections_by_title_attributes["sections_title"] = sections_title

        sections = []

        for section in self.sections:
            if section.title == sections_title:
                sections.append(section)

        return sections

    async def get_course_sections(
        self, _: AsyncClient, course_id: str
    ) -> List[Section]:
        """Get a course's sections test"""

        self.get_course_sections_attributes["course_id"] = course_id

        courses_sections = []

        for section in self.sections:
            if section.course_id == course_id:
                courses_sections.append(section)

        return courses_sections

    async def create_db_section(
        self, _: AsyncClient, section: SectionCreate
    ) -> Section:
        """Create a section test"""

        self.create_db_section_attributes["title"] = section.title
        self.create_db_section_attributes["description"] = section.description
        self.create_db_section_attributes["content_type"] = section.content_type
        self.create_db_section_attributes["grade_media"] = section.grade_media
        self.create_db_section_attributes["course_id"] = section.course_id

        fake_section = Section(
            id=fake.random_int(),
            title=section.title,
            description=section.description,
            content_type=section.content_type,
            grade_media=section.grade_media,
            course_id=section.course_id,
            created_at=fake.date_time(),
            updated_at=fake.date_time(),
        )

        self.sections.append(fake_section)

        return fake_section

    async def patch_db_section(
        self, _: AsyncClient, section_id: int, section: SectionPatch
    ) -> Section:
        """Patch a section test"""

        self.patch_db_section_attributes["section_id"] = section_id
        self.patch_db_section_attributes["title"] = section.title
        self.patch_db_section_attributes["description"] = section.description
        self.patch_db_section_attributes["content_type"] = section.content_type
        self.patch_db_section_attributes["grade_media"] = section.grade_media
        self.patch_db_section_attributes["course_id"] = section.course_id

        fake_section = {
            "title": section.title,
            "description": section.description,
            "content_type": section.content_type,
            "grade_media": section.grade_media,
            "course_id": section.course_id,
        }

        for index, section_mock in enumerate(self.sections):
            if section_mock.id == section_id:
                self.sections[index].title = fake_section["title"]
                self.sections[index].description = fake_section["description"]
                self.sections[index].content_type = fake_section["content_type"]
                self.sections[index].grade_media = fake_section["grade_media"]
                self.sections[index].course_id = fake_section["course_id"]

                break

        return fake_section

    async def delete_db_section(self, _: AsyncClient, section_id: int) -> None:
        """Delete a section test"""

        self.delete_db_section_attributes["section_id"] = section_id

        for index, _ in enumerate(self.sections):
            if self.sections[index].id == section_id:
                del self.sections[index]
                break

        return
