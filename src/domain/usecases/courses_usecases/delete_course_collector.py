from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class DeleteCourseCollectorInterface(ABC):
    """Delete Course Collector Usecase Interface"""

    @abstractmethod
    async def delete_course(self, db_session: AsyncSession, course_id: int) -> None:
        """Must implement"""

        raise Exception("Must implement delete_course method")
