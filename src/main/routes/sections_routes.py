from typing import List

from fastapi import APIRouter, Depends, Body, Path, Query, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.pydantic_schemas.sections import Section, SectionCreate, SectionPatch
from src.infra.config.connection import get_db
from src.infra.repositories.courses_repository import CoursesRepository
from src.infra.repositories.sections_repository import SectionsRepository
from src.data.usecases.sections_usecases.find_section_by_id_collector import (
    FindSectionByIdCollector,
)
from src.data.usecases.sections_usecases.find_sections_by_title_collector import (
    FindSectionsByTitleCollector,
)
from src.data.usecases.sections_usecases.create_section_collector import (
    CreateSectionCollector,
)
from src.data.usecases.sections_usecases.patch_section_collector import (
    PatchSectionCollector,
)
from src.data.usecases.sections_usecases.delete_section_collector import (
    DeleteSectionCollector,
)

sections_router = APIRouter()


@sections_router.get("/sections/{section_id}", response_model=Section)
async def find_section(
    section_id: int = Path(..., description="Section id to retrieve", gt=0),
    db_session: AsyncSession = Depends(get_db),
):
    """Get a section"""

    infra = SectionsRepository()
    use_case = FindSectionByIdCollector(infra)

    section = await use_case.find_section_by_id(db_session, section_id=section_id)

    return JSONResponse(status_code=200, content=jsonable_encoder(section))


@sections_router.get("/sections", response_model=List[Section])
async def read_section_by_title(
    sections_title: str = Query(..., description="Sections title to retrieve"),
    db_session: AsyncSession = Depends(get_db),
):
    """Get all sections by title"""

    infra = SectionsRepository()
    use_case = FindSectionsByTitleCollector(infra)

    sections = await use_case.find_sections_by_title(
        db_session, sections_title=sections_title
    )

    return JSONResponse(status_code=200, content=jsonable_encoder(sections))


@sections_router.post("/sections", response_model=bool, status_code=201)
async def create_section(
    section: SectionCreate = Body(..., description="Course section data to create"),
    db_session: AsyncSession = Depends(get_db),
):
    """Create a section"""

    sections_infra = SectionsRepository()
    courses_infra = CoursesRepository()
    use_case = CreateSectionCollector(sections_infra, courses_infra)

    create_section_response = await use_case.create_section(db_session, section=section)

    return JSONResponse(
        status_code=201, content=jsonable_encoder(create_section_response)
    )


@sections_router.patch("/sections/{section_id}", status_code=204)
async def patch_section(
    section_id: int = Path(..., description="Section id to patch", gt=0),
    section: SectionPatch = Body(..., description="Section data to patch"),
    db_session: AsyncSession = Depends(get_db),
):

    """Patch a section"""

    sections_infra = SectionsRepository()
    courses_infra = CoursesRepository()
    use_case = PatchSectionCollector(sections_infra, courses_infra)

    await use_case.patch_section(db_session, section_id=section_id, section=section)

    return Response(status_code=204)


@sections_router.delete("/sections/{section_id}", status_code=204)
async def delete_section(
    section_id: int = Path(..., description="Section id to delete", gt=0),
    db_session: AsyncSession = Depends(get_db),
):
    """Delete a section"""

    infra = SectionsRepository()
    use_case = DeleteSectionCollector(infra)

    await use_case.delete_section(db_session, section_id=section_id)

    return Response(status_code=204)
