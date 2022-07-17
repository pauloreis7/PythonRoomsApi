from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.pydantic_schemas.course import CoursePatch


class PatchCourseCollectorControllerInterface(ABC):
    """Patch Course Collector Controller Interface"""

    @abstractmethod
    async def handle(
        self, db_session: AsyncSession, course_id: int, course: CoursePatch
    ):
        """Method to handle request"""

        raise Exception("Must implement handler method")
