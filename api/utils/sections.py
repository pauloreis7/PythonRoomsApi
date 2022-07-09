from sqlalchemy.orm import Session

from database.models.course import Section
from pydantic_schemas.sections import SectionCreate, SectionPatch


def get_section_by_id(session: Session, section_id: int):
    """Get a section by id"""

    section = session.query(Section).filter(Section.id == section_id).first()

    return section


def get_sections_by_title(session: Session, title: str):
    """Get sections by title"""

    sections = session.query(Section).filter(Section.title == title).all()

    return sections


def get_course_sections(session: Session, course_id: str):
    """Get a course's sections"""

    sections = session.query(Section).filter(Section.course_id == course_id).all()

    return sections


def create_section(session: Session, section: SectionCreate):
    """Create a section"""

    create_section = Section(
        title=section.title,
        description=section.description,
        type=section.type,
        grade_media=section.grade_media,
        course_id=section.course_id,
    )

    session.add(create_section)
    session.commit()
    session.refresh(create_section)

    return True


def patch_section(session: Session, section_id: int, section: SectionPatch):
    """Patch a section"""

    session.query(Section).filter(Section.id == section_id).update(
        {
            Section.title: section.title,
            Section.description: section.description,
            Section.type: section.type,
            Section.grade_media: section.grade_media,
        }
    )

    session.commit()

    return True


def delete_db_section(session: Session, section_id: int):
    """Delete a section"""

    session.query(Section).filter(Section.id == section_id).delete()

    session.commit()

    return True
