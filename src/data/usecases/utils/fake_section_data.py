from faker import Faker

from src.pydantic_schemas.sections import SectionCreate

fake = Faker()


def create_fake_section(course_id: int = 1):
    """Util to create a fake section"""

    section = SectionCreate(
        title=fake.sentence(),
        description=fake.text(),
        content_type=1,
        grade_media=fake.random_int(),
        course_id=course_id,
    )

    return section
