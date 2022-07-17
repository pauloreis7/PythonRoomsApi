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
from src.presenters.controllers import (
    CreateCourseCollectorController,
)
from src.presenters.controllers import (
    FindCourseByIdCollectorController,
)
from src.presenters.controllers import (
    FindCourseSectionsCollectorController,
)
from src.presenters.controllers import (
    PaginateCoursesCollectorController,
)
from src.presenters.controllers import (
    DeleteCourseCollectorController,
)
from src.presenters.controllers import (
    PatchCourseCollectorController,
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
    controller = PaginateCoursesCollectorController(use_case)

    response = await controller.handle(db_session=db_session, skip=skip, limit=limit)

    return JSONResponse(
        status_code=response["status_code"], content=jsonable_encoder(response["data"])
    )


@courses_router.get("/courses/{course_id}", response_model=Course)
async def find_course(
    course_id: int = Path(..., description="Course id to retrieve", gt=0),
    db_session: AsyncSession = Depends(get_db),
):
    """Get a course"""

    infra = CoursesRepository()
    use_case = FindCourseByIdCollector(infra)
    controller = FindCourseByIdCollectorController(use_case)

    response = await controller.handle(db_session=db_session, course_id=course_id)

    return JSONResponse(
        status_code=response["status_code"], content=jsonable_encoder(response["data"])
    )


@courses_router.get("/courses/sections/{course_id}", response_model=List[Section])
async def read_course_sections(
    course_id: int = Path(..., description="Course id to retrieve sections", gt=0),
    db_session: AsyncSession = Depends(get_db),
):
    """Get course's sections"""

    courses_infra = CoursesRepository()
    sections_infra = SectionsRepository()
    use_case = FindCourseSectionsCollector(courses_infra, sections_infra)
    controller = FindCourseSectionsCollectorController(use_case)

    response = await controller.handle(db_session=db_session, course_id=course_id)

    return JSONResponse(
        status_code=response["status_code"], content=jsonable_encoder(response["data"])
    )


@courses_router.post("/courses", response_model=bool, status_code=201)
async def create_course(
    course: CourseCreate = Body(..., description="Course data to create"),
    db_session: AsyncSession = Depends(get_db),
):
    """Create a course"""

    courses_infra = CoursesRepository()
    users_infra = UsersRepository()
    use_case = CreateCourseCollector(courses_infra, users_infra)
    controller = CreateCourseCollectorController(use_case)

    response = await controller.handle(db_session=db_session, course=course)

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

    courses_infra = CoursesRepository()
    users_infra = UsersRepository()
    use_case = PatchCourseCollector(courses_infra, users_infra)
    controller = PatchCourseCollectorController(use_case)

    response = await controller.handle(
        db_session=db_session, course_id=course_id, course=course
    )

    return Response(status_code=response["status_code"])


@courses_router.delete("/courses/{course_id}", status_code=204)
async def delete_course(
    course_id: int = Path(..., description="Course id to delete", gt=0),
    db_session: AsyncSession = Depends(get_db),
):
    """Delete a course"""

    infra = CoursesRepository()
    use_case = DeleteCourseCollector(infra)
    controller = DeleteCourseCollectorController(use_case)

    response = await controller.handle(db_session=db_session, course_id=course_id)

    return Response(status_code=response["status_code"])
