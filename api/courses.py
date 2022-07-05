from typing import List

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db_setup import get_db
from pydantic_schemas.course import Course, CourseCreate
from api.utils.courses import get_course, get_courses, create_course

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


@courses_router.patch("/courses/{id}")
async def update_course():
    """Update a course"""

    return {"courses": []}


@courses_router.delete("/courses/{id}")
async def delete_course():
    """Delete a course"""

    return {"courses": []}


@courses_router.get("/courses/{id}/sections")
async def read_course_sections():
    """Get a course sections"""

    return {"courses": []}
