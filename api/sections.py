from typing import List

from fastapi import APIRouter, Depends, Body, Path, Query, Response, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.config.connection import get_db
from pydantic_schemas.sections import Section, SectionCreate, SectionPatch
from api.utils.courses import get_course_by_id
from api.utils.sections import (
    get_section_by_id,
    get_sections_by_title,
    create_db_section,
    patch_db_section,
    delete_db_section,
)

sections_router = APIRouter()


@sections_router.get("/sections/{section_id}", response_model=Section)
async def find_section(
    section_id: int = Path(..., description="Section id to retrieve", gt=0),
    db_session: AsyncSession = Depends(get_db),
):
    """Get a section"""

    check_session_exists = await get_section_by_id(db_session, section_id=section_id)

    if check_session_exists is None:
        raise HTTPException(status_code=404, detail="Course section not found")

    return check_session_exists


@sections_router.get("/sections", response_model=List[Section])
async def read_section_by_title(
    sections_title: str = Query(..., description="Sections title to retrieve"),
    db_session: AsyncSession = Depends(get_db),
):
    """Get all sections by title"""

    sections = await get_sections_by_title(db_session, sections_title=sections_title)

    return sections


@sections_router.post("/sections", response_model=bool, status_code=201)
async def create_section(
    section: SectionCreate = Body(..., description="Course section data to create"),
    db_session: AsyncSession = Depends(get_db),
):
    """Create a section"""

    check_course_exists = await get_course_by_id(
        db_session, course_id=section.course_id
    )

    if check_course_exists is None:
        raise HTTPException(status_code=404, detail="Course not found")

    create_db_section_response = await create_db_section(db_session, section=section)

    return create_db_section_response


@sections_router.patch("/sections/{section_id}", status_code=204)
async def patch_section(
    section_id: int = Path(..., description="Section id to patch", gt=0),
    section: SectionPatch = Body(..., description="Section data to patch"),
    db_session: AsyncSession = Depends(get_db),
):

    """Patch a section"""

    check_section_exists = await get_section_by_id(db_session, section_id=section_id)

    if check_section_exists is None:
        raise HTTPException(status_code=404, detail="Course section not found")

    await patch_db_section(db_session, section_id=section_id, section=section)

    return Response(status_code=204)


@sections_router.delete("/sections/{section_id}", status_code=204)
async def delete_section(
    section_id: int = Path(..., description="Section id to delete", gt=0),
    db_session: AsyncSession = Depends(get_db),
):
    """Delete a section"""

    check_section_exists = await get_section_by_id(db_session, section_id=section_id)

    if check_section_exists is None:
        raise HTTPException(status_code=404, detail="Course section not found")

    await delete_db_section(db_session, section_id=section_id)

    return Response(status_code=204)
