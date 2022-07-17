from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class FindCourseSectionsCollectorControllerInterface(ABC):
    """Find Course Sections Collector Controller Interface"""

    @abstractmethod
    async def handle(self, db_session: AsyncSession, course_id: str):
        """Method to handle request"""

        raise Exception("Must implement handler method")
