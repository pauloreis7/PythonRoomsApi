from typing import List
from faker import Faker
from httpx import AsyncClient

from src.pydantic_schemas.course import Course, CourseCreate, CoursePatch
from src.data.interfaces.courses_repository import CoursesRepositoryInterface

fake = Faker()


class CoursesRepositorySpy(CoursesRepositoryInterface):
    """Spy to courses repository"""

    def __init__(self) -> None:
        self.courses: List[Course] = []
        self.get_courses_attributes = {}
        self.get_course_by_id_attributes = {}
        self.get_course_by_title_attributes = {}
        self.get_user_courses_attributes = {}
        self.create_db_course_attributes = {}
        self.patch_db_course_attributes = {}
        self.delete_db_course_attributes = {}

    async def get_courses(
        self, _: AsyncClient, skip: int = 0, limit: int = 100
    ) -> List[Course]:
        """Get all courses list test"""

        self.get_courses_attributes["skip"] = skip
        self.get_courses_attributes["limit"] = limit

        courses = self.courses

        return courses

    async def get_course_by_id(self, _: AsyncClient, course_id: int) -> Course:
        """Get a course by id test"""

        self.get_course_by_id_attributes["course_id"] = course_id

        check_course_exists = None

        for course in self.courses:
            if course.id == course_id:
                check_course_exists = course
                break

        return check_course_exists

    async def get_course_by_title(self, _: AsyncClient, course_title: str) -> Course:
        """Get a course by title test"""

        self.get_course_by_title_attributes["course_title"] = course_title

        check_course_exists = None

        for course in self.courses:
            if course.title == course_title:
                check_course_exists = course
                break

        return check_course_exists

    async def get_user_courses(self, _: AsyncClient, user_id: int) -> List[Course]:
        """Get a user's courses test"""

        self.get_user_courses_attributes["user_id"] = user_id

        users_courses = []

        for course in self.courses:
            if course.user_id == user_id:
                users_courses.append(course)

        return users_courses

    async def create_db_course(self, _: AsyncClient, course: CourseCreate) -> Course:
        """Create a course test"""

        self.create_db_course_attributes["title"] = course.title
        self.create_db_course_attributes["description"] = course.description
        self.create_db_course_attributes["url"] = course.url
        self.create_db_course_attributes["user_id"] = course.user_id

        fake_course = Course(
            id=fake.random_int(),
            title=course.title,
            description=course.description,
            url=course.url,
            user_id=course.user_id,
            created_at=fake.date_time(),
            updated_at=fake.date_time(),
        )

        self.courses.append(fake_course)

        return fake_course

    async def patch_db_course(
        self, _: AsyncClient, course_id: int, course: CoursePatch
    ) -> Course:
        """Patch a course test"""

        self.patch_db_course_attributes["course_id"] = course_id
        self.patch_db_course_attributes["title"] = course.title
        self.patch_db_course_attributes["description"] = course.description
        self.patch_db_course_attributes["url"] = course.url
        self.patch_db_course_attributes["user_id"] = course.user_id

        fake_course = {
            "title": course.title,
            "description": course.description,
            "url": course.url,
            "user_id": course.user_id,
        }

        for index, course_mock in enumerate(self.courses):
            if course_mock.id == course_id:
                self.courses[index].title = fake_course["title"]
                self.courses[index].description = fake_course["description"]
                self.courses[index].url = fake_course["url"]
                self.courses[index].user_id = fake_course["user_id"]

                break

        return fake_course

    async def delete_db_course(self, _: AsyncClient, course_id: int) -> None:
        """Delete a course test"""

        self.delete_db_course_attributes["course_id"] = course_id

        for index, _ in enumerate(self.courses):
            if self.courses[index].id == course_id:
                del self.courses[index]
                break

        return
