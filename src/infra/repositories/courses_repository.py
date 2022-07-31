from typing import List

from sqlalchemy import literal_column, select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.models.course import Course
from src.domain.models.course import CourseCreate, CoursePatch
from src.data.interfaces.courses_repository import CoursesRepositoryInterface


class CoursesRepository(CoursesRepositoryInterface):
    """Class to courses repository"""

    async def get_courses(
        self, db_session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Course]:
        """Get all courses list"""

        query = select(Course).offset(skip).limit(limit)

        query_response = await db_session.execute(query)

        courses = query_response.scalars().all()

        return courses

    async def get_course_by_id(
        self, db_session: AsyncSession, course_id: int
    ) -> Course:
        """Get a course by id"""

        query = select(Course).where(Course.id == course_id)

        query_response = await db_session.execute(query)

        course = query_response.scalars().first()

        return course

    async def get_course_by_title(
        self, db_session: AsyncSession, course_title: str
    ) -> Course:
        """Get a course by title"""

        query = select(Course).where(Course.title == course_title)

        query_response = await db_session.execute(query)

        course = query_response.scalars().first()

        return course

    async def get_user_courses(
        self, db_session: AsyncSession, user_id: int
    ) -> List[Course]:
        """Get a user's courses"""

        query = select(Course).where(Course.user_id == user_id)

        query_response = await db_session.execute(query)

        courses = query_response.scalars().all()

        return courses

    async def create_db_course(
        self, db_session: AsyncSession, course: CourseCreate
    ) -> Course:
        """Create a course"""

        query = (
            insert(Course)
            .values(
                title=course.title,
                description=course.description,
                url=course.url,
                user_id=course.user_id,
            )
            .returning(literal_column("*"))
        )

        query_response = await db_session.execute(query)

        await db_session.commit()

        created_course = query_response.fetchone()

        return created_course

    async def patch_db_course(
        self, db_session: AsyncSession, course_id: int, course: CoursePatch
    ) -> Course:
        """Patch a course"""

        query = (
            update(Course)
            .where(Course.id == course_id)
            .values(
                title=course.title,
                description=course.description,
                url=course.url,
            )
            .returning(literal_column("*"))
        )

        query_response = await db_session.execute(query)

        await db_session.commit()

        patched_course = query_response.fetchone()

        return patched_course

    async def delete_db_course(self, db_session: AsyncSession, course_id: int) -> None:
        """Delete a course"""

        query = delete(Course).where(Course.id == course_id)

        await db_session.execute(query)

        await db_session.commit()

        return
