from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.course import Section
from src.pydantic_schemas.sections import SectionCreate, SectionPatch


async def get_section_by_id(db_session: AsyncSession, section_id: int):
    """Get a section by id"""

    query = select(Section).where(Section.id == section_id)

    query_response = await db_session.execute(query)

    section = query_response.scalars().first()

    return section


async def get_sections_by_title(db_session: AsyncSession, sections_title: str):
    """Get sections by title"""

    query = select(Section).where(Section.title == sections_title)

    query_response = await db_session.execute(query)

    sections = query_response.scalars().all()

    return sections


async def get_course_sections(db_session: AsyncSession, course_id: str):
    """Get a course's sections"""

    query = select(Section).where(Section.course_id == course_id)

    query_response = await db_session.execute(query)

    sections = query_response.scalars().all()

    return sections


async def create_db_section(db_session: AsyncSession, section: SectionCreate):
    """Create a section"""

    query = insert(Section).values(
        title=section.title,
        description=section.description,
        content_type=section.content_type,
        grade_media=section.grade_media,
        course_id=section.course_id,
    )

    await db_session.execute(query)

    await db_session.commit()

    return True


async def patch_db_section(
    db_session: AsyncSession, section_id: int, section: SectionPatch
):
    """Patch a section"""

    query = (
        update(Section)
        .where(Section.id == section_id)
        .values(
            title=section.title,
            description=section.description,
            content_type=section.content_type,
            grade_media=section.grade_media,
        )
    )

    await db_session.execute(query)

    await db_session.commit()

    return


async def delete_db_section(db_session: AsyncSession, section_id: int):
    """Delete a section"""

    query = delete(Section).where(Section.id == section_id)

    await db_session.execute(query)

    await db_session.commit()

    return
