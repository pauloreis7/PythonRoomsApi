from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.pydantic_schemas.course import CourseCreate, CoursePatch
from src.infra.models.course import Course


class CoursesRepositoryInterface(ABC):
    """Courses Repository Interface"""

    @abstractmethod
    async def get_courses(
        self, db_session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Course]:
        """Must implement"""

        raise Exception("Must implement get_courses method")

    @abstractmethod
    async def get_course_by_id(
        self, db_session: AsyncSession, course_id: int
    ) -> Course:
        """Must implement"""

        raise Exception("Must implement get_course_by_id method")

    @abstractmethod
    async def get_course_by_title(
        self, db_session: AsyncSession, course_title: str
    ) -> Course:
        """Must implement"""

        raise Exception("Must implement get_course_by_title method")

    @abstractmethod
    async def get_user_courses(
        self, db_session: AsyncSession, user_id: int
    ) -> List[Course]:
        """Must implement"""

        raise Exception("Must implement get_user_courses method")

    @abstractmethod
    async def create_db_course(
        self, db_session: AsyncSession, course: CourseCreate
    ) -> bool:
        """Must implement"""

        raise Exception("Must implement create_db_course method")

    @abstractmethod
    async def patch_db_course(
        self, db_session: AsyncSession, course_id: int, course: CoursePatch
    ) -> None:
        """Must implement"""

        raise Exception("Must implement patch_db_course method")

    @abstractmethod
    async def delete_db_course(self, db_session: AsyncSession, course_id: int) -> None:
        """Must implement"""

        raise Exception("Must implement delete_db_course method")
