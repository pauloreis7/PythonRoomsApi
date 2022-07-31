from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.course import CoursePatch


class PatchCourseCollectorInterface(ABC):
    """Patch Course Collector Usecase Interface"""

    @abstractmethod
    async def patch_course(
        self, db_session: AsyncSession, course_id: int, course: CoursePatch
    ) -> None:
        """Must implement"""

        raise Exception("Must implement patch_course method")
