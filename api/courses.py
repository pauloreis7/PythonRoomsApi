from typing import List

from fastapi import APIRouter, Path, Query, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db_setup import get_db
from pydantic_schemas.course import Course, CourseCreate, CoursePatch
from api.utils.users import get_user_by_id
from api.utils.courses import (
    get_course_by_id,
    get_course_by_title,
    get_courses,
    create_db_course,
    patch_db_course,
    delete_db_course,
)

courses_router = APIRouter()


@courses_router.get("/courses", response_model=List[Course])
async def read_courses(
    skip: int = Query(0, description="skip items in pagination"),
    limit: int = Query(100, description="limit items in pagination"),
    db_session: Session = Depends(get_db),
):
    """Get all courses list"""

    courses = get_courses(session=db_session, skip=skip, limit=limit)

    return courses


@courses_router.get("/courses/{course_id}", response_model=Course)
async def find_course(
    course_id: int = Path(..., description="Course id to retrieve", gt=0),
    db_session: Session = Depends(get_db),
):
    """Get a course"""

    check_course_exists = get_course_by_id(session=db_session, course_id=course_id)

    if check_course_exists is None:
        raise HTTPException(status_code=404, detail="Course not found")

    return check_course_exists


@courses_router.post("/courses", response_model=bool, status_code=201)
async def create_course(
    course: CourseCreate = Body(..., description="Course data to create"),
    db_session: Session = Depends(get_db),
):
    """Create a course"""

    check_course_exists = get_course_by_title(
        session=db_session, course_title=course.title
    )

    if check_course_exists:
        raise HTTPException(status_code=400, detail="Course already exists!")

    check_user_exists = get_user_by_id(session=db_session, user_id=course.user_id)

    if check_user_exists is None:
        raise HTTPException(status_code=404, detail="User not found")

    create_db_course_response = create_db_course(session=db_session, course=course)

    return create_db_course_response


@courses_router.patch("/courses/{course_id}", response_model=bool)
async def patch_course(
    course_id: int = Path(..., description="Course id to patch", gt=0),
    course: CoursePatch = Body(..., description="Course data to patch"),
    db_session: Session = Depends(get_db),
):
    """Patch a course"""

    check_course_exists = get_course_by_id(session=db_session, course_id=course_id)

    if check_course_exists is None:
        raise HTTPException(status_code=404, detail="Course not found")

    patch_db_course_response = patch_db_course(
        session=db_session, course_id=course_id, course=course
    )

    return patch_db_course_response


@courses_router.delete("/courses/{course_id}", response_model=bool)
async def delete_course(
    course_id: int = Path(..., description="Course id to delete", gt=0),
    db_session: Session = Depends(get_db),
):
    """Delete a course"""

    check_course_exists = get_course_by_id(session=db_session, course_id=course_id)

    if check_course_exists is None:
        raise HTTPException(status_code=404, detail="Course not found")

    delete_db_course_response = delete_db_course(
        session=db_session, course_id=course_id
    )

    return delete_db_course_response


# @courses_router.get("/courses/{id}/sections")
# async def read_course_sections():
#     """Get a course sections"""

#     return {"courses": []}
