from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.course import CourseCreate


class CreateCourseCollectorInterface(ABC):
    """Create Course Collector Usecase Interface"""

    @abstractmethod
    async def create_course(
        self, db_session: AsyncSession, course: CourseCreate
    ) -> bool:
        """Must implement"""

        raise Exception("Must implement create_course method")
