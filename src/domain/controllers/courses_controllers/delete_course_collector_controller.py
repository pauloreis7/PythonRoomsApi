from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class DeleteCourseCollectorControllerInterface(ABC):
    """Delete Course Collector Controller Interface"""

    @abstractmethod
    async def handle(self, db_session: AsyncSession, course_id: int):
        """Method to handle request"""

        raise Exception("Must implement handler method")
