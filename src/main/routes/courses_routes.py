from typing import List

from fastapi import APIRouter, Depends, Body, Path, Query, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.pydantic_schemas.course import Course, CourseCreate, CoursePatch
from src.pydantic_schemas.sections import Section
from src.infra.config.connection import get_db
from src.main.composers.courses_composers.paginate_courses_composer import (
    paginate_courses_composer,
)
from src.main.composers.courses_composers.find_course_by_id_composer import (
    find_course_by_id_composer,
)
from src.main.composers.courses_composers.find_course_sections_composer import (
    find_course_sections_composer,
)
from src.main.composers.courses_composers.create_course_composer import (
    create_course_composer,
)
from src.main.composers.courses_composers.patch_course_composer import (
    patch_course_composer,
)
from src.main.composers.courses_composers.delete_course_composer import (
    delete_course_composer,
)

courses_router = APIRouter()


@courses_router.get("/courses", response_model=List[Course])
async def read_courses(
    skip: int = Query(0, description="skip items in pagination"),
    limit: int = Query(100, description="limit items in pagination"),
    db_session: AsyncSession = Depends(get_db),
):
    """Get all courses list"""

    paginate_courses_controller = paginate_courses_composer()

    response = await paginate_courses_controller.handle(
        db_session=db_session, skip=skip, limit=limit
    )

    return JSONResponse(
        status_code=response["status_code"], content=jsonable_encoder(response["data"])
    )


@courses_router.get("/courses/{course_id}", response_model=Course)
async def find_course(
    course_id: int = Path(..., description="Course id to retrieve", gt=0),
    db_session: AsyncSession = Depends(get_db),
):
    """Get a course"""

    find_course_by_id_controller = find_course_by_id_composer()

    response = await find_course_by_id_controller.handle(
        db_session=db_session, course_id=course_id
    )

    return JSONResponse(
        status_code=response["status_code"], content=jsonable_encoder(response["data"])
    )


@courses_router.get("/courses/sections/{course_id}", response_model=List[Section])
async def read_course_sections(
    course_id: int = Path(..., description="Course id to retrieve sections", gt=0),
    db_session: AsyncSession = Depends(get_db),
):
    """Get course's sections"""

    find_course_sections_controller = find_course_sections_composer()

    response = await find_course_sections_controller.handle(
        db_session=db_session, course_id=course_id
    )

    return JSONResponse(
        status_code=response["status_code"], content=jsonable_encoder(response["data"])
    )


@courses_router.post("/courses", response_model=bool, status_code=201)
async def create_course(
    course: CourseCreate = Body(..., description="Course data to create"),
    db_session: AsyncSession = Depends(get_db),
):
    """Create a course"""

    create_course_controller = create_course_composer()

    response = await create_course_controller.handle(
        db_session=db_session, course=course
    )

    return JSONResponse(
        status_code=response["status_code"], content=jsonable_encoder(response["data"])
    )


@courses_router.patch("/courses/{course_id}", status_code=204)
async def patch_course(
    course_id: int = Path(..., description="Course id to patch", gt=0),
    course: CoursePatch = Body(..., description="Course data to patch"),
    db_session: AsyncSession = Depends(get_db),
):
    """Patch a course"""

    patch_course_controller = patch_course_composer()

    response = await patch_course_controller.handle(
        db_session=db_session, course_id=course_id, course=course
    )

    return Response(status_code=response["status_code"])


@courses_router.delete("/courses/{course_id}", status_code=204)
async def delete_course(
    course_id: int = Path(..., description="Course id to delete", gt=0),
    db_session: AsyncSession = Depends(get_db),
):
    """Delete a course"""

    delete_course_controller = delete_course_composer()

    response = await delete_course_controller.handle(
        db_session=db_session, course_id=course_id
    )

    return Response(status_code=response["status_code"])
