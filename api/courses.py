from fastapi import APIRouter

courses_router = APIRouter()


@courses_router.get("/courses")
async def read_courses():
    """Get all courses list"""

    return {"courses": []}


@courses_router.post("/courses")
async def create_course_api():
    """Create a course"""

    return {"courses": []}


@courses_router.get("/courses/{id}")
async def read_course():
    """Get a course"""

    return {"courses": []}


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
