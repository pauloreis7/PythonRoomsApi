from typing import List

from fastapi import APIRouter, Depends, Body, Path, Query, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession


from src.pydantic_schemas.sections import Section, SectionCreate, SectionPatch
from src.infra.config.connection import get_db
from src.presenters.errors.error_controller import handle_errors
from src.main.composers.sections_composers.find_section_by_id_composer import (
    find_section_by_id_composer,
)
from src.main.composers.sections_composers.find_sections_by_title_composer import (
    find_sections_by_title_composer,
)
from src.main.composers.sections_composers.create_section_composer import (
    create_section_composer,
)
from src.main.composers.sections_composers.patch_section_composer import (
    patch_section_composer,
)
from src.main.composers.sections_composers.delete_section_composer import (
    delete_section_composer,
)


sections_router = APIRouter()


@sections_router.get("/sections/{section_id}", response_model=Section)
async def find_section(
    section_id: int = Path(..., description="Section id to retrieve", gt=0),
    db_session: AsyncSession = Depends(get_db),
):
    """Get a section"""

    response = None
    find_section_by_id_controller = find_section_by_id_composer()

    try:
        response = await find_section_by_id_controller.handle(
            db_session=db_session, section_id=section_id
        )
    except Exception as error:
        response = handle_errors(error)

    return JSONResponse(
        status_code=response["status_code"], content=jsonable_encoder(response["data"])
    )


@sections_router.get("/sections", response_model=List[Section])
async def read_section_by_title(
    sections_title: str = Query(..., description="Sections title to retrieve"),
    db_session: AsyncSession = Depends(get_db),
):
    """Get all sections by title"""

    response = None
    find_sections_by_title_controller = find_sections_by_title_composer()

    try:
        response = await find_sections_by_title_controller.handle(
            db_session=db_session, sections_title=sections_title
        )
    except Exception as error:
        response = handle_errors(error)

    return JSONResponse(
        status_code=response["status_code"], content=jsonable_encoder(response["data"])
    )


@sections_router.post("/sections", response_model=bool, status_code=201)
async def create_section(
    section: SectionCreate = Body(..., description="Course section data to create"),
    db_session: AsyncSession = Depends(get_db),
):
    """Create a section"""

    response = None
    create_section_controller = create_section_composer()

    try:
        response = await create_section_controller.handle(
            db_session=db_session, section=section
        )
    except Exception as error:
        response = handle_errors(error)

    return JSONResponse(
        status_code=response["status_code"], content=jsonable_encoder(response["data"])
    )


@sections_router.patch("/sections/{section_id}", status_code=204)
async def patch_section(
    section_id: int = Path(..., description="Section id to patch", gt=0),
    section: SectionPatch = Body(..., description="Section data to patch"),
    db_session: AsyncSession = Depends(get_db),
):

    """Patch a section"""

    response = None
    patch_section_controller = patch_section_composer()

    try:
        response = await patch_section_controller.handle(
            db_session=db_session, section_id=section_id, section=section
        )
    except Exception as error:
        response = handle_errors(error)

    return Response(status_code=response["status_code"])


@sections_router.delete("/sections/{section_id}", status_code=204)
async def delete_section(
    section_id: int = Path(..., description="Section id to delete", gt=0),
    db_session: AsyncSession = Depends(get_db),
):
    """Delete a section"""

    response = None
    delete_section_controller = delete_section_composer()

    try:
        response = await delete_section_controller.handle(
            db_session=db_session, section_id=section_id
        )
    except Exception as error:
        response = handle_errors(error)

    return Response(status_code=response["status_code"])
