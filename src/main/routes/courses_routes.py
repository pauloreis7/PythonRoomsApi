from typing import List

from fastapi import APIRouter, Depends, Body, Path, Query, Response, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.pydantic_schemas.course import Course, CourseCreate, CoursePatch
from src.pydantic_schemas.sections import Section
from src.infra.config.connection import get_db
from src.infra.repositories.sections_repository import SectionsRepository
from src.infra.repositories.users_repository import UsersRepository
from src.infra.repositories.courses_repository import CoursesRepository

courses_router = APIRouter()


@courses_router.get("/courses", response_model=List[Course])
async def read_courses(
    skip: int = Query(0, description="skip items in pagination"),
    limit: int = Query(100, description="limit items in pagination"),
    db_session: AsyncSession = Depends(get_db),
):
    """Get all courses list"""

    courses_repository = CoursesRepository()

    courses = await courses_repository.get_courses(db_session, skip=skip, limit=limit)

    return JSONResponse(status_code=200, content=jsonable_encoder(courses))


@courses_router.get("/courses/{course_id}", response_model=Course)
async def find_course(
    course_id: int = Path(..., description="Course id to retrieve", gt=0),
    db_session: AsyncSession = Depends(get_db),
):
    """Get a course"""

    courses_repository = CoursesRepository()

    check_course_exists = await courses_repository.get_course_by_id(
        db_session, course_id=course_id
    )

    if check_course_exists is None:
        raise HTTPException(status_code=404, detail="Course not found")

    return JSONResponse(status_code=200, content=jsonable_encoder(check_course_exists))


@courses_router.get("/courses/sections/{course_id}", response_model=List[Section])
async def read_course_sections(
    course_id: int = Path(..., description="Course id to retrieve sections", gt=0),
    db_session: AsyncSession = Depends(get_db),
):
    """Get course's sections"""

    courses_repository = CoursesRepository()
    sections_repository = SectionsRepository()

    check_course_exists = await courses_repository.get_course_by_id(
        db_session, course_id=course_id
    )

    if check_course_exists is None:
        raise HTTPException(status_code=404, detail="Course not found")

    course_sections_response = await sections_repository.get_course_sections(
        db_session, course_id=course_id
    )

    return JSONResponse(
        status_code=200, content=jsonable_encoder(course_sections_response)
    )


@courses_router.post("/courses", response_model=bool, status_code=201)
async def create_course(
    course: CourseCreate = Body(..., description="Course data to create"),
    db_session: AsyncSession = Depends(get_db),
):
    """Create a course"""

    courses_repository = CoursesRepository()
    users_repository = UsersRepository()

    check_course_exists = await courses_repository.get_course_by_title(
        db_session, course_title=course.title
    )

    if check_course_exists:
        raise HTTPException(status_code=400, detail="Course already exists!")

    check_user_exists = await users_repository.get_user_by_id(
        db_session, user_id=course.user_id
    )

    if check_user_exists is None:
        raise HTTPException(status_code=404, detail="User not found")

    create_db_course_response = await courses_repository.create_db_course(
        db_session, course=course
    )

    return JSONResponse(
        status_code=201, content=jsonable_encoder(create_db_course_response)
    )


@courses_router.patch("/courses/{course_id}", status_code=204)
async def patch_course(
    course_id: int = Path(..., description="Course id to patch", gt=0),
    course: CoursePatch = Body(..., description="Course data to patch"),
    db_session: AsyncSession = Depends(get_db),
):
    """Patch a course"""

    courses_repository = CoursesRepository()

    check_course_exists = await courses_repository.get_course_by_id(
        db_session, course_id=course_id
    )

    if check_course_exists is None:
        raise HTTPException(status_code=404, detail="Course not found")

    await courses_repository.patch_db_course(
        db_session, course_id=course_id, course=course
    )

    return Response(status_code=204)


@courses_router.delete("/courses/{course_id}", status_code=204)
async def delete_course(
    course_id: int = Path(..., description="Course id to delete", gt=0),
    db_session: AsyncSession = Depends(get_db),
):
    """Delete a course"""

    courses_repository = CoursesRepository()

    check_course_exists = await courses_repository.get_course_by_id(
        db_session, course_id=course_id
    )

    if check_course_exists is None:
        raise HTTPException(status_code=404, detail="Course not found")

    await courses_repository.delete_db_course(db_session, course_id=course_id)

    return Response(status_code=204)
