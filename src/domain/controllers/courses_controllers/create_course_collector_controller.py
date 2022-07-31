from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.course import CourseCreate


class CreateCourseCollectorControllerInterface(ABC):
    """Create Course Collector Controller Interface"""

    @abstractmethod
    async def handle(self, db_session: AsyncSession, course: CourseCreate):
        """Method to handle request"""

        raise Exception("Must implement handler method")
