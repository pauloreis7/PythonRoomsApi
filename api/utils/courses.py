from sqlalchemy import select, insert, update, delete

from api.config.connection import session
from database.models.course import Course
from pydantic_schemas.course import CourseCreate, CoursePatch


async def get_courses(skip: int = 0, limit: int = 100):
    """Get all courses list"""

    async with session() as db_session:
        query = select(Course).offset(skip).limit(limit)

        query_response = await db_session.execute(query)

        courses = query_response.scalars().all()

        return courses


async def get_course_by_id(course_id: int):
    """Get a course by id"""

    async with session() as db_session:
        query = select(Course).where(Course.id == course_id)

        query_response = await db_session.execute(query)

        course = query_response.scalars().first()

        return course


async def get_course_by_title(course_title: str):
    """Get a course by title"""

    async with session() as db_session:
        query = select(Course).where(Course.title == course_title)

        query_response = await db_session.execute(query)

        courses = query_response.scalars().all()

        return courses


async def get_user_courses(user_id: int):
    """Get a user's courses"""

    async with session() as db_session:
        query = select(Course).where(Course.user_id == user_id)

        query_response = await db_session.execute(query)

        courses = query_response.scalars().all()

        return courses


async def create_db_course(course: CourseCreate):
    """Create a course"""

    async with session() as db_session:
        query = insert(Course).values(
            title=course.title,
            description=course.description,
            url=course.url,
            user_id=course.user_id,
        )

        await db_session.execute(query)

        await db_session.commit()

        return True


async def patch_db_course(course_id: int, course: CoursePatch):
    """Patch a course"""

    async with session() as db_session:
        query = (
            update(Course)
            .where(Course.id == course_id)
            .values(
                title=course.title,
                description=course.description,
                url=course.url,
            )
        )

        await db_session.execute(query)

        await db_session.commit()

        return


async def delete_db_course(course_id: int):
    """Delete a course"""

    async with session() as db_session:
        query = delete(Course).where(Course.id == course_id)

        await db_session.execute(query)

        await db_session.commit()

        return
