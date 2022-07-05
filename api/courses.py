from typing import List
from xmlrpc.client import Boolean

from fastapi import APIRouter, Path, Query, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db_setup import get_db
from pydantic_schemas.course import Course, CourseCreate, CoursePatch
from api.utils.courses import (
    get_course,
    get_courses,
    create_course,
    patch_course,
    delete_db_course,
)

courses_router = APIRouter()


@courses_router.get("/courses", response_model=List[Course])
async def read_courses(
    skip: int = Query(0, description="skip items in pagination"),
    limit: int = Query(100, description="limit items in pagination"),
    db: Session = Depends(get_db),
):
    """Get all courses list"""

    courses = get_courses(db=db, skip=skip, limit=limit)

    return courses


@courses_router.post("/courses", response_model=Course)
async def create_new_course(course: CourseCreate, db: Session = Depends(get_db)):
    """Create a course"""

    return create_course(db=db, course=course)


@courses_router.get("/courses/{course_id}", response_model=Course)
async def read_course(course_id: int, db: Session = Depends(get_db)):
    """Get a course"""

    db_course = get_course(db=db, course_id=course_id)

    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    return db_course


@courses_router.patch("/courses/{course_id}", response_model=Boolean)
async def update_course(
    course_id: int = Path(..., description="Course id to update", gt=0),
    course: CoursePatch = Body(..., description="Course data to update"),
    db: Session = Depends(get_db),
):
    """Update a course"""

    db_course = get_course(db=db, course_id=course_id)

    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    db_patch_course = patch_course(db=db, course_id=course_id, course=course)

    return db_patch_course


@courses_router.delete("/courses/{course_id}", response_model=Boolean)
async def delete_course(
    course_id: int = Path(..., description="Course id to delete", gt=0),
    db: Session = Depends(get_db),
):
    """Delete a course"""

    db_course = get_course(db=db, course_id=course_id)

    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    db_delete_course = delete_db_course(db=db, course_id=course_id)

    return db_delete_course


@courses_router.get("/courses/{id}/sections")
async def read_course_sections():
    """Get a course sections"""

    return {"courses": []}
