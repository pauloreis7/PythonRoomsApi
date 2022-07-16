from typing import List

from fastapi import APIRouter, Depends, Body, Path, Query, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.pydantic_schemas.course import Course, CourseCreate, CoursePatch
from src.pydantic_schemas.sections import Section
from src.infra.config.connection import get_db
from src.infra.repositories.sections_repository import SectionsRepository
from src.infra.repositories.users_repository import UsersRepository
from src.infra.repositories.courses_repository import CoursesRepository
from src.data.usecases.courses_usecases.paginate_courses_collector import (
    PaginateCoursesCollector,
)
from src.data.usecases.courses_usecases.find_course_by_id_collector import (
    FindCourseByIdCollector,
)
from src.data.usecases.courses_usecases.find_course_sections_collector import (
    FindCourseSectionsCollector,
)
from src.data.usecases.courses_usecases.create_course_collector import (
    CreateCourseCollector,
)
from src.data.usecases.courses_usecases.patch_course_collector import (
    PatchCourseCollector,
)
from src.data.usecases.courses_usecases.delete_course_collector import (
    DeleteCourseCollector,
)

courses_router = APIRouter()


@courses_router.get("/courses", response_model=List[Course])
async def read_courses(
    skip: int = Query(0, description="skip items in pagination"),
    limit: int = Query(100, description="limit items in pagination"),
    db_session: AsyncSession = Depends(get_db),
):
    """Get all courses list"""

    infra = CoursesRepository()
    use_case = PaginateCoursesCollector(infra)

    courses = await use_case.paginate_courses(db_session, skip=skip, limit=limit)

    return JSONResponse(status_code=200, content=jsonable_encoder(courses))


@courses_router.get("/courses/{course_id}", response_model=Course)
async def find_course(
    course_id: int = Path(..., description="Course id to retrieve", gt=0),
    db_session: AsyncSession = Depends(get_db),
):
    """Get a course"""

    infra = CoursesRepository()
    use_case = FindCourseByIdCollector(infra)

    course = await use_case.find_course_by_id(db_session, course_id=course_id)

    return JSONResponse(status_code=200, content=jsonable_encoder(course))


@courses_router.get("/courses/sections/{course_id}", response_model=List[Section])
async def read_course_sections(
    course_id: int = Path(..., description="Course id to retrieve sections", gt=0),
    db_session: AsyncSession = Depends(get_db),
):
    """Get course's sections"""

    courses_infra = CoursesRepository()
    sections_infra = SectionsRepository()
    use_case = FindCourseSectionsCollector(courses_infra, sections_infra)

    course_sections = await use_case.find_course_sections(
        db_session, course_id=course_id
    )

    return JSONResponse(status_code=200, content=jsonable_encoder(course_sections))


@courses_router.post("/courses", response_model=bool, status_code=201)
async def create_course(
    course: CourseCreate = Body(..., description="Course data to create"),
    db_session: AsyncSession = Depends(get_db),
):
    """Create a course"""

    courses_infra = CoursesRepository()
    users_infra = UsersRepository()
    use_case = CreateCourseCollector(courses_infra, users_infra)

    create_course_response = await use_case.create_course(db_session, course=course)

    return JSONResponse(
        status_code=201, content=jsonable_encoder(create_course_response)
    )


@courses_router.patch("/courses/{course_id}", status_code=204)
async def patch_course(
    course_id: int = Path(..., description="Course id to patch", gt=0),
    course: CoursePatch = Body(..., description="Course data to patch"),
    db_session: AsyncSession = Depends(get_db),
):
    """Patch a course"""

    courses_infra = CoursesRepository()
    users_infra = UsersRepository()
    use_case = PatchCourseCollector(courses_infra, users_infra)

    await use_case.patch_course(db_session, course_id=course_id, course=course)

    return Response(status_code=204)


@courses_router.delete("/courses/{course_id}", status_code=204)
async def delete_course(
    course_id: int = Path(..., description="Course id to delete", gt=0),
    db_session: AsyncSession = Depends(get_db),
):
    """Delete a course"""

    infra = CoursesRepository()
    use_case = DeleteCourseCollector(infra)

    await use_case.delete_course(db_session, course_id=course_id)

    return Response(status_code=204)
